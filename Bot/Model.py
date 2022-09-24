# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: Model.py
# @Software: PyCharm
# @Github    ：sudoskys
import ast
import json
import pathlib
import random
import time

import aioschedule
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from Bot.Redis import JsonRedis

from utils.BotTool import botWorker, userStates
import binascii
from utils import ChatSystem

# 构建多少秒的验证对象


verifyRedis = JsonRedis(200)


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
            await bot.reply_to(message, config.desc)
        else:
            await bot.reply_to(message, "自定义题库的生物信息验证 Bot，Love From Project:https://github.com/TelechaBot/TelechaBot")


# 主控模块
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
                from utils.ChatSystem import UserUtils
                await UserUtils.renewAnti(message)
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
                r = redis.Redis(host='localhost', port=6379, decode_responses=True)
                task = r.get('tasks')
                task = ast.literal_eval(task)
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
            mins = (random.randint(1, 15) * 1)
            user = botWorker.convert(message.from_user.first_name)
            msgs = await bot.reply_to(message,
                                      f"[{user}](tg://openmessage?user_id={message.from_user.id}) "
                                      f"获得了 {mins} 分钟封锁"
                                      # f"答题可以解锁，但是不答题或答错会被踢出群组，等待6分钟\n\n"
                                      f"管理员手动解封请使用 `+unban {message.from_user.id}` ",
                                      # reply_markup=bot_link,
                                      parse_mode='MarkdownV2')
            aioschedule.every(60).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                msgs.message_id * abs(msgs.chat.id))
            try:
                # userId = "".join(list(filter(str.isdigit, user)))
                # verifyRedis.checker(tar=[key])
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False,
                                               can_send_media_messages=False,
                                               can_send_other_messages=False, until_date=message.date + mins * 60)
            except Exception as e:
                print(e)
                pass


# 群组管理员操作命令
async def Admin(bot, message, config):
    if "/whatmodel" == message.text or ("/whatmodel" in message.text and "@" in message.text):
        tiku = botWorker.get_model(message.chat.id)
        msgs = await bot.reply_to(message, f"本群题库目前为 {tiku} ")
        aioschedule.every(12).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
    if "/onantispam" == message.text or ("/onantispam" in message.text and "@" in message.text):
        botWorker.AntiSpam(message.chat.id, True)
        msgs = await bot.reply_to(message, f"启动了AntiSpam反诈系统")
        aioschedule.every(12).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
    if "/offantispam" == message.text or ("/offantispam" in message.text and "@" in message.text):
        botWorker.AntiSpam(message.chat.id, False)
        msgs = await bot.reply_to(message, f"关闭了AntiSpam反诈系统")
        aioschedule.every(12).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
    if "+oncasspam" == message.text or ("+oncasspam" in message.text and "@" in message.text):
        botWorker.casSystem(message.chat.id, True)
        msgs = await bot.reply_to(message, f"启动了CAS反诈系统")
        aioschedule.every(12).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
    if "+offcasspam" == message.text or ("+offcasspam" in message.text and "@" in message.text):
        botWorker.casSystem(message.chat.id, False)
        msgs = await bot.reply_to(message, f"启动了CAS反诈系统")
        aioschedule.every(12).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
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
            aioschedule.every(20).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                msgs.message_id * abs(msgs.chat.id))
            # t = Timer(20, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            aioschedule.every(10).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                msgs.message_id * abs(msgs.chat.id))
            # t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
    if "+diff_min" in message.text and len(message.text) != len("+diff_min"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_min=level)
            msgs = await bot.reply_to(message, "调整难度下限为:" + str(level))
            aioschedule.every(20).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                msgs.message_id * abs(msgs.chat.id))
            # t = Timer(20, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
        else:
            msgs = await bot.reply_to(message, "无效参数,必须为数字")
            aioschedule.every(10).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                msgs.message_id * abs(msgs.chat.id))
            # t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            # t.start()
    if "+unban" in message.text:
        status = message.text.split()[1:]
        for user in status:
            await bot.unban_chat_member(message.chat.id, user_id=user, only_if_banned=True)
            userId = "".join(list(filter(str.isdigit, user)))
            group, key = verifyRedis.read_user(str(userId))
            if group:
                # 机器人核心：通过用户注册请求
                await verifyRedis.grant_resign(userId, groupId=group)
                # 解封用户
                await bot.restrict_chat_member(message.chat.id, userId, can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_other_messages=True)
        # 机器人核心：发送通知并自毁消息
        TIPS = await bot.reply_to(message, "手动解禁:从欧几里得家里解救了" + str(status))
        aioschedule.every(30).seconds.do(botWorker.delmsg, TIPS.chat.id, TIPS.message_id).tag(
            TIPS.message_id * abs(TIPS.chat.id))
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
                await bot.send_message(message.chat.id,
                                       "检查设置发现群组不在白名单之中！...")
                await bot.leave_chat(message.chat.id)


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


