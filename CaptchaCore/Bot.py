# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
# import aiohttp
import random
from pathlib import Path
import json
from threading import Timer

from CaptchaCore.Event import Tool, botWorker
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


class clinetBot(object):
    def __init__(self):
        pass

    def botCreat(self):
        from CaptchaCore.Event import Read, Tool
        config = Read(str(Path.cwd()) + "/Captcha.yaml").get()
        if config.get("version"):
            Tool().console.print("完成初始化:" + config.version, style='blue')
        bot = telebot.TeleBot(config.botToken)
        return bot, config

    def run(self):
        load_csonfig()
        if _csonfig.get("statu"):
            Tool().console.print("Bot Running", style='blue')
            bot, config = self.botCreat()
            from telebot import custom_filters
            from telebot import types, util
            import CaptchaCore.BotEvent
            @bot.chat_member_handler()
            def chat_m(message: types.ChatMemberUpdated):
                CaptchaCore.BotEvent.member_update(bot, message, config)

            @bot.message_handler(commands=["start", 'about'])
            def handle_command(message):
                if "/start" in message.text:
                    CaptchaCore.BotEvent.Start(bot, message, config)
                elif "/about" in message.text:
                    CaptchaCore.BotEvent.About(bot, message, config)

            @bot.message_handler(content_types=['text'], chat_types=['private'])
            def handle_private_msg(message):
                CaptchaCore.BotEvent.Switch(bot, message, config)

            @bot.message_handler(is_chat_admin=False, chat_types=['supergroup', 'group'])
            def group_msg_no_admin(message):
                CaptchaCore.BotEvent.Banme(bot, message, config)

            @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
            def group_msg_no_admin(message):
                CaptchaCore.BotEvent.Admin(bot, message, config)

            @bot.my_chat_member_handler()
            def bot_self(message: types.ChatMemberUpdated):
                CaptchaCore.BotEvent.botSelf(bot, message, config)

            # @bot.message_handler(content_types=['left_chat_member'])
            # def left_chat(message):
            #     CaptchaCore.BotEvent.Left(bot, message, config)

            @bot.message_handler(content_types=util.content_type_service)
            def service_msg(message: types.Message):
                CaptchaCore.BotEvent.msg_del(bot, message, config)

            # 选择题库回调
            @bot.callback_query_handler(func=lambda call: True)
            def callback_query(call):
                def Del_call():
                    t = Timer(3, botWorker.delmsg, args=[bot, call.message.chat.id, call.message.id])
                    t.start()

                # print(call.message.json.get("reply_to_message"))
                if call.from_user.id == call.message.json.get("reply_to_message").get("from").get("id"):
                    Del_call()
                    if call.data:
                        if botWorker.set_model(call.message.chat.id, model=call.data):
                            bot.answer_callback_query(call.id, "Success")
                            msgss = bot.send_message(call.message.chat.id,
                                                     f"Info:群组验证模式已经切换至{call.data}")
                            t = Timer(10, botWorker.delmsg, args=[bot, msgss.chat.id, msgss.id])
                            t.start()
                    # if call.data == "学习强国":
                    #     if botWorker.set_model(call.message.chat.id, model='学习强国'):
                    #         info = "Success"
                    #     else:
                    #         info = "Failed"
                    #     bot.answer_callback_query(call.id, info)
                    # elif call.data == "科目一":
                    #     if botWorker.set_model(call.message.chat.id, model='科目一'):
                    #         info = "Success"
                    #     else:
                    #         info = "Failed"
                    #     bot.answer_callback_query(call.id, info)
                    # elif call.data == "学科题库":
                    #     if botWorker.set_model(call.message.chat.id, model='学科题库'):
                    #         info = "Success"
                    #     else:
                    #         info = "Failed"
                    #     bot.answer_callback_query(call.id, info)
                    # elif call.data == "安全工程师":
                    #     if botWorker.set_model(call.message.chat.id, model='安全工程师'):
                    #         info = "Success"
                    #     else:
                    #         info = "Failed"
                    #     bot.answer_callback_query(call.id, info)
                else:
                    pass
                    # print("Not")

            from BotRedis import JsonRedis
            JsonRedis.timer()
            bot.add_custom_filter(custom_filters.IsAdminFilter(bot))
            bot.add_custom_filter(custom_filters.ChatFilter())
            bot.infinity_polling(allowed_updates=util.update_types)


class sendBot(object):
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token):
        self.BOT = telebot.TeleBot(token, parse_mode="HTML")  # You can set parse_mode by default. HTML or MARKDOWN

    def sendMessage(self, objectID, msg):
        self.BOT.send_message(objectID, str(msg))

    def replyMessage(self, objectID, msg, reply_id):
        self.BOT.send_message(objectID, str(msg), reply_to_message_id=reply_id)

    def postDoc(self, objectID, files):
        if Path(str(files)).exists():
            doc = open(files, 'rb')
            self.BOT.send_document(objectID, doc)
            doc.close()
            return files

    def postVideo(self, objectID, files, source, name):
        if Path(str(files)).exists():
            video = open(files, 'rb')
            self.BOT.send_video(objectID, video, source, name, name)
            # '#音乐MV #AUTOrunning '+str(source)+"   "+name
            # 显示要求为MP4--https://mlog.club/article/5018822
            # print("============Already upload this video============")
            video.close()
            return files

    def postAudio(self, objectID, files, source, name):
        if Path(str(files)).exists():
            audio = open(files, 'rb')
            self.BOT.send_audio(objectID, audio, source, name, name)
            # '#音乐提取 #AUTOrunning '+str(source)+"   "+name
            # print("============ALready upload this flac============")
            audio.close()
            return files
