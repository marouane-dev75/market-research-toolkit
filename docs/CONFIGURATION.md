# Configuration Guide

This guide covers all configuration options available in the Ticker Analysis Tool.

## 📁 Configuration File Location

The main configuration file is located at:
```
config/config.yml
```

## 🔧 Configuration Structure

### Application Settings

```yaml
application:
  # Application name displayed in headers
  name: "Ticker Analysis Tool"
  
  # Version information
  version: "1.0.0"
  
  # Default output format for analysis results
  default_output_format: "console"
  
  # Enable debug mode for detailed logging
  debug_mode: false
```

### Logging Configuration

```yaml
logging:
  # Log verbosity level
  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: INFO
```

**Log Levels Explained**:
- `DEBUG`: Detailed information for debugging
- `INFO`: General information about program execution
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures
- `CRITICAL`: Critical errors that may stop execution

### Data Storage and Caching

```yaml
data:
  # Base directory for cached data storage
  cache_directory: "data"
  
  # Cache settings for different data types
  cache:
    # Company information cache (basic info, ratios, etc.)
    company_info:
      ttl_hours: 168    # Time to live: 1 week
      enabled: true
    
    # Financial statements cache
    income_statements:
      ttl_hours: 168    # 1 week
      enabled: true
    
    balance_sheets:
      ttl_hours: 168    # 1 week  
      enabled: true
    
    cash_flows:
      ttl_hours: 168    # 1 week
      enabled: true
    
    # Dividend data cache
    dividends:
      ttl_hours: 168    # 1 week
      enabled: true
    
    # Price data cache (more volatile, shorter TTL)
    price_data:
      ttl_hours: 24     # 1 day
      enabled: true
```

**Cache TTL Guidelines**:
- **Financial Statements**: 168 hours (1 week) - quarterly/yearly data changes infrequently
- **Company Info**: 168 hours (1 week) - basic company data is relatively stable
- **Price Data**: 24 hours (1 day) - prices change frequently during market hours
- **Dividends**: 168 hours (1 week) - dividend announcements are infrequent

### Telegram Notifications

```yaml
telegram:
  # Enable/disable telegram notifications
  enabled: true
  
  # Telegram Bot Token from @BotFather
  bot_token: "YOUR_BOT_TOKEN_HERE"
  
  # Chat ID where messages will be sent
  chat_id: "YOUR_CHAT_ID_HERE"
  
  # Connection settings
  timeout_seconds: 30
  retry_attempts: 3
```

#### Setting Up Telegram Notifications

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the bot token provided

2. **Get Your Chat ID**:
   - Start a chat with your bot
   - Send any message to the bot
   - Open this URL in your browser (replace `YOUR_BOT_TOKEN`):
     ```
     https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
     ```
   - Look for `"chat":{"id": YOUR_CHAT_ID}` in the response
   - Copy the chat ID (usually a number)

3. **Update Configuration**:
   ```yaml
   telegram:
     enabled: true
     bot_token: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
     chat_id: "123456789"
   ```

### Price Monitoring

```yaml
price_monitor:
  # Enable/disable price monitoring
  enabled: true
  
  # List of price thresholds to monitor
  # Format: "TICKER:OPERATOR:VALUE"
  thresholds:
    # Example thresholds
    - "AAPL:gt:150"      # Apple > $150
    - "MSFT:lt:300"      # Microsoft < $300
    - "GOOGL:gte:2500"   # Google >= $2500
    - "TSLA:lte:200"     # Tesla <= $200
    - "NVDA:eq:500"      # NVIDIA = $500
  
  # Notification settings
  notifications:
    enabled: true
    # Message template for notifications
    message_template: "✅ Price Alert: {triggered_count} threshold(s) triggered\n\n{details}"
```

#### Threshold Format

**Syntax**: `"TICKER:OPERATOR:VALUE"`

**Supported Operators**:
- `gt`: Greater than (>)
- `lt`: Less than (<)
- `gte`: Greater than or equal (>=)
- `lte`: Less than or equal (<=)
- `eq`: Equal (=)

**Examples**:
```yaml
thresholds:
  # Technology stocks
  - "AAPL:gt:150"        # Alert when Apple exceeds $150
  - "MSFT:lt:300"        # Alert when Microsoft drops below $300
  - "GOOGL:gte:2500"     # Alert when Google reaches or exceeds $2500
  
  # Energy stocks
  - "XOM:lt:75"          # Alert when Exxon drops below $75
  - "CVX:gt:120"         # Alert when Chevron exceeds $120
  
  # REITs
  - "VNQ:lte:90"         # Alert when Vanguard REIT ETF drops to $90 or below
```

## 🔒 Security Considerations

### Sensitive Information

**Never commit sensitive data to version control**:
- Telegram bot tokens
- Chat IDs
- API keys (if added in future)

