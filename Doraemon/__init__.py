# !/usr/bin/python
# encoding=utf-8
# @FileName : __init__.py
# @Time     : 2024/11/28 23:24
# @Author   : jiekc

from flask import Flask
from Doraemon.settings import MysqlConfig
from Doraemon.countdown.urls import test_blueprint


def create_app():
    app = Flask(__name__, )
    app.config.from_object(MysqlConfig)
    app.register_blueprint(test_blueprint)
    # db.init_app(app)

    return app