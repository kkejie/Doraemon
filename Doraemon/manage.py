# !/usr/bin/python
# encoding=utf-8
# @FileName : manage.py
# @Time     : 2024/11/28 23:31
# @Author   : jiekc

# -*- coding:utf8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Doraemon import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)

# sudo docker run -d --name=postgres -p 5432:5432  -e POSTGRES_PASSWORD=123456 postgres
