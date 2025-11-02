
"""
Balance Sheet Analysis Module for Company Financial Health Assessment

This module provides balance sheet analysis functionality including quarterly metrics extraction,
yearly trend analysis, and financial health assessment focused on liquidity, leverage, and asset quality.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
from ..data.fetchers.balance_sheet import BalanceSheetData
from ..data.enums import DataFrequency
from .income_statement import FinancialHealthRating, TrendDirection


@dataclass
class BalanceSheetMetrics:
    """
    Dataclass representing key metrics extracted from the latest quarterly balance sheet.
    
    This focuses on liquidity, leverage, and asset quality metrics for financial health analysis.
    """
    
    # Metadata
    ticker: str
    quarter_end_date: Optional[str] = None
    
    # Liquidity Ratios
    current_ratio: Optional[float] = None  # Current Assets / Current Liabilities
    quick_ratio: Optional[float] = None    # (Current Assets - Inventory) / Current Liabilities
    cash_ratio: Optional[float] = None     # Cash & Equivalents / Current Liabilities
    
    # Leverage Ratios
    debt_to_equity: Optional[float] = None      # Total Debt / Total Equity
    debt_to_assets: Optional[float] = None      # Total Debt / Total Assets
    equity_ratio: Optional[float] = None        # Total Equity / Total Assets
    
    # Asset Quality Metrics
    tangible_book_value_per_share: Optional[float] = None
    working_capital: Optional[float] = None
    net_tangible_assets: Optional[float] = None
    
    # Financial Strength Indicators
    cash_and_equivalents: Optional[float] = None
    total_debt: Optional[float] = None
    total_equity: Optional[float] = None
    total_assets: Optional[float] = None
    
    # Asset Composition (percentages)
    current_assets_pct: Optional[float] = None      # Current Assets / Total Assets
    ppe_assets_pct: Optional[float] = None          # Net PPE / Total Assets
    cash_assets_pct: Optional[float] = None         # Cash / Total Assets


@dataclass
class YearlyBalanceSheetData:
    """
    Dataclass representing balance sheet data for a specific year.
    """
    year: int
    total_assets: Optional[float] = None
    total_debt: Optional[float] = None
    total_equity: Optional[float] = None
    working_capital: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    current_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    tangible_book_value: Optional[float] = None


@dataclass
class BalanceSheetTrendAnalysis:
    """
    Dataclass representing comprehensive balance sheet trend analysis over multiple years.
    
    Contains yearly data, growth rates, and trend assessments for key balance sheet metrics.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    years_analyzed: int
    
    # Historical Data
    yearly_data: List[YearlyBalanceSheetData]
    
    # Growth Rate Analysis (Year-over-Year percentages)
    assets_growth_rates: List[float]
    equity_growth_rates: List[float]
    debt_growth_rates: List[float]
    
    # Average Growth Rates
    avg_assets_growth: Optional[float] = None
    avg_equity_growth: Optional[float] = None
    avg_debt_growth: Optional[float] = None
    
    # Trend Direction Assessment
    assets_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    equity_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    debt_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    leverage_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    
    # Stability Metrics
    debt_to_equity_trend: List[float] = None
    current_ratio_trend: List[float] = None
    
    # Consistency Scores (0-10 scale)
    balance_sheet_stability_score: Optional[float] = None
    leverage_consistency_score: Optional[float] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.debt_to_equity_trend is None:
            self.debt_to_equity_trend = []
        if self.current_ratio_trend is None:
            self.current_ratio_trend = []


@dataclass
class BalanceSheetHealthAssessment:
    """
    Dataclass representing comprehensive balance sheet health assessment.
    
    Provides overall balance sheet strength rating and detailed analysis.
    """
    
    # Basic Information
    ticker: str
    assessment_date: str
    
    # Overall Balance Sheet Health
    overall_balance_sheet_rating: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    overall_balance_sheet_score: Optional[float] = None  # 0-10 scale
    
    # Component Ratings
    liquidity_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    leverage_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    asset_quality_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    financial_stability_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    
    # Component Scores (0-10 scale)
    liquidity_score: Optional[float] = None
    leverage_score: Optional[float] = None
    asset_quality_score: Optional[float] = None
    financial_stability_score: Optional[float] = None
    
    # Key Strengths and Concerns
    strengths: List[str] = None
    concerns: List[str] = None
    
    # Summary Assessment
    summary: Optional[str] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.strengths is None:
            self.strengths = []
        if self.concerns is None:
            self.concerns = []