async def NewRequest(bot, msg, config):
    load_csonfig()
    # print(msg)
    checkOK = await botWorker.checkGroup(bot, msg, config)
    if checkOK:
        ChatSystem.ChatUtils().addGroup(str(msg.chat.id))
        checkObj = str(msg.from_user.first_name) + str(msg.from_user.last_name)
        AntiSpamSystem = ChatSystem.UserUtils()
        IsSpam = await AntiSpamSystem.checkUser(userId=str(msg.from_user.id), info=checkObj, _csonfig=load_csonfig())
        if not IsSpam:
            resign_key = verifyRedis.resign_user(str(msg.from_user.id), str(msg.chat.id))
            user = botWorker.convert(msg.from_user.id)
            group_name = botWorker.convert(msg.chat.title)
            info = f"您正在申请加入 `{group_name}`，从现在开始您有 200 秒时间开始验证！如果期间您被管理员拒绝,机器人并不会向您发送通知\n如果中途被其他管理同意，机器人不被通知故不会放行，请手动解禁" \
                   f"\nPassID:`{resign_key}`" \
                   f"\n群组ID:`{msg.chat.id}`" \
                   f"\n您的标识符是:`{user}`" \
                   f"\n按下 \/start 开始验证"
            await bot.send_message(msg.from_user.id, botWorker.convert(info),
                                   parse_mode='MarkdownV2')
        else:
            AntiSpamSystem.addSpamUser(groupId=str(msg.chat.id), userId=str(msg.from_user.id))
            await bot.decline_chat_join_request(chat_id=str(msg.chat.id), user_id=str(msg.from_user.id))
            # await verifyRedis.checker(fail_user=[msg.from_user.id])
            info = "当前群组开启了 Spam 过滤，您的身份不符合设定或数据库记录仍未消除，请等待 Spam 键值对过期，大约几天，为你带来了烦扰很抱歉！"
            await bot.send_message(msg.from_user.id, botWorker.convert(info),
                                   parse_mode='MarkdownV2')


