# -*- coding: utf-8 -*-
# @Time    : 9/1/22 5:31 PM
# @FileName: ChatSystem.py
# @Software: PyCharm
# @Github    ：sudoskys

# 基于 Redis 的存储系统

import pathlib
import time
from utils.DataManager import UserProfile, DataWorker, CommandTable, GroupStrategyManger, GroupStrategy
from utils.safeDetect import Nude
from utils.DfaDetect import DFA, Censor
from utils.BotTool import ReadConfig
from utils.DataManager import UserManger

# 远端敏感词库
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
    config = ReadConfig().parseFile(str(pathlib.Path.cwd()) + "/Config/Captcha.toml")
    if config.Proxy.status:
        proxies = {
            'all://': config.Proxy.url,
        }  # 'http://127.0.0.1:7890'  # url
        return Censor.InitWords(url=urlForm, home_dir="./Data/", proxy=proxies)
    else:
        return Censor.InitWords(url=urlForm, home_dir="./Data/")


if not pathlib.Path("./Data/AntiSpam.bin").exists():
    InitCensor()
# 初始化反 Spam 系统，供下面使用
SpamDfa = DFA(path="./Data/AntiSpam.bin")
NsfwDfa = DFA(path="./Data/Nsfw.bin")
PoliticsDfa = DFA(path="./Data/Politics.bin")
AbsolutelySafeDfa = DFA(path="./Data/AbsolutelySafe.bin")


class UserUtils(object):
    def __init__(self):
        pass


class SpamUtils(object):
    def __init__(self):
        self.DataWorker = DataWorker(prefix="Spams_")

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

    async def checkUser(self, _csonfig, info: str):
        spam = False
        # print(_csonfig)
        # if self.isUserSpam(userId):
        #    return True
        if info:
            if not pathlib.Path("./Data/AntiSpam.bin").exists():
                await SpamUtils.renewAnti(message=None)
            if SpamDfa.exists(info):
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
            # 重载 AntiSpam 主题库
            SpamDfa.change_words(path="./Data/AntiSpam.bin")
            errors = "Success"
        if message:
            await bot.reply_to(message, f"{'|'.join(keys)}\n\n{errors}")


class DictUpdate(object):
    @staticmethod
    def dict_update(raw, new):
        DictUpdate.dict_update_iter(raw, new)
        DictUpdate.dict_add(raw, new)

    @staticmethod
    def dict_update_iter(raw, new):
        for key in raw:
            if key not in new.keys():
                continue
            if isinstance(raw[key], dict) and isinstance(new[key], dict):
                DictUpdate.dict_update(raw[key], new[key])
            else:
                raw[key] = new[key]

    @staticmethod
    def dict_add(raw, new):
        update_dict = {}
        for key in new:
            if key not in raw.keys():
                update_dict[key] = new[key]
        raw.update(update_dict)


class strategyUtils(object):
    """
    策略组提取/修复/创建，供给给预处理管线
    """

    def __init__(self, groupId: str):
        self.group_id = groupId
        _Strategy = GroupStrategyManger(groupId=groupId).read()
        # 初始化策略组
        if not _Strategy:
            default_setting = CommandTable.GroupStrategy_default_strategy()
            GroupStrategyManger(groupId=groupId).save(groupStrategyObj=GroupStrategy(**default_setting))

    def getDoorStrategy(self) -> dict:
        default = CommandTable.GroupStrategy_default_door_strategy()
        setting = GroupStrategyManger(groupId=self.group_id).read()
        if setting.get("door"):
            DictUpdate.dict_update(default, setting.get("door"))
            return default
        else:
            # 初始化 door 字段
            _Strategy = {
                "id": self.group_id,
                "door": default,
            }
            DictUpdate.dict_update(setting, _Strategy)
            GroupStrategyManger(groupId=self.group_id).save(groupStrategyObj=GroupStrategy(**setting))
            return default

    def setDoorStrategy(self, key: dict) -> bool:
        door_strategy = self.getDoorStrategy()
        setting = GroupStrategyManger(groupId=self.group_id).read()
        # 更新策略组
        DictUpdate.dict_update(door_strategy, key)
        _Strategy = {
            "id": self.group_id,
            "door": door_strategy,
        }
        DictUpdate.dict_update(setting, _Strategy)
        GroupStrategyManger(groupId=self.group_id).save(groupStrategyObj=GroupStrategy(**setting))
        return True


