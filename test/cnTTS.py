# -*- coding: utf-8 -*-
# @Time    : 12/1/22 8:11 PM
# @FileName: cnTTS.py
# @Software: PyCharm
# @Github    ：sudoskys

from gtts import gTTS


def GetText(seed: int):
    import random
    from faker import Faker
    faker = Faker("zh_CN")  # 设置中文
    Faker.seed(seed)
    _answer = faker.words(nb=4)
    answer = "".join(_answer)
    _random_int = random.randint(seed * 2, seed * 4)  # 噪音
    Faker.seed(_random_int)
    _noise = faker.words(nb=10)
    noise = list(set(_noise + _answer))
    random.shuffle(noise)
    return answer, noise


print(GetText(100))
# tts.save('hello.mp3')
