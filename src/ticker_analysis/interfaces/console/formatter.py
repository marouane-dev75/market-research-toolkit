"""
Console text formatting utilities with color support.
"""

import sys
import os
import re
from datetime import datetime
from typing import Optional
from .styles import Colors, LogLevelColors, Symbols


class ConsoleFormatter:
    """Handles console text formatting with colors and styles."""
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize the console formatter.
        
        Args:
            use_colors: Whether to use colors in output (auto-detected if None)
        """
        self.use_colors = use_colors and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Check if the terminal supports color output."""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            sys.platform != 'win32' or 'ANSICON' in os.environ
        )
    
    def colorize(self, text: str, color: str) -> str:
        """
        Apply color to text if colors are enabled.
        
        Args:
            text: Text to colorize
            color: ANSI color code
            
        Returns:
            Colored text or plain text if colors disabled
        """
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"
    
    def format_log_level(self, level: str) -> str:
        """
        Format a log level with appropriate color and symbol.
        
        Args:
            level: Log level name (INFO, WARNING, ERROR, etc.)
            
        Returns:
            Formatted log level string
        """
        level_upper = level.upper()
        color = getattr(LogLevelColors, level_upper, Colors.WHITE)
        symbol = getattr(Symbols, level_upper, "•")
        
        if self.use_colors:
            return f"{color}{symbol} {level_upper}{Colors.RESET}"
        return f"{symbol} {level_upper}"
    
    def format_timestamp(self, timestamp: Optional[datetime] = None) -> str:
        """
        Format a timestamp for log output.
        
        Args:
            timestamp: Datetime object (uses current time if None)
            
        Returns:
            Formatted timestamp string
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        time_str = timestamp.strftime("%H:%M:%S")
        return self.colorize(time_str, Colors.DIM + Colors.WHITE)
    
    def format_message(self, message: str, level: str = "INFO") -> str:
        """
        Format a complete log message with level, timestamp, and content.
        
        Args:
            message: The message content
            level: Log level
            
        Returns:
            Fully formatted message
        """
        timestamp = self.format_timestamp()
        level_formatted = self.format_log_level(level)
        
        return f"[{timestamp}] {level_formatted} {message}"
    
    def format_header(self, title: str, width: int = 50) -> str:
        """
        Format a header with decorative borders.
        
        Args:
            title: Header title
            width: Total width of the header
            
        Returns:
            Formatted header string
        """
        border = "=" * width
        title_line = f" {title} ".center(width)
        
        if self.use_colors:
            border = self.colorize(border, Colors.BLUE + Colors.BOLD)
            title_line = self.colorize(title_line, Colors.BLUE + Colors.BOLD)
        
        return f"\n{border}\n{title_line}\n{border}"
    
    def format_section(self, title: str) -> str:
        """
        Format a section header.
        
        Args:
            title: Section title
            
        Returns:
            Formatted section header
        """
        return self.colorize(f"\n{title}:", Colors.CYAN + Colors.BOLD)
    
    def format_bullet_point(self, text: str, indent: int = 2) -> str:
        """
        Format a bullet point with proper indentation.
        
        Args:
            text: Bullet point text
            indent: Number of spaces to indent
            
        Returns:
            Formatted bullet point
        """
        spaces = " " * indent
        bullet = self.colorize(Symbols.BULLET, Colors.BLUE)
        return f"{spaces}{bullet} {text}"
    
    def format_command(self, command: str) -> str:
        """
        Format a command for display.
        
        Args:
            command: Command string
            
        Returns:
            Formatted command
        """
        return self.colorize(command, Colors.GREEN + Colors.BOLD)
    
    def format_example(self, example: str) -> str:
        """
        Format an example command or usage.
        
        Args:
            example: Example string
            
        Returns:
            Formatted example
        """
        return self.colorize(example, Colors.YELLOW)
    
    def strip_ansi_codes(self, text: str) -> str:
        """
        Remove ANSI escape sequences from text.
        
        Args:
            text: Text that may contain ANSI codes
            
        Returns:
            Text with ANSI codes removed
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def get_display_width(self, text: str) -> int:
        """
        Get the display width of text (excluding ANSI codes).
        
        Args:
            text: Text that may contain ANSI codes
            
        Returns:
            Visual width of the text
        """
        return len(self.strip_ansi_codes(text))
    
    def pad_with_ansi(self, text: str, width: int, align: str = 'left') -> str:
        """
        Pad text to a specific width while preserving ANSI color codes.
        
        Args:
            text: Text that may contain ANSI codes
            width: Target display width
            align: Alignment ('left', 'right', 'center')
            
        Returns:
            Padded text with ANSI codes preserved
        """
        display_width = self.get_display_width(text)
        
        if display_width >= width:
            return text
        
        padding_needed = width - display_width
        
        if align == 'left':
            return text + ' ' * padding_needed
        elif align == 'right':
            return ' ' * padding_needed + text
        elif align == 'center':
            left_padding = padding_needed // 2
            right_padding = padding_needed - left_padding
            return ' ' * left_padding + text + ' ' * right_padding
        else:
            raise ValueError(f"Invalid alignment: {align}. Use 'left', 'right', or 'center'")
    
    def format_table_row(self, columns: list, widths: list, alignments: list = None) -> str:
        """
        Format a table row with proper ANSI-aware alignment.
        
        Args:
            columns: List of column values (may contain ANSI codes)
            widths: List of column widths
            alignments: List of alignments for each column ('left', 'right', 'center')
            
        Returns:
            Formatted table row
        """
        if alignments is None:
            alignments = ['left'] * len(columns)
        
        if len(columns) != len(widths) or len(columns) != len(alignments):
            raise ValueError("columns, widths, and alignments must have the same length")
        
        formatted_columns = []
        for col, width, align in zip(columns, widths, alignments):
            formatted_columns.append(self.pad_with_ansi(str(col), width, align))
        
        return ' '.join(formatted_columns)