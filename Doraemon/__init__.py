# !/usr/bin/python
# encoding=utf-8
# @FileName : __init__.py
# @Time     : 2024/11/28 23:24
# @Author   : jiekc
import os

from flask import Flask
from Doraemon.settings import MysqlConfig
from Doraemon.countdown.urls import test_blueprint
from Doraemon.numberToExcel.main import convert_blueprint
from Doraemon.magnetFileDown.getWechatMessage import get_we_chat_message_blueprint


def create_app():
    app = Flask(__name__, )
    # 配置应用参数
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['CONVERTED_FOLDER'] = 'converted'

    # 确保上传和转换文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

    app.config.from_object(MysqlConfig)
    app.register_blueprint(test_blueprint)
    app.register_blueprint(convert_blueprint)
    app.register_blueprint(get_we_chat_message_blueprint)

    # db.init_app(app)

    return app