# 此函数已经不再使用！
# 启动新用户通知
async def member_update(bot, msg, config):
    # if msg.left_chat_member.id != bot.get_me().id:
    old = msg.old_chat_member
    new = msg.new_chat_member
    load_csonfig()

    async def verify_user(bot, config, statu):
        # 用户操作
        resign_key = verifyRedis.resign_user(str(new.user.id), str(msg.chat.id))
        user_ke = str(resign_key) + " " + str(statu) + " " + str(new.user.id)
        user_key = binascii.b2a_hex(user_ke.encode('ascii')).decode('ascii')
        InviteLink = config.link + "?start=" + str(user_key)
        # print(InviteLink)
        bot_link = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        bot_link.add(
            InlineKeyboardButton("点这里进行生物验证", url=InviteLink))  # Added Invite Link to Inline Keyboard
        user = botWorker.convert(new.user.first_name)
        group_name = botWorker.convert(msg.chat.title)
        info = f"[{user}](tg://openmessage?user_id={new.user.id}) 正在申请加入 `{group_name}`" \
               f"\nPassID:`{botWorker.convert(user_key)}`" \
               f"\n群组ID:`{botWorker.convert(msg.chat.id)}`" \
               f"\n赫免命令`+unban {new.user.id}`"
        try:
            msgss = await bot.send_message(msg.chat.id,
                                           info,
                                           reply_markup=bot_link,
                                           parse_mode='MarkdownV2')
        except Exception as e:
            print(e)
            msgss = await bot.send_message(msg.chat.id,
                                           info,
                                           reply_markup=bot_link,
                                           parse_mode='MarkdownV2')
        aioschedule.every(60).seconds.do(botWorker.delmsg, msgss.chat.id, msgss.message_id).tag(
            msgss.message_id * abs(msgss.chat.id))
        # t = Timer(88, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
        # t.start()
        try:
            await bot.restrict_chat_member(msg.chat.id, new.user.id, can_send_messages=False,
                                           can_send_media_messages=False,
                                           can_send_other_messages=False)
        except Exception as e:
            print(e)
            no_power = await bot.send_message(msg.chat.id,
                                              f"对不起，没有权限执行对新用户 `{new.user.id}` 的限制\nPassID: `{user_key}` \nGroupID:`{msg.chat.id}`",
                                              parse_mode='HTML')
            aioschedule.every(6).seconds.do(botWorker.delmsg, no_power.chat.id, no_power.message_id).tag(
                no_power.message_id * abs(no_power.chat.id))
            # t = Timer(6, botWorker.delmsg, args=[bot, no_power.chat.id, no_power.message_id])
            # t.start()

    iss, info_ = botWorker.new_member_checker(msg)
    if info_ is not None:
        # ID = info.get("id")
        # Group = info.get("group")
        # await bot.restrict_chat_member(Group, ID, can_send_messages=False,
        #                                can_send_media_messages=False,
        #                                can_send_other_messages=False)
        # 在回调函数中我们无法对返回的数据做管理员校验处理，所以禁用了此功能
        # def bot_verify():
        #     markup = InlineKeyboardMarkup()
        #     markup.row_width = 1
        #     markup.add(
        #         InlineKeyboardButton("通过同类", callback_data=f"Pass+{Group}+{ID}"),
        #         InlineKeyboardButton("踢出同类", callback_data=f"Ban+{Group}+{ID}"),
        #     )
        #     return markup

        msgs = await bot.send_message(msg.chat.id, botWorker.convert(info_.get("text")))  # , reply_markup=bot_verify())
        aioschedule.every(8).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
            msgs.message_id * abs(msgs.chat.id))
    if iss:
        print(str(new.user.id) + "加入了" + str(msg.chat.id))
        if _csonfig.get("whiteGroupSwitch"):
            if int(msg.chat.id) in _csonfig.get("whiteGroup") or abs(int(msg.chat.id)) in _csonfig.get(
                    "whiteGroup"):
                await verify_user(bot, config, old.status)
            else:
                if hasattr(config.ClientBot, "contact_details"):
                    contact = botWorker.convert(config.ClientBot.contact_details)
                else:
                    contact = "There is no reserved contact information."
                await bot.send_message(msg.chat.id,
                                       f"Bot开启了白名单模式，有人将我添加到此群组，但该群组不在我的白名单中...."
                                       f"请向所有者申请权限...."
                                       f"\nContact details:{contact}"
                                       f'添加白名单命令:`/addwhite {msg.chat.id}`',
                                       parse_mode='HTML')
                await bot.leave_chat(msg.chat.id)
        else:
            await verify_user(bot, config, old.status)
        # 启动验证流程
    if new.status in ["left", 'kicked',
                      "restricted"] and not msg.old_chat_member.is_member and not msg.from_user.is_bot:
        # 注销任务
        if new.status in ["kicked", "left"]:
            print(str(new.user.id) + "离开了" + str(msg.chat.id))
            await verifyRedis.remove_user(new.user.id, str(msg.chat.id))
            try:
                await bot.delete_state(new.user.id, msg.chat.id)
            except Exception as e:
                pass
            # bot.ban_chat_member(msg.chat.id, user_id=new.user.id)


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
                await bot.reply_to(message, f"好了，您已经被添加进群组了\nPassID{verify_info}")
                # 通知群组
                msgs = await botWorker.send_ok(message, bot, group_k, well_unban)
                aioschedule.every(25).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                    msgs.message_id * abs(msgs.chat.id))
                # 取消状态
                await bot.delete_state(message.from_user.id, message.chat.id)
            else:
                await verifyRedis.checker(fail_user=[key])
                await bot.reply_to(message, '可惜是错误的回答....你12分钟后才能再次进入群组')
                # 通知群组
                msgs = await botWorker.send_ban(message, bot, group_k)
                aioschedule.every(360).seconds.do(botWorker.unbanUser, bot, msgs.chat.id, message.from_user.id).tag(
                    message.from_user.id * abs(msgs.chat.id))
                aioschedule.every(25).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                    msgs.message_id * abs(msgs.chat.id))
                # 取消状态
                await bot.delete_state(message.from_user.id, message.chat.id)
        except Exception as e:
            await bot.reply_to(message, f'机器人出错了，请发送日志到项目Issue,谢谢你！\n 日志:`{botWorker.convert(e)}`',
                               parse_mode='MarkdownV2')


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
                await bot.reply_to(message, f"好了，您已经被添加进群组了\nPassID{verify_info}")
                msgs = await botWorker.send_ok(message, bot, group_k, well_unban)
                aioschedule.every(25).seconds.do(botWorker.delmsg, msgs.chat.id, msgs.message_id).tag(
                    msgs.message_id * abs(msgs.chat.id))
                # 删除状态
                await bot.delete_state(message.from_user.id, message.chat.id)
            else:
                await bot.reply_to(message, '可惜是错误的回答....你还有一次机会，不能重置')
                await bot.set_state(message.from_user.id, userStates.answer2, message.chat.id)
                # await bot.register_next_step_handler(message, verify_step2, pipe)
        except Exception as e:
            await bot.reply_to(message, f'机器人出错了，请发送日志到项目Issue,谢谢你！\n 日志:`{botWorker.convert(e)}`',
                               parse_mode='MarkdownV2')


