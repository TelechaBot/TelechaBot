# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: Model.py
# @Software: PyCharm
# @Github  :sudoskys
# import binascii
import json
import pathlib
import random
import time

import datetime

# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from Bot.Redis import JsonRedis

from utils.BotTool import botWorker, userStates
# import binascii
from utils import ChatSystem

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def set_delay_del(msgs, second: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        botWorker.delmsg,
        args=[msgs.chat.id, msgs.message_id],
        trigger='date',
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=second)
    )
    scheduler.start()


# 构建多少秒的验证对象
verifyRedis = JsonRedis()


# IO
def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)
        return _csonfig


# IO
def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


# ABOUT
async def About(bot, message, config):
    if message.chat.type == "private":
        if config.desc:
            await bot.reply_to(message, botWorker.convert(config.desc), parse_mode='MarkdownV2')
        else:
            await bot.reply_to(message,
                               "自定义题库的生物信息验证 Bot，Love From Project:https://github.com/TelechaBot/TelechaBot")


# Control
async def Switch(bot, message, config):
    userID = message.from_user.id
    load_csonfig()
    if str(userID) == config.ClientBot.owner:
        try:
            command = message.text
            if command == "/show":
                await bot.reply_to(message, str(_csonfig))
            if command == "/onw":
                _csonfig["whiteGroupSwitch"] = True
                await bot.reply_to(message, "On:whiteGroup")
                save_csonfig()
            if command == "/offw":
                _csonfig["whiteGroupSwitch"] = False
                await bot.reply_to(message, "Off:whiteGroup")
                save_csonfig()
            if command == "/renew":
                from StarPuller import Worker
                Worker().get_index()
                await bot.reply_to(message, "OK..Renew it")
            if command == "/upantispam":
                from utils.ChatSystem import SpamUtils
                await SpamUtils.renewAnti(message)
            if "/cat" in command:
                for item in command.split()[1:]:
                    path = str(pathlib.Path().cwd()) + "/" + item
                    if pathlib.Path(path).exists():
                        doc = open(path, 'rb')
                        await bot.send_document(message.chat.id, doc)
                    else:
                        await bot.reply_to(message, "这个文件没有找到....")

            if "/groupuser" in command:
                import redis
                # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
                task = ChatSystem.ChatUtils().getGroupItem()
                with open('tmp.log', 'w') as f:  # 设置文件对象
                    f.write(str(task))
                doc = open('tmp.log', 'rb')

                await bot.send_document(message.chat.id, doc)
            if "/redis" in command:
                import redis
                # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
                _redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
                Course = _redis.get("_Telecha_Task")
                task = json.loads(Course)
                with open('taskRedis.json', 'w') as f:  # 设置文件对象
                    json.dump(task, f, indent=4, ensure_ascii=False)
                doc = open('taskRedis.json', 'rb')
                await bot.send_document(message.chat.id, doc)
            if "/unban" in command:
                def extract_arg(arg):
                    return arg

                if len(command.split()[1:]) == 2:
                    try:
                        await botWorker.unbanUser(bot, extract_arg(command)[0], extract_arg(command)[1])
                    except Exception as e:
                        await bot.reply_to(message, "发生了错误:\n" + str(e))
                    else:
                        await bot.reply_to(message, "手动解封了" + str(extract_arg(command)))
            if "/addwhite" in command:
                def extract_arg(arg):
                    return arg.split()[1:]

                for group in extract_arg(command):
                    groupId = "".join(list(filter(str.isdigit, group)))
                    _csonfig["whiteGroup"].append(int(groupId))
                    await bot.reply_to(message, '白名单加入了' + str(groupId))
                save_csonfig()
            if "/removewhite" in command:
                def extract_arg(arg):
                    return arg.split()[1:]

                for group in extract_arg(command):
                    groupId = "".join(list(filter(str.isdigit, group)))
                    if int(groupId) in _csonfig["whiteGroup"]:
                        _csonfig["whiteGroup"].remove(int(groupId))
                        await bot.reply_to(message, '白名单移除了' + str(groupId))
                if isinstance(_csonfig["whiteGroup"], list):
                    _csonfig["whiteGroup"] = list(set(_csonfig["whiteGroup"]))
                save_csonfig()

        except Exception as e:
            await bot.reply_to(message, "Wrong:" + str(e))


