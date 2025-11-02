"""
Cache manager for financial data using pickle-based storage
"""

import os
import pickle
import time
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, List
from pathlib import Path
import logging
from dataclasses import dataclass

from ...interfaces.console.logger import get_logger
from .config import CacheConfig
from .utils import CacheUtils


@dataclass
class CacheMetadata:
    """Metadata for cached items"""
    cache_key: str
    ticker: str
    data_type: str
    frequency: Optional[str]
    period: Optional[str]
    created_at: datetime
    expires_at: datetime
    file_path: str
    file_size: int


class CacheManager:
    """Manages pickle-based caching for financial data"""
    
    def __init__(self, base_cache_dir: Optional[str] = None):
        """
        Initialize cache manager
        
        Args:
            base_cache_dir: Base directory for cache storage (optional)
        """
        self.base_cache_dir = Path(base_cache_dir) if base_cache_dir else CacheConfig.get_cache_dir()
        self.cache_dir = self.base_cache_dir / "cache"
        self.metadata_dir = self.base_cache_dir / "metadata"
        self.logger = get_logger()
        
        # Create cache directories
        self._create_cache_directories()
        
        # Load cache index
        self._cache_index: Dict[str, CacheMetadata] = self._load_cache_index()
    
    def _create_cache_directories(self) -> None:
        """Create necessary cache directories"""
        directories = [self.metadata_dir]
        
        # Add data type specific directories
        for data_type in CacheConfig.get_cache_directories():
            directories.append(self.cache_dir / data_type)
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created cache directory: {directory}")
    
    def _get_cache_file_path(self, data_type: str, cache_key: str) -> Path:
        """
        Get the file path for a cache entry
        
        Args:
            data_type: Type of financial data
            cache_key: Cache key
            
        Returns:
            Path: Full path to cache file
        """
        return self.cache_dir / data_type / f"{cache_key}.pkl"
    
    def _is_cache_enabled(self, data_type: str) -> bool:
        """
        Check if caching is enabled for a data type
        
        Args:
            data_type: Type of financial data
            
        Returns:
            bool: True if caching is enabled
        """
        return CacheConfig.is_cache_enabled(data_type)
    
    def _get_ttl_hours(self, data_type: str) -> int:
        """
        Get TTL in hours for a data type
        
        Args:
            data_type: Type of financial data
            
        Returns:
            int: TTL in hours
        """
        return CacheConfig.get_ttl_hours(data_type)
    
    def _is_cache_valid(self, metadata: CacheMetadata) -> bool:
        """
        Check if a cache entry is still valid
        
        Args:
            metadata: Cache metadata
            
        Returns:
            bool: True if cache is valid
        """
        now = datetime.now()
        return now < metadata.expires_at and os.path.exists(metadata.file_path)
    
    def _load_cache_index(self) -> Dict[str, CacheMetadata]:
        """
        Load cache index from disk
        
        Returns:
            Dict[str, CacheMetadata]: Cache index
        """
        index_file = self.metadata_dir / "cache_index.pkl"
        
        if not index_file.exists():
            self.logger.debug("Cache index not found, creating new one")
            return {}
        
        try:
            with open(index_file, 'rb') as f:
                index = pickle.load(f)
            self.logger.debug(f"Loaded cache index with {len(index)} entries")
            return index
        except Exception as e:
            self.logger.warning(f"Failed to load cache index: {e}")
            return {}
    
    def _save_cache_index(self) -> None:
        """Save cache index to disk"""
        index_file = self.metadata_dir / "cache_index.pkl"
        
        try:
            with open(index_file, 'wb') as f:
                pickle.dump(self._cache_index, f)
            self.logger.debug(f"Saved cache index with {len(self._cache_index)} entries")
        except Exception as e:
            self.logger.error(f"Failed to save cache index: {e}")
    
    def get_cached_data(self, ticker: str, data_type: str, 
                       frequency: Optional[str] = None,
                       period: Optional[str] = None,
                       **kwargs) -> Optional[Any]:
        """
        Retrieve cached data if available and valid
        
        Args:
            ticker: Stock ticker symbol
            data_type: Type of financial data
            frequency: Data frequency (optional)
            period: Time period (optional)
            **kwargs: Additional parameters
            
        Returns:
            Optional[Any]: Cached data or None if not available/valid
        """
        if not self._is_cache_enabled(data_type):
            return None
        
        # Sanitize ticker for consistent cache key generation
        sanitized_ticker = CacheUtils.sanitize_ticker(ticker)
        
        # Generate cache key
        if frequency or period or kwargs:
            cache_key = CacheUtils.generate_cache_key(sanitized_ticker, data_type, frequency, period, **kwargs)
        else:
            cache_key = CacheUtils.generate_simple_cache_key(sanitized_ticker, data_type)
        
        # Check if we have metadata for this key
        if cache_key not in self._cache_index:
            self.logger.info(f"Cache miss: {cache_key}")
            return None
        
        metadata = self._cache_index[cache_key]
        
        # Check if cache is still valid
        if not self._is_cache_valid(metadata):
            self.logger.info(f"Cache expired: {cache_key}")
            self._remove_cache_entry(cache_key)
            return None
        
        # Load cached data
        try:
            with open(metadata.file_path, 'rb') as f:
                data = pickle.load(f)
            
            # Validate data structure
            if not CacheUtils.validate_cache_data(data, data_type):
                self.logger.warning(f"Invalid cached data structure for {cache_key}")
                self._remove_cache_entry(cache_key)
                return None
            
            self.logger.info(f"Cache hit: {cache_key}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load cached data for {cache_key}: {e}")
            self._remove_cache_entry(cache_key)
            return None
    
    def store_cached_data(self, data: Any, ticker: str, data_type: str,
                         frequency: Optional[str] = None,
                         period: Optional[str] = None,
                         **kwargs) -> bool:
        """
        Store data in cache
        
        Args:
            data: Data to cache
            ticker: Stock ticker symbol
            data_type: Type of financial data
            frequency: Data frequency (optional)
            period: Time period (optional)
            **kwargs: Additional parameters
            
        Returns:
            bool: True if successfully cached
        """
        if not self._is_cache_enabled(data_type):
            return False
        
        # Validate ticker
        if not CacheUtils.is_valid_ticker(ticker):
            self.logger.warning(f"Invalid ticker format: {ticker}")
            return False
        
        # Sanitize ticker for file system
        sanitized_ticker = CacheUtils.sanitize_ticker(ticker)
        
        # Generate cache key
        if frequency or period or kwargs:
            cache_key = CacheUtils.generate_cache_key(sanitized_ticker, data_type, frequency, period, **kwargs)
        else:
            cache_key = CacheUtils.generate_simple_cache_key(sanitized_ticker, data_type)
        
        file_path = self._get_cache_file_path(data_type, cache_key)
        
        try:
            # Store the data
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            # Create metadata
            now = datetime.now()
            ttl_hours = self._get_ttl_hours(data_type)
            expires_at = now + timedelta(hours=ttl_hours)
            file_size = os.path.getsize(file_path)
            
            metadata = CacheMetadata(
                cache_key=cache_key,
                ticker=sanitized_ticker.upper(),
                data_type=data_type,
                frequency=frequency,
                period=period,
                created_at=now,
                expires_at=expires_at,
                file_path=str(file_path),
                file_size=file_size
            )
            
            # Update cache index
            self._cache_index[cache_key] = metadata
            self._save_cache_index()
            
            self.logger.info(f"Cached data: {cache_key} (expires: {expires_at})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cache data for {cache_key}: {e}")
            # Clean up partial file if it exists
            if file_path.exists():
                try:
                    file_path.unlink()
                except:
                    pass
            return False
    
    def _remove_cache_entry(self, cache_key: str) -> None:
        """
        Remove a cache entry and its file
        
        Args:
            cache_key: Cache key to remove
        """
        if cache_key in self._cache_index:
            metadata = self._cache_index[cache_key]
            
            # Remove file if it exists
            try:
                if os.path.exists(metadata.file_path):
                    os.remove(metadata.file_path)
            except Exception as e:
                self.logger.warning(f"Failed to remove cache file {metadata.file_path}: {e}")
            
            # Remove from index
            del self._cache_index[cache_key]
            self._save_cache_index()
            
            self.logger.debug(f"Removed cache entry: {cache_key}")
    
    def clean_ticker_cache(self, ticker: str) -> int:
        """
        Clean all cache entries for a specific ticker
        
        Args:
            ticker: Ticker symbol to clean
            
        Returns:
            int: Number of entries removed
        """
        ticker_upper = CacheUtils.sanitize_ticker(ticker).upper()
        keys_to_remove = []
        
        for cache_key, metadata in self._cache_index.items():
            if metadata.ticker == ticker_upper:
                keys_to_remove.append(cache_key)
        
        for cache_key in keys_to_remove:
            self._remove_cache_entry(cache_key)
        
        self.logger.info(f"Cleaned {len(keys_to_remove)} cache entries for ticker {ticker_upper}")
        return len(keys_to_remove)
    
    def clean_data_type_cache(self, data_type: str) -> int:
        """
        Clean all cache entries for a specific data type
        
        Args:
            data_type: Data type to clean
            
        Returns:
            int: Number of entries removed
        """
        keys_to_remove = []
        
        for cache_key, metadata in self._cache_index.items():
            if metadata.data_type == data_type:
                keys_to_remove.append(cache_key)
        
        for cache_key in keys_to_remove:
            self._remove_cache_entry(cache_key)
        
        self.logger.info(f"Cleaned {len(keys_to_remove)} cache entries for data type {data_type}")
        return len(keys_to_remove)
    
    def clean_expired_cache(self) -> int:
        """
        Clean all expired cache entries
        
        Returns:
            int: Number of entries removed
        """
        now = datetime.now()
        keys_to_remove = []
        
        for cache_key, metadata in self._cache_index.items():
            if now >= metadata.expires_at or not os.path.exists(metadata.file_path):
                keys_to_remove.append(cache_key)
        
        for cache_key in keys_to_remove:
            self._remove_cache_entry(cache_key)
        
        self.logger.info(f"Cleaned {len(keys_to_remove)} expired cache entries")
        return len(keys_to_remove)
    
    def clean_all_cache(self) -> int:
        """
        Clean all cache entries
        
        Returns:
            int: Number of entries removed
        """
        keys_to_remove = list(self._cache_index.keys())
        
        for cache_key in keys_to_remove:
            self._remove_cache_entry(cache_key)
        
        self.logger.info(f"Cleaned all {len(keys_to_remove)} cache entries")
        return len(keys_to_remove)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        now = datetime.now()
        total_entries = len(self._cache_index)
        expired_entries = 0
        total_size = 0
        stats_by_type = {}
        
        for metadata in self._cache_index.values():
            # Count expired entries
            if now >= metadata.expires_at:
                expired_entries += 1
            
            # Calculate total size
            if os.path.exists(metadata.file_path):
                total_size += metadata.file_size
            
            # Stats by data type
            data_type = metadata.data_type
            if data_type not in stats_by_type:
                stats_by_type[data_type] = {'count': 0, 'size': 0}
            
            stats_by_type[data_type]['count'] += 1
            stats_by_type[data_type]['size'] += metadata.file_size
        
        return {
            'total_entries': total_entries,
            'valid_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'total_size_bytes': total_size,
            'total_size_formatted': CacheUtils.format_cache_size(total_size),
            'stats_by_type': stats_by_type,
            'cache_directory': str(self.cache_dir),
            'cache_enabled': any(CacheConfig.is_cache_enabled(dt) for dt in CacheConfig.get_all_data_types())
        }
    
    def list_cache_entries(self, ticker: Optional[str] = None, 
                          data_type: Optional[str] = None) -> List[CacheMetadata]:
        """
        List cache entries with optional filtering
        
        Args:
            ticker: Filter by ticker (optional)
            data_type: Filter by data type (optional)
            
        Returns:
            List[CacheMetadata]: List of cache entries
        """
        entries = []
        
        for metadata in self._cache_index.values():
            # Apply filters
            if ticker and metadata.ticker != CacheUtils.sanitize_ticker(ticker).upper():
                continue
            if data_type and metadata.data_type != data_type:
                continue
            
            entries.append(metadata)
        
        # Sort by creation date (newest first)
        entries.sort(key=lambda x: x.created_at, reverse=True)
        return entries


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """
    Get the global cache manager instance
    
    Returns:
        CacheManager: Global cache manager
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager