# -*- coding: utf-8 -*-
# @Time    : 9/29/22 10:04 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys
import datetime
import json
import time
import redis
import uuid
import multiprocessing

task_lock = multiprocessing.Lock()
_redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
_MsgTask = {}


class JsonRedis(object):

    @staticmethod
    def start():
        """
        全内存队列设计，操作全局变量的同时做到中断重载
        优化在于深度遍历
        """
        # 如果没有消息，就尝试继承上次的消息队列
        global _MsgTask, task_lock
        try:
            task_lock.acquire()
            if len(_MsgTask) == 0:
                if Course := _redis.get("_Telecha_Task"):
                    _MsgTask = json.loads(Course)
                    # print("队列:初始化上次检查的数据")
        except Exception as err:
            raise err
        finally:
            task_lock.release()

    @staticmethod
    def create_data(user_id: str, group_id: str):
        """
        创建一个新的用户档案，使用当前时间值作为键名。
        :param user_id:
        :param group_id:

        :return: key ,data 返回dict仿api字段,只许str类型键
        """
        if not user_id:
            raise KeyError("not found user_id")
        if not group_id:
            raise KeyError("not found group_id")
        group_id = str(group_id)
        user_id = str(user_id)
        # 上版的时间戳导致了重复的几率，所以采用新的队列算法
        _time = str(int(time.time()))
        _uukey = uuid.uuid5(uuid.NAMESPACE_DNS, f"{user_id}{group_id}")
        return f"Task_{user_id}_{group_id}", {"user": user_id,
                                              "group": group_id,
                                              "time": _time,
                                              "uuid": str(_uukey),
                                              "interval": 200,
                                              }

    @staticmethod
    def read_user(userId: int):
        """
        从队列取出一个数据！
        :param userId: 用户 ID
        :return: 返回 groupId，和 key
        """
        global _MsgTask, task_lock
        try:
            task_lock.acquire()
            groupKey = False
            key = False
            for item in _MsgTask:
                _Data = _MsgTask[item]
                if str(_Data.get("user")) == str(userId):
                    groupKey = _Data.get("group")
                    key = _Data.get("uuid")
            return groupKey, key
        except Exception as err:
            raise err
        finally:
            task_lock.release()

    @staticmethod
    def resign_user(userId: int, groupId: int):
        global _MsgTask, task_lock
        try:
            task_lock.acquire()
            request_ = {"user_id": userId, "group_id": groupId}
            _key, _profile = JsonRedis.create_data(**request_)
            if not _MsgTask.get(_key):
                _MsgTask[_key] = _profile
                return _profile.get("uuid")
            else:
                return _MsgTask.get(_key).get("uuid")
        except Exception as err:
            raise err
        finally:
            task_lock.release()

    @staticmethod
    async def grant_resign(userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _data = JsonRedis.create_data(**request_)
        if Data := _MsgTask.get(_key):
            await JsonRedis.checker(unban=[_data])
            return Data.get("uuid")
        else:
            return "没有记录"

    @staticmethod
    async def remove_user(userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _data = JsonRedis.create_data(**request_)
        await JsonRedis.checker(dismiss=[_data])

    @staticmethod
    async def checker(ban=None, unban=None, dismiss=None):
        global _MsgTask, task_lock
        if dismiss is None:
            dismiss = []
        if unban is None:
            unban = []
        if ban is None:
            ban = []
        # 筛选数据
        for key in _MsgTask:
            _data = _MsgTask[key]
            if abs(int(time.time()) - int(_data["time"])) > int(_data["interval"]):
                ban.append({"user": _data["user"], "group": _data["group"]})
        # 先处理掉 dismiss 的数据，然后对数据进行检查，添加到执行队列封杀
        try:
            for key in unban:
                profile = key
                userId = profile.get("user")
                groupId = profile.get("group")
                from Bot.Controller import clientBot
                bot, config = clientBot().botCreate()
                await bot.delete_state(userId, groupId)
                await bot.approve_chat_join_request(chat_id=groupId, user_id=userId)
            for key in ban:
                profile = key
                userId = profile.get("user")
                groupId = profile.get("group")
                # print(f"释放{uuid}，{userId}-{groupId}")
                if groupId and userId:
                    from Bot.Controller import clientBot
                    bot, config = clientBot().botCreate()
                    await bot.delete_state(userId, groupId)
                    await bot.decline_chat_join_request(chat_id=groupId, user_id=userId)
                    await bot.ban_chat_member(chat_id=groupId, user_id=userId,
                                              until_date=datetime.datetime.timestamp(
                                                  datetime.datetime.now() + datetime.timedelta(minutes=12)))
                    await bot.send_message(userId, f"验证失败或超时，此群组会话验证需要冷却 12 分钟")
        except Exception as err:
            print(err)

        # 释放数据
        try:
            task_lock.acquire()
            allL = []
            allL.extend(ban)
            allL.extend(dismiss)
            allL.extend(unban)
            # print(allL)
            for key in allL:
                profile = key
                userId = profile.get("user")
                groupId = profile.get("group")
                _key = JsonRedis.crateKey(user_id=userId, group_id=groupId)
                _MsgTask.pop(_key, None)
        except Exception as err:
            raise err
        finally:
            task_lock.release()
            _redis.set("_Telecha_Task", json.dumps(_MsgTask))

    @staticmethod
    def crateKey(user_id, group_id):
        return f"Task_{user_id}_{group_id}"
