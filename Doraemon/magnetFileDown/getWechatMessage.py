# !/usr/bin/python
# encoding=utf-8
# @FileName : getWechatMessage.py
# @Time     : 2024/12/15 22:02
# @Author   : jiekc

import sys
import os
import re
import time
import base64
import hashlib
import struct
import logging
import configparser
import xml.etree.ElementTree as ET
from flask import Blueprint, render_template, request, send_file, jsonify
from Crypto.Cipher import AES
from pathlib import Path

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 将项目根目录添加到 Python 搜索路径
sys.path.append(project_root)
from Doraemon.magnetFileDown.magentLinkDownload import DownloadResources

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建 Blueprint
get_we_chat_message_blueprint = Blueprint('getWeChatMessage', __name__)

# 你的企业微信 Token 和 EncodingAESKey
TOKEN = "noqCF5YPpwY4s4VdAiFDdlgEM0Bf87UM"
ENCODING_AES_KEY = "UUB2qYJEXPbhuQaaEOmyuh8DrABe1bF2fUzQAWBWnvP"
processed_msg_ids = set()


# 解密函数
def decrypt_message(encrypted_data, encoding_aes_key):
    aes_key = base64.b64decode(encoding_aes_key + "=")
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])

    encrypted_data = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(encrypted_data)

    length, = struct.unpack("I", decrypted_data[:4])
    message = decrypted_data[4: 4 + length].decode('utf-8')

    return message


# 处理消息的接口
@get_we_chat_message_blueprint.route('/hook_path', methods=['POST'])
def wecom_message():
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    # 构造唯一的请求标识
    unique_id = f"{msg_signature}_{timestamp}_{nonce}"

    if unique_id in processed_msg_ids:
        return "Request already processed", 200  # 直接返回，避免重复执行

    processed_msg_ids.add(unique_id)
    # 打印原始请求体
    logging.info(f"Raw request data:{request.data}")

    # 解析 XML 数据
    try:
        root = ET.fromstring(request.data)
        encrypt = root.find('Encrypt').text
        decrypt_encrypt = decrypt_message(encrypt, ENCODING_AES_KEY)
        pattern_content = r'<Content><!\[CDATA\[(.*?)\]\]></Content>'
        pattern_from_user = r'<FromUserName><!\[CDATA\[(.*?)\]\]></FromUserName>'
        content = re.findall(pattern_content, decrypt_encrypt)[0]
        from_user = re.findall(pattern_from_user, decrypt_encrypt)[0]
        agent_id = root.find('AgentID').text
        logging.info(f"ToUserName: {from_user}, Encrypt: {content}, AgentID: {agent_id}")
    except Exception as e:
        logging.error(f"Error parsing XML: {e}")
        return jsonify({"status": "error", "message": "请求数据格式错误"}), 400

    # 校验消息是否来自企业微信
    # if not verify_signature(request):
    #     return jsonify({"status": "error", "message": "签名验证失败"})

    # 根据消息内容（Encrypt）自动请求外部 API
    if content:
        api_response = DownloadResources().load_accessing_web_pages(content, from_user)  # 调用外部 API
        time.sleep(1)
        return jsonify({"status": "success", "message": "任务已启动", "api_response": api_response})
    else:
        return jsonify({"status": "error", "message": "消息内容解析失败"})


@get_we_chat_message_blueprint.route('/set_flg/<flg>', methods=['GET', 'POST'])
def set_flg(flg):
    # 创建配置解析器
    config = configparser.ConfigParser()
    # 读取配置文件
    abs_path = "Doraemon/magnetFileDown/config.ini"
    config_path = Path(project_root) / abs_path
    config.read(config_path, encoding='utf-8')
    config['Flg']['flg'] = flg
    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    return f"Flag updated to {flg}", 200


@get_we_chat_message_blueprint.route('/get_magnet_list/<flg>', methods=['GET', 'POST'])
def get_magnet_list(flg):
    set_flg(flg)
    time.sleep(3)
    DownloadResources().main()
    return f'执行成功，等待数据返回'


def verify_signature(req):
    """
    验证消息来源是否合法
    """
    signature = req.args.get('signature')
    timestamp = req.args.get('timestamp')
    nonce = req.args.get('nonce')
    token = TOKEN

    # 对 token、timestamp、nonce 和 signature 进行排序
    sorted_list = sorted([token, timestamp, nonce])
    tmp_str = ''.join(sorted_list)

    # 用 SHA1 加密
    hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

    return hashcode == signature


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
