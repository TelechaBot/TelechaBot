![a](https://s1.328888.xyz/2022/08/24/wlGew.png)

------------------------------------
<p align="center">
  <img alt="License" src="https://img.shields.io/badge/LICENSE-Mit-ff69b4">
  <img src="https://img.shields.io/badge/USE-python-green" alt="PYTHON" >
  <img src="https://img.shields.io/github/v/release/TelechaBot/TelechaBot?style=plastic" alt="V" >
  <a href="https://dun.mianbaoduo.com/@Sky0717"><img src="https://img.shields.io/badge/Become-sponsor-DB94A2" alt="SPONSOR"></a>
</p>

<h2 align="center">TelechaBot</h2>

TelechaBot 是一个使用 Python 编写的机器人项目，使用可更新小初高题目模组进行生物验证！
项目经过严格模块化重构，便于扩展。目前由 `Sudoskys`做维护支持

验证机器人主体，接入学科生物验证核心。

### 环境需求

应当使用 Python 3.7 或更高版本.

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
nano Captcha.yaml
```

#### 配置文件说明

*USE Captcha.yaml*

```yaml
# statu: True
version: "2.0.5"
desc: 'a bot'
link: "https://t.me/SmartCapthaBot"
botToken: '57xxxxxxxxxxxxxxxxxxxxdqMuqPs'
#when you select lock:true,you must use aes to encode all Token! And Dont push your token to github directly.
ClientBot: { owner: '5477776859' }
```

### 部署机器人

**后台运行**

```shell
nohup python3 main.py > output.log 2>&1 &
```

**查看进程**

```
ps -aux|grep python3
```

**终止进程**

```
kill -9  进程号
```

### 使用

| 命令                      | 含义                      | 作用域        | 
|-------------------------|-------------------------|------------|
| `+unban id`             | 本群组手动提权解封用户             | 单个群组       |
| `/onw`                  | 机器人开启白名单模式，不能被未认证的用户再拉入 | 机器人        |
| `/offw`                 | 关闭白名单，开放机器人             | 机器人        |
| `/show`                 | 对config设定的主人显示配置        | 私聊         |
| `/addwhite group_id`    | 加入白名单，仅开启白名单时生效         | 机器人下一次加入群组 |
| `/removewhite group_id` | 移除白名单，仅开启白名单时生效         | 机器人下一次加入群组 |
| `/cat filepath`         | 查看文件                    | 私聊         |

机器人目前不会自动释放用户，请手动释放

### 关于验证模型


作用是抽取并随机生成题目，支持难度梯度过滤
`some = model_name.Importer().pull(difficulty_limit=5)`

[项目详细信息和参数信息](https://github.com/TelechaBot/CaptchCore)

**实例**

```
长度为34的线段 AB 的两个端点A、B都在抛物线y2(2次方)=8x 上滑动，则线段 AB 的中点 M 到 y 轴的最短距离为?(四舍五入)
8
一个圆锥的底面积为72π，高为26，求其体积!(四舍五入，只答出数字部分！)
8
一个圆锥的底面积为39π，高为8，求其体积!(四舍五入，只答出数字部分！)
32
```
