# -*- coding: utf-8 -*-
# @Time    : 8/28/22 11:48 AM
# @FileName: asnc.py
# @Software: PyCharm
# @Github    ：sudoskys
async def verify_step2(message, pipe2):
    try:
        # group, keys = verifyRedis.read_user(str(message.from_user.id))
        # chat_id = message.chat.id
        answer = message.text
        if str(answer) == str(pipe2[1].get("rightKey")):
            botWorker.un_restrict(message, bot, group_k, un_restrict_all=well_unban)
            verifyRedis.grant_resign(message.from_user.id, group_k)
            await bot.reply_to(message, "好险！是正确的答案，如果没有被解封请通知群组管理员～")
            msgss = botWorker.send_ok(message, bot, group_k, well_unban)
            t = Timer(25, botWorker.delmsg, args=[bot, msgss.chat.id, msgss.message_id])
            t.start()
        else:
            if group_k:
                verifyRedis.checker(fail_user=[key])
                # bot.kick_chat_member(group, message.from_user.id)
                await bot.reply_to(message, '回答错误，很抱歉我不能让您进入这个群组...\n6分钟后可以重新进入')
                t = Timer(360, botWorker.unbanUser, args=[bot, group_k, message.from_user.id])
                t.start()
                mgs = botWorker.send_ban(message, bot, group_k)
                t = Timer(30, botWorker.delmsg, args=[bot, mgs.chat.id, mgs.message_id])
                t.start()
    except Exception as e:
        await bot.reply_to(message, f'机器人出错了，请发送日志到项目 Issue ,谢谢你！\n 日志:`{e}`',
                           parse_mode='Markdown')