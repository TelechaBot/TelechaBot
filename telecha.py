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
Tool().console.print("News: 3.1.1 增加过滤器，优化过滤库，DFA快速算法", style="yellow")
Tool().console.print("News: 3.1.0 切换为策略组模式，群组设置更多样", style="yellow")
Tool().console.print("News: 3.0.1 增加TTS验证，可选使用， sudo apt install espeak ffmpeg libespeak1", style="yellow")
Tool().console.print("News: 2.1.0 配置解析库已经改动，请填写新的机器人设置文件", style="yellow")

# pushService = sendBot(config.botToken)
clientBot(ConfigPath=str(Path.cwd()) + "/Config/Captcha.toml").run()
