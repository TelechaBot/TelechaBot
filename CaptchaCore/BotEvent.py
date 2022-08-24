# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import pathlib

from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotRedis import JsonRedis
from threading import Timer
from CaptchaCore.Event import botWorker

# from telebot import formatting


# 构建多少秒的验证对象
verifyRedis = JsonRedis(175)


# 全局加载配置
def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


# 存储全局配置
def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


# 关于
def About(bot, config):
    @bot.message_handler(commands=['about'])
    def send_about(message):
        if message.chat.type == "private":
            if config.desc:
                bot.reply_to(message, config.desc)
            else:
                bot.reply_to(message, "生物信息验证 Bot，自主Project:https://github.com/sudoskys/")


# 主控模块
def Switch(bot, config):
    @bot.message_handler(content_types=['text'])
    def masters(message, items=None):
        userID = message.from_user.id
        load_csonfig()
        if str(userID) == config.ClientBot.owner:
            try:
                command = message.text
                if command == "/show":
                    bot.reply_to(message, str(_csonfig))
                if command == "/onw":
                    _csonfig["whiteGroupSwitch"] = True
                    bot.reply_to(message, "On:whiteGroup")
                    save_csonfig()
                if command == "/offw":
                    _csonfig["whiteGroupSwitch"] = False
                    bot.reply_to(message, "Off:whiteGroup")
                    save_csonfig()
                if "/cat" in command:
                    def extract_arg(arg):
                        return arg.split()[1:]

                    for item in extract_arg(command):
                        path = str(pathlib.Path().cwd()) + "/" + item
                        if pathlib.Path(path).exists():
                            doc = open(path, 'rb')
                            bot.send_document(message.chat.id, doc)
                        else:
                            bot.reply_to(message, "这个文件没有找到....")

                if "/addwhite" in command:
                    def extract_arg(arg):
                        return arg.split()[1:]

                    for group in extract_arg(command):
                        groupId = "".join(list(filter(str.isdigit, group)))
                        _csonfig["whiteGroup"].append(int(groupId))
                        bot.reply_to(message, '白名单加入了' + str(groupId))
                    save_csonfig()
                if "/removewhite" in command:
                    def extract_arg(arg):
                        return arg.split()[1:]

                    for group in extract_arg(command):
                        groupId = "".join(list(filter(str.isdigit, group)))
                        if int(groupId) in _csonfig["whiteGroup"]:
                            _csonfig["whiteGroup"].remove(int(groupId))
                            bot.reply_to(message, '白名单移除了' + str(groupId))
                    if isinstance(_csonfig["whiteGroup"], list):
                        _csonfig["whiteGroup"] = list(set(_csonfig["whiteGroup"]))
                    save_csonfig()

            except Exception as e:
                bot.reply_to(message, "Wrong:" + str(e))


# 群组管理员操作命令
def Admin(bot, config):
    @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
    def answer_for_admin(message):
        if "+test" in message.text:
            def extract_arg(arg):
                return arg.split()[1:]

            status = extract_arg(message.text)
            for user in status:
                bot.reply_to(message, "6分钟封锁，俄罗斯转盘模式已经开启, 答题可以解锁，不答题请等待，但是答错会被踢出群组，等待12分钟:" + str(status))
                try:
                    userId = "".join(list(filter(str.isdigit, user)))
                    verifyRedis.add(userId, str(message.chat.id))
                    bot.restrict_chat_member(message.chat.id, userId, can_send_messages=False,
                                             can_send_media_messages=False,
                                             can_send_other_messages=False, until_date=message.date + 360)
                except Exception as e:
                    pass

        if "+unban" in message.text:
            def extract_arg(arg):
                return arg.split()[1:]

            status = extract_arg(message.text)
            for user in status:
                userId = "".join(list(filter(str.isdigit, user)))
                group, key = verifyRedis.read(str(userId))
                if group:
                    # 机器人核心：通过用户注册请求
                    verifyRedis.promote(userId)
                    # 解封用户
                    bot.restrict_chat_member(message.chat.id, userId, can_send_messages=True,
                                             can_send_media_messages=True,
                                             can_send_other_messages=True)
            # 机器人核心：发送通知并自毁消息
            unbanr = bot.reply_to(message, "已手动解封这些小可爱:" + str(status))

            def delmsg(bot, chat, message):
                bot.delete_message(chat, message)

            t = Timer(30, delmsg, args=[bot, unbanr.chat.id, unbanr.message_id])
            t.start()


# 白名单系统
def botSelf(bot, config):
    # if bot is added to group
    @bot.my_chat_member_handler()
    def my_chat_m(message: types.ChatMemberUpdated):
        # old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "member":
            load_csonfig()
            bot.send_message(message.chat.id,
                             "我是璃月科技的生物验证机器人，负责群内新人的生物验证。\n注意:这个 Bot 需要删除消息和禁用用户的权限才能正常行动")
            if int(message.chat.id) in _csonfig.get("whiteGroup") or abs(int(message.chat.id)) in _csonfig.get(
                    "whiteGroup"):
                pass
                # bot.send_message(message.chat.id,
                #                 "Hello bro! i can use high level problem to verify new chat member~~")
            else:
                if _csonfig.get("whiteGroupSwitch"):
                    bot.send_message(message.chat.id,
                                     "检查设置发现群组不在白名单之中！...")
                    bot.leave_chat(message.chat.id)


# 群组离开
def Left(bot, config):
    @bot.message_handler(content_types=['left_chat_member'])
    def left(msg):
        #   if msg.left_chat_member.id != bot.get_me().id:
        load_csonfig()
        # 用户操作
        verifyRedis.removed(msg.from_user.id, str(msg.chat.id))


