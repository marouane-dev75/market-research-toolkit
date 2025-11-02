"""
Magic Formula Calculator Module

This module contains the core calculation logic and data structures for Joel Greenblatt's Magic Formula.
Handles the mathematical computations for earnings yield, return on capital, and ranking calculations.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MagicFormulaData:
    """
    Dataclass representing Magic Formula analysis data for a ticker.
    
    Contains the calculated metrics, rankings, and scores used in the Magic Formula.
    """
    
    # Basic Information
    ticker: str
    company_name: Optional[str] = None
    
    # Raw Financial Data
    ebit: Optional[float] = None
    enterprise_value: Optional[float] = None
    invested_capital: Optional[float] = None
    
    # Magic Formula Metrics
    earnings_yield: Optional[float] = None  # EBIT / Enterprise Value
    return_on_capital: Optional[float] = None  # EBIT / Invested Capital
    
    # Rankings (1 = best)
    earnings_yield_rank: Optional[int] = None
    return_on_capital_rank: Optional[int] = None
    combined_rank: Optional[int] = None
    
    # Magic Formula Score (lower is better)
    magic_formula_score: Optional[float] = None
    
    # Data Quality Flags
    has_complete_data: bool = False
    missing_data_reason: Optional[str] = None


class MagicFormulaCalculator:
    """
    Calculator class for Magic Formula metrics and rankings.
    
    This class handles the core mathematical computations of the Magic Formula,
    including metric calculations and ranking algorithms.
    """
    
    def calculate_metrics(self, data: MagicFormulaData) -> MagicFormulaData:
        """
        Calculate Magic Formula metrics for a single ticker.
        
        Args:
            data: MagicFormulaData object with raw financial data
            
        Returns:
            Updated MagicFormulaData object with calculated metrics
        """
        # Validate required data
        missing_fields = []
        if data.ebit is None or data.ebit <= 0:
            missing_fields.append("EBIT")
        if data.enterprise_value is None or data.enterprise_value <= 0:
            missing_fields.append("Enterprise Value")
        if data.invested_capital is None or data.invested_capital <= 0:
            missing_fields.append("Invested Capital")
        
        if missing_fields:
            data.missing_data_reason = f"Missing or invalid: {', '.join(missing_fields)}"
            data.has_complete_data = False
        else:
            # Calculate Magic Formula metrics
            data.earnings_yield = data.ebit / data.enterprise_value
            data.return_on_capital = data.ebit / data.invested_capital
            data.has_complete_data = True
        
        return data
    
    def calculate_rankings(self, data_list: List[MagicFormulaData]) -> List[MagicFormulaData]:
        """
        Calculate Magic Formula rankings and scores for valid data.
        
        Args:
            data_list: List of MagicFormulaData objects with complete data
            
        Returns:
            List of MagicFormulaData objects sorted by Magic Formula score
        """
        if not data_list:
            return []
        
        # Sort by earnings yield (descending - higher is better) and assign ranks
        sorted_by_earnings_yield = sorted(data_list, key=lambda x: x.earnings_yield, reverse=True)
        for rank, data in enumerate(sorted_by_earnings_yield, 1):
            data.earnings_yield_rank = rank
        
        # Sort by return on capital (descending - higher is better) and assign ranks
        sorted_by_return_on_capital = sorted(data_list, key=lambda x: x.return_on_capital, reverse=True)
        for rank, data in enumerate(sorted_by_return_on_capital, 1):
            data.return_on_capital_rank = rank
        
        # Calculate combined Magic Formula score (sum of ranks - lower is better)
        for data in data_list:
            data.magic_formula_score = data.earnings_yield_rank + data.return_on_capital_rank
        
        # Sort by Magic Formula score (ascending - lower score is better) and assign final ranks
        sorted_by_score = sorted(data_list, key=lambda x: x.magic_formula_score)
        for rank, data in enumerate(sorted_by_score, 1):
            data.combined_rank = rank
        
        return sorted_by_score