async def Banme(bot, message, config):
    if len(message.text) == 6:
        if "+banme" == message.text:
            # resign_key = verifyRedis.resign_user(str(message.from_user.id), str(message.chat.id))
            # user_ke = str(resign_key) + " " + str("left") + " " + str(message.from_user.id)
            # user_key = binascii.b2a_hex(user_ke.encode('ascii')).decode('ascii')
            # InviteLink = config.link + "?start=" + str(user_key)
            # bot_link = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
            # bot_link.add(
            #    InlineKeyboardButton("点击这里进行生物验证", url=InviteLink))  # Added Invite Link to Inline Keyboard
            mins = (random.randint(1, 20) * 1)
            user = botWorker.convert(message.from_user.first_name)
            msgs = await bot.reply_to(message,
                                      f"[{user}](tg://openmessage?user_id={message.from_user.id}) "
                                      f"获得了 {mins} 分钟封锁"
                                      # f"答题可以解锁，但是不答题或答错会被踢出群组，等待6分钟\n\n"
                                      f"管理员手动解封请使用 `+unban {message.from_user.id}` ",
                                      # reply_markup=bot_link,
                                      parse_mode='MarkdownV2')
            set_delay_del(msgs, second=10)
            try:
                # userId = "".join(list(filter(str.isdigit, user)))
                # verifyRedis.checker(unban=[key])
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False,
                                               can_send_media_messages=False,
                                               can_send_other_messages=False, until_date=message.date + mins * 60)
            except Exception as e:
                print(e)
                pass


"""
    if "/onantispam" == message.text or ("/onantispam" in message.text and "@" in message.text):
        botWorker.AntiSpam(message.chat.id, True)
        msgs = await bot.reply_to(message, f"启动了AntiSpam反诈系统")
        set_delay_del(msgs, second=12)
    if "/offantispam" == message.text or ("/offantispam" in message.text and "@" in message.text):
        botWorker.AntiSpam(message.chat.id, False)
        msgs = await bot.reply_to(message, f"关闭了AntiSpam反诈系统")
        set_delay_del(msgs, second=12)
"""


class Command(object):
    @staticmethod
    def parseDoorCommand(text: str) -> [list | bool]:
        """
        !set!premium=[level=5|type=on|info=1,3]
        command="11,22",
        }
        :param text:
        :return:
        """
        import re
        table = {}
        allowKey = ["level", "type", "command"]
        key = re.findall(r"!door!(.+?)=", text)
        content = re.findall(r"\[(.+)\]", text)
        if not key:
            return None
        if not content:
            return None
        content = content[0].split("|")
        for item in content:
            command = item.split("=")
            if len(command) == 2:
                keys = command[0]
                tls = command[1]
                if keys in allowKey and len(tls) < 5:
                    if keys in ["level"]:
                        table[keys] = int(''.join(filter(str.isdigit, tls)))
                    else:
                        table[keys] = str(tls)
        return [key[0].strip(), table]


