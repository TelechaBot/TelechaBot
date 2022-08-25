# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import pathlib
import random
import time
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotRedis import JsonRedis
from threading import Timer
from CaptchaCore.Event import botWorker
import binascii

# from telebot import formatting


# 构建多少秒的验证对象
verifyRedis = JsonRedis(175)


# 全局加载配置
def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


# 存储全局配置
def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


def About(bot, message, config):
    if message.chat.type == "private":
        if config.desc:
            bot.reply_to(message, config.desc)
        else:
            bot.reply_to(message, "生物信息验证 Bot，自主Project:https://github.com/sudoskys/")


# 主控模块
def Switch(bot, message, config):
    userID = message.from_user.id
    load_csonfig()
    if str(userID) == config.ClientBot.owner:
        try:
            command = message.text
            if command == "/show":
                bot.reply_to(message, str(_csonfig))
            if command == "/onw":
                _csonfig["whiteGroupSwitch"] = True
                bot.reply_to(message, "On:whiteGroup")
                save_csonfig()
            if command == "/offw":
                _csonfig["whiteGroupSwitch"] = False
                bot.reply_to(message, "Off:whiteGroup")
                save_csonfig()
            if "/cat" in command:
                for item in command.split()[1:]:
                    path = str(pathlib.Path().cwd()) + "/" + item
                    if pathlib.Path(path).exists():
                        doc = open(path, 'rb')
                        bot.send_document(message.chat.id, doc)
                    else:
                        bot.reply_to(message, "这个文件没有找到....")
            if "/unban" in command:
                def extract_arg(arg):
                    return arg

                if len(command.split()[1:]) == 2:
                    try:
                        botWorker.unbanUser(bot, extract_arg(command)[0], extract_arg(command)[1])
                    except:
                        pass
                    else:
                        bot.reply_to(message, "手动解封了" + str(extract_arg(command)))
            if "/addwhite" in command:
                def extract_arg(arg):
                    return arg.split()[1:]

                for group in extract_arg(command):
                    groupId = "".join(list(filter(str.isdigit, group)))
                    _csonfig["whiteGroup"].append(int(groupId))
                    bot.reply_to(message, '白名单加入了' + str(groupId))
                save_csonfig()
            if "/removewhite" in command:
                def extract_arg(arg):
                    return arg.split()[1:]

                for group in extract_arg(command):
                    groupId = "".join(list(filter(str.isdigit, group)))
                    if int(groupId) in _csonfig["whiteGroup"]:
                        _csonfig["whiteGroup"].remove(int(groupId))
                        bot.reply_to(message, '白名单移除了' + str(groupId))
                if isinstance(_csonfig["whiteGroup"], list):
                    _csonfig["whiteGroup"] = list(set(_csonfig["whiteGroup"]))
                save_csonfig()

        except Exception as e:
            bot.reply_to(message, "Wrong:" + str(e))


def Banme(bot, message, config):
    if len(message.text) == 6:
        if "+banme" == message.text:
            InviteLink = config.link
            # print(InviteLink)
            resign_key = verifyRedis.resign_user(str(message.from_user.id), str(message.chat.id))
            user_ke = str(resign_key) + " " + str("left")
            user_key = binascii.b2a_hex(user_ke.encode('ascii')).decode('ascii')
            InviteLink = config.link + "?start=" + str(user_key)
            bot_link = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
            bot_link.add(
                InlineKeyboardButton("点击这里进行生物验证", url=InviteLink))  # Added Invite Link to Inline Keyboard
            mins = (random.randint(1, 10) * 1)
            msgs = bot.reply_to(message,
                                f" {message.from_user.username} 获得了 {mins} 分钟封锁，俄罗斯转盘模式已经开启, "
                                f"答题可以解锁，不答题会被踢出群组，答错会被踢出群组，等待12分钟.\n管理员手动解封请使用`+unban {message.from_user.id}`",
                                reply_markup=bot_link,
                                parse_mode='Markdown')
            t = Timer(60, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            t.start()
            try:
                # userId = "".join(list(filter(str.isdigit, user)))
                key = verifyRedis.resign_user(str(message.from_user.id), str(message.chat.id))
                # verifyRedis.checker(tar=[key])
                bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False,
                                         can_send_media_messages=False,
                                         can_send_other_messages=False, until_date=message.date + mins * 60)
            except Exception as e:
                pass


