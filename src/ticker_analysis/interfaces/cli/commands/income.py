"""
Income Statement Command Implementation

This command fetches and displays income statement data for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import (
    IncomeStatementFetcher,
    DataFrequency,
    display_income_statement
)


class IncomeCommand(BaseCommand):
    """Command to fetch and display income statement data."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "income"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display income statement data for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["inc", "income-statement"]

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
            self.logger.info("Usage: python main.py income <TICKER> <FREQUENCY>")
            self.logger.info("Example: python main.py income AAPL yearly")
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
        Execute the income statement command.

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

        self.logger.info(f"Fetching {frequency.value} income statement for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = IncomeStatementFetcher()
            income_statements = fetcher.fetch_income_statement(ticker_symbol, frequency)

            # Check if we got any data
            if not income_statements:
                return self.handle_error(
                    f"No income statement data found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Retrieved {len(income_statements)} period(s) of data")
            self.logger.info("")  # Blank line for spacing

            # Display only the latest income statement
            display_income_statement(income_statements[0])

            return self.handle_success()

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch income statement: {str(e)}",
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
        self.logger.print_bullet("Fetches financial data using yfinance and displays formatted income statements")

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
        self.logger.print_example("python main.py income AAPL yearly")
        self.logger.print_example("python main.py income MSFT quarterly")
        self.logger.print_example("python main.py inc GOOGL q")
        self.logger.print_example("python main.py income-statement TSLA year")

        self.logger.print_section("OUTPUT")
        self.logger.print_bullet("Displays formatted income statement with the following sections:")
        self.logger.print_bullet("  - Period Information")
        self.logger.print_bullet("  - Revenue breakdown")
        self.logger.print_bullet("  - Operating Expenses")
        self.logger.print_bullet("  - Operating Income and EBITDA")
        self.logger.print_bullet("  - Non-Operating Items")
        self.logger.print_bullet("  - Income and Tax information")
        self.logger.print_bullet("  - Net Income details")
        self.logger.print_bullet("  - Earnings Per Share (EPS)")
