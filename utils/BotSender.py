# -*- coding: utf-8 -*-
# @Time    : 9/1/22 3:46 PM
# @FileName: BotSender.py
# @Software: PyCharm
# @Github    ：sudoskys
import telebot
from pathlib import Path


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
            # print("============Already upload this flac============")
            audio.close()
            return files
