# -*- coding: utf-8 -*-
# @Time    : 8/29/22 9:23 AM
# @FileName: Redis.py
# @Software: PyCharm
# @Github    ：sudoskys
import importlib
import json
import math
import os
import random
import string
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
def MD5(strs: str):
    import hashlib
    hl = hashlib.md5()
    hl.update(strs.encode(encoding='utf-8'))
    return hl.hexdigest()


# TTS
class TTS_verification(object):
    def __init__(self, sample):
        self.id = sample
        pass

    @property
    def difficulty(self):
        return 1

    @staticmethod
    def nofind():
        lena = (random.randint(5, 20) * 2)
        r = (random.randint(5, 10) * 2)
        Q = f"TTSFileNoFind:一个扇形弧长为{lena}，半径为{r}，求其面积为多少π！（四舍五入，只答出数字）"
        A = (lena * r) / 2
        Question = {"question": Q, "type": "text"}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        try:
            _now = int(time.time() * 100)
            import pyttsx3
            def engine_init():
                importlib.reload(pyttsx3)  # Workaround to be avoid pyttsx3 being stuck
                engine = pyttsx3.init()
                return engine

            tts = engine_init()
            tts.setProperty('rate', 1)
            tts.setProperty('volume', 3.0)
            _random = [f"{random.randint(0, 7)}", f"{random.randint(0, 7)}", f"{random.randint(0, 7)}",
                       f"{random.randint(0, 7)}", f"{random.randint(0, 7)}"]
            _letter = f"{random.choice(string.ascii_lowercase)}s"
            _random_q = " ".join(iter(_random))
            _random_int = "".join(iter(_random))
            TTS = [[_random_q, _random_int],
                   # [f"{_random_q} {_letter}", _random_int + _letter],
                   # [f"{_letter} {_random_q}", _letter + _random_int]
                   ]
            _NowTTS = random.choice(TTS)
            pathlib.Path("TTS").mkdir(exist_ok=True)
            file_name = f'TTS/{MD5(_random_int)}.mp3'
            if not os.path.exists(file_name):
                tts.save_to_file(_NowTTS[0], file_name)
                # tts.say(_NowTTS[0])
                tts.runAndWait()
                _i = 100
                while not os.path.exists(file_name) and _i != 0:
                    time.sleep(0.1)
                    _i = _i - 1
            if not os.path.exists(file_name):
                raise FileNotFoundError("NO TTS File")
            Q = f"听这段音频，它由数字组成\n发送你听到的内容，不要有空格"
            A = _NowTTS[1]
            Question = {"question": Q, "voice_path": file_name, "type": "voice"}
            Answer = {"rightKey": A}
        except FileNotFoundError as e:
            Question, Answer = Idiom_verification.nofind()
        return Question, Answer


