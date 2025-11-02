"""
Console styling constants and color definitions.
"""

class Colors:
    """ANSI color codes for console output."""
    
    # Standard colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class LogLevelColors:
    """Color mapping for different log levels."""
    
    INFO = Colors.BLUE
    WARNING = Colors.YELLOW
    ERROR = Colors.RED
    SUCCESS = Colors.GREEN
    DEBUG = Colors.CYAN
    CRITICAL = Colors.RED + Colors.BOLD


class Symbols:
    """Unicode symbols for enhanced console output."""
    
    INFO = "ℹ"
    WARNING = "⚠"
    ERROR = "✗"
    SUCCESS = "✓"
    DEBUG = "🐛"
    CRITICAL = "💥"
    ARROW = "→"
    BULLET = "•"