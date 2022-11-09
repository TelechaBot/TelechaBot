# -*- coding: utf-8 -*-
# @Time    : 9/1/22 5:31 PM
# @FileName: ChatSystem.py
# @Software: PyCharm
# @Github    ：sudoskys
import ast
import json
import pathlib
import time

import requests

from utils.BotTool import botWorker
from utils.safeDetect import Nude

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
        self.DataWorker = DataWorker(prefix="Users_")

    def setUser(self, userId: str, profile: dict):
        return self.DataWorker.setKey(key=userId, obj=profile)

    def getUser(self, userId: str):
        listSpam = self.DataWorker.getKey(userId)
        return listSpam

    @staticmethod
    def checkQrcode(filepath: str):
        import zxing
        reader = zxing.BarCodeReader()
        barcode = reader.decode(filepath)
        if barcode.format:
            return True
        else:
            return False

    async def Check(self, bot, _csonfig, groupId: str, UserProfile: dict, userId: str):
        """
        检查
        :param bot: 机器人实例
        :param _csonfig:
        :param groupId:
        :param UserProfile:
        :param userId:
        :return:
        """
        self.setUser(userId=UserProfile["id"], profile=UserProfile)
        Setting = botWorker.GetGroupStrategy(group_id=groupId)["scanUser"]
        _spam = Setting.get("spam")
        _premium = Setting.get("premium")
        _nsfw = Setting.get("nsfw")
        _suspect = Setting.get("suspect")
        _downPhoto = False
        _photoPath = "VerifyUser.jpg"
        # +[nsfw!on!ban!5] 代表入群审计头像是否含有 nsfw 内容
        # +[nsfw!off!pass!4]
        # +[nsfw!on!ask!30]
        # Init Status
        Status = {"spam": False, "premium": False, "nsfw": False, "suspect": False}
        suspect = 0
        # Status["24hjoin"] = False
        # 因为检查成本过高，所以换用逐项判定的方式
        if _spam:
            if _spam.get("type") == "on":
                # Check photo
                if UserProfile["photo"]:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfile["photo"])
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    IsSpam = self.checkQrcode(filepath=_photoPath)
                    if IsSpam:
                        Status["spam"] = _spam["level"]
                # Check profile text
                if UserProfile["token"]:
                    IsSpam = await SpamUtils().checkUser(_csonfig=_csonfig, info=UserProfile["token"], userId=userId)
                    if IsSpam:
                        Status["spam"] = _spam["level"]
        # NSFW
        if _nsfw:
            if _nsfw.get("type") == "on":
                if UserProfile["photo"]:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfile["photo"])
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    n = Nude(_photoPath)
                    n.resize(maxheight=160, maxwidth=160)
                    n.parse()
                    if n.result:
                        Status["nsfw"] = _nsfw["level"]
                # TODO 采用以下敏感词库并编码
                # "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/%E8%89%B2%E6%83%85%E7%B1%BB.txt"
        # suspect
        if _suspect:
            if _suspect.get("type") == "on":
                total = 30
                if not UserProfile["photo"]:
                    suspect += 10
                if not UserProfile["bio"]:
                    suspect += 10
                if not UserProfile["username"]:
                    suspect += 10
                if UserProfile["is_premium"]:
                    suspect -= 20
                if suspect < (total / 2):
                    Status["suspect"] = _suspect["level"]
        # Check premium
        if _premium:
            if _premium.get("type") == "on":
                if UserProfile["is_premium"]:
                    Status["premium"] = _premium["level"]
        # 排序启用的命令
        key = max(Status, key=Status.get)
        if Status[key]:
            return Setting.get(key)
        else:
            return None


class SpamUtils(object):
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

    async def checkUser(self, _csonfig, info: str, userId: str):
        spam = False
        # print(_csonfig)
        # if self.isUserSpam(userId):
        #    return True
        if info:
            if not pathlib.Path("Data/AntiSpam.txt").exists():
                lists = ["远控", "外挂", "支付", "哈希", "日赚", "广告", "招商", "梯子", "搞钱", "电报中文", "投放",
                         "集团", "财神", "合作", "微信",
                         "流量", "支付", "流量", "现货", "中文电报", "VPN免费", "vpn免费", "免费免", "咨询我", "接洽我",
                         "问询我",
                         "免费翻墙", "免翻墙", "我主页"]
                await SpamUtils.renewAnti(message=None)
            else:
                with open('Data/AntiSpam.txt') as f:  # 默认模式为‘r’，只读模式
                    contents = f.read()  # 读取文件全部内容
                    lists = contents.split("\n")
            for i in lists:
                if len(i) > 1:
                    if i in info:
                        return True
        if _csonfig.get("casSystem") and userId:
            netWork = requests.get(f'https://api.cas.chat/check?user_id={userId}')
            if netWork.status_code == 200:
                if netWork.json().get("ok"):
                    return True
        return spam

    @staticmethod
    async def renewAnti(message):
        import aiohttp
        from Bot.Controller import clientBot
        bot, config = clientBot().botCreate()
        async with aiohttp.request('GET',
                                   'https://raw.githubusercontent.com/TelechaBot/AntiSpam/main/Spam.txt') as response:
            if response.status == 200:
                some = await response.text()
                with open("Data/AntiSpam.txt", 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                    f.write(some)
                if message:
                    await bot.reply_to(message, "OK..Renew it")
            else:
                if message:
                    await bot.reply_to(message, f"Fail..{response.status}")
