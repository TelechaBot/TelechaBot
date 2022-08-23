# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys

from pathlib import Path
from CaptchaCore.Bot import sendBot, clinetBot
from CaptchaCore.Event import Check, Read, Tool

# 初始化文件系统
Check().run()

# pushService = sendBot(config.botToken)
clinetBot().run()