# 群组管理员操作命令
async def Admin(bot, message, config):
    if message.text.strip().startswith('!door!'):
        load_csonfig()
        command = Command.parseDoorCommand(message.text)
        if command:
            _Setting = botWorker.GetGroupStrategy(group_id=message.chat.id)
            if command[0] in botWorker.get_door_strategy().keys():
                if not _Setting["scanUser"].get(command[0]):
                    _Setting["scanUser"][command[0]] = {}
                _Setting["scanUser"][command[0]].update(command[1])
                _csonfig["GroupStrategy"][str(message.chat.id)] = _Setting
                save_csonfig()
            msgs = await bot.reply_to(message, f"设置完毕{command[1]}")
            set_delay_del(msgs, second=24)

    if "/whatstrategy" == message.text or ("/whatstrategy" in message.text and "@" in message.text):
        _Setting = botWorker.GetGroupStrategy(group_id=message.chat.id)
        Config = _Setting["scanUser"]
        info = []
        after_info = []
        Config = dict(sorted(Config.items(), key=lambda x: x[1]["level"], reverse=True))
        for key in Config:
            item = Config[key]
            if item['type'] == "on":
                info.append(f"{key} Use-{item['command']} Status-{item['type']} Level-{item['level']}\n")
            else:
                after_info.append(f"{key} Use-{item['command']} Status-{item['type']} Level-{item['level']}\n")
        info.extend(after_info)
        _types = botWorker.get_door_strategy().keys()
        msgs = await bot.reply_to(message, f"本群验证前策略为\n{''.join(info)} \n Support Type:{','.join(_types)}")

    if "/whatmodel" == message.text or ("/whatmodel" in message.text and "@" in message.text):
        tiku = botWorker.get_model(message.chat.id)
        msgs = await bot.reply_to(message, f"本群题库目前为 {tiku} ")
        set_delay_del(msgs, second=12)

    if "+oncasspam" == message.text or ("+oncasspam" in message.text and "@" in message.text):
        botWorker.casSystem(message.chat.id, True)
        msgs = await bot.reply_to(message, f"启动了CAS反诈系统")
        set_delay_del(msgs, second=12)
    if "+offcasspam" == message.text or ("+offcasspam" in message.text and "@" in message.text):
        botWorker.casSystem(message.chat.id, False)
        msgs = await bot.reply_to(message, f"启动了CAS反诈系统")
        set_delay_del(msgs, second=12)
    if "+select" in message.text and len(message.text) == len("+select"):
        def gen_markup():
            import CaptchaCore
            Get = {}
            for i in CaptchaCore.Importer.getMethod():
                Get.update({i: {'callback_data': i}})
            return quick_markup(Get, row_width=2)

        ti_ku = botWorker.get_model(message.chat.id)
        await bot.reply_to(message, f"选择哪一个题库？目前为{ti_ku}", reply_markup=gen_markup())

    if "+diff_limit" in message.text and len(message.text) != len("+diff_limit"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_limit=level)
            msgs = await bot.reply_to(message, "调整难度上限为:" + str(level))
            set_delay_del(msgs, second=20)
            # t = Timer(20, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            set_delay_del(msgs, second=10)
            # t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
    if "+diff_min" in message.text and len(message.text) != len("+diff_min"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_min=level)
            msgs = await bot.reply_to(message, "调整难度下限为:" + str(level))
            set_delay_del(msgs, second=20)
            # t = Timer(20, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            set_delay_del(msgs, second=10)
            # t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
    if "+unban" in message.text:
        status = message.text.split()[1:]
        for user in status:
            await bot.unban_chat_member(message.chat.id, user_id=user, only_if_banned=True)
            userId = int("".join(list(filter(str.isdigit, user))))
            group, key = verifyRedis.read_user(userId)
            if group:
                # 机器人核心：通过用户注册请求
                await verifyRedis.grant_resign(userId, groupId=group)
                # 解封用户
                await bot.restrict_chat_member(message.chat.id, userId, can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_other_messages=True)
        # 机器人核心：发送通知并自毁消息
        TIPS = await bot.reply_to(message, f"手动解禁:从欧几里得家里解救了{status}")
        set_delay_del(TIPS, second=30)
        # t = Timer(30, botWorker.delmsg, args=[bot, TIPS.chat.id, TIPS.message_id])
        # t.start()
    if "+ban" in message.text:
        status = message.text.split()[1:]
        if len(message.text) == 4:
            try:
                if message.reply_to_message.from_user.id:
                    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)  # .from_user.id)
                    await bot.reply_to(message.reply_to_message,
                                       f'我已经把 {message.reply_to_message.from_user.id} 扭送到璃月警察局了！')
            except:
                pass
        for user in status:
            try:
                await bot.ban_chat_member(message.chat.id, user)
                await bot.reply_to(message.reply_to_message, f'我已经把{user}扭送到璃月警察局了！')
            except Exception as err:
                pass


