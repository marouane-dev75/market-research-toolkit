"""
Balance Sheet Analysis PDF Formatter

This module formats the balance sheet analysis section for PDF output.
"""

from typing import List
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.units import inch

from ..models import CompanyAnalysisData
from ..balance_sheet import BalanceSheetHealthAssessment
from .base_formatter import BasePDFFormatter


class BalanceSheetFormatter(BasePDFFormatter):
    """
    Formatter for the balance sheet analysis section in PDF reports.
    """

    def format_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the balance sheet analysis section.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        elements = []

        # Section header
        elements.append(self.create_section_header("🏦 BALANCE SHEET ANALYSIS"))
        elements.append(Spacer(1, 0.1 * inch))

        # Latest quarter metrics
        if data.balance_sheet_metrics:
            elements.extend(self._format_balance_sheet_metrics(data.balance_sheet_metrics))

        # Balance sheet trends
        if data.balance_sheet_trends:
            elements.extend(self._format_balance_sheet_trends(data.balance_sheet_trends))

        # Balance sheet health
        if data.balance_sheet_health:
            elements.extend(self._format_balance_sheet_health(data.balance_sheet_health))

        return elements

    def _format_balance_sheet_metrics(self, metrics) -> List:
        """Format balance sheet metrics subsection."""
        elements = []

        elements.append(self.create_subheader("Latest Quarter Balance Sheet Metrics"))
        elements.append(Spacer(1, 0.05 * inch))

        # Quarter information
        if metrics.quarter_end_date:
            elements.append(self.create_bullet_point(f"Quarter End Date: {metrics.quarter_end_date}"))

        # Liquidity ratios
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Liquidity Ratios:"))
        if metrics.current_ratio is not None:
            ratio_color = self.get_status_color(metrics.current_ratio, (1.5, 1.0))
            elements.append(self.create_bullet_point(f"  Current Ratio: {self.format_ratio(metrics.current_ratio)}", ratio_color))

        if metrics.quick_ratio is not None:
            ratio_color = self.get_status_color(metrics.quick_ratio, (1.0, 0.5))
            elements.append(self.create_bullet_point(f"  Quick Ratio: {self.format_ratio(metrics.quick_ratio)}", ratio_color))

        if metrics.cash_ratio is not None:
            elements.append(self.create_bullet_point(f"  Cash Ratio: {self.format_ratio(metrics.cash_ratio)}"))

        # Leverage ratios
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Leverage Ratios:"))
        if metrics.debt_to_equity is not None:
            ratio_color = self.get_status_color(metrics.debt_to_equity, (0.6, 1.5))
            elements.append(self.create_bullet_point(f"  Debt-to-Equity: {self.format_ratio(metrics.debt_to_equity)}", ratio_color))

        if metrics.debt_to_assets is not None:
            elements.append(self.create_bullet_point(f"  Debt-to-Assets: {self.format_ratio(metrics.debt_to_assets)}"))

        if metrics.equity_ratio is not None:
            elements.append(self.create_bullet_point(f"  Equity Ratio: {self.format_ratio(metrics.equity_ratio)}"))

        # Financial strength indicators
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Financial Strength:"))
        elements.append(self.create_bullet_point(f"  Cash & Equivalents: {self.format_currency(metrics.cash_and_equivalents, compact=True)}"))
        elements.append(self.create_bullet_point(f"  Total Debt: {self.format_currency(metrics.total_debt, compact=True)}"))
        elements.append(self.create_bullet_point(f"  Total Equity: {self.format_currency(metrics.total_equity, compact=True)}"))
        elements.append(self.create_bullet_point(f"  Working Capital: {self.format_currency(metrics.working_capital, compact=True)}"))

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_balance_sheet_trends(self, trends) -> List:
        """Format balance sheet trends subsection."""
        elements = []

        elements.append(self.create_subheader("Balance Sheet Trends"))
        elements.append(Spacer(1, 0.05 * inch))

        # Basic trend information
        elements.append(self.create_bullet_point(f"Analysis Period: {trends.years_analyzed} years of data"))
        elements.append(self.create_bullet_point(f"Analysis Date: {trends.analysis_date}"))

        # Average growth rates
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Average Annual Growth Rates:"))
        if trends.avg_assets_growth is not None:
            growth_color = self.get_status_color(trends.avg_assets_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Assets Growth: {self.format_percentage(trends.avg_assets_growth / 100)}", growth_color))

        if trends.avg_equity_growth is not None:
            growth_color = self.get_status_color(trends.avg_equity_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Equity Growth: {self.format_percentage(trends.avg_equity_growth / 100)}", growth_color))

        if trends.avg_debt_growth is not None:
            growth_color = self.get_status_color(trends.avg_debt_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Debt Growth: {self.format_percentage(trends.avg_debt_growth / 100)}", growth_color))

        # Trend directions
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Trend Assessment:"))
        elements.append(self.create_bullet_point(f"  Assets Trend: {trends.assets_trend.value}"))
        elements.append(self.create_bullet_point(f"  Equity Trend: {trends.equity_trend.value}"))
        elements.append(self.create_bullet_point(f"  Debt Trend: {trends.debt_trend.value}"))
        elements.append(self.create_bullet_point(f"  Leverage Trend: {trends.leverage_trend.value}"))

        # Stability scores
        if trends.balance_sheet_stability_score is not None or trends.leverage_consistency_score is not None:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Stability Scores (0-10 scale):"))
            if trends.balance_sheet_stability_score is not None:
                score_color = self.get_status_color(trends.balance_sheet_stability_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Balance Sheet Stability: {trends.balance_sheet_stability_score:.1f}/10", score_color))

            if trends.leverage_consistency_score is not None:
                score_color = self.get_status_color(trends.leverage_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Leverage Consistency: {trends.leverage_consistency_score:.1f}/10", score_color))

        # Historical data table
        if trends.yearly_data:
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(self.create_subheader("Historical Balance Sheet Data"))

            # Create table data
            table_data = [
                ['Year', 'Assets', 'Equity', 'Debt', 'D/E Ratio']  # Header
            ]

            for year_data in trends.yearly_data:
                table_data.append([
                    str(year_data.year),
                    self.format_currency(year_data.total_assets, compact=True) if year_data.total_assets else "N/A",
                    self.format_currency(year_data.total_equity, compact=True) if year_data.total_equity else "N/A",
                    self.format_currency(year_data.total_debt, compact=True) if year_data.total_debt else "N/A",
                    self.format_ratio(year_data.debt_to_equity) if year_data.debt_to_equity else "N/A"
                ])

            # Create table
            col_widths = [0.6 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.8 * inch]
            table = self.create_table(table_data, col_widths)
            elements.append(table)

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_balance_sheet_health(self, assessment: BalanceSheetHealthAssessment) -> List:
        """Format balance sheet health assessment subsection."""
        elements = []

        elements.append(self.create_subheader("Balance Sheet Health Assessment"))
        elements.append(Spacer(1, 0.05 * inch))

        # Overall balance sheet health rating
        if assessment.overall_balance_sheet_rating.value != "Insufficient Data":
            rating_color = self._get_health_rating_color(assessment.overall_balance_sheet_rating)
            elements.append(self.create_bullet_point(f"Overall Balance Sheet Health: {assessment.overall_balance_sheet_rating.value}", rating_color))

            if assessment.overall_balance_sheet_score is not None:
                score_color = self.get_status_color(assessment.overall_balance_sheet_score, (7.0, 5.0))
                elements.append(self.create_bullet_point(f"Balance Sheet Score: {assessment.overall_balance_sheet_score:.1f}/10", score_color))

        # Component ratings
        component_ratings = [
            ("Liquidity Health", assessment.liquidity_health, assessment.liquidity_score),
            ("Leverage Health", assessment.leverage_health, assessment.leverage_score),
            ("Asset Quality Health", assessment.asset_quality_health, assessment.asset_quality_score),
            ("Financial Stability", assessment.financial_stability_health, assessment.financial_stability_score)
        ]

        has_component_data = any(rating.value != "Insufficient Data" for _, rating, _ in component_ratings)

        if has_component_data:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Component Health Ratings:"))

            for name, rating, score in component_ratings:
                if rating.value != "Insufficient Data":
                    rating_color = self._get_health_rating_color(rating)
                    score_text = f" ({score:.1f}/10)" if score is not None else ""
                    elements.append(self.create_bullet_point(f"  {name}: {rating.value}{score_text}", rating_color))

        # Strengths and concerns
        if assessment.strengths:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Balance Sheet Strengths:"))
            for strength in assessment.strengths:
                elements.append(self.create_bullet_point(f"  • {strength}", self.colors.GREEN))

        if assessment.concerns:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Balance Sheet Concerns:"))
            for concern in assessment.concerns:
                elements.append(self.create_bullet_point(f"  • {concern}", self.colors.RED))

        # Summary
        if assessment.summary:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Balance Sheet Summary:"))
            elements.append(self.create_bullet_point(f"  {assessment.summary}"))

        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _get_health_rating_color(self, rating):
        """Get color for health rating."""
        rating_value = rating.value.lower()
        if "excellent" in rating_value or "good" in rating_value:
            return self.colors.GREEN
        elif "fair" in rating_value:
            return self.colors.YELLOW
        elif "poor" in rating_value:
            return self.colors.RED
        else:
            return self.colors.BLACK
