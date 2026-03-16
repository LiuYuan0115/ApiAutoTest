import logging
import os
from datetime import datetime
import allure
import random
import re
from config.config import GLOBAL_ID_MAP


@allure.step("1.解析请求数据")
def analyse_case(case):
    method = case["method"]
    # 从环境变量中获取url
    url = os.environ["URL"] + case["path"]
    # url = BASE_URL + case["path"]
    hearders = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    # json = eval(case["json"]) if isinstance(case["json"], str) else None

    # 支持随机id复用逻辑
    group = case.get("group", "") or "default"  # 没有写group就放default组
    json_data = case["json"]
    if isinstance(json_data, str):
        # 随机ID：仅首次生成
        if "ly-随机id" in json_data:
            if group not in GLOBAL_ID_MAP:
                GLOBAL_ID_MAP[group] = f"ly-{random.randint(100000, 999999)}"
            json_data = re.sub('"ly-随机id"', f'"{GLOBAL_ID_MAP[group]}"', json_data)

        # 替换 "ly-随机数" 为随机字符串
        json_data = re.sub(r'"ly-随机数"', f'"ly-{random.randint(1, 9999999999)}"', json_data)
        json_data = re.sub(r'"ly-时间"', f'"ly-{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}-{random.randint(1, 999)}"', json_data)
        json_data = re.sub(r'"ly-日期"', f'"ly-{datetime.now().strftime("%Y-%m-%d")}"', json_data)
        json = eval(json_data)
    else:
        json = None
    files = eval(case["files"]) if isinstance(case["files"], str) else None

    request_data = {
        "method": method,
        "url": url,
        "headers": hearders,
        "params": params,
        "data": data,
        "json": json,
        "files": files,
    }
    logging.info(f"✅ 1.解析请求数据, 请求数据为: {request_data}")
    allure.attach(f"{request_data}", name="解析数据结果")
    return request_data
