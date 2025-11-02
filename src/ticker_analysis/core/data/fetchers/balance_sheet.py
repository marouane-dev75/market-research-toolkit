"""
Balance Sheet Fetcher Module

This module provides functionality to fetch and display balance sheet data
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ..enums import DataFrequency
from ....infrastructure.cache.manager import get_cache_manager


@dataclass
class BalanceSheetData:
    """
    Dataclass representing balance sheet data for a ticker.

    All financial values are in the currency of the company's reporting.
    Values may be None if not available from the data source.
    """

    # Metadata
    ticker: str
    frequency: DataFrequency
    period_end_date: Optional[str] = None

    # Share Information
    treasury_shares_number: Optional[float] = None
    ordinary_shares_number: Optional[float] = None
    share_issued: Optional[float] = None

    # Debt and Capital
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    tangible_book_value: Optional[float] = None
    invested_capital: Optional[float] = None
    working_capital: Optional[float] = None
    net_tangible_assets: Optional[float] = None
    capital_lease_obligations: Optional[float] = None

    # Equity
    common_stock_equity: Optional[float] = None
    total_capitalization: Optional[float] = None
    total_equity_gross_minority_interest: Optional[float] = None
    stockholders_equity: Optional[float] = None
    gains_losses_not_affecting_retained_earnings: Optional[float] = None
    other_equity_adjustments: Optional[float] = None
    retained_earnings: Optional[float] = None
    capital_stock: Optional[float] = None
    common_stock: Optional[float] = None

    # Liabilities
    total_liabilities_net_minority_interest: Optional[float] = None
    total_non_current_liabilities_net_minority_interest: Optional[float] = None
    other_non_current_liabilities: Optional[float] = None
    tradeand_other_payables_non_current: Optional[float] = None
    long_term_debt_and_capital_lease_obligation: Optional[float] = None
    long_term_capital_lease_obligation: Optional[float] = None
    long_term_debt: Optional[float] = None

    # Current Liabilities
    current_liabilities: Optional[float] = None
    other_current_liabilities: Optional[float] = None
    current_deferred_liabilities: Optional[float] = None
    current_deferred_revenue: Optional[float] = None
    current_debt_and_capital_lease_obligation: Optional[float] = None
    current_capital_lease_obligation: Optional[float] = None
    current_debt: Optional[float] = None
    other_current_borrowings: Optional[float] = None
    commercial_paper: Optional[float] = None
    payables_and_accrued_expenses: Optional[float] = None
    payables: Optional[float] = None
    total_tax_payable: Optional[float] = None
    income_tax_payable: Optional[float] = None
    accounts_payable: Optional[float] = None

    # Assets
    total_assets: Optional[float] = None
    total_non_current_assets: Optional[float] = None
    other_non_current_assets: Optional[float] = None
    non_current_deferred_assets: Optional[float] = None
    non_current_deferred_taxes_assets: Optional[float] = None
    investments_and_advances: Optional[float] = None
    other_investments: Optional[float] = None
    investment_in_financial_assets: Optional[float] = None
    available_for_sale_securities: Optional[float] = None
    net_ppe: Optional[float] = None
    accumulated_depreciation: Optional[float] = None
    gross_ppe: Optional[float] = None
    leases: Optional[float] = None
    other_properties: Optional[float] = None
    machinery_furniture_equipment: Optional[float] = None
    land_and_improvements: Optional[float] = None
    properties: Optional[float] = None

    # Current Assets
    current_assets: Optional[float] = None
    other_current_assets: Optional[float] = None
    inventory: Optional[float] = None
    receivables: Optional[float] = None
    other_receivables: Optional[float] = None
    accounts_receivable: Optional[float] = None
    cash_cash_equivalents_and_short_term_investments: Optional[float] = None
    other_short_term_investments: Optional[float] = None
    cash_and_cash_equivalents: Optional[float] = None
    cash_equivalents: Optional[float] = None
    cash_financial: Optional[float] = None


class BalanceSheetFetcher:
    """
    Fetcher class for retrieving and processing balance sheet data.

    This class handles fetching financial data from yfinance and mapping it
    to the BalanceSheetData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_balance_sheet(
        self,
        ticker_symbol: str,
        frequency: DataFrequency
    ) -> list[BalanceSheetData]:
        """
        Fetch balance sheet data for a given ticker and frequency.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
            frequency: Data frequency (YEARLY or QUARTERLY)

        Returns:
            List of BalanceSheetData objects, one for each period

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching {frequency.value} balance sheet for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='balance_sheets',
                frequency=frequency.value
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached {frequency.value} balance sheet for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching {frequency.value} balance sheet from API for {ticker_symbol}")

            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch balance sheet based on frequency
            if frequency == DataFrequency.YEARLY:
                balance_df = ticker.balance_sheet
            else:  # QUARTERLY
                balance_df = ticker.quarterly_balance_sheet

            # Check if data was retrieved
            if balance_df is None or balance_df.empty:
                raise ValueError(f"No balance sheet data available for {ticker_symbol}")

            # Map dataframe to list of BalanceSheetData objects
            balance_data = self._map_to_dataclass(ticker_symbol, frequency, balance_df)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=balance_data,
                ticker=ticker_symbol,
                data_type='balance_sheets',
                frequency=frequency.value
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached {frequency.value} balance sheet for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache {frequency.value} balance sheet for {ticker_symbol}")
            
            return balance_data

        except Exception as e:
            self.logger.error(f"Failed to fetch balance sheet: {str(e)}")
            raise

    def _map_to_dataclass(
        self,
        ticker_symbol: str,
        frequency: DataFrequency,
        balance_df
    ) -> list[BalanceSheetData]:
        """
        Map pandas DataFrame to list of BalanceSheetData objects.

        Args:
            ticker_symbol: Stock ticker symbol
            frequency: Data frequency
            balance_df: Pandas DataFrame with balance sheet data

        Returns:
            List of BalanceSheetData objects
        """
        balance_sheets = []

        # Iterate through each column (each column represents a period)
        for period_date in balance_df.columns:
            period_data = balance_df[period_date]

            # Helper function to safely get values
            def get_value(key: str) -> Optional[float]:
                try:
                    if key in period_data.index:
                        val = period_data[key]
                        return float(val) if val is not None else None
                    return None
                except (ValueError, TypeError):
                    return None

            # Create BalanceSheetData object
            statement = BalanceSheetData(
                ticker=ticker_symbol,
                frequency=frequency,
                period_end_date=str(period_date.date()),

                # Share Information
                treasury_shares_number=get_value("Treasury Shares Number"),
                ordinary_shares_number=get_value("Ordinary Shares Number"),
                share_issued=get_value("Share Issued"),

                # Debt and Capital
                net_debt=get_value("Net Debt"),
                total_debt=get_value("Total Debt"),
                tangible_book_value=get_value("Tangible Book Value"),
                invested_capital=get_value("Invested Capital"),
                working_capital=get_value("Working Capital"),
                net_tangible_assets=get_value("Net Tangible Assets"),
                capital_lease_obligations=get_value("Capital Lease Obligations"),

                # Equity
                common_stock_equity=get_value("Common Stock Equity"),
                total_capitalization=get_value("Total Capitalization"),
                total_equity_gross_minority_interest=get_value("Total Equity Gross Minority Interest"),
                stockholders_equity=get_value("Stockholders Equity"),
                gains_losses_not_affecting_retained_earnings=get_value("Gains Losses Not Affecting Retained Earnings"),
                other_equity_adjustments=get_value("Other Equity Adjustments"),
                retained_earnings=get_value("Retained Earnings"),
                capital_stock=get_value("Capital Stock"),
                common_stock=get_value("Common Stock"),

                # Liabilities
                total_liabilities_net_minority_interest=get_value("Total Liabilities Net Minority Interest"),
                total_non_current_liabilities_net_minority_interest=get_value("Total Non Current Liabilities Net Minority Interest"),
                other_non_current_liabilities=get_value("Other Non Current Liabilities"),
                tradeand_other_payables_non_current=get_value("Tradeand Other Payables Non Current"),
                long_term_debt_and_capital_lease_obligation=get_value("Long Term Debt And Capital Lease Obligation"),
                long_term_capital_lease_obligation=get_value("Long Term Capital Lease Obligation"),
                long_term_debt=get_value("Long Term Debt"),

                # Current Liabilities
                current_liabilities=get_value("Current Liabilities"),
                other_current_liabilities=get_value("Other Current Liabilities"),
                current_deferred_liabilities=get_value("Current Deferred Liabilities"),
                current_deferred_revenue=get_value("Current Deferred Revenue"),
                current_debt_and_capital_lease_obligation=get_value("Current Debt And Capital Lease Obligation"),
                current_capital_lease_obligation=get_value("Current Capital Lease Obligation"),
                current_debt=get_value("Current Debt"),
                other_current_borrowings=get_value("Other Current Borrowings"),
                commercial_paper=get_value("Commercial Paper"),
                payables_and_accrued_expenses=get_value("Payables And Accrued Expenses"),
                payables=get_value("Payables"),
                total_tax_payable=get_value("Total Tax Payable"),
                income_tax_payable=get_value("Income Tax Payable"),
                accounts_payable=get_value("Accounts Payable"),

                # Assets
                total_assets=get_value("Total Assets"),
                total_non_current_assets=get_value("Total Non Current Assets"),
                other_non_current_assets=get_value("Other Non Current Assets"),
                non_current_deferred_assets=get_value("Non Current Deferred Assets"),
                non_current_deferred_taxes_assets=get_value("Non Current Deferred Taxes Assets"),
                investments_and_advances=get_value("Investments And Advances"),
                other_investments=get_value("Other Investments"),
                investment_in_financial_assets=get_value("Investmentin Financial Assets"),
                available_for_sale_securities=get_value("Available For Sale Securities"),
                net_ppe=get_value("Net PPE"),
                accumulated_depreciation=get_value("Accumulated Depreciation"),
                gross_ppe=get_value("Gross PPE"),
                leases=get_value("Leases"),
                other_properties=get_value("Other Properties"),
                machinery_furniture_equipment=get_value("Machinery Furniture Equipment"),
                land_and_improvements=get_value("Land And Improvements"),
                properties=get_value("Properties"),

                # Current Assets
                current_assets=get_value("Current Assets"),
                other_current_assets=get_value("Other Current Assets"),
                inventory=get_value("Inventory"),
                receivables=get_value("Receivables"),
                other_receivables=get_value("Other Receivables"),
                accounts_receivable=get_value("Accounts Receivable"),
                cash_cash_equivalents_and_short_term_investments=get_value("Cash Cash Equivalents And Short Term Investments"),
                other_short_term_investments=get_value("Other Short Term Investments"),
                cash_and_cash_equivalents=get_value("Cash And Cash Equivalents"),
                cash_equivalents=get_value("Cash Equivalents"),
                cash_financial=get_value("Cash Financial"),
            )

            balance_sheets.append(statement)

        return balance_sheets


def display_balance_sheet(balance_data: BalanceSheetData) -> None:
    """
    Display balance sheet data in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided BalanceSheetData object.

    Args:
        balance_data: BalanceSheetData object to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    # Display header
    logger.print_header(f"Balance Sheet - {balance_data.ticker}")

    # Display metadata
    logger.print_section("Period Information")
    logger.print_bullet(f"Frequency: {balance_data.frequency.value.capitalize()}")
    logger.print_bullet(f"Period End Date: {balance_data.period_end_date or 'N/A'}")

    # Share Information Section
    logger.print_section("Share Information")
    logger.print_bullet(f"Treasury Shares Number: {formatter.format_shares(balance_data.treasury_shares_number, compact=True)}")
    logger.print_bullet(f"Ordinary Shares Number: {formatter.format_shares(balance_data.ordinary_shares_number, compact=True)}")
    logger.print_bullet(f"Share Issued: {formatter.format_shares(balance_data.share_issued, compact=True)}")

    # Current Assets Section
    logger.print_section("Current Assets")
    logger.print_bullet(f"Cash Financial: {formatter.format_currency(balance_data.cash_financial, compact=True)}")
    logger.print_bullet(f"Cash Equivalents: {formatter.format_currency(balance_data.cash_equivalents, compact=True)}")
    logger.print_bullet(f"Cash & Cash Equivalents: {formatter.format_currency(balance_data.cash_and_cash_equivalents, compact=True)}")
    logger.print_bullet(f"Other Short Term Investments: {formatter.format_currency(balance_data.other_short_term_investments, compact=True)}")
    logger.print_bullet(f"Cash & Short Term Investments: {formatter.format_currency(balance_data.cash_cash_equivalents_and_short_term_investments, compact=True)}")
    logger.print_bullet(f"Accounts Receivable: {formatter.format_currency(balance_data.accounts_receivable, compact=True)}")
    logger.print_bullet(f"Other Receivables: {formatter.format_currency(balance_data.other_receivables, compact=True)}")
    logger.print_bullet(f"Receivables: {formatter.format_currency(balance_data.receivables, compact=True)}")
    logger.print_bullet(f"Inventory: {formatter.format_currency(balance_data.inventory, compact=True)}")
    logger.print_bullet(f"Other Current Assets: {formatter.format_currency(balance_data.other_current_assets, compact=True)}")
    logger.print_bullet(f"Current Assets: {formatter.format_currency(balance_data.current_assets, compact=True)}")

    # Non-Current Assets Section
    logger.print_section("Non-Current Assets")
    logger.print_bullet(f"Properties: {formatter.format_currency(balance_data.properties, compact=True)}")
    logger.print_bullet(f"Land And Improvements: {formatter.format_currency(balance_data.land_and_improvements, compact=True)}")
    logger.print_bullet(f"Machinery Furniture Equipment: {formatter.format_currency(balance_data.machinery_furniture_equipment, compact=True)}")
    logger.print_bullet(f"Other Properties: {formatter.format_currency(balance_data.other_properties, compact=True)}")
    logger.print_bullet(f"Leases: {formatter.format_currency(balance_data.leases, compact=True)}")
    logger.print_bullet(f"Gross PPE: {formatter.format_currency(balance_data.gross_ppe, compact=True)}")
    logger.print_bullet(f"Accumulated Depreciation: {formatter.format_currency(balance_data.accumulated_depreciation, compact=True)}")
    logger.print_bullet(f"Net PPE: {formatter.format_currency(balance_data.net_ppe, compact=True)}")
    logger.print_bullet(f"Available For Sale Securities: {formatter.format_currency(balance_data.available_for_sale_securities, compact=True)}")
    logger.print_bullet(f"Investment in Financial Assets: {formatter.format_currency(balance_data.investment_in_financial_assets, compact=True)}")
    logger.print_bullet(f"Other Investments: {formatter.format_currency(balance_data.other_investments, compact=True)}")
    logger.print_bullet(f"Investments And Advances: {formatter.format_currency(balance_data.investments_and_advances, compact=True)}")
    logger.print_bullet(f"Non Current Deferred Taxes Assets: {formatter.format_currency(balance_data.non_current_deferred_taxes_assets, compact=True)}")
    logger.print_bullet(f"Non Current Deferred Assets: {formatter.format_currency(balance_data.non_current_deferred_assets, compact=True)}")
    logger.print_bullet(f"Other Non Current Assets: {formatter.format_currency(balance_data.other_non_current_assets, compact=True)}")
    logger.print_bullet(f"Total Non Current Assets: {formatter.format_currency(balance_data.total_non_current_assets, compact=True)}")

    # Total Assets Section
    logger.print_section("Total Assets")
    logger.print_bullet(f"Total Assets: {formatter.format_currency(balance_data.total_assets, compact=True)}")

    # Current Liabilities Section
    logger.print_section("Current Liabilities")
    logger.print_bullet(f"Accounts Payable: {formatter.format_currency(balance_data.accounts_payable, compact=True)}")
    logger.print_bullet(f"Income Tax Payable: {formatter.format_currency(balance_data.income_tax_payable, compact=True)}")
    logger.print_bullet(f"Total Tax Payable: {formatter.format_currency(balance_data.total_tax_payable, compact=True)}")
    logger.print_bullet(f"Payables: {formatter.format_currency(balance_data.payables, compact=True)}")
    logger.print_bullet(f"Payables And Accrued Expenses: {formatter.format_currency(balance_data.payables_and_accrued_expenses, compact=True)}")
    logger.print_bullet(f"Commercial Paper: {formatter.format_currency(balance_data.commercial_paper, compact=True)}")
    logger.print_bullet(f"Other Current Borrowings: {formatter.format_currency(balance_data.other_current_borrowings, compact=True)}")
    logger.print_bullet(f"Current Debt: {formatter.format_currency(balance_data.current_debt, compact=True)}")
    logger.print_bullet(f"Current Capital Lease Obligation: {formatter.format_currency(balance_data.current_capital_lease_obligation, compact=True)}")
    logger.print_bullet(f"Current Debt And Capital Lease Obligation: {formatter.format_currency(balance_data.current_debt_and_capital_lease_obligation, compact=True)}")
    logger.print_bullet(f"Current Deferred Revenue: {formatter.format_currency(balance_data.current_deferred_revenue, compact=True)}")
    logger.print_bullet(f"Current Deferred Liabilities: {formatter.format_currency(balance_data.current_deferred_liabilities, compact=True)}")
    logger.print_bullet(f"Other Current Liabilities: {formatter.format_currency(balance_data.other_current_liabilities, compact=True)}")
    logger.print_bullet(f"Current Liabilities: {formatter.format_currency(balance_data.current_liabilities, compact=True)}")

    # Non-Current Liabilities Section
    logger.print_section("Non-Current Liabilities")
    logger.print_bullet(f"Long Term Debt: {formatter.format_currency(balance_data.long_term_debt, compact=True)}")
    logger.print_bullet(f"Long Term Capital Lease Obligation: {formatter.format_currency(balance_data.long_term_capital_lease_obligation, compact=True)}")
    logger.print_bullet(f"Long Term Debt And Capital Lease Obligation: {formatter.format_currency(balance_data.long_term_debt_and_capital_lease_obligation, compact=True)}")
    logger.print_bullet(f"Tradeand Other Payables Non Current: {formatter.format_currency(balance_data.tradeand_other_payables_non_current, compact=True)}")
    logger.print_bullet(f"Other Non Current Liabilities: {formatter.format_currency(balance_data.other_non_current_liabilities, compact=True)}")
    logger.print_bullet(f"Total Non Current Liabilities Net Minor: {formatter.format_currency(balance_data.total_non_current_liabilities_net_minority_interest, compact=True)}")

    # Total Liabilities Section
    logger.print_section("Total Liabilities")
    logger.print_bullet(f"Total Liabilities Net Minority Interest: {formatter.format_currency(balance_data.total_liabilities_net_minority_interest, compact=True)}")

    # Equity Section
    logger.print_section("Stockholders' Equity")
    logger.print_bullet(f"Common Stock: {formatter.format_currency(balance_data.common_stock, compact=True)}")
    logger.print_bullet(f"Capital Stock: {formatter.format_currency(balance_data.capital_stock, compact=True)}")
    logger.print_bullet(f"Retained Earnings: {formatter.format_currency(balance_data.retained_earnings, compact=True)}")
    logger.print_bullet(f"Other Equity Adjustments: {formatter.format_currency(balance_data.other_equity_adjustments, compact=True)}")
    logger.print_bullet(f"Gains Losses Not Affecting Retained Earnings: {formatter.format_currency(balance_data.gains_losses_not_affecting_retained_earnings, compact=True)}")
    logger.print_bullet(f"Stockholders Equity: {formatter.format_currency(balance_data.stockholders_equity, compact=True)}")
    logger.print_bullet(f"Total Equity Gross Minority Interest: {formatter.format_currency(balance_data.total_equity_gross_minority_interest, compact=True)}")
    logger.print_bullet(f"Total Capitalization: {formatter.format_currency(balance_data.total_capitalization, compact=True)}")
    logger.print_bullet(f"Common Stock Equity: {formatter.format_currency(balance_data.common_stock_equity, compact=True)}")

    # Key Metrics Section
    logger.print_section("Key Metrics")
    logger.print_bullet(f"Capital Lease Obligations: {formatter.format_currency(balance_data.capital_lease_obligations, compact=True)}")
    logger.print_bullet(f"Net Tangible Assets: {formatter.format_currency(balance_data.net_tangible_assets, compact=True)}")
    logger.print_bullet(f"Working Capital: {formatter.format_currency(balance_data.working_capital, compact=True)}")
    logger.print_bullet(f"Invested Capital: {formatter.format_currency(balance_data.invested_capital, compact=True)}")
    logger.print_bullet(f"Tangible Book Value: {formatter.format_currency(balance_data.tangible_book_value, compact=True)}")
    logger.print_bullet(f"Total Debt: {formatter.format_currency(balance_data.total_debt, compact=True)}")
    logger.print_bullet(f"Net Debt: {formatter.format_currency(balance_data.net_debt, compact=True)}")