"""
Monitor Command Implementation

This command runs price monitoring checks against configured thresholds
and sends notifications when thresholds are triggered.
"""

from typing import List
from .base import BaseCommand
from ....infrastructure.monitoring.manager import get_price_monitor_manager


class MonitorCommand(BaseCommand):
    """Command to run price monitoring checks."""

    @property
    def name(self) -> str:
        """Return the command name."""
        return "monitor"

    @property
    def description(self) -> str:
        """Return the command description."""
        return "Monitor stock prices against configured thresholds and send alerts"

    @property
    def aliases(self) -> List[str]:
        """Return command aliases."""
        return ["m", "watch", "alert"]

    @property
    def usage(self) -> str:
        """Return command usage string."""
        return f"python main.py {self.name} [--test] [--status]\n" \
               f"       --test: Test configuration without running monitoring\n" \
               f"       --status: Show current monitoring status and configuration"

    def validate_args(self, args: List[str]) -> bool:
        """
        Validate command arguments.

        Args:
            args: Command line arguments

        Returns:
            True if arguments are valid, False otherwise
        """
        # Check for invalid arguments
        valid_flags = ["--test", "--status", "--help", "-h"]
        for arg in args:
            if arg.startswith("--") and arg not in valid_flags:
                self.logger.error(f"Unknown flag: {arg}")
                self.logger.info(f"Valid flags: {', '.join(valid_flags)}")
                return False
        
        return True

    def execute(self, args: List[str]) -> int:
        """
        Execute the monitor command.

        Args:
            args: Command line arguments

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Validate arguments
        if not self.validate_args(args):
            return 1

        # Handle help flag
        if "--help" in args or "-h" in args:
            self.show_help()
            return 0

        try:
            manager = get_price_monitor_manager()

            # Handle status flag
            if "--status" in args:
                return self._show_status(manager)

            # Handle test flag
            if "--test" in args:
                return self._test_configuration(manager)

            # Run normal monitoring
            return self._run_monitoring(manager)

        except Exception as e:
            return self.handle_error(f"Failed to run price monitoring: {str(e)}")

    def _show_status(self, manager) -> int:
        """
        Show monitoring status and configuration.

        Args:
            manager: PriceMonitorManager instance

        Returns:
            Exit code
        """
        self.logger.print_header("Price Monitoring Status")

        try:
            status = manager.get_monitoring_status()

            self.logger.print_section("Configuration")
            self.logger.print_bullet(f"Monitoring enabled: {'✅ Yes' if status['enabled'] else '❌ No'}")
            self.logger.print_bullet(f"Notifications enabled: {'✅ Yes' if status['notifications_enabled'] else '❌ No'}")
            self.logger.print_bullet(f"Configured thresholds: {status['threshold_count']}")

            if status['configured_tickers']:
                self.logger.print_section("Monitored Tickers")
                for ticker in sorted(status['configured_tickers']):
                    self.logger.print_bullet(ticker)

            if status['notification_providers']:
                self.logger.print_section("Available Notification Providers")
                for provider in status['notification_providers']:
                    self.logger.print_bullet(f"{provider.value}")
            else:
                self.logger.print_section("Notification Providers")
                self.logger.print_bullet("❌ No providers configured")

            return self.handle_success()

        except Exception as e:
            return self.handle_error(f"Failed to get monitoring status: {str(e)}")

    def _test_configuration(self, manager) -> int:
        """
        Test the monitoring configuration.

        Args:
            manager: PriceMonitorManager instance

        Returns:
            Exit code
        """
        self.logger.print_header("Price Monitoring Configuration Test")

        try:
            test_results = manager.test_configuration()

            # Show overall status
            self.logger.print_section("Overall Status")
            self.logger.print_bullet(f"Monitoring enabled: {'✅ Yes' if test_results['monitoring_enabled'] else '❌ No'}")
            self.logger.print_bullet(f"Notifications enabled: {'✅ Yes' if test_results['notifications_enabled'] else '❌ No'}")

            # Show threshold parsing results
            self.logger.print_section("Threshold Configuration")
            if not test_results['thresholds']:
                self.logger.print_bullet("❌ No thresholds configured")
            else:
                valid_count = sum(1 for t in test_results['thresholds'] if t['parsed'])
                invalid_count = len(test_results['thresholds']) - valid_count
                
                self.logger.print_bullet(f"Total thresholds: {len(test_results['thresholds'])}")
                self.logger.print_bullet(f"Valid thresholds: ✅ {valid_count}")
                if invalid_count > 0:
                    self.logger.print_bullet(f"Invalid thresholds: ❌ {invalid_count}")

                # Show details for each threshold
                for threshold in test_results['thresholds']:
                    if threshold['parsed']:
                        self.logger.print_bullet(
                            f"✅ {threshold['string']} → {threshold['ticker']} {threshold['operator']} ${threshold['target_price']:.2f}",
                            indent=4
                        )
                    else:
                        self.logger.print_bullet(f"❌ {threshold['string']} → Error: {threshold['error']}", indent=4)

            # Show notification test results
            if test_results['notification_test'] is not None:
                self.logger.print_section("Notification Test")
                if test_results['notification_test']['success']:
                    self.logger.print_bullet("✅ Test notification sent successfully")
                else:
                    self.logger.print_bullet(f"❌ Test notification failed: {test_results['notification_test']['error']}")
            else:
                self.logger.print_section("Notification Test")
                self.logger.print_bullet("⏭️ Skipped (notifications disabled)")

            return self.handle_success("Configuration test completed")

        except Exception as e:
            return self.handle_error(f"Failed to test configuration: {str(e)}")

    def _run_monitoring(self, manager) -> int:
        """
        Run the actual monitoring check.

        Args:
            manager: PriceMonitorManager instance

        Returns:
            Exit code
        """
        self.logger.print_header("Running Price Monitoring Check")

        try:
            # Check if monitoring is enabled
            if not manager.is_enabled():
                self.logger.warning("Price monitoring is disabled in configuration")
                self.logger.info("Enable it in config.yml under 'price_monitor.enabled'")
                return 1

            # Run the monitoring check
            results = manager.run_monitoring_check()

            if not results:
                self.logger.info("No thresholds configured or all parsing failed")
                return 1

            # Display results
            self.logger.print_section("Monitoring Results")

            triggered_results = [r for r in results if r.triggered and r.is_success]
            error_results = [r for r in results if r.error is not None]
            ok_results = [r for r in results if not r.triggered and r.is_success]

            # Show summary
            self.logger.print_bullet(f"Total thresholds checked: {len(results)}")
            self.logger.print_bullet(f"Thresholds triggered: {len(triggered_results)}")
            self.logger.print_bullet(f"Thresholds OK: {len(ok_results)}")
            if error_results:
                self.logger.print_bullet(f"Errors encountered: {len(error_results)}")

            # Show triggered alerts
            if triggered_results:
                self.logger.print_section("🚨 TRIGGERED ALERTS")
                for result in triggered_results:
                    self.logger.print_bullet(result.get_alert_message())

            # Show errors if any
            if error_results:
                self.logger.print_section("❌ ERRORS")
                for result in error_results:
                    self.logger.print_bullet(f"{result.ticker}: {result.error}")

            # Show OK results in debug mode
            if ok_results and self.logger.logger.level <= 10:  # DEBUG level
                self.logger.print_section("✅ OK (No Alerts)")
                for result in ok_results:
                    self.logger.print_bullet(f"{result.ticker}: ${result.current_price:.2f}")

            # Final status
            if triggered_results:
                self.logger.warning(f"⚠️  {len(triggered_results)} threshold(s) triggered - notifications sent")
                return 0  # Not an error, just alerts
            else:
                return self.handle_success("✅ All thresholds OK - no alerts triggered")

        except Exception as e:
            return self.handle_error(f"Failed to run monitoring check: {str(e)}")

    def show_help(self) -> None:
        """Show detailed help information for this command."""
        self.logger.print_header(f"{self.name.upper()} Command Help")

        self.logger.print_section("DESCRIPTION")
        self.logger.print_bullet(self.description)
        self.logger.print_bullet("Monitors stock prices against configured thresholds in config.yml")
        self.logger.print_bullet("Sends notifications via Telegram when thresholds are triggered")

        self.logger.print_section("USAGE")
        lines = self.usage.split('\n')
        for line in lines:
            if line.strip():
                self.logger.print_bullet(line.strip())

        self.logger.print_section("FLAGS")
        self.logger.print_bullet("--status: Show current monitoring configuration and status")
        self.logger.print_bullet("--test: Test configuration and send test notification")
        self.logger.print_bullet("--help, -h: Show this help message")

        if self.aliases:
            self.logger.print_section("ALIASES")
            for alias in self.aliases:
                self.logger.print_bullet(alias)

        self.logger.print_section("CONFIGURATION")
        self.logger.print_bullet("Configure thresholds in config.yml under 'price_monitor.thresholds'")
        self.logger.print_bullet("Threshold format: 'TICKER:OPERATOR:VALUE'")
        self.logger.print_bullet("Operators: eq (equal), gt (>), lt (<), gte (>=), lte (<=)")

        self.logger.print_section("EXAMPLES")
        self.logger.print_example("python main.py monitor")
        self.logger.print_example("python main.py monitor --status")
        self.logger.print_example("python main.py monitor --test")
        self.logger.print_example("python main.py m")  # Using alias

        self.logger.print_section("THRESHOLD EXAMPLES")
        self.logger.print_bullet("AAPL:gt:150 - Alert when Apple stock > $150")
        self.logger.print_bullet("MSFT:lt:300 - Alert when Microsoft stock < $300")
        self.logger.print_bullet("TSLA:eq:200 - Alert when Tesla stock equals $200")
        self.logger.print_bullet("GOOGL:gte:2500 - Alert when Google stock >= $2500")
