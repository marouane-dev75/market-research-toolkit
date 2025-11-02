# Ticker Analysis Tool

A comprehensive financial analysis tool for stock market research, screening, and monitoring. This Python application provides detailed company analysis, technical indicators, Magic Formula screening, and real-time price monitoring with notifications.

## 🚀 Features

### 📊 Comprehensive Analysis
- **Company Information**: Basic info, market data, valuation metrics
- **Financial Statement Analysis**: Income statement, balance sheet, and cash flow analysis
- **Technical Analysis**: MACD, RSI, Moving Averages, Bollinger Bands with scoring
- **Price Analysis**: Multi-timeframe price movements and volume analysis
- **Dividend Analysis**: Historical dividend trends and statistics

### 🔍 Magic Formula Screening
- Implementation of Joel Greenblatt's Magic Formula from "The Little Book That Beats the Market"
- Ranks stocks by Earnings Yield and Return on Capital
- Supports both quarterly and yearly data analysis
- Batch processing of multiple tickers

### 📈 Price Monitoring & Alerts
- Real-time price threshold monitoring
- Telegram notifications for triggered alerts
- Configurable thresholds with multiple operators (>, <, =, >=, <=)
- Support for multiple notification providers

### ⚡ Performance & Caching
- Intelligent caching system with configurable TTL
- Optimized data fetching from Yahoo Finance
- Concurrent processing for multiple tickers

### 🎨 Rich Console Output
- Professional formatting with colors and structured display
- Detailed help system for all commands
- Progress indicators and status messages

## 📋 Requirements

- Python 3.8+
- Internet connection for financial data fetching
- Optional: Telegram Bot Token for notifications

## 🛠️ Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ticker_analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run your first analysis**
   ```bash
   python main.py analysis AAPL
   ```

## 🚀 Quick Start Guide

### Basic Company Analysis
```bash
# Comprehensive analysis of Apple Inc.
python main.py analysis AAPL

# Quick aliases
python main.py a MSFT
python main.py analyze GOOGL
```

### Magic Formula Screening
```bash
# Screen multiple stocks using Magic Formula
python main.py magic AAPL,MSFT,GOOGL,TSLA

# Use yearly data instead of quarterly
python main.py magic AAPL,MSFT,GOOGL yearly

# Quick alias
python main.py mf JPM,BAC,WFC,C
```

### Individual Analysis Commands
```bash
# Income statement analysis
python main.py income AAPL quarterly

# Balance sheet analysis
python main.py balance MSFT yearly

# Cash flow analysis
python main.py cashflow GOOGL

# Dividend analysis
python main.py dividend KO

# Price analysis with technical indicators
python main.py price TSLA
```

### Price Monitoring
```bash
# Run monitoring check
python main.py monitor
```

### Cache Management
```bash
# Clear all cache
python main.py cache clear

# Show cache status
python main.py cache status

# Clear specific ticker cache
python main.py cache clear AAPL
```

## ⚙️ Configuration

### Basic Configuration

The application uses a YAML configuration file located at [`config/config.yml`](config/config.yml). Key settings include:

```yaml
# Application Settings
application:
  name: "Ticker Analysis Tool"
  version: "1.0.0"
  debug_mode: false

# Data Caching (TTL in hours)
data:
  cache_directory: "data"
  cache:
    company_info:
      ttl_hours: 168  # 1 week
    price_data:
      ttl_hours: 24   # 1 day

# Telegram Notifications
telegram:
  enabled: true
  bot_token: "YOUR_BOT_TOKEN_HERE"
  chat_id: "YOUR_CHAT_ID_HERE"

# Price Monitoring
price_monitor:
  enabled: true
  thresholds:
    - "AAPL:gt:150"    # Alert when Apple > $150
    - "MSFT:lt:300"    # Alert when Microsoft < $300
```

### Setting up Telegram Notifications

1. **Create a Telegram Bot**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Copy the bot token

2. **Get your Chat ID**
   - Start a chat with your bot
   - Send any message
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Update Configuration**
   ```yaml
   telegram:
     enabled: true
     bot_token: "your_actual_bot_token"
     chat_id: "your_actual_chat_id"
   ```

### Price Monitoring Setup

Configure price thresholds in [`config/config.yml`](config/config.yml):

