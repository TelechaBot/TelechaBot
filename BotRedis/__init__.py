import json
import pathlib
import time

# 必须需要一个创建机器人对象的类才能使用KickMember功能！

class JsonRedis(object):
    def __init__(self, interval,config):
        self.interval = interval
        JsonRedis.load_tasks()
        if not _tasks.get("Time_id"):
            _tasks["Time_id"] = {}
            JsonRedis.save_tasks()
        if not _tasks.get("Time_group"):
            _tasks["Time_group"] = {}
            JsonRedis.save_tasks()
        if not _tasks.get("User_group"):
            _tasks["User_group"] = {}
            JsonRedis.save_tasks()
        if not _tasks.get("super"):
            _tasks["super"] = {}
            JsonRedis.save_tasks()
        if not _tasks.get("interval"):
            _tasks["interval"] = self.interval
            JsonRedis.save_tasks()

    @staticmethod
    def load_tasks():
        global _tasks
        if pathlib.Path("taskRedis.json").exists():
            with open("taskRedis.json", encoding="utf-8") as f:
                _tasks = json.load(f)
        else:
            _tasks = {}

    @staticmethod
    def save_tasks():
        with open("taskRedis.json", "w", encoding="utf8") as f:
            json.dump(_tasks, f, indent=4, ensure_ascii=False)

    @staticmethod
    def readUser(where, group):
        where = str(where)
        JsonRedis.load_tasks()
        if _tasks.get(where):
            oss = _tasks[where].get(str(group))
            if oss:
                return oss
            else:
                return []
        else:
            return []

    @staticmethod
    def popUser(where, group, key):
        where = str(where)
        JsonRedis.load_tasks()
        if _tasks.get(where):
            if _tasks[where][str(group)]:
                if key in _tasks[where][str(group)]:
                    _tasks[where][str(group)].pop(key)
        JsonRedis.save_tasks()

    @staticmethod
    def saveUser(where, group, key):
        where = str(where)
        JsonRedis.load_tasks()
        if _tasks.get(where):
            if _tasks[where][str(group)]:
                if not (key in _tasks[where][str(group)]):
                    _tasks[where][str(group)].append(key)
            else:
                _tasks[where][str(group)] = []
                _tasks[where][str(group)].append(key)
        else:
            _tasks[where] = {}
            _tasks[where][str(group)] = []
            _tasks[where][str(group)].append(key)
        JsonRedis.save_tasks()

    def add(self, userId, groupId):
        JsonRedis.load_tasks()
        _tasks["Time_id"][str(int(time.time()))] = userId
        _tasks["Time_group"][str(int(time.time()))] = str(groupId)
        JsonRedis.save_tasks()
        JsonRedis.saveUser("User_group", userId, str(int(time.time())))

    def read(self, userId):
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                key = _tasks["User_group"].get(str(userId))[0]
                # user = _tasks["Time_id"].get(key)
                group = _tasks["Time_group"].get(key)
                return group
            else:
                return False
        else:
            return False

    def removed(self, userId, groupId):
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                for key, i in _tasks["Time_group"].items():
                    if i == str(groupId):
                        JsonRedis.checker([key])

    def promote(self, userId, groupId=None):
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                if groupId:
                    for key, i in _tasks["Time_group"].items():
                        if i == str(groupId):
                            JsonRedis.checker([key])
                            JsonRedis.saveUser("super", userId, str(groupId))
                else:
                    key = _tasks["User_group"].get(str(userId))[0]
                    groupId = _tasks["Time_group"].get(key)
                    JsonRedis.checker([key])
                    JsonRedis.saveUser("super", userId, str(groupId))

    @staticmethod
    def run_timer():
        JsonRedis.checker()
        JsonRedis.timer()

    @staticmethod
    def timer():
        from threading import Timer
        t = Timer(3, JsonRedis.run_timer)
        t.start()

    @staticmethod
    def checker(tar=None):
        if tar is None:
            tar = []
            # 豁免名单
        JsonRedis.load_tasks()
        ban = []
        ban = ban + tar
        for key, item in _tasks["Time_id"].items():
            if int(time.time()) - int(key) > int(_tasks["interval"]):
                ban.append(key)
            else:
                pass
                # 用户未过期
                # print("No")
        for key in ban:
            user = _tasks["Time_id"].pop(key)
            group = _tasks["Time_group"].pop(key)
            _tasks["User_group"][str(user)].remove(key)
            if not (key in tar):
                # 过期验证的操作
                from CaptchaCore.Bot import clinetBot
                bot, config =clinetBot().botCreat()
                bot.kick_chat_member(group,user)
                # print("ban " + str(user) + str(group))


        JsonRedis.save_tasks()

    def interval(self):
        return self.interval

#
# JsonRedis(6).add(1222, str(-52333))
#
# JsonRedis.timer()
#
# print(2)
