"""
Cash Flow Analysis Module for Company Financial Health Assessment

This module provides cash flow analysis functionality including quarterly metrics extraction,
yearly trend analysis, and financial health assessment focused on cash flow quality,
sustainability, and growth patterns.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
from ..data.fetchers.cash_flow import CashFlowData
from ..data.enums import DataFrequency
from .income_statement import FinancialHealthRating, TrendDirection


@dataclass
class CashFlowMetrics:
    """
    Dataclass representing key metrics extracted from the latest quarterly cash flow statement.
    
    This focuses on cash flow quality, sustainability, and operational efficiency metrics.
    """
    
    # Metadata
    ticker: str
    quarter_end_date: Optional[str] = None
    
    # Core Cash Flow Metrics
    operating_cash_flow: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    net_change_in_cash: Optional[float] = None
    
    # Cash Flow Quality Metrics
    operating_cash_flow_margin: Optional[float] = None  # OCF / Revenue (needs revenue from income statement)
    free_cash_flow_margin: Optional[float] = None       # FCF / Revenue
    cash_flow_to_debt_ratio: Optional[float] = None     # OCF / Total Debt
    
    # Sustainability Metrics
    capital_expenditure: Optional[float] = None
    capex_to_ocf_ratio: Optional[float] = None          # CapEx / OCF
    cash_flow_coverage_ratio: Optional[float] = None    # OCF / (CapEx + Dividends)
    
    # Working Capital Efficiency
    change_in_working_capital: Optional[float] = None
    working_capital_to_ocf_ratio: Optional[float] = None
    
    # Cash Position Strength
    beginning_cash_position: Optional[float] = None
    ending_cash_position: Optional[float] = None
    cash_burn_rate: Optional[float] = None              # Negative OCF periods only
    
    # Financing Activity Analysis
    debt_issuance: Optional[float] = None
    debt_repayment: Optional[float] = None
    net_debt_activity: Optional[float] = None
    dividend_payments: Optional[float] = None
    share_repurchases: Optional[float] = None


@dataclass
class YearlyCashFlowData:
    """
    Dataclass representing cash flow data for a specific year.
    """
    year: int
    operating_cash_flow: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    net_change_in_cash: Optional[float] = None
    dividend_payments: Optional[float] = None
    beginning_cash: Optional[float] = None
    ending_cash: Optional[float] = None


@dataclass
class CashFlowTrendAnalysis:
    """
    Dataclass representing comprehensive cash flow trend analysis over multiple years.
    
    Contains yearly data, growth rates, and trend assessments for key cash flow metrics.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    years_analyzed: int
    
    # Historical Data
    yearly_data: List[YearlyCashFlowData]
    
    # Growth Rate Analysis (Year-over-Year percentages)
    ocf_growth_rates: List[float]
    fcf_growth_rates: List[float]
    capex_growth_rates: List[float]
    
    # Average Growth Rates
    avg_ocf_growth: Optional[float] = None
    avg_fcf_growth: Optional[float] = None
    avg_capex_growth: Optional[float] = None
    
    # Trend Direction Assessment
    ocf_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    fcf_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    capex_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    cash_generation_trend: TrendDirection = TrendDirection.INSUFFICIENT_DATA
    
    # Volatility Metrics
    ocf_volatility: Optional[float] = None
    fcf_volatility: Optional[float] = None
    
    # Consistency Scores (0-10 scale)
    ocf_consistency_score: Optional[float] = None
    fcf_consistency_score: Optional[float] = None
    cash_flow_stability_score: Optional[float] = None
    
    # Cash Flow Quality Metrics
    avg_ocf_to_fcf_conversion: Optional[float] = None   # How much OCF converts to FCF
    capex_intensity_trend: List[float] = None           # CapEx as % of OCF over time
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.capex_intensity_trend is None:
            self.capex_intensity_trend = []


@dataclass
class CashFlowHealthAssessment:
    """
    Dataclass representing comprehensive cash flow health assessment.
    
    Provides overall cash flow strength rating and detailed analysis.
    """
    
    # Basic Information
    ticker: str
    assessment_date: str
    
    # Overall Cash Flow Health
    overall_cash_flow_rating: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    overall_cash_flow_score: Optional[float] = None  # 0-10 scale
    
    # Component Ratings
    cash_flow_quality_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    cash_flow_sustainability_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    cash_flow_growth_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    cash_flow_stability_health: FinancialHealthRating = FinancialHealthRating.INSUFFICIENT_DATA
    
    # Component Scores (0-10 scale)
    cash_flow_quality_score: Optional[float] = None
    cash_flow_sustainability_score: Optional[float] = None
    cash_flow_growth_score: Optional[float] = None
    cash_flow_stability_score: Optional[float] = None
    
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


