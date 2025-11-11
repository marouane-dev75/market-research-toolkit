"""
PDF Formatter - Main PDF Generation Class

This module provides the main PDFFormatter class that coordinates all section formatters
to generate a comprehensive PDF analysis report.
"""

from typing import List, Optional
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Paragraph
from reportlab.lib import colors

from ..models import CompanyAnalysisData
from .base_formatter import BasePDFFormatter
from .generic_metrics_formatter import GenericMetricsFormatter
from .income_statement_formatter import IncomeStatementFormatter
from .balance_sheet_formatter import BalanceSheetFormatter
from .cash_flow_formatter import CashFlowFormatter
from .technical_formatter import TechnicalFormatter


class PDFFormatter(BasePDFFormatter):
    """
    Main PDF formatter that coordinates all section formatters to generate
    a comprehensive company analysis PDF report.
    """

    def __init__(self):
        """Initialize the PDF formatter."""
        super().__init__()
        self._init_section_formatters()

    def _init_section_formatters(self):
        """Initialize all section formatters."""
        self.generic_formatter = GenericMetricsFormatter()
        self.income_statement_formatter = IncomeStatementFormatter()
        self.balance_sheet_formatter = BalanceSheetFormatter()
        self.cash_flow_formatter = CashFlowFormatter()
        self.technical_formatter = TechnicalFormatter()

    def generate_pdf(self, analysis_data: CompanyAnalysisData, filename: str) -> None:
        """
        Generate a comprehensive PDF analysis report.

        Args:
            analysis_data: CompanyAnalysisData object with all analysis results
            filename: Output PDF filename
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        # Build the story (content flow)
        story = []

        # Add title page
        story.extend(self._create_title_page(analysis_data))

        # Add all analysis sections
        story.extend(self._create_analysis_sections(analysis_data))

        # Build the PDF
        doc.build(story, onFirstPage=self._add_page_header_footer,
                 onLaterPages=self._add_page_header_footer)

    def _create_title_page(self, analysis_data: CompanyAnalysisData) -> List:
        """Create the professional title page content."""
        story = []

        # Add top spacing
        story.append(Spacer(1, 1 * inch))

        # Main title with enhanced styling
        title_style = ParagraphStyle(
            name='TitlePageTitle',
            fontName=self.fonts.BOLD,
            fontSize=24,
            textColor=self.colors.PRIMARY_TEXT,
            alignment=1,  # Center alignment
            spaceAfter=20,
            leading=28
        )

        story.append(Paragraph("COMPANY ANALYSIS REPORT", title_style))

        # Company ticker with prominent styling
        ticker_style = ParagraphStyle(
            name='TitlePageTicker',
            fontName=self.fonts.BOLD,
            fontSize=32,
            textColor=self.colors.ACCENT_BACKGROUND,
            alignment=1,  # Center alignment
            spaceAfter=40,
            leading=36
        )

        story.append(Paragraph(analysis_data.ticker, ticker_style))

        # Generation info with professional styling
        generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_style = ParagraphStyle(
            name='TitlePageInfo',
            fontName=self.fonts.NORMAL,
            fontSize=self.fonts.SMALL_SIZE,
            textColor=self.colors.SECONDARY_TEXT,
            alignment=1,  # Center alignment
            spaceAfter=60
        )

        story.append(Paragraph(f"Generated on: {generation_time}", info_style))

        # Company basic info with improved formatting
        if analysis_data.exchange or analysis_data.sector:
            basic_info_style = ParagraphStyle(
                name='TitlePageBasicInfo',
                fontName=self.fonts.NORMAL,
                fontSize=self.fonts.NORMAL_SIZE,
                textColor=self.colors.PRIMARY_TEXT,
                alignment=1,  # Center alignment
                spaceAfter=15
            )

            basic_info = []
            if analysis_data.exchange:
                basic_info.append(f"Exchange: {analysis_data.exchange}")
            if analysis_data.sector:
                basic_info.append(f"Sector: {analysis_data.sector}")

            for info in basic_info:
                story.append(Paragraph(info, basic_info_style))

        story.append(PageBreak())
        return story

    def _create_analysis_sections(self, analysis_data: CompanyAnalysisData) -> List:
        """Create all analysis sections in the correct order."""
        story = []

        # 1. Basic Info
        story.extend(self.generic_formatter.format_section('basic_info', analysis_data))

        # 2. Market Data
        story.extend(self.generic_formatter.format_section('market_data', analysis_data))

        # 3. Leverage Metrics
        story.extend(self.generic_formatter.format_section('leverage', analysis_data))

        # 4. Growth Metrics
        story.extend(self.generic_formatter.format_section('growth', analysis_data))

        # 5. Valuation Metrics
        story.extend(self.generic_formatter.format_section('valuation', analysis_data))

        # 6. Profitability Metrics
        story.extend(self.generic_formatter.format_section('profitability', analysis_data))

        # 7. Liquidity Metrics
        story.extend(self.generic_formatter.format_section('liquidity', analysis_data))

        # 8. External Analysis Sentiment
        story.extend(self.generic_formatter.format_section('external_analysis', analysis_data))

        # 9. Dividend Analysis
        story.extend(self.generic_formatter.format_dividend_analysis_section(analysis_data))

        # 10. Income Statement Header & Analysis
        story.extend(self.income_statement_formatter.format_section(analysis_data))

        # 11. Balance Sheet Header & Analysis
        story.extend(self.balance_sheet_formatter.format_section(analysis_data))

        # 12. Cash Flow Header & Analysis
        story.extend(self.cash_flow_formatter.format_section(analysis_data))

        # 13. Price Analysis Header & Analysis
        story.extend(self.generic_formatter.format_price_analysis_section(analysis_data))

        # 14. Technical Analysis Header & Analysis
        story.extend(self.technical_formatter.format_section(analysis_data))

        return story

    def _add_page_header_footer(self, canvas, doc):
        """
        Add header and footer to each page.

        Args:
            canvas: ReportLab canvas object
            doc: Document object
        """
        canvas.saveState()

        # Header
        header_text = "Company Financial Analysis Report"
        canvas.setFont(self.fonts.NORMAL, 8)
        canvas.setFillColor(self.colors.GRAY)
        canvas.drawString(self.margin, self.page_height - 0.5 * inch, header_text)

        # Footer
        footer_text = f"Page {doc.page}"
        canvas.setFont(self.fonts.NORMAL, 8)
        canvas.setFillColor(self.colors.GRAY)
        canvas.drawString(self.margin, 0.5 * inch, footer_text)

        # Generation timestamp in footer
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        canvas.drawRightString(self.page_width - self.margin, 0.5 * inch, timestamp)

        canvas.restoreState()
