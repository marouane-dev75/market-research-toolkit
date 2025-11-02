"""
Cash Flow Statement Fetcher Module

This module provides functionality to fetch and display cash flow statement data
from financial APIs using yfinance.
"""

from dataclasses import dataclass
from typing import Optional
import yfinance as yf
from ....interfaces.console.logger import get_logger, FinancialFormatter
from ..enums import DataFrequency
from ....infrastructure.cache.manager import get_cache_manager


@dataclass
class CashFlowData:
    """
    Dataclass representing cash flow statement data for a ticker.

    All financial values are in the currency of the company's reporting.
    Values may be None if not available from the data source.
    """

    # Metadata
    ticker: str
    frequency: DataFrequency
    period_end_date: Optional[str] = None

    # Operating Activities
    net_income_from_continuing_operations: Optional[float] = None
    depreciation_and_amortization: Optional[float] = None
    depreciation_amortization_depletion: Optional[float] = None
    deferred_income_tax: Optional[float] = None
    deferred_tax: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    other_non_cash_items: Optional[float] = None
    
    # Changes in Working Capital
    change_in_working_capital: Optional[float] = None
    changes_in_account_receivables: Optional[float] = None
    change_in_receivables: Optional[float] = None
    change_in_inventory: Optional[float] = None
    change_in_account_payable: Optional[float] = None
    change_in_payable: Optional[float] = None
    change_in_payables_and_accrued_expense: Optional[float] = None
    change_in_other_current_assets: Optional[float] = None
    change_in_other_current_liabilities: Optional[float] = None
    change_in_other_working_capital: Optional[float] = None
    
    # Operating Cash Flow
    operating_cash_flow: Optional[float] = None
    cash_flow_from_continuing_operating_act: Optional[float] = None

    # Investing Activities
    capital_expenditure: Optional[float] = None
    purchase_of_ppe: Optional[float] = None
    net_ppe_purchase_and_sale: Optional[float] = None
    purchase_of_business: Optional[float] = None
    net_business_purchase_and_sale: Optional[float] = None
    purchase_of_investment: Optional[float] = None
    sale_of_investment: Optional[float] = None
    net_investment_purchase_and_sale: Optional[float] = None
    net_other_investing_changes: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    cash_flow_from_continuing_investing_act: Optional[float] = None

    # Financing Activities
    long_term_debt_issuance: Optional[float] = None
    long_term_debt_payments: Optional[float] = None
    net_long_term_debt_issuance: Optional[float] = None
    net_short_term_debt_issuance: Optional[float] = None
    net_issuance_payments_of_debt: Optional[float] = None
    common_stock_issuance: Optional[float] = None
    common_stock_payments: Optional[float] = None
    net_common_stock_issuance: Optional[float] = None
    common_stock_dividend_paid: Optional[float] = None
    cash_dividends_paid: Optional[float] = None
    net_other_financing_charges: Optional[float] = None
    cash_flow_from_continuing_financing_act: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    issuance_of_capital_stock: Optional[float] = None
    issuance_of_debt: Optional[float] = None
    repayment_of_debt: Optional[float] = None
    repurchase_of_capital_stock: Optional[float] = None

    # Summary
    changes_in_cash: Optional[float] = None
    beginning_cash_position: Optional[float] = None
    end_cash_position: Optional[float] = None
    free_cash_flow: Optional[float] = None
    
    # Supplemental Data
    income_tax_paid_supplemental_data: Optional[float] = None
    interest_paid_supplemental_data: Optional[float] = None


