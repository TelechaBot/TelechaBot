# -*- coding: utf-8 -*-
# @Time    : 11/9/22 8:50 AM
# @FileName: censor.py.py
# @Software: PyCharm
# @Github    ：spirit-yzk
from utils.DfaDetect import DFA
import random
import time

ban_words_set = set()
ban_words_list = list()
example100k = list()


def test_get_words():
    with open('sensitive_words.txt', 'r', encoding='utf-8-sig') as f:
        for s in f:
            if s.find('\\r'):
                s = s.replace('\r', '')
            s = s.replace('\n', '')
            s = s.strip()
            if len(s) == 0:
                continue
            if str(s) and s not in ban_words_set:
                ban_words_set.add(s)
                ban_words_list.append(str(s))
        for _ in range(10000):
            example100k.append(str_generator())


def str_generator():
    str_test = str()
    for _ in range(random.randint(1, 200)):
        if random.random() < 0.1:
            str_test += random.choice(ban_words_list)
        else:
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)
            val = f'{head:x}{body:x}'
            str_test += bytes.fromhex(val).decode('gb2312')
    # print(str_test)
    new_str = str()
    for x in str_test:
        new_str += x
        if random.random() < 0.5:
            new_str += ' '
    # print(new_str)
    return new_str


def test_exists():
    s = "98-广-告-代-发"
    print(dfa.exists(s))
    # assert dfa.exists(s) is True
    # print(dfa.exists(s))
    s = "一个测试哈"
    # print(dfa.exists(s))
    print(dfa.exists(s))


if __name__ == '__main__':
    t1 = time.time() * 100
    dfa = DFA()
    test_exists()
    t2 = time.time() * 100
    print(t2 - t1)
