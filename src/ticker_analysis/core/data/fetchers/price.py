"""
Price Fetcher Module

This module provides functionality to fetch and display historical price data
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ....infrastructure.cache.manager import get_cache_manager


class TimePeriod(Enum):
    """Enumeration for time period options."""
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    YEAR_TO_DATE = "ytd"
    MAX = "max"


@dataclass
class PriceData:
    """
    Dataclass representing historical price data for a ticker.

    All price values are in the currency of the company's reporting.
    Values may be None if not available from the data source.
    """

    # Metadata
    ticker: str
    period: TimePeriod
    date: Optional[str] = None

    # OHLCV Data
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    adjusted_close: Optional[float] = None
    volume: Optional[int] = None

    # Calculated Metrics
    daily_change: Optional[float] = None
    daily_change_percent: Optional[float] = None
    price_range: Optional[float] = None
    price_range_percent: Optional[float] = None

    # Additional Metrics
    vwap: Optional[float] = None  # Volume Weighted Average Price
    turnover: Optional[float] = None  # Volume * Close Price


class PriceFetcher:
    """
    Fetcher class for retrieving and processing historical price data.

    This class handles fetching financial data from yfinance and mapping it
    to the PriceData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_price_data(
        self,
        ticker_symbol: str,
        period: TimePeriod
    ) -> List[PriceData]:
        """
        Fetch historical price data for a given ticker and time period.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
            period: Time period (ONE_DAY, FIVE_DAYS, etc.)

        Returns:
            List of PriceData objects, one for each trading day

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching {period.value} price data for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='price_data',
                period=period.value
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached {period.value} price data for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching {period.value} price data from API for {ticker_symbol}")

            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch historical data based on period
            hist_df = ticker.history(period=period.value)

            # Check if data was retrieved
            if hist_df is None or hist_df.empty:
                raise ValueError(f"No price data available for {ticker_symbol}")

            # Map dataframe to list of PriceData objects
            price_data = self._map_to_dataclass(ticker_symbol, period, hist_df)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=price_data,
                ticker=ticker_symbol,
                data_type='price_data',
                period=period.value
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached {period.value} price data for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache {period.value} price data for {ticker_symbol}")
            
            return price_data

        except Exception as e:
            self.logger.error(f"Failed to fetch price data: {str(e)}")
            raise

    def _map_to_dataclass(
        self,
        ticker_symbol: str,
        period: TimePeriod,
        hist_df
    ) -> List[PriceData]:
        """
        Map pandas DataFrame to list of PriceData objects.

        Args:
            ticker_symbol: Stock ticker symbol
            period: Time period
            hist_df: Pandas DataFrame with historical price data

        Returns:
            List of PriceData objects
        """
        price_data_list = []

        # Iterate through each row (each row represents a trading day)
        for date_index, row in hist_df.iterrows():
            # Helper function to safely get values
            def get_value(key: str) -> Optional[float]:
                try:
                    if key in row.index:
                        val = row[key]
                        return float(val) if val is not None else None
                    return None
                except (ValueError, TypeError):
                    return None

            # Get basic OHLCV data
            open_price = get_value("Open")
            high_price = get_value("High")
            low_price = get_value("Low")
            close_price = get_value("Close")
            adjusted_close = get_value("Adj Close")
            volume = get_value("Volume")

            # Calculate derived metrics
            daily_change = None
            daily_change_percent = None
            if open_price is not None and close_price is not None:
                daily_change = close_price - open_price
                if open_price != 0:
                    daily_change_percent = (daily_change / open_price) * 100

            price_range = None
            price_range_percent = None
            if high_price is not None and low_price is not None:
                price_range = high_price - low_price
                if low_price != 0:
                    price_range_percent = (price_range / low_price) * 100

            # Calculate VWAP (approximation using close price)
            vwap = None
            if close_price is not None and volume is not None and volume > 0:
                vwap = close_price  # Simplified - in reality would need intraday data

            # Calculate turnover
            turnover = None
            if close_price is not None and volume is not None:
                turnover = close_price * volume

            # Create PriceData object
            price_data = PriceData(
                ticker=ticker_symbol,
                period=period,
                date=str(date_index.date()),

                # OHLCV Data
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                adjusted_close=adjusted_close,
                volume=int(volume) if volume is not None else None,

                # Calculated Metrics
                daily_change=daily_change,
                daily_change_percent=daily_change_percent,
                price_range=price_range,
                price_range_percent=price_range_percent,

                # Additional Metrics
                vwap=vwap,
                turnover=turnover,
            )

            price_data_list.append(price_data)

        return price_data_list


def display_price_data(price_data: PriceData) -> None:
    """
    Display price data in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided PriceData object.

    Args:
        price_data: PriceData object to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    # Display header
    logger.print_header(f"Price Data - {price_data.ticker}")

    # Display metadata
    logger.print_section("Period Information")
    logger.print_bullet(f"Time Period: {price_data.period.value}")
    logger.print_bullet(f"Date: {price_data.date or 'N/A'}")

    # OHLCV Section
    logger.print_section("OHLCV Data")
    logger.print_bullet(f"Open: {formatter.format_currency(price_data.open_price)}")
    logger.print_bullet(f"High: {formatter.format_currency(price_data.high_price)}")
    logger.print_bullet(f"Low: {formatter.format_currency(price_data.low_price)}")
    logger.print_bullet(f"Close: {formatter.format_currency(price_data.close_price)}")
    logger.print_bullet(f"Adjusted Close: {formatter.format_currency(price_data.adjusted_close)}")
    logger.print_bullet(f"Volume: {formatter.format_volume(price_data.volume)}")

    # Daily Performance Section
    logger.print_section("Daily Performance")
    logger.print_bullet(f"Daily Change: {formatter.format_currency(price_data.daily_change, show_sign=True)}")
    logger.print_bullet(f"Daily Change %: {formatter.format_percentage(price_data.daily_change_percent, show_sign=True, multiply_by_100=False)}")
    logger.print_bullet(f"Price Range: {formatter.format_currency(price_data.price_range)}")
    logger.print_bullet(f"Price Range %: {formatter.format_percentage(price_data.price_range_percent, multiply_by_100=False)}")

    # Additional Metrics Section
    logger.print_section("Additional Metrics")
    logger.print_bullet(f"VWAP: {formatter.format_currency(price_data.vwap)}")
    logger.print_bullet(f"Turnover: {formatter.format_currency(price_data.turnover, compact=True)}")


