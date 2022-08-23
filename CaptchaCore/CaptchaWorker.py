# -*- coding: utf-8 -*-
# @Time    : 8/25/22 7:42 PM
# @FileName: ScienceCaptcha.py
# @Software: PyCharm
# @Github    ：sudoskys
# -*- coding: utf-8 -*-
# @Time    : 8/24/22 12:57 AM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
# @Version    ：1
import math
import random

special_angle = [30, 60, 90, 120, 150, 180]

# 难度系数
difficulty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# two basic usage!!
# from random import choice
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(choice(l)) # 随机抽取一个

# print(random.randint(0, 9))

# π


class radius(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 1

    def create(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"一个扇形弧长为{lena}，半径为{r}，求其面积！四舍五入，只答出数字"
        A = (lena * r) / 2
        return Q, round(A)


class find_volume_cone(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 3

    def create(self):
        lena = (random.randint(1, 28) * 3)
        h = (random.randint(1, 20) * 2)

        Q = f"一个圆锥的底面积为{lena}π，高为{h}，求其体积!(四舍五入，只答出数字部分！)"
        A = (lena * h) / 3
        return Q, round(A)


class find_ball_cone(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 2

    def create(self):
        # lena = (random.randint(1, 30) * 3)
        r = (random.randint(1, 14) * 3)
        Q = f"一个球的半径为{r}，求其体积!(四舍五入，只答出数字部分！)"
        A = 4 / 3 * r ** 3
        return Q, round(A)


class gravity_work(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 4

    def create(self):
        # lena = (random.randint(1, 30) * 3)
        g1 = (random.randint(1, 15) * 4)
        g2 = (random.randint(1, 6) * 1)
        long = (random.randint(1, 6) * 1)
        high = (random.randint(1, 6) * 1)
        Q = f"经测量，重{g1}N的物体沿斜面运行时，受到的摩擦力为{g2}N,斜面的长和高分别是{long}和{high}，如果物体从斜面顶部自由滑到底端，重力对物体所做的功和克服摩擦力所做的功的和是(四舍五入)？(只答出数字部分！)"
        A = g1 * high + g2 * long
        return Q, round(A)


class binary_first_equation(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 7

    def create(self):
        # lena = (random.randint(1, 30) * 3)
        a = (random.randint(1, 5) * 1)
        b = (random.randint(8, 15) * 5)
        c = (random.randint(1, 3) * 1)

        def work(a, b, c):
            d = b * b - 4 * a * c
            if d < 0:
                return False, '方程无解'
            else:
                if a == 0:
                    if b == 0:
                        if c == 0:
                            return False, '方程解为全体实数'
                        else:
                            return False, '方程无解'
                    else:
                        x1 = -c / b
                        x2 = x1
                        return x1, x2
                else:
                    x1 = (-b + math.sqrt(d)) / (2 * a)
                    x2 = (-b - math.sqrt(d)) / (2 * a)
                    return True, x1 + x2

        iss, A = work(a, b, c)
        if not iss:
            A = 0
        qustion = f"已知二元一次方程 ax²+bx+c=0，其中a为{a}，b为{b}，c为{c}。求其根的和四舍五入的绝对值。如果无解请写0."
        return qustion, round(abs(A))


class parabola(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 8

    def create(self):
        p = (random.randint(2, 5) * 2)
        a = p * 4 + 2
        Q = f"长度为{a}的线段 AB 的两个端点A、B都在抛物线y2(2次方)={p}x 上滑动，则线段 AB 的中点 M 到 y 轴的最短距离为?(四舍五入)"
        A = (a - p / 2) / 2
        return Q, round(A)


class parabola_2(object):
    def __init__(self):
        pass

    @property
    def difficulty(self):
        return 8

    def create(self):
        num = (random.randint(1, 3) * 2)
        num2 = (random.randint(7, 21) * 4)
        Q = f"若抛物线x2(2次方)=-2py(p>0)上纵坐标为-{num}的点到焦点的距离为{num2}，则焦点到准线的距离是?四舍五入且取绝对值"
        A = (num2 - num) / 2
        return Q, round(A)


class Importer(object):
    def __init__(self):
        self.items = [{"diff": parabola_2().difficulty, "obj": parabola_2()},
                      {"diff": radius().difficulty, "obj": parabola()},
                      {"diff": find_volume_cone().difficulty, "obj": find_volume_cone()},
                      {"diff": find_ball_cone().difficulty, "obj": find_ball_cone()},
                      {"diff": gravity_work().difficulty, "obj": gravity_work()},
                      {"diff": binary_first_equation().difficulty, "obj": binary_first_equation()},
                      ]

    def pull(self, difficulty_limit=5):
        from random import choice
        if difficulty_limit < 1:
            difficulty_limit = 1
        verify_papaer = [i for i in self.items if i.get("diff") <= difficulty_limit]
        verify = (choice(verify_papaer))
        return verify.get("obj")


some = Importer().pull()
print(some.create())
print(some.create()[0])
print(some.create()[1])