# 白名单系统
async def botSelf(bot, message, config):
    # if bot is added to group
    # old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member" and message.chat.type != "private":
        load_csonfig()
        await bot.send_message(message.chat.id,
                               "我是璃月科技的生物验证机器人，负责群内新人的生物验证。\n提示:这个 Bot 需要删除消息,封禁用户和邀请用户的权限才能正常行动\n"
                               "请开启新人入群审批，我会自动审批")
        if int(message.chat.id) in _csonfig.get("whiteGroup") or abs(int(message.chat.id)) in _csonfig.get(
                "whiteGroup"):
            pass
            # bot.send_message(message.chat.id,
            #                 "Hello bro! i can use high level problem to verify new chat member~~")
        else:
            if _csonfig.get("whiteGroupSwitch"):
                await bot.send_message(message.chat.id, "检查设置发现群组不在白名单之中！...")
                await bot.leave_chat(message.chat.id)


async def deal_send(bot, message, sth, tip):
    """
    题目库解析
    :param bot:
    :param message:
    :param sth:
    :param tip:
    :return:
    """
    # "\n\n输入 /saveme 重新生成题目，答题后不能重置。"
    if sth[0].get("type") == "text" or sth[0].get("type") is None:
        await bot.reply_to(message,
                           botWorker.convert(
                               sth[0].get("question")) + tip)
    elif sth[0].get("type") == "photo":
        await bot.send_photo(message.chat.id,
                             caption=botWorker.convert(
                                 sth[0].get("question")) + tip,
                             photo=sth[0].get("picture"))
    elif sth[0].get("type") == "voice":
        await bot.send_message(message.chat.id,
                               text=botWorker.convert(sth[0].get(
                                   "question")) + tip)
        await bot.send_voice(message.chat.id, voice=open(sth[0].get("voice_path"), 'rb'),
                             protect_content=True)
    else:
        await bot.reply_to(message, "题库出现了没有标记的类型数据，无法出题")


async def msg_del(bot, message, config):
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        if "bot was kicked" in str(e):
            print("Bot被踢出了群组")
        else:
            print(e)
        pass

    # print(cmu.from_user)  # User : The admin who changed the bot's status
    # print(cmu.old_chat_member)  # ChatMember : The bot's previous status
    # print(cmu.new_chat_member)  # ChatMember : The bot's new status


async def Verify(bot, message, config):
    if message.chat.type == "private":
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            QA = data["QA"]
            group_k = data['Group']
            well_unban = data['BanState']
            times = data['times']
            key = data['key']
        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 veridyRedis 来决定用户去留！
        answers = message.text
        try:
            if str(answers) == str(QA[1].get("rightKey")):
                verify_info = await verifyRedis.grant_resign(message.from_user.id, group_k)
                await bot.reply_to(message, f"好了，您已经被添加进群组了\nPassID {verify_info}")
                # msgs = await botWorker.send_ok(message, bot, group_k, well_unban)
                # aioschedule.every(2).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                #     msgs.message_id * abs(msgs.chat.id))
                # 删除状态
                await bot.delete_state(message.from_user.id, message.chat.id)
            else:
                await bot.reply_to(message, '可惜是错误的回答....你还有一次机会，不能重置')
                await bot.set_state(message.from_user.id, userStates.answer2, message.chat.id)
                # await bot.register_next_step_handler(message, verify_step2, pipe)
        except Exception as e:
            await bot.reply_to(message,
                               f'机器人出错了，请发送日志到项目Issue,或尝试等待队列自然过期再尝试验证\n 日志:`{botWorker.convert(e)}`',
                               parse_mode='MarkdownV2')