class CashFlowAnalyzer:
    """
    Analyzer class for processing cash flow data and generating comprehensive financial analysis.
    
    This class takes raw cash flow data and produces quarterly metrics, trend analysis,
    and financial health assessments focused on cash flow strength and sustainability.
    """
    
    def __init__(self):
        """Initialize the cash flow analyzer."""
        pass
    
    def analyze_latest_quarter(self, quarterly_data: List[CashFlowData]) -> Optional[CashFlowMetrics]:
        """
        Analyze the latest quarterly cash flow data and extract key metrics.
        
        Args:
            quarterly_data: List of CashFlowData objects (quarterly frequency)
            
        Returns:
            CashFlowMetrics object with latest quarter analysis, or None if insufficient data
        """
        if not quarterly_data:
            return None
            
        # Get the most recent quarter (first in the list)
        latest_quarter = quarterly_data[0]
        
        # Calculate derived metrics
        capex_to_ocf_ratio = None
        working_capital_to_ocf_ratio = None
        cash_flow_coverage_ratio = None
        
        # Calculate ratios if we have operating cash flow
        if latest_quarter.operating_cash_flow and latest_quarter.operating_cash_flow > 0:
            if latest_quarter.capital_expenditure:
                capex_to_ocf_ratio = abs(latest_quarter.capital_expenditure) / latest_quarter.operating_cash_flow
            
            if latest_quarter.change_in_working_capital:
                working_capital_to_ocf_ratio = abs(latest_quarter.change_in_working_capital) / latest_quarter.operating_cash_flow
            
            # Cash flow coverage ratio: OCF / (CapEx + Dividends)
            capex = abs(latest_quarter.capital_expenditure) if latest_quarter.capital_expenditure else 0
            dividends = abs(latest_quarter.cash_dividends_paid) if latest_quarter.cash_dividends_paid else 0
            total_obligations = capex + dividends
            if total_obligations > 0:
                cash_flow_coverage_ratio = latest_quarter.operating_cash_flow / total_obligations
        
        # Calculate net debt activity
        net_debt_activity = None
        if latest_quarter.net_long_term_debt_issuance or latest_quarter.net_short_term_debt_issuance:
            long_term = latest_quarter.net_long_term_debt_issuance or 0
            short_term = latest_quarter.net_short_term_debt_issuance or 0
            net_debt_activity = long_term + short_term
        
        # Calculate cash burn rate (for negative OCF periods)
        cash_burn_rate = None
        if latest_quarter.operating_cash_flow and latest_quarter.operating_cash_flow < 0:
            cash_burn_rate = abs(latest_quarter.operating_cash_flow)
        
        return CashFlowMetrics(
            ticker=latest_quarter.ticker,
            quarter_end_date=latest_quarter.period_end_date,
            
            # Core cash flow metrics
            operating_cash_flow=latest_quarter.operating_cash_flow,
            investing_cash_flow=latest_quarter.investing_cash_flow,
            financing_cash_flow=latest_quarter.financing_cash_flow,
            free_cash_flow=latest_quarter.free_cash_flow,
            net_change_in_cash=latest_quarter.changes_in_cash,
            
            # Sustainability metrics
            capital_expenditure=latest_quarter.capital_expenditure,
            capex_to_ocf_ratio=capex_to_ocf_ratio,
            cash_flow_coverage_ratio=cash_flow_coverage_ratio,
            
            # Working capital efficiency
            change_in_working_capital=latest_quarter.change_in_working_capital,
            working_capital_to_ocf_ratio=working_capital_to_ocf_ratio,
            
            # Cash position
            beginning_cash_position=latest_quarter.beginning_cash_position,
            ending_cash_position=latest_quarter.end_cash_position,
            cash_burn_rate=cash_burn_rate,
            
            # Financing activities
            net_debt_activity=net_debt_activity,
            dividend_payments=latest_quarter.cash_dividends_paid,
            share_repurchases=latest_quarter.repurchase_of_capital_stock
        )
    
    def analyze_yearly_trends(self, yearly_data: List[CashFlowData]) -> Optional[CashFlowTrendAnalysis]:
        """
        Analyze yearly cash flow trends over the last 3 years.
        
        Args:
            yearly_data: List of CashFlowData objects (yearly frequency)
            
        Returns:
            CashFlowTrendAnalysis object with trend analysis results, or None if insufficient data
        """
        if not yearly_data or len(yearly_data) < 2:
            return None
        
        # Take the last 3 years (or all available if less than 3)
        recent_years = yearly_data[:3]  # Most recent first
        recent_years.reverse()  # Oldest first for trend calculation
        
        ticker = recent_years[0].ticker
        
        # Convert to YearlyCashFlowData objects
        yearly_cash_flow_data = []
        for year_data in recent_years:
            year = int(year_data.period_end_date[:4]) if year_data.period_end_date else 0
            yearly_cash_flow_data.append(YearlyCashFlowData(
                year=year,
                operating_cash_flow=year_data.operating_cash_flow,
                investing_cash_flow=year_data.investing_cash_flow,
                financing_cash_flow=year_data.financing_cash_flow,
                free_cash_flow=year_data.free_cash_flow,
                capital_expenditure=year_data.capital_expenditure,
                net_change_in_cash=year_data.changes_in_cash,
                dividend_payments=year_data.cash_dividends_paid,
                beginning_cash=year_data.beginning_cash_position,
                ending_cash=year_data.end_cash_position
            ))
        
        # Calculate growth rates
        ocf_growth_rates = self._calculate_growth_rates([yd.operating_cash_flow for yd in yearly_cash_flow_data])
        fcf_growth_rates = self._calculate_growth_rates([yd.free_cash_flow for yd in yearly_cash_flow_data])
        capex_growth_rates = self._calculate_growth_rates([abs(yd.capital_expenditure) if yd.capital_expenditure else None for yd in yearly_cash_flow_data])
        
        # Calculate average growth rates
        avg_ocf_growth = self._calculate_average(ocf_growth_rates)
        avg_fcf_growth = self._calculate_average(fcf_growth_rates)
        avg_capex_growth = self._calculate_average(capex_growth_rates)
        
        # Assess trend directions
        ocf_trend = self._assess_trend_direction(ocf_growth_rates, avg_ocf_growth)
        fcf_trend = self._assess_trend_direction(fcf_growth_rates, avg_fcf_growth)
        capex_trend = self._assess_trend_direction(capex_growth_rates, avg_capex_growth)
        cash_generation_trend = self._assess_cash_generation_trend(ocf_growth_rates, fcf_growth_rates)
        
        # Calculate volatility
        ocf_volatility = self._calculate_volatility(ocf_growth_rates)
        fcf_volatility = self._calculate_volatility(fcf_growth_rates)
        
        # Calculate consistency scores
        ocf_consistency_score = self._calculate_consistency_score(ocf_growth_rates, ocf_volatility)
        fcf_consistency_score = self._calculate_consistency_score(fcf_growth_rates, fcf_volatility)
        cash_flow_stability_score = self._calculate_cash_flow_stability_score(
            ocf_consistency_score, fcf_consistency_score
        )
        
        # Calculate OCF to FCF conversion efficiency
        avg_ocf_to_fcf_conversion = self._calculate_ocf_to_fcf_conversion(yearly_cash_flow_data)
        
        # Calculate CapEx intensity trend
        capex_intensity_trend = self._calculate_capex_intensity_trend(yearly_cash_flow_data)
        
        return CashFlowTrendAnalysis(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            years_analyzed=len(yearly_cash_flow_data),
            yearly_data=yearly_cash_flow_data,
            ocf_growth_rates=ocf_growth_rates,
            fcf_growth_rates=fcf_growth_rates,
            capex_growth_rates=capex_growth_rates,
            avg_ocf_growth=avg_ocf_growth,
            avg_fcf_growth=avg_fcf_growth,
            avg_capex_growth=avg_capex_growth,
            ocf_trend=ocf_trend,
            fcf_trend=fcf_trend,
            capex_trend=capex_trend,
            cash_generation_trend=cash_generation_trend,
            ocf_volatility=ocf_volatility,
            fcf_volatility=fcf_volatility,
            ocf_consistency_score=ocf_consistency_score,
            fcf_consistency_score=fcf_consistency_score,
            cash_flow_stability_score=cash_flow_stability_score,
            avg_ocf_to_fcf_conversion=avg_ocf_to_fcf_conversion,
            capex_intensity_trend=capex_intensity_trend
        )
    
    def assess_cash_flow_health(
        self, 
        metrics: Optional[CashFlowMetrics], 
        trends: Optional[CashFlowTrendAnalysis]
    ) -> CashFlowHealthAssessment:
        """
        Assess overall cash flow health based on quarterly metrics and trend analysis.
        
        Args:
            metrics: CashFlowMetrics from latest quarter
            trends: CashFlowTrendAnalysis from yearly data
            
        Returns:
            CashFlowHealthAssessment with comprehensive health evaluation
        """
        ticker = metrics.ticker if metrics else (trends.ticker if trends else "UNKNOWN")
        
        assessment = CashFlowHealthAssessment(
            ticker=ticker,
            assessment_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        if not metrics and not trends:
            assessment.summary = "Insufficient cash flow data available for health assessment."
            return assessment
        
        # Assess cash flow quality health
        quality_score, quality_rating = self._assess_cash_flow_quality_health(metrics, trends)
        assessment.cash_flow_quality_score = quality_score
        assessment.cash_flow_quality_health = quality_rating
        
        # Assess cash flow sustainability health
        sustainability_score, sustainability_rating = self._assess_cash_flow_sustainability_health(metrics, trends)
        assessment.cash_flow_sustainability_score = sustainability_score
        assessment.cash_flow_sustainability_health = sustainability_rating
        
        # Assess cash flow growth health
        growth_score, growth_rating = self._assess_cash_flow_growth_health(trends)
        assessment.cash_flow_growth_score = growth_score
        assessment.cash_flow_growth_health = growth_rating
        
        # Assess cash flow stability health
        stability_score, stability_rating = self._assess_cash_flow_stability_health(trends)
        assessment.cash_flow_stability_score = stability_score
        assessment.cash_flow_stability_health = stability_rating
        
        # Calculate overall cash flow health score and rating
        scores = [s for s in [quality_score, sustainability_score, growth_score, stability_score] if s is not None]
        if scores:
            assessment.overall_cash_flow_score = sum(scores) / len(scores)
            assessment.overall_cash_flow_rating = self._score_to_rating(assessment.overall_cash_flow_score)
        
        # Generate strengths and concerns
        assessment.strengths, assessment.concerns = self._generate_cash_flow_strengths_and_concerns(
            metrics, trends, assessment
        )
        
        # Generate summary
        assessment.summary = self._generate_cash_flow_health_summary(assessment)
        
        return assessment
    
    # Helper methods for calculations
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
        if volatility and volatility > 30:  # More than 30% standard deviation for cash flows
            return TrendDirection.VOLATILE
        
        # Trend assessment based on average growth
        if avg_growth > 15:  # More than 15% average growth
            return TrendDirection.STRONG_GROWTH
        elif avg_growth > 5:  # 5-15% average growth
            return TrendDirection.MODERATE_GROWTH
        elif avg_growth > -5:  # Between -5% and 5%
            return TrendDirection.STABLE
        else:  # Less than -5% average growth
            return TrendDirection.DECLINING
    
    def _assess_cash_generation_trend(self, ocf_growth_rates: List[float], fcf_growth_rates: List[float]) -> TrendDirection:
        """Assess overall cash generation trend combining OCF and FCF."""
        if not ocf_growth_rates and not fcf_growth_rates:
            return TrendDirection.INSUFFICIENT_DATA
        
        # Combine available growth rates
        combined_rates = []
        if ocf_growth_rates:
            combined_rates.extend(ocf_growth_rates)
        if fcf_growth_rates:
            combined_rates.extend(fcf_growth_rates)
        
        if not combined_rates:
            return TrendDirection.INSUFFICIENT_DATA
        
        avg_combined_growth = sum(combined_rates) / len(combined_rates)
        return self._assess_trend_direction(combined_rates, avg_combined_growth)
    
    def _calculate_consistency_score(self, growth_rates: List[float], volatility: Optional[float]) -> Optional[float]:
        """Calculate consistency score (0-10) based on growth rates and volatility."""
        if not growth_rates or volatility is None:
            return None
        
        # Base score starts at 10
        score = 10.0
        
        # Penalize high volatility (cash flows are naturally more volatile)
        volatility_penalty = min(volatility / 8, 7)  # Max penalty of 7 points
        score -= volatility_penalty
        
        # Bonus for positive average growth
        avg_growth = sum(growth_rates) / len(growth_rates)
        if avg_growth > 0:
            growth_bonus = min(avg_growth / 15, 2)  # Max bonus of 2 points
            score += growth_bonus
        
        return max(0.0, min(10.0, score))
    
    def _calculate_cash_flow_stability_score(self, ocf_score: Optional[float], fcf_score: Optional[float]) -> Optional[float]:
        """Calculate overall cash flow stability score."""
        scores = [s for s in [ocf_score, fcf_score] if s is not None]
        if not scores:
            return None
        return sum(scores) / len(scores)
    
    def _calculate_ocf_to_fcf_conversion(self, yearly_data: List[YearlyCashFlowData]) -> Optional[float]:
        """Calculate average OCF to FCF conversion efficiency."""
        conversions = []
        
        for year_data in yearly_data:
            if (year_data.operating_cash_flow and year_data.free_cash_flow and 
                year_data.operating_cash_flow > 0):
                conversion = year_data.free_cash_flow / year_data.operating_cash_flow
                conversions.append(conversion)
        
        if not conversions:
            return None
        return sum(conversions) / len(conversions)
    
    def _calculate_capex_intensity_trend(self, yearly_data: List[YearlyCashFlowData]) -> List[float]:
        """Calculate CapEx intensity (CapEx as % of OCF) over time."""
        intensity_trend = []
        
        for year_data in yearly_data:
            if (year_data.operating_cash_flow and year_data.capital_expenditure and 
                year_data.operating_cash_flow > 0):
                intensity = abs(year_data.capital_expenditure) / year_data.operating_cash_flow * 100
                intensity_trend.append(intensity)
        
        return intensity_trend
    
    # Health assessment methods
    def _assess_cash_flow_quality_health(self, metrics: Optional[CashFlowMetrics], trends: Optional[CashFlowTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess cash flow quality health and return score and rating."""
        score = 5.0  # Base score
        
        # Operating cash flow assessment
        if metrics and metrics.operating_cash_flow:
            if metrics.operating_cash_flow > 0:
                score += 2
            else:
                score -= 3
        
        # Free cash flow assessment
        if metrics and metrics.free_cash_flow:
            if metrics.free_cash_flow > 0:
                score += 2
            else:
                score -= 2
        
        # OCF to FCF conversion assessment
        if trends and trends.avg_ocf_to_fcf_conversion:
            if trends.avg_ocf_to_fcf_conversion > 0.7:  # Good conversion
                score += 1
            elif trends.avg_ocf_to_fcf_conversion < 0.3:  # Poor conversion
                score -= 1
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_cash_flow_sustainability_health(self, metrics: Optional[CashFlowMetrics], trends: Optional[CashFlowTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess cash flow sustainability health and return score and rating."""
        score = 5.0  # Base score
        
        # CapEx coverage assessment
        if metrics and metrics.capex_to_ocf_ratio:
            if metrics.capex_to_ocf_ratio < 0.5:  # CapEx < 50% of OCF
                score += 2
            elif metrics.capex_to_ocf_ratio < 0.8:  # CapEx < 80% of OCF
                score += 1
            elif metrics.capex_to_ocf_ratio > 1.2:  # CapEx > 120% of OCF
                score -= 2
        
        # Cash flow coverage ratio assessment
        if metrics and metrics.cash_flow_coverage_ratio:
            if metrics.cash_flow_coverage_ratio > 1.5:
                score += 2
            elif metrics.cash_flow_coverage_ratio > 1.0:
                score += 1
            elif metrics.cash_flow_coverage_ratio < 0.8:
                score -= 2
        
        # CapEx intensity trend assessment
        if trends and trends.capex_intensity_trend and len(trends.capex_intensity_trend) > 1:
            recent_intensity = trends.capex_intensity_trend[-1]
            if recent_intensity < 60:  # CapEx < 60% of OCF
                score += 1
            elif recent_intensity > 100:  # CapEx > 100% of OCF
                score -= 1
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_cash_flow_growth_health(self, trends: Optional[CashFlowTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess cash flow growth health and return score and rating."""
        if not trends:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        score = 5.0  # Base score
        
        # OCF growth assessment
        if trends.avg_ocf_growth:
            if trends.avg_ocf_growth > 10:
                score += 2
            elif trends.avg_ocf_growth > 3:
                score += 1
            elif trends.avg_ocf_growth < -5:
                score -= 2
        
        # FCF growth assessment
        if trends.avg_fcf_growth:
            if trends.avg_fcf_growth > 10:
                score += 2
            elif trends.avg_fcf_growth > 3:
                score += 1
            elif trends.avg_fcf_growth < -5:
                score -= 2
        
        score = max(0.0, min(10.0, score))
        return score, self._score_to_rating(score)
    
    def _assess_cash_flow_stability_health(self, trends: Optional[CashFlowTrendAnalysis]) -> Tuple[Optional[float], FinancialHealthRating]:
        """Assess cash flow stability health and return score and rating."""
        if not trends or not trends.cash_flow_stability_score:
            return None, FinancialHealthRating.INSUFFICIENT_DATA
        
        return trends.cash_flow_stability_score, self._score_to_rating(trends.cash_flow_stability_score)
    
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
    
    def _generate_cash_flow_strengths_and_concerns(
        self, 
        metrics: Optional[CashFlowMetrics], 
        trends: Optional[CashFlowTrendAnalysis],
        assessment: CashFlowHealthAssessment
    ) -> Tuple[List[str], List[str]]:
        """Generate lists of cash flow strengths and concerns."""
        strengths = []
        concerns = []
        
        # Operating cash flow analysis
        if metrics and metrics.operating_cash_flow:
            if metrics.operating_cash_flow > 0:
                strengths.append("Positive operating cash flow generation")
            else:
                concerns.append("Negative operating cash flow")
        
        # Free cash flow analysis
        if metrics and metrics.free_cash_flow:
            if metrics.free_cash_flow > 0:
                strengths.append("Positive free cash flow generation")
            else:
                concerns.append("Negative free cash flow")
        
        # Sustainability analysis
        if metrics and metrics.cash_flow_coverage_ratio:
            if metrics.cash_flow_coverage_ratio > 1.5:
                strengths.append(f"Strong cash flow coverage ratio of {metrics.cash_flow_coverage_ratio:.2f}")
            elif metrics.cash_flow_coverage_ratio < 1.0:
                concerns.append(f"Insufficient cash flow coverage ratio of {metrics.cash_flow_coverage_ratio:.2f}")
        
        # Growth trend analysis
        if trends:
            if trends.avg_ocf_growth and trends.avg_ocf_growth > 8:
                strengths.append(f"Strong operating cash flow growth averaging {trends.avg_ocf_growth:.1f}% annually")
            elif trends.avg_ocf_growth and trends.avg_ocf_growth < -5:
                concerns.append(f"Declining operating cash flow with {trends.avg_ocf_growth:.1f}% average annual decline")
            
            if trends.avg_fcf_growth and trends.avg_fcf_growth > 8:
                strengths.append(f"Strong free cash flow growth averaging {trends.avg_fcf_growth:.1f}% annually")
            elif trends.avg_fcf_growth and trends.avg_fcf_growth < -5:
                concerns.append(f"Declining free cash flow with {trends.avg_fcf_growth:.1f}% average annual decline")
        
        # Consistency analysis
        if trends and trends.cash_flow_stability_score:
            if trends.cash_flow_stability_score > 7:
                strengths.append("Consistent and stable cash flow performance")
            elif trends.cash_flow_stability_score < 4:
                concerns.append("High volatility in cash flow performance")
        
        return strengths, concerns
    
    def _generate_cash_flow_health_summary(self, assessment: CashFlowHealthAssessment) -> str:
        """Generate a comprehensive cash flow health summary."""
        if assessment.overall_cash_flow_rating == FinancialHealthRating.INSUFFICIENT_DATA:
            return "Insufficient cash flow data available for comprehensive health assessment."
        
        rating_text = assessment.overall_cash_flow_rating.value.lower()
        score_text = f"{assessment.overall_cash_flow_score:.1f}/10" if assessment.overall_cash_flow_score else "N/A"
        
        summary = f"Overall cash flow health is {rating_text} with a score of {score_text}. "
        
        if assessment.strengths:
            summary += f"Key strengths include {', '.join(assessment.strengths[:2])}. "
        
        if assessment.concerns:
            summary += f"Areas of concern include {', '.join(assessment.concerns[:2])}."
        
        return summary.strip()