# 成语验证
class Idiom_verification(object):
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
        Question = {"question": Q, "type": "text"}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        if pathlib.Path('Data/Idiom.json').exists():
            with open("Data/Idiom.json", 'r') as tiku_file:
                samples = json.load(tiku_file)
            if samples is not None:
                item = random.choice(samples)
                Pic = item.get("pic")
                Tips = item.get("confound")
                Exp = item.get("explain")
                Q = f"成语的词汇在以下词组内\n{Tips}\n\n释义为{Exp}\n\n猜猜看吧～"
                A = item.get("answer")
                Question = {"question": Q, "picture": Pic, "type": "photo"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = Idiom_verification.nofind()
        else:
            Question, Answer = Idiom_verification.nofind()
        return Question, Answer


# 化学图形验证
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
        Question = {"question": Q, "type": "text"}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
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
                Question = {"question": Q, "picture": Pic, "type": "photo"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = Chemical_verification.nofind()
        else:
            Question, Answer = Chemical_verification.nofind()
        return Question, Answer


class Tool_CaptchaCore(object):
    def __init__(self):
        """
        意义不明的工具类
        """
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
        Question = {"question": Q, "type": "text"}
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
                Question = {"question": Q, "type": "text"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = bili_hard_core.nofind()
        else:
            Question, Answer = bili_hard_core.nofind()
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
        Question = {"question": Q, "type": "text"}
        Answer = {"rightKey": round(A)}
        return Question, Answer

    @staticmethod
    def create():
        # rsd = (random.randint(1, 5) * 1)
        sde = (random.randint(2, 8) * 1)
        # rse = (random.randint(1, 4) * 2)
        inputs = f"P{sde}+H2O"
        output = "PH4+H3PO4"
        key = "PH4"
        tip_key = "H2O"
        input_, samples = Tool_CaptchaCore.peiping(one=inputs, two=output)
        tip = input_.get(tip_key)
        if samples:
            Q = f"现在有 {inputs}={output} 这个没有配平的化学方程式，不考虑是否合理的情况下，前面的{tip_key}的系数为{tip}请问方程式后半段的 {key} 的系数是多少？(答出数字)"
            A = samples.get(key)
            Question = {"question": Q, "type": "text"}
            Answer = {"rightKey": A}
        else:
            Question, Answer = chemical_formula.nofind()
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
        Question = {"question": Q, "type": "text"}
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
                Question = {"question": Q, "type": "text"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = car_subject_one.nofind()
        else:
            Question, Answer = car_subject_one.nofind()
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
        Question = {"question": Q, "type": "text"}
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
                Question = {"question": Q, "type": "text"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = songci_300.nofind()

        else:
            Question, Answer = songci_300.nofind()
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
        Question = {"question": Q, "type": "text"}
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
                Question = {"question": Q, "type": "text"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = lunyu.nofind()

        else:
            Question, Answer = lunyu.nofind()
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
        Question = {"question": Q, "type": "text"}
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
                Question = {"question": Q, "type": "text"}
                Answer = {"rightKey": A}
            else:
                Question, Answer = study_build_up.nofind()
        else:
            Question, Answer = study_build_up.nofind()
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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

        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Q = f"用标志重捕法来估计某个种群的个体数量，例如在对某种鼠群的种群密度的调查中，" \
            f"第一次捕获并标志{once}只，第二次捕获{twice}只，其中有标志鼠{scend}只，则对该种群的数量估计，该种群数量大约为多少只？(答出数字) "
        A = (twice * once) / scend
        # A = 128 * (num1 + num2) - 18 * num2
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
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
        Question = {"question": Q, "type": "text"}
        Answer = {"rightKey": round(A)}
        return Question, Answer


# --------------------------------

def TTS_VOICE(s):
    _TTS_VOICE = [
        {"diff": TTS_verification(s).difficulty,
         "obj": TTS_verification(s).create()},
    ]
    return _TTS_VOICE


def Idiom_Pic(s):
    _Idiom_Pic = [
        {"diff": Idiom_verification(s).difficulty,
         "obj": Idiom_verification(s).create()},

    ]
    return _Idiom_Pic


def Chemistry_Pic(s):
    _Chemistry_Pic = [
        {"diff": Chemical_verification(s).difficulty,
         "obj": Chemical_verification(s).create()},

    ]
    return _Chemistry_Pic


def Chemistry(s):
    _Chemistry = [
        {"diff": Combustion_Calculations(s).difficulty,
         "obj": Combustion_Calculations(s).create()},
        {"diff": chemical_formula(s).difficulty,
         "obj": chemical_formula(s).create()},

    ]
    return _Chemistry


def Biology(s):
    _Biology = [
        {"diff": biological_gene(s).difficulty, "obj": biological_gene(s).create()},
        {"diff": biological_DNA(s).difficulty, "obj": biological_DNA(s).create()},
        {"diff": biological_protein(s).difficulty, "obj": biological_protein(s).create()},
        {"diff": biological_Flag_Recap(s).difficulty, "obj": biological_Flag_Recap(s).create()},

    ]
    return _Biology


def Mathematics(s):
    _Mathematics = [
        {"diff": find_volume_cone(s).difficulty, "obj": find_volume_cone(s).create()},
        {"diff": find_ball_cone(s).difficulty, "obj": find_ball_cone(s).create()},
        {"diff": binary_first_equation(s).difficulty, "obj": binary_first_equation(s).create()},
        {"diff": parabola_2(s).difficulty, "obj": parabola_2(s).create()},
        {"diff": parabola(s).difficulty, "obj": parabola(s).create()},
        {"diff": radius(s).difficulty, "obj": radius(s).create()},
    ]
    return _Mathematics


def Physics(s):
    _Physics = [
        {"diff": gravity_work(s).difficulty, "obj": gravity_work(s).create()},
        {"diff": cosmic_speed(s).difficulty, "obj": cosmic_speed(s).create()},
    ]
    return _Physics


def study(s):
    _study = [
        {"diff": study_build_up(s).difficulty, "obj": study_build_up(s).create()},
    ]
    return _study


def car_subject(s):
    _car_subject = [
        {"diff": car_subject_one(s).difficulty, "obj": car_subject_one(s).create()},
    ]
    return _car_subject


def bili(s):
    _bili = [
        {"diff": bili_hard_core(s).difficulty, "obj": bili_hard_core(s).create()},
    ]
    return _bili


def Songci(s):
    _songci = [
        {"diff": songci_300(s).difficulty, "obj": songci_300(s).create()},
    ]
    return _songci


def Lunyu(s):
    _lunyus = [
        {"diff": lunyu(s).difficulty, "obj": lunyu(s).create()},
    ]
    return _lunyus


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
        return ["数学题库", "物理题库", "化学题库", "生物题库", "图形化学", "学习强国", "宋词300", "论语问答", "科目一",
                "哔哩硬核测试", "图形成语", "基础听力验证"]

    def pull(self, difficulty_min=1, difficulty_limit=5, model_name="数学题库"):
        difficulty_min = int(difficulty_min)
        difficulty_limit = int(difficulty_limit)
        id_now = time.time()
        verify = {"diff": binary_first_equation(id_now).difficulty,
                  "obj": binary_first_equation(id_now).create()}
        difficulty_min, difficulty_limit = Importer.reset(difficulty_min, difficulty_limit)
        if model_name == "数学题库":
            verify_papaer = [i for i in Mathematics(self.samples) if
                             difficulty_min <= i.get("diff") <= difficulty_limit]
            verify = {"diff": binary_first_equation(id_now).difficulty,
                      "obj": binary_first_equation(id_now).create()}
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))

        elif model_name == "物理题库":
            verify_papaer = [i for i in Physics(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            verify = {"diff": gravity_work(id_now).difficulty, "obj": gravity_work(id_now).create()}
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))

        elif model_name == "化学题库":
            verify_papaer = [i for i in Chemistry(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            verify = {"diff": Combustion_Calculations(id_now).difficulty,
                      "obj": Combustion_Calculations(id_now).create()}
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))

        elif model_name == "生物题库":
            verify_papaer = [i for i in Biology(self.samples) if difficulty_min <= i.get("diff") <= difficulty_limit]
            verify = {"diff": biological_gene(id_now).difficulty, "obj": biological_gene(id_now).create()}
            if len(verify_papaer) != 0:
                random.shuffle(verify_papaer)
                verify = (choice(verify_papaer))
                # verify = (random.sample(verify_papaer, 1)[0])

        elif model_name == "图形化学":
            verify = Chemistry_Pic(id_now)[0]
        elif model_name == "图形成语":
            verify = Idiom_Pic(id_now)[0]
        elif model_name == "学习强国":
            verify = study(id_now)[0]
        elif model_name == "宋词300":
            verify = Songci(id_now)[0]
        elif model_name == "论语问答":
            verify = Lunyu(id_now)[0]
        elif model_name == "科目一":
            verify = car_subject(id_now)[0]
        elif model_name == "哔哩硬核测试":
            verify = bili(id_now)[0]
        elif model_name == "基础听力验证":
            verify = TTS_VOICE(id_now)[0]
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
