import json
import os

import pymysql
import pytest

from config.config import *
from utils.send_feishu_msg import send_feishu_message


@pytest.fixture(scope="session", autouse=True)
def destroy_data():

    yield

    sqls = [sql for sql in (SQL1, SQL2, SQL3) if sql]
    db_config = os.environ.get("DB")
    if not sqls or not db_config:
        return

    conn = pymysql.Connect(
        **json.loads(db_config),
        charset="utf8",
        autocommit=True
    )
    cur = conn.cursor()

    for sql in sqls:
        cur.execute(sql)

    cur.close()
    conn.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # 获取测试结果
    outcome = yield
    summary = terminalreporter.summary_stats()

    # 提取测试数据
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))

    # 发送飞书消息
    send_feishu_message(total, passed, failed)
