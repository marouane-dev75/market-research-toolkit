"""
Data Frequency Enumeration

This module defines the data frequency options used across financial fetchers.
"""

from enum import Enum


class DataFrequency(Enum):
    """Enumeration for data frequency options."""
    YEARLY = "yearly"
    QUARTERLY = "quarterly"