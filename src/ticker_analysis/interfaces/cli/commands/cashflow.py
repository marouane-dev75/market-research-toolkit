"""
Cash Flow Statement Command Implementation

This command fetches and displays cash flow statement data for a given ticker.
"""

from typing import List
from .base import BaseCommand
from src.ticker_analysis.core.data.fetchers import (
    CashFlowFetcher,
    DataFrequency,
    display_cash_flow
)


class CashFlowCommand(BaseCommand):
    """Command to fetch and display cash flow statement data."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "cashflow"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display cash flow statement data for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["cf", "cash-flow", "cash"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER> <FREQUENCY>\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)\n" \
               f"       FREQUENCY: 'yearly' or 'quarterly' (can also use 'year', 'quarter', 'y', 'q')"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker, frequency]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 2:
            self.logger.error("Missing required arguments")
            self.logger.info("Usage: python main.py cashflow <TICKER> <FREQUENCY>")
            self.logger.info("Example: python main.py cashflow AAPL yearly")
            return False

        # Validate frequency argument
        frequency_arg = args[1].lower()
        valid_frequencies = ['yearly', 'quarterly', 'year', 'quarter', 'y', 'q']

        if frequency_arg not in valid_frequencies:
            self.logger.error(f"Invalid frequency: {args[1]}")
            self.logger.info(f"Valid frequencies: {', '.join(valid_frequencies)}")
            return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the cash flow statement command.

        Args:
            args: Command line arguments [ticker, frequency]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        ticker_symbol = args[0].upper()
        frequency_arg = args[1].lower()

        # Map frequency argument to DataFrequency enum
        frequency = self._parse_frequency(frequency_arg)

        self.logger.info(f"Fetching {frequency.value} cash flow statement for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = CashFlowFetcher()
            cash_flows = fetcher.fetch_cash_flow(ticker_symbol, frequency)

            # Check if we got any data
            if not cash_flows:
                return self.handle_error(
                    f"No cash flow data found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Retrieved {len(cash_flows)} period(s) of data")
            self.logger.info("")  # Blank line for spacing

            # Display only the latest cash flow statement
            display_cash_flow(cash_flows[0])

            return self.handle_success()

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch cash flow statement: {str(e)}",
                exit_code=1
            )

    def _parse_frequency(self, frequency_arg: str) -> DataFrequency:
        """
        Parse frequency argument to DataFrequency enum.

        Args:
            frequency_arg: Frequency string from command line

        Returns:
            DataFrequency enum value
        """
        frequency_map = {
            'yearly': DataFrequency.YEARLY,
            'year': DataFrequency.YEARLY,
            'y': DataFrequency.YEARLY,
            'quarterly': DataFrequency.QUARTERLY,
            'quarter': DataFrequency.QUARTERLY,
            'q': DataFrequency.QUARTERLY,
        }

        return frequency_map[frequency_arg.lower()]

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Fetches financial data using yfinance and displays formatted cash flow statements")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")
        self.logger.print_bullet("FREQUENCY: Data frequency - 'yearly', 'quarterly', 'year', 'quarter', 'y', or 'q'")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py cashflow AAPL yearly")
        self.logger.print_example("python main.py cashflow MSFT quarterly")
        self.logger.print_example("python main.py cf GOOGL q")
        self.logger.print_example("python main.py cash-flow TSLA year")

        self.logger.print_section("OUTPUT")
        self.logger.print_bullet("Displays formatted cash flow statement with the following sections:")
        self.logger.print_bullet("  - Period Information")
        self.logger.print_bullet("  - Operating Activities breakdown")
        self.logger.print_bullet("  - Changes in Working Capital")
        self.logger.print_bullet("  - Operating Cash Flow")
        self.logger.print_bullet("  - Investing Activities")
        self.logger.print_bullet("  - Financing Activities")
        self.logger.print_bullet("  - Cash Flow Summary")
        self.logger.print_bullet("  - Key Metrics (Free Cash Flow)")