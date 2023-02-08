# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: Model.py
# @Software: PyCharm
# @Github  :sudoskys

import datetime
import json
import pathlib
import random
import time
from typing import Union
from telebot import types, util
# import telebot.types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from Bot.Redis import JsonRedis
# import binascii
from utils import ChatSystem, DataManager
from utils.BotTool import botWorker, userStates, LogForm
from utils.ChatSystem import TelechaEvaluator, strategyUtils
from utils.DataManager import CommandTable, GroupProfile, DataWorker, User_Data

# 构建多少秒的验证对象
verifyRedis = JsonRedis()
RETRIES = 3


def set_delay_del(msgs, second: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        botWorker.delmsg,
        args=[msgs.chat.id, msgs.message_id],
        trigger='date',
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=second)
    )
    scheduler.start()


global _csonfig
resign_Record = DataWorker(prefix="Telecha_resign_")


# IO
def load_csonfig():
    global _csonfig
    with open("./Config/config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)
        return _csonfig


# IO
def save_csonfig():
    with open("./Config/config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


# ABOUT
async def About(bot, message, config):
    if message.chat.type == "private":
        if "desc" in config.keys():
            await bot.reply_to(message, botWorker.convert(config.desc), parse_mode='MarkdownV2')
        else:
            await bot.reply_to(message, "自定义题库的生物信息验证 Bot，"
                                        "Love From Project:https://github.com/TelechaBot/TelechaBot")


# Control
async def Switch(bot, message, config):
    load_csonfig()
    if str(message.from_user.id) == config.ClientBot.owner:
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

            # if "/groupuser" in command:
            #     import redis
            #     # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
            #     task = ChatSystem.ChatUtils().getGroupItem()
            #     with open('tmp.log', 'w') as f:  # 设置文件对象
            #         f.write(str(task))
            #     doc = open('tmp.log', 'rb')
            #     await bot.send_document(message.chat.id, doc)

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
                    _csonfig["whiteGroup"].append(str(groupId))
                    await bot.reply_to(message, 'White Group Added' + str(groupId))
                save_csonfig()
            if "/removewhite" in command:
                def extract_arg(arg):
                    return arg.split()[1:]

                for group in extract_arg(command):
                    groupId = "".join(list(filter(str.isdigit, group)))
                    if int(groupId) in _csonfig["whiteGroup"]:
                        _csonfig["whiteGroup"].remove(str(groupId))
                        await bot.reply_to(message, 'White Group Removed ' + str(groupId))
                if isinstance(_csonfig["whiteGroup"], list):
                    _csonfig["whiteGroup"] = list(set(_csonfig["whiteGroup"]))
                save_csonfig()
        except Exception as e:
            logger.error(e)
            await bot.reply_to(message, "Error:" + str(e))


async def Group_User(bot, message, config):
    if "/banme" == message.text or ("/banme@" in message.text):
        _min = (random.randint(1, 20) * 1)
        user = botWorker.convert(message.from_user.first_name)
        msgs = await bot.reply_to(message,
                                  f"好的... [{user}](tg://openmessage?user_id={message.from_user.id}) "
                                  f"获得了 {_min} 分钟封锁",
                                  parse_mode='MarkdownV2')
        set_delay_del(msgs, second=25)
        try:
            await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False,
                                           can_send_media_messages=False,
                                           can_send_other_messages=False, until_date=message.date + _min * 60)
        except Exception as e:
            logger.error(e)


class Command(object):
    """
    命令解析器
    """

    @staticmethod
    def parseDoorCommand(text: str) -> Union[list, bool]:
        """
        !set!premium=[level=5|type=on|info=1,3]
        command="11,22",
        }
        :param text:
        :return:
        """
        import re
        table = {}
        allowKey = {"level": 8, "type": 8, "command": 8, "flag": 50}
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
                # 检查非法键和组合长度
                if keys in allowKey.keys():
                    if len(tls) < allowKey.get(keys):
                        if keys in ["level"]:
                            table[keys] = int(''.join(filter(str.isdigit, tls)))
                        else:
                            table[keys] = str(tls)
        return [key[0].strip(), table]


# 群组管理员操作命令
async def Admin(bot, message, config):
    """
    管理员命令
    :param bot: 机器人
    :param message: 消息对象
    :param config: 配置
    :return:
    """

    # Door
    if message.text.strip().startswith('!door!'):
        command = Command.parseDoorCommand(message.text)
        if command:
            _update = {command[0]: command[1]}
            # 检查非法指令
            if command[0] in CommandTable.GroupStrategy_default_door_strategy().keys():
                if strategyUtils(groupId=message.chat.id).setDoorStrategy(key=_update):
                    _reply = f"设置完毕{command[1]}"
                else:
                    _reply = f"设置失败{command[1]}"
                msgs = await bot.reply_to(message, _reply)
                set_delay_del(msgs, second=24)

    # What Strategy
    if "/whatstrategy" == message.text or ("/whatstrategy" in message.text and "@" in message.text):
        _Setting = strategyUtils(groupId=message.chat.id).getDoorStrategy()
        Config = _Setting
        info = []
        after_info = []
        Config = dict(sorted(Config.items(), key=lambda x: x[1]["level"], reverse=True))
        for key in Config:
            item = Config[key]
            _info = f"{key} Use-{item['command']} Status-{item['type']} Level-{item['level']}\n"
            if item['type'] == "on":
                info.append(_info)
            else:
                after_info.append(_info)
        info.extend(after_info)
        _types = CommandTable.GroupStrategy_default_door_strategy().keys()
        msgs = await bot.reply_to(message, f"本群入群策略为\n{''.join(info)} \n Support Type:{','.join(_types)}")

    if "/whatmodel" == message.text or ("/whatmodel" in message.text and "@" in message.text):
        tiku = botWorker.get_model(message.chat.id)
        msgs = await bot.reply_to(message, f"本群题库目前为 {tiku} ")
        set_delay_del(msgs, second=12)

    if any(["/select" == message.text, ("/select@" in message.text),
            "/choose" == message.text, ("/choose@" in message.text)]):
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
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            set_delay_del(msgs, second=10)

    if "+diff_min" in message.text and len(message.text) != len("+diff_min"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_min=level)
            msgs = await bot.reply_to(message, "调整难度下限为:" + str(level))
            set_delay_del(msgs, second=20)
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            set_delay_del(msgs, second=10)

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
        TIPS = await bot.reply_to(message, f"Unban: {status}")
        set_delay_del(TIPS, second=30)

    if "+ban" in message.text:
        status = message.text.split()[1:]
        if len(message.text) == 4:
            try:
                if message.reply_to_message.from_user.id:
                    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)  # .from_user.id)
                    await bot.reply_to(message.reply_to_message,
                                       f'Good Bye, {message.reply_to_message.from_user.id} was kicked!')
            except:
                pass
        for user in status:
            try:
                await bot.ban_chat_member(message.chat.id, user)
                await bot.reply_to(message.reply_to_message, f'Good Bye, {user} was kicked！')
            except Exception as err:
                pass


