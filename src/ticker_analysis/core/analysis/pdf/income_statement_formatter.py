"""
Income Statement Analysis PDF Formatter

This module formats the income statement analysis section for PDF output.
"""

from typing import List
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.units import inch

from ..models import CompanyAnalysisData
from ..income_statement import FinancialHealthRating, TrendDirection
from .base_formatter import BasePDFFormatter


class IncomeStatementFormatter(BasePDFFormatter):
    """
    Formatter for the income statement analysis section in PDF reports.
    """

    def format_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the income statement analysis section.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        elements = []

        # Section header
        elements.append(self.create_section_header("📊 INCOME STATEMENT ANALYSIS"))
        elements.append(Spacer(1, 0.1 * inch))

        # Latest quarter metrics
        if data.income_statement_metrics:
            elements.extend(self._format_latest_quarter_metrics(data.income_statement_metrics))

        # Trend analysis
        if data.trend_analysis:
            elements.extend(self._format_trend_analysis(data.trend_analysis))

        # Financial health assessment
        if data.financial_health_assessment:
            elements.extend(self._format_financial_health_assessment(data.financial_health_assessment))

        return elements

    def _format_latest_quarter_metrics(self, metrics) -> List:
        """Format latest quarter metrics subsection."""
        elements = []

        elements.append(self.create_subheader("Latest Quarter Performance"))
        elements.append(Spacer(1, 0.05 * inch))

        # Quarter information
        if metrics.quarter_end_date:
            elements.append(self.create_bullet_point(f"Quarter End Date: {metrics.quarter_end_date}"))

        # Core financial metrics
        elements.append(self.create_bullet_point(f"Revenue: {self.format_currency(metrics.latest_quarter_revenue, compact=True)}"))
        elements.append(self.create_bullet_point(f"Net Income: {self.format_currency(metrics.latest_quarter_net_income, compact=True)}"))
        elements.append(self.create_bullet_point(f"Operating Income: {self.format_currency(metrics.latest_quarter_operating_income, compact=True)}"))
        elements.append(self.create_bullet_point(f"Diluted EPS: {self.format_eps(metrics.latest_quarter_eps)}"))

        # Additional metrics if available
        if metrics.latest_quarter_gross_profit is not None:
            elements.append(self.create_bullet_point(f"Gross Profit: {self.format_currency(metrics.latest_quarter_gross_profit, compact=True)}"))
        if metrics.latest_quarter_ebitda is not None:
            elements.append(self.create_bullet_point(f"EBITDA: {self.format_currency(metrics.latest_quarter_ebitda, compact=True)}"))

        # Margin analysis
        if any([metrics.net_profit_margin, metrics.operating_margin, metrics.gross_margin]):
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Profitability Margins:"))
            if metrics.net_profit_margin is not None:
                elements.append(self.create_bullet_point(f"  Net Profit Margin: {self.format_percentage(metrics.net_profit_margin / 100)}"))
            if metrics.operating_margin is not None:
                elements.append(self.create_bullet_point(f"  Operating Margin: {self.format_percentage(metrics.operating_margin / 100)}"))
            if metrics.gross_margin is not None:
                elements.append(self.create_bullet_point(f"  Gross Margin: {self.format_percentage(metrics.gross_margin / 100)}"))

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_trend_analysis(self, trends) -> List:
        """Format trend analysis subsection."""
        elements = []

        elements.append(self.create_subheader("3-Year Financial Trends"))
        elements.append(Spacer(1, 0.05 * inch))

        # Basic trend information
        elements.append(self.create_bullet_point(f"Analysis Period: {trends.years_analyzed} years of data"))
        elements.append(self.create_bullet_point(f"Analysis Date: {trends.analysis_date}"))

        # Average growth rates
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Average Annual Growth Rates:"))
        if trends.avg_revenue_growth is not None:
            growth_color = self.get_status_color(trends.avg_revenue_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Revenue Growth: {self.format_percentage(trends.avg_revenue_growth / 100)}", growth_color))

        if trends.avg_net_income_growth is not None:
            growth_color = self.get_status_color(trends.avg_net_income_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Net Income Growth: {self.format_percentage(trends.avg_net_income_growth / 100)}", growth_color))

        if trends.avg_operating_income_growth is not None:
            growth_color = self.get_status_color(trends.avg_operating_income_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  Operating Growth: {self.format_percentage(trends.avg_operating_income_growth / 100)}", growth_color))

        if trends.avg_eps_growth is not None:
            growth_color = self.get_status_color(trends.avg_eps_growth, (0.03, -0.03))
            elements.append(self.create_bullet_point(f"  EPS Growth: {self.format_percentage(trends.avg_eps_growth / 100)}", growth_color))

        # Trend directions
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Trend Assessment:"))
        elements.append(self.create_bullet_point(f"  Revenue Trend: {self._format_trend_direction(trends.revenue_trend)}"))
        elements.append(self.create_bullet_point(f"  Net Income Trend: {self._format_trend_direction(trends.net_income_trend)}"))
        elements.append(self.create_bullet_point(f"  Operating Trend: {self._format_trend_direction(trends.operating_income_trend)}"))
        elements.append(self.create_bullet_point(f"  Earnings Trend: {self._format_trend_direction(trends.earnings_trend)}"))

        # Consistency scores
        if any([trends.revenue_consistency_score, trends.earnings_consistency_score, trends.overall_consistency_score]):
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Consistency Scores (0-10 scale):"))
            if trends.revenue_consistency_score is not None:
                score_color = self.get_status_color(trends.revenue_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Revenue Consistency: {trends.revenue_consistency_score:.1f}/10", score_color))

            if trends.earnings_consistency_score is not None:
                score_color = self.get_status_color(trends.earnings_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Earnings Consistency: {trends.earnings_consistency_score:.1f}/10", score_color))

            if trends.overall_consistency_score is not None:
                score_color = self.get_status_color(trends.overall_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Overall Consistency: {trends.overall_consistency_score:.1f}/10", score_color))

        # Historical data table
        if trends.yearly_data:
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(self.create_subheader("Historical Financial Data"))

            # Create table data
            table_data = [
                ['Year', 'Revenue', 'Net Income', 'Operating', 'EPS']  # Header
            ]

            for year_data in trends.yearly_data:
                table_data.append([
                    str(year_data.year),
                    self.format_currency(year_data.revenue, compact=True) if year_data.revenue else "N/A",
                    self.format_currency(year_data.net_income, compact=True) if year_data.net_income else "N/A",
                    self.format_currency(year_data.operating_income, compact=True) if year_data.operating_income else "N/A",
                    self.format_eps(year_data.eps) if year_data.eps else "N/A"
                ])

            # Create table
            col_widths = [0.6 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.8 * inch]
            table = self.create_table(table_data, col_widths)
            elements.append(table)

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_financial_health_assessment(self, assessment) -> List:
        """Format financial health assessment subsection."""
        elements = []

        elements.append(self.create_subheader("Financial Health Assessment"))
        elements.append(Spacer(1, 0.05 * inch))

        # Overall health rating
        if assessment.overall_health_rating != FinancialHealthRating.INSUFFICIENT_DATA:
            rating_color = self._get_health_rating_color(assessment.overall_health_rating)
            elements.append(self.create_bullet_point(f"Overall Health: {assessment.overall_health_rating.value}", rating_color))

            if assessment.overall_health_score is not None:
                score_color = self.get_status_color(assessment.overall_health_score, (7.0, 5.0))
                elements.append(self.create_bullet_point(f"Health Score: {assessment.overall_health_score:.1f}/10", score_color))

        # Component ratings
        component_ratings = [
            ("Revenue Health", assessment.revenue_health, assessment.revenue_score),
            ("Profitability Health", assessment.profitability_health, assessment.profitability_score),
            ("Growth Health", assessment.growth_health, assessment.growth_score),
            ("Consistency Health", assessment.consistency_health, assessment.consistency_score)
        ]

        has_component_data = any(rating != FinancialHealthRating.INSUFFICIENT_DATA for _, rating, _ in component_ratings)

        if has_component_data:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Component Health Ratings:"))

            for name, rating, score in component_ratings:
                if rating != FinancialHealthRating.INSUFFICIENT_DATA:
                    rating_color = self._get_health_rating_color(rating)
                    score_text = f" ({score:.1f}/10)" if score is not None else ""
                    elements.append(self.create_bullet_point(f"  {name}: {rating.value}{score_text}", rating_color))

        # Strengths and concerns
        if assessment.strengths:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Key Strengths:"))
            for strength in assessment.strengths:
                elements.append(self.create_bullet_point(f"  • {strength}", self.colors.GREEN))

        if assessment.concerns:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Areas of Concern:"))
            for concern in assessment.concerns:
                elements.append(self.create_bullet_point(f"  • {concern}", self.colors.RED))

        # Summary
        if assessment.summary:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Summary:"))
            elements.append(self.create_bullet_point(f"  {assessment.summary}"))

        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _format_trend_direction(self, trend: TrendDirection) -> str:
        """Format trend direction with color."""
        if trend == TrendDirection.STRONG_GROWTH:
            return "Strong Growth"
        elif trend == TrendDirection.MODERATE_GROWTH:
            return "Moderate Growth"
        elif trend == TrendDirection.STABLE:
            return "Stable"
        elif trend == TrendDirection.DECLINING:
            return "Declining"
        elif trend == TrendDirection.VOLATILE:
            return "Volatile"
        else:
            return trend.value

    def _get_health_rating_color(self, rating: FinancialHealthRating):
        """Get color for health rating."""
        if rating == FinancialHealthRating.EXCELLENT:
            return self.colors.GREEN
        elif rating == FinancialHealthRating.GOOD:
            return self.colors.GREEN
        elif rating == FinancialHealthRating.FAIR:
            return self.colors.YELLOW
        elif rating == FinancialHealthRating.POOR:
            return self.colors.RED
        else:
            return self.colors.BLACK
