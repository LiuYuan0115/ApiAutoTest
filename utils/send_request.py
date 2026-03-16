import json
import logging
import os

import allure
import pymysql
import requests


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    res.encoding = 'utf-8'
    response_text=res.text if res.text else "<空响应>"
    logging.info(f"✅ 2.发送HTTP请求, 响应状态码：{res.status_code};响应文本为: {response_text}")
    return res

def send_jdbc_request(sql, index=0):
    conn = pymysql.Connect(
        **json.loads(os.environ["DB"]),
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]


