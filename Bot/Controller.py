# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Controller.py
# @Software: PyCharm
# @Github    ：sudoskys
# import aiohttp
import json
import asyncio
import datetime
from pathlib import Path

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot import types, util

import Bot.Model
import CaptchaCore
from utils.BotTool import Tool
from utils.BotTool import botWorker, userStates
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loguru import logger

logger.add("run.log", rotation="100MB", encoding="utf-8", enqueue=True, retention="4 days")


def set_delay_del(msgs, second: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        botWorker.delmsg,
        args=[msgs.chat.id, msgs.message_id],
        trigger='date',
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=second),
        max_instances=10
    )
    scheduler.start()


async def set_cron(funcs, second: int):
    """
    启动一个异步定时器
    :param funcs: 回调函数
    :param second: 秒数
    :return:
    """
    tick_scheduler = AsyncIOScheduler()
    tick_scheduler.add_job(funcs, 'interval', max_instances=10, seconds=second)
    tick_scheduler.start()


global _csonfig


# IO
def load_csonfig():
    global _csonfig
    with open("./Config/config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


class clientBot(object):
    def __init__(self, ConfigPath: str = None):
        from utils.BotTool import ReadConfig
        if not ConfigPath:
            ConfigPath = str(Path.cwd()) + "/Config/Captcha.toml"
        self.config = ReadConfig().parseFile(ConfigPath)

    def botCreate(self):
        bot = AsyncTeleBot(self.config.botToken, state_storage=StateMemoryStorage())
        return bot, self.config

    def SyncBotCreate(self):
        logger.info("Create NoAsync Bot Obj")
        bot = telebot.TeleBot(self.config.botToken)
        return bot, self.config

    # 入口的控制器
    def run(self):
        load_csonfig()
        if _csonfig.get("statu"):
            logger.success("Bot Start")
            bot, config = self.botCreate()
            if config.get("Proxy"):
                if config.Proxy.status:
                    from telebot import asyncio_helper
                    asyncio_helper.proxy = config.Proxy.url  # 'http://127.0.0.1:7890'  # url
                    logger.success("正在使用隧道！")

            # 捕获加群请求
            @bot.chat_join_request_handler()
            async def new_request(message):
                await Bot.Model.NewRequest(bot, message, config)

            # 捕获私聊启动请求
            @bot.message_handler(commands=["start", 'about'])
            async def handle_command(message: types.Message):
                if "/start" in message.text:
                    await Bot.Model.Start(bot, message, config)
                elif "/about" in message.text:
                    await Bot.Model.About(bot, message, config)

            # 验证
            @bot.message_handler(state="*", commands='saveme')
            async def save_me(message: types.Message):
                await Bot.Model.Saveme(bot, message, config)

            @bot.message_handler(state=userStates.answer)
            async def check_answer(message: types.Message):
                await Bot.Model.Verify(bot, message, config)

            # 私聊事件捕获
            @bot.message_handler(content_types=['text'], chat_types=['private'])
            async def handle_private_msg(message: types.Message):
                await Bot.Model.Switch(bot, message, config)

            # 非管理命令捕获
            @bot.message_handler(is_chat_admin=False, chat_types=['supergroup', 'group'])
            async def group_msg_no_admin(message: types.Message):
                await Bot.Model.Group_User(bot, message, config)

            # 管理命令捕获
            @bot.message_handler(chat_types=['supergroup', 'group'], is_chat_admin=True)
            async def group_msg_admin(message: types.Message):
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
                            await bot.answer_callback_query(call.id, "Success Change")
                            msgs = await bot.send_message(call.message.chat.id,
                                                          f"Info:群组验证模式已经切换至{call.data}",
                                                          reply_to_message_id=call.message.json["reply_to_message"][
                                                              "message_id"])
                            set_delay_del(msgs=msgs, second=120)

            from telebot import asyncio_filters
            bot.add_custom_filter(asyncio_filters.IsAdminFilter(bot))
            bot.add_custom_filter(asyncio_filters.ChatFilter())
            bot.add_custom_filter(asyncio_filters.StateFilter(bot))
            from Bot.Redis import JsonRedis
            JsonRedis.start()

            # 不再使用的
            # await asyncio.gather(bot.infinity_polling(skip_pending=False, allowed_updates=util.update_types),
            async def main():
                await asyncio.gather(bot.polling(skip_pending=False, non_stop=True, allowed_updates=util.update_types),
                                     set_cron(JsonRedis.checker, second=5))

            asyncio.run(main())
