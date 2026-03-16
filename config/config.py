import os

# excel格式的测试用例文件配置
EXCEL_FILE = os.environ.get("EXCEL_FILE", "./data/测试用例.xlsx")
SHEET_NAME = os.environ.get("SHEET_NAME", "Sheet1")

# mysql资源销毁，未配置设备号时自动跳过
TEST_DEVICE_ID = os.environ.get("TEST_DEVICE_ID", "")
SQL1 = f'select * from userInfo where deviceid = "{TEST_DEVICE_ID}"' if TEST_DEVICE_ID else ""
SQL2 = f'select * from userInfo where deviceid = "{TEST_DEVICE_ID}"' if TEST_DEVICE_ID else ""
SQL3 = f'select * from userInfo where deviceid = "{TEST_DEVICE_ID}"' if TEST_DEVICE_ID else ""

# 飞书相关配置文件
WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

# 项目名称
PROJECT = os.environ.get("PROJECT_NAME", "solvely-plugin项目")

# 是否发送飞书消息的开关
FEISHU_IS_SEND = os.environ.get("FEISHU_IS_SEND", "false").lower() == "true"

# 测试报告地址
REPORT_PATH = os.environ.get("REPORT_PATH", "")

# 用于存储每组的共享ID
GLOBAL_ID_MAP = {}