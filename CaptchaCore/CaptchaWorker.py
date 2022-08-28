# -*- coding: utf-8 -*-
# @Time    : 8/24/22 12:57 AM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
# @Version    ：1
import json
import math
import random
import time
import pathlib
from random import choice

special_angle = [30, 60, 90, 120, 150, 180]

# 难度系数
difficulty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# two basic usage!!
# from random import choice
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(choice(l)) # 随机抽取一个

# print(random.randint(0, 9))

# π
class bili_hard_core(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 8

    def nofind(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    def create(self):
        if pathlib.Path('data/Bili.json').exists():
            with open("data/Bili.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                data_list = samples.get("datas")
                well_data = [i for i in data_list if
                             i.get("answer") in ["A", "B", "C", "D"]]
                key_obj = choice(well_data)
                q = key_obj.get("question")
                a = str(key_obj.get("opt1"))
                b = str(key_obj.get("opt2"))
                c = str(key_obj.get("opt3"))
                d = str(key_obj.get("opt4"))
                Q = f"{q}\n{a}\n{b}\n{c}\n{d}\n请回答 A|B|C|D 选项大写字母"
                A = key_obj.get("answer")
            else:
                Q, A = self.nofind()

        else:
            Q, A = self.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


class car_subject_one(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 5

    def nofind(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    def create(self):

        if pathlib.Path('data/Drive.json').exists():
            with open("data/Drive.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                data_list = samples.get("datas")
                well_data = [i for i in data_list if
                             i.get("answer") in ["A", "B", "C", "D"] and (i.get('pic') is None or i.get('pic') == "")]
                key_obj = choice(well_data)
                q = key_obj.get("question")
                a = str(key_obj.get("opt1"))
                b = str(key_obj.get("opt2"))
                c = str(key_obj.get("opt3"))
                d = str(key_obj.get("opt4"))
                Q = f"{q}\n{a}\n{b}\n{c}\n{d}\n请回答 A|B|C|D 选项大写字母"
                A = key_obj.get("answer")
            else:
                Q, A = self.nofind()

        else:
            Q, A = self.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


# songci
class songci_300(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 5

    def nofind(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    def create(self):

        if pathlib.Path('data/Songci.json').exists():
            with open("data/Songci.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = self.nofind()

        else:
            Q, A = self.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


# lunyun
class lunyu(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 5

    def nofind(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    def create(self):

        if pathlib.Path('data/Lunyu.json').exists():
            with open("data/Lunyu.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = self.nofind()

        else:
            Q, A = self.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


# 学习强国
class study_build_up(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 5

    def nofind(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    def create(self):

        if pathlib.Path('data/XXQG.json').exists():
            with open("data/XXQG.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = self.nofind()

        else:
            Q, A = self.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


class radius(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 1

    def create(self):
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class find_volume_cone(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 3

    def create(self):
        lena = (random.randint(1, 28) * 3)
        h = (random.randint(1, 20) * 2)

        Q = f"一个圆锥的底面积为{lena}π，高为{h}，求其体积为多少π!(四舍五入，只答出数字部分！)"
        A = (lena * h) / 3
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class find_ball_cone(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 2

    def create(self):
        # lena = (random.randint(1, 30) * 3)
        r = (random.randint(1, 14) * 3)
        Q = f"一个球的半径为{r}，求其体积是多少π!(四舍五入，只答出数字部分！)"
        A = 4 / 3 * r ** 3
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class gravity_work(object):
    def __init__(self, sample):
        self.id = sample
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
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class binary_first_equation(object):
    def __init__(self, sample):
        self.id = sample
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
        Q = f"已知二元一次方程 ax²+bx+c=0，其中a为{a}，b为{b}，c为{c}。求其根的和四舍五入的绝对值。如果无解请写0."
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(abs(A))}
        return Question, Answer


class parabola(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 6

    def create(self):
        p = (random.randint(2, 5) * 2)
        a = p * 4 + 2
        Q = f"长度为{a}的线段 AB 的两个端点A、B都在抛物线y2(2次方)={p}x 上滑动，则线段 AB 的中点 M 到 y 轴的最短距离为?(四舍五入)"
        A = (a - p / 2) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class parabola_2(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 8

    def create(self):
        num = (random.randint(1, 3) * 2)
        num2 = (random.randint(7, 21) * 4)
        Q = f"若抛物线x2(2次方)=-2py(p>0)上纵坐标为-{num}的点到焦点的距离为{num2}，则焦点到准线的距离是?四舍五入且取绝对值"
        A = (num2 - num) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class biological_gene(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 7

    def create(self):
        num1 = (random.randint(7, 21) * 4)
        num2 = (random.randint(7, 21) * 4)
        num3 = (random.randint(7, 21) * 4)
        from random import choice
        chos = choice(["A", "a"])
        Q = f"如若二倍体生物的某一基因位点上有一对等位基因A和a，该种群中相关的基因型有AA、Aa、aa，如果他们的个数是{num1, num2, num3}, 则该种群{chos}基因的基因频率是多少？(答出四舍五入取整后的百分数，不带%)"
        if chos == "A":
            An = (2 * num1 + num2) / (2 * (num1 + num2 + num3)) * 100
        else:
            An = (num2 + 2 * num3) / (2 * (num1 + num2 + num3)) * 100
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(An)}
        return Question, Answer


class Importer(object):
    def __init__(self, s=time.time()):
        self.samples = s

        self.items = [{"diff": parabola_2(s).difficulty, "obj": parabola_2(s)},
                      {"diff": radius(s).difficulty, "obj": parabola(s)},
                      {"diff": find_volume_cone(s).difficulty, "obj": find_volume_cone(s)},
                      {"diff": find_ball_cone(s).difficulty, "obj": find_ball_cone(s)},
                      {"diff": gravity_work(s).difficulty, "obj": gravity_work(s)},
                      {"diff": binary_first_equation(s).difficulty, "obj": binary_first_equation(s)},
                      {"diff": biological_gene(s).difficulty, "obj": biological_gene(s)},
                      ]
        self.study = [
            {"diff": study_build_up(s).difficulty, "obj": study_build_up(s)},
        ]
        self.car_subject_one = [
            {"diff": car_subject_one(s).difficulty, "obj": car_subject_one(s)},
        ]
        self.bili_hard_core = [
            {"diff": bili_hard_core(s).difficulty, "obj": bili_hard_core(s)},
        ]

        self.songci_300 = [
            {"diff": songci_300(s).difficulty, "obj": songci_300(s)},
        ]
        self.lunyu = [
            {"diff": lunyu(s).difficulty, "obj": lunyu(s)},
        ]

    def pull(self, difficulty_min=1, difficulty_limit=5, model_name="学科题库"):

        verify = {"diff": biological_gene(time.time()).difficulty, "obj": biological_gene(time.time())}
        if model_name == "学科题库":
            if difficulty_limit < 1 or difficulty_limit < difficulty_min:
                if difficulty_limit < 0:
                    difficulty_limit = 9
                if difficulty_min >= 9:
                    difficulty_min = 1
            verify_papaer = [i for i in self.items if difficulty_min <= i.get("diff") <= difficulty_limit]
            if len(verify_papaer) != 0:
                verify = (choice(verify_papaer))
        elif model_name == "学习强国":
            verify = self.study[0]
        elif model_name == "宋词300":
            verify = self.songci_300[0]
        elif model_name == "论语问答":
            verify = self.lunyu[0]
        elif model_name == "科目一":
            verify = self.car_subject_one[0]
        elif model_name == "哔哩硬核测试":
            verify = self.bili_hard_core[0]
        return verify.get("obj")

# print(biological_gene().create())

###########################
# 如果需要创建不重复对象
# import time
# print(Importer(time.time()).pull().create())
# print(Importer(time.time()).pull().create())
# print(Importer(time.time()).pull().create())
#########################


#
# some =
# print(some.create())
# print(some.create()[0])
# print(some.create()[1])
