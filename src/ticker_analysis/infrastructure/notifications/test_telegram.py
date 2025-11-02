#!/usr/bin/env python3
"""
Telegram Notification Test

This test file demonstrates how to use the notifier module to send
a simple "hello" message via Telegram.

Before running this test:
1. Update config/config.yml with your bot token and chat ID
2. Set telegram.enabled to true in the config
3. Run: python -m notifier.test_telegram
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ticker_analysis.infrastructure.notifications.manager import (
    send_notification, 
    get_notification_manager, 
    ProviderType,
    NotificationStatus
)
from src.ticker_analysis.interfaces.console.logger import get_logger


def test_simple_notification():
    """Test sending a simple notification using the convenience function."""
    logger = get_logger(__name__)
    
    logger.info("Testing simple notification...")
    
    # Send a simple "hello" message
    result = send_notification("Hello from ticker analysis tool! 🚀")
    
    if result.status == NotificationStatus.SUCCESS:
        logger.info("✅ Simple notification sent successfully!")
        logger.info(f"Message: {result.message}")
    else:
        logger.error("❌ Failed to send simple notification")
        logger.error(f"Error: {result.error_details}")
    
    return result.status == NotificationStatus.SUCCESS


def test_telegram_specific():
    """Test sending a message specifically via Telegram provider."""
    logger = get_logger(__name__)
    
    logger.info("Testing Telegram-specific notification...")
    
    manager = get_notification_manager()
    
    # Send message with Telegram-specific formatting
    message = f"""
🎯 *Ticker Analysis Notification Test*

Hello from the ticker analysis tool!

This is a test message to verify that Telegram notifications are working correctly.

Features:
• ✅ Configuration loaded
• ✅ Provider initialized
• ✅ Message sent successfully

_Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
    """.strip()
    
    result = manager.send_message(
        message, 
        ProviderType.TELEGRAM,
        parse_mode='Markdown'
    )
    
    if result.status == NotificationStatus.SUCCESS:
        logger.info("✅ Telegram-specific notification sent successfully!")
        logger.info(f"Message: {result.message}")
    else:
        logger.error("❌ Failed to send Telegram-specific notification")
        logger.error(f"Error: {result.error_details}")
    
    return result.status == NotificationStatus.SUCCESS


def test_provider_status():
    """Test and display provider status information."""
    logger = get_logger(__name__)
    
    logger.info("Checking provider status...")
    
    manager = get_notification_manager()
    
    # Get provider status
    status = manager.get_provider_status()
    
    logger.info("Provider Status:")
    for provider_name, info in status.items():
        status_icon = "✅" if info['configured'] else "❌"
        logger.info(f"  {status_icon} {info['name']}: {'Configured' if info['configured'] else 'Not configured'}")
    
    # Test connections
    logger.info("Testing provider connections...")
    test_results = manager.test_providers()
    
    for provider_name, result in test_results.items():
        if result.status == NotificationStatus.SUCCESS:
            logger.info(f"  ✅ {provider_name}: {result.message}")
        else:
            logger.error(f"  ❌ {provider_name}: {result.error_details}")
    
    return any(result.status == NotificationStatus.SUCCESS for result in test_results.values())


def main():
    """Main test function."""
    logger = get_logger(__name__)
    
    logger.info("=" * 60)
    logger.info("🚀 TELEGRAM NOTIFICATION TEST")
    logger.info("=" * 60)
    
    # Check if any providers are configured
    manager = get_notification_manager()
    if not manager.is_any_provider_configured():
        logger.error("❌ No notification providers are configured!")
        logger.error("Please update config/config.yml with your Telegram bot token and chat ID")
        logger.error("Set telegram.enabled to true in the configuration")
        return False
    
    # Run tests
    tests = [
        ("Provider Status Check", test_provider_status),
        ("Simple Notification", test_simple_notification),
        ("Telegram Specific", test_telegram_specific)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        logger.info("-" * 40)
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
    
    logger.info(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Telegram notifications are working correctly.")
        return True
    else:
        logger.error("⚠️  Some tests failed. Please check your configuration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)