"""
Company Data Models

This module contains data models for general company financial analysis.
"""

from dataclasses import dataclass
from typing import Optional
from ..data.fetchers.company_info import CompanyInfoData
from .dividend import DividendAnalysisData
from .income_statement import IncomeStatementMetrics, TrendAnalysis, FinancialHealthAssessment
from .balance_sheet import BalanceSheetMetrics, BalanceSheetTrendAnalysis, BalanceSheetHealthAssessment
from .cash_flow import CashFlowMetrics, CashFlowTrendAnalysis, CashFlowHealthAssessment
from .price import PriceAnalysisData
from .technical import TechnicalIndicators


@dataclass
class CompanyAnalysisData:
    """
    Dataclass representing comprehensive analysis information for a ticker.
    
    This extends the basic CompanyInfoData with additional metrics
    and provides a clean interface for company analysis and reporting.
    """
    
    # Basic Information
    ticker: str
    exchange: Optional[str] = None
    sector: Optional[str] = None
    
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
    
    # External Analysis Sentiment (renamed from Analyst Data)
    recommendation: Optional[str] = None
    target_price: Optional[float] = None
    
    # Future company-specific metrics (placeholders for evolution)
    # These can be added later as the command evolves
    funds_from_operations: Optional[float] = None  # FFO (primarily for real estate companies)
    adjusted_funds_from_operations: Optional[float] = None  # AFFO (primarily for real estate companies)
    net_asset_value: Optional[float] = None  # NAV (primarily for real estate companies)
    occupancy_rate: Optional[float] = None  # For real estate companies
    
    # Dividend Analysis
    dividend_analysis: Optional[DividendAnalysisData] = None
    
    # Income Statement Analysis
    income_statement_metrics: Optional[IncomeStatementMetrics] = None
    trend_analysis: Optional[TrendAnalysis] = None
    financial_health_assessment: Optional[FinancialHealthAssessment] = None
    
    # Balance Sheet Analysis
    balance_sheet_metrics: Optional[BalanceSheetMetrics] = None
    balance_sheet_trends: Optional[BalanceSheetTrendAnalysis] = None
    balance_sheet_health: Optional[BalanceSheetHealthAssessment] = None
    
    # Cash Flow Analysis
    cash_flow_metrics: Optional[CashFlowMetrics] = None
    cash_flow_trends: Optional[CashFlowTrendAnalysis] = None
    cash_flow_health: Optional[CashFlowHealthAssessment] = None
    
    # Price Analysis
    price_analysis: Optional[PriceAnalysisData] = None
    
    # Technical Analysis
    technical_analysis: Optional[TechnicalIndicators] = None
    
    @classmethod
    def from_company_info(
        cls,
        company_info: CompanyInfoData,
        dividend_analysis: Optional[DividendAnalysisData] = None,
        income_statement_metrics: Optional[IncomeStatementMetrics] = None,
        trend_analysis: Optional[TrendAnalysis] = None,
        financial_health_assessment: Optional[FinancialHealthAssessment] = None,
        balance_sheet_metrics: Optional[BalanceSheetMetrics] = None,
        balance_sheet_trends: Optional[BalanceSheetTrendAnalysis] = None,
        balance_sheet_health: Optional[BalanceSheetHealthAssessment] = None,
        cash_flow_metrics: Optional[CashFlowMetrics] = None,
        cash_flow_trends: Optional[CashFlowTrendAnalysis] = None,
        cash_flow_health: Optional[CashFlowHealthAssessment] = None,
        price_analysis: Optional[PriceAnalysisData] = None,
        technical_analysis: Optional[TechnicalIndicators] = None
    ) -> 'CompanyAnalysisData':
        """
        Create CompanyAnalysisData from CompanyInfoData and analysis components.
        
        Args:
            company_info: CompanyInfoData object from the fetcher
            dividend_analysis: Optional dividend analysis data
            income_statement_metrics: Optional latest quarter income statement metrics
            trend_analysis: Optional 3-year trend analysis
            financial_health_assessment: Optional financial health assessment
            balance_sheet_metrics: Optional latest quarter balance sheet metrics
            balance_sheet_trends: Optional 3-year balance sheet trend analysis
            balance_sheet_health: Optional balance sheet health assessment
            cash_flow_metrics: Optional latest quarter cash flow metrics
            cash_flow_trends: Optional 3-year cash flow trend analysis
            cash_flow_health: Optional cash flow health assessment
            price_analysis: Optional price analysis data with percentage changes
            technical_analysis: Optional technical indicators and analysis
            
        Returns:
            CompanyAnalysisData object with mapped values
        """
        return cls(
            # Basic Information (minimal)
            ticker=company_info.ticker,
            exchange=company_info.exchange,
            sector=company_info.sector,
            
            # Market Data
            last_price=company_info.last_price,
            market_cap=company_info.market_cap,
            last_volume=company_info.last_volume,
            avg_volume=company_info.avg_volume,
            fifty_two_week_high=company_info.fifty_two_week_high,
            fifty_two_week_low=company_info.fifty_two_week_low,
            
            # Valuation Metrics
            pe_ratio=company_info.pe_ratio,
            forward_pe=company_info.forward_pe,
            pb_ratio=company_info.pb_ratio,
            price_to_sales=company_info.price_to_sales,
            enterprise_value=company_info.enterprise_value,
            ev_to_revenue=company_info.ev_to_revenue,
            ev_to_ebitda=company_info.ev_to_ebitda,
            dividend_yield=company_info.dividend_yield,
            beta=company_info.beta,
            
            # Financial Metrics
            profit_margins=company_info.profit_margins,
            operating_margins=company_info.operating_margins,
            return_on_assets=company_info.return_on_assets,
            return_on_equity=company_info.return_on_equity,
            debt_to_equity=company_info.debt_to_equity,
            current_ratio=company_info.current_ratio,
            quick_ratio=company_info.quick_ratio,
            revenue_growth=company_info.revenue_growth,
            earnings_growth=company_info.earnings_growth,
            
            # External Analysis Sentiment
            recommendation=company_info.recommendation,
            target_price=company_info.target_price,
            
            # Company-specific metrics (None for now, will be populated later)
            funds_from_operations=None,
            adjusted_funds_from_operations=None,
            net_asset_value=None,
            occupancy_rate=None,
            
            # Dividend Analysis
            dividend_analysis=dividend_analysis,
            
            # Income Statement Analysis
            income_statement_metrics=income_statement_metrics,
            trend_analysis=trend_analysis,
            financial_health_assessment=financial_health_assessment,
            
            # Balance Sheet Analysis
            balance_sheet_metrics=balance_sheet_metrics,
            balance_sheet_trends=balance_sheet_trends,
            balance_sheet_health=balance_sheet_health,
            
            # Cash Flow Analysis
            cash_flow_metrics=cash_flow_metrics,
            cash_flow_trends=cash_flow_trends,
            cash_flow_health=cash_flow_health,
            
            # Price Analysis
            price_analysis=price_analysis,
            
            # Technical Analysis
            technical_analysis=technical_analysis
        )