# 白名单系统
async def botSelf(bot, message, config):
    # if bot is added to group
    # old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member" and message.chat.type != "private":
        load_csonfig()
        try:
            await bot.send_message(message.chat.id,
                                   "我是璃月科技的生物验证机器人，负责群内新人的生物验证。\n提示:这个 Bot 需要删除消息,封禁用户和邀请用户的权限才能正常行动\n"
                                   "请开启新人入群审批，我会自动审批")
        except:
            pass
        if str(message.chat.id) in _csonfig.get("whiteGroup"):
            pass
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
                           sth[0].get("question") + tip,
                           )
    elif sth[0].get("type") == "photo":
        await bot.send_photo(message.chat.id,
                             caption=sth[0].get("question") + tip,
                             photo=sth[0].get("picture"),
                             )
    elif sth[0].get("type") == "voice":
        await bot.send_message(message.chat.id,
                               text=sth[0].get("question") + tip)
        await bot.send_audio(message.chat.id, audio=open(sth[0].get("voice_path"), 'rb'))
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
        data_raw = resign_Record.getKey(f"{message.from_user.id}_data")
        if data_raw:
            data = User_Data(**data_raw)
            group_k = data.Group
            QA = data.QaPair
            UUID = data.UUID
        else:
            logger.error(f"Bad Verify")
            return
        answers = message.text
        try:
            if str(answers) == str(QA[1].get("rightKey")):
                resign_Record.setKey(f"{message.from_user.id}", message.chat.id, exN=1)
                await bot.delete_state(message.from_user.id, message.chat.id)
                #
                verify_info = await verifyRedis.grant_resign(message.from_user.id, int(group_k))
                await LogForm(bot=bot, logChannel=config.logChannel).send(tag="#Pass",
                                                                          user=UUID,
                                                                          group=int(group_k)
                                                                          )
                #
                logger.info(f"通过了 {message.from_user.id}{group_k} --title {message.from_user.last_name}")
                await bot.reply_to(message, f"好了，您已经被添加进群组了\nPassID {verify_info}")
                # msgs = await botWorker.send_ok(message, bot, group_k, well_unban)
            else:
                resign_Record.setKey(f"{message.from_user.id}", message.chat.id, exN=1)
                await bot.delete_state(message.from_user.id, message.chat.id)
                #
                _, _keys = verifyRedis.create_data(user_id=message.from_user.id, group_id=group_k)
                await verifyRedis.checker(ban=[_keys])
                await LogForm(bot=bot, logChannel=config.logChannel).send(tag="#Unpass ",
                                                                          user=UUID,
                                                                          group=int(group_k)
                                                                          )
                await bot.reply_to(message, '回答错误')
        except Exception as e:
            logger.error(f"{message.from_user.id}-{e}")
            try:
                await bot.reply_to(message,
                                   f'机器人出错了，请发送日志到项目Issue,或尝试等待队列自然过期再尝试验证\n 日志:`{botWorker.convert(e)}`',
                                   parse_mode='MarkdownV2')
            except Exception as e:
                pass


