"""
Balance Sheet Command Implementation

This command fetches and displays balance sheet data for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import (
    BalanceSheetFetcher,
    DataFrequency,
    display_balance_sheet
)


class BalanceCommand(BaseCommand):
    """Command to fetch and display balance sheet data."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "balance"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display balance sheet data for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["bal", "balance-sheet", "bs"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER> [FREQUENCY]\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)\n" \
               f"       FREQUENCY: 'yearly' or 'quarterly' (can also use 'year', 'quarter', 'y', 'q') - defaults to 'yearly'"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker, optional frequency]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required ticker argument")
            self.logger.info("Usage: python main.py balance <TICKER> [FREQUENCY]")
            self.logger.info("Example: python main.py balance AAPL yearly")
            return False

        # Validate frequency argument if provided
        if len(args) > 1:
            frequency_arg = args[1].lower()
            valid_frequencies = ['yearly', 'quarterly', 'year', 'quarter', 'y', 'q']

            if frequency_arg not in valid_frequencies:
                self.logger.error(f"Invalid frequency: {args[1]}")
                self.logger.info(f"Valid frequencies: {', '.join(valid_frequencies)}")
                return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the balance sheet command.

        Args:
            args: Command line arguments [ticker, optional frequency]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        ticker_symbol = args[0].upper()
        frequency_arg = args[1].lower() if len(args) > 1 else "yearly"

        # Map frequency argument to DataFrequency enum
        frequency = self._parse_frequency(frequency_arg)

        self.logger.info(f"Fetching {frequency.value} balance sheet for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = BalanceSheetFetcher()
            balance_sheets = fetcher.fetch_balance_sheet(ticker_symbol, frequency)

            # Check if we got any data
            if not balance_sheets:
                return self.handle_error(
                    f"No balance sheet data found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Retrieved {len(balance_sheets)} period(s) of data")
            self.logger.info("")  # Blank line for spacing

            # Display only the latest balance sheet
            display_balance_sheet(balance_sheets[0])

            return self.handle_success()

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch balance sheet: {str(e)}",
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
        self.logger.print_bullet("Fetches financial data using yfinance and displays formatted balance sheets")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")
        self.logger.print_bullet("FREQUENCY: Optional data frequency - 'yearly', 'quarterly', 'year', 'quarter', 'y', or 'q' (defaults to 'yearly')")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py balance AAPL yearly")
        self.logger.print_example("python main.py balance MSFT quarterly")
        self.logger.print_example("python main.py bal GOOGL q")
        self.logger.print_example("python main.py balance-sheet TSLA year")

        self.logger.print_section("OUTPUT")
        self.logger.print_bullet("Displays formatted balance sheet with the following sections:")
        self.logger.print_bullet("  - Period Information")
        self.logger.print_bullet("  - Current Assets breakdown")
        self.logger.print_bullet("  - Non-Current Assets")
        self.logger.print_bullet("  - Total Assets")
        self.logger.print_bullet("  - Current Liabilities")
        self.logger.print_bullet("  - Non-Current Liabilities")
        self.logger.print_bullet("  - Total Liabilities")
        self.logger.print_bullet("  - Stockholders' Equity")
        self.logger.print_bullet("  - Share Information")
        self.logger.print_bullet("  - Key Metrics")
