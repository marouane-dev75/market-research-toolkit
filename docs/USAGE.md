# Usage Guide

This comprehensive guide covers all features and commands available in the Ticker Analysis Tool.

## 🎯 Quick Start

### Basic Analysis
```bash
# Analyze Apple Inc.
python main.py analysis AAPL

# Using aliases
python main.py a MSFT
python main.py analyze GOOGL
```

### Magic Formula Screening
```bash
# Screen multiple stocks
python main.py magic AAPL,MSFT,GOOGL,TSLA

# Using yearly data
python main.py magic AAPL,MSFT,GOOGL yearly
```

## 📊 Available Commands

### 1. Comprehensive Analysis (`analysis`)

**Purpose**: Complete financial analysis of a single company

**Usage**:
```bash
python main.py analysis <TICKER>
python main.py a <TICKER>          # Short alias
python main.py analyze <TICKER>    # Long alias
```

**Examples**:
```bash
python main.py analysis AAPL
python main.py a MSFT
python main.py analyze TSLA
```

**Output Includes**:
- Basic company information
- Market data (price, market cap, volume)
- Technical analysis (RSI, MACD, Moving Averages)
- Financial health assessment
- Income statement analysis
- Balance sheet analysis
- Cash flow analysis
- Dividend analysis (if applicable)
- Price analysis with percentage changes

### 2. Magic Formula Screening (`magic`)

**Purpose**: Screen stocks using Joel Greenblatt's Magic Formula methodology

**Usage**:
```bash
python main.py magic <TICKER1,TICKER2,...> [FREQUENCY]
python main.py mf <TICKERS>                    # Short alias
python main.py magic_formula <TICKERS>         # Long alias
```

**Parameters**:
- `TICKERS`: Comma-separated list of stock symbols
- `FREQUENCY`: `yearly`, `quarterly`, `year`, `quarter`, `y`, or `q` (default: quarterly)

**Examples**:
```bash
python main.py magic AAPL,MSFT,GOOGL
python main.py magic AAPL,MSFT,GOOGL quarterly
python main.py magic JPM,BAC,WFC,C yearly
python main.py mf TSLA,NVDA,AMD,INTC q
```

**Output**:
- Ranked stocks by Magic Formula score
- Earnings Yield and Return on Capital for each stock
- Individual rankings and combined scores
- Excluded stocks with missing data

### 3. Individual Analysis Commands

#### Income Statement Analysis (`income`)
```bash
python main.py income <TICKER> [FREQUENCY]
python main.py inc <TICKER>                    # Short alias

# Examples
python main.py income AAPL quarterly
python main.py inc MSFT yearly
```

#### Balance Sheet Analysis (`balance`)
```bash
python main.py balance <TICKER> [FREQUENCY]
python main.py bal <TICKER>                    # Short alias

# Examples
python main.py balance GOOGL quarterly
python main.py bal TSLA yearly
```

#### Cash Flow Analysis (`cashflow`)
```bash
python main.py cashflow <TICKER> [FREQUENCY]
python main.py cf <TICKER>                     # Short alias

# Examples
python main.py cashflow NVDA quarterly
python main.py cf AMD yearly
```

#### Dividend Analysis (`dividend`)
```bash
python main.py dividend <TICKER>
python main.py div <TICKER>                    # Short alias

# Examples
python main.py dividend KO
python main.py div JNJ
```

#### Price Analysis (`price`)
```bash
python main.py price <TICKER> [PERIOD]
python main.py p <TICKER>                      # Short alias

# Examples
python main.py price AAPL 1y
python main.py p MSFT 6mo
```

**Available Periods**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

#### Company Information (`info`)
```bash
python main.py info <TICKER>
python main.py i <TICKER>                      # Short alias

# Examples
python main.py info AAPL
python main.py i MSFT
```

### 4. Price Monitoring (`monitor`)

**Purpose**: Monitor stock prices against configured thresholds

**Usage**:
```bash
python main.py monitor [OPTIONS]
python main.py m [OPTIONS]                     # Short alias
python main.py watch [OPTIONS]                 # Alternative alias
python main.py alert [OPTIONS]                 # Alternative alias
```

**Options**:
- `--status`: Show current monitoring configuration
- `--test`: Test configuration and send test notification
- `--help`: Show detailed help

**Examples**:
```bash
python main.py monitor                         # Run monitoring check
python main.py monitor --status                # Show configuration
python main.py monitor --test                  # Test setup
python main.py m                              # Using alias
```

**Configuration**: Set up thresholds in [`config/config.yml`](../config/config.yml):
```yaml
price_monitor:
  enabled: true
  thresholds:
    - "AAPL:gt:150"    # Alert when Apple > $150
    - "MSFT:lt:300"    # Alert when Microsoft < $300
    - "GOOGL:gte:2500" # Alert when Google >= $2500
```

### 5. Cache Management (`cache`)

**Purpose**: Manage cached financial data

**Usage**:
```bash
python main.py cache <ACTION> [TICKER]
python main.py c <ACTION>                      # Short alias
```

**Actions**:
- `status`: Show cache status and statistics
- `clear`: Clear all cached data
- `clear <TICKER>`: Clear cache for specific ticker