async def Saveme(bot, message, config):
    """
    重置验证题目状态
    :param bot: 机器人对象
    :param message: 消息对象
    :param config: 配置
    :return: 没有返回
    """
    if message.chat.type == "private":
        data_raw = resign_Record.getKey(f"{message.from_user.id}_data")
        if data_raw:
            data = User_Data(**data_raw)
            group_k = data.Group
            times = data.Times
            times = times - 1
            if times >= 0:
                import CaptchaCore
                _model = botWorker.get_model(group_k)
                min_, limit_ = botWorker.get_difficulty(group_k)
                _Question, _Answer = CaptchaCore.Importer(s=time.time()).pull(min_, limit_, model_name=_model)
                QAPair = [_Question, _Answer]
                if times == 0:
                    tip = "\n\n输入 /saveme 重新生成题目,必须回答"
                else:
                    tip = f"\n\n输入 /saveme 重新生成题目,目前还能生成{times}次"
                # 处理发送题目 paper tip
                await deal_send(bot, message, sth=QAPair, tip=tip)
                # await bot.delete_state(message.from_user.id, message.chat.id)
                new_data = {'QaPair': QAPair, 'Group': group_k, 'Times': times}
                _now = data.dict()
                _now.update(new_data)
                resign_Record.setKey(f"{message.from_user.id}_data", User_Data(**_now).dict(), exN=500)
                await bot.set_state(message.from_user.id, userStates.answer, message.chat.id)


async def Start(bot, message, config):
    """
    start 命令拦截
    :param bot: 机器人对象
    :param message: 消息对象
    :param config: 配置
    :return:
    """
    if message.chat.type == "private":
        _New_User = True
        group_k, UUID = verifyRedis.read_user(message.from_user.id)
        if resign_Record.getKey(f"{message.from_user.id}") == group_k:
            _New_User = False
        if _New_User and group_k:
            status, result = await PrepareCheck(bot, message, userId=message.from_user.id, groupId=group_k)
            if status:
                await LogForm(bot=bot, logChannel=config.logChannel).send(
                    tag=f"{result} \n 自动策略处理",
                    user=UUID,
                    group=group_k
                )
                logger.info(f"PerCheck: {message.from_user.id}{group_k} --user {message.from_user.last_name}")
            else:
                # 开始判断
                _seem = f"开始验证群组 {group_k}" \
                        f"\n\nPassID #U{UUID}" \
                        f"\nAuthID {message.from_user.id}"
                await bot.reply_to(message, _seem)
                # 拉取设置信息
                load_csonfig()
                min_, limit_ = botWorker.get_difficulty(group_k)
                model = botWorker.get_model(group_k)
                resign_Record.setKey(f"{message.from_user.id}", group_k, exN=300)
                # 拉取题目例子
                import CaptchaCore
                Question, Answer = CaptchaCore.Importer(s=time.time()).pull(min_, limit_, model_name=model)
                QAPair = [Question, Answer]
                await deal_send(bot, message, sth=QAPair, tip="\n\n输入 /saveme 重新生成题目.")
                data = {'QaPair': QAPair, 'Group': group_k, 'Times': RETRIES, "UUID": str(UUID)}
                resign_Record.setKey(f"{message.from_user.id}_data", User_Data(**data).dict(), exN=500)
                # 注册状态
                await bot.set_state(message.from_user.id, userStates.answer, message.chat.id)
        else:
            if not _New_User:
                await bot.reply_to(message, "NO duplicate Verification!")
            else:
                await bot.reply_to(message, "NO ongoing verification tasks")
                # pass
                # 防止洪水攻击


