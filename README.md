# Market Research Toolkit

A comprehensive Python-based financial analysis tool for stock market research and ticker analysis. This toolkit provides command-line interfaces for fetching, analyzing, and monitoring financial data from various sources.

## 🚀 Features

- **Comprehensive Financial Analysis**: Complete company analysis including financial statements, ratios, and key metrics
- **Magic Formula Screening**: Implementation of Joel Greenblatt's Magic Formula for stock screening
- **Financial Statements**: Access to income statements, balance sheets, and cash flow statements
- **Price Monitoring**: Real-time price alerts and threshold monitoring
- **Dividend Analysis**: Historical dividend data and analysis
- **Caching System**: Intelligent caching to reduce API calls and improve performance
- **Telegram Notifications**: Real-time alerts via Telegram bot integration
- **Rich Console Output**: Beautiful, formatted output with colors and tables

## 📋 Requirements

- Python 3.8+
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/marouane-dev75/market-research-toolkit.git
   cd market-research-toolkit
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### Basic Usage

Run the main script to see available commands:
```bash
python main.py --help
```

### Example Commands

1. **Get comprehensive company analysis**:
   ```bash
   python main.py analysis AAPL
   ```

2. **View financial statements**:
   ```bash
   python main.py income MSFT
   python main.py balance GOOGL yearly
   python main.py cashflow TSLA
   ```

3. **Magic Formula screening**:
   ```bash
   python main.py magic AAPL,GOOGL,MSFT,NVDA,TSLA
   ```

4. **Price monitoring**:
   ```bash
   python main.py price AAPL
   python main.py monitor --status
   ```

5. **Company information**:
   ```bash
   python main.py info NVDA
   ```

## 📊 Available Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `analysis` | `a`, `analyze` | Comprehensive company analysis |
| `magic` | `mf`, `magic_formula` | Magic Formula stock screening |
| `income` | `inc` | Income statement data |
| `balance` | `bal` | Balance sheet data |
| `cashflow` | `cf` | Cash flow statement data |
| `dividend` | `div` | Dividend history and analysis |
| `price` | `p` | Historical price data |
| `info` | `i` | Company information |
| `cache` | `c` | Cache management |
| `monitor` | `m`, `watch`, `alert` | Price monitoring |

### Command Examples

```bash
# Comprehensive analysis
python main.py analysis AAPL
python main.py a GOOGL  # Using alias

# Financial statements with different frequencies
python main.py income MSFT yearly
python main.py balance AAPL quarterly
python main.py cashflow TSLA

# Magic Formula screening
python main.py magic AAPL,GOOGL,MSFT
python main.py mf AAPL,GOOGL yearly

# Price and dividend data
python main.py price NVDA
python main.py dividend AAPL

# Cache management
python main.py cache status
python main.py cache clear AAPL
python main.py cache clear  # Clear all

# Monitoring
python main.py monitor --status
python main.py monitor --test
```

## ⚙️ Configuration

The application uses a YAML configuration file located at [`src/ticker_analysis/config/config.yml`](src/ticker_analysis/config/config.yml). Key configuration options include:

### Application Settings
```yaml
application:
  name: "Ticker Analysis Tool"
  version: "1.0.0"
  default_output_format: "console"
  debug_mode: false
```

### Cache Configuration
```yaml
data:
  cache_directory: "cache_data"
  cache:
    company_info:
      ttl_hours: 168  # 1 week
      enabled: true
    price_data:
      ttl_hours: 24   # 1 day
      enabled: true
```

### Telegram Notifications
```yaml
telegram:
  enabled: true
  bot_token: "YOUR_BOT_TOKEN_HERE"
  chat_id: "YOUR_CHAT_ID_HERE"
  timeout_seconds: 30
  retry_attempts: 3
```

### Price Monitoring
```yaml
price_monitor:
  enabled: true
  thresholds:
    - "AAPL:gt:150"    # Alert when Apple > $150
    - "MSFT:lt:300"    # Alert when Microsoft < $300
    - "GOOGL:gte:2500" # Alert when Google >= $2500
```

## 🔧 Setting Up Telegram Notifications

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Copy the bot token

2. **Get Your Chat ID**:
   - Start a chat with your bot
   - Send any message
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Update Configuration**:
   - Edit [`src/ticker_analysis/config/config.yml`](src/ticker_analysis/config/config.yml)
   - Replace `YOUR_BOT_TOKEN_HERE` and `YOUR_CHAT_ID_HERE`

## 🧪 Testing

Run the comprehensive integration test:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run integration tests
python tests/test_integration_global.py
```

The test suite validates all CLI commands with test tickers: AAPL, GOOGL, MSFT, NVDA, TSLA.

## 📁 Project Structure

```
market-research-toolkit/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── src/ticker_analysis/            # Main package
│   ├── config/                     # Configuration management
│   ├── core/                       # Core business logic
│   │   ├── analysis/              # Financial analysis modules
│   │   ├── data/                  # Data fetchers and models
│   │   └── screening/             # Stock screening algorithms
│   ├── infrastructure/            # Infrastructure services
│   │   ├── cache/                 # Caching system
│   │   ├── monitoring/            # Price monitoring
│   │   └── notifications/         # Notification providers
│   └── interfaces/                # User interfaces
│       ├── cli/                   # Command-line interface
│       └── console/               # Console formatting
└── tests/                         # Test suites
```

## 🔍 Core Features

### Financial Analysis
- **Company Analysis**: Comprehensive financial metrics and ratios
- **Financial Statements**: Income statements, balance sheets, cash flows
- **Technical Analysis**: Price trends and technical indicators
- **Dividend Analysis**: Dividend history, yield calculations, and trends

### Stock Screening
- **Magic Formula**: Joel Greenblatt's proven stock screening methodology
- **Custom Metrics**: Earnings yield and return on invested capital
- **Ranking System**: Automated ranking based on Magic Formula criteria

### Data Management
- **Intelligent Caching**: Configurable TTL for different data types
- **Multiple Data Sources**: Integration with Yahoo Finance and other providers
- **Data Validation**: Robust error handling and data validation

### Monitoring & Alerts
- **Price Thresholds**: Configurable price alerts with multiple operators
- **Real-time Notifications**: Telegram integration for instant alerts
- **Monitoring Dashboard**: Status monitoring and configuration testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please:
1. Check the documentation and examples above
2. Run commands with `--help` flag for detailed usage
3. Enable debug mode with `--debug` flag for troubleshooting
4. Open an issue on GitHub for bugs or feature requests

## 🔗 Links

- **Repository**: [https://github.com/marouane-dev75/market-research-toolkit](https://github.com/marouane-dev75/market-research-toolkit)
- **Issues**: [https://github.com/marouane-dev75/market-research-toolkit/issues](https://github.com/marouane-dev75/market-research-toolkit/issues)