**Examples**:
```bash
python main.py cache status                    # Show cache info
python main.py cache clear                     # Clear all cache
python main.py cache clear AAPL                # Clear Apple cache
python main.py c status                        # Using alias
```

## 🔧 Advanced Usage

### Batch Processing

**Magic Formula with Many Stocks**:
```bash
# Screen large number of stocks
python main.py magic AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,META,NFLX,CRM,ADBE

# Using file input (create tickers.txt with one ticker per line)
python main.py magic $(cat tickers.txt | tr '\n' ',' | sed 's/,$//')
```

### Automation and Scripting

**Daily Monitoring Script** (`scripts/daily_check.sh`):
```bash
#!/bin/bash
echo "=== Daily Stock Analysis ==="
python main.py monitor
python main.py analysis AAPL
python main.py magic AAPL,MSFT,GOOGL,AMZN
```

**Portfolio Analysis Script** (`scripts/portfolio_analysis.py`):
```python
#!/usr/bin/env python3
import subprocess
import sys

portfolio = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in portfolio:
    print(f"\n=== Analyzing {ticker} ===")
    subprocess.run([sys.executable, "main.py", "analysis", ticker])
```

### Configuration Customization

**Cache Settings**:
```yaml
data:
  cache_directory: "data"
  cache:
    company_info:
      ttl_hours: 168      # 1 week
    price_data:
      ttl_hours: 24       # 1 day
    income_statements:
      ttl_hours: 168      # 1 week
```

**Logging Configuration**:
```yaml
logging:
  level: INFO                     # DEBUG, INFO, WARNING, ERROR
```

**Application Settings**:
```yaml
application:
  debug_mode: false
  default_output_format: "console"
```

## 📈 Understanding Output

### Technical Analysis Scores

**RSI (Relative Strength Index)**:
- 0-30: Oversold (potentially undervalued)
- 30-70: Neutral
- 70-100: Overbought (potentially overvalued)

**MACD (Moving Average Convergence Divergence)**:
- Bullish: MACD line above signal line
- Bearish: MACD line below signal line

**Overall Technical Score**:
- 1-3: Strong Sell
- 4-6: Sell/Hold
- 7-8: Buy
- 9-10: Strong Buy

### Magic Formula Interpretation

**Earnings Yield**: EBIT / Enterprise Value
- Higher is better (company generates more earnings per dollar of value)

**Return on Capital**: EBIT / Invested Capital  
- Higher is better (company uses capital more efficiently)

**Magic Formula Score**: Combined ranking (lower is better)
- Rank 1 = Best Magic Formula candidate
- Higher ranks = Less attractive by Magic Formula criteria

### Financial Health Ratings

**Overall Ratings**:
- Excellent: Strong across all metrics
- Good: Above average performance
- Fair: Mixed performance
- Poor: Below average performance
- Critical: Significant concerns

## 🚨 Error Handling

### Common Issues and Solutions

**No Data Available**:
```bash
# Try different ticker symbol
python main.py analysis AAPL    # Instead of APPLE

# Check if ticker exists
python main.py info UNKNOWN_TICKER
```

**Network Issues**:
```bash
# Test connectivity
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['symbol'])"

# Clear cache and retry
python main.py cache clear
python main.py analysis AAPL
```

**Configuration Issues**:
```bash
# Test monitoring configuration
python main.py monitor --test

# Validate config file
python -c "import yaml; yaml.safe_load(open('config/config.yml'))"
```

## 💡 Tips and Best Practices

### Performance Optimization

1. **Use Caching**: Let the cache system work - repeated queries are much faster
2. **Batch Analysis**: Use Magic Formula for multiple stocks instead of individual analysis
3. **Appropriate Frequency**: Use quarterly data for recent analysis, yearly for trends

### Analysis Best Practices

1. **Combine Multiple Metrics**: Don't rely on single indicators
2. **Consider Context**: Market conditions affect all metrics
3. **Historical Perspective**: Look at trends, not just current values
4. **Diversification**: Analyze multiple stocks in different sectors

### Monitoring Setup

1. **Reasonable Thresholds**: Set alerts for significant price movements
2. **Test Configuration**: Always test before relying on alerts
3. **Regular Updates**: Review and update thresholds periodically

## 🔗 Integration Examples

### Jupyter Notebook Integration

```python
import subprocess
import json

def analyze_stock(ticker):
    """Analyze stock and return structured data."""
    result = subprocess.run(
        ["python", "main.py", "analysis", ticker],
        capture_output=True, text=True
    )
    return result.stdout

# Analyze multiple stocks
stocks = ["AAPL", "MSFT", "GOOGL"]
for stock in stocks:
    print(f"=== {stock} ===")
    print(analyze_stock(stock))
```

### Cron Job Setup

```bash
# Add to crontab for daily monitoring at 9 AM
0 9 * * * cd /path/to/ticker_analysis && python main.py monitor

# Weekly portfolio analysis on Sundays at 10 AM  
0 10 * * 0 cd /path/to/ticker_analysis && python scripts/portfolio_analysis.py
```

---

**Ready to analyze the markets! 📊**

For more detailed information, see:
- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](CONFIGURATION.md)
- [API Documentation](API.md)