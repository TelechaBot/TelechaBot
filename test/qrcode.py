# -*- coding: utf-8 -*-
# @Time    : 11/8/22 4:30 PM
# @FileName: qrcode.py.py
# @Software: PyCharm
# @Github    ：sudoskys
# import cv2
# import os
# img = cv2.imread("001.png")
# # cv2.imshow("imge", img)
# det = cv2.QRCodeDetector()
# val, pts, st_code = det.detectAndDecode(img)
# print(val)

import zxing
reader = zxing.BarCodeReader()
barcode = reader.decode("TestData/qrcode3.png")
if barcode.format:
    print(barcode.format)
