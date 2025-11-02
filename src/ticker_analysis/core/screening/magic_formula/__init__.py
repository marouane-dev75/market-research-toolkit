"""Magic Formula screening package."""

from .fetcher import MagicFormulaFetcher
from .display import display_magic_formula_results

__all__ = [
    'MagicFormulaFetcher',
    'display_magic_formula_results'
]