### Best Practices

1. **Use Environment Variables** (optional enhancement):
   ```yaml
   telegram:
     bot_token: "${TELEGRAM_BOT_TOKEN}"
     chat_id: "${TELEGRAM_CHAT_ID}"
   ```

2. **File Permissions**:
   ```bash
   chmod 600 config/config.yml  # Read/write for owner only
   ```

3. **Backup Configuration**:
   ```bash
   cp config/config.yml config/config.yml.backup
   ```

## 🎛️ Advanced Configuration

### Custom Cache Directory

```yaml
data:
  cache_directory: "/custom/path/to/cache"
```

**Requirements**:
- Directory must be writable
- Sufficient disk space for cache files
- Consider using absolute paths for production

### Performance Tuning

**For High-Frequency Usage**:
```yaml
data:
  cache:
    price_data:
      ttl_hours: 1      # Cache for 1 hour only
    company_info:
      ttl_hours: 24     # Cache for 1 day
```

**For Low-Frequency Usage**:
```yaml
data:
  cache:
    price_data:
      ttl_hours: 168    # Cache for 1 week
    company_info:
      ttl_hours: 720    # Cache for 1 month
```

### Debugging Configuration

**Enable Debug Mode**:
```yaml
application:
  debug_mode: true

logging:
  level: DEBUG
```

**This enables**:
- Detailed logging output
- Cache hit/miss information
- API request details
- Performance timing information

## 📝 Configuration Templates

### Minimal Configuration

```yaml
application:
  name: "Ticker Analysis Tool"
  version: "1.0.0"

logging:
  level: INFO

data:
  cache_directory: "data"

telegram:
  enabled: false

price_monitor:
  enabled: false
```

### Production Configuration

```yaml
application:
  name: "Ticker Analysis Tool"
  version: "1.0.0"
  debug_mode: false

logging:
  level: WARNING

data:
  cache_directory: "/var/cache/ticker_analysis"
  cache:
    company_info:
      ttl_hours: 168
      enabled: true
    price_data:
      ttl_hours: 24
      enabled: true

telegram:
  enabled: true
  bot_token: "your_production_bot_token"
  chat_id: "your_production_chat_id"
  timeout_seconds: 30
  retry_attempts: 3

price_monitor:
  enabled: true
  thresholds:
    - "AAPL:gt:150"
    - "MSFT:lt:300"
  notifications:
    enabled: true
```

### Development Configuration

```yaml
application:
  name: "Ticker Analysis Tool (Dev)"
  version: "1.0.0-dev"
  debug_mode: true

logging:
  level: DEBUG

data:
  cache_directory: "data_dev"
  cache:
    company_info:
      ttl_hours: 1      # Short cache for testing
      enabled: true
    price_data:
      ttl_hours: 1      # Short cache for testing
      enabled: true

telegram:
  enabled: true
  bot_token: "your_test_bot_token"
  chat_id: "your_test_chat_id"

price_monitor:
  enabled: true
  thresholds:
    - "AAPL:gt:1"       # Low threshold for testing
  notifications:
    enabled: true
```

## 🔧 Configuration Validation

### Manual Validation

**Test Configuration Syntax**:
```bash
python -c "import yaml; yaml.safe_load(open('config/config.yml'))"
```

**Test Telegram Configuration**:
```bash
python main.py monitor --test
```

**Test Cache Configuration**:
```bash
python main.py cache status
```

### Common Configuration Errors

1. **Invalid YAML Syntax**:
   ```yaml
   # Wrong - missing quotes
   bot_token: 123:ABC-def
   
   # Correct
   bot_token: "123:ABC-def"
   ```

2. **Invalid Threshold Format**:
   ```yaml
   # Wrong
   - "AAPL > 150"
   
   # Correct  
   - "AAPL:gt:150"
   ```

3. **Missing Required Fields**:
   ```yaml
   # Wrong - missing chat_id
   telegram:
     enabled: true
     bot_token: "123:ABC"
   
   # Correct
   telegram:
     enabled: true
     bot_token: "123:ABC"
     chat_id: "456789"
   ```

## 🔄 Configuration Updates

### Updating Configuration

1. **Backup Current Config**:
   ```bash
   cp config/config.yml config/config.yml.backup
   ```

2. **Edit Configuration**:
   ```bash
   nano config/config.yml
   ```

3. **Validate Changes**:
   ```bash
   python main.py monitor --test
   ```

4. **Test Functionality**:
   ```bash
   python main.py analysis AAPL
   ```

### Configuration Migration

When updating the application, check for new configuration options:

1. Compare with example configuration
2. Add new sections as needed
3. Update version numbers
4. Test all functionality

---

**Configuration complete! Ready for customized analysis! ⚙️**

For more information, see:
- [Installation Guide](INSTALLATION.md)
- [Usage Guide](USAGE.md)