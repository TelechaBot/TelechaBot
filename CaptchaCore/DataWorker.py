# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:41 PM
# @FileName: DataWorker.py
# @Software: PyCharm
# @Github    ：sudoskys
import json


def load_csonfig():
    global _csonfig
    with open("config.json", encoding="utf-8") as f:
        _csonfig = json.load(f)


def save_csonfig():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_csonfig, f, indent=4, ensure_ascii=False)


# 支持三层读取创建操作并且不报错！
def readUser(where, group):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        oss = _csonfig[where].get(group)
        if oss:
            return oss
        else:
            return []
    else:
        return []


def popUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        if _csonfig[where].get(group):
            if key in _csonfig[where][str(group)]:
                _csonfig[where][str(group)].remove(key)
    save_csonfig()


def saveUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_csonfig()
    if _csonfig.get(where):
        if _csonfig[where].get(group):
            if not key in _csonfig[where][str(group)]:
                _csonfig[where][str(group)].append(key)
        else:
            _csonfig[where][str(group)] = []
            _csonfig[where][str(group)].append(key)
    else:
        _csonfig[where] = {}
        _csonfig[where][str(group)] = []
        _csonfig[where][str(group)].append(key)
    save_csonfig()