# 群组管理员操作命令
def Admin(bot, message, config):
    if "+diff_limit" in message.text and len(message.text) != len("+diff_limit"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_limit=level)
            msgs = bot.reply_to(message, "调整难度上限为:" + str(level))
            t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            t.start()
        else:
            msgs = bot.reply_to(message, "无效参数,必须为数字")
            t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            t.start()
    if "+diff_min" in message.text and len(message.text) != len("+diff_min"):
        status = message.text.split()[1:]
        level = "".join(list(filter(str.isdigit, status[0])))
        if level:
            botWorker.set_difficulty(message.chat.id, difficulty_min=level)
            msgs = bot.reply_to(message, "调整难度下限为:" + str(level))
            t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            t.start()
        else:
            msgs = bot.reply_to(message, "无效参数,必须为数字")
            t = Timer(10, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
            t.start()
    if "+unban" in message.text:
        status = message.text.split()[1:]
        for user in status:
            bot.unban_chat_member(message.chat.id, user_id=user, only_if_banned=True)
            userId = "".join(list(filter(str.isdigit, user)))
            group, key = verifyRedis.read_user(str(userId))
            if group:
                # 机器人核心：通过用户注册请求
                verifyRedis.grant_resign(userId)
                # 解封用户
                bot.restrict_chat_member(message.chat.id, userId, can_send_messages=True,
                                         can_send_media_messages=True,
                                         can_send_other_messages=True)
        # 机器人核心：发送通知并自毁消息
        TIPS = bot.reply_to(message, "手动解禁:从欧几里得家里解救了" + str(status))
        t = Timer(30, botWorker.delmsg, args=[bot, TIPS.chat.id, TIPS.message_id])
        t.start()
    if "+ban" in message.text:
        status = message.text.split()[1:]
        if len(message.text) == 4:
            try:
                if message.reply_to_message.from_user.id:
                    bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)  # .from_user.id)
                    bot.reply_to(message.reply_to_message, f'我已经把{message.reply_to_message.from_user.id}扭送到璃月警察局了！')
            except:
                pass
        for user in status:
            try:
                bot.ban_chat_member(message.chat.id, user)
                bot.reply_to(message.reply_to_message, f'我已经把{user}扭送到璃月警察局了！')
            except Exception as err:
                pass


# 白名单系统
def botSelf(bot, message, config):
    # if bot is added to group
    # old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member" and message.chat.type != "private":
        load_csonfig()
        bot.send_message(message.chat.id,
                         "我是璃月科技的生物验证机器人，负责群内新人的生物验证。\n注意:这个 Bot 需要删除消息和禁用用户的权限才能正常行动")
        if int(message.chat.id) in _csonfig.get("whiteGroup") or abs(int(message.chat.id)) in _csonfig.get(
                "whiteGroup"):
            pass
            # bot.send_message(message.chat.id,
            #                 "Hello bro! i can use high level problem to verify new chat member~~")
        else:
            if _csonfig.get("whiteGroupSwitch"):
                bot.send_message(message.chat.id,
                                 "检查设置发现群组不在白名单之中！...")
                bot.leave_chat(message.chat.id)


def msg_del(bot, message, config):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        if "bot was kicked" in str(e):
            print("Bot被踢出了群组")
        else:
            print(e)
        pass

    # print(cmu.from_user)  # User : The admin who changed the bot's status
    # print(cmu.old_chat_member)  # ChatMember : The bot's previous status
    # print(cmu.new_chat_member)  # ChatMember : The bot's new status


