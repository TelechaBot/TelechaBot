# -*- coding: utf-8 -*-
# @Time    : 9/1/22 5:31 PM
# @FileName: ChatSystem.py
# @Software: PyCharm
# @Github    ：sudoskys
import ast
import json
import time

import requests

redis_installed = True
try:
    from redis import Redis, ConnectionPool
except:
    redis_installed = False


class DataWorker(object):
    def __init__(self, host='localhost', port=6379, db=0, password=None, prefix='Telecha_'):
        self.redis = ConnectionPool(host=host, port=port, db=db, password=password)
        # self.con = Redis(connection_pool=self.redis) -> use this when necessary
        #
        # {chat_id: {user_id: {'state': None, 'data': {}}, ...}, ...}
        self.prefix = prefix
        if not redis_installed:
            raise Exception("Redis is not installed. Install it via 'pip install redis'")

    def setKey(self, key, obj, exN=None):
        connection = Redis(connection_pool=self.redis)
        connection.set(self.prefix + str(key), json.dumps(obj), ex=exN)
        connection.close()
        return True

    def deleteKey(self, key):
        connection = Redis(connection_pool=self.redis)
        connection.delete(self.prefix + str(key))
        connection.close()
        return True

    def getKey(self, key):
        connection = Redis(connection_pool=self.redis)
        result = connection.get(self.prefix + str(key))
        connection.close()
        if result:
            return json.loads(result)
        else:
            return False

    def addToList(self, key, listData: list):
        data = self.getKey(key)
        if isinstance(data, str):
            listGet = ast.literal_eval(data)
        else:
            listGet = []
        listGet = listGet + listData
        listGet = list(set(listGet))
        if self.setKey(key, str(listGet)):
            return True

    def getList(self, key):
        listGet = ast.literal_eval(self.getKey(key))
        if not listGet:
            listGet = []
        return listGet

    def getPuffix(self, fix):
        connection = Redis(connection_pool=self.redis)
        listGet = connection.scan_iter(f"{fix}*")
        connection.close()
        return listGet


class ChatUtils(object):
    def __init__(self):
        self.DataWorker = DataWorker(prefix="Utils_")

    def addGroup(self, groupId: str):
        self.DataWorker.addToList("Chat", [groupId])

    def getGroupItem(self):
        return self.DataWorker.getList("Chat")


class UserUtils(object):
    def __init__(self):
        self.DataWorker = DataWorker(prefix="Spams_")

    def addSpamUser(self, userId: str, groupId: str):
        self.DataWorker.setKey(userId, str(time.time()), exN=43200)  # 86400 * 1)
        if groupId:
            self.DataWorker.addToList(groupId, [userId])

    def isUserSpam(self, userId: str):
        listSpam = self.DataWorker.getKey(userId)
        if listSpam:
            return True
        else:
            return False

    def getGroupSpamListHistory(self, groupId: str):
        return self.DataWorker.getList(groupId)

    def getAllSpamUser(self):
        return self.DataWorker.getPuffix("Spams_")
        # self.DataWorker.getList("Spam")

    def checkUser(self, _csonfig, info: str, userId: str):
        spam = False
        # print(_csonfig)
        if self.isUserSpam(userId):
            spam = True
        if _csonfig.get("antiSpam") and info:
            aList = ["远控", "外挂", "百万娱乐", "暗雷", "收U", "支付", "哈希", "日赚", "广告", "招商", "梯子", "搞钱", "转账", "电报中文", "投放", "集团",
                     "财神"]
            bList = ["合作", "微信", "流量", "支付", "流量", "现货", "中文电报", "VPN免费", "vpn免费", "免费免", "咨询我", "接洽我", "问询我", "询问我",
                     "免费翻墙", "免翻墙"]
            for i in aList + bList:
                if i in info:
                    spam = True
        if _csonfig.get("casSystem") and userId:
            netWork = requests.get(f'https://api.cas.chat/check?user_id={userId}')
            if netWork.status_code == 200:
                if netWork.json().get("ok"):
                    spam = True
        return spam

    def UpdateSpam(self):
        pass
