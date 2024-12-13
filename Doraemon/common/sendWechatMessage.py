# !/usr/bin/python
# encoding=utf-8
# @FileName : sendWechatMessage.py
# @Time     : 2024/12/10 22:11
# @Author   : jiekc
import requests
import json

# 企业微信凭证
CORP_ID = "ww9fd4c96bc1b57759"  # 企业微信的 CorpID
SECRET = "VJuIpEuyrktBFiPpvgJ8_5odDfFiukuzmoCz5V5oUCE"  # 应用的 Secret
AGENT_ID = 1000002  # 应用的 AgentId


# 获取 AccessToken
def get_access_token():
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
    response = requests.get(url).json()
    return response.get("access_token")


# 发送消息
def send_message(to_user, message):
    access_token = get_access_token()
    if not access_token:
        print("获取 AccessToken 失败")
        return

    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": AGENT_ID,
        "text": {
            "content": message
        },
        "safe": 0
    }
    response = requests.post(url, data=json.dumps(payload))
    print(response.json())


# 发送图文消息
def send_news_message(articles, to_user="@all"):
    access_token = get_access_token()
    if not access_token:
        print("获取 AccessToken 失败")
        return
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,  # 目标用户，支持 UserID、@all 等
        "msgtype": "news",
        "agentid": AGENT_ID,
        "news": {"articles": articles},
        "safe": 0  # 非保密消息
    }
    response = requests.post(url, json=payload)
    return response.json()


# 上传文件并获取media_id
def upload_file(access_token, file_path):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file"
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"media": file})
    data = response.json()
    if data.get("errcode") == 0:
        return data.get("media_id")
    else:
        raise Exception(f"文件上传失败: {data}")


# 发送文件消息
def send_file_message(file_path, to_user="@all"):
    access_token = get_access_token()
    if not access_token:
        print("获取 AccessToken 失败")
        return
    media_id = upload_file(access_token, file_path)
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,  # 接收人：指定用户ID，或使用 "@all" 全员发送
        "msgtype": "file",
        "agentid": AGENT_ID,
        "file": {"media_id": media_id},
        "safe": 0  # 0 表示不保密，1 表示保密消息
    }
    response = requests.post(url, json=payload)
    return response.json()


# 示例发送消息
# send_message("kejie", "你好，这是一条测试消息！")
# message = [{
#     "title": "福建高颜长腿女神调教3P换妻好淫乱",
#     "description": "magnet:?xt=urn:btih:ac7e0462527f37892da7894656d2c0c8d38e7615&amp;tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&amp;tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&amp;tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
#     "url": "magnet:?xt=urn:btih:1F020C1FE517095CE952488A42EDFEAE37586E2A",
#     "picurl": "https://i0.wp.com/madouqu.com/wp-content/uploads/2024/12/1734092884-ae11b7867f1f4cb.png"
#     }]

# send_news_message(message, 'kejie')
# send_file_message('send_message.py', 'kejie')
import time
# 获取当前时间的时间戳
current_time = time.localtime()

# 获取年月日
year = current_time.tm_year
month = current_time.tm_mon
day = current_time.tm_mday
print(f"{year}{month:02d}{day:02d}")