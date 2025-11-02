"""
Data Models for Price Monitoring

This module contains data classes and enums used throughout the price monitoring system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging


class ThresholdOperator(Enum):
    """Enumeration of supported threshold operators."""
    EQUAL = "eq"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN_OR_EQUAL = "lte"

    @classmethod
    def from_string(cls, operator_str: str) -> 'ThresholdOperator':
        """
        Create ThresholdOperator from string.
        
        Args:
            operator_str: String representation of operator
            
        Returns:
            ThresholdOperator: Corresponding enum value
            
        Raises:
            ValueError: If operator string is not valid
        """
        operator_map = {
            "eq": cls.EQUAL,
            "gt": cls.GREATER_THAN,
            "lt": cls.LESS_THAN,
            "gte": cls.GREATER_THAN_OR_EQUAL,
            "lte": cls.LESS_THAN_OR_EQUAL,
        }
        
        if operator_str.lower() not in operator_map:
            valid_operators = list(operator_map.keys())
            raise ValueError(f"Invalid operator '{operator_str}'. Valid operators: {valid_operators}")
        
        return operator_map[operator_str.lower()]

    def evaluate(self, current_value: float, target_value: float) -> bool:
        """
        Evaluate the threshold condition.
        
        Args:
            current_value: Current price value
            target_value: Target threshold value
            
        Returns:
            bool: True if threshold condition is met
        """
        if self == ThresholdOperator.EQUAL:
            # For equality, use a small tolerance for floating point comparison
            return abs(current_value - target_value) < 0.01
        elif self == ThresholdOperator.GREATER_THAN:
            return current_value > target_value
        elif self == ThresholdOperator.LESS_THAN:
            return current_value < target_value
        elif self == ThresholdOperator.GREATER_THAN_OR_EQUAL:
            return current_value >= target_value
        elif self == ThresholdOperator.LESS_THAN_OR_EQUAL:
            return current_value <= target_value
        else:
            raise ValueError(f"Unknown operator: {self}")

    def get_description(self) -> str:
        """Get human-readable description of the operator."""
        descriptions = {
            ThresholdOperator.EQUAL: "equal to",
            ThresholdOperator.GREATER_THAN: "greater than",
            ThresholdOperator.LESS_THAN: "less than",
            ThresholdOperator.GREATER_THAN_OR_EQUAL: "greater than or equal to",
            ThresholdOperator.LESS_THAN_OR_EQUAL: "less than or equal to",
        }
        return descriptions[self]


@dataclass
class PriceThreshold:
    """
    Represents a price threshold configuration.
    
    Attributes:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        operator: Threshold operator (eq, gt, lt, gte, lte)
        target_price: Target price value for comparison
    """
    ticker: str
    operator: ThresholdOperator
    target_price: float

    @classmethod
    def from_string(cls, threshold_str: str) -> 'PriceThreshold':
        """
        Create PriceThreshold from string format.
        
        Args:
            threshold_str: String in format "TICKER:OPERATOR:VALUE"
                          e.g., "AAPL:gt:150" or "MSFT:lte:300"
            
        Returns:
            PriceThreshold: Parsed threshold object
            
        Raises:
            ValueError: If string format is invalid
        """
        try:
            parts = threshold_str.strip().split(':')
            if len(parts) != 3:
                raise ValueError(f"Invalid threshold format. Expected 'TICKER:OPERATOR:VALUE', got '{threshold_str}'")
            
            ticker, operator_str, price_str = parts
            
            # Validate ticker
            ticker = ticker.strip().upper()
            if not ticker:
                raise ValueError("Ticker symbol cannot be empty")
            
            # Parse operator
            operator = ThresholdOperator.from_string(operator_str.strip())
            
            # Parse price
            try:
                target_price = float(price_str.strip())
                if target_price < 0:
                    raise ValueError("Target price cannot be negative")
            except ValueError as e:
                raise ValueError(f"Invalid price value '{price_str}': {str(e)}")
            
            return cls(ticker=ticker, operator=operator, target_price=target_price)
            
        except Exception as e:
            raise ValueError(f"Failed to parse threshold '{threshold_str}': {str(e)}")

    def __str__(self) -> str:
        """String representation of the threshold."""
        return f"{self.ticker}:{self.operator.value}:{self.target_price}"

    def get_description(self) -> str:
        """Get human-readable description of the threshold."""
        return f"{self.ticker} {self.operator.get_description()} ${self.target_price:.2f}"


@dataclass
class ThresholdResult:
    """
    Represents the result of a threshold evaluation.
    
    Attributes:
        threshold: The threshold that was evaluated
        current_price: Current market price of the ticker
        triggered: Whether the threshold condition was met
        message: Human-readable message describing the result
        error: Optional error message if price fetch failed
    """
    threshold: PriceThreshold
    current_price: Optional[float]
    triggered: bool
    message: str
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        """Check if the evaluation was successful (no errors)."""
        return self.error is None

    @property
    def ticker(self) -> str:
        """Get the ticker symbol."""
        return self.threshold.ticker

    def get_alert_message(self) -> str:
        """
        Get formatted alert message for notifications.
        
        Returns:
            str: Formatted alert message
        """
        if self.error:
            return f"❌ {self.ticker}: Error - {self.error}"
        
        if not self.triggered:
            return f"✅ {self.ticker}: ${self.current_price:.2f} (No alert)"
        
        # Format triggered alert
        price_str = f"${self.current_price:.2f}" if self.current_price is not None else "N/A"
        target_str = f"${self.threshold.target_price:.2f}"
        operator_desc = self.threshold.operator.get_description()
        
        return f"💸 {self.ticker}: {price_str} is {operator_desc} {target_str}"

    def __str__(self) -> str:
        """String representation of the result."""
        return self.message