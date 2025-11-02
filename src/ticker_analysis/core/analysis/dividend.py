"""
Dividend Analysis Module

This module provides dividend analysis functionality for general company analysis,
including yearly aggregation, statistical calculations, and trend analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
from ..data.fetchers.dividend import DividendData


class DividendTrend(Enum):
    """Enumeration for dividend trend analysis."""
    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    STABLE = "Stable"
    VOLATILE = "Volatile"
    INSUFFICIENT_DATA = "Insufficient Data"


@dataclass
class YearlyDividendData:
    """
    Dataclass representing aggregated dividend data for a specific year.
    """
    year: int
    total_amount: float
    payment_count: int
    average_payment: float
    first_payment_date: str
    last_payment_date: str


@dataclass
class DividendAnalysisData:
    """
    Dataclass representing comprehensive dividend analysis results.
    
    Contains yearly aggregated data and statistical analysis for dividend payments.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    total_years: int
    total_payments: int
    
    # Yearly Data
    yearly_data: List[YearlyDividendData]
    
    # Statistical Analysis
    highest_year_amount: float
    highest_year: int
    lowest_year_amount: float
    lowest_year: int
    
    # Trend Analysis
    dividend_trend: DividendTrend
    average_growth_rate: Optional[float]  # Percentage per year
    year_over_year_variance: Optional[float]  # Percentage
    
    # Recent Performance (last 12 months)
    trailing_12_month_total: Optional[float]
    
    # Consistency Metrics
    consistency_score: Optional[float]  # 0-10 scale
    
    # Years without dividends
    years_without_dividends: List[int]  # Years with no dividend payments


