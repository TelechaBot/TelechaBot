# -*- coding: utf-8 -*-
# @Time    : 11/14/22 10:08 AM
# @FileName: DataManager.py
# @Software: PyCharm
# @Github    ：sudoskys

import ast
import json
# 这里是数据基本类
from pydantic import BaseModel, ValidationError, validator
from typing import Optional, Union

redis_installed = True

try:
    from redis import Redis, ConnectionPool
except Exception:
    redis_installed = False


class User_Data(BaseModel):
    QaPair: list
    Group: str
    Times: int
    UUID: str = "not found"


class CommandTable(object):
    @staticmethod
    def GroupStrategy_door_strategy():
        return {"spam": False, "premium": False, "nsfw": False, "suspect": False, "safe": False, "politics": False,
                "lang": False}

    @staticmethod
    def GroupStrategy_default_door_strategy():
        return {
            "spam": {
                "level": 8,
                "command": "ban",
                "type": "on",
                "flag": "None",
                "info": "群组策略:反垃圾系统"
            },
            "premium": {
                "level": 5,
                "command": "pass",
                "type": "off",
                "flag": "None",
                "info": "群组策略:自动通过"
            },
            "nsfw": {
                "level": 4,
                "command": "ask",
                "type": "off",
                "flag": "None",
                "info": "群组策略:色情审查"
            },
            "safe": {
                "level": 1,
                "command": "ban",
                "type": "off",
                "flag": "None",
                "info": "群组策略:安全审查"
            },
            "suspect": {
                "level": 2,
                "command": "ask",
                "type": "off",
                "flag": "None",
                "info": "群组策略:嫌疑识别"
            },
            "politics": {
                "level": 2,
                "command": "ask",
                "type": "off",
                "flag": "None",
                "info": "群组策略:立场审查"
            },
            "lang": {
                "level": 1,
                "command": "ask",
                "type": "off",
                "flag": "None",
                "info": "群组策略:语言限制"
            }
        }

    @staticmethod
    def GroupStrategy_default_strategy() -> dict:
        return GroupStrategy(id="").dict()

    @staticmethod
    def GroupUtils_default(groupId: str, userId: str):
        return GroupProfile(id=groupId, user={userId: {}}).dict()

    @staticmethod
    def UserTrack_default():
        return UserTrack().dict()


class UserTrack(BaseModel):
    group: Optional[dict] = {
        # "1": [{"time": 1, "result": "ban"}]
    }
    score: Optional[dict] = {
        # "1": [{"time": 1, "detect": "ban", "score": 1}]
    }
    deliver: Optional[bool] = False
    level: Optional[int] = 1


class GroupStrategy(BaseModel):
    id: str
    door: Optional[dict] = {}


class UserProfile(BaseModel):
    language_code: Optional[str]
    is_bot: Optional[bool]
    is_premium: Optional[bool]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    photo: Optional[str]
    bio: Optional[str]
    time: Union[None, str, int]
    token: Optional[str]
    name: Optional[str]
    id: int


class Commander(BaseModel):
    """
    命令
    """
    level: int = 1
    command: str = "off"
    type: str = "ask"
    info: str

    @validator('info', always=True)
    def check_consistency(cls, v, values):
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v


class GroupProfile(BaseModel):
    """
    param id int

    param bio Optional[str]

    :param user Optional[dict]

    :param keys Optional[int]

    :param times
    """
    id: int
    bio: Optional[str]
    user: Optional[dict]
    # 联盟线
    keys: Optional[int]
    times: Optional[int] = 0


class DataWorker(object):
    """
    Redis 数据基类
    """

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
            return {}

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


