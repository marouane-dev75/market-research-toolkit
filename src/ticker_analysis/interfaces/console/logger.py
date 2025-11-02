"""
Enhanced logging functionality with colorful console output.
"""

import logging
import sys
from typing import Optional
from .formatter import ConsoleFormatter
from .financial_formatter import FinancialFormatter
from .styles import Colors
from ...config import get_config_manager


class ColoredConsoleHandler(logging.StreamHandler):
    """Custom logging handler with colored output."""
    
    def __init__(self, stream=None, use_colors: bool = True):
        """
        Initialize the colored console handler.
        
        Args:
            stream: Output stream (defaults to sys.stdout)
            use_colors: Whether to use colors in output
        """
        super().__init__(stream or sys.stdout)
        self.formatter_helper = ConsoleFormatter(use_colors)
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors.
        
        Args:
            record: Log record to format
            
        Returns:
            Formatted log message
        """
        # Map logging levels to our custom levels
        level_mapping = {
            'DEBUG': 'DEBUG',
            'INFO': 'INFO',
            'WARNING': 'WARNING',
            'ERROR': 'ERROR',
            'CRITICAL': 'CRITICAL'
        }
        
        level_name = level_mapping.get(record.levelname, 'INFO')
        return self.formatter_helper.format_message(record.getMessage(), level_name)


class TickerLogger:
    """Enhanced logger for the ticker analysis application."""
    
    def __init__(self, name: str = "ticker_analysis", use_colors: Optional[bool] = None):
        """
        Initialize the ticker logger.
        
        Args:
            name: Logger name
            use_colors: Whether to use colors in console output (None = use config)
        """
        self.logger = logging.getLogger(name)
        
        # Get configuration
        try:
            config_manager = get_config_manager()
            config = config_manager.get_config()
            
            # Set log level from config
            level_mapping = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            self.logger.setLevel(level_mapping.get(config.logging.level, logging.INFO))
            
            # Use config for colors if not explicitly provided
            if config.logging.use_colors is not None:
                use_colors = config.logging.use_colors
                
        except Exception:
            # Fallback to defaults if config loading fails
            self.logger.setLevel(logging.INFO)
            if use_colors is None:
                use_colors = True
        
        self.formatter_helper = ConsoleFormatter(use_colors)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Add colored console handler
        console_handler = ColoredConsoleHandler(use_colors=use_colors)
        self.logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)
    
    def success(self, message: str) -> None:
        """Log a success message (custom level)."""
        # Create a custom success message using INFO level but SUCCESS formatting
        formatted_msg = self.formatter_helper.format_message(message, "SUCCESS")
        print(formatted_msg)
    
    def set_level(self, level: str) -> None:
        """
        Set the logging level.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        level_mapping = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_mapping:
            self.logger.setLevel(level_mapping[level.upper()])
    
    def print_header(self, title: str, width: int = 50) -> None:
        """
        Print a formatted header.
        
        Args:
            title: Header title
            width: Header width
        """
        header = self.formatter_helper.format_header(title, width)
        print(header)
    
    def print_section(self, title: str) -> None:
        """
        Print a formatted section header.
        
        Args:
            title: Section title
        """
        section = self.formatter_helper.format_section(title)
        print(section)
    
    def print_bullet(self, text: str, indent: int = 2) -> None:
        """
        Print a formatted bullet point.
        
        Args:
            text: Bullet point text
            indent: Indentation level
        """
        bullet = self.formatter_helper.format_bullet_point(text, indent)
        print(bullet)
    
    def print_command(self, command: str, description: str = "") -> None:
        """
        Print a formatted command with optional description.
        
        Args:
            command: Command string
            description: Optional command description
        """
        formatted_cmd = self.formatter_helper.format_command(command)
        if description:
            print(f"  {formatted_cmd:<20} {description}")
        else:
            print(f"  {formatted_cmd}")
    
    def print_example(self, example: str, description: str = "") -> None:
        """
        Print a formatted example with optional description.
        
        Args:
            example: Example string
            description: Optional example description
        """
        formatted_example = self.formatter_helper.format_example(example)
        if description:
            print(f"  {formatted_example}")
            if description:
                print(f"    {description}")
        else:
            print(f"  {formatted_example}")


# Global logger instance
_global_logger: Optional[TickerLogger] = None


def get_logger(name: str = "ticker_analysis", use_colors: bool = True) -> TickerLogger:
    """
    Get or create a global logger instance.
    
    Args:
        name: Logger name
        use_colors: Whether to use colors
        
    Returns:
        TickerLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = TickerLogger(name, use_colors)
    return _global_logger


def set_log_level(level: str) -> None:
    """
    Set the global log level.
    
    Args:
        level: Logging level
    """
    logger = get_logger()
    logger.set_level(level)