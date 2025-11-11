"""
Technical Analysis PDF Formatter

This module formats the technical analysis section for PDF output.
"""

from typing import List
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch

from ..models import CompanyAnalysisData
from ..technical import TechnicalSignal
from .base_formatter import BasePDFFormatter


class TechnicalFormatter(BasePDFFormatter):
    """
    Formatter for the technical analysis section in PDF reports.
    """

    def format_section(self, data: CompanyAnalysisData) -> List:
        """
        Format the technical analysis section.

        Args:
            data: CompanyAnalysisData object

        Returns:
            List of PDF elements for this section
        """
        elements = []

        if not data.technical_analysis:
            return elements

        analysis = data.technical_analysis

        # Professional section header
        elements.extend(self.create_professional_section_header("TECHNICAL ANALYSIS"))

        # Overall technical assessment
        elements.append(self.create_subheader("Overall Technical Assessment"))
        elements.append(self.create_spacing("small"))

        if analysis.overall_score is not None:
            score_color = self.get_score_color(analysis.overall_score)
            elements.append(self.create_metric_display("Technical Score", f"{analysis.overall_score:.1f}/10", score_color))

        if analysis.overall_signal:
            signal_color = self.get_signal_color(analysis.overall_signal.value)
            elements.append(self.create_metric_display("Overall Signal", analysis.overall_signal.value, signal_color))

        if analysis.confidence_level is not None:
            elements.append(self.create_metric_display("Confidence Level", f"{analysis.confidence_level:.0f}%"))

        # Signal summary
        elements.append(self.create_metric_display("Bullish Indicators", str(analysis.bullish_indicators)))
        elements.append(self.create_metric_display("Bearish Indicators", str(analysis.bearish_indicators)))
        elements.append(self.create_metric_display("Neutral Indicators", str(analysis.neutral_indicators)))

        # Individual indicators
        if analysis.macd:
            elements.extend(self._format_macd_analysis(analysis.macd))

        if analysis.rsi:
            elements.extend(self._format_rsi_analysis(analysis.rsi))

        if analysis.moving_averages:
            elements.extend(self._format_moving_averages_analysis(analysis.moving_averages))

        if analysis.bollinger_bands:
            elements.extend(self._format_bollinger_bands_analysis(analysis.bollinger_bands))

        elements.append(Spacer(1, 0.2 * inch))

        return elements

    def _format_macd_analysis(self, macd) -> List:
        """Format MACD analysis section."""
        elements = []

        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("MACD Analysis:"))

        if macd.macd_line is not None:
            elements.append(self.create_bullet_point(f"  MACD Line: {self.format_ratio(macd.macd_line)}"))
        if macd.signal_line is not None:
            elements.append(self.create_bullet_point(f"  Signal Line: {self.format_ratio(macd.signal_line)}"))
        if macd.histogram is not None:
            hist_color = self.colors.SUCCESS_GREEN if macd.histogram > 0 else self.colors.WARNING_RED
            elements.append(self.create_bullet_point(f"  Histogram: {self.format_ratio(macd.histogram)}", hist_color))

        if macd.signal:
            signal_color = self.get_signal_color(macd.signal.value)
            elements.append(self.create_bullet_point(f"  MACD Signal: {macd.signal.value}", signal_color))

        if macd.score is not None:
            score_color = self.get_score_color(macd.score)
            elements.append(self.create_bullet_point(f"  MACD Score: {macd.score:.1f}/10", score_color))

        return elements

    def _format_rsi_analysis(self, rsi) -> List:
        """Format RSI analysis section."""
        elements = []

        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("RSI Analysis:"))

        if rsi.rsi_value is not None:
            rsi_color = self.colors.WARNING_RED if rsi.is_overbought else self.colors.SUCCESS_GREEN if rsi.is_oversold else self.colors.CAUTION_YELLOW
            elements.append(self.create_bullet_point(f"  RSI Value: {rsi.rsi_value:.1f}", rsi_color))

        if rsi.is_overbought:
            elements.append(self.create_bullet_point("  Status: Overbought (>70)", self.colors.WARNING_RED))
        elif rsi.is_oversold:
            elements.append(self.create_bullet_point("  Status: Oversold (<30)", self.colors.SUCCESS_GREEN))
        else:
            elements.append(self.create_bullet_point("  Status: Normal (30-70)", self.colors.CAUTION_YELLOW))

        if rsi.signal:
            signal_color = self.get_signal_color(rsi.signal.value)
            elements.append(self.create_bullet_point(f"  RSI Signal: {rsi.signal.value}", signal_color))

        if rsi.score is not None:
            score_color = self.get_score_color(rsi.score)
            elements.append(self.create_bullet_point(f"  RSI Score: {rsi.score:.1f}/10", score_color))

        return elements

    def _format_moving_averages_analysis(self, ma) -> List:
        """Format moving averages analysis section."""
        elements = []

        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Moving Averages Analysis:"))

        if ma.current_price is not None:
            elements.append(self.create_bullet_point(f"  Current Price: {self.format_currency(ma.current_price)}"))

        if ma.sma_20 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_20 else "Below"
            color = self.colors.SUCCESS_GREEN if price_vs_sma == "Above" else self.colors.WARNING_RED
            elements.append(self.create_bullet_point(f"  SMA 20: {self.format_currency(ma.sma_20)} ({price_vs_sma})", color))

        if ma.sma_50 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_50 else "Below"
            color = self.colors.SUCCESS_GREEN if price_vs_sma == "Above" else self.colors.WARNING_RED
            elements.append(self.create_bullet_point(f"  SMA 50: {self.format_currency(ma.sma_50)} ({price_vs_sma})", color))

        if ma.sma_200 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_200 else "Below"
            color = self.colors.SUCCESS_GREEN if price_vs_sma == "Above" else self.colors.WARNING_RED
            elements.append(self.create_bullet_point(f"  SMA 200: {self.format_currency(ma.sma_200)} ({price_vs_sma})", color))

        if ma.ema_12 is not None:
            elements.append(self.create_bullet_point(f"  EMA 12: {self.format_currency(ma.ema_12)}"))

        if ma.ema_26 is not None:
            elements.append(self.create_bullet_point(f"  EMA 26: {self.format_currency(ma.ema_26)}"))

        if ma.trend_strength:
            trend_color = self.get_trend_color(ma.trend_strength)
            elements.append(self.create_bullet_point(f"  Trend Strength: {ma.trend_strength}", trend_color))

        if ma.signal:
            signal_color = self.get_signal_color(ma.signal.value)
            elements.append(self.create_bullet_point(f"  MA Signal: {ma.signal.value}", signal_color))

        if ma.score is not None:
            score_color = self.get_score_color(ma.score)
            elements.append(self.create_bullet_point(f"  MA Score: {ma.score:.1f}/10", score_color))

        return elements

    def _format_bollinger_bands_analysis(self, bb) -> List:
        """Format Bollinger Bands analysis section."""
        elements = []

        elements.append(Spacer(1, 0.05 * inch))
        elements.append(self.create_subsection_header("Bollinger Bands Analysis:"))

        if bb.current_price is not None:
            elements.append(self.create_bullet_point(f"  Current Price: {self.format_currency(bb.current_price)}"))

        if bb.upper_band is not None:
            elements.append(self.create_bullet_point(f"  Upper Band: {self.format_currency(bb.upper_band)}"))

        if bb.middle_band is not None:
            elements.append(self.create_bullet_point(f"  Middle Band: {self.format_currency(bb.middle_band)}"))

        if bb.lower_band is not None:
            elements.append(self.create_bullet_point(f"  Lower Band: {self.format_currency(bb.lower_band)}"))

        if bb.percent_b is not None:
            position = "Above Upper" if bb.percent_b > 100 else "Below Lower" if bb.percent_b < 0 else "Within Bands"
            position_color = self.colors.WARNING_RED if bb.percent_b > 100 or bb.percent_b < 0 else self.colors.SUCCESS_GREEN
            elements.append(self.create_bullet_point(f"  %B Position: {bb.percent_b:.1f}% ({position})", position_color))

        if bb.bandwidth is not None:
            elements.append(self.create_bullet_point(f"  Bandwidth: {bb.bandwidth:.2f}%"))

        if bb.squeeze:
            elements.append(self.create_bullet_point("  Squeeze: Yes (Low Volatility)", self.colors.CAUTION_YELLOW))
        else:
            elements.append(self.create_bullet_point("  Squeeze: No"))

        if bb.signal:
            signal_color = self.get_signal_color(bb.signal.value)
            elements.append(self.create_bullet_point(f"  BB Signal: {bb.signal.value}", signal_color))

        if bb.score is not None:
            score_color = self.get_score_color(bb.score)
            elements.append(self.create_bullet_point(f"  BB Score: {bb.score:.1f}/10", score_color))

        return elements
