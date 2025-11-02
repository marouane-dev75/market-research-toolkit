"""
Threshold Checker Module

This module handles the core logic for checking price thresholds against current market prices.
It fetches real-time price data using yfinance and evaluates threshold conditions.
"""

import logging
from typing import List, Dict, Optional
import yfinance as yf
from .models import PriceThreshold, ThresholdResult, ThresholdOperator


class ThresholdChecker:
    """
    Handles price threshold checking and evaluation.
    
    This class fetches current market prices and evaluates them against
    configured thresholds without using cache (as prices change frequently).
    """
    
    def __init__(self):
        """Initialize the threshold checker."""
        self.logger = logging.getLogger(__name__)
    
    def parse_thresholds(self, threshold_strings: List[str]) -> List[PriceThreshold]:
        """
        Parse threshold strings into PriceThreshold objects.
        
        Args:
            threshold_strings: List of threshold strings in format "TICKER:OPERATOR:VALUE"
            
        Returns:
            List[PriceThreshold]: List of parsed threshold objects
        """
        thresholds = []
        
        for threshold_str in threshold_strings:
            try:
                threshold = PriceThreshold.from_string(threshold_str)
                thresholds.append(threshold)
                self.logger.debug(f"Parsed threshold: {threshold.get_description()}")
            except ValueError as e:
                self.logger.error(f"Failed to parse threshold '{threshold_str}': {str(e)}")
                # Continue with other thresholds even if one fails
                continue
        
        return thresholds
    
    def fetch_current_price(self, ticker: str) -> Optional[float]:
        """
        Fetch current market price for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Optional[float]: Current price or None if fetch failed
        """
        try:
            self.logger.debug(f"Fetching current price for {ticker}")
            
            # Create yfinance ticker object
            ticker_obj = yf.Ticker(ticker)
            
            # Get current market data - use fast_info for real-time price
            try:
                # Try to get the last price from fast_info (most recent)
                current_price = ticker_obj.fast_info.get('lastPrice')
                if current_price is not None and current_price > 0:
                    self.logger.debug(f"Got fast_info price for {ticker}: ${current_price:.2f}")
                    return float(current_price)
            except Exception as e:
                self.logger.debug(f"fast_info failed for {ticker}, trying history: {str(e)}")
            
            # Fallback to recent history if fast_info fails
            try:
                hist = ticker_obj.history(period="1d", interval="1m")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    self.logger.debug(f"Got history price for {ticker}: ${current_price:.2f}")
                    return float(current_price)
            except Exception as e:
                self.logger.debug(f"History fallback failed for {ticker}: {str(e)}")
            
            # Final fallback to basic info
            try:
                info = ticker_obj.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                if current_price is not None and current_price > 0:
                    self.logger.debug(f"Got info price for {ticker}: ${current_price:.2f}")
                    return float(current_price)
            except Exception as e:
                self.logger.debug(f"Info fallback failed for {ticker}: {str(e)}")
            
            self.logger.warning(f"No valid price data found for {ticker}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching price for {ticker}: {str(e)}")
            return None
    
    def fetch_multiple_prices(self, tickers: List[str]) -> Dict[str, Optional[float]]:
        """
        Fetch current prices for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Dict[str, Optional[float]]: Dictionary mapping ticker to current price
        """
        prices = {}
        
        for ticker in tickers:
            prices[ticker] = self.fetch_current_price(ticker)
        
        return prices
    
    def evaluate_threshold(self, threshold: PriceThreshold, current_price: Optional[float]) -> ThresholdResult:
        """
        Evaluate a single threshold against current price.
        
        Args:
            threshold: Threshold to evaluate
            current_price: Current market price (None if fetch failed)
            
        Returns:
            ThresholdResult: Result of the evaluation
        """
        # Handle price fetch failure
        if current_price is None:
            return ThresholdResult(
                threshold=threshold,
                current_price=None,
                triggered=False,
                message=f"Failed to fetch price for {threshold.ticker}",
                error=f"Unable to retrieve current price for {threshold.ticker}"
            )
        
        # Evaluate the threshold condition
        triggered = threshold.operator.evaluate(current_price, threshold.target_price)
        
        # Create result message
        if triggered:
            message = f"ALERT: {threshold.ticker} price ${current_price:.2f} is {threshold.operator.get_description()} ${threshold.target_price:.2f}"
        else:
            message = f"OK: {threshold.ticker} price ${current_price:.2f} is not {threshold.operator.get_description()} ${threshold.target_price:.2f}"
        
        return ThresholdResult(
            threshold=threshold,
            current_price=current_price,
            triggered=triggered,
            message=message
        )
    
    def check_thresholds(self, thresholds: List[PriceThreshold]) -> List[ThresholdResult]:
        """
        Check all thresholds against current market prices.
        
        Args:
            thresholds: List of thresholds to check
            
        Returns:
            List[ThresholdResult]: Results for all threshold evaluations
        """
        if not thresholds:
            self.logger.info("No thresholds to check")
            return []
        
        self.logger.info(f"Checking {len(thresholds)} price thresholds...")
        
        # Get unique tickers
        tickers = list(set(threshold.ticker for threshold in thresholds))
        self.logger.debug(f"Fetching prices for tickers: {', '.join(tickers)}")
        
        # Fetch all prices at once for efficiency
        current_prices = self.fetch_multiple_prices(tickers)
        
        # Evaluate each threshold
        results = []
        for threshold in thresholds:
            current_price = current_prices.get(threshold.ticker)
            result = self.evaluate_threshold(threshold, current_price)
            results.append(result)
            
            # Log the result
            if result.triggered:
                self.logger.warning(f"THRESHOLD TRIGGERED: {result.message}")
            else:
                self.logger.debug(f"Threshold OK: {result.message}")
        
        # Summary logging
        triggered_count = sum(1 for result in results if result.triggered)
        error_count = sum(1 for result in results if result.error)
        
        self.logger.info(f"Threshold check complete: {triggered_count} triggered, {error_count} errors")
        
        return results
    
    def get_triggered_results(self, results: List[ThresholdResult]) -> List[ThresholdResult]:
        """
        Filter results to only include triggered thresholds.
        
        Args:
            results: List of all threshold results
            
        Returns:
            List[ThresholdResult]: Only triggered results
        """
        return [result for result in results if result.triggered and result.is_success]
    
    def get_error_results(self, results: List[ThresholdResult]) -> List[ThresholdResult]:
        """
        Filter results to only include errors.
        
        Args:
            results: List of all threshold results
            
        Returns:
            List[ThresholdResult]: Only error results
        """
        return [result for result in results if result.error is not None]