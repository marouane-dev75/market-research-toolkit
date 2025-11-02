"""Ticker Analysis Tool - A comprehensive financial analysis application."""

__version__ = "1.0.0"
__author__ = "Your Name"

# Core exports
from .core import CompanyAnalysisData, DataFrequency, fetchers, display_comprehensive_analysis

# Configuration
from .config import get_config_manager

# Infrastructure
from .infrastructure import cache

# Main interface (imported last to avoid circular imports)
from .interfaces.cli import main

__all__ = [
    # Core data and analysis
    "CompanyAnalysisData",
    "DataFrequency",
    "fetchers",
    "display_comprehensive_analysis",
    
    # Main interface
    "main",
    
    # Configuration
    "get_config_manager",
    
    # Infrastructure
    "cache"
]