class DividendAnalyzer:
    """
    Analyzer class for processing dividend data and generating comprehensive analysis.
    
    This class takes raw dividend data and produces aggregated yearly statistics,
    trend analysis, and other metrics useful for company dividend evaluation.
    """
    
    def __init__(self):
        """Initialize the dividend analyzer."""
        pass
    
    def analyze_dividends(self, dividend_data: List[DividendData]) -> Optional[DividendAnalysisData]:
        """
        Analyze dividend data and return comprehensive analysis results.
        
        Args:
            dividend_data: List of DividendData objects
            
        Returns:
            DividendAnalysisData object with analysis results, or None if insufficient data
        """
        if not dividend_data:
            return None
            
        ticker = dividend_data[0].ticker
        
        # Aggregate dividends by year
        yearly_data = self._aggregate_by_year(dividend_data)
        
        if not yearly_data:
            return None
            
        # Calculate statistical metrics
        stats = self._calculate_statistics(yearly_data)
        
        # Analyze trends
        trend_analysis = self._analyze_trends(yearly_data)
        
        # Calculate trailing 12-month total
        trailing_12m = self._calculate_trailing_12_months(dividend_data)
        
        # Calculate consistency score
        consistency = self._calculate_consistency_score(yearly_data)
        
        # Find years without dividends
        years_without_dividends = self._find_years_without_dividends(dividend_data, yearly_data)
        
        return DividendAnalysisData(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            total_years=len(yearly_data),
            total_payments=len(dividend_data),
            yearly_data=yearly_data,
            highest_year_amount=stats['highest_amount'],
            highest_year=stats['highest_year'],
            lowest_year_amount=stats['lowest_amount'],
            lowest_year=stats['lowest_year'],
            dividend_trend=trend_analysis['trend'],
            average_growth_rate=trend_analysis['avg_growth_rate'],
            year_over_year_variance=trend_analysis['variance'],
            trailing_12_month_total=trailing_12m,
            consistency_score=consistency,
            years_without_dividends=years_without_dividends
        )
    
    def _aggregate_by_year(self, dividend_data: List[DividendData]) -> List[YearlyDividendData]:
        """
        Aggregate dividend payments by year.
        
        Args:
            dividend_data: List of DividendData objects
            
        Returns:
            List of YearlyDividendData objects, sorted by year (most recent first)
        """
        yearly_aggregates: Dict[int, List[DividendData]] = {}
        
        # Group dividends by year
        for dividend in dividend_data:
            year = dividend.date.year
            if year not in yearly_aggregates:
                yearly_aggregates[year] = []
            yearly_aggregates[year].append(dividend)
        
        # Create yearly data objects
        yearly_data = []
        for year, dividends in yearly_aggregates.items():
            total_amount = sum(d.amount for d in dividends)
            payment_count = len(dividends)
            average_payment = total_amount / payment_count if payment_count > 0 else 0
            
            # Sort dividends by date to get first and last
            sorted_dividends = sorted(dividends, key=lambda x: x.date)
            first_date = sorted_dividends[0].date.strftime("%Y-%m-%d")
            last_date = sorted_dividends[-1].date.strftime("%Y-%m-%d")
            
            yearly_data.append(YearlyDividendData(
                year=year,
                total_amount=total_amount,
                payment_count=payment_count,
                average_payment=average_payment,
                first_payment_date=first_date,
                last_payment_date=last_date
            ))
        
        # Sort by year (most recent first)
        yearly_data.sort(key=lambda x: x.year, reverse=True)
        
        return yearly_data
    
    def _calculate_statistics(self, yearly_data: List[YearlyDividendData]) -> Dict:
        """
        Calculate basic statistical metrics from yearly data.
        
        Args:
            yearly_data: List of YearlyDividendData objects
            
        Returns:
            Dictionary with statistical metrics
        """
        if not yearly_data:
            return {}
        
        amounts = [yd.total_amount for yd in yearly_data]
        
        highest_idx = amounts.index(max(amounts))
        lowest_idx = amounts.index(min(amounts))
        
        return {
            'highest_amount': yearly_data[highest_idx].total_amount,
            'highest_year': yearly_data[highest_idx].year,
            'lowest_amount': yearly_data[lowest_idx].total_amount,
            'lowest_year': yearly_data[lowest_idx].year
        }
    
    def _analyze_trends(self, yearly_data: List[YearlyDividendData]) -> Dict:
        """
        Analyze dividend trends over time.
        
        Args:
            yearly_data: List of YearlyDividendData objects (sorted by year, most recent first)
            
        Returns:
            Dictionary with trend analysis results
        """
        if len(yearly_data) < 2:
            return {
                'trend': DividendTrend.INSUFFICIENT_DATA,
                'avg_growth_rate': None,
                'variance': None
            }
        
        # Sort by year (oldest first) for trend calculation
        sorted_data = sorted(yearly_data, key=lambda x: x.year)
        amounts = [yd.total_amount for yd in sorted_data]
        
        # Calculate year-over-year changes
        yoy_changes = []
        for i in range(1, len(amounts)):
            if amounts[i-1] > 0:  # Avoid division by zero
                change = ((amounts[i] - amounts[i-1]) / amounts[i-1]) * 100
                yoy_changes.append(change)
        
        if not yoy_changes:
            return {
                'trend': DividendTrend.INSUFFICIENT_DATA,
                'avg_growth_rate': None,
                'variance': None
            }
        
        # Calculate average growth rate
        avg_growth_rate = sum(yoy_changes) / len(yoy_changes)
        
        # Calculate variance (standard deviation of year-over-year changes)
        if len(yoy_changes) > 1:
            mean = avg_growth_rate
            variance = sum((x - mean) ** 2 for x in yoy_changes) / len(yoy_changes)
            std_dev = variance ** 0.5
        else:
            std_dev = 0
        
        # Determine trend
        trend = self._determine_trend(yoy_changes, avg_growth_rate, std_dev)
        
        return {
            'trend': trend,
            'avg_growth_rate': avg_growth_rate,
            'variance': std_dev
        }
    
    def _determine_trend(self, yoy_changes: List[float], avg_growth: float, std_dev: float) -> DividendTrend:
        """
        Determine the overall dividend trend based on year-over-year changes.
        
        Args:
            yoy_changes: List of year-over-year percentage changes
            avg_growth: Average growth rate
            std_dev: Standard deviation of changes
            
        Returns:
            DividendTrend enum value
        """
        # High volatility threshold
        if std_dev > 20:  # More than 20% standard deviation
            return DividendTrend.VOLATILE
        
        # Trend thresholds
        if avg_growth > 2:  # More than 2% average growth
            return DividendTrend.INCREASING
        elif avg_growth < -2:  # More than 2% average decline
            return DividendTrend.DECREASING
        else:  # Between -2% and 2%
            return DividendTrend.STABLE
    
    def _calculate_trailing_12_months(self, dividend_data: List[DividendData]) -> Optional[float]:
        """
        Calculate total dividends for the trailing 12 months.
        
        Args:
            dividend_data: List of DividendData objects
            
        Returns:
            Total dividend amount for trailing 12 months, or None if insufficient data
        """
        if not dividend_data:
            return None
        
        # Get current date and 12 months ago
        current_date = datetime.now().date()
        twelve_months_ago = datetime(current_date.year - 1, current_date.month, current_date.day).date()
        
        # Filter dividends within the last 12 months
        recent_dividends = [
            d for d in dividend_data 
            if d.date >= twelve_months_ago and d.date <= current_date
        ]
        
        if not recent_dividends:
            return None
        
        return sum(d.amount for d in recent_dividends)
    
    def _calculate_consistency_score(self, yearly_data: List[YearlyDividendData]) -> Optional[float]:
        """
        Calculate a consistency score (0-10) based on dividend payment regularity.
        
        Args:
            yearly_data: List of YearlyDividendData objects
            
        Returns:
            Consistency score from 0-10, or None if insufficient data
        """
        if len(yearly_data) < 2:
            return None
        
        # Base score
        score = 10.0
        
        # Penalize for missing years (if there are gaps in the data)
        years = sorted([yd.year for yd in yearly_data])
        expected_years = years[-1] - years[0] + 1
        actual_years = len(years)
        if actual_years < expected_years:
            gap_penalty = (expected_years - actual_years) * 1.5
            score -= gap_penalty
        
        # Penalize for high variance in payment amounts
        amounts = [yd.total_amount for yd in yearly_data]
        if len(amounts) > 1:
            mean_amount = sum(amounts) / len(amounts)
            if mean_amount > 0:
                variance = sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)
                cv = (variance ** 0.5) / mean_amount  # Coefficient of variation
                variance_penalty = cv * 5  # Scale the penalty
                score -= variance_penalty
        
        # Penalize for irregular payment frequency
        payment_counts = [yd.payment_count for yd in yearly_data]
        if payment_counts:
            most_common_count = max(set(payment_counts), key=payment_counts.count)
            irregular_years = sum(1 for count in payment_counts if count != most_common_count)
            frequency_penalty = (irregular_years / len(payment_counts)) * 2
            score -= frequency_penalty
        
        # Ensure score is between 0 and 10
        return max(0.0, min(10.0, score))
    
    def _find_years_without_dividends(self, dividend_data: List[DividendData], yearly_data: List[YearlyDividendData]) -> List[int]:
        """
        Find years within the dividend history range that had no dividend payments.
        
        Args:
            dividend_data: List of DividendData objects
            yearly_data: List of YearlyDividendData objects
            
        Returns:
            List of years with no dividend payments, sorted in ascending order
        """
        if not dividend_data or not yearly_data:
            return []
        
        # Get the range of years from the dividend data
        all_years = [d.date.year for d in dividend_data]
        min_year = min(all_years)
        max_year = max(all_years)
        
        # Get years that have dividend payments
        years_with_dividends = set(yd.year for yd in yearly_data)
        
        # Find missing years in the range
        years_without_dividends = []
        for year in range(min_year, max_year + 1):
            if year not in years_with_dividends:
                years_without_dividends.append(year)
        
        return sorted(years_without_dividends)