async def NewRequest(bot, msg: types.Message, config):
    """
    处理新请求
    :param bot: 机器人对象
    :param msg: 消息对象
    :param config: 设置
    :return:
    """
    # 加载一次设置
    load_csonfig()
    logger.info(f"NewReq:{msg.from_user.id}:{msg.chat.id} --user {msg.from_user.last_name} --title {msg.chat.title}")
    WorkOn = await botWorker.checkGroup(bot, msg, config)
    if WorkOn:
        group_k, UUID = verifyRedis.read_user(msg.from_user.id)
        if not group_k:
            UUID = verifyRedis.resign_user(msg.from_user.id, msg.chat.id)
            # 字符处理
            user = botWorker.convert(msg.from_user.id)
            group_name = botWorker.convert(msg.chat.title)
            _info = f"您正在申请加入 `{group_name}` " \
                    f"\nAuthID `{user}`" \
                    f"\nChatID `{msg.chat.id}`" \
                    f"\nPassID `{UUID}`" \
                    f"\n从现在开始您有 240 秒时间开始验证！如果期间您被管理员拒绝或同意,机器人并不会向您发送通知" \
                    f"\n按下 \/start 开始验证"
            try:
                await bot.send_message(msg.from_user.id, _info, parse_mode='MarkdownV2')
            except Exception as e:
                logger.error(f"InitRequest:{e}")
                await LogForm(bot=bot, logChannel=config.logChannel).send(
                    tag=f"#UnreachableRequest \n{msg.chat.title}",
                    user=UUID,
                    group=msg.chat.id
                )
            else:
                await LogForm(bot=bot, logChannel=config.logChannel).send(tag=f"#Request \n{msg.chat.title}",
                                                                          user=UUID,
                                                                          group=msg.chat.id
                                                                          )
        else:
            _info = f"验证群组 {group_k} 仍未完成"
            await bot.send_message(msg.from_user.id, botWorker.convert(_info), parse_mode='MarkdownV2')


async def PrepareCheck(bot, msg, userId, groupId) -> tuple:
    """
    预先检查
    :param bot: 机器人对象
    :param msg: 消息
    :param userId: 用户ID
    :param groupId: 群组ID
    :return: 是否被处理
    """
    try:
        _chat_info = await bot.get_chat(chat_id=userId)
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
            "name": f"{msg.from_user.first_name}{msg.from_user.last_name}",
            "username": msg.from_user.username,
            "id": userId,
            "photo": pic_id,
            "bio": _chat_info.bio,
            "time": msg.date,
            "token": f"{msg.from_user.first_name}{msg.from_user.last_name}{_chat_info.bio}"
        }
        # Commands = {"command": "error", "info": "error"}
        Commands = await TelechaEvaluator(groupId=groupId, userId=userId).checkUser(bot=bot,
                                                                                    UserProfileData=DataManager.UserProfile(
                                                                                        **UserThis),
                                                                                    _csonfig=load_csonfig())
    except Exception as e:
        print(e)
        Commands = {"level": 1, "command": "error", "type": "on", "info": e}
    # RUN
    if not Commands:
        return False, "#None"
    elif Commands.get("command") == "ban":
        # await verifyRedis.checker(fail_user=[msg.from_user.id])
        _, _keys = verifyRedis.create_data(user_id=userId, group_id=groupId)
        await verifyRedis.checker(ban=[_keys])
        try:
            await bot.send_message(userId, botWorker.convert(
                f"GroupPolicy {Commands.get('info')}causes Intercept，wait 15～50 min \n "
                f"IF You Think its an Error， report it"),
                                   parse_mode='MarkdownV2')
        except:
            pass
        return True, "#AutoBan"
    elif Commands.get("command") == "pass":
        _, _keys = verifyRedis.create_data(user_id=userId, group_id=groupId)
        await verifyRedis.checker(unban=[_keys])
        try:
            await bot.send_message(userId, botWorker.convert(
                f"GroupPolicy {Commands.get('info')}causes AutoMaticPassing"),
                                   parse_mode='MarkdownV2')
        except:
            pass
        return True, "#AutoPass"
    else:
        return False, ""
