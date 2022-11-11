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
from utils.DfaDetecte import DFA, Censor
from utils.BotTool import ReadConfig

redis_installed = True

try:
    from redis import Redis, ConnectionPool
except Exception:
    redis_installed = False

urlForm = {
    "AntiSpam.bin": [
        "https://raw.githubusercontent.com/TelechaBot/AntiSpam/main/Spam.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/色情类.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/广告.txt",
        "https://raw.githubusercontent.com/Jaimin1304/sensitive-word-detector/main/sample_files/sample_banned_words.txt",
    ],
    "Nsfw.bin": [
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/色情类.txt"],
    "Politics.bin": [
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/政治类.txt",
    ],
    "AbsolutelySafe.bin": [
        "https://raw.githubusercontent.com/adlered/DangerousSpamWords/master/DangerousSpamWords/General_SpamWords_V1.0.1_CN.min.txt",
        "https://raw.githubusercontent.com/nonecares/-/master/ban.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/政治类.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/广告.txt",
    ]
}


def InitCensor():
    config = ReadConfig().parseFile(str(pathlib.Path.cwd()) + "/Captcha.toml")
    if config.Proxy.status:
        proxies = {
            'all://': config.Proxy.url,
        }  # 'http://127.0.0.1:7890'  # url
        return Censor.InitWords(url=urlForm, proxy=proxies)
    else:
        return Censor.InitWords(url=urlForm)


if not pathlib.Path("AntiSpam.bin").exists():
    InitCensor()
SpamDfa = DFA(path="AntiSpam.bin")
NsfwDfa = DFA(path="Nsfw.bin")
PoliticsDfa = DFA(path="Politics.bin")
AbsolutelySafeDfa = DFA(path="AbsolutelySafe.bin")


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
        try:
            import zxing
            reader = zxing.BarCodeReader()
            barcode = reader.decode(filepath)
            if barcode.format:
                return True
            else:
                return False
        except Exception as e:
            print(e)
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
        _politics = Setting.get("politics")
        _safe = Setting.get("safe")
        _downPhoto = False
        _photoPath = "VerifyUser.jpg"
        # +[nsfw!on!ban!5] 代表入群审计头像是否含有 nsfw 内容
        # +[nsfw!off!pass!4]
        # +[nsfw!on!ask!30]
        # Init Status
        Status = botWorker.get_door_strategy()
        suspect = 0

        # Status["24hjoin"] = False
        # 因为检查成本过高，所以换用逐项判定的方式
        def getlevel(clas):
            if clas.get("level"):
                return clas["level"]
            else:
                return 1

        if _politics:
            if _politics.get("type") == "on":
                # Check profile text
                if UserProfile["token"]:
                    if PoliticsDfa.exists(UserProfile["token"]):
                        Status["politics"] = getlevel(_politics)
        if _safe:
            if _safe.get("type") == "on":
                # Check photo
                if not UserProfile["photo"]:
                    Status["safe"] = getlevel(_safe)
                # Check profile text
                if UserProfile["token"]:
                    if AbsolutelySafeDfa.exists(UserProfile["token"]):
                        Status["safe"] = getlevel(_safe)
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
                        Status["spam"] = getlevel(_spam)
                # Check profile text
                if UserProfile["token"]:
                    IsSpam = await SpamUtils().checkUser(_csonfig=_csonfig, info=UserProfile["token"], userId=userId)
                    if IsSpam:
                        Status["spam"] = getlevel(_spam)
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
                        Status["nsfw"] = getlevel(_nsfw)
                if UserProfile["token"]:
                    if NsfwDfa.exists(UserProfile["token"]):
                        Status["nsfw"] = getlevel(_nsfw)
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
                    Status["suspect"] = getlevel(_suspect)
        # Check premium
        if _premium:
            if _premium.get("type") == "on":
                if UserProfile["is_premium"]:
                    Status["premium"] = getlevel(_premium)
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
            if not pathlib.Path("AntiSpam.bin").exists():
                await SpamUtils.renewAnti(message=None)
            if SpamDfa.exists(info):
                return True
        if _csonfig.get("casSystem") and userId:
            try:
                netWork = requests.get(f'https://api.cas.chat/check?user_id={userId}')
            except:
                pass
            else:
                if netWork.status_code == 200:
                    if netWork.json().get("ok"):
                        return True
        return spam

    @staticmethod
    async def renewAnti(message):
        from Bot.Controller import clientBot
        bot, config = clientBot().botCreate()
        keys, _error = InitCensor()
        if _error:
            error = '\n'.join(_error)
            errors = f"Error:\n{error}"
        else:
            SpamDfa.change_words(path="AntiSpam.bin")
            errors = "No Error"
        if message:
            await bot.reply_to(message, f"{'|'.join(keys)}\n\n{errors}")
