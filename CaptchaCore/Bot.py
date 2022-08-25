# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
# import aiohttp
from pathlib import Path
import joblib
import json
from CaptchaCore.Event import Tool
import telebot
from telebot import custom_filters


# from telebot import types, util
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.async_telebot import AsyncTeleBot


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
            import CaptchaCore.BotEvent
            from telebot import custom_filters
            from telebot import types, util
            # 开关
            CaptchaCore.BotEvent.New(bot, config)
            CaptchaCore.BotEvent.Left(bot, config)
            CaptchaCore.BotEvent.Starts(bot, config)
            CaptchaCore.BotEvent.About(bot, config)
            CaptchaCore.BotEvent.Banme(bot, config)
            CaptchaCore.BotEvent.Admin(bot, config)
            # 加载事件
            CaptchaCore.BotEvent.botSelf(bot, config)
            CaptchaCore.BotEvent.message_del(bot, config)
            CaptchaCore.BotEvent.Switch(bot, config)

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
