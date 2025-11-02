# Installation Guide

This guide provides detailed installation instructions for the Ticker Analysis Tool.

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Internet Connection**: Required for fetching financial data
- **Memory**: Minimum 512MB RAM (1GB+ recommended for large datasets)
- **Storage**: ~100MB for application and cache

## 🚀 Quick Installation

### Option 1: Standard Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/marouane-dev75/market-research-toolkit
   cd ticker_analysis
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python main.py --help
   ```

### Option 2: Virtual Environment (Recommended)

1. **Clone and navigate**
   ```bash
   git clone https://github.com/marouane-dev75/market-research-toolkit
   cd ticker_analysis
   ```

2. **Create virtual environment**
   ```bash
   # Using venv (Python 3.8+)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test installation**
   ```bash
   python main.py analysis AAPL
   ```

## 🔧 Development Installation

For contributors and developers:

1. **Clone repository**
   ```bash
   git clone https://github.com/marouane-dev75/market-research-toolkit
   cd ticker_analysis
   ```

2. **Create development environment**
   ```bash
   python -m venv venv-dev
   source venv-dev/bin/activate  # or venv-dev\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   # Core dependencies
   pip install -r requirements.txt
   
   # Development dependencies
   pip install -r requirements-dev.txt
   ```

4. **Install in development mode**
   ```bash
   pip install -e .
   ```

## 📦 Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `colorama` | >=0.4.6 | Cross-platform colored terminal output |
| `click` | >=8.1.0 | Command-line interface framework |
| `rich` | >=13.0.0 | Rich text and beautiful formatting |
| `yfinance` | >=0.2.40 | Yahoo Finance data fetching |
| `pandas` | >=2.0.0 | Data manipulation and analysis |
| `numpy` | >=1.24.0 | Numerical computing |
| `PyYAML` | >=6.0.0 | YAML configuration file parsing |
| `requests` | >=2.31.0 | HTTP library for API calls |


## 🔧 Configuration Setup

### Basic Configuration

1. **Copy example configuration**
   ```bash
   cp config/config.yml.example config/config.yml
   ```

2. **Edit configuration**
   ```bash
   # Edit with your preferred editor
   nano config/config.yml
   ```

### Telegram Notifications Setup

1. **Create Telegram Bot**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Get Chat ID**
   - Start chat with your bot
   - Send any message
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Update configuration**
   ```yaml
   telegram:
     enabled: true
     bot_token: "your_bot_token_here"
     chat_id: "your_chat_id_here"
   ```

## ✅ Verification

### Test Basic Functionality

```bash
# Test company analysis
python main.py analysis AAPL

# Test Magic Formula screening
python main.py magic AAPL,MSFT,GOOGL

# Test price monitoring configuration
python main.py monitor --test

# Test cache functionality
python main.py cache status
```

### Expected Output

If installation is successful, you should see:
- Colorful, formatted output
- Financial data retrieved from Yahoo Finance
- No import errors or missing dependencies

## 🚨 Troubleshooting

### Common Issues

#### 1. Python Version Issues
```bash
# Check Python version
python --version

# If using Python 3.8+, try:
python3 main.py --help
```

#### 2. Permission Errors
```bash
# On macOS/Linux, try:
sudo pip install -r requirements.txt

# Or use user installation:
pip install --user -r requirements.txt
```

#### 3. Network/Firewall Issues
```bash
# Test internet connectivity
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['symbol'])"
```

#### 4. Missing Dependencies
```bash
# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### 5. Cache Directory Issues
```bash
# Create cache directory manually
mkdir -p data
chmod 755 data
```

### Platform-Specific Issues

#### Windows
- Use `python` instead of `python3`
- Use `Scripts\activate` instead of `bin/activate`
- Install Microsoft Visual C++ if compilation errors occur

#### macOS
- Install Xcode command line tools: `xcode-select --install`
- Use Homebrew Python if system Python causes issues

#### Linux
- Install development packages: `sudo apt-get install python3-dev`
- For CentOS/RHEL: `sudo yum install python3-devel`

## 🔄 Updating

### Update Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Update Dependencies Only
```bash
# Update all packages
pip install -r requirements.txt --upgrade

# Update specific package
pip install yfinance --upgrade
```

## 🗑️ Uninstallation

### Remove Application
```bash
# Remove virtual environment
rm -rf venv/

# Remove application directory
cd ..
rm -rf ticker_analysis/
```

### Remove Dependencies
```bash
# If installed globally
pip uninstall -r requirements.txt -y
```

## 📞 Support

If you encounter issues during installation:

1. **Check Requirements**: Ensure Python 3.8+ is installed
2. **Review Logs**: Look for specific error messages
3. **Search Issues**: Check GitHub issues for similar problems
4. **Create Issue**: Report new bugs with system information

### System Information Template
```bash
# Gather system info for bug reports
python --version
pip --version
uname -a  # Linux/macOS
systeminfo  # Windows
```

---

**Installation complete! Ready to analyze! 📈**