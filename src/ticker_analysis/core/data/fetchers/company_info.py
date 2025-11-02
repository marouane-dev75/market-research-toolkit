"""
Company Info Fetcher Module

This module provides functionality to fetch and display comprehensive company information
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ....infrastructure.cache.manager import get_cache_manager


@dataclass
class CompanyInfoData:
    """
    Dataclass representing comprehensive company information for a ticker.

    All financial values are in the currency of the company's reporting.
    Values may be None if not available from the data source.
    """

    # Basic Information
    ticker: str
    company_name: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    employees: Optional[int] = None

    # Market Data
    last_price: Optional[float] = None
    market_cap: Optional[float] = None
    last_volume: Optional[float] = None
    avg_volume: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None

    # Valuation Metrics
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    pb_ratio: Optional[float] = None
    price_to_sales: Optional[float] = None
    enterprise_value: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None

    # Financial Metrics
    profit_margins: Optional[float] = None
    operating_margins: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None

    # Analyst Data
    recommendation: Optional[str] = None
    target_price: Optional[float] = None

    # Business Summary
    business_summary: Optional[str] = None


class CompanyInfoFetcher:
    """
    Fetcher class for retrieving and processing comprehensive company information.

    This class handles fetching financial data from yfinance and mapping it
    to the CompanyInfoData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_company_info(self, ticker_symbol: str) -> CompanyInfoData:
        """
        Fetch comprehensive company information for a given ticker.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            CompanyInfoData object with company information

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching company information for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='company_info'
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached company information for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching from API for {ticker_symbol}")
            
            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch company info
            info = ticker.info

            # Check if data was retrieved
            if not info or len(info) == 0:
                raise ValueError(f"No company information available for {ticker_symbol}")

            # Map info dictionary to dataclass
            company_data = self._map_to_dataclass(ticker_symbol, info)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=company_data,
                ticker=ticker_symbol,
                data_type='company_info'
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached company information for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache company information for {ticker_symbol}")
            
            return company_data

        except Exception as e:
            self.logger.error(f"Failed to fetch company information: {str(e)}")
            raise

    def _map_to_dataclass(self, ticker_symbol: str, info: dict) -> CompanyInfoData:
        """
        Map yfinance info dictionary to CompanyInfoData object.

        Args:
            ticker_symbol: Stock ticker symbol
            info: Dictionary from yfinance ticker.info

        Returns:
            CompanyInfoData object
        """
        def get_value(key: str, default=None):
            """Helper function to safely get values from info dict."""
            try:
                value = info.get(key, default)
                if value is None or value == 'N/A' or value == '':
                    return None
                return value
            except (ValueError, TypeError, KeyError):
                return None

        def get_float_value(key: str, default=None):
            """Helper function to safely get float values."""
            try:
                value = info.get(key, default)
                if value is None or value == 'N/A' or value == '':
                    return None
                return float(value)
            except (ValueError, TypeError, KeyError):
                return None

        def get_int_value(key: str, default=None):
            """Helper function to safely get integer values."""
            try:
                value = info.get(key, default)
                if value is None or value == 'N/A' or value == '':
                    return None
                return int(value)
            except (ValueError, TypeError, KeyError):
                return None

        # Create CompanyInfoData object
        company_info = CompanyInfoData(
            ticker=ticker_symbol,

            # Basic Information
            company_name=get_value('longName') or get_value('shortName'),
            exchange=get_value('exchange'),
            currency=get_value('currency'),
            country=get_value('country'),
            website=get_value('website'),
            sector=get_value('sector'),
            industry=get_value('industry'),
            employees=get_int_value('fullTimeEmployees'),

            # Market Data
            last_price=get_float_value('currentPrice') or get_float_value('regularMarketPrice'),
            market_cap=get_float_value('marketCap'),
            last_volume=get_float_value('volume') or get_float_value('regularMarketVolume'),
            avg_volume=get_float_value('averageVolume') or get_float_value('averageVolume10days'),
            fifty_two_week_high=get_float_value('fiftyTwoWeekHigh'),
            fifty_two_week_low=get_float_value('fiftyTwoWeekLow'),

            # Valuation Metrics
            pe_ratio=get_float_value('trailingPE') or get_float_value('priceToEarningsTrailing12Months'),
            forward_pe=get_float_value('forwardPE'),
            pb_ratio=get_float_value('priceToBook'),
            price_to_sales=get_float_value('priceToSalesTrailing12Months'),
            enterprise_value=get_float_value('enterpriseValue'),
            ev_to_revenue=get_float_value('enterpriseToRevenue'),
            ev_to_ebitda=get_float_value('enterpriseToEbitda'),
            dividend_yield=get_float_value('dividendYield') / 100 if get_float_value('dividendYield') is not None else None,
            beta=get_float_value('beta'),

            # Financial Metrics
            profit_margins=get_float_value('profitMargins'),
            operating_margins=get_float_value('operatingMargins'),
            return_on_assets=get_float_value('returnOnAssets'),
            return_on_equity=get_float_value('returnOnEquity'),
            debt_to_equity=get_float_value('debtToEquity') / 100 if get_float_value('debtToEquity') is not None else None,
            current_ratio=get_float_value('currentRatio'),
            quick_ratio=get_float_value('quickRatio'),
            revenue_growth=get_float_value('revenueGrowth'),
            earnings_growth=get_float_value('earningsGrowth'),

            # Analyst Data
            recommendation=get_value('recommendationKey'),
            target_price=get_float_value('targetMeanPrice'),

            # Business Summary
            business_summary=get_value('longBusinessSummary')
        )

        return company_info


def display_company_info(company_info: CompanyInfoData) -> None:
    """
    Display company information in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided CompanyInfoData object.

    Args:
        company_info: CompanyInfoData object to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    # Display header
    logger.print_header(f"Company Information for {company_info.ticker}")

    # Basic Information Section
    logger.print_section("BASIC INFORMATION")
    logger.print_bullet(f"Company Name:     {company_info.company_name or 'N/A'}")
    logger.print_bullet(f"Symbol:           {company_info.ticker}")
    logger.print_bullet(f"Exchange:         {company_info.exchange or 'N/A'}")
    logger.print_bullet(f"Currency:         {company_info.currency or 'N/A'}")
    logger.print_bullet(f"Country:          {company_info.country or 'N/A'}")
    logger.print_bullet(f"Website:          {company_info.website or 'N/A'}")
    logger.print_bullet(f"Sector:           {company_info.sector or 'N/A'}")
    logger.print_bullet(f"Industry:         {company_info.industry or 'N/A'}")
    logger.print_bullet(f"Employees:        {formatter.format_shares(company_info.employees) if company_info.employees else 'N/A'}")

    # Market Data Section
    logger.print_section("MARKET DATA")
    logger.print_bullet(f"Last Price:       {formatter.format_currency(company_info.last_price)}")
    logger.print_bullet(f"Market Cap:       {formatter.format_market_cap(company_info.market_cap)}")
    logger.print_bullet(f"Last Volume:      {formatter.format_volume(company_info.last_volume)}")
    logger.print_bullet(f"Avg Volume:       {formatter.format_volume(company_info.avg_volume)}")
    logger.print_bullet(f"52-Week High:     {formatter.format_currency(company_info.fifty_two_week_high)}")
    logger.print_bullet(f"52-Week Low:      {formatter.format_currency(company_info.fifty_two_week_low)}")

    # Valuation Metrics Section
    logger.print_section("VALUATION METRICS")
    logger.print_bullet(f"P/E Ratio:        {formatter.format_ratio(company_info.pe_ratio)}")
    logger.print_bullet(f"Forward P/E:      {formatter.format_ratio(company_info.forward_pe)}")
    logger.print_bullet(f"P/B Ratio:        {formatter.format_ratio(company_info.pb_ratio)}")
    logger.print_bullet(f"Price/Sales:      {formatter.format_ratio(company_info.price_to_sales)}")
    logger.print_bullet(f"Enterprise Value: {formatter.format_market_cap(company_info.enterprise_value)}")
    logger.print_bullet(f"EV/Revenue:       {formatter.format_ratio(company_info.ev_to_revenue)}")
    logger.print_bullet(f"EV/EBITDA:        {formatter.format_ratio(company_info.ev_to_ebitda)}")
    logger.print_bullet(f"Dividend Yield:   {formatter.format_percentage(company_info.dividend_yield)}")
    logger.print_bullet(f"Beta:             {formatter.format_ratio(company_info.beta)}")

    # Financial Metrics Section
    logger.print_section("FINANCIAL METRICS")
    logger.print_bullet(f"Profit Margins:   {formatter.format_percentage(company_info.profit_margins)}")
    logger.print_bullet(f"Operating Margins: {formatter.format_percentage(company_info.operating_margins)}")
    logger.print_bullet(f"ROA:              {formatter.format_percentage(company_info.return_on_assets)}")
    logger.print_bullet(f"ROE:              {formatter.format_percentage(company_info.return_on_equity)}")
    logger.print_bullet(f"Debt/Equity:      {formatter.format_percentage(company_info.debt_to_equity)}")
    logger.print_bullet(f"Current Ratio:    {formatter.format_ratio(company_info.current_ratio)}")
    logger.print_bullet(f"Quick Ratio:      {formatter.format_ratio(company_info.quick_ratio)}")
    logger.print_bullet(f"Revenue Growth:   {formatter.format_percentage(company_info.revenue_growth)}")
    logger.print_bullet(f"Earnings Growth:  {formatter.format_percentage(company_info.earnings_growth)}")

    # Analyst Data Section
    logger.print_section("ANALYST DATA")
    logger.print_bullet(f"Recommendation:   {company_info.recommendation or 'N/A'}")
    logger.print_bullet(f"Target Price:     {formatter.format_currency(company_info.target_price)}")

    # Business Summary Section
    if company_info.business_summary:
        logger.print_section("BUSINESS SUMMARY")
        # Truncate summary if too long (keep first 300 characters + "...")
        summary = company_info.business_summary
        if len(summary) > 300:
            summary = summary[:297] + "..."
        logger.print_bullet(summary)