# Exchange Rate Query Tool

A command-line tool for querying exchange rates between Chinese Yuan (CNY) and New Taiwan Dollar (TWD) using Taiwan Bank's data.

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