def display_price_summary(price_data_list: List[PriceData]) -> None:
    """
    Display a summary of multiple price data points.

    Args:
        price_data_list: List of PriceData objects to summarize
    """
    if not price_data_list:
        return

    logger = get_logger()
    formatter = FinancialFormatter()

    ticker = price_data_list[0].ticker
    period = price_data_list[0].period

    # Calculate summary statistics
    prices = [p.close_price for p in price_data_list if p.close_price is not None]
    volumes = [p.volume for p in price_data_list if p.volume is not None]

    if not prices:
        logger.error("No valid price data to summarize")
        return

    # Calculate metrics
    latest_price = prices[-1]
    earliest_price = prices[0]
    highest_price = max(prices)
    lowest_price = min(prices)
    avg_price = sum(prices) / len(prices)
    
    total_return = ((latest_price - earliest_price) / earliest_price) * 100 if earliest_price != 0 else 0
    avg_volume = sum(volumes) / len(volumes) if volumes else 0

    # Display summary
    logger.print_header(f"Price Summary - {ticker} ({period.value})")

    logger.print_section("Price Statistics")
    logger.print_bullet(f"Latest Price: {formatter.format_currency(latest_price)}")
    logger.print_bullet(f"Period High: {formatter.format_currency(highest_price)}")
    logger.print_bullet(f"Period Low: {formatter.format_currency(lowest_price)}")
    logger.print_bullet(f"Average Price: {formatter.format_currency(avg_price)}")

    logger.print_section("Performance")
    logger.print_bullet(f"Total Return: {formatter.format_growth_rate(total_return, multiply_by_100=False)}")
    logger.print_bullet(f"Price Range: {formatter.format_currency(highest_price - lowest_price)}")

    logger.print_section("Volume")
    logger.print_bullet(f"Average Volume: {formatter.format_volume(avg_volume)}")
    logger.print_bullet(f"Total Data Points: {len(price_data_list)}")