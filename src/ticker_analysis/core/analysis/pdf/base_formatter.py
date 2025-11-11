"""
Base PDF Formatter

This module provides the base class and common utilities for PDF formatting,
including colors, fonts, and shared formatting functions.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


@dataclass
class PDFColors:
    """Enhanced color constants for professional PDF formatting."""
    # Status colors - more sophisticated palette
    SUCCESS_GREEN = colors.Color(0.15, 0.6, 0.3)    # Professional green
    WARNING_RED = colors.Color(0.8, 0.25, 0.2)      # Professional red
    CAUTION_YELLOW = colors.Color(0.95, 0.6, 0.1)   # Professional amber
    INFO_BLUE = colors.Color(0.2, 0.4, 0.8)         # Professional blue

    # Legacy aliases removed - use descriptive names above

    # Text colors
    PRIMARY_TEXT = colors.Color(0.2, 0.2, 0.2)      # Dark gray for better readability
    SECONDARY_TEXT = colors.Color(0.4, 0.4, 0.4)    # Medium gray for secondary text
    BLACK = colors.black
    WHITE = colors.white
    GRAY = colors.Color(0.6, 0.6, 0.6)              # Light gray

    # Background colors - professional palette
    PAGE_BACKGROUND = colors.white
    HEADER_BACKGROUND = colors.Color(0.95, 0.97, 1.0)  # Very light blue
    SECTION_BACKGROUND = colors.Color(0.98, 0.98, 0.98) # Very light gray
    ACCENT_BACKGROUND = colors.Color(0.1, 0.3, 0.6)     # Professional blue

    # Border colors
    LIGHT_BORDER = colors.Color(0.8, 0.8, 0.8)
    MEDIUM_BORDER = colors.Color(0.6, 0.6, 0.6)
    DARK_BORDER = colors.Color(0.3, 0.3, 0.3)

    # Legacy aliases
    LIGHT_GRAY = SECTION_BACKGROUND
    HEADER_BLUE = ACCENT_BACKGROUND


@dataclass
class PDFFonts:
    """Enhanced font system with professional typography."""
    # Font families
    PRIMARY = "Helvetica"
    TITLE = "Helvetica-Bold"
    HEADER = "Helvetica-Bold"
    SUBHEADER = "Helvetica-Bold"
    NORMAL = "Helvetica"
    BOLD = "Helvetica-Bold"
    ITALIC = "Helvetica-Oblique"
    BOLD_ITALIC = "Helvetica-BoldOblique"

    # Size hierarchy - improved proportions
    TITLE_SIZE = 18
    HEADER_SIZE = 14
    SUBHEADER_SIZE = 12
    NORMAL_SIZE = 10
    SMALL_SIZE = 8
    TINY_SIZE = 6

    # Line heights for better spacing
    TITLE_LINE_HEIGHT = 1.2
    HEADER_LINE_HEIGHT = 1.3
    NORMAL_LINE_HEIGHT = 1.4


class BasePDFFormatter:
    """
    Base class for PDF formatters with common utilities and formatting functions.
    """

    def __init__(self):
        """Initialize the base PDF formatter."""
        self.colors = PDFColors()
        self.fonts = PDFFonts()
        self.page_width, self.page_height = A4  # Use A4 for better international compatibility
        self.margin = 0.75 * inch
        self.content_width = self.page_width - 2 * self.margin

        # Initialize styles
        self._setup_styles()

    def _setup_styles(self):
        """Set up enhanced paragraph styles for professional formatting."""
        self.styles = getSampleStyleSheet()

        # Title style - enhanced
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            fontName=self.fonts.TITLE,
            fontSize=self.fonts.TITLE_SIZE,
            spaceAfter=24,
            spaceBefore=12,
            textColor=self.colors.PRIMARY_TEXT,
            alignment=1  # Center alignment
        ))

        # Header style - enhanced
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            fontName=self.fonts.HEADER,
            fontSize=self.fonts.HEADER_SIZE,
            spaceAfter=16,
            spaceBefore=20,
            textColor=self.colors.ACCENT_BACKGROUND,
            leading=self.fonts.HEADER_SIZE * self.fonts.HEADER_LINE_HEIGHT
        ))

        # Subheader style - enhanced
        self.styles.add(ParagraphStyle(
            name='CustomSubheader',
            fontName=self.fonts.SUBHEADER,
            fontSize=self.fonts.SUBHEADER_SIZE,
            spaceAfter=12,
            spaceBefore=8,
            textColor=self.colors.PRIMARY_TEXT,
            leading=self.fonts.SUBHEADER_SIZE * self.fonts.NORMAL_LINE_HEIGHT
        ))

        # Normal style - enhanced
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            fontName=self.fonts.NORMAL,
            fontSize=self.fonts.NORMAL_SIZE,
            spaceAfter=10,
            textColor=self.colors.PRIMARY_TEXT,
            leading=self.fonts.NORMAL_SIZE * self.fonts.NORMAL_LINE_HEIGHT
        ))

        # Small style - enhanced
        self.styles.add(ParagraphStyle(
            name='CustomSmall',
            fontName=self.fonts.NORMAL,
            fontSize=self.fonts.SMALL_SIZE,
            spaceAfter=6,
            textColor=self.colors.SECONDARY_TEXT,
            leading=self.fonts.SMALL_SIZE * self.fonts.NORMAL_LINE_HEIGHT
        ))

        # Professional bullet point style
        self.styles.add(ParagraphStyle(
            name='ProfessionalBullet',
            parent=self.styles['CustomNormal'],
            leftIndent=15,
            firstLineIndent=-15,
            bulletIndent=0,
            spaceAfter=8
        ))

        # Subsection header style - for analysis, assessment, and summary sections
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            fontName=self.fonts.BOLD,
            fontSize=self.fonts.NORMAL_SIZE,
            textColor=self.colors.GRAY,
            spaceAfter=6,
            spaceBefore=4,
            leftIndent=10
        ))

    def create_colored_paragraph(self, text: str, color: colors.Color = None) -> Paragraph:
        """
        Create a paragraph with optional color.

        Args:
            text: Text content
            color: Optional color for the text

        Returns:
            Paragraph object
        """
        style = ParagraphStyle(
            name='ColoredNormal',
            parent=self.styles['CustomNormal'],
            textColor=color or self.colors.BLACK
        )
        return Paragraph(text, style)

    def create_table(self, data: List[List], col_widths: List[float] = None,
                    style_commands: List = None) -> Table:
        """
        Create a formatted table.

        Args:
            data: Table data as list of lists
            col_widths: Optional column widths
            style_commands: Optional table style commands

        Returns:
            Table object
        """
        table = Table(data, colWidths=col_widths)

        # Default style
        default_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors.LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors.BLACK),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.fonts.BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), self.fonts.NORMAL_SIZE),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors.WHITE),
            ('GRID', (0, 0), (-1, -1), 1, self.colors.GRAY),
            ('FONTNAME', (0, 1), (-1, -1), self.fonts.NORMAL),
            ('FONTSIZE', (0, 1), (-1, -1), self.fonts.SMALL_SIZE),
        ])

        # Apply custom style commands if provided
        if style_commands:
            for cmd in style_commands:
                default_style.add(*cmd)

        table.setStyle(default_style)
        return table

    def format_currency(self, value: Optional[float], compact: bool = False, show_sign: bool = False) -> str:
        """
        Format currency values.

        Args:
            value: Numeric value
            compact: Use compact notation for large numbers
            show_sign: Whether to show + for positive values

        Returns:
            Formatted currency string
        """
        if value is None:
            return "N/A"

        sign = "+" if show_sign and value > 0 else ""

        if compact and abs(value) >= 1e9:
            return f"{sign}{value/1e9:.1f}B"
        elif compact and abs(value) >= 1e6:
            return f"{sign}{value/1e6:.1f}M"
        elif compact and abs(value) >= 1e3:
            return f"{sign}{value/1e3:.1f}K"
        else:
            return f"{sign}{value:.2f}"

    def format_percentage(self, value: Optional[float], show_sign: bool = False, multiply_by_100: bool = True) -> str:
        """
        Format percentage values.

        Args:
            value: Numeric value (as decimal, e.g., 0.15 for 15%)
            show_sign: Include +/- sign
            multiply_by_100: Whether to multiply by 100 (for decimal values like 0.15 -> 15%)

        Returns:
            Formatted percentage string
        """
        if value is None:
            return "N/A"

        # Convert to percentage if needed
        if multiply_by_100:
            value *= 100

        sign = "+" if show_sign and value > 0 else ""
        return f"{sign}{value:.2f}%"

    def format_ratio(self, value: Optional[float]) -> str:
        """
        Format ratio values.

        Args:
            value: Numeric value

        Returns:
            Formatted ratio string
        """
        if value is None:
            return "N/A"
        return f"{value:.2f}"

    def format_volume(self, value: Optional[float]) -> str:
        """
        Format volume values.

        Args:
            value: Numeric value

        Returns:
            Formatted volume string
        """
        if value is None:
            return "N/A"

        if value >= 1e9:
            return f"{value/1e9:.1f}B"
        elif value >= 1e6:
            return f"{value/1e6:.1f}M"
        elif value >= 1e3:
            return f"{value/1e3:.1f}K"
        else:
            return f"{value:,.0f}"

    def format_eps(self, value: Optional[float]) -> str:
        """
        Format EPS values.

        Args:
            value: Numeric value

        Returns:
            Formatted EPS string
        """
        if value is None:
            return "N/A"
        return f"{value:.2f}"

    def get_status_color(self, value: float, thresholds: Tuple[float, float]) -> colors.Color:
        """
        Get color based on value thresholds.

        Args:
            value: Numeric value to evaluate
            thresholds: Tuple of (good_threshold, bad_threshold)

        Returns:
            Color based on thresholds
        """
        good_threshold, bad_threshold = thresholds

        if value >= good_threshold:
            return self.colors.SUCCESS_GREEN
        elif value <= bad_threshold:
            return self.colors.WARNING_RED
        else:
            return self.colors.CAUTION_YELLOW

    def get_score_color(self, score: float, excellent_threshold: float = 8.0,
                       good_threshold: float = 6.0, fair_threshold: float = 4.0) -> colors.Color:
        """
        Get color for score-based metrics (0-10 scale).

        Args:
            score: Score value (0-10)
            excellent_threshold: Threshold for excellent (green)
            good_threshold: Threshold for good (green)
            fair_threshold: Threshold for fair (yellow)

        Returns:
            Color based on score
        """
        if score >= excellent_threshold:
            return self.colors.SUCCESS_GREEN
        elif score >= good_threshold:
            return self.colors.SUCCESS_GREEN
        elif score >= fair_threshold:
            return self.colors.CAUTION_YELLOW
        else:
            return self.colors.WARNING_RED

    def get_signal_color(self, signal_value: str) -> colors.Color:
        """
        Get color for signal-based values (buy/sell/hold signals).

        Args:
            signal_value: Signal string (case-insensitive)

        Returns:
            Color based on signal type
        """
        signal_lower = signal_value.lower() if signal_value else ""

        if any(term in signal_lower for term in ['strong_buy', 'buy', 'bullish']):
            return self.colors.SUCCESS_GREEN
        elif any(term in signal_lower for term in ['strong_sell', 'sell', 'bearish']):
            return self.colors.WARNING_RED
        else:
            return self.colors.CAUTION_YELLOW

    def get_trend_color(self, trend_value: str) -> colors.Color:
        """
        Get color for trend-based values.

        Args:
            trend_value: Trend description string

        Returns:
            Color based on trend direction
        """
        trend_lower = trend_value.lower() if trend_value else ""

        if any(term in trend_lower for term in ['strong_uptrend', 'uptrend', 'bullish']):
            return self.colors.SUCCESS_GREEN
        elif any(term in trend_lower for term in ['strong_downtrend', 'downtrend', 'bearish']):
            return self.colors.WARNING_RED
        else:
            return self.colors.CAUTION_YELLOW

    def get_health_rating_color(self, rating_value: str) -> colors.Color:
        """
        Get color for health rating values.

        Args:
            rating_value: Health rating string

        Returns:
            Color based on rating
        """
        rating_lower = rating_value.lower() if rating_value else ""

        if 'excellent' in rating_lower:
            return self.colors.SUCCESS_GREEN
        elif 'good' in rating_lower:
            return self.colors.SUCCESS_GREEN
        elif 'fair' in rating_lower:
            return self.colors.CAUTION_YELLOW
        elif any(term in rating_lower for term in ['poor', 'weak', 'insufficient']):
            return self.colors.WARNING_RED
        else:
            return self.colors.PRIMARY_TEXT

    def create_section_header(self, title: str) -> Paragraph:
        """
        Create a section header paragraph.

        Args:
            title: Section title

        Returns:
            Paragraph object
        """
        return Paragraph(title, self.styles['CustomHeader'])

    def create_subheader(self, title: str) -> Paragraph:
        """
        Create a subheader paragraph.

        Args:
            title: Subheader title

        Returns:
            Paragraph object
        """
        return Paragraph(title, self.styles['CustomSubheader'])

    def create_bullet_point(self, text: str, color: colors.Color = None) -> Paragraph:
        """
        Create a bullet point paragraph.

        Args:
            text: Bullet point text
            color: Optional text color

        Returns:
            Paragraph object
        """
        style = ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['CustomNormal'],
            leftIndent=20,
            bulletIndent=10,
            textColor=color or self.colors.PRIMARY_TEXT
        )
        return Paragraph(f"• {text}", style)

    def create_professional_section_header(self, title: str, icon: str = None) -> List:
        """
        Create a professional section header with background and styling.

        Args:
            title: Section title text
            icon: Optional icon/emoji (will be removed for professional look)

        Returns:
            List of PDF elements for the header
        """
        elements = []

        # Clean title (remove emojis)
        clean_title = title
        if icon and icon in title:
            clean_title = title.replace(icon, "").strip()

        # Add top spacing
        elements.append(Spacer(1, 0.15 * inch))

        # Create header with professional styling
        header_style = ParagraphStyle(
            name='ProfessionalHeader',
            fontName=self.fonts.HEADER,
            fontSize=self.fonts.HEADER_SIZE,
            textColor=self.colors.ACCENT_BACKGROUND,
            spaceAfter=8,
            spaceBefore=4
        )

        elements.append(Paragraph(clean_title.upper(), header_style))

        # Add subtle underline
        elements.append(HRFlowable(
            width=self.content_width,
            thickness=1,
            color=self.colors.LIGHT_BORDER,
            spaceBefore=2,
            spaceAfter=12
        ))

        return elements

    def create_spacing(self, size: str = "normal") -> Spacer:
        """
        Create consistent spacing elements.

        Args:
            size: Spacing size ("small", "normal", "large", "xlarge")

        Returns:
            Spacer object
        """
        sizes = {
            "tiny": 0.05 * inch,
            "small": 0.1 * inch,
            "normal": 0.15 * inch,
            "large": 0.2 * inch,
            "xlarge": 0.3 * inch,
            "section": 0.25 * inch
        }

        height = sizes.get(size, sizes["normal"])
        return Spacer(1, height)



    def create_subsection_header(self, text: str) -> Paragraph:
        """
        Create a subsection header for analysis, assessment, and summary sections.

        Args:
            text: Header text

        Returns:
            Paragraph object with subsection header styling
        """
        return Paragraph(text, self.styles['SubsectionHeader'])

    def create_metric_display(self, label: str, value: str, status_color: colors.Color = None) -> Paragraph:
        """
        Create a professional metric display with optional status color.

        Args:
            label: Metric label
            value: Metric value
            status_color: Optional status indicator color

        Returns:
            Paragraph object
        """
        if status_color:
            # Add a small colored indicator using ReportLab color format
            # Convert RGB values to hex format for HTML
            r, g, b = int(status_color.red * 255), int(status_color.green * 255), int(status_color.blue * 255)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            indicator = f'<font color="{hex_color}">●</font> '
            styled_text = f'{indicator}<b>{label}:</b> {value}'
        else:
            styled_text = f'<b>{label}:</b> {value}'

        style = ParagraphStyle(
            name='MetricDisplay',
            parent=self.styles['CustomNormal'],
            spaceAfter=8,
            leftIndent=10
        )

        return Paragraph(styled_text, style)

    def create_standard_section(self, title: str, metrics: List[Tuple[str, str, Optional[colors.Color]]],
                               subheader: str = None) -> List:
        """
        Create a standard section with professional header, optional subheader, and metrics.

        Args:
            title: Section title
            metrics: List of (label, value, color) tuples
            subheader: Optional subheader text

        Returns:
            List of PDF elements for the section
        """
        elements = []

        # Professional section header
        elements.extend(self.create_professional_section_header(title))

        # Optional subheader
        if subheader:
            elements.append(self.create_subheader(subheader))
            elements.append(self.create_spacing("small"))

        # Add metrics
        for label, value, color in metrics:
            elements.append(self.create_metric_display(label, value, color))

        # Add section spacing
        elements.append(self.create_spacing("section"))

        return elements
