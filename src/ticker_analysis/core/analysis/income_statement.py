"""
Income Statement Analysis Module for Company Analysis

This module provides income statement analysis functionality for general company analysis,
including quarterly metrics extraction, yearly trend analysis, and financial health assessment.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
from ..data.fetchers.income_statement import IncomeStatementData
from ..data.enums import DataFrequency


class FinancialHealthRating(Enum):
    """Enumeration for financial health assessment ratings."""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    INSUFFICIENT_DATA = "Insufficient Data"


class TrendDirection(Enum):
    """Enumeration for trend direction analysis."""
    STRONG_GROWTH = "Strong Growth"
    MODERATE_GROWTH = "Moderate Growth"
    STABLE = "Stable"
    DECLINING = "Declining"
    VOLATILE = "Volatile"
    INSUFFICIENT_DATA = "Insufficient Data"


@dataclass
class IncomeStatementMetrics:
    """
    Dataclass representing key metrics extracted from the latest quarterly income statement.
    
    This focuses on the core financial health metrics for company analysis.
    """
    
    # Metadata
    ticker: str
    quarter_end_date: Optional[str] = None
    
    # Core Revenue Metrics
    latest_quarter_revenue: Optional[float] = None
    latest_quarter_net_income: Optional[float] = None
    latest_quarter_operating_income: Optional[float] = None
    latest_quarter_eps: Optional[float] = None
    
    # Additional Key Metrics
    latest_quarter_gross_profit: Optional[float] = None
    latest_quarter_ebitda: Optional[float] = None
    
    # Margin Calculations (derived metrics)
    net_profit_margin: Optional[float] = None  # Net Income / Revenue
    operating_margin: Optional[float] = None   # Operating Income / Revenue
    gross_margin: Optional[float] = None       # Gross Profit / Revenue


@dataclass
class YearlyFinancialData:
    """
    Dataclass representing financial data for a specific year.
    """
    year: int
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    operating_income: Optional[float] = None
    eps: Optional[float] = None
    gross_profit: Optional[float] = None
    ebitda: Optional[float] = None


@dataclass
class TrendAnalysis:
    """
    Dataclass representing comprehensive trend analysis over 3 years.
    
    Contains yearly data, growth rates, and trend assessments for key financial metrics.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    years_analyzed: int
    
    # Historical Data (3 years)
    yearly_data: List[YearlyFinancialData]
    
    # Growth Rate Analysis (Year-over-Year percentages)
    revenue_growth_rates: List[float]  # YoY growth rates
    net_income_growth_rates: List[float]
    operating_income_growth_rates: List[float]
    eps_growth_rates: List[float]
    
    # Average Growth Rates (3-year average)
    avg_revenue_growth: Optional[float] = None
    avg_net_income_growth: Optional[float] = None
    avg_operating_income_growth: Optional[float] = None
    avg_eps_growth: Optional[float] = None
    
    # Trend Direction Assessment
    revenue_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    net_income_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    operating_income_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    earnings_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    
    # Volatility Metrics (Standard deviation of growth rates)
    revenue_volatility: Optional[float] = None
    net_income_volatility: Optional[float] = None
    operating_income_volatility: Optional[float] = None
    
    # Consistency Scores (0-10 scale)
    revenue_consistency_score: Optional[float] = None
    earnings_consistency_score: Optional[float] = None
    overall_consistency_score: Optional[float] = None


@dataclass
class FinancialHealthAssessment:
    """
    Dataclass representing comprehensive financial health assessment.
    
    Provides overall health rating and detailed analysis of financial performance.
    """
    
    # Basic Information
    ticker: str
    assessment_date: str
    
    # Overall Health Rating
    overall_health_rating: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    overall_health_score: Optional[float] = None  # 0-10 scale
    
    # Component Ratings
    revenue_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    profitability_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    growth_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    consistency_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    
    # Component Scores (0-10 scale)
    revenue_score: Optional[float] = None
    profitability_score: Optional[float] = None
    growth_score: Optional[float] = None
    consistency_score: Optional[float] = None
    
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