def message_del(bot, config):
    @bot.message_handler(content_types=util.content_type_service)
    def del_msg(message: types.Message):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            if "bot was kicked" in str(e):
                print("Bot被踢出了群组")
            else:
                print(e)
            pass

        # print(cmu.from_user)  # User : The admin who changed the bot's status
        # print(cmu.old_chat_member)  # ChatMember : The bot's previous status
        # print(cmu.new_chat_member)  # ChatMember : The bot's new status


# 启动新用户通知
def New(bot, config):
    @bot.chat_member_handler()
    def newer(msg: types.ChatMemberUpdated):
        # if msg.left_chat_member.id != bot.get_me().id:
        load_csonfig()
        old = msg.old_chat_member
        new = msg.new_chat_member

        def verify_user():
            # 用户操作
            try:
                bot.restrict_chat_member(msg.chat.id, new.user.id, can_send_messages=False,
                                         can_send_media_messages=False,
                                         can_send_other_messages=False)
            except Exception as e:
                no_power = bot.send_message(msg.chat.id, "没有权限执行对新用户的限制")
                t = Timer(30, botWorker.delmsg, args=[bot, no_power.chat.id, no_power.message_id])
                t.start()
            else:
                verifyRedis.add(new.user.id, str(msg.chat.id))
                InviteLink = config.link
                # print(InviteLink)
                bot_link = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
                bot_link.add(
                    InlineKeyboardButton("接受测试", url=InviteLink))  # Added Invite Link to Inline Keyboard
                msgs = bot.send_message(msg.chat.id,
                                        f"你好！{msg.from_user.first_name}.\n请start我进行私聊验证，来证明你的资格\n管理员手动解封请使用`+unban {new.user.id}`",
                                        reply_markup=bot_link,
                                        parse_mode='Markdown')
                t = Timer(30, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
                t.start()

        # 验证白名单
        if new.status == "member":
            if _csonfig.get("whiteGroupSwitch"):
                if int(msg.chat.id) in _csonfig.get("whiteGroup") or abs(int(msg.chat.id)) in _csonfig.get(
                        "whiteGroup"):
                    verify_user()
                else:
                    bot.send_message(msg.chat.id,
                                     "Somebody added me to this group , but the group not in my white list... 请向Bot所有者申请白名单")
                    bot.leave_chat(msg.chat.id)
            else:
                verify_user()
            # 启动验证流程


def Starts(bot, config):
    @bot.message_handler(commands=['start'])
    def welcome(message):
        # bot.reply_to(message, "未检索到你的信息。你无需验证")
        if message.chat.type == "private":
            group_k, key = verifyRedis.read(str(message.from_user.id))
            if group_k:
                bot.reply_to(message, f"开始验证群组{group_k}，你有175秒的时间计算这道题目")
                from CaptchaCore import CaptchaWorker
                paper = CaptchaWorker.Importer().pull(difficulty_min=1, difficulty_limit=7)
                sth = paper.create()
                bot.reply_to(message, sth[0])
                print("生成了一道题目:" + str(sth))

                def verify_step2(message):
                    try:
                        # group, keys = verifyRedis.read(str(message.from_user.id))
                        # chat_id = message.chat.id
                        answer = message.text
                        if str(answer) == str(sth[1]):
                            botWorker.un_restrict(message, bot, group_k)
                            verifyRedis.promote(message.from_user.id, group_k)
                            bot.reply_to(message, "好险！是正确的答案，如果没有被解封请通知群组管理员～")
                            msgss = botWorker.send_ok(message, bot, group_k)
                            t = Timer(25, botWorker.delmsg, args=[bot, msgss.chat.id, msgss.message_id])
                            t.start()
                        else:
                            if group_k:
                                verifyRedis.checker(fail_user=[key])
                                # bot.kick_chat_member(group, message.from_user.id)
                                mgs = botWorker.send_ban(message, bot, group_k)
                                t = Timer(30, botWorker.delmsg, args=[bot, mgs.chat.id, mgs.message_id])
                                t.start()
                                bot.reply_to(message, '回答错误，很抱歉我不能让您进入这个群组...您不符合管理员的筛选预期\n12分钟后可以重新进入')
                                t = Timer(720, botWorker.unbanUser, args=[bot, group_k, message.from_user.id])
                                t.start()
                    except Exception as e:
                        bot.reply_to(message, f'机器人出错了，请发送日志到项目 Issue ,谢谢你！\n 日志:`{e}`',
                                     parse_mode='Markdown')

                def verify_step(message):
                    try:
                        # chat_id = message.chat.id
                        answer = message.text
                        # 用户操作
                        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 veridyRedis 来决定用户去留！
                        if str(answer) == str(sth[1]):
                            botWorker.un_restrict(message, bot, group_k)
                            verifyRedis.promote(message.from_user.id, group_k)
                            bot.reply_to(message, "通过，是正确的答案！如果没有解封请通知管理员～")
                            msgss = botWorker.send_ok(message, bot, group_k)
                            t = Timer(25, botWorker.delmsg, args=[bot, msgss.chat.id, msgss.message_id])
                            t.start()

                        else:
                            bot.reply_to(message, '可惜是错误的回答....你还有一次机会')
                            bot.register_next_step_handler(message, verify_step2)
                    except Exception as e:
                        bot.reply_to(message, f'机器人出错了，请发送日志到项目Issue,谢谢你！\n 日志:`{e}`',
                                     parse_mode='Markdown')

                bot.register_next_step_handler(message, verify_step)
                # verify_step(bot, message)

            else:
                bot.reply_to(message, "数据库内没有你的信息哦，你无需验证！")
        else:
            pass
            # print(0)
