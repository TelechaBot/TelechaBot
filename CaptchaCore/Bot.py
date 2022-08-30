# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
# import aiohttp
import asyncio
import json
import pathlib
import time
from pathlib import Path

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from CaptchaCore.Event import Read, Tool
from CaptchaCore.Event import botWorker, userStates


def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


class clinetBot(object):
    def __init__(self):
        self.config = Read(str(Path.cwd()) + "/Captcha.yaml").get()

    def botCreate(self):
        if pathlib.Path("project.ini").exists():
            from configparser import ConfigParser
            value = ConfigParser()
            value.read("project.ini")
            version = value.get('project', 'version')
            Tool().console.print("Create Bot,版本:" + version, style='blue')
        bot = AsyncTeleBot(self.config.botToken, state_storage=StateMemoryStorage())
        return bot, self.config

    def SyncBotCreate(self):
        print("同步Bot定时器被创建执行,危险")
        bot = telebot.TeleBot(self.config.botToken)
        return bot, self.config

    def run(self):
        load_csonfig()
        if _csonfig.get("statu"):
            Tool().console.print("Bot Running", style='blue')
            bot, config = self.botCreate()

            # from telebot import asyncio_helper
            # asyncio_helper.proxy = 'http://127.0.0.1:7890'  # url
            # print("正在使用代理！")

            from telebot import types, util
            import CaptchaCore.BotEvent

            @bot.chat_member_handler()
            async def chat_m(message: types.ChatMemberUpdated):
                await CaptchaCore.BotEvent.member_update(bot, message, config)

            # 核心
            @bot.message_handler(commands=["start", 'about'])
            async def handle_command(message):
                if "/start" in message.text:
                    await CaptchaCore.BotEvent.Start(bot, message, config)
                elif "/about" in message.text:
                    await CaptchaCore.BotEvent.About(bot, message, config)

            @bot.message_handler(state="*", commands='saveme')
            async def save_me(message):
                await CaptchaCore.BotEvent.Saveme(bot, message, config)

            @bot.message_handler(state=userStates.answer)
            async def check_answer(message):
                await CaptchaCore.BotEvent.Verify(bot, message, config)

            @bot.message_handler(state=userStates.answer2)
            async def check_answer(message):
                await CaptchaCore.BotEvent.Verify2(bot, message, config)

            # 事件
            @bot.message_handler(content_types=['text'], chat_types=['private'])
            async def handle_private_msg(message):
                await CaptchaCore.BotEvent.Switch(bot, message, config)

            @bot.message_handler(is_chat_admin=False, chat_types=['supergroup', 'group'])
            async def group_msg_no_admin(message):
                await CaptchaCore.BotEvent.Banme(bot, message, config)

            @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
            async def group_msg_no_admin(message):
                await CaptchaCore.BotEvent.Admin(bot, message, config)

            @bot.my_chat_member_handler()
            async def bot_self(message: types.ChatMemberUpdated):
                await CaptchaCore.BotEvent.botSelf(bot, message, config)

            @bot.message_handler(content_types=util.content_type_service)
            async def service_msg(message: types.Message):
                await CaptchaCore.BotEvent.msg_del(bot, message, config)

            # 选择题库回调
            @bot.callback_query_handler(func=lambda call: True)
            async def callback_query(call):
                def Del_call():
                    aioschedule.every(30).seconds.do(botWorker.delmsg, call.message.chat.id, call.message.id).tag(
                        call.message.id * abs(call.message.chat.id))

                from CaptchaCore.CaptchaWorker import Importer
                if call.data in Importer.getMethod():
                    if call.from_user.id == call.message.json.get("reply_to_message").get("from").get("id"):
                        Del_call()
                        if botWorker.set_model(call.message.chat.id, model=call.data):
                            await bot.answer_callback_query(call.id, "Success")
                            msgss = await bot.send_message(call.message.chat.id,
                                                           f"Info:群组验证模式已经切换至{call.data}")
                            aioschedule.every(30).seconds.do(botWorker.delmsg, msgss.chat.id, msgss.id).tag(
                                msgss.id * abs(msgss.chat.id))

                else:
                    # print(call.message.from_user)
                    Del_call()
                    listP = call.data.split('+')
                    listKey = listP[0]
                    if listKey in ["Ban", "Pass"]:
                        pass
                        # if listKey[0] == "Ban":

            from telebot import asyncio_filters
            bot.add_custom_filter(asyncio_filters.IsAdminFilter(bot))
            bot.add_custom_filter(asyncio_filters.ChatFilter())
            bot.add_custom_filter(asyncio_filters.StateFilter(bot))
            from BotRedis import JsonRedis
            import aioschedule
            aioschedule.every(3).seconds.do(JsonRedis.checker)

            async def scheduler():
                while True:
                    await aioschedule.run_pending()
                    await asyncio.sleep(1)

            async def main():
                await asyncio.gather(bot.polling(non_stop=True, allowed_updates=util.update_types), scheduler())

            asyncio.run(main())


class sendBot(object):

    def __init__(self, token):
        self.BOT = telebot.TeleBot(token, parse_mode="HTML")

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
