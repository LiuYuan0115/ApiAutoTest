import requests
from config.config import *
import time


def send_feishu_message(total_cases=0, passed_cases=0, failed_cases=0):
    """发送飞书消息，包含测试用例统计信息
    Args:
        total_cases: 总用例数
        passed_cases: 成功用例数
        failed_cases: 失败用例数
    """
    # 计算成功率
    pass_rate = f"{(passed_cases / total_cases * 100):.2f}%" if total_cases > 0 else "0%"

    detail_content = [
        {
            "tag": "text",
            "text": "详细信息："
        }
    ]
    if REPORT_PATH:
        detail_content.append({
            "tag": "a",
            "text": "查看测试报告",
            "href": REPORT_PATH
        })
    else:
        detail_content.append({
            "tag": "text",
            "text": "未配置报告地址"
        })

    message_data = [
        [
            {
                "tag": "text",
                "text": f"项目名称：{PROJECT}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"ִ执行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"用例总数：{total_cases}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"成功数量：{passed_cases}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"失败数量：{failed_cases}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"成功率：{pass_rate}"
            }
        ],
        [
            {
                "tag": "text",
                "text": f"其中预计失败 0 条..."
            }
        ],
        detail_content
    ]

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "接口自动化测试报告",
                    "content": message_data
                }
            }
        }
    }
    if FEISHU_IS_SEND and WEBHOOK:
        response = requests.post(WEBHOOK, json=payload)
        return response

    return None


if __name__ == '__main__':
    send_feishu_message()
