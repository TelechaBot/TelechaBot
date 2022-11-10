![a](https://raw.githubusercontent.com/TelechaBot/.github/main/profile/cover.png)

------------------------------------
<p align="center">
  <img alt="License" src="https://img.shields.io/badge/LICENSE-Other-ff69b4">
  <img src="https://img.shields.io/badge/USE-python-green" alt="PYTHON" >
  <a href="https://github.com/TelechaBot/TelechaBot/releases"><img src="https://img.shields.io/github/v/release/TelechaBot/TelechaBot?style=plastic" alt="V" ></a>
  <a href="https://afdian.net/a/Suki1077"><img src="https://img.shields.io/badge/Become-sponsor-DB94A2" alt="SPONSOR"></a>
</p>

<h2 align="center">TelechaBot</h2>

*TelechaBot* 是一个使用 Python 编写的机器人项目，使用 可更新模组 进行生物验证！ 项目经过模块化，便于扩展。

为了给群组提供有效的验证模式，便捷的以**筛选**为目的**梯度验证**模式，它支持诸如 **成语验证** **普通语音听力验证** **图片验证** **文本验证** **诗词验证** **数学** **物理** **化学** **生物** **哔哩哔哩题库** 等验证模式。

这让它既可以作为普通群组的智能安全的验证工具(推荐 听力验证 和 科目一 等系列)，也可以作为严肃型群组的得力助手(例如数学验证)。

目前由 `Sudoskys` 做维护支持，点击 [使用一个可爱的实例](https://t.me/SmartCapthaBot?startgroup=start&admin=can_invite_users) *如果服务器没钱可能就不会维护*

## 👋特性

* MVC架构
* 支持白名单
* 支持一键部署
* 异步 + 线程锁
* 模块化**题库**模组
* 体验第一性能第二
* 支持英文语音验证
* 内存散列表过期队列实现
* 支持热载维护反Spam关键词
* 群组自定义 绿卡/红牌 策略支持
* 自由选择的枚举和不可枚举混合题库
* 反垃圾内容全方位系统，用户从头像到Bio,人类能看见的它也可以看见。

## 🙌应用

- 机器人的封禁策略

延迟定时封禁。到时间自动释放(博弈交给机器人)，避免误封后永不解封的问题。

如果遇到了碰撞入群的情况，请开启高级 不可枚举题库 或语音验证。

如果遇到被突破的情况，请提交反馈进行变动。

### 🤔如何使用

本机器人采用 **自动审批邀请** 的验证方式，舍弃旧的禁言公屏验证方式。

* 防止机器人宕机拦截不及时
* 防止响应过慢导致的拦截不住
* 防止操作记录被污染和打扰聊天(邀请只能管理员看到)
* 适应 Topic 验证

先在群组设置 `群组类型` 中开启 `批准新成员` 或 `加入需要审核` 选项。

然后你需要将机器人添加进入群组，然后给予 `禁言` `邀请用户` `封禁用户` 权限。此时机器人管理就可以读取群内消息了。
基于白名单机制需要，机器人会存储一下群组 ID。

### 命令表格

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
| `/groupuser`              | 对config设定的主人显示正在使用的群组      | 私聊  | 主人           |
| `/addwhite group_id`      | 加入白名单，仅开启白名单时生效            | 私聊  | 主人           |
| `/removewhite group_id`   | 移除白名单，仅开启白名单时生效            | 私聊  | 主人           |
| `/cat filepath`           | 查看文件                       | 私聊  | 主人           |
| `/unban group_id user_id` | 解封指定群组的指定用户                | 私聊  | 主人           |
| `/ban group_id user_id`   | 为了防止部署者滥权，没做功能             | 私聊  | 主人           |
| `/redis`                  | 查看队列顺便备份 redis 键表          | 私聊  | 主人           |
| `/renew`                  | 从网络更新题库                    | 私聊  | 主人           |
| `/about`                  | 关于机器人的信息（读取config中的预设描述）   | 私聊  | 任何人          |
| `/upantispam`             | 更新反诈库                      | 私聊  | 主人           |
| `/whatstrategy`           | 查看本群策略                     | 群组  | 管理           |


#### ⚒群组管理命令

缇茶 *目前* 使用 `+` 作为关键符。

```shell
+select 选择题库
+ban 回复或+ID
+banme 俄罗斯轮盘
+diff_min 设定最小难度
+diff_limit 设定最大难度
+unban 解禁+ID
```

#### 🎛策略组

什么是入群前策略组？

缇茶会在验证之前先根据群组的策略进行分流筛选，然后根据特征将待验证者分流到不同的操作逻辑。

* 样式
```
!door!premium=[level=1|type=off]
```

使用 ``/whatstrategy`` 查看策略和支持的键类型。

支持的属性为 ["level", "type", "command"]  
`level` 为优先级（冲突时高等级策略优先），`type` 为 `on` 或者 `off` ，`command` 分 `ask`(验证),`ban`(禁止),`pass`(绿卡通过) 找不到默认 ask。


### 🔨待办

- [ ] 智能通过可信用户(在严格模式下)
- [ ] 日志频道支持
- [ ] 兼容 Rose 语法
- [x] 异步实现
- [x] 网络热加载
- [x] 群组白名单
- [x] 手动解除封锁
- [x] 重新选择题目
- [x] 重构消息逻辑
- [x] 自动释放黑名单
- [x] DFA 反内容算法
- [x] 反 QrCode 判定
- [x] CV 计算判定NSFW
- [x] 群组设置自定义难度
- [x] 重构设计模式为 MVC
- [x] 自定义题目仓库在线更新
- [x] 初步使用Redis接管数据
- [x] 使用Redis重构队列逻辑
- [x] 群组设置自定义题目仓库，设计题库读取类

## ⚙️自部署指南

### 🥪环境支持

应当使用 Python 3.7 或更高版本，主机需要安装 `redis-server`

* 安装 Redis

```shell
apt-get install redis
```

使用 ```systemctl start redis.service``` 启动服务，或者使用```nohup redis-server > output.log 2>&1 &```启动，推荐前者。

* 安装TTS支持
  使用 `sudo apt install espeak ffmpeg libespeak1` 安装 TTS 语音验证支持。

### 🥕安装维护

* 拉取/更新程序

安装脚本会自动备份恢复配置，在根目录运行(不要在程序目录内)
，更新时候重新运行就可以备份程序了，如果是小更新可以直接 ``git pull``

```shell
curl -LO https://raw.githubusercontent.com/TelechaBot/TelechaBot/main/setup.sh && sh setup.sh
```

然后切换到程序目录进行配置 ``cd TelechaBot``

#### ⚙️配置

* 安装依赖库

```shell
cd TelechaBot
pip install -r requirements.txt
```

* 编辑配置文件 `Captcha.toml`

```shell
sudo apt install nano
cp Captcha_exp.toml Captcha.toml
nano Captcha.toml 
```

#### 📚配置文件说明

* nano Captcha.toml

```toml
# Sample
desc = "生物信息验证 Bot\nChannel @TelechaBot_real\ngithub.com/TelechaBot/TelechaBot"
link = "https://t.me/SmartCapthaBot"
botToken = '57xxxxxxxxxxxxxxxxxxxxdqMuqPs'

[ClientBot]
owner = '5477776859'
contact_details = "判定为非白名单群组后的联系方式"

[Proxy]
status = false
url = "http://127.0.0.1:7890" 
```

这里的 `botToken` 填写你在 `botFather` 那里申请的botToken,这个是机器人的登陆凭证，请妥善保管。

这里的 `desc` 是 About 字段，可以删除整个字段。

### 🚀运行

#### 📚命令模板


```md
start - 私聊 开始验证
about - 私聊 关于这个好玩的Bot
whatmodel - 管理 查看当前模组
whatstrategy - 管理 查看本群策略
renew - 主人 更新题库
upantispam - 主人 更新反诈数据
unban - 主人 群组ID+用户ID
onw - 主人 对群组开启白名单
offw - 主人 对群组关闭白名单
show - 主人 对主人显示配置
addwhite - 主人 加入白名单
removewhite - 主人 踢出白名单
cat - 主人 查看文件
redis - 主人 查看目前队列
groupuser - 主人 查看使用者
```


#### 🧊后台运行

```shell
# 长时间运行
nohup python3 telecha.py > /dev/null 2>&1 & 
```

```shell
# 有日志，因为TG脆弱的土豆服务器，可能会日志爆炸
nohup python3 telecha.py > output.log 2>&1 &
cat output.log
```

* 查看进程
```shell
ps -aux|grep python3
```

* 终止进程
后加进程号码
```shell
kill -9  
```

* 更新

```shell
cd TelechaBot
```

小型更新也可以使用 `git pull`
```shell
curl -LO https://raw.githubusercontent.com/TelechaBot/TelechaBot/main/setup.sh && sh setup.sh
```

### 🪐关于反内容系统

使用 CV2 和 DFA 技术，智能识别。

如果出现 **误报** 或 **失效**，请提交 ISSUE 进行相关处理。

### 🪐关于验证模型

支持多重模型，自定义模型,自带多重模型。

理论可以兼容其他绝大部分机器人的验证方式！

抽取或随机生成题目，支持难度梯度过滤。

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

将你的题库文件放在Github或者托管在其他可以直链公开访问的服务上，然后写一个类，处理这个文件返回Q和A两个参数，并提交到 [这个仓库](https://github.com/TelechaBot/QaBank)
的Issue 或者 Pr。

调试需要启动 `redis-server`

### 协议和信息保管
#### 用户信息协议

本项目会保存验证人员的用户数据画像用于反垃圾内容系统的识别。

本项目不会向其他组织共享任何数据。

本项目的实例不保证提供稳定的服务。

#### 协议

见 LICENSE
