"""
Generic Metrics PDF Formatter

This module provides a configurable formatter for simple metric sections
that can replace multiple individual formatters.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch

from ..models import CompanyAnalysisData
from .base_formatter import BasePDFFormatter


@dataclass
class MetricDefinition:
    """Definition for a single metric to display."""
    label: str
    value_attr: str
    formatter: Callable[[Any], str]
    color_logic: Optional[Callable[[Any], Any]] = None


@dataclass
class SectionDefinition:
    """Definition for a complete section."""
    title: str
    metrics: List[MetricDefinition]


class GenericMetricsFormatter(BasePDFFormatter):
    """
    Generic formatter for simple metric sections using configuration.

    This replaces multiple individual formatters like ValuationFormatter,
    ProfitabilityFormatter, LiquidityFormatter, etc.
    """

    def __init__(self):
        super().__init__()
        self._section_configs = self._build_section_configs()

    def _build_section_configs(self) -> Dict[str, SectionDefinition]:
        """Build configuration for all supported sections."""
        return {
            'basic_info': SectionDefinition(
                title="BASIC INFORMATION",
                metrics=[
                    MetricDefinition("Symbol", "ticker", str),
                    MetricDefinition("Exchange", "exchange", str),
                    MetricDefinition("Sector", "sector", str),
                ]
            ),
            'market_data': SectionDefinition(
                title="MARKET DATA",
                metrics=[
                    MetricDefinition("Last Price", "last_price", self.format_currency),
                    MetricDefinition("Market Cap", "market_cap",
                                   lambda x: self.format_currency(x, compact=True)),
                    MetricDefinition("Avg Volume", "avg_volume", self.format_volume),
                    MetricDefinition("52-Week Low", "fifty_two_week_low", self.format_currency),
                    MetricDefinition("52-Week High", "fifty_two_week_high", self.format_currency),
                    MetricDefinition("Dividend Yield", "dividend_yield", self.format_percentage),
                ]
            ),
            'valuation': SectionDefinition(
                title="VALUATION METRICS",
                metrics=[
                    MetricDefinition("P/E Ratio", "pe_ratio", self.format_ratio),
                    MetricDefinition("P/B Ratio", "pb_ratio", self.format_ratio),
                    MetricDefinition("Price/Sales", "price_to_sales", self.format_ratio),
                    MetricDefinition("EV/Revenue", "ev_to_revenue", self.format_ratio),
                    MetricDefinition("EV/EBITDA", "ev_to_ebitda", self.format_ratio),
                    MetricDefinition("Beta", "beta", self.format_ratio),
                    MetricDefinition("Enterprise Value", "enterprise_value",
                                   lambda x: self.format_currency(x, compact=True)),
                ]
            ),
            'profitability': SectionDefinition(
                title="PROFITABILITY METRICS",
                metrics=[
                    MetricDefinition("Profit Margins", "profit_margins", self.format_percentage),
                    MetricDefinition("Operating Margins", "operating_margins", self.format_percentage),
                    MetricDefinition("ROA", "return_on_assets", self.format_percentage),
                    MetricDefinition("ROE", "return_on_equity", self.format_percentage),
                ]
            ),
            'liquidity': SectionDefinition(
                title="LIQUIDITY METRICS",
                metrics=[
                    MetricDefinition("Current Ratio", "current_ratio", self.format_ratio),
                    MetricDefinition("Quick Ratio", "quick_ratio", self.format_ratio),
                ]
            ),
            'leverage': SectionDefinition(
                title="LEVERAGE METRICS",
                metrics=[
                    MetricDefinition("Debt/Equity", "debt_to_equity", self.format_percentage),
                ]
            ),
            'growth': SectionDefinition(
                title="GROWTH METRICS",
                metrics=[
                    MetricDefinition("Revenue Growth", "revenue_growth", self.format_percentage),
                    MetricDefinition("Earnings Growth", "earnings_growth", self.format_percentage),
                ]
            ),
            'external_analysis': SectionDefinition(
                title="EXTERNAL ANALYSIS SENTIMENT",
                metrics=[
                    MetricDefinition("Recommendation", "recommendation", str),
                    MetricDefinition("Target Price", "target_price", self.format_currency),
                ]
            ),
        }

    def format_section(self, section_name: str, data: CompanyAnalysisData) -> List:
        """
        Format a section using configuration.

        Args:
            section_name: Name of the section to format
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        if section_name not in self._section_configs:
            return []

        config = self._section_configs[section_name]
        elements = []

        # Professional section header
        elements.extend(self.create_professional_section_header(config.title))

        # Add metrics
        for metric in config.metrics:
            value = getattr(data, metric.value_attr, None)
            if value is not None:
                formatted_value = metric.formatter(value)
                color = metric.color_logic(value) if metric.color_logic else None
                elements.append(self.create_metric_display(metric.label, formatted_value, color))

        # Add section spacing
        elements.append(self.create_spacing("section"))

        return elements

    def format_price_analysis_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the price analysis section with nested data access.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        elements = []

        if not data.price_analysis:
            return elements

        analysis = data.price_analysis

        # Professional section header
        elements.extend(self.create_professional_section_header("PRICE ANALYSIS"))

        elements.append(self.create_subheader("Current Price & Performance"))

        # Current price information
        if analysis.current_price is not None:
            elements.append(self.create_metric_display("Current Price", self.format_currency(analysis.current_price)))
        if analysis.previous_close is not None:
            elements.append(self.create_metric_display("Previous Close", self.format_currency(analysis.previous_close)))

        # Daily change
        if analysis.daily_change is not None and analysis.daily_change_percent is not None:
            change_color = self.colors.SUCCESS_GREEN if analysis.daily_change > 0 else self.colors.WARNING_RED if analysis.daily_change < 0 else self.colors.BLACK
            change_text = f"{self.format_currency(analysis.daily_change, show_sign=True)} ({self.format_percentage(analysis.daily_change_percent, show_sign=True, multiply_by_100=False)})"
            elements.append(self.create_metric_display("Daily Change", change_text, change_color))

        # 52-week range
        if analysis.fifty_two_week_high is not None and analysis.fifty_two_week_low is not None:
            range_text = f"{self.format_currency(analysis.fifty_two_week_low)} - {self.format_currency(analysis.fifty_two_week_high)}"
            elements.append(self.create_metric_display("52-Week Range", range_text))

        # Volume information
        if analysis.current_volume is not None:
            elements.append(self.create_metric_display("Current Volume", self.format_volume(analysis.current_volume)))
        if analysis.average_volume is not None:
            elements.append(self.create_metric_display("Average Volume", self.format_volume(analysis.average_volume)))
        if analysis.volume_ratio is not None:
            volume_color = self.colors.SUCCESS_GREEN if analysis.volume_ratio > 1.5 else self.colors.CAUTION_YELLOW if analysis.volume_ratio > 0.5 else self.colors.WARNING_RED
            elements.append(self.create_metric_display("Volume Ratio", f"{analysis.volume_ratio:.2f}x", volume_color))

        # Period performance
        elements.append(self.create_subsection_header("Period Performance:"))

        # 7-day change
        if analysis.seven_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.seven_day_change_percent)
            elements.append(self.create_bullet_point(f"  7-Day Change: {self.format_percentage(analysis.seven_day_change_percent / 100, show_sign=True)}", change_color))

        # 30-day change
        if analysis.thirty_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.thirty_day_change_percent)
            elements.append(self.create_bullet_point(f"  30-Day Change: {self.format_percentage(analysis.thirty_day_change_percent / 100, show_sign=True)}", change_color))

        # 90-day change
        if analysis.ninety_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.ninety_day_change_percent)
            elements.append(self.create_bullet_point(f"  90-Day Change: {self.format_percentage(analysis.ninety_day_change_percent / 100, show_sign=True)}", change_color))

        elements.append(self.create_spacing("section"))
        return elements

    def format_dividend_analysis_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the dividend analysis section with nested data access.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        from reportlab.platypus import Table

        elements = []

        if not data.dividend_analysis:
            return elements

        analysis = data.dividend_analysis

        # Professional section header
        elements.extend(self.create_professional_section_header("DIVIDEND ANALYSIS"))

        # Basic dividend information
        elements.append(self.create_metric_display("Dividend History", f"{analysis.total_years} years of data"))
        elements.append(self.create_metric_display("Total Payments", str(analysis.total_payments)))

        # Recent performance
        if analysis.trailing_12_month_total is not None:
            elements.append(self.create_metric_display("Trailing 12M Total", self.format_currency(analysis.trailing_12_month_total)))

        # Yearly extremes
        elements.append(self.create_metric_display("Highest Year", f"{self.format_currency(analysis.highest_year_amount)} ({analysis.highest_year})"))
        elements.append(self.create_metric_display("Lowest Year", f"{self.format_currency(analysis.lowest_year_amount)} ({analysis.lowest_year})"))

        # Trend analysis
        elements.append(self.create_metric_display("Dividend Trend", analysis.dividend_trend.value))

        if analysis.average_growth_rate is not None:
            elements.append(self.create_metric_display("Avg Growth Rate", f"{self.format_percentage(analysis.average_growth_rate / 100)} per year"))

        if analysis.year_over_year_variance is not None:
            elements.append(self.create_metric_display("Year-over-Year Var", self.format_percentage(analysis.year_over_year_variance / 100)))

        # Consistency score
        if analysis.consistency_score is not None:
            elements.append(self.create_metric_display("Consistency Score", f"{analysis.consistency_score:.1f}/10"))

        # Years without dividends
        if analysis.years_without_dividends:
            years_str = ", ".join(str(year) for year in analysis.years_without_dividends)
            elements.append(self.create_metric_display("Years Without Dividends", years_str, self.colors.WARNING_RED))

        # Display recent yearly data (last 5 years)
        if analysis.yearly_data:
            elements.append(self.create_subheader("Recent Yearly Dividends"))

            recent_years = analysis.yearly_data[:5]  # Most recent 5 years

            # Create table data
            table_data = [
                ['Year', 'Total', 'Payments']  # Header
            ]

            for year_data in recent_years:
                table_data.append([
                    str(year_data.year),
                    self.format_currency(year_data.total_amount),
                    str(year_data.payment_count)
                ])

            # Create table
            col_widths = [0.8 * inch, 1.2 * inch, 1.0 * inch]
            table = self.create_table(table_data, col_widths)
            elements.append(table)

        elements.append(self.create_spacing("section"))
        return elements

    def _get_performance_color(self, change_percent: float) -> object:
        """Get color for performance display."""
        if change_percent > 5:
            return self.colors.SUCCESS_GREEN
        elif change_percent > 0:
            return self.colors.SUCCESS_GREEN
        elif change_percent > -5:
            return self.colors.WARNING_RED
        else:
            return self.colors.WARNING_RED
