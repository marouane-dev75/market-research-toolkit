"""
Magic Formula Display Module

This module handles the console output and formatting for Magic Formula screening results.
Provides formatted display of rankings, metrics, and analysis results.
"""

from typing import List
from src.ticker_analysis.interfaces.console.logger import get_logger, FinancialFormatter
from src.ticker_analysis.interfaces.console.formatter import ConsoleFormatter
from src.ticker_analysis.core.data.fetchers import DataFrequency
from .calculator import MagicFormulaData


def display_magic_formula_results(results: List[MagicFormulaData], frequency: DataFrequency = DataFrequency.QUARTERLY) -> None:
    """
    Display Magic Formula screening results in a formatted console output.
    
    Args:
        results: List of MagicFormulaData objects to display
        frequency: Data frequency used for the analysis
    """
    logger = get_logger()
    formatter = FinancialFormatter()
    console_formatter = ConsoleFormatter()
    
    # Display header
    logger.print_header("Magic Formula Stock Screening Results")
    
    # Separate valid and invalid results
    valid_results = [r for r in results if r.has_complete_data]
    invalid_results = [r for r in results if not r.has_complete_data]
    
    if valid_results:
        logger.print_section("RANKED STOCKS (by Magic Formula Score)")
        logger.print_bullet("Lower scores are better. Score = Earnings Yield Rank + Return on Capital Rank")
        logger.print_bullet("")
        
        # Define column widths and alignments
        column_widths = [4, 8, 25, 8, 8, 8, 9, 5]
        column_alignments = ['left', 'left', 'left', 'right', 'right', 'right', 'right', 'right']
        
        # Display table header
        header_columns = ['Rank', 'Ticker', 'Company', 'EY', 'ROC', 'EY Rank', 'ROC Rank', 'Score']
        header_row = console_formatter.format_table_row(header_columns, column_widths, column_alignments)
        logger.print_bullet(header_row)
        
        # Create separator line based on actual display width
        separator_width = sum(column_widths) + len(column_widths) - 1  # Add spaces between columns
        logger.print_bullet("-" * separator_width)
        
        # Display each ranked stock
        for data in valid_results:
            company_name = (data.company_name or "N/A")[:24]  # Truncate long names
            
            # Format data columns
            columns = [
                str(data.combined_rank),
                data.ticker,
                company_name,
                formatter.format_percentage(data.earnings_yield),
                formatter.format_percentage(data.return_on_capital),
                str(data.earnings_yield_rank),
                str(data.return_on_capital_rank),
                f"{data.magic_formula_score:.0f}"
            ]
            
            # Format the row with proper ANSI-aware alignment
            row = console_formatter.format_table_row(columns, column_widths, column_alignments)
            logger.print_bullet(row)
        
        logger.print_section("LEGEND")
        logger.print_bullet("EY = Earnings Yield (EBIT / Enterprise Value)")
        logger.print_bullet("ROC = Return on Capital (EBIT / Invested Capital)")
        logger.print_bullet("EY Rank = Earnings Yield ranking (1 = highest)")
        logger.print_bullet("ROC Rank = Return on Capital ranking (1 = highest)")
        logger.print_bullet("Score = Combined ranking (lower is better)")
    
    if invalid_results:
        logger.print_section("EXCLUDED STOCKS (Missing Data)")
        for data in invalid_results:
            logger.print_bullet(f"{data.ticker}: {data.missing_data_reason}")
    
    if not valid_results and not invalid_results:
        logger.warning("No data to display")
    
    logger.print_section("MAGIC FORMULA METHODOLOGY")
    logger.print_bullet("Based on Joel Greenblatt's 'The Little Book That Beats the Market'")
    logger.print_bullet("Ranks stocks by Earnings Yield and Return on Capital")
    logger.print_bullet("Lower combined scores indicate better Magic Formula candidates")
    logger.print_bullet(f"Uses latest {frequency.value} financial data")