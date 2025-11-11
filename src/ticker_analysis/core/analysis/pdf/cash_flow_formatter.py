"""
Cash Flow Analysis PDF Formatter

This module formats the cash flow analysis section for PDF output.
"""

from typing import List
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.units import inch

from ..models import CompanyAnalysisData
from .base_formatter import BasePDFFormatter


class CashFlowFormatter(BasePDFFormatter):
    """
    Formatter for the cash flow analysis section in PDF reports.
    """

    def format_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the cash flow analysis section.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        elements = []

        # Section header
        elements.append(self.create_section_header("💰 CASH FLOW ANALYSIS"))
        elements.append(Spacer(1, 0.1 * inch))

        # Latest quarter metrics
        if data.cash_flow_metrics:
            elements.extend(self._format_cash_flow_metrics(data.cash_flow_metrics))

        # Cash flow trends
        if data.cash_flow_trends:
            elements.extend(self._format_cash_flow_trends(data.cash_flow_trends))

        # Cash flow health
        if data.cash_flow_health:
            elements.extend(self._format_cash_flow_health(data.cash_flow_health))

        return elements

    def _format_cash_flow_metrics(self, metrics) -> List:
        """Format cash flow metrics subsection."""
        elements = []

        elements.append(self.create_subheader("Latest Quarter Cash Flow Metrics"))
        elements.append(Spacer(1, 0.05 * inch))

        # Quarter information
        if metrics.quarter_end_date:
            elements.append(self.create_bullet_point(f"Quarter End Date: {metrics.quarter_end_date}"))

        # Core cash flow metrics
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Core Cash Flow Metrics:"))
        if metrics.operating_cash_flow is not None:
            ocf_color = self.colors.GREEN if metrics.operating_cash_flow > 0 else self.colors.RED
            elements.append(self.create_bullet_point(f"  Operating Cash Flow: {self.format_currency(metrics.operating_cash_flow, compact=True)}", ocf_color))

        if metrics.free_cash_flow is not None:
            fcf_color = self.colors.GREEN if metrics.free_cash_flow > 0 else self.colors.RED
            elements.append(self.create_bullet_point(f"  Free Cash Flow: {self.format_currency(metrics.free_cash_flow, compact=True)}", fcf_color))

        elements.append(self.create_bullet_point(f"  Investing Cash Flow: {self.format_currency(metrics.investing_cash_flow, compact=True)}"))
        elements.append(self.create_bullet_point(f"  Financing Cash Flow: {self.format_currency(metrics.financing_cash_flow, compact=True)}"))
        elements.append(self.create_bullet_point(f"  Net Change in Cash: {self.format_currency(metrics.net_change_in_cash, compact=True)}"))

        # Sustainability metrics
        if any([metrics.capex_to_ocf_ratio, metrics.cash_flow_coverage_ratio]):
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Sustainability Metrics:"))
            if metrics.capital_expenditure is not None:
                elements.append(self.create_bullet_point(f"  Capital Expenditure: {self.format_currency(metrics.capital_expenditure, compact=True)}"))
            if metrics.capex_to_ocf_ratio is not None:
                ratio_color = self.get_status_color(metrics.capex_to_ocf_ratio, (0.5, 1.2))
                elements.append(self.create_bullet_point(f"  CapEx/OCF Ratio: {self.format_ratio(metrics.capex_to_ocf_ratio)}", ratio_color))
            if metrics.cash_flow_coverage_ratio is not None:
                coverage_color = self.get_status_color(metrics.cash_flow_coverage_ratio, (1.5, 0.8))
                elements.append(self.create_bullet_point(f"  Cash Flow Coverage: {self.format_ratio(metrics.cash_flow_coverage_ratio)}", coverage_color))

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_cash_flow_trends(self, trends) -> List:
        """Format cash flow trends subsection."""
        elements = []

        elements.append(self.create_subheader("Cash Flow Trends"))
        elements.append(Spacer(1, 0.05 * inch))

        # Basic trend information
        elements.append(self.create_bullet_point(f"Analysis Period: {trends.years_analyzed} years of data"))
        elements.append(self.create_bullet_point(f"Analysis Date: {trends.analysis_date}"))

        # Average growth rates
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Average Annual Growth Rates:"))
        if trends.avg_ocf_growth is not None:
            growth_color = self.get_status_color(trends.avg_ocf_growth, (0.05, -0.05))
            elements.append(self.create_bullet_point(f"  Operating Cash Flow: {self.format_percentage(trends.avg_ocf_growth / 100)}", growth_color))

        if trends.avg_fcf_growth is not None:
            growth_color = self.get_status_color(trends.avg_fcf_growth, (0.05, -0.05))
            elements.append(self.create_bullet_point(f"  Free Cash Flow: {self.format_percentage(trends.avg_fcf_growth / 100)}", growth_color))

        if trends.avg_capex_growth is not None:
            growth_color = self.get_status_color(trends.avg_capex_growth, (0.05, -0.05))
            elements.append(self.create_bullet_point(f"  Capital Expenditure: {self.format_percentage(trends.avg_capex_growth / 100)}", growth_color))

        # Trend directions
        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Trend Assessment:"))
        elements.append(self.create_bullet_point(f"  OCF Trend: {trends.ocf_trend.value}"))
        elements.append(self.create_bullet_point(f"  FCF Trend: {trends.fcf_trend.value}"))
        elements.append(self.create_bullet_point(f"  CapEx Trend: {trends.capex_trend.value}"))
        elements.append(self.create_bullet_point(f"  Cash Generation: {trends.cash_generation_trend.value}"))

        # Consistency scores
        if any([trends.ocf_consistency_score, trends.fcf_consistency_score, trends.cash_flow_stability_score]):
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Consistency Scores (0-10 scale):"))
            if trends.ocf_consistency_score is not None:
                score_color = self.get_status_color(trends.ocf_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  OCF Consistency: {trends.ocf_consistency_score:.1f}/10", score_color))

            if trends.fcf_consistency_score is not None:
                score_color = self.get_status_color(trends.fcf_consistency_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  FCF Consistency: {trends.fcf_consistency_score:.1f}/10", score_color))

            if trends.cash_flow_stability_score is not None:
                score_color = self.get_status_color(trends.cash_flow_stability_score, (7.0, 4.0))
                elements.append(self.create_bullet_point(f"  Overall Stability: {trends.cash_flow_stability_score:.1f}/10", score_color))

        # Quality metrics
        if trends.avg_ocf_to_fcf_conversion is not None:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Cash Flow Quality:"))
            conversion_color = self.get_status_color(trends.avg_ocf_to_fcf_conversion, (0.7, 0.3))
            elements.append(self.create_bullet_point(f"  OCF to FCF Conversion: {self.format_percentage(trends.avg_ocf_to_fcf_conversion)}", conversion_color))

        # Historical data table
        if trends.yearly_data:
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(self.create_subheader("Historical Cash Flow Data"))

            # Create table data
            table_data = [
                ['Year', 'Op. Cash Flow', 'Free Cash Flow', 'CapEx', 'Net Change']  # Header
            ]

            for year_data in trends.yearly_data:
                table_data.append([
                    str(year_data.year),
                    self.format_currency(year_data.operating_cash_flow, compact=True) if year_data.operating_cash_flow else "N/A",
                    self.format_currency(year_data.free_cash_flow, compact=True) if year_data.free_cash_flow else "N/A",
                    self.format_currency(year_data.capital_expenditure, compact=True) if year_data.capital_expenditure else "N/A",
                    self.format_currency(year_data.net_change_in_cash, compact=True) if year_data.net_change_in_cash else "N/A"
                ])

            # Create table
            col_widths = [0.6 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch]
            table = self.create_table(table_data, col_widths)
            elements.append(table)

        elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _format_cash_flow_health(self, assessment) -> List:
        """Format cash flow health assessment subsection."""
        elements = []

        elements.append(self.create_subheader("Cash Flow Health Assessment"))
        elements.append(Spacer(1, 0.05 * inch))

        # Overall cash flow health rating
        if assessment.overall_cash_flow_rating.value != "Insufficient Data":
            rating_color = self._get_health_rating_color(assessment.overall_cash_flow_rating)
            elements.append(self.create_bullet_point(f"Overall Cash Flow Health: {assessment.overall_cash_flow_rating.value}", rating_color))

            if assessment.overall_cash_flow_score is not None:
                score_color = self.get_status_color(assessment.overall_cash_flow_score, (7.0, 5.0))
                elements.append(self.create_bullet_point(f"Cash Flow Score: {assessment.overall_cash_flow_score:.1f}/10", score_color))

        # Component ratings
        component_ratings = [
            ("Cash Flow Quality", assessment.cash_flow_quality_health, assessment.cash_flow_quality_score),
            ("Cash Flow Sustainability", assessment.cash_flow_sustainability_health, assessment.cash_flow_sustainability_score),
            ("Cash Flow Growth", assessment.cash_flow_growth_health, assessment.cash_flow_growth_score),
            ("Cash Flow Stability", assessment.cash_flow_stability_health, assessment.cash_flow_stability_score)
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
            elements.append(self.create_subsection_header("Cash Flow Strengths:"))
            for strength in assessment.strengths:
                elements.append(self.create_bullet_point(f"  • {strength}", self.colors.GREEN))

        if assessment.concerns:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Cash Flow Concerns:"))
            for concern in assessment.concerns:
                elements.append(self.create_bullet_point(f"  • {concern}", self.colors.RED))

        # Summary
        if assessment.summary:
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(self.create_subsection_header("Cash Flow Summary:"))
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
