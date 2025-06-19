# Exchange Rate Query Tool

## 介紹

本工具可查詢台灣銀行匯率歷史資料，支援 CLI 與 Python 程式呼叫。

---

## 安裝需求
- requests
- beautifulsoup4

安裝：
```
pip install -r requirements.txt
```

---

## CLI 用法

```bash
python exchange_tool.py "CNY to TWD last 3 months"
python exchange_tool.py "USD to TWD 2024-01-01~2024-03-31"
```

查詢格式：
- `CURRENCY1 to CURRENCY2 [last X months/years]`
- `CURRENCY1 to CURRENCY2 YYYY-MM-DD~YYYY-MM-DD`

---

## 程式呼叫範例

```python
from exchange_tool import ExchangeTool

tool = ExchangeTool()
# 查人民幣對台幣近一個月
result = tool.run("CNY to TWD")
# 查美元對台幣近一年
result = tool.run("USD to TWD last 1 year")
# 查人民幣對台幣 2024/1/1~2024/3/31
result = tool.run("CNY to TWD 2024-01-01~2024-03-31")

# 取得 dict 結果，可直接給 LLM 或程式處理
print(result)

# 若要印出格式化資訊
tool.print_result(result)
```

---

## 回傳格式
- `current_rate`: 最新匯率
- `statistics`: 平均、最高、最低、趨勢、期間
- `historical_data`: 每日匯率列表
- 若查詢錯誤，dict 會有 `error` 欄位

---

## 注意事項
- 目前僅支援台灣銀行網站，且網址預設查詢 CNY（如需多幣別請修改程式）

## Features

- Query current exchange rate between CNY and TWD
- View historical exchange rate data
- Calculate statistics including average, minimum, and maximum rates
- Analyze exchange rate trends
- Support for custom time ranges
- Detailed historical data display

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Query the current exchange rate:
```bash
python exchange_tool.py "CNY to TWD"
```

### Time Range Queries

You can specify a time range in two ways:

1. Relative time range:
```bash
# Last 1 month
python exchange_tool.py "CNY to TWD last 1 months"

# Last 1 year
python exchange_tool.py "CNY to TWD last 1 years"
```

2. Absolute date range:
```bash
# Specific date range
python exchange_tool.py "CNY to TWD 2025-05-01~2025-05-30"
```

### Output Format

The tool provides the following information:
- Current exchange rate
- Statistics:
  - Average rate
  - Minimum rate
  - Maximum rate
  - Trend analysis
  - Period covered
- Historical data (last 10 entries)

## Project Structure

```
.
├── README.md                 # Project documentation
├── exchange_tool.py      # Main script for exchange rate queries
└── requirements.txt          # Python package dependencies
```