class CashFlowFetcher:
    """
    Fetcher class for retrieving and processing cash flow statement data.

    This class handles fetching financial data from yfinance and mapping it
    to the CashFlowData dataclass structure.
    """

    def __init__(self):
        """Initialize the fetcher with a logger instance."""
        self.logger = get_logger()
        self.cache_manager = get_cache_manager()

    def fetch_cash_flow(
        self,
        ticker_symbol: str,
        frequency: DataFrequency
    ) -> list[CashFlowData]:
        """
        Fetch cash flow statement data for a given ticker and frequency.

        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
            frequency: Data frequency (YEARLY or QUARTERLY)

        Returns:
            List of CashFlowData objects, one for each period

        Raises:
            ValueError: If ticker is invalid or data cannot be fetched
        """
        try:
            self.logger.debug(f"Fetching {frequency.value} cash flow for {ticker_symbol}")

            # Try to get data from cache first
            cached_data = self.cache_manager.get_cached_data(
                ticker=ticker_symbol,
                data_type='cash_flows',
                frequency=frequency.value
            )
            
            if cached_data is not None:
                self.logger.info(f"Using cached {frequency.value} cash flow for {ticker_symbol}")
                return cached_data

            # Cache miss - fetch from API
            self.logger.info(f"Cache miss - fetching {frequency.value} cash flow from API for {ticker_symbol}")

            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Fetch cash flow based on frequency
            if frequency == DataFrequency.YEARLY:
                cashflow_df = ticker.cashflow
            else:  # QUARTERLY
                cashflow_df = ticker.quarterly_cashflow

            # Check if data was retrieved
            if cashflow_df is None or cashflow_df.empty:
                raise ValueError(f"No cash flow data available for {ticker_symbol}")

            # Map dataframe to list of CashFlowData objects
            cashflow_data = self._map_to_dataclass(ticker_symbol, frequency, cashflow_df)
            
            # Store in cache
            cache_success = self.cache_manager.store_cached_data(
                data=cashflow_data,
                ticker=ticker_symbol,
                data_type='cash_flows',
                frequency=frequency.value
            )
            
            if cache_success:
                self.logger.debug(f"Successfully cached {frequency.value} cash flow for {ticker_symbol}")
            else:
                self.logger.debug(f"Failed to cache {frequency.value} cash flow for {ticker_symbol}")
            
            return cashflow_data

        except Exception as e:
            self.logger.error(f"Failed to fetch cash flow: {str(e)}")
            raise

    def _map_to_dataclass(
        self,
        ticker_symbol: str,
        frequency: DataFrequency,
        cashflow_df
    ) -> list[CashFlowData]:
        """
        Map pandas DataFrame to list of CashFlowData objects.

        Args:
            ticker_symbol: Stock ticker symbol
            frequency: Data frequency
            cashflow_df: Pandas DataFrame with cash flow data

        Returns:
            List of CashFlowData objects
        """
        cash_flows = []

        # Iterate through each column (each column represents a period)
        for period_date in cashflow_df.columns:
            period_data = cashflow_df[period_date]

            # Helper function to safely get values
            def get_value(key: str) -> Optional[float]:
                try:
                    if key in period_data.index:
                        val = period_data[key]
                        return float(val) if val is not None else None
                    return None
                except (ValueError, TypeError):
                    return None

            # Create CashFlowData object
            statement = CashFlowData(
                ticker=ticker_symbol,
                frequency=frequency,
                period_end_date=str(period_date.date()),

                # Operating Activities
                net_income_from_continuing_operations=get_value("Net Income From Continuing Operations"),
                depreciation_and_amortization=get_value("Depreciation And Amortization"),
                depreciation_amortization_depletion=get_value("Depreciation Amortization Depletion"),
                deferred_income_tax=get_value("Deferred Income Tax"),
                deferred_tax=get_value("Deferred Tax"),
                stock_based_compensation=get_value("Stock Based Compensation"),
                other_non_cash_items=get_value("Other Non Cash Items"),
                
                # Changes in Working Capital
                change_in_working_capital=get_value("Change In Working Capital"),
                changes_in_account_receivables=get_value("Changes In Account Receivables"),
                change_in_receivables=get_value("Change In Receivables"),
                change_in_inventory=get_value("Change In Inventory"),
                change_in_account_payable=get_value("Change In Account Payable"),
                change_in_payable=get_value("Change In Payable"),
                change_in_payables_and_accrued_expense=get_value("Change In Payables And Accrued Expense"),
                change_in_other_current_assets=get_value("Change In Other Current Assets"),
                change_in_other_current_liabilities=get_value("Change In Other Current Liabilities"),
                change_in_other_working_capital=get_value("Change In Other Working Capital"),
                
                # Operating Cash Flow
                operating_cash_flow=get_value("Operating Cash Flow"),
                cash_flow_from_continuing_operating_act=get_value("Cash Flow From Continuing Operating Act"),

                # Investing Activities
                capital_expenditure=get_value("Capital Expenditure"),
                purchase_of_ppe=get_value("Purchase Of PPE"),
                net_ppe_purchase_and_sale=get_value("Net PPE Purchase And Sale"),
                purchase_of_business=get_value("Purchase Of Business"),
                net_business_purchase_and_sale=get_value("Net Business Purchase And Sale"),
                purchase_of_investment=get_value("Purchase Of Investment"),
                sale_of_investment=get_value("Sale Of Investment"),
                net_investment_purchase_and_sale=get_value("Net Investment Purchase And Sale"),
                net_other_investing_changes=get_value("Net Other Investing Changes"),
                investing_cash_flow=get_value("Investing Cash Flow"),
                cash_flow_from_continuing_investing_act=get_value("Cash Flow From Continuing Investing Act"),

                # Financing Activities
                long_term_debt_issuance=get_value("Long Term Debt Issuance"),
                long_term_debt_payments=get_value("Long Term Debt Payments"),
                net_long_term_debt_issuance=get_value("Net Long Term Debt Issuance"),
                net_short_term_debt_issuance=get_value("Net Short Term Debt Issuance"),
                net_issuance_payments_of_debt=get_value("Net Issuance Payments Of Debt"),
                common_stock_issuance=get_value("Common Stock Issuance"),
                common_stock_payments=get_value("Common Stock Payments"),
                net_common_stock_issuance=get_value("Net Common Stock Issuance"),
                common_stock_dividend_paid=get_value("Common Stock Dividend Paid"),
                cash_dividends_paid=get_value("Cash Dividends Paid"),
                net_other_financing_charges=get_value("Net Other Financing Charges"),
                cash_flow_from_continuing_financing_act=get_value("Cash Flow From Continuing Financing Act"),
                financing_cash_flow=get_value("Financing Cash Flow"),
                issuance_of_capital_stock=get_value("Issuance Of Capital Stock"),
                issuance_of_debt=get_value("Issuance Of Debt"),
                repayment_of_debt=get_value("Repayment Of Debt"),
                repurchase_of_capital_stock=get_value("Repurchase Of Capital Stock"),

                # Summary
                changes_in_cash=get_value("Changes In Cash"),
                beginning_cash_position=get_value("Beginning Cash Position"),
                end_cash_position=get_value("End Cash Position"),
                free_cash_flow=get_value("Free Cash Flow"),
                
                # Supplemental Data
                income_tax_paid_supplemental_data=get_value("Income Tax Paid Supplemental Data"),
                interest_paid_supplemental_data=get_value("Interest Paid Supplemental Data"),
            )

            cash_flows.append(statement)

        return cash_flows


