#!/usr/bin/env python3
"""
Global integration test that calls all CLI commands with test tickers.

This test verifies that all commands can be executed successfully with
the provided test tickers: AAPL, GOOGL, MSFT, NVDA, TSLA

Usage:
    python tests/test_integration_global.py
"""

import sys
import os
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ticker_analysis.interfaces.cli.manager import main as cli_main


class GlobalIntegrationTest:
    """Global integration test class for all CLI commands."""
    
    # Test tickers as specified in the requirements
    TEST_TICKERS = ["AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"]
    
    def __init__(self):
        """Initialize the test runner."""
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        self.failures = []
        
    def run_command(self, command_args, description=""):
        """
        Helper method to run a CLI command and capture its exit code.
        
        Args:
            command_args: List of command arguments
            description: Description of the test for logging
            
        Returns:
            Exit code from the command
        """
        try:
            # Capture output to prevent cluttering test output
            with StringIO() as captured_output:
                with redirect_stdout(captured_output), redirect_stderr(captured_output):
                    exit_code = cli_main(command_args)
                return exit_code
        except SystemExit as e:
            return e.code if e.code is not None else 0
        except Exception as e:
            print(f"Exception during command execution ({description}): {e}")
            return 1
    
    def assert_success(self, exit_code, test_name, details=""):
        """Assert that a command executed successfully."""
        self.total_tests += 1
        if exit_code == 0:
            self.passed_tests += 1
            print(f"✓ {test_name}")
        else:
            self.failed_tests += 1
            failure_msg = f"✗ {test_name} - Exit code: {exit_code}"
            if details:
                failure_msg += f" ({details})"
            print(failure_msg)
            self.failures.append(failure_msg)
    
    def test_analysis_command(self):
        """Test the analysis command with all test tickers."""
        print("\n=== Testing Analysis Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["analysis", ticker], f"analysis {ticker}")
            self.assert_success(exit_code, f"Analysis command for {ticker}")
    
    def test_analysis_command_aliases(self):
        """Test the analysis command aliases."""
        print("\n=== Testing Analysis Command Aliases ===")
        exit_code = self.run_command(["a", "AAPL"], "analysis alias 'a'")
        self.assert_success(exit_code, "Analysis alias 'a' with AAPL")
        
        exit_code = self.run_command(["analyze", "GOOGL"], "analysis alias 'analyze'")
        self.assert_success(exit_code, "Analysis alias 'analyze' with GOOGL")
    
    def test_magic_formula_command(self):
        """Test the magic formula command."""
        print("\n=== Testing Magic Formula Command ===")
        tickers_str = ",".join(self.TEST_TICKERS)
        exit_code = self.run_command(["magic", tickers_str], "magic formula with all tickers")
        self.assert_success(exit_code, "Magic formula with all test tickers")
        
        exit_code = self.run_command(["magic", "AAPL,MSFT", "yearly"], "magic formula yearly")
        self.assert_success(exit_code, "Magic formula with yearly data")
    
    def test_magic_formula_aliases(self):
        """Test magic formula command aliases."""
        print("\n=== Testing Magic Formula Aliases ===")
        exit_code = self.run_command(["mf", "AAPL,GOOGL"], "magic formula alias 'mf'")
        self.assert_success(exit_code, "Magic formula alias 'mf'")
        
        exit_code = self.run_command(["magic_formula", "MSFT,NVDA"], "magic formula alias 'magic_formula'")
        self.assert_success(exit_code, "Magic formula alias 'magic_formula'")
    
    def test_income_statement_command(self):
        """Test the income statement command."""
        print("\n=== Testing Income Statement Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["income", ticker], f"income {ticker}")
            self.assert_success(exit_code, f"Income command for {ticker}")
            
            exit_code = self.run_command(["income", ticker, "yearly"], f"income {ticker} yearly")
            self.assert_success(exit_code, f"Income command yearly for {ticker}")
    
    def test_income_command_alias(self):
        """Test income command alias."""
        print("\n=== Testing Income Command Alias ===")
        exit_code = self.run_command(["inc", "AAPL"], "income alias 'inc'")
        self.assert_success(exit_code, "Income alias 'inc' with AAPL")
    
    def test_balance_sheet_command(self):
        """Test the balance sheet command."""
        print("\n=== Testing Balance Sheet Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["balance", ticker], f"balance {ticker}")
            self.assert_success(exit_code, f"Balance command for {ticker}")
            
            exit_code = self.run_command(["balance", ticker, "yearly"], f"balance {ticker} yearly")
            self.assert_success(exit_code, f"Balance command yearly for {ticker}")
    
    def test_balance_command_alias(self):
        """Test balance command alias."""
        print("\n=== Testing Balance Command Alias ===")
        exit_code = self.run_command(["bal", "MSFT"], "balance alias 'bal'")
        self.assert_success(exit_code, "Balance alias 'bal' with MSFT")
    
    def test_cashflow_command(self):
        """Test the cash flow command."""
        print("\n=== Testing Cash Flow Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["cashflow", ticker], f"cashflow {ticker}")
            self.assert_success(exit_code, f"Cashflow command for {ticker}")
            
            exit_code = self.run_command(["cashflow", ticker, "yearly"], f"cashflow {ticker} yearly")
            self.assert_success(exit_code, f"Cashflow command yearly for {ticker}")
    
    def test_cashflow_command_alias(self):
        """Test cashflow command alias."""
        print("\n=== Testing Cash Flow Command Alias ===")
        exit_code = self.run_command(["cf", "GOOGL"], "cashflow alias 'cf'")
        self.assert_success(exit_code, "Cashflow alias 'cf' with GOOGL")
    
    def test_dividend_command(self):
        """Test the dividend command."""
        print("\n=== Testing Dividend Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["dividend", ticker], f"dividend {ticker}")
            self.assert_success(exit_code, f"Dividend command for {ticker}")
    
    def test_dividend_command_alias(self):
        """Test dividend command alias."""
        print("\n=== Testing Dividend Command Alias ===")
        exit_code = self.run_command(["div", "AAPL"], "dividend alias 'div'")
        self.assert_success(exit_code, "Dividend alias 'div' with AAPL")
    
    def test_price_command(self):
        """Test the price command."""
        print("\n=== Testing Price Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["price", ticker], f"price {ticker}")
            self.assert_success(exit_code, f"Price command for {ticker}")
    
    def test_price_command_alias(self):
        """Test price command alias."""
        print("\n=== Testing Price Command Alias ===")
        exit_code = self.run_command(["p", "NVDA"], "price alias 'p'")
        self.assert_success(exit_code, "Price alias 'p' with NVDA")
    
    def test_info_command(self):
        """Test the info command."""
        print("\n=== Testing Info Command ===")
        for ticker in self.TEST_TICKERS:
            exit_code = self.run_command(["info", ticker], f"info {ticker}")
            self.assert_success(exit_code, f"Info command for {ticker}")
    
    def test_info_command_alias(self):
        """Test info command alias."""
        print("\n=== Testing Info Command Alias ===")
        exit_code = self.run_command(["i", "TSLA"], "info alias 'i'")
        self.assert_success(exit_code, "Info alias 'i' with TSLA")
    
    def test_cache_commands(self):
        """Test cache management commands."""
        print("\n=== Testing Cache Commands ===")
        exit_code = self.run_command(["cache", "stats"], "cache stats")
        self.assert_success(exit_code, "Cache stats command")

        exit_code = self.run_command(["cache", "clear", "AAPL"], "cache clear AAPL")
        self.assert_success(exit_code, "Cache clear for AAPL")

        exit_code = self.run_command(["cache", "clear"], "cache clear all")
        self.assert_success(exit_code, "Cache clear all")
    
    def test_cache_command_alias(self):
        """Test cache command alias."""
        print("\n=== Testing Cache Command Alias ===")
        exit_code = self.run_command(["c", "stats"], "cache alias 'c'")
        self.assert_success(exit_code, "Cache alias 'c' stats")
    
    def test_monitor_commands(self):
        """Test monitoring commands."""
        print("\n=== Testing Monitor Commands ===")
        exit_code = self.run_command(["monitor", "--status"], "monitor status")
        self.assert_success(exit_code, "Monitor status command")
        
        exit_code = self.run_command(["monitor", "--test"], "monitor test")
        self.assert_success(exit_code, "Monitor test command")
    
    def test_monitor_command_aliases(self):
        """Test monitor command aliases."""
        print("\n=== Testing Monitor Command Aliases ===")
        exit_code = self.run_command(["m", "--status"], "monitor alias 'm'")
        self.assert_success(exit_code, "Monitor alias 'm' status")
        
        exit_code = self.run_command(["watch", "--status"], "monitor alias 'watch'")
        self.assert_success(exit_code, "Monitor alias 'watch' status")
        
        exit_code = self.run_command(["alert", "--status"], "monitor alias 'alert'")
        self.assert_success(exit_code, "Monitor alias 'alert' status")
    
    def test_help_commands(self):
        """Test help functionality."""
        print("\n=== Testing Help Commands ===")
        commands = [
            "analysis", "magic", "income", "balance", "cashflow", 
            "dividend", "price", "info", "cache", "monitor"
        ]
        
        for command in commands:
            exit_code = self.run_command([command, "--help"], f"{command} help")
            self.assert_success(exit_code, f"Help for {command} command")
    
    def test_global_help_and_version(self):
        """Test global help and version commands."""
        print("\n=== Testing Global Help and Version ===")
        exit_code = self.run_command(["--help"], "global help")
        self.assert_success(exit_code, "Global --help flag")
        
        exit_code = self.run_command(["-h"], "global help short")
        self.assert_success(exit_code, "Global -h flag")
        
        exit_code = self.run_command(["--version"], "version")
        self.assert_success(exit_code, "Global --version flag")
        
        exit_code = self.run_command(["-v"], "version short")
        self.assert_success(exit_code, "Global -v flag")
    
    def test_comprehensive_workflow(self):
        """Test a comprehensive workflow using multiple commands."""
        print("\n=== Testing Comprehensive Workflow ===")
        ticker = "AAPL"
        
        workflow_steps = [
            (["info", ticker], f"Workflow: info {ticker}"),
            (["analysis", ticker], f"Workflow: analysis {ticker}"),
            (["price", ticker], f"Workflow: price {ticker}"),
            (["dividend", ticker], f"Workflow: dividend {ticker}"),
            (["income", ticker], f"Workflow: income {ticker}"),
            (["balance", ticker], f"Workflow: balance {ticker}"),
            (["cashflow", ticker], f"Workflow: cashflow {ticker}"),
            (["magic", f"{ticker},GOOGL"], "Workflow: magic formula"),
            (["cache", "stats"], "Workflow: cache stats"),
        ]
        
        for command_args, description in workflow_steps:
            exit_code = self.run_command(command_args, description)
            self.assert_success(exit_code, description)
    
    def run_all_tests(self):
        """Run all integration tests."""
        print("=" * 60)
        print("GLOBAL INTEGRATION TEST - TICKER ANALYSIS TOOL")
        print("=" * 60)
        print(f"Testing with tickers: {', '.join(self.TEST_TICKERS)}")
        print("=" * 60)
        
        # Run all test methods
        test_methods = [
            self.test_analysis_command,
            self.test_analysis_command_aliases,
            self.test_magic_formula_command,
            self.test_magic_formula_aliases,
            self.test_income_statement_command,
            self.test_income_command_alias,
            self.test_balance_sheet_command,
            self.test_balance_command_alias,
            self.test_cashflow_command,
            self.test_cashflow_command_alias,
            self.test_dividend_command,
            self.test_dividend_command_alias,
            self.test_price_command,
            self.test_price_command_alias,
            self.test_info_command,
            self.test_info_command_alias,
            self.test_cache_commands,
            self.test_cache_command_alias,
            self.test_monitor_commands,
            self.test_monitor_command_aliases,
            self.test_help_commands,
            self.test_global_help_and_version,
            self.test_comprehensive_workflow,
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"Error running {test_method.__name__}: {e}")
                self.failed_tests += 1
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        if self.failed_tests > 0:
            print(f"\nFAILURES ({self.failed_tests}):")
            for failure in self.failures:
                print(f"  {failure}")
            print("\n" + "=" * 60)
            return 1
        else:
            print("\n🎉 ALL TESTS PASSED! 🎉")
            print("=" * 60)
            return 0


def main():
    """Main entry point for the integration test."""
    test_runner = GlobalIntegrationTest()
    exit_code = test_runner.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