async def Saveme(bot, message, config):
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
            import CaptchaCore
            if times == 0:
                tip = f"必须回答"
            else:
                tip = f"目前还能生成{times}次"
            if paper[0].get("picture") is None:
                await bot.reply_to(message,
                                   botWorker.convert(paper[0].get("question")) + f"\n\n输入 /saveme 重新生成题目,{tip}")
            else:
                await bot.send_photo(message.chat.id, caption=botWorker.convert(
                    paper[0].get("question")) + f"\n\n输入 /saveme 重新生成题目,{tip}",
                                     photo=paper[0].get("picture"))
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
                # print(Data)
                if data is None:
                    New = True
                else:
                    New = False
        except Exception as e:
            New = True
        if New:
            # 读取用户
            group_k, key = verifyRedis.read_user(str(message.from_user.id))
            PassID = key
            well_unban = False
            # 如果有参数，进行解码覆盖
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

            # 开始判断
            info = f"开始验证群组 `{group_k}`,你有总 200 秒的时间回答下面的问题" \
                   f"\n\nPassID:`{PassID}`" \
                   f"\nAuthID:`{message.from_user.id}`"
            if group_k:
                await bot.reply_to(message,
                                   botWorker.convert(info),
                                   parse_mode='MarkdownV2')
                load_csonfig()
                # 拉取设置信息
                min_, limit_ = botWorker.get_difficulty(group_k)
                model = botWorker.get_model(group_k)

                # 拉取题目例子
                import CaptchaCore
                sth = CaptchaCore.Importer(s=time.time()).pull(min_, limit_, model_name=model)
                if sth[0].get("picture") is None:
                    await bot.reply_to(message,
                                       botWorker.convert(sth[0].get("question")) + f"\n\n输入 /saveme 重新生成题目，答题后不能重置。")
                else:
                    await bot.send_photo(message.chat.id,
                                         caption=botWorker.convert(
                                             sth[0].get("question")) + "\n\n输入 /saveme 重新生成题目，答题后不能重置。",
                                         photo=sth[0].get("picture"))
                # 注册状态
                await bot.set_state(message.from_user.id, userStates.answer, message.chat.id)
                async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['QA'] = sth
                    data['Group'] = group_k
                    data['BanState'] = well_unban
                    data['times'] = 2
                    data['key'] = key
                # print("生成了一道题目:" + str(sth))
            else:
                await bot.reply_to(message, "数据库内没有你的信息哦，你无需验证！")
        else:
            await bot.reply_to(message, "不能重复验证！")
    else:
        pass
    # print(0)
