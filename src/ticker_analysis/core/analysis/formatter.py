"""
Analysis Formatter Module

This module provides formatting and display functionality
for console output.
"""

from ...interfaces.console.logger import get_logger, FinancialFormatter
from ...interfaces.console.formatter import ConsoleFormatter
from ...interfaces.console.styles import Colors
from .models import CompanyAnalysisData
from .dividend import DividendAnalysisData, DividendTrend
from .income_statement import (
    IncomeStatementMetrics,
    TrendAnalysis,
    FinancialHealthAssessment,
    FinancialHealthRating,
    TrendDirection
)
from .balance_sheet import (
    BalanceSheetMetrics,
    BalanceSheetTrendAnalysis,
    BalanceSheetHealthAssessment
)
from .cash_flow import (
    CashFlowMetrics,
    CashFlowTrendAnalysis,
    CashFlowHealthAssessment
)
from .price import PriceAnalysisData
from .technical import TechnicalIndicators, TechnicalSignal


class CompanyFormatter:
    """Handles formatting for console display."""
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize the company formatter.
        
        Args:
            use_colors: Whether to use colors in output
        """
        self.use_colors = use_colors
        self.financial_formatter = FinancialFormatter(use_colors=use_colors)
        self.console_formatter = ConsoleFormatter(use_colors=use_colors)
        self.logger = get_logger()
    
    def format_company_header(self, ticker: str) -> None:
        """
        Format and display the analysis header.
        
        Args:
            ticker: Stock ticker symbol
        """
        self.logger.print_header(f"Company Analysis for {ticker}")
    
    def format_basic_info(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display basic company information (minimal).
        
        Args:
            company_data: CompanyAnalysisData object
        """
        self.logger.print_section("📋 BASIC INFORMATION")
        self.logger.print_bullet(f"Symbol:           {company_data.ticker}")
        self.logger.print_bullet(f"Exchange:         {company_data.exchange or 'N/A'}")
        self.logger.print_bullet(f"Sector:           {company_data.sector or 'N/A'}")
    
    def format_market_data(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display market data section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("📈 MARKET DATA")
        self.logger.print_bullet(f"Last Price:       {formatter.format_currency(company_data.last_price)}")
        self.logger.print_bullet(f"Market Cap:       {formatter.format_market_cap(company_data.market_cap)}")
        self.logger.print_bullet(f"Avg Volume:       {formatter.format_volume(company_data.avg_volume)}")
        self.logger.print_bullet(f"52-Week Range:    {formatter.format_currency(company_data.fifty_two_week_low)} - {formatter.format_currency(company_data.fifty_two_week_high)}")
        self.logger.print_bullet(f"Dividend Yield:   {formatter.format_percentage(company_data.dividend_yield)}")
    
    def format_valuation_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display valuation metrics section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("💰 VALUATION METRICS")
        self.logger.print_bullet(f"P/E Ratio:        {formatter.format_ratio(company_data.pe_ratio)}")
        self.logger.print_bullet(f"P/B Ratio:        {formatter.format_ratio(company_data.pb_ratio)}")
        self.logger.print_bullet(f"Price/Sales:      {formatter.format_ratio(company_data.price_to_sales)}")
        self.logger.print_bullet(f"EV/Revenue:       {formatter.format_ratio(company_data.ev_to_revenue)}")
        self.logger.print_bullet(f"EV/EBITDA:        {formatter.format_ratio(company_data.ev_to_ebitda)}")
        self.logger.print_bullet(f"Beta:             {formatter.format_ratio(company_data.beta)}")
        self.logger.print_bullet(f"Enterprise Value: {formatter.format_market_cap(company_data.enterprise_value)}")
    
    def format_profitability_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display profitability metrics section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("💵 PROFITABILITY METRICS")
        self.logger.print_bullet(f"Profit Margins:    {formatter.format_percentage(company_data.profit_margins)}")
        self.logger.print_bullet(f"Operating Margins: {formatter.format_percentage(company_data.operating_margins)}")
        self.logger.print_bullet(f"ROA:               {formatter.format_percentage(company_data.return_on_assets)}")
        self.logger.print_bullet(f"ROE:               {formatter.format_percentage(company_data.return_on_equity)}")
    
    def format_liquidity_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display liquidity metrics section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("💧 LIQUIDITY METRICS")
        self.logger.print_bullet(f"Current Ratio:     {formatter.format_ratio(company_data.current_ratio)}")
        self.logger.print_bullet(f"Quick Ratio:       {formatter.format_ratio(company_data.quick_ratio)}")
    
    def format_leverage_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display leverage metrics section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("⚖️ LEVERAGE METRICS")
        self.logger.print_bullet(f"Debt/Equity:       {formatter.format_percentage(company_data.debt_to_equity)}")
    
    def format_growth_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display growth metrics section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("📊 GROWTH METRICS (quater yoy)")
        self.logger.print_bullet(f"Revenue Growth:    {formatter.format_percentage(company_data.revenue_growth)}")
        self.logger.print_bullet(f"Earnings Growth:   {formatter.format_percentage(company_data.earnings_growth)}")
    
    def format_external_analysis_sentiment(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display external analysis sentiment section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        formatter = self.financial_formatter
        
        self.logger.print_section("🎯 EXTERNAL ANALYSIS SENTIMENT")
        self.logger.print_bullet(f"Recommendation:   {company_data.recommendation or 'N/A'}")
        self.logger.print_bullet(f"Target Price:     {formatter.format_currency(company_data.target_price)}")
    
    def format_company_specific_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display company-specific metrics section (for future evolution).
        
        Args:
            company_data: CompanyAnalysisData object
        """
        # This section is prepared for future company-specific metrics
        # Currently, these metrics are None, so we skip displaying them
        has_company_metrics = any([
            company_data.funds_from_operations,
            company_data.adjusted_funds_from_operations,
            company_data.net_asset_value,
            company_data.occupancy_rate
        ])
        
    
    def format_latest_quarter_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display latest quarter income statement metrics.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.income_statement_metrics:
            return
            
        metrics = company_data.income_statement_metrics
        formatter = self.financial_formatter
        
        self.logger.print_section("📅 LATEST QUARTER PERFORMANCE")
        
        # Quarter information
        if metrics.quarter_end_date:
            self.logger.print_bullet(f"Quarter End Date:     {metrics.quarter_end_date}")
        
        # Core financial metrics
        self.logger.print_bullet(f"Revenue:              {formatter.format_currency(metrics.latest_quarter_revenue, compact=True)}")
        self.logger.print_bullet(f"Net Income:           {formatter.format_currency(metrics.latest_quarter_net_income, compact=True)}")
        self.logger.print_bullet(f"Operating Income:     {formatter.format_currency(metrics.latest_quarter_operating_income, compact=True)}")
        self.logger.print_bullet(f"Diluted EPS:          {formatter.format_eps(metrics.latest_quarter_eps)}")
        
        # Additional metrics if available
        if metrics.latest_quarter_gross_profit is not None:
            self.logger.print_bullet(f"Gross Profit:         {formatter.format_currency(metrics.latest_quarter_gross_profit, compact=True)}")
        if metrics.latest_quarter_ebitda is not None:
            self.logger.print_bullet(f"EBITDA:               {formatter.format_currency(metrics.latest_quarter_ebitda, compact=True)}")
        
        # Margin analysis
        if any([metrics.net_profit_margin, metrics.operating_margin, metrics.gross_margin]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Profitability Margins:")
            if metrics.net_profit_margin is not None:
                self.logger.print_bullet(f"  Net Profit Margin:  {formatter.format_percentage(metrics.net_profit_margin / 100)}")
            if metrics.operating_margin is not None:
                self.logger.print_bullet(f"  Operating Margin:   {formatter.format_percentage(metrics.operating_margin / 100)}")
            if metrics.gross_margin is not None:
                self.logger.print_bullet(f"  Gross Margin:       {formatter.format_percentage(metrics.gross_margin / 100)}")
    
    def format_trend_analysis(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display 3-year financial trend analysis.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.trend_analysis:
            return
            
        trends = company_data.trend_analysis
        formatter = self.financial_formatter
        
        self.logger.print_section("📈 3-YEAR FINANCIAL TRENDS")
        
        # Basic trend information
        self.logger.print_bullet(f"Analysis Period:      {trends.years_analyzed} years of data")
        self.logger.print_bullet(f"Analysis Date:        {trends.analysis_date}")
        
        # Average growth rates
        self.logger.print_bullet("")
        self.logger.print_bullet("Average Annual Growth Rates:")
        if trends.avg_revenue_growth is not None:
            growth_color = self._get_growth_color(trends.avg_revenue_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Revenue Growth:     {growth_color}{formatter.format_percentage(trends.avg_revenue_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Revenue Growth:     {formatter.format_percentage(trends.avg_revenue_growth / 100)}")
        
        if trends.avg_net_income_growth is not None:
            growth_color = self._get_growth_color(trends.avg_net_income_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Net Income Growth:  {growth_color}{formatter.format_percentage(trends.avg_net_income_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Net Income Growth:  {formatter.format_percentage(trends.avg_net_income_growth / 100)}")
        
        if trends.avg_operating_income_growth is not None:
            growth_color = self._get_growth_color(trends.avg_operating_income_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Operating Growth:   {growth_color}{formatter.format_percentage(trends.avg_operating_income_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Operating Growth:   {formatter.format_percentage(trends.avg_operating_income_growth / 100)}")
        
        if trends.avg_eps_growth is not None:
            growth_color = self._get_growth_color(trends.avg_eps_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  EPS Growth:         {growth_color}{formatter.format_percentage(trends.avg_eps_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  EPS Growth:         {formatter.format_percentage(trends.avg_eps_growth / 100)}")
        
        # Trend directions
        self.logger.print_bullet("")
        self.logger.print_bullet("Trend Assessment:")
        self.logger.print_bullet(f"  Revenue Trend:      {self._format_trend_direction(trends.revenue_trend)}")
        self.logger.print_bullet(f"  Net Income Trend:   {self._format_trend_direction(trends.net_income_trend)}")
        self.logger.print_bullet(f"  Operating Trend:    {self._format_trend_direction(trends.operating_income_trend)}")
        self.logger.print_bullet(f"  Earnings Trend:     {self._format_trend_direction(trends.earnings_trend)}")
        
        # Consistency scores
        if any([trends.revenue_consistency_score, trends.earnings_consistency_score, trends.overall_consistency_score]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Consistency Scores (0-10 scale):")
            if trends.revenue_consistency_score is not None:
                score_color = self._get_score_color(trends.revenue_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Revenue Consistency: {score_color}{trends.revenue_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Revenue Consistency: {trends.revenue_consistency_score:.1f}/10")
            
            if trends.earnings_consistency_score is not None:
                score_color = self._get_score_color(trends.earnings_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Earnings Consistency: {score_color}{trends.earnings_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Earnings Consistency: {trends.earnings_consistency_score:.1f}/10")
            
            if trends.overall_consistency_score is not None:
                score_color = self._get_score_color(trends.overall_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Overall Consistency:  {score_color}{trends.overall_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Overall Consistency:  {trends.overall_consistency_score:.1f}/10")
        
        # Historical data table
        if trends.yearly_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Historical Financial Data:")
            
            # Define column widths and alignments
            column_widths = [4, 12, 12, 10, 8]
            column_alignments = ['left', 'right', 'right', 'right', 'right']
            
            # Display table header
            header_columns = ['Year', 'Revenue', 'Net Income', 'Operating', 'EPS']
            header_row = self.console_formatter.format_table_row(header_columns, column_widths, column_alignments)
            self.logger.print_bullet(header_row)
            
            # Create separator line based on actual display width
            separator_width = sum(column_widths) + len(column_widths) - 1  # Add spaces between columns
            self.logger.print_bullet("-" * separator_width)
            
            for year_data in trends.yearly_data:
                year_str = str(year_data.year)
                revenue_str = formatter.format_currency(year_data.revenue, compact=True) if year_data.revenue else "N/A"
                net_income_str = formatter.format_currency(year_data.net_income, compact=True) if year_data.net_income else "N/A"
                operating_str = formatter.format_currency(year_data.operating_income, compact=True) if year_data.operating_income else "N/A"
                eps_str = formatter.format_eps(year_data.eps) if year_data.eps else "N/A"
                
                # Format data columns
                columns = [year_str, revenue_str, net_income_str, operating_str, eps_str]
                
                # Format the row with proper ANSI-aware alignment
                row = self.console_formatter.format_table_row(columns, column_widths, column_alignments)
                self.logger.print_bullet(row)
    
    def format_financial_health_assessment(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display financial health assessment.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.financial_health_assessment:
            return
            
        assessment = company_data.financial_health_assessment
        formatter = self.financial_formatter
        
        self.logger.print_section("🏥 FINANCIAL HEALTH ASSESSMENT")
        
        # Overall health rating
        if assessment.overall_health_rating != FinancialHealthRating.INSUFFICIENT_DATA:
            rating_color = self._get_health_rating_color(assessment.overall_health_rating)
            if self.use_colors and rating_color:
                self.logger.print_bullet(f"Overall Health:       {rating_color}{assessment.overall_health_rating.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Overall Health:       {assessment.overall_health_rating.value}")
            
            if assessment.overall_health_score is not None:
                score_color = self._get_score_color(assessment.overall_health_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"Health Score:         {score_color}{assessment.overall_health_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"Health Score:         {assessment.overall_health_score:.1f}/10")
        
        # Component ratings
        component_ratings = [
            ("Revenue Health", assessment.revenue_health, assessment.revenue_score),
            ("Profitability Health", assessment.profitability_health, assessment.profitability_score),
            ("Growth Health", assessment.growth_health, assessment.growth_score),
            ("Consistency Health", assessment.consistency_health, assessment.consistency_score)
        ]
        
        has_component_data = any(rating != FinancialHealthRating.INSUFFICIENT_DATA for _, rating, _ in component_ratings)
        
        if has_component_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Component Health Ratings:")
            
            for name, rating, score in component_ratings:
                if rating != FinancialHealthRating.INSUFFICIENT_DATA:
                    rating_color = self._get_health_rating_color(rating)
                    score_text = f" ({score:.1f}/10)" if score is not None else ""
                    
                    if self.use_colors and rating_color:
                        self.logger.print_bullet(f"  {name:18} {rating_color}{rating.value}{Colors.RESET}{score_text}")
                    else:
                        self.logger.print_bullet(f"  {name:18} {rating.value}{score_text}")
        
        # Strengths and concerns
        if assessment.strengths:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Key Strengths:{Colors.RESET}")
            else:
                self.logger.print_bullet("Key Strengths:")
            for strength in assessment.strengths:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.GREEN}✓{Colors.RESET} {strength}")
                else:
                    self.logger.print_bullet(f"  • {strength}")
        
        if assessment.concerns:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Areas of Concern:{Colors.RESET}")
            else:
                self.logger.print_bullet("Areas of Concern:")
            for concern in assessment.concerns:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.RED}⚠{Colors.RESET} {concern}")
                else:
                    self.logger.print_bullet(f"  • {concern}")
        
        # Summary
        if assessment.summary:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Summary:{Colors.RESET}")
            else:
                self.logger.print_bullet("Summary:")
            self.logger.print_bullet(f"  {assessment.summary}")
    
    def _get_growth_color(self, growth_rate: float) -> str:
        """Get color for growth rate display."""
        if not self.use_colors:
            return ""
        
        if growth_rate > 5:
            return Colors.GREEN
        elif growth_rate > 0:
            return Colors.YELLOW
        elif growth_rate > -5:
            return Colors.YELLOW
        else:
            return Colors.RED
    
    def _get_score_color(self, score: float) -> str:
        """Get color for score display."""
        if not self.use_colors:
            return ""
        
        if score >= 8:
            return Colors.GREEN
        elif score >= 6:
            return Colors.YELLOW
        else:
            return Colors.RED
    
    def _get_health_rating_color(self, rating: FinancialHealthRating) -> str:
        """Get color for health rating display."""
        if not self.use_colors:
            return ""
        
        if rating == FinancialHealthRating.EXCELLENT:
            return Colors.GREEN
        elif rating == FinancialHealthRating.GOOD:
            return Colors.GREEN
        elif rating == FinancialHealthRating.FAIR:
            return Colors.YELLOW
        elif rating == FinancialHealthRating.POOR:
            return Colors.RED
        else:
            return ""
    
    def _format_trend_direction(self, trend: TrendDirection) -> str:
        """Format trend direction with color if enabled."""
        if not self.use_colors:
            return trend.value
        
        if trend == TrendDirection.STRONG_GROWTH:
            return f"{Colors.GREEN}{trend.value}{Colors.RESET}"
        elif trend == TrendDirection.MODERATE_GROWTH:
            return f"{Colors.GREEN}{trend.value}{Colors.RESET}"
        elif trend == TrendDirection.STABLE:
            return f"{Colors.YELLOW}{trend.value}{Colors.RESET}"
        elif trend == TrendDirection.DECLINING:
            return f"{Colors.RED}{trend.value}{Colors.RESET}"
        elif trend == TrendDirection.VOLATILE:
            return f"{Colors.RED}{trend.value}{Colors.RESET}"
        else:
            return trend.value

    def format_income_statement_header(self) -> None:
        """
        Format and display the income statement analysis header.
        """
        self.logger.print_header("📊 INCOME STATEMENT ANALYSIS")

    def format_balance_sheet_header(self) -> None:
        """
        Format and display the balance sheet analysis header.
        """
        self.logger.print_header("🏦 BALANCE SHEET ANALYSIS")

    def format_dividend_analysis(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display dividend analysis section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.dividend_analysis:
            return
            
        analysis = company_data.dividend_analysis
        formatter = self.financial_formatter
        
        self.logger.print_section("💎 DIVIDEND ANALYSIS")
        
        # Basic dividend information
        self.logger.print_bullet(f"Dividend History:     {analysis.total_years} years of data")
        self.logger.print_bullet(f"Total Payments:       {analysis.total_payments}")
        
        # Recent performance
        if analysis.trailing_12_month_total is not None:
            self.logger.print_bullet(f"Trailing 12M Total:   {formatter.format_currency(analysis.trailing_12_month_total)}")
        
        # Yearly extremes
        self.logger.print_bullet(f"Highest Year:         {formatter.format_currency(analysis.highest_year_amount)} ({analysis.highest_year})")
        self.logger.print_bullet(f"Lowest Year:          {formatter.format_currency(analysis.lowest_year_amount)} ({analysis.lowest_year})")
        
        # Trend analysis
        self.logger.print_bullet(f"Dividend Trend:       {analysis.dividend_trend.value}")
        
        if analysis.average_growth_rate is not None:
            self.logger.print_bullet(f"Avg Growth Rate:      {formatter.format_percentage(analysis.average_growth_rate / 100)} per year")
        
        if analysis.year_over_year_variance is not None:
            self.logger.print_bullet(f"Year-over-Year Var:   {formatter.format_percentage(analysis.year_over_year_variance / 100)}")
        
        # Consistency score
        if analysis.consistency_score is not None:
            score_formatted = f"{analysis.consistency_score:.1f}/10"
            self.logger.print_bullet(f"Consistency Score:    {score_formatted}")
        
        # Years without dividends (in red color)
        if analysis.years_without_dividends:
            years_str = ", ".join(str(year) for year in analysis.years_without_dividends)
            if self.use_colors:
                colored_text = f"{Colors.BOLD}Years Without Dividends: {Colors.RED}{years_str}{Colors.RESET}"
                self.logger.print_bullet(colored_text)
            else:
                self.logger.print_bullet(f"Years Without Dividends: {years_str}")
        
        # Display recent yearly data (last 5 years)
        if analysis.yearly_data:
            recent_years = analysis.yearly_data[:5]  # Most recent 5 years
            self.logger.print_bullet("")
            self.logger.print_bullet("Recent Yearly Dividends:")
            
            # Define column widths and alignments
            column_widths = [4, 10, 8]
            column_alignments = ['left', 'right', 'right']
            
            # Display table header
            header_columns = ['Year', 'Total', 'Payments']
            header_row = self.console_formatter.format_table_row(header_columns, column_widths, column_alignments)
            self.logger.print_bullet(header_row)
            
            # Create separator line based on actual display width
            separator_width = sum(column_widths) + len(column_widths) - 1  # Add spaces between columns
            self.logger.print_bullet("-" * separator_width)
            
            for year_data in recent_years:
                year_str = str(year_data.year)
                total_str = formatter.format_currency(year_data.total_amount)
                payments_str = str(year_data.payment_count)
                
                # Format data columns
                columns = [year_str, total_str, payments_str]
                
                # Format the row with proper ANSI-aware alignment
                row = self.console_formatter.format_table_row(columns, column_widths, column_alignments)
                self.logger.print_bullet(row)

    def format_balance_sheet_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display latest quarter balance sheet metrics.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.balance_sheet_metrics:
            return
            
        metrics = company_data.balance_sheet_metrics
        formatter = self.financial_formatter
        
        self.logger.print_section("🏦 LATEST QUARTER BALANCE SHEET METRICS")
        
        # Quarter information
        if metrics.quarter_end_date:
            self.logger.print_bullet(f"Quarter End Date:     {metrics.quarter_end_date}")
        
        # Liquidity ratios
        self.logger.print_bullet("")
        self.logger.print_bullet("Liquidity Ratios:")
        if metrics.current_ratio is not None:
            ratio_color = self._get_liquidity_color(metrics.current_ratio, "current")
            if self.use_colors and ratio_color:
                self.logger.print_bullet(f"  Current Ratio:      {ratio_color}{formatter.format_ratio(metrics.current_ratio)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Current Ratio:      {formatter.format_ratio(metrics.current_ratio)}")
        
        if metrics.quick_ratio is not None:
            ratio_color = self._get_liquidity_color(metrics.quick_ratio, "quick")
            if self.use_colors and ratio_color:
                self.logger.print_bullet(f"  Quick Ratio:        {ratio_color}{formatter.format_ratio(metrics.quick_ratio)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Quick Ratio:        {formatter.format_ratio(metrics.quick_ratio)}")
        
        if metrics.cash_ratio is not None:
            self.logger.print_bullet(f"  Cash Ratio:         {formatter.format_ratio(metrics.cash_ratio)}")
        
        # Leverage ratios
        self.logger.print_bullet("")
        self.logger.print_bullet("Leverage Ratios:")
        if metrics.debt_to_equity is not None:
            ratio_color = self._get_leverage_color(metrics.debt_to_equity)
            if self.use_colors and ratio_color:
                self.logger.print_bullet(f"  Debt-to-Equity:     {ratio_color}{formatter.format_ratio(metrics.debt_to_equity)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Debt-to-Equity:     {formatter.format_ratio(metrics.debt_to_equity)}")
        
        if metrics.debt_to_assets is not None:
            self.logger.print_bullet(f"  Debt-to-Assets:     {formatter.format_ratio(metrics.debt_to_assets)}")
        
        if metrics.equity_ratio is not None:
            self.logger.print_bullet(f"  Equity Ratio:       {formatter.format_ratio(metrics.equity_ratio)}")
        
        # Financial strength indicators
        self.logger.print_bullet("")
        self.logger.print_bullet("Financial Strength:")
        self.logger.print_bullet(f"  Cash & Equivalents: {formatter.format_currency(metrics.cash_and_equivalents, compact=True)}")
        self.logger.print_bullet(f"  Total Debt:         {formatter.format_currency(metrics.total_debt, compact=True)}")
        self.logger.print_bullet(f"  Total Equity:       {formatter.format_currency(metrics.total_equity, compact=True)}")
        self.logger.print_bullet(f"  Working Capital:    {formatter.format_currency(metrics.working_capital, compact=True)}")
        
        # Asset composition
        if any([metrics.current_assets_pct, metrics.ppe_assets_pct, metrics.cash_assets_pct]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Asset Composition:")
            if metrics.current_assets_pct is not None:
                self.logger.print_bullet(f"  Current Assets:     {formatter.format_percentage(metrics.current_assets_pct / 100)}")
            if metrics.ppe_assets_pct is not None:
                self.logger.print_bullet(f"  PPE Assets:         {formatter.format_percentage(metrics.ppe_assets_pct / 100)}")
            if metrics.cash_assets_pct is not None:
                self.logger.print_bullet(f"  Cash Assets:        {formatter.format_percentage(metrics.cash_assets_pct / 100)}")

    def format_balance_sheet_trends(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display balance sheet trend analysis.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.balance_sheet_trends:
            return
            
        trends = company_data.balance_sheet_trends
        formatter = self.financial_formatter
        
        self.logger.print_section("📊 BALANCE SHEET TRENDS")
        
        # Basic trend information
        self.logger.print_bullet(f"Analysis Period:      {trends.years_analyzed} years of data")
        self.logger.print_bullet(f"Analysis Date:        {trends.analysis_date}")
        
        # Average growth rates
        self.logger.print_bullet("")
        self.logger.print_bullet("Average Annual Growth Rates:")
        if trends.avg_assets_growth is not None:
            growth_color = self._get_growth_color(trends.avg_assets_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Assets Growth:      {growth_color}{formatter.format_percentage(trends.avg_assets_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Assets Growth:      {formatter.format_percentage(trends.avg_assets_growth / 100)}")
        
        if trends.avg_equity_growth is not None:
            growth_color = self._get_growth_color(trends.avg_equity_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Equity Growth:      {growth_color}{formatter.format_percentage(trends.avg_equity_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Equity Growth:      {formatter.format_percentage(trends.avg_equity_growth / 100)}")
        
        if trends.avg_debt_growth is not None:
            growth_color = self._get_growth_color(trends.avg_debt_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Debt Growth:        {growth_color}{formatter.format_percentage(trends.avg_debt_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Debt Growth:        {formatter.format_percentage(trends.avg_debt_growth / 100)}")
        
        # Trend directions
        self.logger.print_bullet("")
        self.logger.print_bullet("Trend Assessment:")
        self.logger.print_bullet(f"  Assets Trend:       {self._format_trend_direction(trends.assets_trend)}")
        self.logger.print_bullet(f"  Equity Trend:       {self._format_trend_direction(trends.equity_trend)}")
        self.logger.print_bullet(f"  Debt Trend:         {self._format_trend_direction(trends.debt_trend)}")
        self.logger.print_bullet(f"  Leverage Trend:     {self._format_trend_direction(trends.leverage_trend)}")
        
        # Stability scores
        if trends.balance_sheet_stability_score is not None or trends.leverage_consistency_score is not None:
            self.logger.print_bullet("")
            self.logger.print_bullet("Stability Scores (0-10 scale):")
            if trends.balance_sheet_stability_score is not None:
                score_color = self._get_score_color(trends.balance_sheet_stability_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Balance Sheet Stability: {score_color}{trends.balance_sheet_stability_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Balance Sheet Stability: {trends.balance_sheet_stability_score:.1f}/10")
            
            if trends.leverage_consistency_score is not None:
                score_color = self._get_score_color(trends.leverage_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Leverage Consistency:    {score_color}{trends.leverage_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Leverage Consistency:    {trends.leverage_consistency_score:.1f}/10")
        
        # Historical data table
        if trends.yearly_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Historical Balance Sheet Data:")
            
            # Define column widths and alignments
            column_widths = [4, 12, 12, 12, 10]
            column_alignments = ['left', 'right', 'right', 'right', 'right']
            
            # Display table header
            header_columns = ['Year', 'Assets', 'Equity', 'Debt', 'D/E Ratio']
            header_row = self.console_formatter.format_table_row(header_columns, column_widths, column_alignments)
            self.logger.print_bullet(header_row)
            
            # Create separator line based on actual display width
            separator_width = sum(column_widths) + len(column_widths) - 1  # Add spaces between columns
            self.logger.print_bullet("-" * separator_width)
            
            for year_data in trends.yearly_data:
                year_str = str(year_data.year)
                assets_str = formatter.format_currency(year_data.total_assets, compact=True) if year_data.total_assets else "N/A"
                equity_str = formatter.format_currency(year_data.total_equity, compact=True) if year_data.total_equity else "N/A"
                debt_str = formatter.format_currency(year_data.total_debt, compact=True) if year_data.total_debt else "N/A"
                de_ratio_str = formatter.format_ratio(year_data.debt_to_equity) if year_data.debt_to_equity else "N/A"
                
                # Format data columns
                columns = [year_str, assets_str, equity_str, debt_str, de_ratio_str]
                
                # Format the row with proper ANSI-aware alignment
                row = self.console_formatter.format_table_row(columns, column_widths, column_alignments)
                self.logger.print_bullet(row)

    def format_balance_sheet_health(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display balance sheet health assessment.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.balance_sheet_health:
            return
            
        assessment = company_data.balance_sheet_health
        
        self.logger.print_section("🏥 BALANCE SHEET HEALTH ASSESSMENT")
        
        # Overall balance sheet health rating
        if assessment.overall_balance_sheet_rating != FinancialHealthRating.INSUFFICIENT_DATA:
            rating_color = self._get_health_rating_color(assessment.overall_balance_sheet_rating)
            if self.use_colors and rating_color:
                self.logger.print_bullet(f"Overall Balance Sheet Health: {rating_color}{assessment.overall_balance_sheet_rating.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Overall Balance Sheet Health: {assessment.overall_balance_sheet_rating.value}")
            
            if assessment.overall_balance_sheet_score is not None:
                score_color = self._get_score_color(assessment.overall_balance_sheet_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"Balance Sheet Score:          {score_color}{assessment.overall_balance_sheet_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"Balance Sheet Score:          {assessment.overall_balance_sheet_score:.1f}/10")
        
        # Component ratings
        component_ratings = [
            ("Liquidity Health", assessment.liquidity_health, assessment.liquidity_score),
            ("Leverage Health", assessment.leverage_health, assessment.leverage_score),
            ("Asset Quality Health", assessment.asset_quality_health, assessment.asset_quality_score),
            ("Financial Stability", assessment.financial_stability_health, assessment.financial_stability_score)
        ]
        
        has_component_data = any(rating != FinancialHealthRating.INSUFFICIENT_DATA for _, rating, _ in component_ratings)
        
        if has_component_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Component Health Ratings:")
            
            for name, rating, score in component_ratings:
                if rating != FinancialHealthRating.INSUFFICIENT_DATA:
                    rating_color = self._get_health_rating_color(rating)
                    score_text = f" ({score:.1f}/10)" if score is not None else ""
                    
                    if self.use_colors and rating_color:
                        self.logger.print_bullet(f"  {name:20} {rating_color}{rating.value}{Colors.RESET}{score_text}")
                    else:
                        self.logger.print_bullet(f"  {name:20} {rating.value}{score_text}")
        
        # Strengths and concerns
        if assessment.strengths:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Balance Sheet Strengths:{Colors.RESET}")
            else:
                self.logger.print_bullet("Balance Sheet Strengths:")
            for strength in assessment.strengths:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.GREEN}✓{Colors.RESET} {strength}")
                else:
                    self.logger.print_bullet(f"  • {strength}")
        
        if assessment.concerns:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Balance Sheet Concerns:{Colors.RESET}")
            else:
                self.logger.print_bullet("Balance Sheet Concerns:")
            for concern in assessment.concerns:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.RED}⚠{Colors.RESET} {concern}")
                else:
                    self.logger.print_bullet(f"  • {concern}")
        
        # Summary
        if assessment.summary:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Balance Sheet Summary:{Colors.RESET}")
            else:
                self.logger.print_bullet("Balance Sheet Summary:")
            self.logger.print_bullet(f"  {assessment.summary}")

    def _get_liquidity_color(self, ratio: float, ratio_type: str) -> str:
        """Get color for liquidity ratio display."""
        if not self.use_colors:
            return ""
        
        if ratio_type == "current":
            if ratio > 2.0:
                return Colors.GREEN
            elif ratio > 1.5:
                return Colors.YELLOW
            elif ratio < 1.0:
                return Colors.RED
        elif ratio_type == "quick":
            if ratio > 1.0:
                return Colors.GREEN
            elif ratio > 0.5:
                return Colors.YELLOW
            else:
                return Colors.RED
        
        return ""
    
    def _get_leverage_color(self, ratio: float) -> str:
        """Get color for leverage ratio display."""
        if not self.use_colors:
            return ""
        
        if ratio < 0.3:
            return Colors.GREEN
        elif ratio < 0.6:
            return Colors.YELLOW
        elif ratio > 1.5:
            return Colors.RED
        else:
            return Colors.YELLOW

    def format_cash_flow_header(self) -> None:
        """
        Format and display the cash flow analysis header.
        """
        self.logger.print_header("💰 CASH FLOW ANALYSIS")

    def format_cash_flow_metrics(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display latest quarter cash flow metrics.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.cash_flow_metrics:
            return
            
        metrics = company_data.cash_flow_metrics
        formatter = self.financial_formatter
        
        self.logger.print_section("💰 LATEST QUARTER CASH FLOW METRICS")
        
        # Quarter information
        if metrics.quarter_end_date:
            self.logger.print_bullet(f"Quarter End Date:     {metrics.quarter_end_date}")
        
        # Core cash flow metrics
        self.logger.print_bullet("")
        self.logger.print_bullet("Core Cash Flow Metrics:")
        if metrics.operating_cash_flow is not None:
            ocf_color = Colors.GREEN if metrics.operating_cash_flow > 0 else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  Operating Cash Flow:  {ocf_color}{formatter.format_currency(metrics.operating_cash_flow, compact=True)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Operating Cash Flow:  {formatter.format_currency(metrics.operating_cash_flow, compact=True)}")
        
        if metrics.free_cash_flow is not None:
            fcf_color = Colors.GREEN if metrics.free_cash_flow > 0 else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  Free Cash Flow:       {fcf_color}{formatter.format_currency(metrics.free_cash_flow, compact=True)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Free Cash Flow:       {formatter.format_currency(metrics.free_cash_flow, compact=True)}")
        
        self.logger.print_bullet(f"  Investing Cash Flow:  {formatter.format_currency(metrics.investing_cash_flow, compact=True)}")
        self.logger.print_bullet(f"  Financing Cash Flow:  {formatter.format_currency(metrics.financing_cash_flow, compact=True)}")
        self.logger.print_bullet(f"  Net Change in Cash:   {formatter.format_currency(metrics.net_change_in_cash, compact=True)}")
        
        # Sustainability metrics
        if any([metrics.capex_to_ocf_ratio, metrics.cash_flow_coverage_ratio]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Sustainability Metrics:")
            if metrics.capital_expenditure is not None:
                self.logger.print_bullet(f"  Capital Expenditure:  {formatter.format_currency(metrics.capital_expenditure, compact=True)}")
            if metrics.capex_to_ocf_ratio is not None:
                ratio_color = self._get_capex_ratio_color(metrics.capex_to_ocf_ratio)
                if self.use_colors and ratio_color:
                    self.logger.print_bullet(f"  CapEx/OCF Ratio:      {ratio_color}{formatter.format_ratio(metrics.capex_to_ocf_ratio)}{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  CapEx/OCF Ratio:      {formatter.format_ratio(metrics.capex_to_ocf_ratio)}")
            if metrics.cash_flow_coverage_ratio is not None:
                coverage_color = self._get_coverage_ratio_color(metrics.cash_flow_coverage_ratio)
                if self.use_colors and coverage_color:
                    self.logger.print_bullet(f"  Cash Flow Coverage:   {coverage_color}{formatter.format_ratio(metrics.cash_flow_coverage_ratio)}{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Cash Flow Coverage:   {formatter.format_ratio(metrics.cash_flow_coverage_ratio)}")
        
        # Cash position
        if any([metrics.beginning_cash_position, metrics.ending_cash_position]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Cash Position:")
            if metrics.beginning_cash_position is not None:
                self.logger.print_bullet(f"  Beginning Cash:       {formatter.format_currency(metrics.beginning_cash_position, compact=True)}")
            if metrics.ending_cash_position is not None:
                self.logger.print_bullet(f"  Ending Cash:          {formatter.format_currency(metrics.ending_cash_position, compact=True)}")
            if metrics.cash_burn_rate is not None:
                self.logger.print_bullet(f"  Cash Burn Rate:       {formatter.format_currency(metrics.cash_burn_rate, compact=True)}")
        
        # Financing activities
        if any([metrics.dividend_payments, metrics.share_repurchases, metrics.net_debt_activity]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Financing Activities:")
            if metrics.dividend_payments is not None:
                self.logger.print_bullet(f"  Dividend Payments:    {formatter.format_currency(metrics.dividend_payments, compact=True)}")
            if metrics.share_repurchases is not None:
                self.logger.print_bullet(f"  Share Repurchases:    {formatter.format_currency(metrics.share_repurchases, compact=True)}")
            if metrics.net_debt_activity is not None:
                self.logger.print_bullet(f"  Net Debt Activity:    {formatter.format_currency(metrics.net_debt_activity, compact=True)}")

    def format_cash_flow_trends(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display cash flow trend analysis.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.cash_flow_trends:
            return
            
        trends = company_data.cash_flow_trends
        formatter = self.financial_formatter
        
        self.logger.print_section("📈 CASH FLOW TRENDS")
        
        # Basic trend information
        self.logger.print_bullet(f"Analysis Period:      {trends.years_analyzed} years of data")
        self.logger.print_bullet(f"Analysis Date:        {trends.analysis_date}")
        
        # Average growth rates
        self.logger.print_bullet("")
        self.logger.print_bullet("Average Annual Growth Rates:")
        if trends.avg_ocf_growth is not None:
            growth_color = self._get_growth_color(trends.avg_ocf_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Operating Cash Flow:  {growth_color}{formatter.format_percentage(trends.avg_ocf_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Operating Cash Flow:  {formatter.format_percentage(trends.avg_ocf_growth / 100)}")
        
        if trends.avg_fcf_growth is not None:
            growth_color = self._get_growth_color(trends.avg_fcf_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Free Cash Flow:       {growth_color}{formatter.format_percentage(trends.avg_fcf_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Free Cash Flow:       {formatter.format_percentage(trends.avg_fcf_growth / 100)}")
        
        if trends.avg_capex_growth is not None:
            growth_color = self._get_growth_color(trends.avg_capex_growth)
            if self.use_colors and growth_color:
                self.logger.print_bullet(f"  Capital Expenditure:  {growth_color}{formatter.format_percentage(trends.avg_capex_growth / 100)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Capital Expenditure:  {formatter.format_percentage(trends.avg_capex_growth / 100)}")
        
        # Trend directions
        self.logger.print_bullet("")
        self.logger.print_bullet("Trend Assessment:")
        self.logger.print_bullet(f"  OCF Trend:            {self._format_trend_direction(trends.ocf_trend)}")
        self.logger.print_bullet(f"  FCF Trend:            {self._format_trend_direction(trends.fcf_trend)}")
        self.logger.print_bullet(f"  CapEx Trend:          {self._format_trend_direction(trends.capex_trend)}")
        self.logger.print_bullet(f"  Cash Generation:      {self._format_trend_direction(trends.cash_generation_trend)}")
        
        # Consistency scores
        if any([trends.ocf_consistency_score, trends.fcf_consistency_score, trends.cash_flow_stability_score]):
            self.logger.print_bullet("")
            self.logger.print_bullet("Consistency Scores (0-10 scale):")
            if trends.ocf_consistency_score is not None:
                score_color = self._get_score_color(trends.ocf_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  OCF Consistency:      {score_color}{trends.ocf_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  OCF Consistency:      {trends.ocf_consistency_score:.1f}/10")
            
            if trends.fcf_consistency_score is not None:
                score_color = self._get_score_color(trends.fcf_consistency_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  FCF Consistency:      {score_color}{trends.fcf_consistency_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  FCF Consistency:      {trends.fcf_consistency_score:.1f}/10")
            
            if trends.cash_flow_stability_score is not None:
                score_color = self._get_score_color(trends.cash_flow_stability_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"  Overall Stability:    {score_color}{trends.cash_flow_stability_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"  Overall Stability:    {trends.cash_flow_stability_score:.1f}/10")
        
        # Quality metrics
        if trends.avg_ocf_to_fcf_conversion is not None:
            self.logger.print_bullet("")
            self.logger.print_bullet("Cash Flow Quality:")
            conversion_color = self._get_conversion_color(trends.avg_ocf_to_fcf_conversion)
            if self.use_colors and conversion_color:
                self.logger.print_bullet(f"  OCF to FCF Conversion: {conversion_color}{formatter.format_percentage(trends.avg_ocf_to_fcf_conversion)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  OCF to FCF Conversion: {formatter.format_percentage(trends.avg_ocf_to_fcf_conversion)}")
        
        # Historical data table
        if trends.yearly_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Historical Cash Flow Data:")
            
            # Define column widths and alignments
            column_widths = [4, 14, 14, 12, 12]
            column_alignments = ['left', 'right', 'right', 'right', 'right']
            
            # Display table header
            header_columns = ['Year', 'Op. Cash Flow', 'Free Cash Flow', 'CapEx', 'Net Change']
            header_row = self.console_formatter.format_table_row(header_columns, column_widths, column_alignments)
            self.logger.print_bullet(header_row)
            
            # Create separator line based on actual display width
            separator_width = sum(column_widths) + len(column_widths) - 1  # Add spaces between columns
            self.logger.print_bullet("-" * separator_width)
            
            for year_data in trends.yearly_data:
                year_str = str(year_data.year)
                ocf_str = formatter.format_currency(year_data.operating_cash_flow, compact=True) if year_data.operating_cash_flow else "N/A"
                fcf_str = formatter.format_currency(year_data.free_cash_flow, compact=True) if year_data.free_cash_flow else "N/A"
                capex_str = formatter.format_currency(year_data.capital_expenditure, compact=True) if year_data.capital_expenditure else "N/A"
                change_str = formatter.format_currency(year_data.net_change_in_cash, compact=True) if year_data.net_change_in_cash else "N/A"
                
                # Format data columns
                columns = [year_str, ocf_str, fcf_str, capex_str, change_str]
                
                # Format the row with proper ANSI-aware alignment
                row = self.console_formatter.format_table_row(columns, column_widths, column_alignments)
                self.logger.print_bullet(row)

    def format_cash_flow_health(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display cash flow health assessment.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.cash_flow_health:
            return
            
        assessment = company_data.cash_flow_health
        
        self.logger.print_section("🏥 CASH FLOW HEALTH ASSESSMENT")
        
        # Overall cash flow health rating
        if assessment.overall_cash_flow_rating != FinancialHealthRating.INSUFFICIENT_DATA:
            rating_color = self._get_health_rating_color(assessment.overall_cash_flow_rating)
            if self.use_colors and rating_color:
                self.logger.print_bullet(f"Overall Cash Flow Health: {rating_color}{assessment.overall_cash_flow_rating.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Overall Cash Flow Health: {assessment.overall_cash_flow_rating.value}")
            
            if assessment.overall_cash_flow_score is not None:
                score_color = self._get_score_color(assessment.overall_cash_flow_score)
                if self.use_colors and score_color:
                    self.logger.print_bullet(f"Cash Flow Score:          {score_color}{assessment.overall_cash_flow_score:.1f}/10{Colors.RESET}")
                else:
                    self.logger.print_bullet(f"Cash Flow Score:          {assessment.overall_cash_flow_score:.1f}/10")
        
        # Component ratings
        component_ratings = [
            ("Cash Flow Quality", assessment.cash_flow_quality_health, assessment.cash_flow_quality_score),
            ("Cash Flow Sustainability", assessment.cash_flow_sustainability_health, assessment.cash_flow_sustainability_score),
            ("Cash Flow Growth", assessment.cash_flow_growth_health, assessment.cash_flow_growth_score),
            ("Cash Flow Stability", assessment.cash_flow_stability_health, assessment.cash_flow_stability_score)
        ]
        
        has_component_data = any(rating != FinancialHealthRating.INSUFFICIENT_DATA for _, rating, _ in component_ratings)
        
        if has_component_data:
            self.logger.print_bullet("")
            self.logger.print_bullet("Component Health Ratings:")
            
            for name, rating, score in component_ratings:
                if rating != FinancialHealthRating.INSUFFICIENT_DATA:
                    rating_color = self._get_health_rating_color(rating)
                    score_text = f" ({score:.1f}/10)" if score is not None else ""
                    
                    if self.use_colors and rating_color:
                        self.logger.print_bullet(f"  {name:22} {rating_color}{rating.value}{Colors.RESET}{score_text}")
                    else:
                        self.logger.print_bullet(f"  {name:22} {rating.value}{score_text}")
        
        # Strengths and concerns
        if assessment.strengths:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Cash Flow Strengths:{Colors.RESET}")
            else:
                self.logger.print_bullet("Cash Flow Strengths:")
            for strength in assessment.strengths:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.GREEN}✓{Colors.RESET} {strength}")
                else:
                    self.logger.print_bullet(f"  • {strength}")
        
        if assessment.concerns:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Cash Flow Concerns:{Colors.RESET}")
            else:
                self.logger.print_bullet("Cash Flow Concerns:")
            for concern in assessment.concerns:
                if self.use_colors:
                    self.logger.print_bullet(f"  {Colors.RED}⚠{Colors.RESET} {concern}")
                else:
                    self.logger.print_bullet(f"  • {concern}")
        
        # Summary
        if assessment.summary:
            self.logger.print_bullet("")
            if self.use_colors:
                self.logger.print_bullet(f"{Colors.BOLD}Cash Flow Summary:{Colors.RESET}")
            else:
                self.logger.print_bullet("Cash Flow Summary:")
            self.logger.print_bullet(f"  {assessment.summary}")

    def _get_capex_ratio_color(self, ratio: float) -> str:
        """Get color for CapEx/OCF ratio display."""
        if not self.use_colors:
            return ""
        
        if ratio < 0.5:  # CapEx < 50% of OCF
            return Colors.GREEN
        elif ratio < 0.8:  # CapEx < 80% of OCF
            return Colors.YELLOW
        elif ratio > 1.2:  # CapEx > 120% of OCF
            return Colors.RED
        else:
            return Colors.YELLOW
    
    def _get_coverage_ratio_color(self, ratio: float) -> str:
        """Get color for cash flow coverage ratio display."""
        if not self.use_colors:
            return ""
        
        if ratio > 1.5:
            return Colors.GREEN
        elif ratio > 1.0:
            return Colors.YELLOW
        else:
            return Colors.RED
    
    def _get_conversion_color(self, conversion: float) -> str:
        """Get color for OCF to FCF conversion display."""
        if not self.use_colors:
            return ""
        
        if conversion > 0.7:  # Good conversion
            return Colors.GREEN
        elif conversion > 0.3:  # Moderate conversion
            return Colors.YELLOW
        else:  # Poor conversion
            return Colors.RED

    def format_price_analysis_header(self) -> None:
        """
        Format and display the price analysis header.
        """
        self.logger.print_header("📈 PRICE ANALYSIS")

    def format_price_analysis(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display price analysis section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.price_analysis:
            return
            
        analysis = company_data.price_analysis
        formatter = self.financial_formatter
        
        self.logger.print_section("📈 CURRENT PRICE & PERFORMANCE")
        
        # Current price information
        self.logger.print_bullet(f"Current Price:        {formatter.format_currency(analysis.current_price)}")
        if analysis.previous_close is not None:
            self.logger.print_bullet(f"Previous Close:       {formatter.format_currency(analysis.previous_close)}")
        
        # Daily change
        if analysis.daily_change is not None and analysis.daily_change_percent is not None:
            change_color = Colors.GREEN if analysis.daily_change > 0 else Colors.RED if analysis.daily_change < 0 else ""
            if self.use_colors and change_color:
                self.logger.print_bullet(f"Daily Change:         {change_color}{formatter.format_currency(analysis.daily_change, show_sign=True)} ({formatter.format_percentage(analysis.daily_change_percent / 100, show_sign=True)}){Colors.RESET}")
            else:
                self.logger.print_bullet(f"Daily Change:         {formatter.format_currency(analysis.daily_change, show_sign=True)} ({formatter.format_percentage(analysis.daily_change_percent / 100, show_sign=True)})")
        
        # 52-week range
        if analysis.fifty_two_week_high is not None and analysis.fifty_two_week_low is not None:
            self.logger.print_bullet(f"52-Week Range:        {formatter.format_currency(analysis.fifty_two_week_low)} - {formatter.format_currency(analysis.fifty_two_week_high)}")
        
        # Volume information
        if analysis.current_volume is not None:
            self.logger.print_bullet(f"Current Volume:       {formatter.format_volume(analysis.current_volume)}")
        if analysis.average_volume is not None:
            self.logger.print_bullet(f"Average Volume:       {formatter.format_volume(analysis.average_volume)}")
        if analysis.volume_ratio is not None:
            volume_color = Colors.GREEN if analysis.volume_ratio > 1.5 else Colors.YELLOW if analysis.volume_ratio > 0.5 else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"Volume Ratio:         {volume_color}{analysis.volume_ratio:.2f}x{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Volume Ratio:         {analysis.volume_ratio:.2f}x")
        
        # Period performance
        self.logger.print_bullet("")
        self.logger.print_bullet("Period Performance:")
        
        # 7-day change
        if analysis.seven_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.seven_day_change_percent)
            if self.use_colors and change_color:
                self.logger.print_bullet(f"  7-Day Change:       {change_color}{formatter.format_percentage(analysis.seven_day_change_percent / 100, show_sign=True)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  7-Day Change:       {formatter.format_percentage(analysis.seven_day_change_percent / 100, show_sign=True)}")
        
        # 30-day change
        if analysis.thirty_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.thirty_day_change_percent)
            if self.use_colors and change_color:
                self.logger.print_bullet(f"  30-Day Change:      {change_color}{formatter.format_percentage(analysis.thirty_day_change_percent / 100, show_sign=True)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  30-Day Change:      {formatter.format_percentage(analysis.thirty_day_change_percent / 100, show_sign=True)}")
        
        # 90-day change
        if analysis.ninety_day_change_percent is not None:
            change_color = self._get_performance_color(analysis.ninety_day_change_percent)
            if self.use_colors and change_color:
                self.logger.print_bullet(f"  90-Day Change:      {change_color}{formatter.format_percentage(analysis.ninety_day_change_percent / 100, show_sign=True)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  90-Day Change:      {formatter.format_percentage(analysis.ninety_day_change_percent / 100, show_sign=True)}")

    def format_technical_analysis_header(self) -> None:
        """
        Format and display the technical analysis header.
        """
        self.logger.print_header("📊 TECHNICAL ANALYSIS")

    def format_technical_analysis(self, company_data: CompanyAnalysisData) -> None:
        """
        Format and display technical analysis section.
        
        Args:
            company_data: CompanyAnalysisData object
        """
        if not company_data.technical_analysis:
            return
            
        analysis = company_data.technical_analysis
        formatter = self.financial_formatter
        
        # Overall technical score and signal
        self.logger.print_section("📊 OVERALL TECHNICAL ASSESSMENT")
        
        if analysis.overall_score is not None:
            score_color = self._get_technical_score_color(analysis.overall_score)
            if self.use_colors and score_color:
                self.logger.print_bullet(f"Technical Score:      {score_color}{analysis.overall_score:.1f}/10{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Technical Score:      {analysis.overall_score:.1f}/10")
        
        if analysis.overall_signal:
            signal_color = self._get_signal_color(analysis.overall_signal)
            if self.use_colors and signal_color:
                self.logger.print_bullet(f"Overall Signal:       {signal_color}{analysis.overall_signal.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"Overall Signal:       {analysis.overall_signal.value}")
        
        if analysis.confidence_level is not None:
            self.logger.print_bullet(f"Confidence Level:     {analysis.confidence_level:.0f}%")
        
        # Signal summary
        self.logger.print_bullet(f"Bullish Indicators:   {analysis.bullish_indicators}")
        self.logger.print_bullet(f"Bearish Indicators:   {analysis.bearish_indicators}")
        self.logger.print_bullet(f"Neutral Indicators:   {analysis.neutral_indicators}")
        
        # Individual indicators
        if analysis.macd:
            self._format_macd_analysis(analysis.macd, formatter)
        
        if analysis.rsi:
            self._format_rsi_analysis(analysis.rsi, formatter)
        
        if analysis.moving_averages:
            self._format_moving_averages_analysis(analysis.moving_averages, formatter)
        
        if analysis.bollinger_bands:
            self._format_bollinger_bands_analysis(analysis.bollinger_bands, formatter)

    def _format_macd_analysis(self, macd, formatter) -> None:
        """Format MACD analysis section."""
        self.logger.print_bullet("")
        self.logger.print_bullet("MACD Analysis:")
        
        if macd.macd_line is not None:
            self.logger.print_bullet(f"  MACD Line:          {formatter.format_ratio(macd.macd_line)}")
        if macd.signal_line is not None:
            self.logger.print_bullet(f"  Signal Line:        {formatter.format_ratio(macd.signal_line)}")
        if macd.histogram is not None:
            hist_color = Colors.GREEN if macd.histogram > 0 else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  Histogram:          {hist_color}{formatter.format_ratio(macd.histogram)}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Histogram:          {formatter.format_ratio(macd.histogram)}")
        
        if macd.signal:
            signal_color = self._get_signal_color(macd.signal)
            if self.use_colors and signal_color:
                self.logger.print_bullet(f"  MACD Signal:        {signal_color}{macd.signal.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  MACD Signal:        {macd.signal.value}")
        
        if macd.score is not None:
            score_color = self._get_technical_score_color(macd.score)
            if self.use_colors and score_color:
                self.logger.print_bullet(f"  MACD Score:         {score_color}{macd.score:.1f}/10{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  MACD Score:         {macd.score:.1f}/10")

    def _format_rsi_analysis(self, rsi, formatter) -> None:
        """Format RSI analysis section."""
        self.logger.print_bullet("")
        self.logger.print_bullet("RSI Analysis:")
        
        if rsi.rsi_value is not None:
            rsi_color = ""
            if self.use_colors:
                if rsi.is_overbought:
                    rsi_color = Colors.RED
                elif rsi.is_oversold:
                    rsi_color = Colors.GREEN
                else:
                    rsi_color = Colors.YELLOW
            
            if rsi_color:
                self.logger.print_bullet(f"  RSI Value:          {rsi_color}{rsi.rsi_value:.1f}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  RSI Value:          {rsi.rsi_value:.1f}")
        
        if rsi.is_overbought:
            if self.use_colors:
                self.logger.print_bullet(f"  Status:             {Colors.RED}Overbought (>70){Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Status:             Overbought (>70)")
        elif rsi.is_oversold:
            if self.use_colors:
                self.logger.print_bullet(f"  Status:             {Colors.GREEN}Oversold (<30){Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Status:             Oversold (<30)")
        else:
            self.logger.print_bullet(f"  Status:             Normal (30-70)")
        
        if rsi.signal:
            signal_color = self._get_signal_color(rsi.signal)
            if self.use_colors and signal_color:
                self.logger.print_bullet(f"  RSI Signal:         {signal_color}{rsi.signal.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  RSI Signal:         {rsi.signal.value}")
        
        if rsi.score is not None:
            score_color = self._get_technical_score_color(rsi.score)
            if self.use_colors and score_color:
                self.logger.print_bullet(f"  RSI Score:          {score_color}{rsi.score:.1f}/10{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  RSI Score:          {rsi.score:.1f}/10")

    def _format_moving_averages_analysis(self, ma, formatter) -> None:
        """Format moving averages analysis section."""
        self.logger.print_bullet("")
        self.logger.print_bullet("Moving Averages Analysis:")
        
        if ma.current_price is not None:
            self.logger.print_bullet(f"  Current Price:      {formatter.format_currency(ma.current_price)}")
        
        if ma.sma_20 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_20 else "Below"
            color = Colors.GREEN if price_vs_sma == "Above" else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  SMA 20:             {formatter.format_currency(ma.sma_20)} ({color}{price_vs_sma}{Colors.RESET})")
            else:
                self.logger.print_bullet(f"  SMA 20:             {formatter.format_currency(ma.sma_20)} ({price_vs_sma})")
        
        if ma.sma_50 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_50 else "Below"
            color = Colors.GREEN if price_vs_sma == "Above" else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  SMA 50:             {formatter.format_currency(ma.sma_50)} ({color}{price_vs_sma}{Colors.RESET})")
            else:
                self.logger.print_bullet(f"  SMA 50:             {formatter.format_currency(ma.sma_50)} ({price_vs_sma})")
        
        if ma.sma_200 is not None:
            price_vs_sma = "Above" if ma.current_price and ma.current_price > ma.sma_200 else "Below"
            color = Colors.GREEN if price_vs_sma == "Above" else Colors.RED
            if self.use_colors:
                self.logger.print_bullet(f"  SMA 200:            {formatter.format_currency(ma.sma_200)} ({color}{price_vs_sma}{Colors.RESET})")
            else:
                self.logger.print_bullet(f"  SMA 200:            {formatter.format_currency(ma.sma_200)} ({price_vs_sma})")
        
        if ma.ema_12 is not None:
            self.logger.print_bullet(f"  EMA 12:             {formatter.format_currency(ma.ema_12)}")
        
        if ma.ema_26 is not None:
            self.logger.print_bullet(f"  EMA 26:             {formatter.format_currency(ma.ema_26)}")
        
        if ma.trend_strength:
            trend_color = self._get_trend_color(ma.trend_strength)
            if self.use_colors and trend_color:
                self.logger.print_bullet(f"  Trend Strength:     {trend_color}{ma.trend_strength}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Trend Strength:     {ma.trend_strength}")
        
        if ma.signal:
            signal_color = self._get_signal_color(ma.signal)
            if self.use_colors and signal_color:
                self.logger.print_bullet(f"  MA Signal:          {signal_color}{ma.signal.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  MA Signal:          {ma.signal.value}")
        
        if ma.score is not None:
            score_color = self._get_technical_score_color(ma.score)
            if self.use_colors and score_color:
                self.logger.print_bullet(f"  MA Score:           {score_color}{ma.score:.1f}/10{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  MA Score:           {ma.score:.1f}/10")

    def _format_bollinger_bands_analysis(self, bb, formatter) -> None:
        """Format Bollinger Bands analysis section."""
        self.logger.print_bullet("")
        self.logger.print_bullet("Bollinger Bands Analysis:")
        
        if bb.current_price is not None:
            self.logger.print_bullet(f"  Current Price:      {formatter.format_currency(bb.current_price)}")
        
        if bb.upper_band is not None:
            self.logger.print_bullet(f"  Upper Band:         {formatter.format_currency(bb.upper_band)}")
        
        if bb.middle_band is not None:
            self.logger.print_bullet(f"  Middle Band:        {formatter.format_currency(bb.middle_band)}")
        
        if bb.lower_band is not None:
            self.logger.print_bullet(f"  Lower Band:         {formatter.format_currency(bb.lower_band)}")
        
        if bb.percent_b is not None:
            position = "Above Upper" if bb.percent_b > 100 else "Below Lower" if bb.percent_b < 0 else "Within Bands"
            position_color = Colors.RED if bb.percent_b > 100 or bb.percent_b < 0 else Colors.GREEN
            if self.use_colors:
                self.logger.print_bullet(f"  %B Position:        {bb.percent_b:.1f}% ({position_color}{position}{Colors.RESET})")
            else:
                self.logger.print_bullet(f"  %B Position:        {bb.percent_b:.1f}% ({position})")
        
        if bb.bandwidth is not None:
            self.logger.print_bullet(f"  Bandwidth:          {bb.bandwidth:.2f}%")
        
        if bb.squeeze:
            if self.use_colors:
                self.logger.print_bullet(f"  Squeeze:            {Colors.YELLOW}Yes (Low Volatility){Colors.RESET}")
            else:
                self.logger.print_bullet(f"  Squeeze:            Yes (Low Volatility)")
        else:
            self.logger.print_bullet(f"  Squeeze:            No")
        
        if bb.signal:
            signal_color = self._get_signal_color(bb.signal)
            if self.use_colors and signal_color:
                self.logger.print_bullet(f"  BB Signal:          {signal_color}{bb.signal.value}{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  BB Signal:          {bb.signal.value}")
        
        if bb.score is not None:
            score_color = self._get_technical_score_color(bb.score)
            if self.use_colors and score_color:
                self.logger.print_bullet(f"  BB Score:           {score_color}{bb.score:.1f}/10{Colors.RESET}")
            else:
                self.logger.print_bullet(f"  BB Score:           {bb.score:.1f}/10")

    def _get_performance_color(self, change_percent: float) -> str:
        """Get color for performance display."""
        if not self.use_colors:
            return ""
        
        if change_percent > 5:
            return Colors.GREEN
        elif change_percent > 0:
            return Colors.GREEN
        elif change_percent > -5:
            return Colors.RED
        else:
            return Colors.RED

    def _get_technical_score_color(self, score: float) -> str:
        """Get color for technical score display."""
        if not self.use_colors:
            return ""
        
        if score >= 8:
            return Colors.GREEN
        elif score >= 6:
            return Colors.GREEN
        elif score >= 4:
            return Colors.YELLOW
        elif score >= 2:
            return Colors.RED
        else:
            return Colors.RED

    def _get_signal_color(self, signal: TechnicalSignal) -> str:
        """Get color for signal display."""
        if not self.use_colors:
            return ""
        
        if signal in [TechnicalSignal.STRONG_BUY, TechnicalSignal.BUY]:
            return Colors.GREEN
        elif signal in [TechnicalSignal.STRONG_SELL, TechnicalSignal.SELL]:
            return Colors.RED
        else:
            return Colors.YELLOW

    def _get_trend_color(self, trend: str) -> str:
        """Get color for trend display."""
        if not self.use_colors:
            return ""
        
        if "Strong Uptrend" in trend or "Uptrend" in trend:
            return Colors.GREEN
        elif "Strong Downtrend" in trend or "Downtrend" in trend:
            return Colors.RED
        else:
            return Colors.YELLOW


def display_comprehensive_analysis(company_data: CompanyAnalysisData) -> None:
    """
    Display comprehensive company analysis in a formatted console output.
    
    This function provides the main interface for displaying complete company analysis data
    with comprehensive formatting, including financial metrics, price analysis, technical analysis,
    balance sheet analysis, cash flow analysis, and dividend analysis.
    
    Args:
        company_data: CompanyAnalysisData object to display
    """
    formatter = CompanyFormatter()
    
    # Display all sections in logical order
    formatter.format_company_header(company_data.ticker)
    formatter.format_basic_info(company_data)
    formatter.format_market_data(company_data)
    
    # Existing sections
    formatter.format_leverage_metrics(company_data)
    formatter.format_growth_metrics(company_data)
    formatter.format_valuation_metrics(company_data)
    formatter.format_profitability_metrics(company_data)
    formatter.format_liquidity_metrics(company_data)
    formatter.format_external_analysis_sentiment(company_data)
    formatter.format_dividend_analysis(company_data)
    formatter.format_company_specific_metrics(company_data)
    
    # Income statement analysis sections
    formatter.format_income_statement_header()
    formatter.format_latest_quarter_metrics(company_data)
    formatter.format_trend_analysis(company_data)
    formatter.format_financial_health_assessment(company_data)
    
    # Balance sheet analysis sections
    formatter.format_balance_sheet_header()
    formatter.format_balance_sheet_metrics(company_data)
    formatter.format_balance_sheet_trends(company_data)
    formatter.format_balance_sheet_health(company_data)
    
    # Cash flow analysis sections
    formatter.format_cash_flow_header()
    formatter.format_cash_flow_metrics(company_data)
    formatter.format_cash_flow_trends(company_data)
    formatter.format_cash_flow_health(company_data)
    
    # Price analysis section
    formatter.format_price_analysis_header()
    formatter.format_price_analysis(company_data)
    
    # Technical analysis section
    formatter.format_technical_analysis_header()
    formatter.format_technical_analysis(company_data)