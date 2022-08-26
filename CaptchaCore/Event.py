# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:48 PM
# @FileName: Event.py
# @Software: PyCharm
# @Github    ：sudoskys
import pathlib
from pathlib import Path
import yaml
import time
import json

from rich.console import Console


def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


class botWorker(object):
    def __init__(self):
        pass

    @staticmethod
    def delmsg(bot, chat, message):
        bot.delete_message(chat, message)

    @staticmethod
    def un_restrict(message, bot, groups, un_restrict_all=False):
        if un_restrict_all:
            bot.restrict_chat_member(groups, message.from_user.id, can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_pin_messages=True,
                                     can_change_info=True,
                                     can_send_polls=True,
                                     can_invite_users=True,
                                     can_add_web_page_previews=True,
                                     )
        else:
            bot.restrict_chat_member(groups, message.from_user.id, can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_send_polls=True,
                                     )

    @staticmethod
    def send_ban(message, bot, groups):
        msgss = bot.send_message(groups,
                                 f"刚刚{message.from_user.first_name}没有通过验证，已经被扭送璃月警察局...加入了黑名单！"
                                 f"\n在其不在验证或冷却时禁言来永久封禁\n用户6分钟后从黑名单中保释")
        return msgss

    @staticmethod
    def unbanUser(bot, chat, user):
        msgss = bot.unban_chat_member(chat, user_id=user, only_if_banned=True)
        print("执行了移除黑名单:" + str(user))
        return msgss

    @staticmethod
    def send_ok(message, bot, groups, well_unban):
        if well_unban:
            info = "完全解封"
        else:
            info = "因为被踢出，只保留基本权限"
        msgss = bot.send_message(groups,
                                 f"刚刚{message.from_user.first_name}通过了验证！{info}")
        return msgss

    @staticmethod
    def get_difficulty(cls):
        load_csonfig()
        if _csonfig.get("difficulty_limit") is None:
            _csonfig["difficulty_limit"] = {}
            save_csonfig()
        if _csonfig.get("difficulty_min") is None:
            _csonfig["difficulty_min"] = {}
            save_csonfig()
        limit = _csonfig.get("difficulty_limit").get(str(cls))
        mina = _csonfig.get("difficulty_min").get(str(cls))
        if limit is None:
            limit = 7
        else:
            limit = "".join(list(filter(str.isdigit, limit)))
        if mina is None:
            mina = 1
        else:
            mina = "".join(list(filter(str.isdigit, mina)))
        return mina, limit

    @staticmethod
    def set_difficulty(group_id, difficulty_limit=None, difficulty_min=None):
        load_csonfig()
        if _csonfig.get("difficulty_limit") is None:
            _csonfig["difficulty_limit"] = {}
            save_csonfig()
        if _csonfig.get("difficulty_min") is None:
            _csonfig["difficulty_min"] = {}
            save_csonfig()
        set_difficulty_limit = False
        set_difficulty_min = False
        if not (difficulty_limit is None):
            _csonfig["difficulty_limit"][str(group_id)] = difficulty_limit
            set_difficulty_limit = True
        if not (difficulty_min is None):
            _csonfig["difficulty_min"][str(group_id)] = difficulty_min
            set_difficulty_min = True
        save_csonfig()
        return set_difficulty_min, set_difficulty_limit

    @staticmethod
    def extract_arg(arg):
        return arg.split()[1:]


class yamler(object):
    # sudoskys@github
    def __init__(self):
        self.debug = False
        self.home = Path().cwd()

    def debug(self, log):
        if self.debug:
            print(log)

    def rm(self, top):
        Path(top).unlink()

    def read(self, path):
        if Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                result = yaml.full_load(f.read())
            return result
        else:
            raise Exception("Config dont exists in" + path)

    def save(self, path, Data):
        with open(path, 'w+', encoding='utf-8') as f:
            yaml.dump(data=Data, stream=f, allow_unicode=True)


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tool(object):
    def __init__(self):
        self.console = Console(color_system='256', style=None)
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def dictToObj(self, dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = self.dictToObj(v)
        return d


class Read(object):
    def __init__(self, paths):
        data = yamler().read(paths)
        self.config = Tool().dictToObj(data)

    def get(self):
        return self.config


class Check(object):
    def __init__(self):
        self.file = [
            "/config.json",
            "/Captcha.yaml",
        ]
        self.dir = [
            # "/data",
        ]
        self.inits = [
            "/data/whitelist.user",
            "/data/blacklist.user",
        ]
        self.RootDir = str(pathlib.Path().cwd())

    def mk(self, tab, context, mkdir=True):

        for i in tab:
            if mkdir:
                pathlib.Path(self.RootDir + i).mkdir(parents=True, exist_ok=True)
            else:
                files = pathlib.Path(self.RootDir + i)
                if not files.exists():
                    files.touch(exist_ok=True)
                    if i in self.inits:
                        with files.open("w") as fs:
                            fs.write(context)

    # 禁用此函数
    def initConfig(self, path):
        with open(path, "w") as file:
            file.write("{}")

    def run(self):
        self.mk(self.dir, "{}", mkdir=True)
        self.mk(self.file, "{}", mkdir=False)
