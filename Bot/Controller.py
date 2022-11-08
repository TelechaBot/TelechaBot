# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Controller.py
# @Software: PyCharm
# @Github    ：sudoskys
# import aiohttp
import asyncio
import datetime
import json
from pathlib import Path

import telebot
import Bot.Model
import CaptchaCore
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot import types, util
from utils.BotTool import Tool
from utils.BotTool import botWorker, userStates
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


async def set_cron(funcs, second: int):
    tick_scheduler = AsyncIOScheduler()
    tick_scheduler.add_job(funcs, 'interval', seconds=second)
    tick_scheduler.start()


# IO
def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


class clientBot(object):
    def __init__(self):
        from utils.BotTool import ReadConfig
        self.config = ReadConfig().parseFile(str(Path.cwd()) + "/Captcha.toml")
        # ReadYaml(str(Path.cwd()) + "/Captcha.yaml").get()

    def botCreate(self):
        # if pathlib.Path("project.ini").exists():
        #     from configparser import ConfigParser
        #     value = ConfigParser()
        #     value.read("project.ini")
        #     version = value.get('project', 'version')
        #     Tool().console.print("Create Async Bot Obj,版本:" + version, style='blue')
        bot = AsyncTeleBot(self.config.botToken, state_storage=StateMemoryStorage())
        return bot, self.config

    def SyncBotCreate(self):
        print("Create NoAsync Bot Obj")
        bot = telebot.TeleBot(self.config.botToken)
        return bot, self.config

    # 入口的控制器
    def run(self):
        load_csonfig()
        if _csonfig.get("statu"):
            Tool().console.print("Bot Running", style='blue')
            bot, config = self.botCreate()
            if config.get("Proxy"):
                if config.Proxy.status:
                    from telebot import asyncio_helper
                    asyncio_helper.proxy = config.Proxy.url  # 'http://127.0.0.1:7890'  # url
                    print("正在使用隧道！")

            # 捕获加群请求
            @bot.chat_join_request_handler()
            async def new_request(message: telebot.types.ChatJoinRequest):
                await Bot.Model.NewRequest(bot, message, config)

            @bot.message_handler(commands=["start", 'about'])
            async def handle_command(message):
                if "/start" in message.text:
                    await Bot.Model.Start(bot, message, config)
                elif "/about" in message.text:
                    await Bot.Model.About(bot, message, config)

            # 验证
            @bot.message_handler(state="*", commands='saveme')
            async def save_me(message):
                await Bot.Model.Saveme(bot, message, config)

            @bot.message_handler(state=userStates.answer)
            async def check_answer(message):
                await Bot.Model.Verify(bot, message, config)

            @bot.message_handler(state=userStates.answer2)
            async def check_answer(message):
                await Bot.Model.Verify2(bot, message, config)

            # 私聊事件捕获
            @bot.message_handler(content_types=['text'], chat_types=['private'])
            async def handle_private_msg(message):
                await Bot.Model.Switch(bot, message, config)

            # 非管理命令捕获
            @bot.message_handler(is_chat_admin=False, chat_types=['supergroup', 'group'])
            async def group_msg_no_admin(message):
                await Bot.Model.Banme(bot, message, config)

            # 管理命令捕获
            @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
            async def group_msg_admin(message):
                await Bot.Model.Admin(bot, message, config)

            # 加群提示
            @bot.my_chat_member_handler()
            async def bot_self(message: types.ChatMemberUpdated):
                await Bot.Model.botSelf(bot, message, config)

            # 服务消息删除
            @bot.message_handler(content_types=util.content_type_service)
            async def service_msg(message: types.Message):
                await Bot.Model.msg_del(bot, message, config)

            # 题库回调
            @bot.callback_query_handler(func=lambda call: True)
            async def callback_query(call):
                # from CaptchaCore.__init__ import Importer
                if call.data in CaptchaCore.Importer.getMethod():
                    set_delay_del(msgs=call.message, second=5)
                    if call.from_user.id == call.message.json.get("reply_to_message").get("from").get("id"):
                        if botWorker.set_model(call.message.chat.id, model=call.data):
                            await bot.answer_callback_query(call.id, "Success")
                            msgs = await bot.reply_to(call.message.json.get("reply_to_message").get("id"),
                                                      f"Info:群组验证模式已经切换至{call.data}")
                            set_delay_del(msgs=msgs, second=30)

                else:
                    # 如果不是题库定义的方法，那就向下执行
                    listP = call.data.split('+')
                    listKey = listP[0]
                    if listKey in ["Ban", "Pass"]:
                        pass

            from telebot import asyncio_filters
            bot.add_custom_filter(asyncio_filters.IsAdminFilter(bot))
            bot.add_custom_filter(asyncio_filters.ChatFilter())
            bot.add_custom_filter(asyncio_filters.StateFilter(bot))
            from Bot.Redis import JsonRedis
            JsonRedis.start()

            # aioschedule.every(3).seconds.do(JsonRedis.checker)
            # 不再使用的
            # await asyncio.gather(bot.infinity_polling(skip_pending=False, allowed_updates=util.update_types),
            async def main():
                await asyncio.gather(bot.polling(skip_pending=True, non_stop=True, allowed_updates=util.update_types),
                                     set_cron(JsonRedis.checker, second=3))

            asyncio.run(main())