async def Verify2(bot, message, config):
    if message.chat.type == "private":
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            QA = data["QA"]
            group_k = data['Group']
            well_unban = data['BanState']
            times = data['times']
            key = data['key']
        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 verifyRedis 来决定用户去留！
        answers = message.text
        try:
            if str(answers) == str(QA[1].get("rightKey")):
                # await botWorker.un_restrict(message, bot, group_k, un_restrict_all=well_unban)
                verify_info = await verifyRedis.grant_resign(message.from_user.id, group_k)
                await bot.reply_to(message, f"好了，您已经被添加进群组了\nPassID {verify_info}")
                # 通知群组
                # msgs = await botWorker.send_ok(message, bot, group_k, well_unban)
                # aioschedule.every(25).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                #     msgs.message_id * abs(msgs.chat.id))
                # 取消状态
                await bot.delete_state(message.from_user.id, message.chat.id)
            else:
                # 取消状态
                await bot.delete_state(message.from_user.id, message.chat.id)
                _, _keys = verifyRedis.create_data(user_id=message.from_user.id, group_id=group_k)
                await verifyRedis.checker(ban=[_keys])
                await bot.reply_to(message, '回答错误')
                # 不通知群组
                # msgs = await botWorker.send_ban(message, bot, group_k)
                # aioschedule.every(360 * 2).seconds.do(botWorker.unbanUser, bot, group_k, message.from_user.id).tag(
                #    message.from_user.id * abs(int(group_k)))
                # aioschedule.every(25).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                #    msgs.message_id * abs(msgs.chat.id))
        except Exception as e:
            await bot.reply_to(message,
                               f'机器人出错了，请发送日志到项目Issue,或尝试等待队列自然过期再尝试验证\n 日志:`{botWorker.convert(e)}`',
                               parse_mode='MarkdownV2')


async def Saveme(bot, message, config):
    """
    重置验证题目状态
    :param bot: 机器人对象
    :param message: 消息对象
    :param config: 配置
    :return: 没有返回
    """
    if message.chat.type == "private":
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            group_k = data['Group']
            QA = data["QA"]
            group_k = data['Group']
            well_unban = data['BanState']
            times = data['times']
        times = times - 1
        if times >= 0:
            min_, limit_ = botWorker.get_difficulty(group_k)
            _model = botWorker.get_model(group_k)
            # from CaptchaCore import __init__
            import CaptchaCore
            paper = (CaptchaCore.Importer(s=time.time()).pull(difficulty_min=min_,
                                                              difficulty_limit=limit_ - 1,
                                                              model_name=_model))
            if times == 0:
                tip = "\n\n输入 /saveme 重新生成题目,必须回答"
            else:
                tip = f"\n\n输入 /saveme 重新生成题目,目前还能生成{times}次"
            # 处理发送题目 paper tip
            await deal_send(bot, message, sth=paper, tip=tip)
            # await bot.delete_state(message.from_user.id, message.chat.id)
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['QA'] = paper
                data['Group'] = group_k
                data['BanState'] = well_unban
                data['times'] = times
                # 注册状态
                await bot.set_state(message.from_user.id, userStates.answer, message.chat.id)


async def Start(bot, message, config):
    if message.chat.type == "private":
        try:
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if data is None:
                    _New_User = True
                else:
                    _New_User = False
        except Exception as e:
            _New_User = True
        group_k, key = verifyRedis.read_user(message.from_user.id)
        if _New_User and group_k:
            # 开始判断
            _seem = f"开始验证群组 `{group_k}`" \
                    f"\n\nPassID:`{key}`" \
                    f"\nAuthID:`{message.from_user.id}`"
            await bot.reply_to(message, _seem, parse_mode='MarkdownV2')
            # 拉取设置信息
            load_csonfig()
            min_, limit_ = botWorker.get_difficulty(group_k)
            model = botWorker.get_model(group_k)
            # 注册状态
            await bot.set_state(message.from_user.id, userStates.answer, message.chat.id)
            # 拉取题目例子
            import CaptchaCore
            sth = CaptchaCore.Importer(s=time.time()).pull(min_, limit_, model_name=model)
            await deal_send(bot, message, sth=sth, tip="\n\n输入 /saveme 重新生成题目，答题后不能重置。")
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['QA'] = sth
                data['Group'] = group_k
                data['BanState'] = False
                data['times'] = 2
                data['key'] = key
                # print("生成了一道题目:" + str(sth))
        else:
            if not _New_User:
                await bot.reply_to(message, "不能重复验证！")
            else:
                pass
                # 防止洪水攻击
                # await bot.reply_to(message, "数据库内没有你的信息哦，你无需验证！")