def display_cash_flow(cash_flow_data: CashFlowData) -> None:
    """
    Display cash flow statement data in a formatted console output.

    This function is completely independent and does not fetch data.
    It only displays the provided CashFlowData object.

    Args:
        cash_flow_data: CashFlowData object to display
    """
    logger = get_logger()
    formatter = FinancialFormatter()

    # Display header
    logger.print_header(f"Cash Flow Statement - {cash_flow_data.ticker}")

    # Display metadata
    logger.print_section("Period Information")
    logger.print_bullet(f"Frequency: {cash_flow_data.frequency.value.capitalize()}")
    logger.print_bullet(f"Period End Date: {cash_flow_data.period_end_date or 'N/A'}")

    # Operating Activities Section
    logger.print_section("Operating Activities")
    logger.print_bullet(f"Net Income (Continuing Operations): {formatter.format_currency(cash_flow_data.net_income_from_continuing_operations, compact=True)}")
    logger.print_bullet(f"Depreciation & Amortization: {formatter.format_currency(cash_flow_data.depreciation_and_amortization or cash_flow_data.depreciation_amortization_depletion, compact=True)}")
    logger.print_bullet(f"Stock Based Compensation: {formatter.format_currency(cash_flow_data.stock_based_compensation, compact=True)}")
    logger.print_bullet(f"Deferred Income Tax: {formatter.format_currency(cash_flow_data.deferred_income_tax or cash_flow_data.deferred_tax, compact=True)}")
    logger.print_bullet(f"Other Non-Cash Items: {formatter.format_currency(cash_flow_data.other_non_cash_items, compact=True)}")

    # Working Capital Changes
    logger.print_section("Changes in Working Capital")
    logger.print_bullet(f"Total Changes in Working Capital: {formatter.format_currency(cash_flow_data.change_in_working_capital, compact=True)}")
    logger.print_bullet(f"Change in Receivables: {formatter.format_currency(cash_flow_data.changes_in_account_receivables or cash_flow_data.change_in_receivables, compact=True)}")
    logger.print_bullet(f"Change in Inventory: {formatter.format_currency(cash_flow_data.change_in_inventory, compact=True)}")
    logger.print_bullet(f"Change in Payables: {formatter.format_currency(cash_flow_data.change_in_account_payable or cash_flow_data.change_in_payable, compact=True)}")
    logger.print_bullet(f"Change in Payables & Accrued Expense: {formatter.format_currency(cash_flow_data.change_in_payables_and_accrued_expense, compact=True)}")
    logger.print_bullet(f"Change in Other Current Assets: {formatter.format_currency(cash_flow_data.change_in_other_current_assets, compact=True)}")
    logger.print_bullet(f"Change in Other Current Liabilities: {formatter.format_currency(cash_flow_data.change_in_other_current_liabilities, compact=True)}")
    logger.print_bullet(f"Change in Other Working Capital: {formatter.format_currency(cash_flow_data.change_in_other_working_capital, compact=True)}")

    # Operating Cash Flow Total
    logger.print_section("Operating Cash Flow")
    logger.print_bullet(f"Operating Cash Flow: {formatter.format_currency(cash_flow_data.operating_cash_flow, compact=True)}")
    logger.print_bullet(f"Cash Flow From Continuing Operating Activities: {formatter.format_currency(cash_flow_data.cash_flow_from_continuing_operating_act, compact=True)}")

    # Investing Activities Section
    logger.print_section("Investing Activities")
    logger.print_bullet(f"Capital Expenditure: {formatter.format_currency(cash_flow_data.capital_expenditure, compact=True)}")
    logger.print_bullet(f"Purchase of PPE: {formatter.format_currency(cash_flow_data.purchase_of_ppe, compact=True)}")
    logger.print_bullet(f"Net PPE Purchase & Sale: {formatter.format_currency(cash_flow_data.net_ppe_purchase_and_sale, compact=True)}")
    logger.print_bullet(f"Purchase of Business: {formatter.format_currency(cash_flow_data.purchase_of_business, compact=True)}")
    logger.print_bullet(f"Net Business Purchase & Sale: {formatter.format_currency(cash_flow_data.net_business_purchase_and_sale, compact=True)}")
    logger.print_bullet(f"Purchase of Investment: {formatter.format_currency(cash_flow_data.purchase_of_investment, compact=True)}")
    logger.print_bullet(f"Sale of Investment: {formatter.format_currency(cash_flow_data.sale_of_investment, compact=True)}")
    logger.print_bullet(f"Net Investment Purchase & Sale: {formatter.format_currency(cash_flow_data.net_investment_purchase_and_sale, compact=True)}")
    logger.print_bullet(f"Other Investing Changes: {formatter.format_currency(cash_flow_data.net_other_investing_changes, compact=True)}")
    logger.print_bullet(f"Total Investing Cash Flow: {formatter.format_currency(cash_flow_data.investing_cash_flow, compact=True)}")

    # Financing Activities Section
    logger.print_section("Financing Activities")
    logger.print_bullet(f"Long Term Debt Issuance: {formatter.format_currency(cash_flow_data.long_term_debt_issuance, compact=True)}")
    logger.print_bullet(f"Long Term Debt Payments: {formatter.format_currency(cash_flow_data.long_term_debt_payments, compact=True)}")
    logger.print_bullet(f"Net Long Term Debt Issuance: {formatter.format_currency(cash_flow_data.net_long_term_debt_issuance, compact=True)}")
    logger.print_bullet(f"Net Short Term Debt Issuance: {formatter.format_currency(cash_flow_data.net_short_term_debt_issuance, compact=True)}")
    logger.print_bullet(f"Net Issuance/Payments of Debt: {formatter.format_currency(cash_flow_data.net_issuance_payments_of_debt, compact=True)}")
    logger.print_bullet(f"Common Stock Issuance: {formatter.format_currency(cash_flow_data.common_stock_issuance, compact=True)}")
    logger.print_bullet(f"Common Stock Payments: {formatter.format_currency(cash_flow_data.common_stock_payments, compact=True)}")
    logger.print_bullet(f"Net Common Stock Issuance: {formatter.format_currency(cash_flow_data.net_common_stock_issuance, compact=True)}")
    logger.print_bullet(f"Cash Dividends Paid: {formatter.format_currency(cash_flow_data.cash_dividends_paid, compact=True)}")
    logger.print_bullet(f"Common Stock Dividend Paid: {formatter.format_currency(cash_flow_data.common_stock_dividend_paid, compact=True)}")
    logger.print_bullet(f"Issuance of Capital Stock: {formatter.format_currency(cash_flow_data.issuance_of_capital_stock, compact=True)}")
    logger.print_bullet(f"Repurchase of Capital Stock: {formatter.format_currency(cash_flow_data.repurchase_of_capital_stock, compact=True)}")
    logger.print_bullet(f"Issuance of Debt: {formatter.format_currency(cash_flow_data.issuance_of_debt, compact=True)}")
    logger.print_bullet(f"Repayment of Debt: {formatter.format_currency(cash_flow_data.repayment_of_debt, compact=True)}")
    logger.print_bullet(f"Other Financing Changes: {formatter.format_currency(cash_flow_data.net_other_financing_charges, compact=True)}")
    logger.print_bullet(f"Total Financing Cash Flow: {formatter.format_currency(cash_flow_data.financing_cash_flow, compact=True)}")

    # Summary Section
    logger.print_section("Cash Flow Summary")
    logger.print_bullet(f"Beginning Cash Position: {formatter.format_currency(cash_flow_data.beginning_cash_position, compact=True)}")
    logger.print_bullet(f"Net Change in Cash: {formatter.format_currency(cash_flow_data.changes_in_cash, compact=True)}")
    logger.print_bullet(f"Ending Cash Position: {formatter.format_currency(cash_flow_data.end_cash_position, compact=True)}")

    # Key Metrics Section
    logger.print_section("Key Metrics")
    logger.print_bullet(f"Free Cash Flow: {formatter.format_currency(cash_flow_data.free_cash_flow, compact=True)}")
    
    # Supplemental Data Section
    logger.print_section("Supplemental Data")
    logger.print_bullet(f"Income Tax Paid: {formatter.format_currency(cash_flow_data.income_tax_paid_supplemental_data, compact=True)}")
    logger.print_bullet(f"Interest Paid: {formatter.format_currency(cash_flow_data.interest_paid_supplemental_data, compact=True)}")