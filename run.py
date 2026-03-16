import os
import json
import logging
import subprocess
import sys

import pytest

from utils.send_feishu_msg import send_feishu_message


def build_db_config(env_name):
    """根据环境前缀读取数据库配置。"""
    prefix = env_name.upper()
    field_mapping = {
        "host": "DB_HOST",
        "port": "DB_PORT",
        "database": "DB_NAME",
        "user": "DB_USER",
        "password": "DB_PASSWORD",
    }
    db_config = {}
    missing_vars = []

    for field, suffix in field_mapping.items():
        env_key = f"{prefix}_{suffix}"
        env_value = os.environ.get(env_key)
        if not env_value:
            missing_vars.append(env_key)
            continue
        db_config[field] = int(env_value) if field == "port" else env_value

    return db_config, missing_vars


def prepare_runtime_env(env_name):
    """将运行时需要的配置整理到统一环境变量中。"""
    normalized_env = env_name.lower()
    if normalized_env not in {"test", "prod"}:
        raise ValueError("Unsupported environment. Use 'test' or 'prod'.")

    base_url_key = f"{normalized_env.upper()}_BASE_URL"
    base_url = os.environ.get(base_url_key, "").rstrip("/")
    db_config, missing_vars = build_db_config(normalized_env)

    if not base_url:
        missing_vars.append(base_url_key)

    if missing_vars:
        missing_text = ", ".join(missing_vars)
        raise ValueError(f"Missing required environment variables: {missing_text}")

    os.environ["URL"] = base_url
    os.environ["DB"] = json.dumps(db_config)
    os.environ["ENV"] = normalized_env


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        try:
            prepare_runtime_env(sys.argv[1])
        except ValueError as exc:
            logging.error(str(exc))
            sys.exit(1)
    else:
        logging.error("Usage: python3 run.py test or python3 run.py prod")
        sys.exit(1)

    pytest.main(["-vs", "./testcases/test_stream.py", "--alluredir", "./report/json_report", "--clean-alluredir"])

    # 检查 allure 命令是否存在
    try:
        subprocess.run(["allure", "--version"], check=True, capture_output=True)
        os.system("allure generate ./report/json_report -o ./report/html_report --clean")
        logging.info("Allure报告生成成功")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.warning("Allure command not found. Skip HTML report generation. Install it with 'brew install allure' or 'npm install -g allure-commandline'.")