"""
        code = botWorker.extract_arg(message.text)
        if len(code) == 1:
            PassID = code[0]
            param = binascii.a2b_hex(code[0].encode('ascii')).decode('ascii').split()
            if len(param) == 3:
                key = param[0]
                statu = param[1]
                user_id = param[2]
                if str(user_id) != str(message.from_user.id):
                    group_k = False
                if statu in ["member", "left"]:
                    well_unban = True
"""


async def NewRequest(bot, msg, config):
    # 加载一次设置
    load_csonfig()
    # 白名单参数检查
    WorkOn = await botWorker.checkGroup(bot, msg, config)
    if WorkOn:
        # 记录群组数据
        ChatSystem.ChatUtils().addGroup(msg.chat.id)
        CheckSystem = ChatSystem.UserUtils()
        _chat_info = await bot.get_chat(chat_id=msg.from_user.id)
        pic_id = None
        if _chat_info.photo:
            pic_id = _chat_info.photo.small_file_id
        # 构建画像
        UserThis = {
            "language_code": msg.from_user.language_code,
            "is_bot": msg.from_user.is_bot,
            "is_premium": msg.from_user.is_premium,
            "first_name": msg.from_user.first_name,
            "last_name": msg.from_user.last_name,
            "username": msg.from_user.username,
            "id": msg.from_user.id,
            "photo": pic_id,
            "bio": _chat_info.bio,
            "time": msg.date,
            "token": f"{msg.from_user.first_name}{msg.from_user.last_name}{_chat_info.bio}"
        }
        try:
            Commands = await CheckSystem.Check(bot=bot, userId=msg.from_user.id, groupId=str(msg.chat.id),
                                               UserProfile=UserThis, _csonfig=load_csonfig())
        except Exception as e:
            Commands = {"command": "ask", "info": "error"}
        if Commands.get("command") == "ban":
            # await verifyRedis.checker(fail_user=[msg.from_user.id])
            await bot.decline_chat_join_request(chat_id=str(msg.chat.id), user_id=str(msg.from_user.id))
            await bot.ban_chat_member(chat_id=str(msg.chat.id), user_id=str(msg.from_user.id),
                                      until_date=datetime.datetime.timestamp(
                                          datetime.datetime.now() + datetime.timedelta(minutes=15)))
            await bot.send_message(msg.from_user.id, botWorker.convert(
                f"GroupPolicy{Commands.get('info')}causes Intercept，wait 15～50 min \n "
                f"IF You Think its an Error， report it"),
                                   parse_mode='MarkdownV2')

        elif Commands.get("command") == "pass":
            await bot.approve_chat_join_request(chat_id=str(msg.chat.id), user_id=str(msg.from_user.id))
            await bot.send_message(msg.from_user.id, botWorker.convert(
                f"GroupPolicy{Commands.get('info')}causes AutoMaticPassing"),
                                   parse_mode='MarkdownV2')
        else:
            group_k, key = verifyRedis.read_user(msg.from_user.id)
            if not group_k:
                resign_key = verifyRedis.resign_user(msg.from_user.id, msg.chat.id)
                # 字符处理
                user = botWorker.convert(msg.from_user.id)
                group_name = botWorker.convert(msg.chat.title)
                _info = f"您正在申请加入 `{group_name}`，从现在开始您有 240 秒时间开始验证！如果期间您被管理员拒绝," \
                        f"机器人并不会向您发送通知\n如果中途被其他管理同意，机器人不被通知故不会放行，请手动解禁" \
                        f"\nPassID:`{resign_key}`" \
                        f"\nChatID:`{msg.chat.id}`" \
                        f"\nAuthID:`{user}`" \
                        f"\n按下 \/start 开始验证"
                await bot.send_message(msg.from_user.id, _info, parse_mode='MarkdownV2')
            else:
                _info = f"验证群组 {group_k} 仍未完成"
                await bot.send_message(msg.from_user.id, botWorker.convert(_info), parse_mode='MarkdownV2')
