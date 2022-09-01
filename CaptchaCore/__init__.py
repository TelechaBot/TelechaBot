# -*- coding: utf-8 -*-
# @Time    : 8/29/22 9:23 AM
# @FileName: Redis.py
# @Software: PyCharm
# @Github    ：sudoskys

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


# 学习强国
class Chemical_verification(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 8

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        Pic = None
        if pathlib.Path('Data/PubChems.json').exists():
            with open("Data/PubChems.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Qn = key_obj[0]
                Q = Qn + "\n\n输入大写选项字母"
                An = (samples[Qn])
                A = An.get("Answer")
                Pic = An.get("Pic")
            else:
                Q, A = study_build_up.nofind()

        else:
            Q, A = study_build_up.nofind()
        Question = {"question": Q, "picture": Pic}
        Answer = {"rightKey": A}
        return Question, Answer


class Tool_CaptchaCore(object):
    def __init__(self):
        pass

    @staticmethod
    def peiping(one=None, two=None):
        from chempy import balance_stoichiometry
        if one is None or two is None:
            print("请输入正确的化学方程式。格式:\n/peiping+你的化学方程式,反应物与生成物之间使用空格连接")
            return False, False
        else:
            try:
                reac = set(one.split("+"))
                prod = set(two.split("+"))
                reac, prod = balance_stoichiometry(reac, prod)
                # print("反应物为: " + str(dict(reac)) + "\n生成物为: " + str(dict(prod)))
                return reac, prod
            except Exception as error:
                print(f"出现错误: {str(error)}")
                return False, False

    @staticmethod
    def drawPic(news_content, font='simkai.ttf', filename="temp.png"):
        if pathlib.Path(filename).exists():
            from PIL import Image, ImageDraw, ImageFont  # 引入图片，画图笔，图片字体三个库
            news_content = news_content.splitlines()  # 按行分割
            import textwrap  # 手动换行文字
            news_wrap = []
            for line in news_content:
                if len(line) < 4:
                    continue
                elif len(line) < 25:
                    news_wrap.append(line)  # 添加到数组中
                else:  # 若字数大于25个字
                    wrap = textwrap.wrap(line, 25)  # 按每行25个字分割成数组
                    news_wrap = news_wrap + wrap
            IMG_SIZE = (920, len(news_wrap) * 60)  # 图片尺寸
            img_1 = Image.new('RGB', IMG_SIZE, (255, 255, 255))  # 底色三个255表示纯白
            draw = ImageDraw.Draw(img_1)  # 创建一个画笔

            header_position = (60, 30)
            header_font = ImageFont.truetype(font, 55)
            current_height = 100
            for line in news_wrap:
                if line.startswith('【'):
                    news_font = ImageFont.truetype(font, 45)  # 标题的字体楷体，字号50
                    draw.text((60, current_height + 30), line, '#726053', news_font)
                    current_height += 80
                else:
                    news_font = ImageFont.truetype(font, 30)
                    draw.text((60, current_height), line, '#726053', news_font)
                    current_height += 40

            img_1.save(filename)
            return filename
        else:
            return False


# π
class bili_hard_core(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 8

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/Bili.json').exists():
            with open("Data/Bili.json", 'r') as tiku_file:
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
                Q, A = bili_hard_core.nofind()

        else:
            Q, A = bili_hard_core.nofind()
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": A}
        return Question, Answer


class chemical_formula(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 8

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        # rsd = (random.randint(1, 5) * 1)
        sde = (random.randint(2, 6) * 1)
        rse = (random.randint(1, 4) * 2)
        inputs = f"P{sde}+H2O"
        output = "PH4+H3PO4"
        key = "PH4"
        tip_key = "H2O"
        input_, samples = Tool_CaptchaCore.peiping(one=inputs, two=output)
        tip = input_.get(tip_key)
        if samples:
            Q = f"现在有 {inputs}={output} 这个没有配平的化学方程式，不考虑是否合理的情况下，前面的{tip_key}的系数为{tip}请问方程式后半段的 {key} 的系数是多少？(答出数字)"
            A = samples.get(key)
        else:
            Q, A = chemical_formula.nofind()
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

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/Drive.json').exists():
            with open("Data/Drive.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                data_list = samples.get("datas")
                well_data = [i for i in data_list if
                             i.get("answer") in ["A", "B", "C", "D"] and (i.get('pic') is None or i.get('pic') == "")]
                random.shuffle(well_data)
                key_obj = choice(well_data)
                q = key_obj.get("question")
                a = str(key_obj.get("opt1"))
                b = str(key_obj.get("opt2"))
                c = str(key_obj.get("opt3"))
                d = str(key_obj.get("opt4"))
                Q = f"{q}\n{a}\n{b}\n{c}\n{d}\n请回答 A|B|C|D 选项大写字母"
                A = key_obj.get("answer")
            else:
                Q, A = car_subject_one.nofind()

        else:
            Q, A = car_subject_one.nofind()
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

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/Songci.json').exists():
            with open("Data/Songci.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = songci_300.nofind()

        else:
            Q, A = songci_300.nofind()
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

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/Lunyu.json').exists():
            with open("Data/Lunyu.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = lunyu.nofind()

        else:
            Q, A = lunyu.nofind()
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

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"NoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/XXQG.json').exists():
            with open("Data/XXQG.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                key_obj = random.sample(samples.keys(), 1)
                Q = key_obj[0]
                A = (samples[Q])
            else:
                Q, A = study_build_up.nofind()

        else:
            Q, A = study_build_up.nofind()
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

    @staticmethod
    def create():
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

    @staticmethod
    def create():
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

    @staticmethod
    def create():
        # lena = (random.randint(1, 30) * 3)
        r = (random.randint(1, 14) * 3)
        Q = f"一个球的半径为{r}，求其体积是多少π!(四舍五入，只答出数字部分！)"
        A = 4 / 3 * r ** 3
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class cosmic_speed(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 6

    @staticmethod
    def create():
        # lena = (random.randint(1, 30) * 3)
        bei = (random.randint(1, 15) * 1)
        radius_ = (random.randint(1, 5) * 1)
        Q = f"若取地球的第一宇宙速度为8km/s，缇茶所在的机器人星球的质量是地球的{bei}倍，半径是地球的{radius_}倍，则此行星的第一宇宙速度约为(回答四舍五入后的数字答案！)"
        A = pow(bei / pow(radius_, 2) * radius_, 0.5) * 8

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

    @staticmethod
    def create():
        # lena = (random.randint(1, 30) * 3)
        g1 = (random.randint(1, 15) * 4)
        g2 = (random.randint(1, 6) * 1)
        long = (random.randint(1, 6) * 1)
        high = (random.randint(1, 6) * 1)
        Q = f"经测量，重{g1}N的物体沿斜面运行时，受到的摩擦力为{g2}N,斜面的长和高分别是{long}和{high}，" \
            f"如果物体从斜面顶部自由滑到底端，重力对物体所做的功和克服摩擦力所做的功的和是(四舍五入)？(只答出数字部分！)"
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

    @staticmethod
    def create():
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
        Q = f"已知二元一次方程 ax²+bx+c=0，其中a为{a}，b为{b}，c为{c}。求其两根的和四舍五入后的绝对值。如果无解请写0."
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

    @staticmethod
    def create():
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

    @staticmethod
    def create():
        num = (random.randint(1, 3) * 2)
        num2 = (random.randint(7, 21) * 4)
        Q = f"若抛物线x2(2次方)=-2py(p>0)上纵坐标为-{num}的点到焦点的距离为{num2}，则焦点到准线的距离是?四舍五入且取绝对值"
        A = (num2 - num) / 2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class biological_Flag_Recap(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 3

    @staticmethod
    def create():
        once = (random.randint(10, 15) * 5)
        twice = round(once / (random.randint(1, 5) * 1))
        scend = abs(twice - (random.randint(1, 5) * 1))
        Q = f"用标志重捕法来估计某个种群的个体数量，例如在对某种鼠群的种群密度的调查中，第一次捕获并标志{once}只，第二次捕获{twice}只，其中有标志鼠{scend}只，则对该种群的数量估计，该种群数量大约为多少只？(答出数字)"
        A = (twice * once) / scend
        # A = 128 * (num1 + num2) - 18 * num2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class biological_protein(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 3

    @staticmethod
    def create():
        num1 = (random.randint(2, 5) * 1)
        num2 = (random.randint(7, 21) * 2)
        Q = f"已知20种氨基酸的平均分子量是128，现有一蛋白质分子由{num1}条多肽链组成，共有肽键{num2}个，此蛋白质分子量是?(答出数字)"
        A = 128 * (num1 + num2) - 18 * num2
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


class biological_DNA(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 3

    @staticmethod
    def create():
        num1 = (random.randint(7, 21) * 2)
        Q = f"一段DNA有{num1}对碱基对，请问它可以储藏多少种遗传信息？(答出数字)"
        A = num1 * 4
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

    @staticmethod
    def create():
        num1 = (random.randint(7, 21) * 4)
        num2 = (random.randint(7, 21) * 4)
        num3 = (random.randint(7, 21) * 4)
        from random import choice
        chos = choice(["A", "a"])
        Q = f"如若二倍体生物的某一基因位点上有一对等位基因A和a，该种群中相关的基因型有AA、Aa、aa，如果他们的个数是{num1, num2, num3}, " \
            f"则该种群{chos}基因的基因频率是多少？(答出四舍五入取整后的百分数，不带%)"
        if chos == "A":
            An = (2 * num1 + num2) / (2 * (num1 + num2 + num3)) * 100
        else:
            An = (num2 + 2 * num3) / (2 * (num1 + num2 + num3)) * 100
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(An)}
        return Question, Answer


class Combustion_Calculations(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 4

    @staticmethod
    def create():
        Cx = (random.randint(1, 9) * 4)
        Hx = Cx * 4 - (random.randint(1, 2) * 4)
        Q = f"1mol 有机物 C{Cx}H{Hx} 完全燃烧消耗多少mol氧气？(只答出数字并四舍五入)"
        A = Cx + (Hx / 4)
        Question = {"question": Q, "picture": None}
        Answer = {"rightKey": round(A)}
        return Question, Answer


# --------------------------------

def Chemistry_Pic(s):
    Chemistry_Pic = [
        {"diff": Chemical_verification(s).difficulty,
         "obj": Chemical_verification(s).create()},

    ]
    return Chemistry_Pic


def Chemistry(s):
    Chemistry = [
        {"diff": Combustion_Calculations(s).difficulty,
         "obj": Combustion_Calculations(s).create()},
        {"diff": chemical_formula(s).difficulty,
         "obj": chemical_formula(s).create()},

    ]
    return Chemistry


def Biology(s):
    Biology = [
        {"diff": biological_gene(s).difficulty, "obj": biological_gene(s).create()},
        {"diff": biological_DNA(s).difficulty, "obj": biological_DNA(s).create()},
        {"diff": biological_protein(s).difficulty, "obj": biological_protein(s).create()},
        {"diff": biological_Flag_Recap(s).difficulty, "obj": biological_Flag_Recap(s).create()},

    ]
    return Biology


def Mathematics(s):
    Mathematics = [
        {"diff": find_volume_cone(s).difficulty, "obj": find_volume_cone(s).create()},
        {"diff": find_ball_cone(s).difficulty, "obj": find_ball_cone(s).create()},
        {"diff": binary_first_equation(s).difficulty, "obj": binary_first_equation(s).create()},
        {"diff": parabola_2(s).difficulty, "obj": parabola_2(s).create()},
        {"diff": parabola(s).difficulty, "obj": parabola(s).create()},
        {"diff": radius(s).difficulty, "obj": radius(s).create()},
    ]
    return Mathematics


def Physics(s):
    Physics = [
        {"diff": gravity_work(s).difficulty, "obj": gravity_work(s).create()},
        {"diff": cosmic_speed(s).difficulty, "obj": cosmic_speed(s).create()},
    ]
    return Physics


def study(s):
    study = [
        {"diff": study_build_up(s).difficulty, "obj": study_build_up(s).create()},
    ]
    return study


def car_subject(s):
    car_subject = [
        {"diff": car_subject_one(s).difficulty, "obj": car_subject_one(s).create()},
    ]
    return car_subject


def bili(s):
    bili = [
        {"diff": bili_hard_core(s).difficulty, "obj": bili_hard_core(s).create()},
    ]
    return bili


def Songci(s):
    songci = [
        {"diff": songci_300(s).difficulty, "obj": songci_300(s).create()},
    ]
    return songci


def Lunyu(s):
    lunyus = [
        {"diff": lunyu(s).difficulty, "obj": lunyu(s).create()},
    ]
    return lunyus


class Importer(object):
    def __init__(self, s=time.time()):
        self.samples = s

    @staticmethod
    def reset(difficulty_min, difficulty_limit):
        if difficulty_limit < 1 or difficulty_limit < difficulty_min:
            if difficulty_limit < 0:
                difficulty_limit = 9
            if difficulty_min >= 9:
                difficulty_min = 1
        return difficulty_min, difficulty_limit

    @staticmethod
    def getMethod():
        return ["数学题库", "物理题库", "化学题库", "生物题库", "图形化学", "学习强国", "宋词300", "论语问答", "科目一", "哔哩硬核测试"]

    def pull(self, difficulty_min=1, difficulty_limit=5, model_name="数学题库"):
        difficulty_min = int(difficulty_min)
        difficulty_limit = int(difficulty_limit)
        verify = {"diff": binary_first_equation(time.time()).difficulty,
                  "obj": binary_first_equation(time.time()).create()}
        difficulty_min, difficulty_limit = Importer.reset(difficulty_min, difficulty_limit)
        if model_name == "数学题库":
            verify_papaer = [i for i in Mathematics(self.samples) if
                             difficulty_min <= i.get("diff") <= difficulty_limit]
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))
            else:
                verify = {"diff": binary_first_equation(time.time()).difficulty,
                          "obj": binary_first_equation(time.time()).create()}
        elif model_name == "物理题库":
            verify_papaer = [i for i in Physics(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))
            else:
                verify = {"diff": gravity_work(time.time()).difficulty, "obj": gravity_work(time.time()).create()}
        elif model_name == "化学题库":
            verify_papaer = [i for i in Chemistry(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))
            else:
                verify = {"diff": Combustion_Calculations(time.time()).difficulty,
                          "obj": Combustion_Calculations(time.time()).create()}
        elif model_name == "生物题库":
            verify_papaer = [i for i in Biology(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))
                # verify = (random.sample(verify_papaer, 1)[0])
            else:
                verify = {"diff": biological_gene(time.time()).difficulty, "obj": biological_gene(time.time()).create()}
        elif model_name == "图形化学":
            verify = Chemistry_Pic(time.time())[0]
        elif model_name == "学习强国":
            verify = study(time.time())[0]
        elif model_name == "宋词300":
            verify = Songci(time.time())[0]
        elif model_name == "论语问答":
            verify = Lunyu(time.time())[0]
        elif model_name == "科目一":
            verify = car_subject(time.time())[0]
        elif model_name == "哔哩硬核测试":
            verify = bili(time.time())[0]
        return verify.get("obj")

# print(chemical_formula.create())

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
