#!/usr/bin/python
# encoding=utf-8
# @FileName : magentLinkDownload.py
# @Time     : 2024/6/6 22:00
# @Author   : jiekc

import requests
import re
import time
import logging
import random
import configparser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
from Doraemon.common.sendWechatMessage import send_message, send_news_message, send_file_message

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DownloadResources:
    def __init__(self):
        # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # 创建配置解析器
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read('config.ini', encoding='utf-8')

        # 访问默认节（DEFAULT）的值
        self.start_id = int(config['Index']['startID'])

        self.base_url = "https://madouqu.com/"
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
        ]
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "User-Agent": random.choice(self.user_agent_list),
        }
        self.proxies = {
            "http": "192.168.31.121:7890",
            "https": "192.168.31.121:7890",
        }
        url_home = f"{self.base_url}gccm/tx/"

        response = requests.get(url_home, headers=self.headers, proxies=self.proxies, verify=False, timeout=60)
        response.raise_for_status()
        response.encoding = 'utf-8'
        res_html = response.text

        # 正则表达式匹配 magnet 链接
        pattern = r'href="https://madouqu.com/tx(\d+)/"'
        numbers = re.findall(pattern, res_html)

        # 找到最大的数字
        if numbers:
            max_number = max(numbers)
            self.end_id = int(max_number) + 1
            logging.info(f"最大的数字是: {max_number}")
        else:
            self.end_id = self.start_id + 10
            logging.info("未找到任何数字")

        config['Index']['startID'] = str(self.end_id)
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        self.suc_list = []
        self.err_list = []
        self.link_list = []

        # 获取当前时间的时间戳
        current_time = time.localtime()
        time_str = time.strftime("%Y%m%d", current_time)
        self.file_name = f'magnet_links_{time_str}.txt'

    def load_accessing_web_pages(self, index):
        addr = f'tx{index}/'
        url = self.base_url + addr
        logging.info(f"请求 URL: {url}")
        try:
            time.sleep(random.uniform(1, 5))
            response = requests.get(url, headers=self.headers, proxies=self.proxies, verify=False, timeout=60)
            response.raise_for_status()
            response.encoding = 'utf-8'
            res_html = response.text

            # 正则表达式匹配 magnet 链接
            pattern_magnet = r'href="(magnet:[^"]+)"'
            pattern_title = r'entry-title">([^<]+)</h1>'
            pattern_png = r'srcset="([^"]+)\s\d+w'
            magnet_links = re.findall(pattern_magnet, res_html)
            title = re.findall(pattern_title, res_html)
            png_link = re.findall(pattern_png, res_html)

            if title and png_link:
                message = [{
                    "title": title[0],
                    "description": "点击查看详情",
                    "url": url,
                    "picurl": png_link[0]
                }]
                send_news_message(message, 'kejie')

            if magnet_links:
                logging.info(f"提取到的 magnet 链接: {magnet_links}")
                # 将 magnet 链接保存到文件
                with open(self.file_name, "a") as f:
                    for link in magnet_links:
                        f.write(link + "\n")
                        self.suc_list.append(index)
            else:
                logging.info("未提取到 magnet 链接")
                self.err_list.append(index)

        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败: {e}")
            self.err_list.append(index)

    def fetch_all_pages(self, index_list):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.load_accessing_web_pages, i) for i in index_list]
            for future in as_completed(futures):
                try:
                    future.result()  # 获取每个线程的结果，确保处理任何抛出的异常
                except Exception as e:
                    logging.error(f"线程异常: {e}")

    def main(self):
        index_list = range(self.start_id, self.end_id)
        self.fetch_all_pages(index_list)

        # 输出成功和失败的记录
        logging.info(f"成功访问的索引: {self.suc_list}")
        logging.info(f"失败访问的索引: {self.err_list}")

        suc_message = '无成功索引数据' if not self.suc_list else f'成功索引：{self.suc_list}'
        err_message = '无失败索引数据' if not self.err_list else f'失败索引：{self.err_list}'

        send_file_message(self.file_name, 'kejie')
        send_message('kejie', suc_message)
        send_message('kejie', err_message)


if __name__ == "__main__":
    dr = DownloadResources()
    dr.main()
