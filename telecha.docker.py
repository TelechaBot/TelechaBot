from pathlib import Path

from Bot.Controller import clientBot
from utils.BotTool import Check
from shutil import copy
import sys

ConfigDir = "/app/Config/"
DataDir = "/app/Data/"
ConfigFile = ConfigDir + "Captcha.toml"
if not Path(ConfigFile).exists():
    copy("/app/test/Config/Captcha.toml", ConfigDir)
    copy("/app/test/Config/config.json", DataDir)
    print("配置文件创建完成,请修改配置文件后重新运行")
    sys.exit()

Check().run()
clientBot(ConfigPath=ConfigFile).run()
