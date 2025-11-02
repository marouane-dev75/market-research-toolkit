"""
Magic Formula Fetcher Module

This module implements Joel Greenblatt's Magic Formula from "The Little Book That Beats the Market".
The Magic Formula ranks stocks based on two key metrics:
1. Earnings Yield (EBIT / Enterprise Value) - Higher is better
2. Return on Capital (EBIT / Invested Capital) - Higher is better

The formula combines these rankings to identify undervalued companies with high returns on capital.
"""

from typing import List
from src.ticker_analysis.interfaces.console.logger import get_logger
from src.ticker_analysis.core.data.fetchers import (
    CompanyInfoFetcher,
    IncomeStatementFetcher,
    BalanceSheetFetcher,
    DataFrequency
)
from .calculator import MagicFormulaData, MagicFormulaCalculator


class MagicFormulaFetcher:
    """
    Fetcher class for implementing Joel Greenblatt's Magic Formula screening.
    
    This class fetches the required financial data and calculates the Magic Formula
    metrics to rank stocks based on earnings yield and return on capital.
    """
    
    def __init__(self, frequency: DataFrequency = DataFrequency.QUARTERLY):
        """Initialize the fetcher with required data fetchers.
        
        Args:
            frequency: Data frequency to use (quarterly or yearly), defaults to quarterly
        """
        self.logger = get_logger()
        self.company_fetcher = CompanyInfoFetcher()
        self.income_fetcher = IncomeStatementFetcher()
        self.balance_fetcher = BalanceSheetFetcher()
        self.calculator = MagicFormulaCalculator()
        self.frequency = frequency
    
    def screen_tickers(self, ticker_symbols: List[str]) -> List[MagicFormulaData]:
        """
        Screen a list of ticker symbols using the Magic Formula.
        
        Args:
            ticker_symbols: List of stock ticker symbols to screen
            
        Returns:
            List of MagicFormulaData objects ranked by Magic Formula score
        """
        self.logger.info(f"Starting Magic Formula screening for {len(ticker_symbols)} tickers...")
        
        # Fetch data for all tickers
        magic_formula_data = []
        for ticker in ticker_symbols:
            ticker = ticker.strip().upper()
            self.logger.debug(f"Processing ticker: {ticker}")
            
            try:
                data = self._fetch_ticker_data(ticker)
                magic_formula_data.append(data)
            except Exception as e:
                self.logger.warning(f"Failed to process {ticker}: {str(e)}")
                # Add ticker with missing data
                magic_formula_data.append(MagicFormulaData(
                    ticker=ticker,
                    has_complete_data=False,
                    missing_data_reason=f"Data fetch error: {str(e)}"
                ))
        
        # Filter out tickers with incomplete data
        valid_data = [data for data in magic_formula_data if data.has_complete_data]
        invalid_data = [data for data in magic_formula_data if not data.has_complete_data]
        
        if invalid_data:
            self.logger.warning(f"Skipping {len(invalid_data)} tickers due to missing data:")
            for data in invalid_data:
                self.logger.warning(f"  {data.ticker}: {data.missing_data_reason}")
        
        if not valid_data:
            self.logger.error("No valid data found for any tickers")
            return magic_formula_data
        
        # Calculate rankings and scores
        ranked_data = self.calculator.calculate_rankings(valid_data)
        
        # Combine valid and invalid data, with valid data first (sorted by score)
        result = ranked_data + invalid_data
        
        self.logger.success(f"Magic Formula screening completed. {len(ranked_data)} tickers ranked successfully.")
        
        return result
    
    def _fetch_ticker_data(self, ticker: str) -> MagicFormulaData:
        """
        Fetch required financial data for a single ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            MagicFormulaData object with fetched data
        """
        data = MagicFormulaData(ticker=ticker)
        
        try:
            # Fetch company info for enterprise value and company name
            self.logger.debug(f"Fetching company info for {ticker}")
            company_info = self.company_fetcher.fetch_company_info(ticker)
            data.company_name = company_info.company_name
            data.enterprise_value = company_info.enterprise_value
            
            # Fetch income statement for EBIT
            self.logger.debug(f"Fetching {self.frequency.value} income statement for {ticker}")
            income_statements = self.income_fetcher.fetch_income_statement(ticker, self.frequency)
            if income_statements:
                # Use the most recent quarter
                latest_income = income_statements[0]
                data.ebit = latest_income.ebit
            
            # Fetch balance sheet for invested capital
            self.logger.debug(f"Fetching {self.frequency.value} balance sheet for {ticker}")
            balance_sheets = self.balance_fetcher.fetch_balance_sheet(ticker, self.frequency)
            if balance_sheets:
                # Use the most recent quarter
                latest_balance = balance_sheets[0]
                data.invested_capital = latest_balance.invested_capital
            
            # Calculate metrics using the calculator
            data = self.calculator.calculate_metrics(data)
            
            if data.has_complete_data:
                self.logger.debug(f"{ticker} - Earnings Yield: {data.earnings_yield:.4f}, Return on Capital: {data.return_on_capital:.4f}")
        
        except Exception as e:
            data.missing_data_reason = f"Data fetch error: {str(e)}"
            data.has_complete_data = False
            raise
        
        return data
    