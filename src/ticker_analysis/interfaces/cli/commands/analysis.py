"""
Analysis Command Implementation

This command fetches and displays comprehensive company analysis for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import CompanyInfoFetcher, DividendFetcher, IncomeStatementFetcher, BalanceSheetFetcher, CashFlowFetcher, PriceFetcher, DataFrequency, TimePeriod
from ....core.analysis.formatter import display_comprehensive_analysis
from ....core.analysis.models import CompanyAnalysisData
from ....core.analysis.dividend import DividendAnalyzer
from ....core.analysis.income_statement import CompanyIncomeStatementAnalyzer
from ....core.analysis.balance_sheet import BalanceSheetAnalyzer
from ....core.analysis.cash_flow import CashFlowAnalyzer
from ....core.analysis.price import PriceAnalyzer
from ....core.analysis.technical import TechnicalAnalyzer


class AnalysisCommand(BaseCommand):
    """Command to fetch and display comprehensive company analysis."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "analysis"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display comprehensive company analysis for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["a", "analyze"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER>\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, VNQ)"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required ticker argument")
            self.logger.info("Usage: python main.py analysis <TICKER>")
            self.logger.info("Example: python main.py analysis AAPL")
            return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the analysis command.

        Args:
            args: Command line arguments [ticker]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        ticker_symbol = args[0].upper()

        self.logger.info(f"Fetching comprehensive analysis for {ticker_symbol}...")

        try:
            # Create fetchers and analyzers
            company_fetcher = CompanyInfoFetcher()
            dividend_fetcher = DividendFetcher()
            income_fetcher = IncomeStatementFetcher()
            balance_fetcher = BalanceSheetFetcher()
            cashflow_fetcher = CashFlowFetcher()
            price_fetcher = PriceFetcher()
            income_analyzer = CompanyIncomeStatementAnalyzer()
            balance_analyzer = BalanceSheetAnalyzer()
            cashflow_analyzer = CashFlowAnalyzer()
            price_analyzer = PriceAnalyzer()
            technical_analyzer = TechnicalAnalyzer()
            
            company_info = company_fetcher.fetch_company_info(ticker_symbol)

            # Check if we got valid data
            if not company_info:
                return self.handle_error(
                    f"No company information found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Successfully retrieved company information for {ticker_symbol}")
            
            # Fetch and analyze dividend data
            dividend_analysis = None
            try:
                self.logger.info("Fetching dividend data for analysis...")
                dividend_data = dividend_fetcher.fetch_dividends(ticker_symbol)
                
                if dividend_data:
                    analyzer = DividendAnalyzer()
                    dividend_analysis = analyzer.analyze_dividends(dividend_data)
                    self.logger.success("Successfully analyzed dividend data")
                else:
                    self.logger.warning("No dividend data available for analysis")
                    
            except Exception as e:
                self.logger.warning(f"Could not fetch dividend data: {str(e)}")
                # Continue without dividend analysis
            
            # Fetch and analyze income statement data
            income_statement_metrics = None
            trend_analysis = None
            financial_health_assessment = None
            
            try:
                self.logger.info("Fetching income statement data for analysis...")
                
                # Fetch quarterly data for latest quarter metrics
                quarterly_data = income_fetcher.fetch_income_statement(ticker_symbol, DataFrequency.QUARTERLY)
                if quarterly_data:
                    income_statement_metrics = income_analyzer.analyze_latest_quarter(quarterly_data)
                    self.logger.success("Successfully analyzed latest quarter metrics")
                else:
                    self.logger.warning("No quarterly income statement data available")
                
                # Fetch yearly data for trend analysis
                yearly_data = income_fetcher.fetch_income_statement(ticker_symbol, DataFrequency.YEARLY)
                if yearly_data:
                    trend_analysis = income_analyzer.analyze_yearly_trends(yearly_data)
                    self.logger.success("Successfully analyzed 3-year financial trends")
                else:
                    self.logger.warning("No yearly income statement data available")
                
                # Generate financial health assessment
                if income_statement_metrics or trend_analysis:
                    financial_health_assessment = income_analyzer.assess_financial_health(
                        income_statement_metrics, trend_analysis
                    )
                    self.logger.success("Successfully generated financial health assessment")
                
            except Exception as e:
                self.logger.warning(f"Could not fetch income statement data: {str(e)}")
                # Continue without income statement analysis
            
            # Fetch and analyze balance sheet data
            balance_sheet_metrics = None
            balance_sheet_trends = None
            balance_sheet_health = None
            
            try:
                self.logger.info("Fetching balance sheet data for analysis...")
                
                # Fetch quarterly data for latest quarter balance sheet metrics
                quarterly_balance_data = balance_fetcher.fetch_balance_sheet(ticker_symbol, DataFrequency.QUARTERLY)
                if quarterly_balance_data:
                    balance_sheet_metrics = balance_analyzer.analyze_latest_quarter(quarterly_balance_data)
                    self.logger.success("Successfully analyzed latest quarter balance sheet metrics")
                else:
                    self.logger.warning("No quarterly balance sheet data available")
                
                # Fetch yearly data for balance sheet trend analysis
                yearly_balance_data = balance_fetcher.fetch_balance_sheet(ticker_symbol, DataFrequency.YEARLY)
                if yearly_balance_data:
                    balance_sheet_trends = balance_analyzer.analyze_yearly_trends(yearly_balance_data)
                    self.logger.success("Successfully analyzed 3-year balance sheet trends")
                else:
                    self.logger.warning("No yearly balance sheet data available")
                
                # Generate balance sheet health assessment
                if balance_sheet_metrics or balance_sheet_trends:
                    balance_sheet_health = balance_analyzer.assess_balance_sheet_health(
                        balance_sheet_metrics, balance_sheet_trends
                    )
                    self.logger.success("Successfully generated balance sheet health assessment")
                
            except Exception as e:
                self.logger.warning(f"Could not fetch balance sheet data: {str(e)}")
                # Continue without balance sheet analysis
            
            # Fetch and analyze cash flow data
            cash_flow_metrics = None
            cash_flow_trends = None
            cash_flow_health = None
            
            try:
                self.logger.info("Fetching cash flow data for analysis...")
                
                # Fetch quarterly data for latest quarter cash flow metrics
                quarterly_cashflow_data = cashflow_fetcher.fetch_cash_flow(ticker_symbol, DataFrequency.QUARTERLY)
                if quarterly_cashflow_data:
                    cash_flow_metrics = cashflow_analyzer.analyze_latest_quarter(quarterly_cashflow_data)
                    self.logger.success("Successfully analyzed latest quarter cash flow metrics")
                else:
                    self.logger.warning("No quarterly cash flow data available")
                
                # Fetch yearly data for cash flow trend analysis
                yearly_cashflow_data = cashflow_fetcher.fetch_cash_flow(ticker_symbol, DataFrequency.YEARLY)
                if yearly_cashflow_data:
                    cash_flow_trends = cashflow_analyzer.analyze_yearly_trends(yearly_cashflow_data)
                    self.logger.success("Successfully analyzed 3-year cash flow trends")
                else:
                    self.logger.warning("No yearly cash flow data available")
                
                # Generate cash flow health assessment
                if cash_flow_metrics or cash_flow_trends:
                    cash_flow_health = cashflow_analyzer.assess_cash_flow_health(
                        cash_flow_metrics, cash_flow_trends
                    )
                    self.logger.success("Successfully generated cash flow health assessment")
                
            except Exception as e:
                self.logger.warning(f"Could not fetch cash flow data: {str(e)}")
                # Continue without cash flow analysis
            
            # Fetch and analyze price data
            price_analysis = None
            technical_analysis = None
            
            try:
                self.logger.info("Fetching price data for analysis...")
                
                # Fetch 1 year of price data for technical analysis (need sufficient data for indicators)
                price_data_list = price_fetcher.fetch_price_data(ticker_symbol, TimePeriod.ONE_YEAR)
                
                if price_data_list:
                    # Perform price analysis
                    price_analysis = price_analyzer.analyze_price_movements(ticker_symbol, price_data_list)
                    if price_analysis:
                        self.logger.success("Successfully analyzed price movements")
                    
                    # Perform technical analysis (need at least 200 data points for accurate analysis)
                    if len(price_data_list) >= 50:  # Minimum for basic technical analysis
                        technical_analysis = technical_analyzer.analyze_technical_indicators(ticker_symbol, price_data_list)
                        if technical_analysis:
                            self.logger.success("Successfully analyzed technical indicators")
                        else:
                            self.logger.warning("Could not perform technical analysis - insufficient data quality")
                    else:
                        self.logger.warning(f"Insufficient price data for technical analysis (got {len(price_data_list)}, need at least 50)")
                else:
                    self.logger.warning("No price data available for analysis")
                    
            except Exception as e:
                self.logger.warning(f"Could not fetch price data: {str(e)}")
                # Continue without price and technical analysis
            
            self.logger.info("")  # Blank line for spacing

            # Convert to analysis data model with all analysis components
            analysis_data = CompanyAnalysisData.from_company_info(
                company_info,
                dividend_analysis,
                income_statement_metrics,
                trend_analysis,
                financial_health_assessment,
                balance_sheet_metrics,
                balance_sheet_trends,
                balance_sheet_health,
                cash_flow_metrics,
                cash_flow_trends,
                cash_flow_health,
                price_analysis,
                technical_analysis
            )
            
            # Display the comprehensive analysis using the formatter
            display_comprehensive_analysis(analysis_data)

            return self.handle_success(f"Successfully processed analysis command for {ticker_symbol}")

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch company information: {str(e)}",
                exit_code=1
            )

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Fetches comprehensive company data using yfinance including:")
        self.logger.print_bullet("  - Basic information (symbol, exchange)")
        self.logger.print_bullet("  - Market data (price, market cap, volume, 52-week range)")
        self.logger.print_bullet("  - Valuation metrics (P/E, P/B, EV ratios, dividend yield)")
        self.logger.print_bullet("  - Financial metrics (margins, ROA, ROE, ratios, growth)")
        self.logger.print_bullet("  - Price analysis (7/30/90-day percentage changes, volume analysis)")
        self.logger.print_bullet("  - Technical analysis (MACD, RSI, Moving Averages, Bollinger Bands)")
        self.logger.print_bullet("  - Technical scoring (1-10 scale with buy/sell recommendations)")
        self.logger.print_bullet("  - Income statement analysis (quarterly metrics, trends, health)")
        self.logger.print_bullet("  - Balance sheet analysis (liquidity, leverage, asset quality)")
        self.logger.print_bullet("  - Cash flow analysis (operating, investing, financing cash flows)")
        self.logger.print_bullet("  - Dividend analysis (yearly aggregation, trends, statistics)")
        self.logger.print_bullet("  - External analysis sentiment (recommendations, target price)")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, VNQ)")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py analysis AAPL")
        self.logger.print_example("python main.py analysis MSFT")
        self.logger.print_example("python main.py a TSLA")
        self.logger.print_example("python main.py analyze SPY")

        self.logger.print_section("OUTPUT SECTIONS")
        self.logger.print_bullet("Basic Information: Symbol and exchange")
        self.logger.print_bullet("Market Data: Current price, market cap, volume, 52-week range")
        self.logger.print_bullet("Price Analysis: 7/30/90-day percentage changes, volume ratios, daily performance")
        self.logger.print_bullet("Technical Analysis: MACD, RSI, Moving Averages, Bollinger Bands with scores")
        self.logger.print_bullet("Technical Scoring: Overall 1-10 score with buy/sell recommendation")
        self.logger.print_bullet("Latest Quarter Performance: Revenue, net income, operating income, EPS, margins")
        self.logger.print_bullet("3-Year Financial Trends: Growth rates, trend directions, consistency scores")
        self.logger.print_bullet("Financial Health Assessment: Overall rating, component scores, strengths/concerns")
        self.logger.print_bullet("Balance Sheet Metrics: Liquidity ratios, leverage ratios, asset composition")
        self.logger.print_bullet("Balance Sheet Trends: Multi-year asset, equity, and debt growth patterns")
        self.logger.print_bullet("Balance Sheet Health: Liquidity, leverage, asset quality, and stability assessment")
        self.logger.print_bullet("Cash Flow Metrics: Operating, investing, financing cash flows, sustainability ratios")
        self.logger.print_bullet("Cash Flow Trends: Multi-year cash flow growth patterns and consistency")
        self.logger.print_bullet("Cash Flow Health: Quality, sustainability, growth, and stability assessment")
        self.logger.print_bullet("Leverage Metrics: Debt-to-equity ratios")
        self.logger.print_bullet("Growth Metrics: Revenue and earnings growth")
        self.logger.print_bullet("Valuation Metrics: P/E, P/B, EV ratios, dividend yield, beta")
        self.logger.print_bullet("Profitability Metrics: Profit margins, ROA, ROE")
        self.logger.print_bullet("Liquidity Metrics: Current and quick ratios")
        self.logger.print_bullet("External Analysis Sentiment: Recommendation and target price")
        self.logger.print_bullet("Dividend Analysis: Yearly totals, trends, growth rates, consistency")