class BalanceSheetAnalyzer:
    """
    Analyzer class for processing balance sheet data and generating comprehensive financial analysis.
    
    This class takes raw balance sheet data and produces quarterly metrics, trend analysis,
    and financial health assessments focused on balance sheet strength.
    """
    
    def __init__(self):
        """Initialize the balance sheet analyzer."""
        pass
    
    def analyze_latest_quarter(self, quarterly_data: List[BalanceSheetData]) -> Optional[BalanceSheetMetrics]:
        """
        Analyze the latest quarterly balance sheet data and extract key metrics.
        
        Args:
            quarterly_data: List of BalanceSheetData objects (quarterly frequency)
            
        Returns:
            BalanceSheetMetrics object with latest quarter analysis, or None if insufficient data
        """
        if not quarterly_data:
            return None
            
        # Get the most recent quarter (first in the list)
        latest_quarter = quarterly_data[0]
        
        # Calculate liquidity ratios
        current_ratio = self._calculate_current_ratio(latest_quarter)
        quick_ratio = self._calculate_quick_ratio(latest_quarter)
        cash_ratio = self._calculate_cash_ratio(latest_quarter)
        
        # Calculate leverage ratios
        debt_to_equity = self._calculate_debt_to_equity(latest_quarter)
        debt_to_assets = self._calculate_debt_to_assets(latest_quarter)
        equity_ratio = self._calculate_equity_ratio(latest_quarter)
        
        # Calculate asset composition percentages
        current_assets_pct = self._calculate_current_assets_percentage(latest_quarter)
        ppe_assets_pct = self._calculate_ppe_percentage(latest_quarter)
        cash_assets_pct = self._calculate_cash_percentage(latest_quarter)
        
        # Calculate tangible book value per share
        tbv_per_share = self._calculate_tangible_book_value_per_share(latest_quarter)
        
        return BalanceSheetMetrics(
            ticker=latest_quarter.ticker,
            quarter_end_date=latest_quarter.period_end_date,
            
            # Liquidity ratios
            current_ratio=current_ratio,
            quick_ratio=quick_ratio,
            cash_ratio=cash_ratio,
            
            # Leverage ratios
            debt_to_equity=debt_to_equity,
            debt_to_assets=debt_to_assets,
            equity_ratio=equity_ratio,
            
            # Asset quality metrics
            tangible_book_value_per_share=tbv_per_share,
            working_capital=latest_quarter.working_capital,
            net_tangible_assets=latest_quarter.net_tangible_assets,
            
            # Financial strength indicators
            cash_and_equivalents=latest_quarter.cash_and_cash_equivalents,
            total_debt=latest_quarter.total_debt,
            total_equity=latest_quarter.stockholders_equity,
            total_assets=latest_quarter.total_assets,
            
            # Asset composition
            current_assets_pct=current_assets_pct,
            ppe_assets_pct=ppe_assets_pct,
            cash_assets_pct=cash_assets_pct
        )
    
    def analyze_yearly_trends(self, yearly_data: List[BalanceSheetData]) -> Optional[BalanceSheetTrendAnalysis]:
        """
        Analyze yearly balance sheet trends over the last 3 years.
        
        Args:
            yearly_data: List of BalanceSheetData objects (yearly frequency)
            
        Returns:
            BalanceSheetTrendAnalysis object with trend analysis results, or None if insufficient data
        """
        if not yearly_data or len(yearly_data) < 2:
            return None
        
        # Take the last 3 years (or all available if less than 3)
        recent_years = yearly_data[:3]  # Most recent first
        recent_years.reverse()  # Oldest first for trend calculation
        
        ticker = recent_years[0].ticker
        
        # Convert to YearlyBalanceSheetData objects
        yearly_balance_data = []
        for year_data in recent_years:
            year = int(year_data.period_end_date[:4]) if year_data.period_end_date else 0
            
            # Calculate ratios for this year
            current_ratio = self._calculate_current_ratio(year_data)
            debt_to_equity = self._calculate_debt_to_equity(year_data)
            
            yearly_balance_data.append(YearlyBalanceSheetData(
                year=year,
                total_assets=year_data.total_assets,
                total_debt=year_data.total_debt,
                total_equity=year_data.stockholders_equity,
                working_capital=year_data.working_capital,
                cash_and_equivalents=year_data.cash_and_cash_equivalents,
                current_ratio=current_ratio,
                debt_to_equity=debt_to_equity,
                tangible_book_value=year_data.tangible_book_value
            ))
        
        # Calculate growth rates
        assets_growth_rates = self._calculate_growth_rates([yd.total_assets for yd in yearly_balance_data])
        equity_growth_rates = self._calculate_growth_rates([yd.total_equity for yd in yearly_balance_data])
        debt_growth_rates = self._calculate_growth_rates([yd.total_debt for yd in yearly_balance_data])
        
        # Calculate average growth rates
        avg_assets_growth = self._calculate_average(assets_growth_rates)
        avg_equity_growth = self._calculate_average(equity_growth_rates)
        avg_debt_growth = self._calculate_average(debt_growth_rates)
        
        # Assess trend directions
        assets_trend = self._assess_trend_direction(assets_growth_rates, avg_assets_growth)
        equity_trend = self._assess_trend_direction(equity_growth_rates, avg_equity_growth)
        debt_trend = self._assess_trend_direction(debt_growth_rates, avg_debt_growth)
        leverage_trend = self._assess_leverage_trend(debt_growth_rates, equity_growth_rates)
        
        # Extract ratio trends
        debt_to_equity_trend = [yd.debt_to_equity for yd in yearly_balance_data if yd.debt_to_equity is not None]
        current_ratio_trend = [yd.current_ratio for yd in yearly_balance_data if yd.current_ratio is not None]
        
        # Calculate stability scores
        balance_sheet_stability_score = self._calculate_balance_sheet_stability_score(
            assets_growth_rates, equity_growth_rates, debt_growth_rates
        )
        leverage_consistency_score = self._calculate_leverage_consistency_score(debt_to_equity_trend)
        
        return BalanceSheetTrendAnalysis(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            years_analyzed=len(yearly_balance_data),
            yearly_data=yearly_balance_data,
            assets_growth_rates=assets_growth_rates,
            equity_growth_rates=equity_growth_rates,
            debt_growth_rates=debt_growth_rates,
            avg_assets_growth=avg_assets_growth,
            avg_equity_growth=avg_equity_growth,
            avg_debt_growth=avg_debt_growth,
            assets_trend=assets_trend,
            equity_trend=equity_trend,
            debt_trend=debt_trend,
            leverage_trend=leverage_trend,
            debt_to_equity_trend=debt_to_equity_trend,
            current_ratio_trend=current_ratio_trend,
            balance_sheet_stability_score=balance_sheet_stability_score,
            leverage_consistency_score=leverage_consistency_score
        )
    
    def assess_balance_sheet_health(
        self, 
        metrics: Optional[BalanceSheetMetrics], 
        trends: Optional[BalanceSheetTrendAnalysis]
    ) -> BalanceSheetHealthAssessment:
        """
        Assess overall balance sheet health based on quarterly metrics and trend analysis.
        
        Args:
            metrics: BalanceSheetMetrics from latest quarter
            trends: BalanceSheetTrendAnalysis from yearly data
            
        Returns:
            BalanceSheetHealthAssessment with comprehensive health evaluation
        """
        ticker = metrics.ticker if metrics else (trends.ticker if trends else "UNKNOWN")
        
        assessment = BalanceSheetHealthAssessment(
            ticker=ticker,
            assessment_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        if not metrics and not trends:
            assessment.summary = "Insufficient balance sheet data available for health assessment."
            return assessment
        
        # Assess liquidity health
        liquidity_score, liquidity_rating = self._assess_liquidity_health(metrics)
        assessment.liquidity_score = liquidity_score
        assessment.liquidity_health = liquidity_rating
        
        # Assess leverage health
        leverage_score, leverage_rating = self._assess_leverage_health(metrics, trends)
        assessment.leverage_score = leverage_score
        assessment.leverage_health = leverage_rating
        
        # Assess asset quality health
        asset_quality_score, asset_quality_rating = self._assess_asset_quality_health(metrics)
        assessment.asset_quality_score = asset_quality_score
        assessment.asset_quality_health = asset_quality_rating
        
        # Assess financial stability health
        stability_score, stability_rating = self._assess_financial_stability_health(trends)
        assessment.financial_stability_score = stability_score
        assessment.financial_stability_health = stability_rating
        
        # Calculate overall balance sheet health score and rating
        scores = [s for s in [liquidity_score, leverage_score, asset_quality_score, stability_score] if s is not None]
        if scores:
            assessment.overall_balance_sheet_score = sum(scores) / len(scores)
            assessment.overall_balance_sheet_rating = self._score_to_rating(assessment.overall_balance_sheet_score)
        
        # Generate strengths and concerns
        assessment.strengths, assessment.concerns = self._generate_balance_sheet_strengths_and_concerns(
            metrics, trends, assessment
        )
        
        # Generate summary
        assessment.summary = self._generate_balance_sheet_health_summary(assessment)
        
        return assessment
    
    # Helper methods for ratio calculations
    def _calculate_current_ratio(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate current ratio."""
        if data.current_assets and data.current_liabilities and data.current_liabilities != 0:
            return data.current_assets / data.current_liabilities
        return None
    
    def _calculate_quick_ratio(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate quick ratio (acid test)."""
        if data.current_assets and data.current_liabilities and data.current_liabilities != 0:
            inventory = data.inventory or 0
            quick_assets = data.current_assets - inventory
            return quick_assets / data.current_liabilities
        return None
    
    def _calculate_cash_ratio(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate cash ratio."""
        cash = data.cash_and_cash_equivalents or 0
        if cash and data.current_liabilities and data.current_liabilities != 0:
            return cash / data.current_liabilities
        return None
    
    def _calculate_debt_to_equity(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate debt-to-equity ratio."""
        if data.total_debt and data.stockholders_equity and data.stockholders_equity != 0:
            return data.total_debt / data.stockholders_equity
        return None
    
    def _calculate_debt_to_assets(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate debt-to-assets ratio."""
        if data.total_debt and data.total_assets and data.total_assets != 0:
            return data.total_debt / data.total_assets
        return None
    
    def _calculate_equity_ratio(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate equity ratio."""
        if data.stockholders_equity and data.total_assets and data.total_assets != 0:
            return data.stockholders_equity / data.total_assets
        return None
    
    def _calculate_current_assets_percentage(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate current assets as percentage of total assets."""
        if data.current_assets and data.total_assets and data.total_assets != 0:
            return (data.current_assets / data.total_assets) * 100
        return None
    
    def _calculate_ppe_percentage(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate PPE as percentage of total assets."""
        if data.net_ppe and data.total_assets and data.total_assets != 0:
            return (data.net_ppe / data.total_assets) * 100
        return None
    
    def _calculate_cash_percentage(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate cash as percentage of total assets."""
        cash = data.cash_and_cash_equivalents or 0
        if cash and data.total_assets and data.total_assets != 0:
            return (cash / data.total_assets) * 100
        return None
    
    def _calculate_tangible_book_value_per_share(self, data: BalanceSheetData) -> Optional[float]:
        """Calculate tangible book value per share."""
        if data.tangible_book_value and data.ordinary_shares_number and data.ordinary_shares_number != 0:
            return data.tangible_book_value / data.ordinary_shares_number
        return None
    
    # Helper methods from income statement analysis (reused)
    def _calculate_growth_rates(self, values: List[Optional[float]]) -> List[float]:
        """Calculate year-over-year growth rates from a list of values."""
        growth_rates = []
        
        for i in range(1, len(values)):
            if values[i-1] is not None and values[i] is not None and values[i-1] != 0:
                growth_rate = ((values[i] - values[i-1]) / abs(values[i-1])) * 100
                growth_rates.append(growth_rate)
        
        return growth_rates
    
    def _calculate_average(self, values: List[float]) -> Optional[float]:
        """Calculate average of a list of values."""
        if not values:
            return None
        return sum(values) / len(values)
    
    def _assess_trend_direction(self, growth_rates: List[float], avg_growth: Optional[float]) -> TrendDirection:
        """Assess the overall trend direction based on growth rates."""
        if not growth_rates or avg_growth is None:
            return TrendDirection.INSUFFICIENT_DATA
        
        volatility = self._calculate_volatility(growth_rates)
        
        # High volatility threshold
        if volatility and volatility > 25:  # More than 25% standard deviation
            return TrendDirection.VOLATILE
        
        # Trend assessment based on average growth
        if avg_growth > 10:  # More than 10% average growth
            return TrendDirection.STRONG_GROWTH
        elif avg_growth > 3:  # 3-10% average growth
            return TrendDirection.MODERATE_GROWTH
        elif avg_growth > -3:  # Between -3% and 3%
            return TrendDirection.STABLE
        else:  # Less than -3% average growth
            return TrendDirection.DECLINING
    
    def _calculate_volatility(self, values: List[float]) -> Optional[float]:
        """Calculate standard deviation (volatility) of a list of values."""
        if len(values) < 2:
            return None
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _assess_leverage_trend(self, debt_growth_rates: List[float], equity_growth_rates: List[float]) -> TrendDirection:
        """Assess leverage trend by comparing debt vs equity growth."""
        if not debt_growth_rates or not equity_growth_rates:
            return TrendDirection.INSUFFICIENT_DATA
        
        avg_debt_growth = self._calculate_average(debt_growth_rates)
        avg_equity_growth = self._calculate_average(equity_growth_rates)
        
        if avg_debt_growth is None or avg_equity_growth is None:
            return TrendDirection.INSUFFICIENT_DATA
        
        leverage_change = avg_debt_growth - avg_equity_growth
        
        if leverage_change > 10:  # Debt growing much faster than equity
            return TrendDirection.DECLINING  # Worsening leverage
        elif leverage_change > 3:
            return TrendDirection.VOLATILE
        elif leverage_change > -3:
            return TrendDirection.STABLE
        else:  # Equity growing faster than debt
            return TrendDirection.MODERATE_GROWTH  # Improving leverage
    
    def _calculate_balance_sheet_stability_score(
        self, 
        assets_growth: List[float], 
        equity_growth: List[float], 
        debt_growth: List[float]
    ) -> Optional[float]:
        """Calculate balance sheet stability score based on growth consistency."""
        all_growth_rates = assets_growth + equity_growth + debt_growth
        if not all_growth_rates:
            return None
        
        volatility = self._calculate_volatility(all_growth_rates)
        if volatility is None:
            return None
        
        # Base score starts at 10
        score = 10.0
        
        # Penalize high volatility
        volatility_penalty = min(volatility / 5, 8)  # Max penalty of 8 points
        score -= volatility_penalty
        
        return max(0.0, min(10.0, score))
    
    def _calculate_leverage_consistency_score(self, debt_to_equity_trend: List[float]) -> Optional[float]:
        """Calculate leverage consistency score."""
        if len(debt_to_equity_trend) < 2:
            return None
        
        volatility = self._calculate_volatility(debt_to_equity_trend)
        if volatility is None:
            return None
        
        # Base score starts at 10
        score = 10.0
        
        # Penalize high volatility in leverage ratios
        volatility_penalty = min(volatility / 2, 8)  # Max penalty of 8 points
        score -= volatility_penalty
        
        return max(0.0, min(10.0, score))
    
    # Health assessment methods
    def _assess_liquidity_health(self, metrics: Optional[BalanceSheetMetrics]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess liquidity health and return score and rating."""
        if not metrics:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        score = 5.0  # Base score
        
        # Current ratio assessment
        if metrics.current_ratio:
            if metrics.current_ratio > 2.0:
                score += 2
            elif metrics.current_ratio > 1.5:
                score += 1
            elif metrics.current_ratio < 1.0:
                score -= 3
        
        # Quick ratio assessment
        if metrics.quick_ratio:
            if metrics.quick_ratio > 1.0:
                score += 1
            elif metrics.quick_ratio < 0.5:
                score -= 2
        
        # Cash ratio assessment
        if metrics.cash_ratio:
            if metrics.cash_ratio > 0.2:
                score += 1
            elif metrics.cash_ratio < 0.1:
                score -= 1
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_leverage_health(self, metrics: Optional[BalanceSheetMetrics], trends: Optional[BalanceSheetTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess leverage health and return score and rating."""
        score = 5.0  # Base score
        
        # Current leverage assessment
        if metrics and metrics.debt_to_equity:
            if metrics.debt_to_equity < 0.3:
                score += 2
            elif metrics.debt_to_equity < 0.6:
                score += 1
            elif metrics.debt_to_equity > 1.5:
                score -= 3
            elif metrics.debt_to_equity > 1.0:
                score -= 1
        
        # Leverage trend assessment
        if trends and trends.leverage_trend:
            if trends.leverage_trend == TrendDirection.MODERATE_GROWTH:  # Improving leverage
                score += 1
            elif trends.leverage_trend == TrendDirection.DECLINING:  # Worsening leverage
                score -= 2
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_asset_quality_health(self, metrics: Optional[BalanceSheetMetrics]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess asset quality health and return score and rating."""
        if not metrics:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        score = 5.0  # Base score
        
        # Working capital assessment
        if metrics.working_capital:
            if metrics.working_capital > 0:
                score += 1
            else:
                score -= 2
        
        # Cash position assessment
        if metrics.cash_assets_pct:
            if metrics.cash_assets_pct > 10:
                score += 1
            elif metrics.cash_assets_pct < 2:
                score -= 1
        
        # Tangible book value assessment
        if metrics.tangible_book_value_per_share:
            if metrics.tangible_book_value_per_share > 0:
                score += 1
            else:
                score -= 1
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_financial_stability_health(self, trends: Optional[BalanceSheetTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess financial stability health and return score and rating."""
        if not trends or not trends.balance_sheet_stability_score:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        return trends.balance_sheet_stability_score, self._score_to_rating(trends.balance_sheet_stability_score)
    
    def _score_to_rating(self, score: float) -> FinancialHealthRating:
        """Convert numerical score to health rating."""
        if score >= 8.5:
            return FinancialHealthRating.EXCELLENT
        elif score >= 7.0:
            return FinancialHealthRating.GOOD
        elif score >= 5.0:
            return FinancialHealthRating.FAIR
        else:
            return FinancialHealthRating.POOR
    
    def _generate_balance_sheet_strengths_and_concerns(
        self, 
        metrics: Optional[BalanceSheetMetrics], 
        trends: Optional[BalanceSheetTrendAnalysis],
        assessment: BalanceSheetHealthAssessment
    ) -> Tuple[List[str], List[str]]:
        """Generate lists of balance sheet strengths and concerns."""
        strengths = []
        concerns = []
        
        # Liquidity analysis
        if metrics:
            if metrics.current_ratio and metrics.current_ratio > 2.0:
                strengths.append(f"Strong liquidity with current ratio of {metrics.current_ratio:.2f}")
            elif metrics.current_ratio and metrics.current_ratio < 1.0:
                concerns.append(f"Poor liquidity with current ratio of {metrics.current_ratio:.2f}")
            
            # Leverage analysis
            if metrics.debt_to_equity and metrics.debt_to_equity < 0.5:
                strengths.append(f"Conservative leverage with debt-to-equity of {metrics.debt_to_equity:.2f}")
            elif metrics.debt_to_equity and metrics.debt_to_equity > 1.5:
                concerns.append(f"High leverage with debt-to-equity of {metrics.debt_to_equity:.2f}")
            
            # Cash position
            if metrics.cash_assets_pct and metrics.cash_assets_pct > 15:
                strengths.append(f"Strong cash position at {metrics.cash_assets_pct:.1f}% of total assets")
            elif metrics.cash_assets_pct and metrics.cash_assets_pct < 3:
                concerns.append(f"Low cash position at {metrics.cash_assets_pct:.1f}% of total assets")
        
        # Trend analysis
        if trends:
            if trends.leverage_trend == TrendDirection.MODERATE_GROWTH:
                strengths.append("Improving leverage position over time")
            elif trends.leverage_trend == TrendDirection.DECLINING:
                concerns.append("Deteriorating leverage position over time")
            
            if trends.equity_trend == TrendDirection.STRONG_GROWTH:
                strengths.append("Strong equity growth trend")
            elif trends.equity_trend == TrendDirection.DECLINING:
                concerns.append("Declining equity trend")
        
        return strengths, concerns
    
    def _generate_balance_sheet_health_summary(self, assessment: BalanceSheetHealthAssessment) -> str:
        """Generate a comprehensive balance sheet health summary."""
        if assessment.overall_balance_sheet_rating == FinancialHealthRating.INSUFFICIENT_DATA:
            return "Insufficient balance sheet data available for comprehensive health assessment."
        
        rating_text = assessment.overall_balance_sheet_rating.value.lower()
        score_text = f"{assessment.overall_balance_sheet_score:.1f}/10" if assessment.overall_balance_sheet_score else "N/A"
        
        summary = f"Overall balance sheet health is {rating_text} with a score of {score_text}. "
        
        if assessment.strengths:
            summary += f"Key strengths include {', '.join(assessment.strengths[:2])}. "
        
        if assessment.concerns:
            summary += f"Areas of concern include {', '.join(assessment.concerns[:2])}."
        
        return summary.strip()