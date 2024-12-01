# !/usr/bin/python
# encoding=utf-8
# @FileName : auth.py
# @Time     : 2024/11/28 23:41
# @Author   : jiekc

from flask import request
from flask_httpauth import HTTPBasicAuth

api_auth = HTTPBasicAuth()


@api_auth.verify_password    # 定义校验密码的回调函数
def verify_password(username, password):
    # 自定义对用户名和密码的校验
    if username == 'user' and password == '123':
        # 校验通过返回True
        print(username, password)
        print(request.method )
        return True


# pip install Flask-HTTPAuth

# 参考链接：https://www.kancloud.cn/cruzen/python/1741476

