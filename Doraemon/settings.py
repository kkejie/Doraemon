# !/usr/bin/python
# encoding=utf-8
# @FileName : settings.py
# @Time     : 2024/11/28 23:39
# @Author   : jiekc


class BaseConfig(object):
    DEBUG = True
    TESTING = True
    JSON_AS_ASCII = False
    JSONIFY_MIMETYPE = 'application/json;charset=utf8'


class MysqlConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.213.135:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY = True

