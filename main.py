# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
from Bot.Controller import clinetBot
from utils.BotTool import Check, Tool

# 初始化文件系统
Check().run()

# from StarPuller import Worker
# Worker().get_index()

Tool().console.print("News:2.0.9需要安装Redis,并且给予机器人邀请权限，不需要封禁权限", style="yellow")

# pushService = sendBot(config.botToken)

clinetBot().run()
