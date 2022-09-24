# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
from pathlib import Path
from Bot.Controller import clientBot
from utils.BotTool import Check, Tool

# 初始化文件系统
Check().run()

# from StarPuller import Worker
# Worker().get_index()

Tool().console.print("News: 2.0.9 需要安装Redis,并且给予机器人邀请权限，可选封禁权限", style="yellow")
Tool().console.print("News: 2.1.0 配置解析库已经改动，请填写新的机器人设置文件", style="yellow")

# pushService = sendBot(config.botToken)
clientBot().run()