class GroupManger(object):
    """
    群组，目前没用
    """

    def __init__(self, groupId: Union[str, int]):
        self.groupId = str(groupId)
        self.DataWorker = DataWorker(prefix="Telecha_Group_")

    def save(self, profile: dict = None, profileObj: GroupProfile = None):
        if not any([profile, profileObj]):
            return False
        if profileObj:
            profile = profileObj.dict()
        return self.DataWorker.setKey(key=self.groupId, obj=profile)

    def read(self) -> Union[dict]:
        _Group = self.DataWorker.getKey(self.groupId)
        return _Group

    def getAllGroup(self):
        return self.DataWorker.getPuffix("Telecha_Group_")


class UserManger(object):
    """
    用户材料更新
    """

    def __init__(self, userId: Union[str, int]):
        self.userId = str(userId)
        self.DataWorker = DataWorker(prefix="Telecha_Users_")

    def save(self, profile: dict = None, profileObj: UserProfile = None):
        if not any([profile, profileObj]):
            return False
        if profileObj:
            profile = profileObj.dict()
        return self.DataWorker.setKey(key=self.userId, obj=profile)

    def read(self) -> Union[dict]:
        _who = self.DataWorker.getKey(self.userId)
        return _who


class GroupStrategyManger(object):
    """
    策略机，提供群组策略的查看
    """

    def __init__(self, groupId: Union[str, int]):
        self.groupId = str(groupId)
        self.DataWorker = DataWorker(prefix="Telecha_GroupStrategy_")

    def save(self, groupStrategy: dict = None, groupStrategyObj: GroupStrategy = None) -> bool:
        if not any([groupStrategy, groupStrategyObj]):
            return False
        if groupStrategyObj:
            groupStrategy = groupStrategyObj.dict()
        return self.DataWorker.setKey(key=self.groupId, obj=groupStrategy)

    def read(self) -> Union[dict]:
        _Strategy = self.DataWorker.getKey(self.groupId)
        return _Strategy


class UserTrackManger(object):
    """
    用户行为持久化机，提供历史数据查看和数据记录功能
    """

    def __init__(self, userId: Union[str, int]):
        self.userId = str(userId)
        self.DataWorker = DataWorker(prefix="Telecha_Tracker_")

    def save(self, _userTrack: dict = None, userTrackObj: UserTrack = None) -> bool:
        if not any([_userTrack, userTrackObj]):
            return False
        if userTrackObj:
            _userTrack = userTrackObj.dict()
        return self.DataWorker.setKey(key=self.userId, obj=_userTrack)

    def read(self) -> Union[dict]:
        _Group = self.DataWorker.getKey(self.userId)
        return _Group

    def getAllHistory(self):
        return self.DataWorker.getPuffix("Telecha_Tracker_")


if __name__ == "__main__":
    default = {
        "scanUser": {
            "spam": {
                "level": 10,
                "command": "ban",
                "type": "on",
                "info": "群组策略:反垃圾系统"
            },
            "premium": {
                "level": 5,
                "command": "pass",
                "type": "off",
                "info": "群组策略:自动通过"
            },
            "nsfw": {
                "level": 4,
                "command": "ask",
                "type": "off",
                "info": "群组策略:色情审查"
            },
            "safe": {
                "level": 1,
                "command": "ban",
                "type": "off",
                "info": "群组策略:安全审查"
            },
            "suspect": {
                "level": 2,
                "command": "ask",
                "type": "off",
                "info": "群组策略:嫌疑识别"
            },
            "politics": {
                "level": 2,
                "command": "ask",
                "type": "off",
                "info": "群组策略:立场审查"
            }
        },
        "afterVerify": {
            "unpass": {
                "level": 5,
                "command": "cancel",
                "type": "on",
                "info": "不通过留看"
            }
        }
    }
    # user = GroupStrategy(**default)

    UserThis = {
        "language_code": None,
        "is_bot": None,
        "is_premium": None,
        "first_name": None,
        "last_name": None,
        "username": None,
        "id": 1,
        "photo": None,
        "bio": None,
        "time": None,
        "token": None,
    }
    users = UserProfile(**UserThis)
    print(users)
    if users.first_name:
        print(0)
