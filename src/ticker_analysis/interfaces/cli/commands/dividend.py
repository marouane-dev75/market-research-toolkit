"""
Dividend Command Implementation

This command fetches and displays dividend data for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import (
    DividendFetcher,
    display_dividends
)


class DividendCommand(BaseCommand):
    """Command to fetch and display dividend data."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "dividend"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display dividend data for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["div", "dividends"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER> [LIMIT]\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)\n" \
               f"       LIMIT: Optional number of recent dividends to display (default: all)"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker, optional limit]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required ticker argument")
            self.logger.info("Usage: python main.py dividend <TICKER> [LIMIT]")
            self.logger.info("Example: python main.py dividend AAPL")
            return False

        # Validate limit argument if provided
        if len(args) > 1:
            try:
                limit = int(args[1])
                if limit <= 0:
                    self.logger.error("Limit must be a positive integer")
                    return False
            except ValueError:
                self.logger.error(f"Invalid limit: {args[1]}. Must be a positive integer")
                return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the dividend command.

        Args:
            args: Command line arguments [ticker, optional limit]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        ticker_symbol = args[0].upper()
        limit = None
        if len(args) > 1:
            limit = int(args[1])

        self.logger.info(f"Fetching dividend data for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = DividendFetcher()
            dividends = fetcher.fetch_dividends(ticker_symbol)

            # Check if we got any data
            if not dividends:
                self.logger.info(f"No dividend payments found for {ticker_symbol} (this is normal for non-dividend paying stocks)")
                return self.handle_success(f"No dividends found for {ticker_symbol}")

            self.logger.success(f"Retrieved {len(dividends)} dividend payment(s)")
            self.logger.info("")  # Blank line for spacing

            # Display dividend data
            display_dividends(dividends, limit)

            return self.handle_success()

        except ValueError as e:
            # Handle the case where no dividend data is available (e.g., TSLA)
            if "No dividend data available" in str(e):
                self.logger.info(f"No dividend payments found for {ticker_symbol} (this is normal for non-dividend paying stocks)")
                return self.handle_success(f"No dividends found for {ticker_symbol}")
            else:
                return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch dividend data: {str(e)}",
                exit_code=1
            )

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Fetches dividend payment history using yfinance and displays formatted dividend data")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")
        self.logger.print_bullet("LIMIT: Optional number of recent dividends to display (default: all)")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py dividend AAPL")
        self.logger.print_example("python main.py dividend MSFT 10")
        self.logger.print_example("python main.py div GOOGL 5")
        self.logger.print_example("python main.py dividends TSLA")

        self.logger.print_section("OUTPUT")
        self.logger.print_bullet("Displays formatted dividend data with the following sections:")
        self.logger.print_bullet("  - Summary information")
        self.logger.print_bullet("  - Current year dividend total")
        self.logger.print_bullet("  - Dividend payment history")
        self.logger.print_bullet("  - Statistical information")
