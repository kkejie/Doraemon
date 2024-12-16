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


# 上传文件并获取media_id
def upload_file(file_path):
    access_token = get_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file"
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"media": file}, timeout=3600)
    data = response.json()
    if data.get("errcode") == 0:
        return data.get("media_id")
    else:
        raise Exception(f"文件上传失败: {data}")


# 获取 AccessToken
def get_access_token():
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
    response = requests.get(url)
    data = response.json()
    if data.get("errcode") == 0:
        return data.get("access_token")
    else:
        raise Exception(f"获取 AccessToken 失败: {data}")


# 通用发送消息方法
def send_message(payload):
    access_token = get_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    response = requests.post(url, json=payload)
    return response.json()


# 发送消息
def send_text_message(message, to_user="@all"):
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": AGENT_ID,
        "text": {
            "content": message
        },
        "safe": 0
    }
    return send_message(payload)


# 发送图片消息
def send_image_message(file_path, touser="@all"):
    media_id = upload_file(file_path)
    payload = {
        "touser": touser,
        "msgtype": "image",
        "agentid": AGENT_ID,
        "image": {"media_id": media_id}
    }
    return send_message(payload)


# 发送图文消息
def send_news_message(articles, to_user="@all"):
    payload = {
        "touser": to_user,  # 目标用户，支持 UserID、@all 等
        "msgtype": "news",
        "agentid": AGENT_ID,
        "news": {"articles": articles},
        "safe": 0  # 非保密消息
    }
    return send_message(payload)


# 发送文件消息
def send_file_message(file_path, to_user="@all"):
    media_id = upload_file(file_path)
    payload = {
        "touser": to_user,  # 接收人：指定用户ID，或使用 "@all" 全员发送
        "msgtype": "file",
        "agentid": AGENT_ID,
        "file": {"media_id": media_id},
        "safe": 0  # 0 表示不保密，1 表示保密消息
    }
    return send_message(payload)


# 发送文本卡片消息
def send_textcard_message(text_card, touser="@all"):
    payload = {
        "touser": touser,
        "msgtype": "textcard",
        "agentid": AGENT_ID,
        "textcard": text_card
    }
    return send_message(payload)


# 发送语音消息
def send_voice_message(media_id, touser="@all"):
    payload = {
        "touser": touser,
        "msgtype": "voice",
        "agentid": AGENT_ID,
        "voice": {"media_id": media_id}
    }
    return send_message(payload)


# 发送视频消息
def send_video_message(file_path, title, description, touser="@all"):
    media_id = upload_file(file_path)
    payload = {
        "touser": touser,
        "msgtype": "video",
        "agentid": AGENT_ID,
        "video": {
            "media_id": media_id,
            "title": title,
            "description": description
        }
    }
    return send_message(payload)


# 发送 Markdown 消息
def send_markdown_message(content, touser="@all"):
    payload = {
        "touser": touser,
        "msgtype": "markdown",
        "agentid": AGENT_ID,
        "markdown": {"content": content}
    }
    return send_message(payload)


# 发送小程序通知消息
def send_miniprogram_notice(appid, page, title, description, touser="@all"):
    payload = {
        "touser": touser,
        "msgtype": "miniprogram_notice",
        "agentid": AGENT_ID,
        "miniprogram_notice": {
            "appid": appid,
            "page": page,
            "title": title,
            "description": description
        }
    }
    return send_message(payload)

# 示例发送消息
# send_text_message("https://i0.wp.com/madouqu.com/wp-content/uploads/2024/12/1734177420-5ba3597367aacd1.png", "kejie")
# send_text_message("https://i0.wp.com/madouqu4.xyz/wp-content/uploads/2024/12/1734238613-fb5e597c183bf7f.png", "kejie")
# message = {
#     "title": "福建高颜长腿女神调教3P换妻好淫乱xyz",
#     "description": "点击查看",
#     "url": "https://madouqu.com/tx1770/",
#     "picurl": "https://i0.wp.com/madouqu4.xyz/wp-content/uploads/2024/12/1734177420-5ba3597367aacd1.png"
#     }
#
# send_news_message(message, 'kejie')
#
# message = {
#     "title": "福建高颜长腿女神调教3P换妻好淫乱com",
#     "description": "点击查看",
#     "url": "https://madouqu.com/tx1770/",
#     "picurl": "https://i0.wp.com/madouqu.com/wp-content/uploads/2024/12/1734238613-fb5e597c183bf7f.png"
#     }
# send_news_message(message, 'kejie')

# send_file_message('send_message.py', 'kejie')

# text_card = {
#     "title": "福建高颜长腿女神调教3P换妻好淫乱",
#     "description": "magnet:?xt=urn:btih:ac7e0462527f37892da7894656d2c0c8d38e7615&amp;tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&amp;tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&amp;tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
#     "url": "https://madouqu.com/tx1770/",
#     "btntxt": "https://i0.wp.com/madouqu.com/wp-content/uploads/2024/12/1734177420-5ba3597367aacd1.png"
# }

# send_textcard_message(text_card, 'kejie')
# send_video_message(r"Z:\迅雷下载\【性爱调教重磅首发】字母圈资深大神『森杰』圈养调教极品性奴『小玲曼曼』性爱开发全记录 高清720P原版\_GHDRz5KvC2kahrJ.mp4","喝醉的女大学生被我捡了便宜", "简介", 'kejie')
# send_video_message(r"Z:\Downloads\9kg\短视频\麻豆传媒\MD0316 4P轮奸可爱女球经 赢了比赛熟了小穴-麻豆社.ts","4P轮奸可爱女球经 赢了比赛熟了小穴", "MD0316 4P轮奸可爱女球经 赢了比赛熟了小穴-麻豆社", 'kejie')
