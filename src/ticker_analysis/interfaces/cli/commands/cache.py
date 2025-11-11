"""
Cache Command Implementation

This command provides cache management functionality including statistics,
cleaning, and configuration display.
"""

from typing import List
from .base import BaseCommand
from ....infrastructure.cache.manager import get_cache_manager, CacheConfig, CacheUtils


class CacheCommand(BaseCommand):
    """Command to manage financial data cache."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "cache"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Manage financial data cache (stats, clean, clear, info)"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["c"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} <ACTION> [OPTIONS]\n" \
               f"       ACTIONS: stats, clean, clear, info\n" \
               f"       OPTIONS: [ticker] for clear action"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments [action, options...]

        Returns:
            True if arguments are valid, False otherwise
        """
        if len(args) < 1:
            self.logger.error("Missing required action argument")
            self.logger.info("Usage: python main.py cache <ACTION>")
            self.logger.info("Actions: stats, clean, clear, info")
            return False

        valid_actions = ['stats', 'clean', 'clear', 'info']
        action = args[0].lower()
        
        if action not in valid_actions:
            self.logger.error(f"Invalid action: {action}")
            self.logger.info(f"Valid actions: {', '.join(valid_actions)}")
            return False

        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the cache command.

        Args:
            args: Command line arguments [action, options...]

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Parse arguments
        action = args[0].lower()
        
        try:
            cache_manager = get_cache_manager()
            
            if action == "stats":
                return self._show_cache_stats(cache_manager)
            elif action == "clean":
                return self._clean_expired_cache(cache_manager)
            elif action == "clear":
                ticker = args[1] if len(args) > 1 else None
                return self._clear_cache(cache_manager, ticker)
            elif action == "info":
                return self._show_cache_info()
            
        except Exception as e:
            return self.handle_error(f"Cache operation failed: {str(e)}", exit_code=1)

        return 0

    def _show_cache_stats(self, cache_manager) -> int:
        """Show cache statistics."""
        self.logger.info("Retrieving cache statistics...")
        
        try:
            stats = cache_manager.get_cache_stats()
            
            self.logger.print_header("Cache Statistics")
            
            # Overall Statistics
            self.logger.print_section("Overall Statistics")
            self.logger.print_bullet(f"Total Entries: {stats['total_entries']}")
            self.logger.print_bullet(f"Valid Entries: {stats['valid_entries']}")
            self.logger.print_bullet(f"Expired Entries: {stats['expired_entries']}")
            self.logger.print_bullet(f"Total Size: {stats['total_size_formatted']}")
            self.logger.print_bullet(f"Cache Directory: {stats['cache_directory']}")
            self.logger.print_bullet(f"Cache Enabled: {'Yes' if stats['cache_enabled'] else 'No'}")
            
            # Statistics by Data Type
            if stats['stats_by_type']:
                self.logger.print_section("Statistics by Data Type")
                for data_type, type_stats in stats['stats_by_type'].items():
                    size_formatted = CacheUtils.format_cache_size(type_stats['size'])
                    self.logger.print_bullet(f"{data_type.replace('_', ' ').title()}: {type_stats['count']} entries, {size_formatted}")
            
            return self.handle_success("Cache statistics retrieved successfully")
            
        except Exception as e:
            return self.handle_error(f"Failed to retrieve cache statistics: {str(e)}")

    def _clean_expired_cache(self, cache_manager) -> int:
        """Clean expired cache entries."""
        self.logger.info("Cleaning expired cache entries...")
        
        try:
            removed_count = cache_manager.clean_expired_cache()
            
            if removed_count > 0:
                return self.handle_success(f"Successfully cleaned {removed_count} expired cache entries")
            else:
                return self.handle_success("No expired cache entries found")
                
        except Exception as e:
            return self.handle_error(f"Failed to clean expired cache: {str(e)}")

    def _clear_cache(self, cache_manager, ticker: str = None) -> int:
        """Clear cache entries."""
        if ticker:
            self.logger.info(f"Clearing cache for ticker {ticker}...")
            try:
                removed_count = cache_manager.clean_ticker_cache(ticker)
                if removed_count > 0:
                    return self.handle_success(f"Successfully cleared {removed_count} cache entries for {ticker}")
                else:
                    return self.handle_success(f"No cache entries found for {ticker}")
            except Exception as e:
                return self.handle_error(f"Failed to clear cache for {ticker}: {str(e)}")
        else:
            self.logger.warning("This will clear ALL cache entries. Are you sure? (This action cannot be undone)")
            self.logger.info("Clearing all cache entries...")
            try:
                removed_count = cache_manager.clean_all_cache()
                return self.handle_success(f"Successfully cleared all {removed_count} cache entries")
            except Exception as e:
                return self.handle_error(f"Failed to clear all cache: {str(e)}")

    def _show_cache_info(self) -> int:
        """Show cache configuration information."""
        self.logger.print_header("Cache Configuration")
        
        # Cache Configuration
        config_summary = CacheConfig.get_cache_stats_summary()
        
        self.logger.print_section("General Configuration")
        self.logger.print_bullet(f"Cache Directory: {config_summary['cache_directory']}")
        self.logger.print_bullet(f"Total Data Types: {config_summary['total_data_types']}")
        self.logger.print_bullet(f"Enabled Data Types: {config_summary['enabled_data_types']}")
        
        # Data Type Configuration
        self.logger.print_section("Data Type Configuration")
        for data_type, config in config_summary['data_types'].items():
            status = "Enabled" if config['enabled'] else "Disabled"
            ttl = config['ttl_hours']
            ttl_desc = f"{ttl} hours"
            if ttl >= 24:
                days = ttl // 24
                ttl_desc += f" ({days} day{'s' if days != 1 else ''})"
            
            self.logger.print_bullet(f"{data_type.replace('_', ' ').title()}: {status}, TTL: {ttl_desc}")
            self.logger.print_bullet(f"  Description: {config['description']}", indent=4)
        
        # Environment Variables
        self.logger.print_section("Environment Configuration")
        self.logger.print_bullet("TICKER_CACHE_DIR: Override default cache directory")
        
        return self.handle_success("Cache configuration displayed successfully")

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Provides comprehensive cache management functionality:")
        self.logger.print_bullet("  - View cache statistics and usage")
        self.logger.print_bullet("  - Clean expired cache entries")
        self.logger.print_bullet("  - Clear cache for specific tickers or all data")
        self.logger.print_bullet("  - Display cache configuration and settings")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            self.logger.print_bullet(line.strip())

        self.logger.print_section("ACTIONS")
        self.logger.print_bullet("stats  - Display cache statistics and usage information")
        self.logger.print_bullet("clean  - Remove expired cache entries")
        self.logger.print_bullet("clear  - Clear cache entries (optionally for specific ticker)")
        self.logger.print_bullet("info   - Show cache configuration and settings")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py cache stats")
        self.logger.print_example("python main.py cache clean")
        self.logger.print_example("python main.py cache clear AAPL")
        self.logger.print_example("python main.py cache clear")
        self.logger.print_example("python main.py cache info")
        self.logger.print_example("python main.py c stats")

        self.logger.print_section("CACHE DATA TYPES")
        self.logger.print_bullet("company_info: Company information and metrics (TTL: 1 week)")
        self.logger.print_bullet("income_statements: Income statement data (TTL: 1 week)")
        self.logger.print_bullet("balance_sheets: Balance sheet data (TTL: 1 week)")
        self.logger.print_bullet("cash_flows: Cash flow statement data (TTL: 1 week)")
        self.logger.print_bullet("dividends: Dividend payment history (TTL: 1 week)")
        self.logger.print_bullet("price_data: Historical price and volume data (TTL: 1 day)")
