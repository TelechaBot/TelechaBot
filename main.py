# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
import time

from CaptchaCore.Bot import clinetBot
from CaptchaCore.Event import Check, Tool

# 初始化文件系统
Check().run()

Tool().console.print("从 2.0.7 开始，bot升级为异步机器人，并引入redis！使用 redis 初步接管数据！", style="yellow")

# run_timer()
# pushService = sendBot(config.botToken)

clinetBot().run()
