# -*- coding: utf-8 -*-
# @Time    : 9/1/22 5:31 PM
# @FileName: ChatSystem.py
# @Software: PyCharm
# @Github    ：sudoskys

# 基于 Redis 的存储系统

import time
import pathlib
from utils.safeDetect import Nude
from utils.BotTool import ReadConfig
from utils.DfaDetect import DFA, Censor
from utils.DataManager import DataWorker, CommandTable
from utils.DataManager import GroupStrategy, UserTrack, UserProfile, GroupProfile
from utils.DataManager import UserTrackManger, UserManger, GroupManger, GroupStrategyManger

# 远端敏感词库
urlForm = {
    "AntiSpam.bin": [
        "https://raw.githubusercontent.com/TelechaBot/AntiSpam/main/Spam.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/色情类.txt",
        "https://raw.githubusercontent.com/fwwdn/sensitive-stop-words/master/广告.txt",
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


class UserTrackUtils(object):
    def __init__(self, userId: str, groupId: str = "1"):
        self.group_id = groupId
        self.user_id = userId
        self._Manger = UserTrackManger(userId=userId)
        # 初始化策略组
        if not self._Manger.read():
            default_setting = CommandTable.UserTrack_default()
            self._Manger.save(userTrackObj=UserTrack(**default_setting))

    def resignGroup(self, groupId: str, status: str):
        self.group_id = groupId
        _Track = self._Manger.read()
        _Main = UserTrack(**_Track)
        Group = _Main.group.get(str(groupId))
        _Now = {"time": int(time.time() * 1000), "result": status}
        if Group:
            Group.append(_Now)
            _Main.group.update({groupId: Group})
        else:
            _Main.group.update({groupId: [_Now]})
        _UpdateData = _Main.dict()
        # DictUpdate.dict_update(_Track, _UpdateData)
        self._Manger.save(userTrackObj=UserTrack(**_UpdateData))
        return _Main.group

    def resignDetect(self, groupId: str, status: str, score: int = -1):
        self.group_id = groupId
        _Track = self._Manger.read()
        _Main = UserTrack(**_Track)
        Score = _Main.score.get(str(groupId))
        _Now = {"time": int(time.time() * 1000), "result": status, "score": score}
        if Score:
            Score.append(_Now)
            _Main.score.update({groupId: Score})
        else:
            _Main.score.update({groupId: [_Now]})
        _UpdateData = _Main.dict()
        # DictUpdate.dict_update(_Track, _UpdateData)
        self._Manger.save(userTrackObj=UserTrack(**_UpdateData))
        return _Main.score

    def getGroupHistory(self, groupId: str):
        _Track = self._Manger.read()
        _Main = UserTrack(**_Track)
        return _Main.group.get(str(groupId))

    def getDetectHistory(self, groupId: str):
        _Track = self._Manger.read()
        _Main = UserTrack(**_Track)
        return _Main.score.get(str(groupId))

    def isBaka(self, groupId: str):
        _Track = self._Manger.read()
        _Main = UserTrack(**_Track)
        if not _Main.group:
            return -1
        _rs = 0
        _total = 1
        _timeout = 0
        for k, d in _Main.group.items():
            for i in d:
                if isinstance(i, dict):
                    _total += 1
                    if i.get("result") == "ban":
                        _rs += 1
                    if i.get("result") == "timeout":
                        _timeout += 1
        BakaScore = (_rs + _timeout) / _total
        DangerScore = _timeout / _total
        WellMan = _total / 10
        return [BakaScore, DangerScore, WellMan]


class GroupUtils(object):
    def __init__(self, groupId: str, userId: str = "1"):
        self.group_id = groupId
        self.user_id = userId
        self._Manger = GroupManger(groupId=groupId)
        # 初始化策略组
        if not self._Manger.read():
            default_setting = CommandTable.GroupUtils_default(groupId=self.group_id, userId=self.user_id)
            self._Manger.save(profileObj=GroupProfile(**default_setting))

    def setUser(self, userId: str, status: str = None):
        """
        设定群组设定的用户状态
        :param userId:
        :param status:
        :return:
        """
        self.user_id = userId
        _GroupData = self._Manger.read()
        _UpdateData = {
            "id": self.group_id,
            "user": {userId: {"status": status}},
        }
        DictUpdate.dict_update(_GroupData, _UpdateData)
        self._Manger.save(profileObj=GroupProfile(**_GroupData))

    def recordStatus(self, userId: str, status: str):
        """
        增加验证次数
        :param status:
        :param userId:
        :return:
        """
        _GroupData = self._Manger.read()
        if not _GroupData.get("time"):
            _GroupData["user"][userId]["time"] = []
        _UpdateData = {
            "id": self.group_id,
            "user": {userId: {"time": _GroupData["time"].append([int(time.time()), status])}},
            "times": _GroupData["times"] + 1
        }
        DictUpdate.dict_update(_GroupData, _UpdateData)
        self._Manger.save(profileObj=GroupProfile(**_GroupData))


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
        _Strategy = GroupStrategyManger(groupId=groupId)
        # 初始化策略组
        if not _Strategy.read():
            default_setting = CommandTable.GroupStrategy_default_strategy()
            _Strategy.save(groupStrategyObj=GroupStrategy(**default_setting))

    def getDoorStrategy(self) -> dict:
        default = CommandTable.GroupStrategy_default_door_strategy()
        _Manger = GroupStrategyManger(groupId=self.group_id)
        setting = _Manger.read()
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
            _Manger.save(groupStrategyObj=GroupStrategy(**setting))
            return default

    def setDoorStrategy(self, key: dict) -> bool:
        door_strategy = self.getDoorStrategy()
        _Manger = GroupStrategyManger(groupId=self.group_id)
        setting = _Manger.read()
        # 更新策略组
        DictUpdate.dict_update(door_strategy, key)
        _Strategy = {
            "id": self.group_id,
            "door": door_strategy,
        }
        DictUpdate.dict_update(setting, _Strategy)
        _Manger.save(groupStrategyObj=GroupStrategy(**setting))
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
        _lang = Setting.get("lang")
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

        if _lang:
            if _lang.get("type") == "on":
                if UserProfileData.language_code:
                    if "NOT" in _lang.get("flag"):
                        if not str(UserProfileData.language_code) in _lang.get("flag"):
                            Status["lang"] = getlevel(_lang)
                    else:
                        if str(UserProfileData.language_code) in _lang.get("flag"):
                            Status["lang"] = getlevel(_lang)
        if _politics:
            if _politics.get("type") == "on":
                # Check profile text
                if UserProfileData.token:
                    if PoliticsDfa.exists(UserProfile.token):
                        Status["politics"] = getlevel(_politics)
        if _safe:
            if _safe.get("type") == "on":
                # Check photo
                if not UserProfileData.photo:
                    Status["safe"] = getlevel(_safe)
                # Check profile text
                if UserProfileData.token:
                    if AbsolutelySafeDfa.exists(UserProfileData.token):
                        Status["safe"] = getlevel(_safe)
        if _spam:
            if _spam.get("type") == "on":
                # Check photo
                if UserProfileData.photo:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfileData.photo)
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    IsSpam = SpamUtils.checkQrcode(filepath=_photoPath)
                    if IsSpam:
                        Status["spam"] = getlevel(_spam)
                # Check profile text
                if UserProfileData.token:
                    IsSpam = await SpamUtils().checkUser(_csonfig=_csonfig, info=UserProfileData.token)
                    if IsSpam:
                        Status["spam"] = getlevel(_spam)
        # NSFW
        if _nsfw:
            if _nsfw.get("type") == "on":
                if UserProfileData.photo:
                    if not _downPhoto:
                        file_path = await bot.get_file(UserProfileData.photo)
                        downloaded_file = await bot.download_file(file_path.file_path)
                        with open(_photoPath, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            _downPhoto = True
                    n = Nude(_photoPath)
                    n.resize(maxheight=160, maxwidth=160)
                    n.parse()
                    if n.result:
                        Status["nsfw"] = getlevel(_nsfw)
                if UserProfileData.token:
                    if NsfwDfa.exists(UserProfileData.token):
                        Status["nsfw"] = getlevel(_nsfw)
        # suspect
        if _suspect:
            if _suspect.get("type") == "on":
                total = 30
                if not UserProfileData.photo:
                    suspect += 10
                if not UserProfileData.bio:
                    suspect += 10
                if not UserProfileData.username:
                    suspect += 10
                if UserProfileData.is_premium:
                    suspect -= 20
                if suspect < (total / 2):
                    Status["suspect"] = getlevel(_suspect)
        # Check premium
        if _premium:
            if _premium.get("type") == "on":
                if UserProfileData.is_premium:
                    Status["premium"] = getlevel(_premium)
        # 排序启用的命令
        key = max(Status, key=Status.get)
        if Status[key]:
            return Setting.get(key)
        else:
            return {"level": 1, "command": "none", "type": "on", "info": "没有策略组"}
