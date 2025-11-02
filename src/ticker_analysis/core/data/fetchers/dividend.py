"""
Dividend Fetcher Module

This module provides functionality to fetch and display dividend data
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, date
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ....infrastructure.cache.manager import get_cache_manager


@dataclass
class DividendData:
    """
    Dataclass representing dividend data for a ticker.
    
    Contains dividend payment information including date and amount.
    """
    
    # Metadata
    ticker: str
    
    # Dividend Information
    date: date
    amount: float


class DividendFetcher:
    """
    Fetcher class for retrieving and processing dividend data.

    This class handles fetching dividend data from yfinance and mapping it
    to the DividendData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_dividends(self, ticker_symbol: str) -> List[DividendData]:
        """
        Fetch dividend data for a given ticker.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            List of DividendData objects, one for each dividend payment

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching dividend data for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='dividends'
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached dividend data for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching dividend data from API for {ticker_symbol}")

            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch dividend data
            dividends = ticker.dividends

            # Check if data was retrieved
            if dividends is None or dividends.empty:
                raise ValueError(f"No dividend data available for {ticker_symbol}")

            # Map series to list of DividendData objects
            dividend_data = self._map_to_dataclass(ticker_symbol, dividends)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=dividend_data,
                ticker=ticker_symbol,
                data_type='dividends'
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached dividend data for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache dividend data for {ticker_symbol}")
            
            return dividend_data

        except Exception as e:
            self.logger.error(f"Failed to fetch dividend data: {str(e)}")
            raise

    def _map_to_dataclass(
        self,
        ticker_symbol: str,
        dividends_series
    ) -> List[DividendData]:
        """
        Map pandas Series to list of DividendData objects.

        Args:
            ticker_symbol: Stock ticker symbol
            dividends_series: Pandas Series with dividend data

        Returns:
            List of DividendData objects
        """
        dividend_data = []

        # Iterate through each dividend payment
        for dividend_date, amount in dividends_series.items():
            dividend = DividendData(
                ticker=ticker_symbol,
                date=dividend_date.date(),
                amount=float(amount)
            )
            dividend_data.append(dividend)

        # Sort by date (most recent first)
        dividend_data.sort(key=lambda x: x.date, reverse=True)

        return dividend_data


def display_dividends(dividend_data: List[DividendData], limit: Optional[int] = None) -> None:
    """
    Display dividend data in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided DividendData objects.

    Args:
        dividend_data: List of DividendData objects to display
        limit: Optional limit on number of dividends to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    if not dividend_data:
        logger.warning("No dividend data to display")
        return

    # Apply limit if specified
    display_data = dividend_data[:limit] if limit else dividend_data

    # Display header
    ticker = dividend_data[0].ticker
    logger.print_header(f"Dividend History - {ticker}")

    # Display summary
    logger.print_section("Summary")
    logger.print_bullet(f"Total Dividend Payments: {len(dividend_data)}")
    if limit and len(dividend_data) > limit:
        logger.print_bullet(f"Showing: Latest {limit} payments")
    
    # Calculate total dividends for the year
    current_year = datetime.now().year
    current_year_dividends = [d for d in dividend_data if d.date.year == current_year]
    if current_year_dividends:
        total_current_year = sum(d.amount for d in current_year_dividends)
        logger.print_bullet(f"Total {current_year} Dividends: {formatter.format_currency(total_current_year)}")

    # Display dividend payments
    logger.print_section("Dividend Payments")
    
    # Table header
    logger.print_bullet("Date          Amount")
    logger.print_bullet("-" * 25)
    
    # Display each dividend
    for dividend in display_data:
        date_formatted = dividend.date.strftime("%Y-%m-%d")
        amount_formatted = formatter.format_currency(dividend.amount)
        logger.print_bullet(f"{date_formatted}    {amount_formatted}")

    # Display statistics if we have data
    if dividend_data:
        logger.print_section("Statistics")
        amounts = [d.amount for d in dividend_data]
        logger.print_bullet(f"Highest Payment: {formatter.format_currency(max(amounts))}")
        logger.print_bullet(f"Lowest Payment: {formatter.format_currency(min(amounts))}")
        logger.print_bullet(f"Average Payment: {formatter.format_currency(sum(amounts) / len(amounts))}")
        
        # Calculate annual dividend yield trend (last 4 quarters if available)
        recent_dividends = dividend_data[:4] if len(dividend_data) >= 4 else dividend_data
        if len(recent_dividends) >= 4:
            annual_dividend = sum(d.amount for d in recent_dividends)
            logger.print_bullet(f"Trailing 12-Month Dividend: {formatter.format_currency(annual_dividend)}")