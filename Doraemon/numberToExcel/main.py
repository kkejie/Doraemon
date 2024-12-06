# !/usr/bin/python
# encoding=utf-8
# @FileName : main.py
# @Time     : 2024/12/5 19:50
# @Author   : jiekc
from flask import Blueprint, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from numbers_parser import Document
import csv

# 创建 Blueprint
convert_blueprint = Blueprint('convert', __name__, template_folder='templates')


@convert_blueprint.route('/numberToExcel')
def index():
    return render_template('numberToExcel.html')


@convert_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        from Doraemon.manage import app

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 调用新的 Aspose.Cells 转换逻辑
        try:
            excel_file_path = convert_numbers_to_excel(file_path)
            return send_file(excel_file_path, as_attachment=True)
        except Exception as e:
            return f"File conversion failed: {str(e)}"


def convert_numbers_to_excel(numbers_file_path):
    """
    将 Numbers 文件转换为 CSV 格式。
    """
    from Doraemon.manage import app
    converted_file_path = os.path.join(app.config['CONVERTED_FOLDER'],
                                       os.path.splitext(os.path.basename(numbers_file_path))[0] + '.csv')

    # 使用 numbers-parser 解析 .numbers 文件
    doc = Document(numbers_file_path)
    sheets = doc.sheets

    with open(converted_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 遍历每个 sheet
        for sheet in sheets:
            for table in sheet.tables:
                data = table.rows()
                for row in data:
                    writer.writerow([cell for cell in row])  # 将每一行写入 CSV

    return converted_file_path


def number_to_excel():
    import jpype
    import asposecells
    jpype.startJVM()
    from asposecells.api import Workbook
    workbook = Workbook(
        r"C:\Users\Administrator\Downloads\COMPLETE-Final2BILT Home Collection Final Assortment Options 2 (1).numbers")
    workbook.save(
        r"C:\Users\Administrator\Downloads\COMPLETE-Final2BILT Home Collection Final Assortment Options 2 (1).xlsm")
    jpype.shutdownJVM()


if __name__ == '__main__':
    number_to_excel()
