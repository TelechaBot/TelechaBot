# -*- coding: utf-8 -*-
# @Time    : 11/8/22 5:06 PM
# @FileName: nudeDetect.py
# @Software: PyCharm
# @Github    ：sudoskys
import time

from utils.safeDetect import Nude

t1 = time.time()
n = Nude("./TestData/safe.jpg")
n.parse()
print(n.result)
n = Nude("./TestData/nude.jpg")
n.parse()
print(n.result)
t2 = time.time()

print(t2 - t1)
