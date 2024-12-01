# !/usr/bin/python
# encoding=utf-8
# @FileName : urls.py
# @Time     : 2024/11/29 0:24
# @Author   : jiekc
import re
from datetime import datetime, timedelta
import holidays
from flask import Blueprint, jsonify, render_template, abort

# test_blueprint = Blueprint('select', __name__, template_folder='../templates', url_prefix='/select')
from jinja2 import TemplateNotFound

test_blueprint = Blueprint('select', __name__, template_folder='../templates')

from flask import jsonify, render_template, abort
from datetime import datetime, timedelta
from jinja2 import TemplateNotFound
import holidays

# 节日中文名映射关系
holidays_chs = {
    "New Year's Day": "元旦",
    "Labour Day": "劳动节",
    "Chinese New Year (Spring Festival)": "春节",
    "National Day": "国庆节",
    "Tomb-Sweeping Day": "清明节",
    "Dragon Boat Festival": "端午节",
    "Mid-Autumn Festival": "中秋节"
}


def find_next_holiday():
    now = datetime.now()
    chs_holidays = holidays.China(years=[now.year, now.year + 1])

    # 按日期排序找到最近的节日
    for date, name in sorted(chs_holidays.items()):
        if date >= now.date():  # 确保节日在未来
            if not bool(re.search(r'[\u4e00-\u9fff]+', name)):
                name = holidays_chs.get(name, "未知节日")  # 映射节日名
            return date, name
    return None, None


@test_blueprint.route('/next-holiday', methods=['GET'])
def get_next_holiday():
    next_date, next_holiday = find_next_holiday()
    if next_date:
        return jsonify({"date": next_date.strftime('%Y-%m-%d'), "name": next_holiday})
    else:
        return jsonify({"error": "在接下来的365天内没有节假日"}), 404


@test_blueprint.route('/nextHoliday', methods=['GET'])
def next_holiday():
    try:
        return render_template('countdown.html')
    except TemplateNotFound:
        abort(404)
