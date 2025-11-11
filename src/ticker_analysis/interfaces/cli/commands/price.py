"""
Price Command Implementation

This command fetches and displays historical price data for a given ticker.
"""

from typing import List
from .base import BaseCommand
from ....core.data.fetchers import (
    PriceFetcher,
    TimePeriod,
    display_price_data,
    display_price_summary
)


class PriceCommand(BaseCommand):
    """Command to fetch and display historical price data."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "price"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Fetch and display historical price data for a ticker symbol"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["p", "prices", "history"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER> [PERIOD]\n" \
               f"       TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)\n" \
               f"       PERIOD: Time period - '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max' - defaults to '1y'"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker, optional period]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required ticker argument")
            self.logger.info("Usage: python main.py price <TICKER> [PERIOD]")
            self.logger.info("Example: python main.py price AAPL 1y")
            return False

        # Validate period argument if provided
        if len(args) > 1:
            period_arg = args[1].lower()
            valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

            if period_arg not in valid_periods:
                self.logger.error(f"Invalid period: {args[1]}")
                self.logger.info(f"Valid periods: {', '.join(valid_periods)}")
                return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the price command.

        Args:
            args: Command line arguments [ticker, optional period]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        ticker_symbol = args[0].upper()
        period_arg = args[1].lower() if len(args) > 1 else "1y"

        # Map period argument to TimePeriod enum
        period = self._parse_period(period_arg)

        self.logger.info(f"Fetching {period.value} price data for {ticker_symbol}...")

        try:
            # Create fetcher and fetch data
            fetcher = PriceFetcher()
            price_data_list = fetcher.fetch_price_data(ticker_symbol, period)

            # Check if we got any data
            if not price_data_list:
                return self.handle_error(
                    f"No price data found for {ticker_symbol}",
                    exit_code=1
                )

            self.logger.success(f"Retrieved {len(price_data_list)} trading day(s) of data")
            self.logger.info("")  # Blank line for spacing

            # Display summary for multiple days, detailed view for single day
            if len(price_data_list) == 1:
                display_price_data(price_data_list[0])
            else:
                display_price_summary(price_data_list)
                self.logger.info("")  # Blank line for spacing
                
                # Also show the latest day's detailed data
                self.logger.print_section("Latest Trading Day Details")
                display_price_data(price_data_list[-1])

            return self.handle_success()

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to fetch price data: {str(e)}",
                exit_code=1
            )

    def _parse_period(self, period_arg: str) -> TimePeriod:
        """
        Parse period argument to TimePeriod enum.

        Args:
            period_arg: Period string from command line

        Returns:
            TimePeriod enum value
        """
        period_map = {
            '1d': TimePeriod.ONE_DAY,
            '5d': TimePeriod.FIVE_DAYS,
            '1mo': TimePeriod.ONE_MONTH,
            '3mo': TimePeriod.THREE_MONTHS,
            '6mo': TimePeriod.SIX_MONTHS,
            '1y': TimePeriod.ONE_YEAR,
            '2y': TimePeriod.TWO_YEARS,
            '5y': TimePeriod.FIVE_YEARS,
            '10y': TimePeriod.TEN_YEARS,
            'ytd': TimePeriod.YEAR_TO_DATE,
            'max': TimePeriod.MAX,
        }

        return period_map[period_arg.lower()]

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Fetches historical OHLCV data using yfinance and displays formatted price information")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKER: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")
        self.logger.print_bullet("PERIOD: Optional time period for historical data (defaults to '1y')")

        self.logger.print_section("AVAILABLE PERIODS")
        self.logger.print_bullet("1d - 1 day")
        self.logger.print_bullet("5d - 5 days")
        self.logger.print_bullet("1mo - 1 month")
        self.logger.print_bullet("3mo - 3 months")
        self.logger.print_bullet("6mo - 6 months")
        self.logger.print_bullet("1y - 1 year")
        self.logger.print_bullet("2y - 2 years")
        self.logger.print_bullet("5y - 5 years")
        self.logger.print_bullet("10y - 10 years")
        self.logger.print_bullet("ytd - Year to date")
        self.logger.print_bullet("max - Maximum available history")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py price AAPL 1y")
        self.logger.print_example("python main.py price MSFT 3mo")
        self.logger.print_example("python main.py p GOOGL 5y")
        self.logger.print_example("python main.py prices TSLA ytd")

        self.logger.print_section("OUTPUT")
        self.logger.print_bullet("For single day: Displays detailed OHLCV data with the following sections:")
        self.logger.print_bullet("  - Period Information")
        self.logger.print_bullet("  - OHLCV Data (Open, High, Low, Close, Volume)")
        self.logger.print_bullet("  - Daily Performance (Change, Range)")
        self.logger.print_bullet("  - Additional Metrics (VWAP, Turnover)")
        self.logger.print_bullet("For multiple days: Displays summary statistics plus latest day details:")
        self.logger.print_bullet("  - Price Statistics (Latest, High, Low, Average)")
        self.logger.print_bullet("  - Performance (Total Return, Price Range)")
        self.logger.print_bullet("  - Volume Information")
