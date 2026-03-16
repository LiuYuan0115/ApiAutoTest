import json
import logging

import allure
import jsonpath
from utils.send_request import send_jdbc_request


# @allure.step("3.HTTP响应断言")
# def http_assert(case, res):
#     # if case["check"]:
#     #     result = jsonpath.jsonpath(res.json(), case["check"])[0]
#     #     logging.info(f'3.HTTP响应断言内容: 实际结果({result}) == 预期结果({case["expected"]})')
#     #     assert result == case["expected"]
#     # else:
#     #     logging.info(f'3.HTTP响应断言内容: 预期结果({case["expected"]}) in 实际结果({res.text})')
#     #     assert case["expected"] in res.text

#     # 双重断言
#     expected = eval(case["expected"])
#     if case["check"]:
#         # 把断言的字段和预期结果转为列表
#         check = eval(case["check"])
#         # 共同来遍历两个列表
#         for c, e in zip(check, expected):
#             result = jsonpath.jsonpath(res.json(), f"$.{c}")[0]
#             logging.info(f'3.HTTP响应断言内容: 实际结果({result}) == 预期结果({e})')
#             assert result == e
#     else:
#         for e in expected:
#             logging.info(f'3.HTTP响应断言内容: 预期结果({e}) in 实际结果({res.text})')
#             assert str(e) in res.text


@allure.step("3.HTTP流式响应断言")
def stream_assert(case,res):
    # 双重断言
    expected = eval(case["expected"])
    if case["check"]:
        # 把断言的字段和预期结果转为列表
        check = eval(case["check"])

        # 初始化每个字段的成功断言计数为 0
        match_counter = {c: 0 for c in check}

        for line in res.iter_lines(decode_unicode=True):
            if line:
                # 如果是 SSE 格式的流（data: 前缀）
                if line.startswith("data:"):
                    line = line[5:].strip()
                elif res.status_code == 200:
                    pass
                else:
                    logging.error(f'❌ 3.HTTP响应断言失败,状态码："{res.status_code}"')
                    assert res.status_code == 200
                try:
                    data = json.loads(line)
                    # 共同来遍历两个列表
                    for c, e in zip(check, expected):
                        if data.get(c) is not None:
                            result = jsonpath.jsonpath(data, f"$.{c}")[0]
                            print(f'"{c}":"{result}"')
                            if result == e:
                                match_counter[c] += 1
                                logging.info(f'✅ 3.HTTP响应断言内容"{c}": 实际结果（"{result}") == 预期结果("{e}")')
                                assert result == e
                            elif str(e) in result:
                                match_counter[c] += 1
                                logging.info(f'✅ 3.HTTP响应断言内容: 预期结果({e}) in 实际结果({result})')
                                assert str(e) in result
                    print("🔹 解析数据:", json.dumps(data, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("⚠️ 原始响应:", line)

        # 最后统计哪些字段断言次数为 0
        for c in match_counter:
            if match_counter[c] == 0:
                logging.info(f'⚠️ 字段"{c}"在所有流响应中没有任何一次断言成功（预期：{expected[check.index(c)]}）')
                assert match_counter[c] != 0

    else:
        for e in expected:
            logging.info(f'✅ 3.HTTP响应断言内容: 预期结果({e}) in 实际结果({res.text})')
            assert str(e) in res.text

def jdbc_assert(case):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC响应断言"):
            result = send_jdbc_request(case["sql_check"])
            logging.info(f'3.JDBC响应断言内容: 实际结果({result}) == 预期结果({case["sql_expected"]})')
            assert result == case["sql_expected"]
