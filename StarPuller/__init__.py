# -*- coding: utf-8 -*-
# @Time    : 8/26/22 5:28 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys
import json

import requests
import pathlib

class Worker(object):
    def __init__(self, mirror=None, header=None):
        self.star_tiku_content = None
        self.index_content = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        self.default_index = "https://raw.githubusercontent.com/TelechaBot/QaBank/main/Bank.json"
        if mirror is not None:
            self.default_index = mirror
        if mirror is not None:
            self.header = header
        self.get_index()

    def get_index(self):
        global star_tiku_content
        cont = {}
        mew = requests.get(self.default_index, headers=self.header)
        if mew.status_code == 200:
            self.index_content = mew.json()
            star_tiku_content = {}
            for key, item in self.index_content.items():
                try:
                    cont = requests.get(item.get("FullUrl"), headers=self.header).json()
                except Exception as e:
                    cont = requests.get(item["Proxy"] + item["Url"], headers=self.header).json()
                finally:
                    star_tiku_content[key] = cont
            self.star_tiku_content = star_tiku_content
            HOME = str(pathlib.Path().cwd()) + "/"
            Dir = HOME + "data/"
            pathlib.Path(Dir).mkdir(exist_ok=True)
            with open("data/star_tiku_content.json", 'w+', encoding="utf8") as f:
                star_tiku_content = json.dumps(star_tiku_content, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
                f.write(star_tiku_content)
            return True
        else:
            return False

    def run(self):
        print(self.star_tiku_content)
        pass