```yaml
price_monitor:
  enabled: true
  thresholds:
    # Format: "TICKER:OPERATOR:VALUE"
    - "AAPL:gt:150"     # Apple > $150
    - "MSFT:lt:300"     # Microsoft < $300
    - "GOOGL:gte:2500"  # Google >= $2500
    - "TSLA:lte:200"    # Tesla <= $200
    - "NVDA:eq:500"     # NVIDIA = $500
```

**Supported Operators:**
- `gt`: Greater than (>)
- `lt`: Less than (<)
- `gte`: Greater than or equal (>=)
- `lte`: Less than or equal (<=)
- `eq`: Equal (=)

## 📚 Available Commands

| Command    | Aliases               | Description                    |
| ---------- | --------------------- | ------------------------------ |
| `analysis` | `a`, `analyze`        | Comprehensive company analysis |
| `magic`    | `mf`, `magic_formula` | Magic Formula stock screening  |
| `income`   | `inc`                 | Income statement analysis      |
| `balance`  | `bal`                 | Balance sheet analysis         |
| `cashflow` | `cf`                  | Cash flow analysis             |
| `dividend` | `div`                 | Dividend analysis              |
| `price`    | `p`                   | Price and technical analysis   |
| `info`     | `i`                   | Basic company information      |
| `monitor`  | `m`, `watch`, `alert` | Price monitoring               |
| `cache`    | `c`                   | Cache management               |

### Getting Help

```bash
# General help
python main.py --help

# Command-specific help
python main.py analysis --help
python main.py magic --help
python main.py monitor --help
```

## 📊 Output Examples

### Company Analysis Output
```
=== APPLE INC (AAPL) ===

📊 MARKET DATA
• Current Price: $175.43 (+2.34%)
• Market Cap: $2.75T
• 52-Week Range: $124.17 - $198.23

📈 TECHNICAL ANALYSIS
• RSI (14): 67.2 (Neutral)
• MACD: Bullish Signal
• Overall Score: 7.2/10 (BUY)

💰 FINANCIAL HEALTH
• Revenue Growth (3Y): 8.2%
• Profit Margin: 25.3%
• ROE: 147.4%
• Debt-to-Equity: 1.73
```

### Magic Formula Screening Output
```
=== MAGIC FORMULA SCREENING RESULTS ===

📊 RANKED STOCKS (Quarterly Data)
┌──────┬────────┬─────────────────────┬────────┬────────┬─────────┬──────────┬───────┐
│ Rank │ Ticker │ Company             │ EY     │ ROC    │ EY Rank │ ROC Rank │ Score │
├──────┼────────┼─────────────────────┼────────┼────────┼─────────┼──────────┼───────┤
│ 1    │ AAPL   │ Apple Inc.          │ 3.2%   │ 147.4% │ 3       │ 1        │ 4     │
│ 2    │ MSFT   │ Microsoft Corp.     │ 3.8%   │ 45.2%  │ 1       │ 2        │ 3     │
│ 3    │ GOOGL  │ Alphabet Inc.       │ 3.5%   │ 29.1%  │ 2       │ 3        │ 5     │
└──────┴────────┴─────────────────────┴────────┴────────┴─────────┴──────────┴───────┘
```

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
├── src/ticker_analysis/
│   ├── core/                    # Business logic
│   │   ├── analysis/            # Analysis engines
│   │   ├── data/                # Data fetching
│   │   └── screening/           # Screening algorithms
│   ├── infrastructure/          # Supporting services
│   │   ├── cache/               # Caching system
│   │   ├── notifications/       # Notification providers
│   │   └── monitoring/          # Price monitoring
│   ├── interfaces/              # User interfaces
│   │   ├── cli/                 # Command-line interface
│   │   └── console/             # Output formatting
│   └── config/                  # Configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Use type hints where appropriate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Joel Greenblatt** - Magic Formula methodology from "The Little Book That Beats the Market"
- **Yahoo Finance** - Financial data source via yfinance library
- **Rich Library** - Beautiful console output formatting

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Comprehensive docs available in the [`docs/`](docs/) directory
- **Examples**: Usage examples in the [`examples/`](examples/) directory

---

**Happy Analyzing! 📈**