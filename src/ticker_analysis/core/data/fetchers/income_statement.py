"""
Income Statement Fetcher Module

This module provides functionality to fetch and display income statement data
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ..enums import DataFrequency
from ....infrastructure.cache.manager import get_cache_manager


@dataclass
class IncomeStatementData:
    """
    Dataclass representing income statement data for a ticker.

    All financial values are in the currency of the company's reporting.
    Values may be None if not available from the data source.
    """

    # Metadata
    ticker: str
    frequency: DataFrequency
    period_end_date: Optional[str] = None

    # Revenue Components
    total_revenue: Optional[float] = None
    operating_revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None

    # Operating Expenses
    operating_expense: Optional[float] = None
    selling_general_and_administration: Optional[float] = None
    research_and_development: Optional[float] = None

    # Operating Income
    operating_income: Optional[float] = None

    # Non-Operating Items
    interest_income_non_operating: Optional[float] = None
    interest_expense_non_operating: Optional[float] = None
    net_non_operating_interest_income_expense: Optional[float] = None
    other_non_operating_income_expenses: Optional[float] = None
    other_income_expense: Optional[float] = None

    # Pre-Tax and Tax
    pretax_income: Optional[float] = None
    tax_provision: Optional[float] = None
    tax_rate_for_calcs: Optional[float] = None
    tax_effect_of_unusual_items: Optional[float] = None

    # Net Income Components
    net_income_continuous_operations: Optional[float] = None
    net_income_including_noncontrolling_interests: Optional[float] = None
    net_income: Optional[float] = None
    net_income_common_stockholders: Optional[float] = None
    diluted_ni_available_to_common_stockholders: Optional[float] = None
    net_income_from_continuing_and_discontinued_operations: Optional[float] = None
    net_income_from_continuing_operations: Optional[float] = None
    normalized_income: Optional[float] = None

    # Earnings Per Share
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None
    basic_average_shares: Optional[float] = None
    diluted_average_shares: Optional[float] = None

    # EBITDA and EBIT
    ebit: Optional[float] = None
    ebitda: Optional[float] = None
    normalized_ebitda: Optional[float] = None
    reconciled_cost_of_revenue: Optional[float] = None
    reconciled_depreciation: Optional[float] = None

    # Interest Items
    interest_income: Optional[float] = None
    interest_expense: Optional[float] = None
    net_interest_income: Optional[float] = None

    # Totals
    total_expenses: Optional[float] = None
    total_operating_income_as_reported: Optional[float] = None


class IncomeStatementFetcher:
    """
    Fetcher class for retrieving and processing income statement data.

    This class handles fetching financial data from yfinance and mapping it
    to the IncomeStatementData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_income_statement(
        self,
        ticker_symbol: str,
        frequency: DataFrequency
    ) -> list[IncomeStatementData]:
        """
        Fetch income statement data for a given ticker and frequency.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
            frequency: Data frequency (YEARLY or QUARTERLY)

        Returns:
            List of IncomeStatementData objects, one for each period

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching {frequency.value} income statement for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='income_statements',
                frequency=frequency.value
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached {frequency.value} income statement for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching {frequency.value} income statement from API for {ticker_symbol}")

            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch income statement based on frequency
            if frequency == DataFrequency.YEARLY:
                income_df = ticker.financials
            else:  # QUARTERLY
                income_df = ticker.quarterly_financials

            # Check if data was retrieved
            if income_df is None or income_df.empty:
                raise ValueError(f"No income statement data available for {ticker_symbol}")

            # Map dataframe to list of IncomeStatementData objects
            income_data = self._map_to_dataclass(ticker_symbol, frequency, income_df)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=income_data,
                ticker=ticker_symbol,
                data_type='income_statements',
                frequency=frequency.value
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached {frequency.value} income statement for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache {frequency.value} income statement for {ticker_symbol}")
            
            return income_data

        except Exception as e:
            self.logger.error(f"Failed to fetch income statement: {str(e)}")
            raise

    def _map_to_dataclass(
        self,
        ticker_symbol: str,
        frequency: DataFrequency,
        income_df
    ) -> list[IncomeStatementData]:
        """
        Map pandas DataFrame to list of IncomeStatementData objects.

        Args:
            ticker_symbol: Stock ticker symbol
            frequency: Data frequency
            income_df: Pandas DataFrame with income statement data

        Returns:
            List of IncomeStatementData objects
        """
        income_statements = []

        # Iterate through each column (each column represents a period)
        for period_date in income_df.columns:
            period_data = income_df[period_date]

            # Helper function to safely get values
            def get_value(key: str) -> Optional[float]:
                try:
                    if key in period_data.index:
                        val = period_data[key]
                        return float(val) if val is not None else None
                    return None
                except (ValueError, TypeError):
                    return None

            # Create IncomeStatementData object
            statement = IncomeStatementData(
                ticker=ticker_symbol,
                frequency=frequency,
                period_end_date=str(period_date.date()),

                # Revenue Components
                total_revenue=get_value("Total Revenue"),
                operating_revenue=get_value("Operating Revenue"),
                cost_of_revenue=get_value("Cost Of Revenue"),
                gross_profit=get_value("Gross Profit"),

                # Operating Expenses
                operating_expense=get_value("Operating Expense"),
                selling_general_and_administration=get_value("Selling General And Administration"),
                research_and_development=get_value("Research And Development"),

                # Operating Income
                operating_income=get_value("Operating Income"),

                # Non-Operating Items
                interest_income_non_operating=get_value("Interest Income Non Operating"),
                interest_expense_non_operating=get_value("Interest Expense Non Operating"),
                net_non_operating_interest_income_expense=get_value("Net Non Operating Interest Income Expense"),
                other_non_operating_income_expenses=get_value("Other Non Operating Income Expenses"),
                other_income_expense=get_value("Other Income Expense"),

                # Pre-Tax and Tax
                pretax_income=get_value("Pretax Income"),
                tax_provision=get_value("Tax Provision"),
                tax_rate_for_calcs=get_value("Tax Rate For Calcs"),
                tax_effect_of_unusual_items=get_value("Tax Effect Of Unusual Items"),

                # Net Income Components
                net_income_continuous_operations=get_value("Net Income Continuous Operations"),
                net_income_including_noncontrolling_interests=get_value("Net Income Including Noncontrolling Interests"),
                net_income=get_value("Net Income"),
                net_income_common_stockholders=get_value("Net Income Common Stockholders"),
                diluted_ni_available_to_common_stockholders=get_value("Diluted NI Availto Com Stockholders"),
                net_income_from_continuing_and_discontinued_operations=get_value("Net Income From Continuing And Discontinued Operations"),
                net_income_from_continuing_operations=get_value("Net Income From Continuing Operation Net Minority Interest"),
                normalized_income=get_value("Normalized Income"),

                # Earnings Per Share
                basic_eps=get_value("Basic EPS"),
                diluted_eps=get_value("Diluted EPS"),
                basic_average_shares=get_value("Basic Average Shares"),
                diluted_average_shares=get_value("Diluted Average Shares"),

                # EBITDA and EBIT
                ebit=get_value("EBIT"),
                ebitda=get_value("EBITDA"),
                normalized_ebitda=get_value("Normalized EBITDA"),
                reconciled_cost_of_revenue=get_value("Reconciled Cost Of Revenue"),
                reconciled_depreciation=get_value("Reconciled Depreciation"),

                # Interest Items
                interest_income=get_value("Interest Income"),
                interest_expense=get_value("Interest Expense"),
                net_interest_income=get_value("Net Interest Income"),

                # Totals
                total_expenses=get_value("Total Expenses"),
                total_operating_income_as_reported=get_value("Total Operating Income As Reported"),
            )

            income_statements.append(statement)

        return income_statements


def display_income_statement(income_data: IncomeStatementData) -> None:
    """
    Display income statement data in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided IncomeStatementData object.

    Args:
        income_data: IncomeStatementData object to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    # Display header
    logger.print_header(f"Income Statement - {income_data.ticker}")

    # Display metadata
    logger.print_section("Period Information")
    logger.print_bullet(f"Frequency: {income_data.frequency.value.capitalize()}")
    logger.print_bullet(f"Period End Date: {income_data.period_end_date or 'N/A'}")

    # Revenue Section
    logger.print_section("Revenue")
    logger.print_bullet(f"Total Revenue: {formatter.format_currency(income_data.total_revenue, compact=True)}")
    logger.print_bullet(f"Operating Revenue: {formatter.format_currency(income_data.operating_revenue, compact=True)}")
    logger.print_bullet(f"Cost of Revenue: {formatter.format_currency(income_data.cost_of_revenue, compact=True)}")
    logger.print_bullet(f"Gross Profit: {formatter.format_currency(income_data.gross_profit, compact=True)}")

    # Operating Expenses Section
    logger.print_section("Operating Expenses")
    logger.print_bullet(f"Total Operating Expense: {formatter.format_currency(income_data.operating_expense, compact=True)}")
    logger.print_bullet(f"Selling, General & Admin: {formatter.format_currency(income_data.selling_general_and_administration, compact=True)}")
    logger.print_bullet(f"Research & Development: {formatter.format_currency(income_data.research_and_development, compact=True)}")

    # Operating Income Section
    logger.print_section("Operating Income")
    logger.print_bullet(f"Operating Income: {formatter.format_currency(income_data.operating_income, compact=True)}")
    logger.print_bullet(f"EBIT: {formatter.format_currency(income_data.ebit, compact=True)}")
    logger.print_bullet(f"EBITDA: {formatter.format_currency(income_data.ebitda, compact=True)}")
    logger.print_bullet(f"Normalized EBITDA: {formatter.format_currency(income_data.normalized_ebitda, compact=True)}")

    # Non-Operating Items Section
    logger.print_section("Non-Operating Items")
    logger.print_bullet(f"Interest Income: {formatter.format_currency(income_data.interest_income_non_operating, compact=True)}")
    logger.print_bullet(f"Interest Expense: {formatter.format_currency(income_data.interest_expense_non_operating, compact=True)}")
    logger.print_bullet(f"Net Interest: {formatter.format_currency(income_data.net_non_operating_interest_income_expense, compact=True)}")
    logger.print_bullet(f"Other Income/Expense: {formatter.format_currency(income_data.other_income_expense, compact=True)}")

    # Income and Tax Section
    logger.print_section("Income and Tax")
    logger.print_bullet(f"Pretax Income: {formatter.format_currency(income_data.pretax_income, compact=True)}")
    logger.print_bullet(f"Tax Provision: {formatter.format_currency(income_data.tax_provision, compact=True)}")
    logger.print_bullet(f"Tax Rate: {formatter.format_percentage(income_data.tax_rate_for_calcs)}")

    # Net Income Section
    logger.print_section("Net Income")
    logger.print_bullet(f"Net Income: {formatter.format_currency(income_data.net_income, compact=True)}")
    logger.print_bullet(f"Net Income (Common): {formatter.format_currency(income_data.net_income_common_stockholders, compact=True)}")
    logger.print_bullet(f"Normalized Income: {formatter.format_currency(income_data.normalized_income, compact=True)}")

    # Earnings Per Share Section
    logger.print_section("Earnings Per Share")
    logger.print_bullet(f"Basic EPS: {formatter.format_eps(income_data.basic_eps)}")
    logger.print_bullet(f"Diluted EPS: {formatter.format_eps(income_data.diluted_eps)}")
    logger.print_bullet(f"Basic Shares: {formatter.format_shares(income_data.basic_average_shares, compact=True)}")
    logger.print_bullet(f"Diluted Shares: {formatter.format_shares(income_data.diluted_average_shares, compact=True)}")
