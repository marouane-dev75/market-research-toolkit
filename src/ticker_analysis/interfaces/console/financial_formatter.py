"""
Financial data formatting utilities for console output.

This module provides specialized formatting functions for financial data
including currency, percentages, shares, and other financial metrics.
"""

from typing import Optional, Union
from decimal import Decimal
from .styles import Colors


class FinancialFormatter:
    """Handles formatting of financial data for console display."""
    
    def __init__(self, use_colors: bool = True, currency_symbol: str = "$"):
        """
        Initialize the financial formatter.
        
        Args:
            use_colors: Whether to use colors in output
            currency_symbol: Currency symbol to use (default: $)
        """
        self.use_colors = use_colors
        self.currency_symbol = currency_symbol
    
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
    
    def format_currency(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2,
        show_sign: bool = False,
        compact: bool = False
    ) -> str:
        """
        Format a currency value with proper formatting.
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places (default: 2)
            show_sign: Whether to show + for positive values
            compact: Whether to use compact notation (K, M, B, T)
            
        Returns:
            Formatted currency string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        # Handle compact notation
        if compact:
            return self._format_compact_currency(num_value, precision, show_sign)
        
        # Standard formatting
        sign = "+" if show_sign and num_value > 0 else ""
        formatted = f"{sign}{self.currency_symbol}{abs(num_value):,.{precision}f}"
        
        # Apply color based on value
        if num_value < 0:
            formatted = f"-{formatted}"
            return self.colorize(formatted, Colors.RED)
        elif num_value > 0:
            return self.colorize(formatted, Colors.GREEN)
        else:
            return self.colorize(formatted, Colors.WHITE)
    
    def _format_compact_currency(
        self,
        value: float,
        precision: int = 2,
        show_sign: bool = False
    ) -> str:
        """Format currency with compact notation (K, M, B, T)."""
        abs_value = abs(value)
        sign = "+" if show_sign and value > 0 else ""
        negative_sign = "-" if value < 0 else ""
        
        if abs_value >= 1_000_000_000_000:  # Trillions
            number_part = f"{sign}{negative_sign}{self.currency_symbol}{abs_value/1_000_000_000_000:.{precision}f}"
            suffix = "T"
        elif abs_value >= 1_000_000_000:  # Billions
            number_part = f"{sign}{negative_sign}{self.currency_symbol}{abs_value/1_000_000_000:.{precision}f}"
            suffix = "B"
        elif abs_value >= 1_000_000:  # Millions
            number_part = f"{sign}{negative_sign}{self.currency_symbol}{abs_value/1_000_000:.{precision}f}"
            suffix = "M"
        elif abs_value >= 1_000:  # Thousands
            number_part = f"{sign}{negative_sign}{self.currency_symbol}{abs_value/1_000:.{precision}f}"
            suffix = "K"
        else:
            formatted = f"{sign}{negative_sign}{self.currency_symbol}{abs_value:.{precision}f}"
            # Apply color based on value for non-compact numbers
            if value < 0:
                return self.colorize(formatted, Colors.RED)
            elif value > 0:
                return self.colorize(formatted, Colors.GREEN)
            else:
                return self.colorize(formatted, Colors.WHITE)
        
        # For compact numbers, make the suffix bold
        if self.use_colors:
            bold_suffix = f"{Colors.BOLD}{suffix}{Colors.RESET}"
            formatted = f"{number_part}{bold_suffix}"
        else:
            formatted = f"{number_part}{suffix}"
        
        # Apply color based on value
        if value < 0:
            return self.colorize(formatted, Colors.RED)
        elif value > 0:
            return self.colorize(formatted, Colors.GREEN)
        else:
            return self.colorize(formatted, Colors.WHITE)
    
    def format_percentage(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2,
        show_sign: bool = False,
        multiply_by_100: bool = True
    ) -> str:
        """
        Format a percentage value.
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places (default: 2)
            show_sign: Whether to show + for positive values
            multiply_by_100: Whether to multiply by 100 (for decimal values like 0.15 -> 15%)
            
        Returns:
            Formatted percentage string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        # Convert to percentage if needed
        if multiply_by_100:
            num_value *= 100
        
        sign = "+" if show_sign and num_value > 0 else ""
        formatted = f"{sign}{num_value:.{precision}f}%"
        
        # Apply color based on value (typically green for positive, red for negative)
        if num_value < 0:
            return self.colorize(formatted, Colors.RED)
        elif num_value > 0:
            return self.colorize(formatted, Colors.GREEN)
        else:
            return self.colorize(formatted, Colors.WHITE)
    
    def format_shares(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        compact: bool = False,
        precision: int = 0
    ) -> str:
        """
        Format share count values.
        
        Args:
            value: Numeric value to format
            compact: Whether to use compact notation (K, M, B)
            precision: Number of decimal places for compact notation
            
        Returns:
            Formatted shares string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        if compact:
            return self._format_compact_number(num_value, precision)
        
        # Standard formatting with commas
        formatted = f"{num_value:,.0f}"
        return self.colorize(formatted, Colors.CYAN)
    
    def _format_compact_number(self, value: float, precision: int = 1) -> str:
        """Format numbers with compact notation (K, M, B, T)."""
        abs_value = abs(value)
        sign = "-" if value < 0 else ""
        
        if abs_value >= 1_000_000_000_000:  # Trillions
            number_part = f"{sign}{abs_value/1_000_000_000_000:.{precision}f}"
            suffix = "T"
        elif abs_value >= 1_000_000_000:  # Billions
            number_part = f"{sign}{abs_value/1_000_000_000:.{precision}f}"
            suffix = "B"
        elif abs_value >= 1_000_000:  # Millions
            number_part = f"{sign}{abs_value/1_000_000:.{precision}f}"
            suffix = "M"
        elif abs_value >= 1_000:  # Thousands
            number_part = f"{sign}{abs_value/1_000:.{precision}f}"
            suffix = "K"
        else:
            formatted = f"{sign}{abs_value:.0f}"
            return self.colorize(formatted, Colors.CYAN)
        
        # Make the suffix bold
        if self.use_colors:
            bold_suffix = f"{Colors.BOLD}{suffix}{Colors.RESET}"
            formatted = f"{number_part}{bold_suffix}"
        else:
            formatted = f"{number_part}{suffix}"
        
        return self.colorize(formatted, Colors.CYAN)
    
    def format_ratio(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2,
        show_sign: bool = False
    ) -> str:
        """
        Format ratio values (like P/E ratio, debt-to-equity, etc.).
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places (default: 2)
            show_sign: Whether to show + for positive values
            
        Returns:
            Formatted ratio string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        sign = "+" if show_sign and num_value > 0 else ""
        formatted = f"{sign}{num_value:.{precision}f}"
        
        # Apply neutral color for ratios
        return self.colorize(formatted, Colors.YELLOW)
    
    def format_growth_rate(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2,
        multiply_by_100: bool = True
    ) -> str:
        """
        Format growth rate values with appropriate coloring.
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places (default: 2)
            multiply_by_100: Whether to multiply by 100 (for decimal values)
            
        Returns:
            Formatted growth rate string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        # Convert to percentage if needed
        if multiply_by_100:
            num_value *= 100
        
        # Always show sign for growth rates
        sign = "+" if num_value > 0 else ""
        formatted = f"{sign}{num_value:.{precision}f}%"
        
        # Color coding: green for positive growth, red for negative
        if num_value > 5:  # Strong positive growth
            return self.colorize(formatted, Colors.GREEN + Colors.BOLD)
        elif num_value > 0:  # Moderate positive growth
            return self.colorize(formatted, Colors.GREEN)
        elif num_value > -5:  # Moderate negative growth
            return self.colorize(formatted, Colors.RED)
        else:  # Strong negative growth
            return self.colorize(formatted, Colors.RED + Colors.BOLD)
    
    def format_market_cap(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2
    ) -> str:
        """
        Format market capitalization values.
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places for compact notation
            
        Returns:
            Formatted market cap string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        # Always use compact notation for market cap
        return self._format_compact_currency(num_value, precision, show_sign=False)
    
    def format_eps(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        precision: int = 2
    ) -> str:
        """
        Format Earnings Per Share values.
        
        Args:
            value: Numeric value to format
            precision: Number of decimal places (default: 2)
            
        Returns:
            Formatted EPS string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        formatted = f"{self.currency_symbol}{num_value:.{precision}f}"
        
        # Color based on value
        if num_value < 0:
            return self.colorize(formatted, Colors.RED)
        elif num_value > 0:
            return self.colorize(formatted, Colors.GREEN)
        else:
            return self.colorize(formatted, Colors.WHITE)
    
    def format_volume(
        self, 
        value: Optional[Union[float, int, Decimal]], 
        compact: bool = True,
        precision: int = 1
    ) -> str:
        """
        Format trading volume values.
        
        Args:
            value: Numeric value to format
            compact: Whether to use compact notation (default: True)
            precision: Number of decimal places for compact notation
            
        Returns:
            Formatted volume string
        """
        if value is None:
            return self.colorize("N/A", Colors.DIM)
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return self.colorize("N/A", Colors.DIM)
        
        if compact:
            formatted = self._format_compact_number(num_value, precision)
        else:
            formatted = f"{num_value:,.0f}"
            formatted = self.colorize(formatted, Colors.CYAN)
        
        return formatted