class CompanyIncomeStatementAnalyzer:
    """
    Analyzer class for processing income statement data and generating comprehensive company analysis.
    
    This class takes raw income statement data and produces quarterly metrics, trend analysis,
    and financial health assessments for general company evaluation.
    """
    
    def __init__(self):
        """Initialize the income statement analyzer."""
        pass
    
    def analyze_latest_quarter(self, quarterly_data: List[IncomeStatementData]) -> Optional[IncomeStatementMetrics]:
        """
        Analyze the latest quarterly income statement data and extract key metrics.
        
        Args:
            quarterly_data: List of IncomeStatementData objects (quarterly frequency)
            
        Returns:
            IncomeStatementMetrics object with latest quarter analysis, or None if insufficient data
        """
        if not quarterly_data:
            return None
            
        # Get the most recent quarter (first in the list)
        latest_quarter = quarterly_data[0]
        
        # Calculate derived metrics
        net_profit_margin = None
        operating_margin = None
        gross_margin = None
        
        if latest_quarter.total_revenue and latest_quarter.total_revenue != 0:
            if latest_quarter.net_income is not None:
                net_profit_margin = (latest_quarter.net_income / latest_quarter.total_revenue) * 100
            if latest_quarter.operating_income is not None:
                operating_margin = (latest_quarter.operating_income / latest_quarter.total_revenue) * 100
            if latest_quarter.gross_profit is not None:
                gross_margin = (latest_quarter.gross_profit / latest_quarter.total_revenue) * 100
        
        return IncomeStatementMetrics(
            ticker=latest_quarter.ticker,
            quarter_end_date=latest_quarter.period_end_date,
            latest_quarter_revenue=latest_quarter.total_revenue,
            latest_quarter_net_income=latest_quarter.net_income,
            latest_quarter_operating_income=latest_quarter.operating_income,
            latest_quarter_eps=latest_quarter.diluted_eps,
            latest_quarter_gross_profit=latest_quarter.gross_profit,
            latest_quarter_ebitda=latest_quarter.ebitda,
            net_profit_margin=net_profit_margin,
            operating_margin=operating_margin,
            gross_margin=gross_margin
        )
    
    def analyze_yearly_trends(self, yearly_data: List[IncomeStatementData]) -> Optional[TrendAnalysis]:
        """
        Analyze yearly income statement trends over the last 3 years.
        
        Args:
            yearly_data: List of IncomeStatementData objects (yearly frequency)
            
        Returns:
            TrendAnalysis object with trend analysis results, or None if insufficient data
        """
        if not yearly_data or len(yearly_data) < 2:
            return None
        
        # Take the last 3 years (or all available if less than 3)
        recent_years = yearly_data[:3]  # Most recent first
        recent_years.reverse()  # Oldest first for trend calculation
        
        ticker = recent_years[0].ticker
        
        # Convert to YearlyFinancialData objects
        yearly_financial_data = []
        for year_data in recent_years:
            year = int(year_data.period_end_date[:4]) if year_data.period_end_date else 0
            yearly_financial_data.append(YearlyFinancialData(
                year=year,
                revenue=year_data.total_revenue,
                net_income=year_data.net_income,
                operating_income=year_data.operating_income,
                eps=year_data.diluted_eps,
                gross_profit=year_data.gross_profit,
                ebitda=year_data.ebitda
            ))
        
        # Calculate growth rates
        revenue_growth_rates = self._calculate_growth_rates([yd.revenue for yd in yearly_financial_data])
        net_income_growth_rates = self._calculate_growth_rates([yd.net_income for yd in yearly_financial_data])
        operating_income_growth_rates = self._calculate_growth_rates([yd.operating_income for yd in yearly_financial_data])
        eps_growth_rates = self._calculate_growth_rates([yd.eps for yd in yearly_financial_data])
        
        # Calculate average growth rates
        avg_revenue_growth = self._calculate_average(revenue_growth_rates)
        avg_net_income_growth = self._calculate_average(net_income_growth_rates)
        avg_operating_income_growth = self._calculate_average(operating_income_growth_rates)
        avg_eps_growth = self._calculate_average(eps_growth_rates)
        
        # Assess trend directions
        revenue_trend = self._assess_trend_direction(revenue_growth_rates, avg_revenue_growth)
        net_income_trend = self._assess_trend_direction(net_income_growth_rates, avg_net_income_growth)
        operating_income_trend = self._assess_trend_direction(operating_income_growth_rates, avg_operating_income_growth)
        earnings_trend = self._assess_trend_direction(eps_growth_rates, avg_eps_growth)
        
        # Calculate volatility (standard deviation)
        revenue_volatility = self._calculate_volatility(revenue_growth_rates)
        net_income_volatility = self._calculate_volatility(net_income_growth_rates)
        operating_income_volatility = self._calculate_volatility(operating_income_growth_rates)
        
        # Calculate consistency scores
        revenue_consistency_score = self._calculate_consistency_score(revenue_growth_rates, revenue_volatility)
        earnings_consistency_score = self._calculate_consistency_score(eps_growth_rates, self._calculate_volatility(eps_growth_rates))
        overall_consistency_score = self._calculate_overall_consistency(
            revenue_consistency_score, earnings_consistency_score
        )
        
        return TrendAnalysis(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            years_analyzed=len(yearly_financial_data),
            yearly_data=yearly_financial_data,
            revenue_growth_rates=revenue_growth_rates,
            net_income_growth_rates=net_income_growth_rates,
            operating_income_growth_rates=operating_income_growth_rates,
            eps_growth_rates=eps_growth_rates,
            avg_revenue_growth=avg_revenue_growth,
            avg_net_income_growth=avg_net_income_growth,
            avg_operating_income_growth=avg_operating_income_growth,
            avg_eps_growth=avg_eps_growth,
            revenue_trend=revenue_trend,
            net_income_trend=net_income_trend,
            operating_income_trend=operating_income_trend,
            earnings_trend=earnings_trend,
            revenue_volatility=revenue_volatility,
            net_income_volatility=net_income_volatility,
            operating_income_volatility=operating_income_volatility,
            revenue_consistency_score=revenue_consistency_score,
            earnings_consistency_score=earnings_consistency_score,
            overall_consistency_score=overall_consistency_score
        )
    
    def assess_financial_health(
        self, 
        metrics: Optional[IncomeStatementMetrics], 
        trends: Optional[TrendAnalysis]
    ) -> FinancialHealthAssessment:
        """
        Assess overall financial health based on quarterly metrics and trend analysis.
        
        Args:
            metrics: IncomeStatementMetrics from latest quarter
            trends: TrendAnalysis from yearly data
            
        Returns:
            FinancialHealthAssessment with comprehensive health evaluation
        """
        ticker = metrics.ticker if metrics else (trends.ticker if trends else "UNKNOWN")
        
        assessment = FinancialHealthAssessment(
            ticker=ticker,
            assessment_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        if not metrics and not trends:
            assessment.summary = "Insufficient data available for financial health assessment."
            return assessment
        
        # Assess revenue health
        revenue_score, revenue_rating = self._assess_revenue_health(metrics, trends)
        assessment.revenue_score = revenue_score
        assessment.revenue_health = revenue_rating
        
        # Assess profitability health
        profitability_score, profitability_rating = self._assess_profitability_health(metrics, trends)
        assessment.profitability_score = profitability_score
        assessment.profitability_health = profitability_rating
        
        # Assess growth health
        growth_score, growth_rating = self._assess_growth_health(trends)
        assessment.growth_score = growth_score
        assessment.growth_health = growth_rating
        
        # Assess consistency health
        consistency_score, consistency_rating = self._assess_consistency_health(trends)
        assessment.consistency_score = consistency_score
        assessment.consistency_health = consistency_rating
        
        # Calculate overall health score and rating
        scores = [s for s in [revenue_score, profitability_score, growth_score, consistency_score] if s is not None]
        if scores:
            assessment.overall_health_score = sum(scores) / len(scores)
            assessment.overall_health_rating = self._score_to_rating(assessment.overall_health_score)
        
        # Generate strengths and concerns
        assessment.strengths, assessment.concerns = self._generate_strengths_and_concerns(
            metrics, trends, assessment
        )
        
        # Generate summary
        assessment.summary = self._generate_health_summary(assessment)
        
        return assessment
    
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
    
    def _calculate_volatility(self, values: List[float]) -> Optional[float]:
        """Calculate standard deviation (volatility) of a list of values."""
        if len(values) < 2:
            return None
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
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
    
    def _calculate_consistency_score(self, growth_rates: List[float], volatility: Optional[float]) -> Optional[float]:
        """Calculate consistency score (0-10) based on growth rates and volatility."""
        if not growth_rates or volatility is None:
            return None
        
        # Base score starts at 10
        score = 10.0
        
        # Penalize high volatility
        volatility_penalty = min(volatility / 5, 8)  # Max penalty of 8 points
        score -= volatility_penalty
        
        # Bonus for positive average growth
        avg_growth = sum(growth_rates) / len(growth_rates)
        if avg_growth > 0:
            growth_bonus = min(avg_growth / 10, 2)  # Max bonus of 2 points
            score += growth_bonus
        
        return max(0.0, min(10.0, score))
    
    def _calculate_overall_consistency(self, revenue_score: Optional[float], earnings_score: Optional[float]) -> Optional[float]:
        """Calculate overall consistency score from component scores."""
        scores = [s for s in [revenue_score, earnings_score] if s is not None]
        if not scores:
            return None
        return sum(scores) / len(scores)
    
    def _assess_revenue_health(self, metrics: Optional[IncomeStatementMetrics], trends: Optional[TrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess revenue health and return score and rating."""
        if not trends or not trends.avg_revenue_growth:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        score = 5.0  # Base score
        
        # Revenue growth assessment
        if trends.avg_revenue_growth > 8:
            score += 3
        elif trends.avg_revenue_growth > 3:
            score += 1
        elif trends.avg_revenue_growth < -5:
            score -= 3
        
        # Revenue consistency assessment
        if trends.revenue_consistency_score:
            consistency_factor = (trends.revenue_consistency_score - 5) / 2
            score += consistency_factor
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_profitability_health(self, metrics: Optional[IncomeStatementMetrics], trends: Optional[TrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess profitability health and return score and rating."""
        score = 5.0  # Base score
        
        # Latest quarter profitability
        if metrics and metrics.net_profit_margin:
            if metrics.net_profit_margin > 15:
                score += 2
            elif metrics.net_profit_margin > 5:
                score += 1
            elif metrics.net_profit_margin < 0:
                score -= 3
        
        # Net income trend
        if trends and trends.avg_net_income_growth:
            if trends.avg_net_income_growth > 10:
                score += 2
            elif trends.avg_net_income_growth > 0:
                score += 1
            elif trends.avg_net_income_growth < -10:
                score -= 2
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_growth_health(self, trends: Optional[TrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess growth health and return score and rating."""
        if not trends:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        score = 5.0  # Base score
        
        # Average growth rates
        growth_rates = [
            trends.avg_revenue_growth,
            trends.avg_net_income_growth,
            trends.avg_operating_income_growth
        ]
        
        valid_rates = [rate for rate in growth_rates if rate is not None]
        if valid_rates:
            avg_overall_growth = sum(valid_rates) / len(valid_rates)
            
            if avg_overall_growth > 8:
                score += 3
            elif avg_overall_growth > 3:
                score += 1
            elif avg_overall_growth < -5:
                score -= 3
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_consistency_health(self, trends: Optional[TrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess consistency health and return score and rating."""
        if not trends or not trends.overall_consistency_score:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        return trends.overall_consistency_score, self._score_to_rating(trends.overall_consistency_score)
    
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
    
    def _generate_strengths_and_concerns(
        self, 
        metrics: Optional[IncomeStatementMetrics], 
        trends: Optional[TrendAnalysis],
        assessment: FinancialHealthAssessment
    ) -> Tuple[List[str], List[str]]:
        """Generate lists of strengths and concerns based on analysis."""
        strengths = []
        concerns = []
        
        # Revenue analysis
        if trends and trends.avg_revenue_growth:
            if trends.avg_revenue_growth > 5:
                strengths.append(f"Strong revenue growth averaging {trends.avg_revenue_growth:.1f}% annually")
            elif trends.avg_revenue_growth < -3:
                concerns.append(f"Declining revenue with {trends.avg_revenue_growth:.1f}% average annual decline")
        
        # Profitability analysis
        if metrics and metrics.net_profit_margin:
            if metrics.net_profit_margin > 10:
                strengths.append(f"Healthy profit margin of {metrics.net_profit_margin:.1f}%")
            elif metrics.net_profit_margin < 0:
                concerns.append(f"Negative profit margin of {metrics.net_profit_margin:.1f}%")
        
        # Consistency analysis
        if trends and trends.overall_consistency_score:
            if trends.overall_consistency_score > 7:
                strengths.append("Consistent financial performance with low volatility")
            elif trends.overall_consistency_score < 4:
                concerns.append("High volatility in financial performance")
        
        # Growth trend analysis
        if trends:
            declining_metrics = []
            if trends.revenue_trend == TrendDirection.DECLINING:
                declining_metrics.append("revenue")
            if trends.net_income_trend == TrendDirection.DECLINING:
                declining_metrics.append("net income")
            if trends.operating_income_trend == TrendDirection.DECLINING:
                declining_metrics.append("operating income")
            
            if declining_metrics:
                concerns.append(f"Declining trend in {', '.join(declining_metrics)}")
        
        return strengths, concerns
    
    def _generate_health_summary(self, assessment: FinancialHealthAssessment) -> str:
        """Generate a comprehensive health summary."""
        if assessment.overall_health_rating == FinancialHealthRating.INSUFFICIENT_DATA:
            return "Insufficient data available for comprehensive financial health assessment."
        
        rating_text = assessment.overall_health_rating.value.lower()
        score_text = f"{assessment.overall_health_score:.1f}/10" if assessment.overall_health_score else "N/A"
        
        summary = f"Overall financial health is {rating_text} with a score of {score_text}. "
        
        if assessment.strengths:
            summary += f"Key strengths include {', '.join(assessment.strengths[:2])}. "
        
        if assessment.concerns:
            summary += f"Areas of concern include {', '.join(assessment.concerns[:2])}."
        
        return summary.strip()