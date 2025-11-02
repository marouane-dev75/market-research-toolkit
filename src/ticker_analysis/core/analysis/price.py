"""
Price Analysis Module

This module provides functionality to analyze price movements and calculate
percentage changes over different time periods.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, timedelta
from ..data.fetchers.price import PriceData


@dataclass
class PriceAnalysisData:
    """
    Dataclass representing price analysis information for a ticker.
    
    Contains current price information and percentage changes over different periods.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    
    # Current Price Information
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    daily_change: Optional[float] = None
    daily_change_percent: Optional[float] = None
    
    # 52-Week Range
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    
    # Percentage Changes
    seven_day_change_percent: Optional[float] = None
    thirty_day_change_percent: Optional[float] = None
    ninety_day_change_percent: Optional[float] = None
    
    # Price Levels for Reference
    seven_day_price: Optional[float] = None
    thirty_day_price: Optional[float] = None
    ninety_day_price: Optional[float] = None
    
    # Volume Information
    current_volume: Optional[int] = None
    average_volume: Optional[int] = None
    volume_ratio: Optional[float] = None  # Current volume / Average volume


class PriceAnalyzer:
    """
    Analyzer class for calculating price movements and percentage changes.
    
    This class processes historical price data to calculate various price metrics
    and percentage changes over different time periods.
    """
    
    def __init__(self):
        """Initialize the price analyzer."""
        pass
    
    def analyze_price_movements(
        self,
        ticker: str,
        price_data_list: List[PriceData]
    ) -> Optional[PriceAnalysisData]:
        """
        Analyze price movements and calculate percentage changes.
        
        Args:
            ticker: Stock ticker symbol
            price_data_list: List of PriceData objects (should be sorted by date, newest first)
            
        Returns:
            PriceAnalysisData object with calculated metrics, or None if insufficient data
        """
        if not price_data_list or len(price_data_list) < 2:
            return None
        
        # Sort by date to ensure newest first
        sorted_data = sorted(price_data_list, key=lambda x: x.date, reverse=True)
        
        # Get current (latest) price data
        current_data = sorted_data[0]
        current_price = current_data.close_price
        
        if current_price is None:
            return None
        
        # Calculate daily change
        previous_close = None
        daily_change = None
        daily_change_percent = None
        
        if len(sorted_data) > 1:
            previous_data = sorted_data[1]
            previous_close = previous_data.close_price
            if previous_close is not None:
                daily_change = current_price - previous_close
                daily_change_percent = (daily_change / previous_close) * 100
        
        # Calculate percentage changes for different periods
        seven_day_change = self._calculate_period_change(sorted_data, current_price, 7)
        thirty_day_change = self._calculate_period_change(sorted_data, current_price, 30)
        ninety_day_change = self._calculate_period_change(sorted_data, current_price, 90)
        
        # Calculate 52-week high/low
        fifty_two_week_high = max(
            (data.high_price for data in sorted_data if data.high_price is not None),
            default=None
        )
        fifty_two_week_low = min(
            (data.low_price for data in sorted_data if data.low_price is not None),
            default=None
        )
        
        # Calculate volume metrics
        current_volume = current_data.volume
        volumes = [data.volume for data in sorted_data if data.volume is not None]
        average_volume = sum(volumes) / len(volumes) if volumes else None
        volume_ratio = None
        if current_volume is not None and average_volume is not None and average_volume > 0:
            volume_ratio = current_volume / average_volume
        
        return PriceAnalysisData(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            current_price=current_price,
            previous_close=previous_close,
            daily_change=daily_change,
            daily_change_percent=daily_change_percent,
            fifty_two_week_high=fifty_two_week_high,
            fifty_two_week_low=fifty_two_week_low,
            seven_day_change_percent=seven_day_change['percent'],
            thirty_day_change_percent=thirty_day_change['percent'],
            ninety_day_change_percent=ninety_day_change['percent'],
            seven_day_price=seven_day_change['price'],
            thirty_day_price=thirty_day_change['price'],
            ninety_day_price=ninety_day_change['price'],
            current_volume=current_volume,
            average_volume=int(average_volume) if average_volume else None,
            volume_ratio=volume_ratio
        )
    
    def _calculate_period_change(
        self,
        sorted_data: List[PriceData],
        current_price: float,
        days_back: int
    ) -> dict:
        """
        Calculate percentage change for a specific period.
        
        Args:
            sorted_data: List of PriceData sorted by date (newest first)
            current_price: Current price
            days_back: Number of days to look back
            
        Returns:
            Dictionary with 'percent' and 'price' keys
        """
        # Find the price from days_back ago
        target_date = None
        target_price = None
        
        # Look for data approximately days_back ago
        if len(sorted_data) >= days_back:
            # Try to get data from exactly days_back position
            if days_back <= len(sorted_data):
                target_data = sorted_data[days_back - 1]
                target_price = target_data.close_price
        
        # If we don't have exact data, find the closest available data
        if target_price is None and len(sorted_data) > 1:
            # Use the oldest available data if we don't have enough history
            target_data = sorted_data[-1]
            target_price = target_data.close_price
        
        # Calculate percentage change
        percent_change = None
        if target_price is not None and target_price != 0:
            percent_change = ((current_price - target_price) / target_price) * 100
        
        return {
            'percent': percent_change,
            'price': target_price
        }