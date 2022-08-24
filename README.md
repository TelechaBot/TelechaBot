# TelechaBot

验证机器人主体，接入学科生物验证核心

### 环境需求

应当使用 Python 3.7 或更高版本.

### 安装

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

| 命令                   | 含义                      | 作用域     | 
|----------------------|-------------------------|---------|
| `/unban id`          | 本群组手动提权解封用户             | 单个群组    |
| `/onW`               | 机器人开启白名单模式，不能被未认证的用户再拉入 | 机器人     |
| `/offW`              | 关闭白名单，开放机器人             | 机器人     |
| `/show`              | 对config设定的主人显示配置        | 私聊      |
| `/addWhite group_id` | 加入白名单，仅开启白名单时有效         | 机器人     |

