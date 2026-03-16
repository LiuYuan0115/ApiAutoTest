import logging
import allure
import jsonpath
import re
from utils.send_request import send_jdbc_request


def json_extractor(case, all, res):
    if case["jsonExData"]:
        with allure.step("4.JSON提取"):
            # 首先要把 jsonExData 的 key, value 拆开
            for key, value in eval(case["jsonExData"]).items():
                if value == "plain":
                    # 如果 Excel 写的是 "plain"，就取整个 res.text
                    value = res.text

                elif value.startswith("urlpart:"):
                    # 特殊提取指令，提取 URL 的路径部分
                    path_value = value.replace("urlpart:", "")
                    full_url = jsonpath.jsonpath(res.json(), path_value)[0]
                    match = re.search(r'https?://[^/]+/(.+)', full_url)
                    value = match.group(1) if match else full_url


                elif value.startswith("filename:"):
                    path_expr = value.replace("filename:", "")
                    full_url = jsonpath.jsonpath(res.json(), path_expr)[0]
                    value = full_url.rstrip("/").split("/")[-1]  # 最后一段

                elif value.startswith("dirname:"):
                    path_expr = value.replace("dirname:", "")
                    full_url = jsonpath.jsonpath(res.json(), path_expr)[0]
                    path_part = re.search(r'https?://[^/]+/(.+)', full_url)
                    if path_part:
                        segments = path_part.group(1).split("/")
                        value = segments[0] if segments else ""

                else:
                    # 正常的 JSONPath 提取
                    value = jsonpath.jsonpath(res.json(), value)[0]
                all[key] = value
            logging.info(f'4.JSON提取, 根据{case["jsonExData"]}提取数据, 此时全局变量为: {all}')


def jdbc_extractor(case, all):
    if case["sqlExData"]:
        with allure.step("4.JDBC提取"):
            for key, value in eval(case["sqlExData"]).items():
                # print(key)
                # print(value)
                value = send_jdbc_request(value)
                # print(value)
                all[key] = value
                # print(all)
            logging.info(f'4.JDBC提取, 根据{case["sqlExData"]}提取数据, 此时全局变量为: {all}')


def request_extractor(case, all, json_body):
    if case.get("reqExData"):
        with allure.step("4.请求体字段提取"):
            for key, path in eval(case["reqExData"]).items():
                result = jsonpath.jsonpath(json_body, path)
                value = result[0] if result and isinstance(result, list) else ""
                all[key] = value
            logging.info(f'4.请求体字段提取，根据 {case["reqExData"]} 提取数据，当前全局变量为: {all}')