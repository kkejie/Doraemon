# !/usr/bin/python
# encoding=utf-8
# @FileName : autoDownMagnet.py
# @Time     : 2024/12/14 3:01
# @Author   : jiekc

import schedule
import time
from Doraemon.magnetFileDown.magentLinkDownload import DownloadResources


def task():
    dr = DownloadResources()
    dr.main()


# 每天 18:00 执行
schedule.every().day.at("18:00").do(task)

while True:
    schedule.run_pending()
    time.sleep(30)
