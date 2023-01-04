# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:48 PM
# @FileName: Model.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import pathlib
import time
import rtoml
from rich.console import Console
from telebot.asyncio_handler_backends import State, StatesGroup
from loguru import logger


class userStates(StatesGroup):
    answer = State()  # states group should contain states
    answer2 = State()
    is_start = State()


global _csonfig


def load_csonfig():
    global _csonfig
    with open("./Config/config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("./Config/config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


class LogForm(object):
    def __init__(self, bot, logChannel):
        self.__bot = bot
        self.__logChannel = logChannel
        pass

    async def send(self, tag: str, user: int, group: int, msg: str = ""):
        user = str(user)
        group = str(group)
        user = user[:-4] + "****"
        # group = group[:-2] + "**"
        try:
            if self.__logChannel < 0:
                msgss = await self.__bot.send_message(self.__logChannel,
                                                      f"{tag} \n #User{user} -> #Group{str(group).strip('-')} \n{msg}")
        except Exception as e:
            logger.error(f"日志无法发送:{e}")
            return
        else:
            return True


class botWorker(object):
    def __init__(self):
        pass

    @staticmethod
    async def delmsg(chat, message):
        """
        通知 Ban
        :param chat:
        :param message:
        :return:
        """
        from Bot.Controller import clientBot
        bot, config = clientBot().botCreate()
        await bot.delete_message(chat, message)

    @staticmethod
    async def un_restrict(message, bot, groups, un_restrict_all=False):
        if un_restrict_all:
            await bot.restrict_chat_member(groups, message.from_user.id, can_send_messages=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True,
                                           can_pin_messages=True,
                                           can_change_info=True,
                                           can_send_polls=True,
                                           can_invite_users=True,
                                           can_add_web_page_previews=True,
                                           )
        else:
            await bot.restrict_chat_member(groups, message.from_user.id, can_send_messages=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True,
                                           can_send_polls=True,
                                           )

    @staticmethod
    async def unbanUser(bot, chat, user):
        msgss = await bot.unban_chat_member(chat, user_id=user, only_if_banned=True)
        print("执行了移除黑名单:" + str(user))
        # aioschedule.clear(user * abs(chat))
        return msgss

    @staticmethod
    def new_member_checker(msg):
        need = True
        old = msg.old_chat_member
        new = msg.new_chat_member
        info = None
        # 机器人
        if old.user.is_bot:
            need = False
        if new.user.is_bot:
            # print(new.status)
            need = False
            if new.status in ["member"] and old.status not in ["member"]:
                userName = botWorker.convert(msg.from_user.first_name)
                botName = botWorker.convert(new.user.username)
                info = {"text": f"{userName}向群组添加了同类 {botName}", "id": str(new.user.id),
                        "group": str(msg.chat.id)}
        if msg.from_user.is_bot:
            need = False
        # 被踢出的
        if new.status in ["kicked", 'left']:
            need = False
        # 被禁言的
        if new.status in ["restricted"] and old.status in ["member", 'restricted'] and msg.old_chat_member.is_member:
            need = False
        # 成员变动
        if msg.old_chat_member.is_member:
            need = False
        # 管理变动处理
        if old.status in ["administrator", "creator"] or new.status in ["administrator", "left", "creator"]:
            need = False
        return need, info

    @staticmethod
    def convert(texts):
        text = str(texts)
        chars = "_*[]()~`>#+-=|{','}.!'"
        for c in chars:
            text = text.replace(c, "\\" + c)
        # In all other places characters '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{',
        # '}', '.', '!' must be escaped with the preceding character '\'.
        return text

    @staticmethod
    def get_model(cls):
        load_csonfig()
        if _csonfig.get("Model") is None:
            _csonfig["Model"] = {}
            save_csonfig()
        Model = _csonfig.get("Model").get(str(cls))
        if Model is None:
            Model = "数学题库"
        return Model

    @staticmethod
    def set_model(group_id, model=None):
        load_csonfig()
        if _csonfig.get("Model") is None:
            _csonfig["Model"] = {}
            save_csonfig()
        OK = False
        if not (model is None):
            _csonfig["Model"][str(group_id)] = model
            OK = True
        save_csonfig()
        return OK

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

    @staticmethod
    async def checkGroup(bot, msg, config):
        load_csonfig()
        if _csonfig.get("whiteGroupSwitch"):
            if int(msg.chat.id) in _csonfig.get("whiteGroup") or abs(int(msg.chat.id)) in _csonfig.get(
                    "whiteGroup"):
                return True
            else:
                if hasattr(config.ClientBot, "contact_details"):
                    contact = botWorker.convert(config.ClientBot.contact_details)
                else:
                    contact = "There is no reserved contact information."
                info = f"Bot开启了白名单模式，有人将我添加到此群组，但该群组不在我的白名单中...."
                f"请向所有者申请权限...."
                f"\nContact details:{contact}"
                f'添加白名单命令:`/addwhite {msg.chat.id}`'
                await bot.send_message(msg.chat.id,
                                       botWorker.convert(info),
                                       parse_mode='MarkdownV2')
                await bot.leave_chat(msg.chat.id)
                return False
        else:
            return True


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tool(object):
    def __init__(self):
        """
        基本工具类
        """
        self.console = Console(color_system='256', style=None)
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def dictToObj(self, dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = self.dictToObj(v)
        return d


class ReadConfig(object):
    def __init__(self, config=None):
        """
        read some further config!

        param paths: the file path
        """
        self.config = config

    def get(self):
        return self.config

    def parseFile(self, paths):
        data = rtoml.load(open(paths, 'r'))
        self.config = Tool().dictToObj(data)
        return self.config

    def parseDict(self, data):
        self.config = Tool().dictToObj(data)
        return self.config


class Check(object):
    def __init__(self):
        self.file = [
            "/Config/config.json",
            "/Config/Captcha.toml",
        ]
        self.dir = [
            "/Data",
            "/TTS",
        ]
        self.inits = [
            "/Config/config.json"
        ]
        self.RootDir = str(pathlib.Path().cwd())

    def mk(self, tab: list, context: dict, is_dir: bool = True):
        for i in tab:
            if is_dir:
                pathlib.Path(self.RootDir + i).mkdir(parents=True, exist_ok=True)
            else:
                files = pathlib.Path(self.RootDir + i)
                if not files.exists():
                    files.touch(exist_ok=True)
                    # 初始化内容
                    if i in self.inits and context.get(i):
                        with files.open("w") as fs:
                            fs.write(context.get(i))

    def run(self):
        init_config = {
            "./Config/config.json": """
{
    "statu": true,
    "whiteGroupSwitch": false,
    "Model": {
    },
    "difficulty_limit": {},
    "difficulty_min": {},
    "whiteGroup": [
    ],
    "GroupStrategy": {
    },
    "antiSpam": {
    },
    "casSystem": {
    }
}
            """
        }
        self.mk(self.dir, {}, is_dir=True)
        self.mk(self.file, init_config, is_dir=False)
