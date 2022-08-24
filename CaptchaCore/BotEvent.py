# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import pathlib

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotRedis import JsonRedis
from threading import Timer
from telebot import formatting

# 构建多少秒的验证对象
verifyRedis = JsonRedis(175)


def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


# 支持三层读取创建操作并且不报错！
def readUser(where, group):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        oss = _csonfig[where].get(group)
        if oss:
            return oss
        else:
            return []
    else:
        return []


def popUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        if _csonfig[where].get(group):
            if key in _csonfig[where][str(group)]:
                _csonfig[where][str(group)].remove(key)
    save_csonfig()


def saveUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        if _csonfig[where].get(group):
            if not key in _csonfig[where][str(group)]:
                _csonfig[where][str(group)].append(key)
        else:
            _csonfig[where][str(group)] = []
            _csonfig[where][str(group)].append(key)
    else:
        _csonfig[where] = {}
        _csonfig[where][str(group)] = []
        _csonfig[where][str(group)].append(key)
    save_csonfig()


def Switch(bot, config):
    @bot.message_handler(content_types=['text'])
    def masters(message, items=None):
        userID = message.from_user.id
        load_csonfig()
        if str(userID) == config.ClientBot.owner:
            try:
                # chat_id = message.chat.id
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


def About(bot, config):
    @bot.message_handler(commands=['about'])
    def send_about(message):
        if message.chat.type == "private":
            if config.desc:
                bot.reply_to(message, config.desc)
            else:
                bot.reply_to(message, "生物信息验证 Bot，自主Project:https://github.com/sudoskys/")


def Admin(bot, config):
    @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
    def answer_for_admin(message):
        # bot.send_message(message.chat.id, "hello my admin")
        if "+unban" in message.text:
            def extract_arg(arg):
                return arg.split()[1:]
            status = extract_arg(message.text)
            for user in status:
                userId = "".join(list(filter(str.isdigit, user)))
                group = verifyRedis.read(str(userId))
                if group:
                    verifyRedis.promote(userId)
                    bot.restrict_chat_member(message.chat.id, userId, can_send_messages=True,
                                             can_send_media_messages=True,
                                             can_send_other_messages=True)
            unbanr = bot.reply_to(message, "已手动解封这些小可爱" + str(status))

            def delmsg(bot, chat, message):
                bot.delete_message(chat, message)
            t = Timer(25, delmsg, args=[bot, unbanr.chat.id, unbanr.message_id])
            t.start()


def Starts(bot, config):
    @bot.message_handler(commands=['start'])
    def welcome(message):
        # bot.reply_to(message, "未检索到你的信息。你无需验证")
        if message.chat.type == "private":
            group = verifyRedis.read(str(message.from_user.id))
            if group:
                bot.reply_to(message, f"开始验证群组{group}，你有175秒的时间计算这道题目")
                from CaptchaCore import CaptchaWorker
                paper = CaptchaWorker.Importer().pull(7)
                sth = paper.create()
                bot.reply_to(message, sth[0])
                print("生成了一道题目 " + str(sth))

                def unban(message):

                    verifyRedis.promote(message.from_user.id)
                    bot.restrict_chat_member(group, message.from_user.id, can_send_messages=True,
                                             can_send_media_messages=True,
                                             can_send_other_messages=True)
                    bot.reply_to(message, "验证成功，如果没有解封请通知管理员")

                def send_ban(message):
                    msgss = bot.send_message(group,
                                             f"刚刚{message.from_user.first_name}没有通过验证，已经被踢出群组...加入了黑名单！")
                    return msgss

                def send_ok(message):
                    msgss = bot.send_message(group,
                                             f"刚刚{message.from_user.first_name}通过了验证！")
                    return msgss

                def verify_step2(message):
                    try:
                        # chat_id = message.chat.id
                        answer = message.text
                        if str(answer) == str(sth[1]):
                            unban(message)
                            msgss = send_ok(message)

                            def delmsg(bot, chat, message):
                                bot.delete_message(chat, message)

                            t = Timer(25, delmsg, args=[bot, msgss.chat.id, msgss.message_id])
                            t.start()
                        else:
                            if verifyRedis.read(str(message.from_user.id)):
                                bot.kick_chat_member(group, message.from_user.id)
                                mgs = send_ban(message)

                                def delmsg(bot, chat, message):
                                    bot.delete_message(chat, message)

                                t = Timer(25, delmsg, args=[bot, mgs.chat.id, mgs.message_id])
                                t.start()
                                bot.reply_to(message, '验证失败...')
                    except Exception as e:
                        bot.reply_to(message, f'机器人出错了，请立刻通知项目组？!\n 日志:`{e}`',
                                     parse_mode='Markdown')

                def verify_step(message):
                    try:
                        chat_id = message.chat.id
                        answer = message.text
                        # 用户操作
                        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 veridyRedis 来决定用户去留！
                        if str(answer) == str(sth[1]):
                            unban(message)
                            msgss = send_ok(message)
                            from threading import Timer
                            def delmsg(bot, chat, message):
                                bot.delete_message(chat, message)

                            t = Timer(25, delmsg, args=[bot, msgss.chat.id, msgss.message_id])
                            t.start()

                        else:
                            bot.reply_to(message, '错误的回答....你还有一次机会')
                            bot.register_next_step_handler(message, verify_step2)
                        # user = User(name)
                        # user_dict[chat_id] = user
                        # msg = bot.reply_to(message, 'How old are you?')
                        # bot.register_next_step_handler(msg, process_age_step)
                    except Exception as e:
                        bot.reply_to(message, f'机器人出错了，请立刻通知项目组？!\n 日志:`{e}`',
                                     parse_mode='Markdown')

                bot.register_next_step_handler(message, verify_step)
                # verify_step(bot, message)

            else:
                bot.reply_to(message, "未检索到你的信息。你无需验证")
        else:
            print(0)


