"""
Price Monitor Manager

This module provides the main orchestration for price monitoring functionality.
It coordinates threshold checking, notification sending, and configuration management.
"""

import logging
from typing import List, Optional
from datetime import datetime

from .models import PriceThreshold, ThresholdResult
from .threshold_checker import ThresholdChecker
from src.ticker_analysis.config import get_config_manager
from src.ticker_analysis.infrastructure.notifications.manager import get_notification_manager


class PriceMonitorManager:
    """
    Main manager for price monitoring operations.
    
    This class orchestrates the entire price monitoring workflow:
    1. Load configuration
    2. Parse thresholds
    3. Check current prices
    4. Send notifications if thresholds are triggered
    """
    
    def __init__(self):
        """Initialize the price monitor manager."""
        self.logger = logging.getLogger(__name__)
        self.config_manager = get_config_manager()
        self.notification_manager = get_notification_manager()
        self.threshold_checker = ThresholdChecker()
    
    def is_enabled(self) -> bool:
        """
        Check if price monitoring is enabled in configuration.
        
        Returns:
            bool: True if price monitoring is enabled
        """
        return self.config_manager.is_price_monitor_enabled()
    
    def get_configured_thresholds(self) -> List[PriceThreshold]:
        """
        Get thresholds from configuration.
        
        Returns:
            List[PriceThreshold]: List of configured thresholds
        """
        if not self.is_enabled():
            self.logger.info("Price monitoring is disabled in configuration")
            return []
        
        threshold_strings = self.config_manager.get_price_thresholds()
        if not threshold_strings:
            self.logger.info("No price thresholds configured")
            return []
        
        self.logger.info(f"Loading {len(threshold_strings)} configured thresholds")
        return self.threshold_checker.parse_thresholds(threshold_strings)
    
    def run_monitoring_check(self) -> List[ThresholdResult]:
        """
        Run a complete monitoring check cycle.
        
        Returns:
            List[ThresholdResult]: Results of all threshold checks
        """
        self.logger.info("Starting price monitoring check...")
        
        # Check if monitoring is enabled
        if not self.is_enabled():
            self.logger.info("Price monitoring is disabled")
            return []
        
        # Get configured thresholds
        thresholds = self.get_configured_thresholds()
        if not thresholds:
            self.logger.info("No valid thresholds to monitor")
            return []
        
        # Check thresholds against current prices
        results = self.threshold_checker.check_thresholds(thresholds)
        
        # Send notifications if any thresholds were triggered
        triggered_results = self.threshold_checker.get_triggered_results(results)
        if triggered_results:
            self._send_notifications(triggered_results, results)
        else:
            self.logger.info("No thresholds triggered - no notifications sent")
        
        return results
    
    def _send_notifications(self, triggered_results: List[ThresholdResult], all_results: List[ThresholdResult]) -> None:
        """
        Send notifications for triggered thresholds.
        
        Args:
            triggered_results: List of triggered threshold results
            all_results: List of all threshold results (for context)
        """
        if not self.config_manager.are_price_notifications_enabled():
            self.logger.info("Price notifications are disabled - skipping notification")
            return
        
        if not self.notification_manager.is_any_provider_configured():
            self.logger.warning("No notification providers configured - cannot send alerts")
            return
        
        # Build notification message
        message = self._build_notification_message(triggered_results, all_results)
        
        # Send notification
        self.logger.info(f"Sending notification for {len(triggered_results)} triggered threshold(s)")
        result = self.notification_manager.send_message(message)
        
        if result.status.name == "SUCCESS":
            self.logger.info("Price alert notification sent successfully")
        else:
            self.logger.error(f"Failed to send price alert notification: {result.error_details}")
    
    def _build_notification_message(self, triggered_results: List[ThresholdResult], all_results: List[ThresholdResult]) -> str:
        """
        Build the notification message for triggered thresholds.
        
        Args:
            triggered_results: List of triggered threshold results
            all_results: List of all threshold results
            
        Returns:
            str: Formatted notification message
        """
        # Get message template from configuration
        template = self.config_manager.get_price_notification_template()
        
        # Build details section
        details_lines = []
        
        # Add triggered alerts
        for result in triggered_results:
            details_lines.append(result.get_alert_message())
        
        # Add summary information
        details_lines.append("")  # Empty line for spacing
        details_lines.append(f"📊 Summary:")
        details_lines.append(f"• Total thresholds checked: {len(all_results)}")
        details_lines.append(f"• Thresholds triggered: {len(triggered_results)}")
        
        # Add error information if any
        error_results = self.threshold_checker.get_error_results(all_results)
        if error_results:
            details_lines.append(f"• Errors encountered: {len(error_results)}")
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        details_lines.append(f"• Check time: {timestamp}")
        
        details = "\n".join(details_lines)
        
        # Format the message using the template
        message = template.format(
            triggered_count=len(triggered_results),
            details=details
        )
        
        return message
    
    def get_monitoring_status(self) -> dict:
        """
        Get current monitoring status and configuration.
        
        Returns:
            dict: Status information
        """
        thresholds = self.get_configured_thresholds()
        
        return {
            "enabled": self.is_enabled(),
            "notifications_enabled": self.config_manager.are_price_notifications_enabled(),
            "threshold_count": len(thresholds),
            "configured_tickers": list(set(t.ticker for t in thresholds)),
            "notification_providers": self.notification_manager.get_available_providers()
        }
    
    def test_configuration(self) -> dict:
        """
        Test the price monitoring configuration.
        
        Returns:
            dict: Test results
        """
        results = {
            "monitoring_enabled": self.is_enabled(),
            "notifications_enabled": self.config_manager.are_price_notifications_enabled(),
            "thresholds": [],
            "notification_test": None
        }
        
        # Test threshold parsing
        threshold_strings = self.config_manager.get_price_thresholds()
        for threshold_str in threshold_strings:
            try:
                threshold = PriceThreshold.from_string(threshold_str)
                results["thresholds"].append({
                    "string": threshold_str,
                    "parsed": True,
                    "ticker": threshold.ticker,
                    "operator": threshold.operator.value,
                    "target_price": threshold.target_price
                })
            except Exception as e:
                results["thresholds"].append({
                    "string": threshold_str,
                    "parsed": False,
                    "error": str(e)
                })
        
        # Test notification system
        if self.config_manager.are_price_notifications_enabled():
            test_message = "🧪 Price Monitor Test - Configuration is working correctly!"
            notification_result = self.notification_manager.send_message(test_message)
            results["notification_test"] = {
                "success": notification_result.status.name == "SUCCESS",
                "error": notification_result.error_details if notification_result.status.name != "SUCCESS" else None
            }
        
        return results


# Global price monitor manager instance
_price_monitor_manager: Optional[PriceMonitorManager] = None


def get_price_monitor_manager() -> PriceMonitorManager:
    """
    Get the global price monitor manager instance.
    
    Returns:
        PriceMonitorManager: Global price monitor manager instance
    """
    global _price_monitor_manager
    if _price_monitor_manager is None:
        _price_monitor_manager = PriceMonitorManager()
    return _price_monitor_manager


def run_price_monitoring() -> List[ThresholdResult]:
    """
    Convenience function to run price monitoring.
    
    Returns:
        List[ThresholdResult]: Results of the monitoring check
    """
    return get_price_monitor_manager().run_monitoring_check()