class TelechaEvaluator(object):
    """
    预先检查管线
    """

    def __init__(self, groupId: str, userId: str):
        self.groupId = str(groupId)
        self.userId = str(userId)

    def _lowLevel(self):
        pass

    def _highLevel(self):
        pass

    def _warnForm(self):
        pass

    def _selectorCreate(self):
        pass

    async def checkUser(self, bot, _csonfig, UserProfileData: UserProfile):
        """
        检查
        :param UserProfileData: UserProfile class
        :param bot: 机器人实例
        :param _csonfig: 设置
        :return:
        """
        CuteCat = UserManger(userId=self.userId)
        if not CuteCat.read():
            CuteCat.save(profileObj=UserProfileData)
        Setting = strategyUtils(groupId=self.groupId).getDoorStrategy()
        _spam = Setting.get("spam")
        _premium = Setting.get("premium")
        _nsfw = Setting.get("nsfw")
        _suspect = Setting.get("suspect")
        _politics = Setting.get("politics")
        _safe = Setting.get("safe")
        _downPhoto = False
        _photoPath = "VerifyUser.jpg"
        Status = CommandTable.GroupStrategy_door_strategy()
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
                if UserProfile.token:
                    if PoliticsDfa.exists(UserProfile.token):
                        Status["politics"] = getlevel(_politics)
        if _safe:
            if _safe.get("type") == "on":
                # Check photo
                if not UserProfile.photo:
                    Status["safe"] = getlevel(_safe)
                # Check profile text
                if UserProfile.token:
                    if AbsolutelySafeDfa.exists(UserProfile.token):
                        Status["safe"] = getlevel(_safe)
        if _spam:
            if _spam.get("type") == "on":
                # Check photo
                if UserProfile.first_name:
                    if len(UserProfile.first_name) < 2:
                        Status["spam"] = getlevel(_spam)

                if UserProfile.photo:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfile.photo)
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    IsSpam = SpamUtils.checkQrcode(filepath=_photoPath)
                    if IsSpam:
                        Status["spam"] = getlevel(_spam)
                # Check profile text
                if UserProfile.token:
                    IsSpam = await SpamUtils().checkUser(_csonfig=_csonfig, info=UserProfile.token)
                    if IsSpam:
                        Status["spam"] = getlevel(_spam)
        # NSFW
        if _nsfw:
            if _nsfw.get("type") == "on":
                if UserProfile.photo:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfile.photo)
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    n = Nude(_photoPath)
                    n.resize(maxheight=160, maxwidth=160)
                    n.parse()
                    if n.result:
                        Status["nsfw"] = getlevel(_nsfw)
                if UserProfile.token:
                    if NsfwDfa.exists(UserProfile.token):
                        Status["nsfw"] = getlevel(_nsfw)
        # suspect
        if _suspect:
            if _suspect.get("type") == "on":
                total = 30
                if not UserProfile.photo:
                    suspect += 10
                if not UserProfile.bio:
                    suspect += 10
                if not UserProfile.username:
                    suspect += 10
                if UserProfile.is_premium:
                    suspect -= 20
                if suspect < (total / 2):
                    Status["suspect"] = getlevel(_suspect)
        # Check premium
        if _premium:
            if _premium.get("type") == "on":
                if UserProfile.is_premium:
                    Status["premium"] = getlevel(_premium)
        # 排序启用的命令
        key = max(Status, key=Status.get)
        if Status[key]:
            return Setting.get(key)
        else:
            return {"level": 1, "command": "none", "type": "on", "info": "没有策略组"}
