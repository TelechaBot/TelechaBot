from pathlib import Path

from Bot.Controller import clientBot
from utils.BotTool import Check
from shutil import copy
import sys

ConfigDir = "/app/Config"
DataDir = "/app/Data"
ConfigFile = DataDir + "Captcha.toml"
if not Path(ConfigFile).exists():
    copy("/app/Captcha_exp.toml", ConfigFile)
    copy("/app/Data/", DataDir)
    print("配置文件创建完成,请修改配置文件后, 重新运行本容器")
    sys.exit()

Check().run()
clientBot(ConfigPath=ConfigFile).run()
