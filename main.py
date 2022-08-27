# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys

from CaptchaCore.Bot import clinetBot
from CaptchaCore.Event import Check

# 初始化文件系统
Check().run()


def run_timer():
    from StarPuller import Worker
    Worker().get_index()
    timer()


def timer():
    from threading import Timer
    t = Timer(5000, run_timer, args=[])
    t.start()


# run_timer()
# pushService = sendBot(config.botToken)
clinetBot().run()