# 启动新用户通知
def member_update(bot, msg, config):
    # if msg.left_chat_member.id != bot.get_me().id:
    old = msg.old_chat_member
    new = msg.new_chat_member
    load_csonfig()

    # print(msg)

    def verify_user(bot, config, statu):
        # 用户操作
        resign_key = verifyRedis.resign_user(str(new.user.id), str(msg.chat.id))
        user_ke = str(resign_key) + " " + str(statu)
        user_key = binascii.b2a_hex(user_ke.encode('ascii')).decode('ascii')
        InviteLink = config.link + "?start=" + str(user_key)
        # print(InviteLink)
        bot_link = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        bot_link.add(
            InlineKeyboardButton("点这里进行生物验证", url=InviteLink))  # Added Invite Link to Inline Keyboard
        msgs = bot.send_message(msg.chat.id,
                                f"{msg.from_user.username}正在申请加入 `{msg.chat.title}`\nPassID:`{user_key}`"
                                f"\n群组ID:`{msg.chat.id}`"
                                f"\n赫免命令`+unban {new.user.id}`",
                                reply_markup=bot_link,
                                parse_mode='Markdown')
        t = Timer(45, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
        t.start()
        try:
            bot.restrict_chat_member(msg.chat.id, new.user.id, can_send_messages=False,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False)
        except Exception as e:
            print(e)
            no_power = bot.send_message(msg.chat.id,
                                        f"对不起，没有权限执行对新用户 `{new.user.id}` 的限制\nPassID:`{user_key}`\nGroupID:`{msg.chat.id}`",
                                        parse_mode='Markdown')
            t = Timer(15, botWorker.delmsg, args=[bot, no_power.chat.id, no_power.message_id])
            t.start()

    ######################################
    if new.status in ["member", "restricted"] and not msg.old_chat_member.is_member and not msg.from_user.is_bot:
        print(str(new.user.id) + "加入了" + str(msg.chat.id))
        if _csonfig.get("whiteGroupSwitch"):
            if int(msg.chat.id) in _csonfig.get("whiteGroup") or abs(int(msg.chat.id)) in _csonfig.get(
                    "whiteGroup"):
                verify_user(bot, config, old.status)
            else:
                if hasattr(config.ClientBot, "contact_details"):
                    contact = config.ClientBot.contact_details
                else:
                    contact = "There is no reserved contact information."
                bot.send_message(msg.chat.id,
                                 f"Bot开启了白名单模式，有人将我添加到此群组，但该群组不在我的白名单中...."
                                 f"请向所有者申请权限...."
                                 f"\nContact details:{contact}"
                                 f'添加白名单命令:`/addwhite {msg.chat.id}`',
                                 parse_mode='Markdown')
                bot.leave_chat(msg.chat.id)
        else:
            verify_user(bot, config, old.status)
        # 启动验证流程
    if new.status in ["left", 'kicked',
                      "restricted"] and not msg.old_chat_member.is_member and not msg.from_user.is_bot:
        # 注销任务
        if new.status in ["kicked", "left", "restricted"]:
            print(str(new.user.id) + "离开了" + str(msg.chat.id))
            verifyRedis.remove_user(new.user.id, str(msg.chat.id))
            # bot.ban_chat_member(msg.chat.id, user_id=new.user.id)


def Start(bot, message, config):
    # bot.reply_to(message, "未检索到你的信息。你无需验证")
    if message.chat.type == "private":
        group_k, key = verifyRedis.read_user(str(message.from_user.id))
        code = botWorker.extract_arg(message.text)
        if len(code) == 1:
            param = binascii.a2b_hex(code[0].encode('ascii')).decode('ascii').split()
            key = param[0]
            statu = param[1]
        else:
            statu = "noparam!"
        if statu in ["member", "left"]:
            well_unban = True
        else:
            well_unban = False
        if group_k:
            bot.reply_to(message,
                         f"开始验证群组 `{group_k}`,你有175秒的时间回答下面的问题...\n\nPassID:`{code[0]}`\nAuthID:`{message.from_user.id}`",
                         parse_mode='Markdown')
            from CaptchaCore import CaptchaWorker
            load_csonfig()
            min_, limit_ = botWorker.get_difficulty(group_k)
            sth = CaptchaWorker.Importer().pull(min_, limit_).create()
            bot.reply_to(message, sth[0] + "\n\n输入 /saveme 重新生成题目")
            print("生成了一道题目:" + str(sth))

            def verify_step2(message, pipe2):
                try:
                    # group, keys = verifyRedis.read_user(str(message.from_user.id))
                    # chat_id = message.chat.id
                    answer = message.text
                    if str(answer) == str(pipe2[1]):
                        botWorker.un_restrict(message, bot, group_k, un_restrict_all=well_unban)
                        verifyRedis.grant_resign(message.from_user.id, group_k)
                        bot.reply_to(message, "好险！是正确的答案，如果没有被解封请通知群组管理员～")
                        msgss = botWorker.send_ok(message, bot, group_k, well_unban)
                        t = Timer(25, botWorker.delmsg, args=[bot, msgss.chat.id, msgss.message_id])
                        t.start()
                    else:
                        if group_k:
                            verifyRedis.checker(fail_user=[key])
                            # bot.kick_chat_member(group, message.from_user.id)
                            bot.reply_to(message, '回答错误，很抱歉我不能让您进入这个群组...\n6分钟后可以重新进入')
                            t = Timer(360, botWorker.unbanUser, args=[bot, group_k, message.from_user.id])
                            t.start()
                            mgs = botWorker.send_ban(message, bot, group_k)
                            t = Timer(30, botWorker.delmsg, args=[bot, mgs.chat.id, mgs.message_id])
                            t.start()
                except Exception as e:
                    bot.reply_to(message, f'机器人出错了，请发送日志到项目 Issue ,谢谢你！\n 日志:`{e}`',
                                 parse_mode='Markdown')

            def verify_step(message, pipe, timea):
                if message.text == "/saveme" and timea > 0:
                    timea = timea - 1
                    if timea == 0:
                        tips = "必须回答"
                    else:
                        tips = f"还可以重置{timea}次."
                    min_, limit_ = botWorker.get_difficulty(group_k)
                    now = limit_ - 2
                    paper = (CaptchaWorker.Importer(s=time.time()).pull(
                        difficulty_min=min_,
                        difficulty_limit=limit_ - 1).create())
                    bot.reply_to(message, paper[0] + f"\n\n输入 /saveme 重新生成题目，目前难度{now},{tips}")
                    print(paper)
                    bot.register_next_step_handler(message,
                                                   verify_step,
                                                   paper,
                                                   timea)
                else:
                    try:
                        # chat_id = message.chat.id
                        answer = message.text
                        # 用户操作
                        # 条件，你需要在这里写调用验证的模块和相关逻辑，调用 veridyRedis 来决定用户去留！
                        if str(answer) == str(pipe[1]):
                            botWorker.un_restrict(message, bot, group_k, un_restrict_all=well_unban)
                            verifyRedis.grant_resign(message.from_user.id, group_k)
                            msgs = botWorker.send_ok(message, bot, group_k, well_unban)
                            bot.reply_to(message, "通过，是正确的答案！如果没有解封请通知管理员～")
                            t = Timer(25, botWorker.delmsg, args=[bot, msgs.chat.id, msgs.message_id])
                            t.start()
                        else:
                            bot.reply_to(message, '可惜是错误的回答....你还有一次机会')
                            bot.register_next_step_handler(message, verify_step2, pipe)
                    except Exception as e:
                        bot.reply_to(message, f'机器人出错了，请发送日志到项目Issue,谢谢你！\n 日志:`{e}`',
                                     parse_mode='Markdown')

            times = 3
            bot.register_next_step_handler(message, verify_step, sth, times)
        else:
            bot.reply_to(message, "数据库内没有你的信息哦，你无需验证！")
    else:
        pass
        # print(0)
