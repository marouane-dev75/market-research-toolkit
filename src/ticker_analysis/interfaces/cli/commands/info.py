"""
Info Command Implementation

This command fetches and displays comprehensive company information for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import (
    CompanyInfoFetcher,
    display_company_info
)


class InfoCommand(BaseCommand):
    """Command to fetch and display comprehensive company information."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "info"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display comprehensive company information for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["i", "company", "details"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER>\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"

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
            self.logger.info("Usage: python main.py info <TICKER>")
            self.logger.info("Example: python main.py info AAPL")
            return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the info command.

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

        self.logger.info(f"Fetching company information for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = CompanyInfoFetcher()
            company_info = fetcher.fetch_company_info(ticker_symbol)

            # Check if we got valid data
            if not company_info:
                return self.handle_error(
                    f"No company information found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Successfully retrieved company information for {ticker_symbol}")
            self.logger.info("")  # Blank line for spacing

            # Display the company information
            display_company_info(company_info)

            return self.handle_success(f"Successfully processed INFO command for {ticker_symbol}")

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
        self.logger.print_bullet("  - Basic company information (name, sector, industry, employees)")
        self.logger.print_bullet("  - Market data (price, market cap, volume, 52-week range)")
        self.logger.print_bullet("  - Valuation metrics (P/E, P/B, EV ratios, dividend yield)")
        self.logger.print_bullet("  - Financial metrics (margins, ROA, ROE, ratios, growth)")
        self.logger.print_bullet("  - Analyst data (recommendations, target price)")
        self.logger.print_bullet("  - Business summary")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py info AAPL")
        self.logger.print_example("python main.py info MSFT")
        self.logger.print_example("python main.py i GOOGL")
        self.logger.print_example("python main.py company TSLA")

        self.logger.print_section("OUTPUT SECTIONS")
        self.logger.print_bullet("Basic Information: Company name, exchange, sector, industry, etc.")
        self.logger.print_bullet("Market Data: Current price, market cap, volume, 52-week range")
        self.logger.print_bullet("Valuation Metrics: P/E, P/B, EV ratios, dividend yield, beta")
        self.logger.print_bullet("Financial Metrics: Profit margins, ROA, ROE, debt ratios, growth")
        self.logger.print_bullet("Analyst Data: Recommendation and target price")
        self.logger.print_bullet("Business Summary: Brief description of company operations")
