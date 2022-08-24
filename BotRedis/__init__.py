import json
import pathlib
import time


# 必须需要一个创建机器人对象的类才能使用KickMember功能！

class JsonRedis(object):
    def __init__(self, interval):
        JsonRedis.load_tasks()
        if not _tasks.get("interval"):
            if interval:
                _tasks["interval"] = interval
                JsonRedis.save_tasks()
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
            if _tasks[where].get(str(group)):
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
        """
        注册队列
        :param userId:
        :param groupId:
        :return:
        """
        JsonRedis.load_tasks()
        _tasks["Time_id"][str(int(time.time()))] = str(userId)
        _tasks["Time_group"][str(int(time.time()))] = str(groupId)
        JsonRedis.save_tasks()
        JsonRedis.saveUser("User_group", userId, str(int(time.time())))

    def read(self, userId):
        """
        读取用户的注册键
        :param userId:
        :return:
        """
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                key = _tasks["User_group"].get(str(userId))[0]
                # user = _tasks["Time_id"].get(key)
                group = _tasks["Time_group"].get(key)
                return group, key
            else:
                return False, False
        else:
            return False, False

    def removed(self, userId, groupId):
        """
        人员被移除或者退群，弹出对目标群组的验证任务
        :param userId:
        :param groupId:
        :return:
        """
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                for key, i in _tasks["Time_group"].items():
                    if i == str(groupId):
                        JsonRedis.checker(tar=[key])

    def promote(self, userId, groupId=None):
        """
        提升用户并取消过期队列,解禁需要另外语句
        :param userId:
        :param groupId:
        :return:
        """
        User = _tasks["User_group"].get(str(userId))
        if User:
            if len(User) != 0:
                if groupId:
                    for key, i in _tasks["Time_group"].items():
                        if i == str(groupId):
                            JsonRedis.checker(tar=[key])
                            JsonRedis.saveUser("super", str(userId), str(groupId))
                else:
                    key = _tasks["User_group"].get(str(userId))[0]
                    groupId = _tasks["Time_group"].get(key)
                    JsonRedis.checker(tar=[key])
                    JsonRedis.saveUser("super", str(userId), str(groupId))

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
    def checker(tar=None, fail_user=None):
        """
        检查器，调用就会检查一次，弹出传入的键值，
        :param tar: 传入这里，则不踢出而弹出
        :param fail_user: 传入这里，则踢出且弹出
        :return:
        """
        if tar is None:
            tar = []
        if fail_user is None:
            fail_user = []
            # 豁免名单
        ban = []
        ban = ban + tar
        ban = ban + fail_user
        JsonRedis.load_tasks()
        for key, item in _tasks["Time_id"].items():
            if abs(int(time.time()) - int(key)) > int(_tasks["interval"]):
                ban.append(key)
            else:
                pass
                # 用户未过期
                # print("No")
        for key in ban:
            user = _tasks["Time_id"].pop(str(key))
            group = _tasks["Time_group"].pop(str(key))
            try:
                _tasks["User_group"].get(str(user)).remove(str(key))
            except Exception as e:
                print(e)
            if not (key in tar):
                user_something = _tasks["super"].get(str(user))
                if user_something is None:
                    user_something = []
                if not (group in user_something):
                    # 过期验证的操作
                    from CaptchaCore.Bot import clinetBot
                    bot, config = clinetBot().botCreat()
                    try:
                        bot.kick_chat_member(group, user)
                    except Exception as e:
                        print(e)
                    # print("ban " + str(user) + str(group))
        JsonRedis.save_tasks()
        # 同步配置队列

#
# JsonRedis(6).add(1222, str(-52333))
#
# JsonRedis.timer()
#
# print(2)
