![a](https://s1.328888.xyz/2022/08/24/wlGew.png)

------------------------------------
<p align="center">
  <img alt="License" src="https://img.shields.io/badge/LICENSE-Mit-ff69b4">
  <img src="https://img.shields.io/badge/USE-python-green" alt="PYTHON" >
  <a href="https://github.com/TelechaBot/TelechaBot/releases"><img src="https://img.shields.io/github/v/release/TelechaBot/TelechaBot?style=plastic" alt="V" ></a>
  <a href="https://dun.mianbaoduo.com/@Sky0717"><img src="https://img.shields.io/badge/Become-sponsor-DB94A2" alt="SPONSOR"></a>
</p>

<h2 align="center">TelechaBot</h2>

TelechaBot 是一个使用 Python 编写的机器人项目，使用可更新小初高题目模组进行生物验证！
项目经过严格模块化重构，便于扩展。目前由 `Sudoskys`做维护支持

验证机器人主体，接入学科生物验证核心。

### 环境需求

应当使用 Python 3.7 或更高版本，主机需要安装redis！

**安装 Redis**

```shell
apt-get install redis
```

使用 ```systemctl start redis.service``` 启动服务，或者使用```nohup redis-server > output.log 2>&1 &```启动，推荐前者。

### 安装

安装脚本会自动备份恢复配置

在根目录运行(不要在程序目录内)

```
curl -LO https://raw.githubusercontent.com/TelechaBot/TelechaBot/main/setup.sh && sh setup.sh

```

或者

```
curl -LO https://raw.fastgit.org/TelechaBot/TelechaBot/main/setup.sh && sh setup.sh
```

安装后不需要手动创建``taskRedis.json``，如果有此文件且``taskRedis.json`` 没有内容，需要手动填入`{}`，否则解析库报错。

**编辑Captcha.yaml**

```bash
cd TelechaBot

sudo apt install nano

cp Captcha_exp.yaml Captcha.yaml
 
nano Captcha.yaml 
```

#### 配置文件说明

*USE Captcha.yaml*

```yaml
# statu: True
version: "2.0.6"
# /about
desc: "生物信息验证 Bot\nChannel @TelechaBot_real\ngithub.com/TelechaBot/TelechaBot"
# 机器人链接，用于跳转
link: "https://t.me/SmartCapthaBot"
# 申请的token 去botfather那里
botToken: 'xxxxx:xxxxxxxxxxxxxxxxx'
# 主人信息
ClientBot: { owner: 'xxxxid',contact_details: "httpxxxxxthaBot" }
```

### 部署机器人

先去 Botfather 获取你自己的 Token

**后台运行**

```shell
nohup python3 main.py > output.log 2>&1 &


cat output.log

```

**查看进程**

```shell
ps -aux|grep python3
```

**终止进程**

```shell
kill -9  进程号
```

**无缝更新**

```shell
curl -LO https://raw.githubusercontent.com/TelechaBot/TelechaBot/main/setup.sh && sh setup.sh
```

```shell
cd TelechaBot
```

```shell
ps -aux|grep python3
```

```shell
kill -9 进程号 && nohup python3 main.py > output.log 2>&1 &
```

### 使用

| 命令                        | 含义                         | 作用域 | 权限(主人,管理,群员) |
|---------------------------|----------------------------|-----|--------------|
| `+unban id`               | 解除用户验证和解除用户限制，移出黑名单        | 群组  | 管理           |
| `+diff_limit level`       | 设定当前群组的验证难度上限              | 群组  | 管理           |
| `+select`                 | 设定验证题库模式，自定义需要自部署或者提交合并    | 群组  | 管理           |
| `+diff_min level`         | 设定当前群组的验证难度下限              | 群组  | 管理           |
| `/whatmodel`              | 查看当前群组的验证模型                | 群组  | 管理           |
| `+banme`                  | 俄罗斯禁言轮盘，管理不能玩              | 群组  | 群员           |
| `+ban`+ID或者回复             | ban掉一个用户                   | 群组  | 管理           |
| `/onw`                    | 机器人开启白名单模式，不能被未认证的用户再拉入或使用 | 机器人 | 主人           |
| `/offw`                   | 关闭白名单，开放机器人                | 机器人 | 主人           |
| `/show`                   | 对config设定的主人显示配置           | 私聊  | 主人           |
| `/addwhite group_id`      | 加入白名单，仅开启白名单时生效            | 群组  | 主人           |
| `/removewhite group_id`   | 移除白名单，仅开启白名单时生效            | 群组  | 主人           |
| `/cat filepath`           | 查看文件                       | 私聊  | 主人           |
| `/unban group_id user_id` | 解封指定群组的指定用户                | 私聊  | 主人           |
| `/ban group_id user_id`   | 为了防止部署者滥权，没做功能             | 私聊  | 主人           |
| `/redis`                  | 查看队列顺便备份 redis 键表          | 私聊  | 主人           |
| `/renew`                  | 从网络更新题库                    | 私聊  | 主人           |
| `/about`                  | 关于机器人的信息（读取config中的预设描述）   | 私聊  | 任何人          |

机器人目前支持自动释放用户，6分钟后自动释放用户,期间中断执行会导致被封禁。

群组管理(+开头)

``````
+ban 回复或+ID
+banme 嗯?
+diff_min 设定最小难度
+select 选择题库
+diff_limit 设定最大难度
+unban 解禁+ID
``````

**模板**

```md
whatmodel - 管理 查看当前模组
start - 私聊 开始验证
about - 私聊 关于这个好玩的Bot
show - 主控 对主人显示配置
renew - 主控 更新题库
onw - 主控 对群组开启白名单
offw - 主控 对群组关闭白名单
addwhite - 主控 加入白名单
removewhite - 主控 踢出白名单
cat - 主控 查看文件
```

### 关于验证模型

支持多重模型，自定义模型,自带多重模型。

理论可以兼容其他绝大部分机器人的验证方式！

作用是抽取并随机生成题目，支持难度梯度过滤

`some = model_name.Importer().pull(difficulty_limit=5)`

[项目详细信息和参数信息](https://github.com/TelechaBot/CaptchCore)

**实例**

```
长度为34的线段 AB 的两个端点A、B都在抛物线y2(2次方)=8x 上滑动，则线段 AB 的中点 M 到 y 轴的最短距离为?(四舍五入)
8

在 周密 的诗《绣鸾凤花犯・花犯》中，有这样一句: 冰弦写怨更多情，骚人恨，枉赋芳兰幽芷。
请问它的下面一句是？ |A:千里孤坟，无处话凄凉。|B:惟有御沟声断，似知人呜咽。|C:春思远，谁叹赏、国香风味。

在论语 先进篇 中，有这样一句对话: 颜渊死。子曰：“噫！天丧予！天丧予！”
请问它的下面一句是？ 
|A:子谓子夏曰：“女为君子儒，无为小人儒。”
|B:子曰：“《诗》三百，一言以蔽之，曰：‘思无邪’。”
|C:颜渊死，子哭之恸，从者曰：“子恸矣！”曰：“有恸乎？非夫人之为恸而谁为？”

俺はGandom(我就是高达)这句话是谁说的？

.....
```

**自定义题库**

将你的题库文件放在Github或者托管在其他可以直链公开访问的服务上，然后写一个类，处理这个文件返回Q和A两个参数，并提交到 [这个仓库](https://github.com/TelechaBot/QaBank) 的Issue 或者
Pr。

调试需要启动 redis-server

### 待办

- [x] 重新选择题目
- [x] 自动释放黑名单
- [x] 群组设置自定义难度
- [x] 手动解除封锁
- [x] 群组白名单
- [x] 网络热加载
- [x] 重构消息逻辑
- [x] 群组设置自定义题目仓库，设计题库读取类
- [x] 自定义题目仓库在线更新
- [x] 异步实现
- [x] 初步使用Redis接管数据
- [ ] 使用Redis重构队列逻辑
- [ ] 重构设计模式