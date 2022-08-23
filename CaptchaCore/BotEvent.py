# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import telebot
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotRedis import JsonRedis

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
                if command == "off":
                    _csonfig["statu"] = False
                    save_csonfig()
                    bot.reply_to(message, 'success！')
                if command == "on":
                    _csonfig["statu"] = True
                    save_csonfig()
                    bot.reply_to(message, 'success！')
            except Exception as e:
                bot.reply_to(message, "Wrong:" + str(e))


def About(bot, config):
    @bot.message_handler(commands=['about'])
    def send_about(message):
        if message.chat.type == "private":
            bot.reply_to(message, "学习永不停息，进步永不止步，Project:https://github.com/sudoskys/")


def Starts(bot, config):
    @bot.message_handler(commands=['start'])
    def welcome(message):
        # bot.reply_to(message, "未检索到你的信息。你无需验证")
        if message.chat.type == "private":
            group = verifyRedis.read(str(message.from_user.id))
            if group:
                bot.reply_to(message, f"开始验证群组{group}，你有175秒的时间计算这道题目")

                def verify_step(message):
                    try:
                        chat_id = message.chat.id
                        answer = message.text
                        # 用户操作
                        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 veridyRedis 来决定用户去留！
                        if True:
                            verifyRedis.promote(message.from_user.id)
                            bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=True,
                                                     can_send_media_messages=True,
                                                     can_send_other_messages=True)
                            bot.reply_to(message, "验证成功，如果没有解封请通知管理员")
                        # user = User(name)
                        # user_dict[chat_id] = user
                        # msg = bot.reply_to(message, 'How old are you?')
                        # bot.register_next_step_handler(msg, process_age_step)
                    except Exception as e:
                        bot.reply_to(message, 'oooops')

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
                                     "Somebody added me to THIS group,but the group not in my white list")
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
        InviteLink = "https://github.com/TelechaBot"
        mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        mrkplink.add(
            InlineKeyboardButton("请与我展开私聊测试，来证明您是真人。 ", url=InviteLink))  # Added Invite Link to Inline Keyboard
        bot.send_message(msg.chat.id,
                         f"Hey there {msg.from_user.first_name}.", reply_markup=mrkplink)

    # InviteLink = "123"
    # mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    # mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
    # await bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
    #    name=new.user.first_name),
    #                       reply_markup=mrkplink)  # Welcome message