def Group(bot, config):
    # if bot is added to group
    @bot.my_chat_member_handler()
    def my_chat_m(message: types.ChatMemberUpdated):
        old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "member":
            load_csonfig()
            if message.chat.id in _csonfig.get("whiteGroup"):
                pass
                # bot.send_message(message.chat.id,
                #                 "Hello bro! i can use high level problem to verify new chat member~~")
            else:
                if _csonfig.get("whiteGroupSwitch"):
                    bot.send_message(message.chat.id,
                                     "Somebody added me to this group,but the group not in my white list...")
                    bot.leave_chat(message.chat.id)


def Left(bot, config):
    @bot.message_handler(content_types=['left_chat_member'])
    def left(msg):
        #   if msg.left_chat_member.id != bot.get_me().id:
        load_csonfig()
        try:
            bot.delete_message(msg.chat.id, msg.message_id)
        except Exception as e:
            print(e)
            bot.send_message(msg.chat.id,
                             f"sorry,i am not admin")
        # 用户操作
        verifyRedis.removed(msg.from_user.id, str(msg.chat.id))


def New(bot, config):
    @bot.message_handler(content_types=['new_chat_members'])
    def new_comer(msg):
        # if msg.left_chat_member.id != bot.get_me().id:
        load_csonfig()
        if _csonfig.get("whiteGroupSwitch"):
            if not (msg.chat.id in _csonfig.get("whiteGroup")):
                bot.send_message(msg.chat.id,
                                 "Somebody added me to this group,but the group not in my white list...")
                bot.leave_chat(msg.chat.id)
        try:
            bot.delete_message(msg.chat.id, msg.message_id)

        except Exception as e:
            print(e)
            bot.send_message(msg.chat.id,
                             f"sorry,i am not admin")
        # 用户操作
        verifyRedis.add(msg.from_user.id, str(msg.chat.id))
        # saveUser("newComer", msg.chat.id, msg.from_user.id)
        bot.restrict_chat_member(msg.chat.id, msg.from_user.id, can_send_messages=False,
                                 can_send_media_messages=False,
                                 can_send_other_messages=False)
        InviteLink = config.link
        # print(InviteLink)
        mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        mrkplink.add(
            InlineKeyboardButton("请与我展开私聊测试，来证明您是真人。 ", url=InviteLink))  # Added Invite Link to Inline Keyboard
        msgs = bot.send_message(msg.chat.id,
                                f"Hey there {msg.from_user.first_name}.\n管理员手动解封使用`+unban {msg.from_user.id}`",
                                reply_markup=mrkplink,
                                parse_mode='Markdown')

        def delmsg(bot, chat, message):
            bot.delete_message(chat, message)

        t = Timer(30, delmsg, args=[bot, msgs.chat.id, msgs.message_id])
        t.start()

    # InviteLink = "123"
    # mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    # mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
    # await bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
    #    name=new.user.first_name),
    #                       reply_markup=mrkplink)  # Welcome message
