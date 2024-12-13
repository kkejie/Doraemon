# !/usr/bin/python
# encoding=utf-8
# @FileName : autoDownMagnet.py
# @Time     : 2024/12/14 3:01
# @Author   : jiekc

import schedule
import time
import sys
import os

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 将项目根目录添加到 Python 搜索路径
sys.path.append(project_root)
from Doraemon.magnetFileDown.magentLinkDownload import DownloadResources


def task():
    dr = DownloadResources()
    dr.main()


# 每天 18:00 执行
schedule.every().day.at("18:30").do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
