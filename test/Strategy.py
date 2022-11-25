# -*- coding: utf-8 -*-
# @Time    : 11/25/22 1:56 PM
# @FileName: Strategy.py
# @Software: PyCharm
# @Github    ：sudoskys
from utils.ChatSystem import strategyUtils

lr = strategyUtils(groupId="5").getDoorStrategy()

print(lr)

output = {'spam': {'level': 10, 'command': 'ban', 'type': 'on', 'info': '群组策略:反垃圾系统'},
          'premium': {'level': 5, 'command': 'pass', 'type': 'off', 'info': '群组策略:会员机制'},
          'nsfw': {'level': 4, 'command': 'ask', 'type': 'off', 'info': '群组策略:色情审查'},
          'safe': {'level': 1, 'command': 'ban', 'type': 'off', 'info': '群组策略:安全审查'},
          'suspect': {'level': 2, 'command': 'ask', 'type': 'off', 'info': '群组策略:嫌疑识别'},
          'politics': {'level': 2, 'command': 'ask', 'type': 'off', 'info': '群组策略:立场审查'}}
