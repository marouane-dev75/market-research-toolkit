"""
PDF Analysis Formatters Module

This module provides PDF formatting functionality for comprehensive company analysis,
including configurable formatters and a main PDF aggregator.
"""

from .base_formatter import BasePDFFormatter, PDFColors, PDFFonts
from .generic_metrics_formatter import GenericMetricsFormatter
from .pdf_formatter import PDFFormatter
from .income_statement_formatter import IncomeStatementFormatter
from .balance_sheet_formatter import BalanceSheetFormatter
from .cash_flow_formatter import CashFlowFormatter
from .technical_formatter import TechnicalFormatter

__all__ = [
    'PDFFormatter'
]
