"""
Magic Command Implementation

This command implements Joel Greenblatt's Magic Formula from "The Little Book That Beats the Market"
to screen and rank stocks based on earnings yield and return on capital.
"""

from typing import List
from .base import BaseCommand
from src.ticker_analysis.core.screening.magic_formula import MagicFormulaFetcher, display_magic_formula_results
from src.ticker_analysis.core.data.fetchers import DataFrequency


class MagicCommand(BaseCommand):
    """Command to screen stocks using the Magic Formula methodology."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "magic"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Screen stocks using Joel Greenblatt's Magic Formula (earnings yield + return on capital)"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["mf", "magic_formula"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <TICKER1,TICKER2,TICKER3,...> [FREQUENCY]\n" \
               f"       TICKERS: Comma-separated list of stock ticker symbols (e.g., AAPL,MSFT,GOOGL)\n" \
               f"       FREQUENCY: 'yearly' or 'quarterly' (can also use 'year', 'quarter', 'y', 'q') - defaults to quarterly"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [ticker_list, frequency (optional)]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required ticker symbols argument")
            self.logger.info("Usage: python main.py magic <TICKER1,TICKER2,TICKER3,...> [FREQUENCY]")
            self.logger.info("Example: python main.py magic AAPL,MSFT,GOOGL,TSLA quarterly")
            return False

        # Validate ticker format
        ticker_input = args[0].strip()
        if not ticker_input:
            self.logger.error("Ticker symbols cannot be empty")
            return False

        # Check for basic format (letters, numbers, commas, periods, hyphens, underscores, spaces allowed)
        import re
        if not re.match(r'^[A-Za-z0-9.,\-_\s]+$', ticker_input):
            # Find invalid characters to help user identify the problem
            invalid_chars = set()
            for char in ticker_input:
                if not re.match(r'[A-Za-z0-9.,\-_\s]', char):
                    invalid_chars.add(char)
            
            if invalid_chars:
                invalid_chars_str = ', '.join(f"'{char}'" for char in sorted(invalid_chars))
                self.logger.error(f"Invalid characters found in ticker symbols: {invalid_chars_str}")
                self.logger.error("Use only letters, numbers, commas, periods, hyphens, underscores, and spaces.")
                self.logger.error(f"Input received: '{ticker_input}'")
            else:
                self.logger.error("Invalid format in ticker symbols. Use only letters, numbers, commas, periods, hyphens, underscores, and spaces.")
            return False

        # Validate frequency argument if provided
        if len(args) >= 2:
            frequency_arg = args[1].lower()
            valid_frequencies = ['yearly', 'quarterly', 'year', 'quarter', 'y', 'q']
            
            if frequency_arg not in valid_frequencies:
                self.logger.error(f"Invalid frequency: {args[1]}")
                self.logger.info(f"Valid frequencies: {', '.join(valid_frequencies)}")
                return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the magic formula command.

        Args:
            args: Command line arguments [ticker_list, frequency (optional)]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Handle help flag
        if args and args[0] in ['--help', '-h', 'help']:
            self.show_help()
            return 0
        
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse ticker symbols
        ticker_input = args[0].strip()
        ticker_symbols = [ticker.strip().upper() for ticker in ticker_input.split(',') if ticker.strip()]
        
        # Parse frequency (default to quarterly)
        frequency = DataFrequency.QUARTERLY
        if len(args) >= 2:
            frequency = self._parse_frequency(args[1])
        
        # Remove duplicates while preserving order
        unique_tickers = []
        seen = set()
        for ticker in ticker_symbols:
            if ticker not in seen:
                unique_tickers.append(ticker)
                seen.add(ticker)
        
        ticker_symbols = unique_tickers

        if not ticker_symbols:
            return self.handle_error("No valid ticker symbols provided")

        if len(ticker_symbols) > 50:
            self.logger.warning(f"Large number of tickers ({len(ticker_symbols)}). This may take a while...")

        self.logger.info(f"Starting Magic Formula screening for: {', '.join(ticker_symbols)} using {frequency.value} data")

        try:
            # Create Magic Formula fetcher with specified frequency
            magic_fetcher = MagicFormulaFetcher(frequency)

            # Screen the tickers
            results = magic_fetcher.screen_tickers(ticker_symbols)

            # Display results
            display_magic_formula_results(results, frequency)

            # Count successful vs failed tickers
            successful_count = len([r for r in results if r.has_complete_data])
            failed_count = len(results) - successful_count

            if successful_count > 0:
                success_msg = f"Magic Formula screening completed successfully for {successful_count}/{len(ticker_symbols)} tickers using {frequency.value} data"
                if failed_count > 0:
                    success_msg += f" ({failed_count} tickers excluded due to missing data)"
                return self.handle_success(success_msg)
            else:
                return self.handle_error(
                    f"No tickers could be processed successfully. All {len(ticker_symbols)} tickers had missing or invalid data.",
                    exit_code=1
                )

        except ValueError as e:
            return self.handle_error(str(e), exit_code=1)

        except Exception as e:
            return self.handle_error(
                f"Failed to complete Magic Formula screening: {str(e)}",
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
        self.logger.print_bullet("Implements Joel Greenblatt's Magic Formula methodology:")
        self.logger.print_bullet("  1. Calculates Earnings Yield (EBIT / Enterprise Value)")
        self.logger.print_bullet("  2. Calculates Return on Capital (EBIT / Invested Capital)")
        self.logger.print_bullet("  3. Ranks stocks by each metric (1 = best)")
        self.logger.print_bullet("  4. Combines rankings (lower total score = better)")
        self.logger.print_bullet("  5. Displays results sorted by Magic Formula score")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ARGUMENTS")
        self.logger.print_bullet("TICKERS: Comma-separated list of stock ticker symbols")
        self.logger.print_bullet("         - No spaces around commas recommended")
        self.logger.print_bullet("         - Duplicates will be automatically removed")
        self.logger.print_bullet("         - Maximum 50 tickers per request")
        self.logger.print_bullet("FREQUENCY: Data frequency - 'yearly', 'quarterly', 'year', 'quarter', 'y', or 'q' (optional, defaults to quarterly)")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py magic AAPL,MSFT,GOOGL")
        self.logger.print_example("python main.py magic AAPL,MSFT,GOOGL quarterly")
        self.logger.print_example("python main.py magic AAPL,MSFT,GOOGL yearly")
        self.logger.print_example("python main.py mf TSLA,NVDA,AMD,INTC q")
        self.logger.print_example("python main.py magic_formula JPM,BAC,WFC,C y")

        self.logger.print_section("OUTPUT SECTIONS")
        self.logger.print_bullet("Ranked Stocks: Companies with complete data, sorted by Magic Formula score")
        self.logger.print_bullet("  - Rank: Final Magic Formula ranking (1 = best)")
        self.logger.print_bullet("  - Ticker: Stock symbol")
        self.logger.print_bullet("  - Company: Company name (truncated if long)")
        self.logger.print_bullet("  - EY: Earnings Yield percentage")
        self.logger.print_bullet("  - ROC: Return on Capital percentage")
        self.logger.print_bullet("  - EY Rank: Earnings Yield ranking")
        self.logger.print_bullet("  - ROC Rank: Return on Capital ranking")
        self.logger.print_bullet("  - Score: Combined ranking score (lower is better)")
        self.logger.print_bullet("Excluded Stocks: Companies with missing or invalid data")
        self.logger.print_bullet("Legend: Explanation of metrics and methodology")

        self.logger.print_section("DATA REQUIREMENTS")
        self.logger.print_bullet("Each ticker must have the following data available:")
        self.logger.print_bullet("  - EBIT (Earnings Before Interest and Taxes)")
        self.logger.print_bullet("  - Enterprise Value")
        self.logger.print_bullet("  - Invested Capital")
        self.logger.print_bullet("Tickers missing any required data will be excluded from ranking")

        self.logger.print_section("METHODOLOGY NOTES")
        self.logger.print_bullet("Based on 'The Little Book That Beats the Market' by Joel Greenblatt")
        self.logger.print_bullet("Uses latest quarterly or yearly financial data for calculations")
        self.logger.print_bullet("Higher earnings yield and return on capital are better")
        self.logger.print_bullet("Lower combined ranking scores indicate better Magic Formula candidates")
        self.logger.print_bullet("This is a screening tool - perform additional analysis before investing")