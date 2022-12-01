# -*- coding: utf-8 -*-
# @Time    : 11/25/22 1:56 PM
# @FileName: Strategy.py
# @Software: PyCharm
# @Github    ：sudoskys
from utils.ChatSystem import strategyUtils, UserTrackUtils
from utils.DataManager import CommandTable

lr = strategyUtils(groupId="5").getDoorStrategy()

# print(lr)

output = {'spam': {'level': 10, 'command': 'ban', 'type': 'on', 'info': '群组策略:反垃圾系统'},
          'premium': {'level': 5, 'command': 'pass', 'type': 'off', 'info': '群组策略:会员机制'},
          'nsfw': {'level': 4, 'command': 'ask', 'type': 'off', 'info': '群组策略:色情审查'},
          'safe': {'level': 1, 'command': 'ban', 'type': 'off', 'info': '群组策略:安全审查'},
          'suspect': {'level': 2, 'command': 'ask', 'type': 'off', 'info': '群组策略:嫌疑识别'},
          'politics': {'level': 2, 'command': 'ask', 'type': 'off', 'info': '群组策略:立场审查'}}
lr = CommandTable.GroupUtils_default(userId="1", groupId="1")

# print(lr)

_T = UserTrackUtils(userId="3")
# lr = _T.resignGroup(groupId="-3", status="ban")
# lr = _T.resignGroup(groupId="-3", status="timeout")
# lr = _T.resignGroup(groupId="-3", status="pass")
# lr = _T.resignGroup(groupId="-3", status="pass")
# lr = _T.resignGroup(groupId="-3", status="pass")
# lr = _T.resignGroup(groupId="-4", status="timeout")
# lr = _T.resignGroup(groupId="-4", status="timeout")
# lr = _T.resignGroup(groupId="-4", status="timeout")
# lr = _T.resignGroup(groupId="-4", status="timeout")
lr = _T.getGroupHistory(groupId="-4")
print(lr)

lr = _T.isBaka(groupId="-4")

print(lr)

u = {'1': [{'time': 112, 'result': 'ban', 'username': ''}], '-1': None,
     '-2': [{'time': 1669389844, 'result': 'ban', 'username': 'init'},
            {'time': 1669389870, 'result': 'ban', 'username': 'init'},
            {'time': 1669389872, 'result': 'ban', 'username': 'init'},
            {'time': 1669389873, 'result': 'ban', 'username': 'init'},
            {'time': 1669389874, 'result': 'ban', 'username': 'init'},
            {'time': 1669389875, 'result': 'ban', 'username': 'init'},
            {'time': 1669389876, 'result': 'ban', 'username': 'init'},
            {'time': 1669389877, 'result': 'ban', 'username': 'init'},
            {'time': 1669389877, 'result': 'ban', 'username': 'init'}]}
r = [{'time': 1669389844, 'result': 'ban', 'username': 'init'},
     {'time': 1669389870, 'result': 'ban', 'username': 'init'},
     {'time': 1669389872, 'result': 'ban', 'username': 'init'},
     {'time': 1669389873, 'result': 'ban', 'username': 'init'},
     {'time': 1669389874, 'result': 'ban', 'username': 'init'},
     {'time': 1669389875, 'result': 'ban', 'username': 'init'},
     {'time': 1669389876, 'result': 'ban', 'username': 'init'},
     {'time': 1669389877, 'result': 'ban', 'username': 'init'},
     {'time': 1669389877, 'result': 'ban', 'username': 'init'}]
