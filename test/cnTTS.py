# -*- coding: utf-8 -*-
# @Time    : 12/1/22 8:11 PM
# @FileName: cnTTS.py
# @Software: PyCharm
# @Github    ：sudoskys
from gtts import gTTS

tts = gTTS('你好，请问你是谁')
tts.save('hello.mp3')
