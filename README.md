# ApiAutoTest

基于 `pytest + requests + openpyxl + allure` 的接口自动化测试项目，使用 Excel 维护测试用例，支持接口请求、响应断言、数据库断言、变量提取和 Allure 报告生成。

## 项目特点

- 使用 Excel 统一维护接口测试用例，降低新增用例成本
- 支持请求数据渲染、接口调用、响应断言、数据库断言和变量提取
- 支持按 `test` / `prod` 环境运行
- 支持生成 Allure 测试报告
- 飞书通知、数据库配置等敏感信息已改为环境变量读取，避免明文入库

## 目录结构

```text
.
├── config/                 # 配置模块
├── data/                   # Excel 测试用例
├── testcases/              # 测试用例入口
├── utils/                  # 工具方法
├── conftest.py             # pytest 全局夹具和汇总逻辑
├── pytest.ini             # pytest 日志配置
├── requirements.txt       # Python 依赖
└── run.py                 # 项目运行入口
```

## 运行环境

- macOS / Linux
- Python 3.10+
- MySQL 可访问测试环境
- 可选：Allure 命令行，用于生成 HTML 报告

安装 Allure：

```bash
brew install allure
```

## 安装依赖

建议先创建虚拟环境，再安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置环境变量

项目不再在代码中保存数据库密码、Webhook 或报告地址。请使用环境变量注入配置。

1. 复制模板：

```bash
cp .env.example .env.local
```

2. 按实际环境修改 `.env.local`
3. 执行前加载变量：

```bash
source .env.local
```

关键变量说明：

- `TEST_BASE_URL`：测试环境接口域名
- `TEST_DB_HOST / TEST_DB_PORT / TEST_DB_NAME / TEST_DB_USER / TEST_DB_PASSWORD`：测试环境数据库配置
- `PROD_BASE_URL`：生产环境接口域名
- `PROD_DB_HOST / PROD_DB_PORT / PROD_DB_NAME / PROD_DB_USER / PROD_DB_PASSWORD`：生产环境数据库配置
- `TEST_DEVICE_ID`：需要清理测试数据时使用的设备号，未配置则跳过收尾 SQL
- `FEISHU_IS_SEND`：是否发送飞书通知，`true` / `false`
- `FEISHU_WEBHOOK`：飞书机器人 Webhook
- `REPORT_PATH`：测试报告地址

## Excel 用例说明

默认用例文件：

```text
data/测试用例.xlsx
```

默认工作表：

```text
Sheet1
```

如需修改，可通过以下环境变量覆盖：

```bash
export EXCEL_FILE="./data/测试用例.xlsx"
export SHEET_NAME="Sheet1"
```

## 执行方式

运行测试环境：

```bash
python3 run.py test
```

运行生产环境：

```bash
python3 run.py prod
```

## 测试报告

- JSON 报告默认输出到 `report/json_report/`
- 若本机已安装 Allure，会自动生成 HTML 报告到 `report/html_report/`
- 若未安装 Allure，会跳过 HTML 报告生成

## 敏感信息处理

当前仓库已按以下原则处理敏感信息：

- 不在源码中保存数据库密码、Webhook、内部报告地址
- 测试报告、日志、缓存文件通过 `.gitignore` 忽略
- 建议使用脱敏后的测试账号、设备号和示例数据维护 Excel 用例

## 常见问题

### 1. 提示缺少环境变量

请先执行：

```bash
source .env.local
```

再重新运行测试。

### 2. 没有生成 HTML 报告

请确认已安装 Allure：

```bash
allure --version
```

如果命令不存在，请执行：

```bash
brew install allure
```
