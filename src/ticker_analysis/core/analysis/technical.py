"""
Technical Analysis Module

This module provides functionality to calculate technical indicators and generate
trading signals and scores based on technical analysis.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np
from ..data.fetchers.price import PriceData


class TechnicalSignal(Enum):
    """Enumeration for technical analysis signals."""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"


@dataclass
class MACDData:
    """MACD indicator data."""
    macd_line: Optional[float] = None
    signal_line: Optional[float] = None
    histogram: Optional[float] = None
    signal: Optional[TechnicalSignal] = None
    score: Optional[float] = None  # 0-10 scale


@dataclass
class RSIData:
    """RSI indicator data."""
    rsi_value: Optional[float] = None
    signal: Optional[TechnicalSignal] = None
    score: Optional[float] = None  # 0-10 scale
    is_overbought: bool = False  # RSI > 70
    is_oversold: bool = False    # RSI < 30


@dataclass
class MovingAveragesData:
    """Moving averages data."""
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    current_price: Optional[float] = None
    signal: Optional[TechnicalSignal] = None
    score: Optional[float] = None  # 0-10 scale
    trend_strength: Optional[str] = None  # "Strong Uptrend", "Uptrend", "Sideways", "Downtrend", "Strong Downtrend"


@dataclass
class BollingerBandsData:
    """Bollinger Bands data."""
    upper_band: Optional[float] = None
    middle_band: Optional[float] = None  # 20-period SMA
    lower_band: Optional[float] = None
    current_price: Optional[float] = None
    bandwidth: Optional[float] = None
    percent_b: Optional[float] = None  # Position within bands
    signal: Optional[TechnicalSignal] = None
    score: Optional[float] = None  # 0-10 scale
    squeeze: bool = False  # Low volatility indicator


@dataclass
class TechnicalIndicators:
    """
    Comprehensive technical indicators data.
    """
    
    # Basic Information
    ticker: str
    analysis_date: str
    data_points: int  # Number of price data points used
    
    # Individual Indicators
    macd: Optional[MACDData] = None
    rsi: Optional[RSIData] = None
    moving_averages: Optional[MovingAveragesData] = None
    bollinger_bands: Optional[BollingerBandsData] = None
    
    # Overall Analysis
    overall_signal: Optional[TechnicalSignal] = None
    overall_score: Optional[float] = None  # 0-10 scale
    confidence_level: Optional[float] = None  # 0-100%
    
    # Summary
    bullish_indicators: int = 0
    bearish_indicators: int = 0
    neutral_indicators: int = 0


class TechnicalAnalyzer:
    """
    Technical analysis calculator for various indicators.
    
    This class processes historical price data to calculate technical indicators
    and generate trading signals and scores.
    """
    
    def __init__(self):
        """Initialize the technical analyzer."""
        pass
    
    def analyze_technical_indicators(
        self,
        ticker: str,
        price_data_list: List[PriceData]
    ) -> Optional[TechnicalIndicators]:
        """
        Analyze technical indicators for the given price data.
        
        Args:
            ticker: Stock ticker symbol
            price_data_list: List of PriceData objects (should have at least 200 data points for accurate analysis)
            
        Returns:
            TechnicalIndicators object with calculated metrics, or None if insufficient data
        """
        if not price_data_list or len(price_data_list) < 20:
            return None
        
        # Convert to pandas DataFrame for easier calculation
        df = self._convert_to_dataframe(price_data_list)
        
        if df is None or len(df) < 20:
            return None
        
        # Calculate individual indicators
        macd_data = self._calculate_macd(df)
        rsi_data = self._calculate_rsi(df)
        ma_data = self._calculate_moving_averages(df)
        bb_data = self._calculate_bollinger_bands(df)
        
        # Calculate overall score and signal
        overall_score, overall_signal, confidence = self._calculate_overall_score(
            macd_data, rsi_data, ma_data, bb_data
        )
        
        # Count indicator signals
        bullish, bearish, neutral = self._count_signals(macd_data, rsi_data, ma_data, bb_data)
        
        return TechnicalIndicators(
            ticker=ticker,
            analysis_date=datetime.now().strftime("%Y-%m-%d"),
            data_points=len(df),
            macd=macd_data,
            rsi=rsi_data,
            moving_averages=ma_data,
            bollinger_bands=bb_data,
            overall_signal=overall_signal,
            overall_score=overall_score,
            confidence_level=confidence,
            bullish_indicators=bullish,
            bearish_indicators=bearish,
            neutral_indicators=neutral
        )
    
    def _convert_to_dataframe(self, price_data_list: List[PriceData]) -> Optional[pd.DataFrame]:
        """Convert PriceData list to pandas DataFrame."""
        try:
            data = []
            for price_data in price_data_list:
                if price_data.close_price is not None:
                    data.append({
                        'date': price_data.date,
                        'open': price_data.open_price,
                        'high': price_data.high_price,
                        'low': price_data.low_price,
                        'close': price_data.close_price,
                        'volume': price_data.volume or 0
                    })
            
            if not data:
                return None
            
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            return df
            
        except Exception:
            return None
    
    def _calculate_macd(self, df: pd.DataFrame) -> Optional[MACDData]:
        """Calculate MACD indicator."""
        try:
            if len(df) < 26:
                return None
            
            # Calculate EMAs
            ema_12 = df['close'].ewm(span=12).mean()
            ema_26 = df['close'].ewm(span=26).mean()
            
            # Calculate MACD line
            macd_line = ema_12 - ema_26
            
            # Calculate signal line (9-period EMA of MACD)
            signal_line = macd_line.ewm(span=9).mean()
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            # Get latest values
            latest_macd = macd_line.iloc[-1]
            latest_signal = signal_line.iloc[-1]
            latest_histogram = histogram.iloc[-1]
            
            # Determine signal and score
            signal, score = self._evaluate_macd_signal(latest_macd, latest_signal, latest_histogram)
            
            return MACDData(
                macd_line=latest_macd,
                signal_line=latest_signal,
                histogram=latest_histogram,
                signal=signal,
                score=score
            )
            
        except Exception:
            return None
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Optional[RSIData]:
        """Calculate RSI indicator."""
        try:
            if len(df) < period + 1:
                return None
            
            # Calculate price changes
            delta = df['close'].diff()
            
            # Separate gains and losses
            gains = delta.where(delta > 0, 0)
            losses = -delta.where(delta < 0, 0)
            
            # Calculate average gains and losses
            avg_gains = gains.rolling(window=period).mean()
            avg_losses = losses.rolling(window=period).mean()
            
            # Calculate RS and RSI
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            
            # Get latest RSI value
            latest_rsi = rsi.iloc[-1]
            
            # Determine signal and score
            signal, score = self._evaluate_rsi_signal(latest_rsi)
            
            return RSIData(
                rsi_value=latest_rsi,
                signal=signal,
                score=score,
                is_overbought=latest_rsi > 70,
                is_oversold=latest_rsi < 30
            )
            
        except Exception:
            return None
    
    def _calculate_moving_averages(self, df: pd.DataFrame) -> Optional[MovingAveragesData]:
        """Calculate moving averages."""
        try:
            current_price = df['close'].iloc[-1]
            
            # Calculate SMAs
            sma_20 = df['close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
            sma_50 = df['close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else None
            sma_200 = df['close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None
            
            # Calculate EMAs
            ema_12 = df['close'].ewm(span=12).mean().iloc[-1] if len(df) >= 12 else None
            ema_26 = df['close'].ewm(span=26).mean().iloc[-1] if len(df) >= 26 else None
            
            # Determine signal and score
            signal, score, trend_strength = self._evaluate_ma_signal(
                current_price, sma_20, sma_50, sma_200, ema_12, ema_26
            )
            
            return MovingAveragesData(
                sma_20=sma_20,
                sma_50=sma_50,
                sma_200=sma_200,
                ema_12=ema_12,
                ema_26=ema_26,
                current_price=current_price,
                signal=signal,
                score=score,
                trend_strength=trend_strength
            )
            
        except Exception:
            return None
    
    def _calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> Optional[BollingerBandsData]:
        """Calculate Bollinger Bands."""
        try:
            if len(df) < period:
                return None
            
            # Calculate middle band (SMA)
            middle_band = df['close'].rolling(window=period).mean()
            
            # Calculate standard deviation
            std = df['close'].rolling(window=period).std()
            
            # Calculate upper and lower bands
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            # Get latest values
            current_price = df['close'].iloc[-1]
            latest_upper = upper_band.iloc[-1]
            latest_middle = middle_band.iloc[-1]
            latest_lower = lower_band.iloc[-1]
            
            # Calculate bandwidth and %B
            bandwidth = (latest_upper - latest_lower) / latest_middle * 100
            percent_b = (current_price - latest_lower) / (latest_upper - latest_lower) * 100
            
            # Check for squeeze (low volatility)
            squeeze = bandwidth < 10  # Arbitrary threshold for squeeze
            
            # Determine signal and score
            signal, score = self._evaluate_bb_signal(current_price, latest_upper, latest_lower, percent_b)
            
            return BollingerBandsData(
                upper_band=latest_upper,
                middle_band=latest_middle,
                lower_band=latest_lower,
                current_price=current_price,
                bandwidth=bandwidth,
                percent_b=percent_b,
                signal=signal,
                score=score,
                squeeze=squeeze
            )
            
        except Exception:
            return None
    
    def _evaluate_macd_signal(self, macd: float, signal: float, histogram: float) -> Tuple[TechnicalSignal, float]:
        """Evaluate MACD signal and score."""
        score = 5.0  # Start neutral
        
        # MACD line above/below signal line
        if macd > signal:
            if histogram > 0:  # Increasing momentum
                score += 2
                signal_type = TechnicalSignal.BUY
            else:
                score += 1
                signal_type = TechnicalSignal.HOLD
        else:
            if histogram < 0:  # Decreasing momentum
                score -= 2
                signal_type = TechnicalSignal.SELL
            else:
                score -= 1
                signal_type = TechnicalSignal.HOLD
        
        # MACD line above/below zero
        if macd > 0:
            score += 0.5
        else:
            score -= 0.5
        
        # Clamp score between 0 and 10
        score = max(0, min(10, score))
        
        # Determine final signal based on score
        if score >= 8:
            signal_type = TechnicalSignal.STRONG_BUY
        elif score >= 6:
            signal_type = TechnicalSignal.BUY
        elif score >= 4:
            signal_type = TechnicalSignal.HOLD
        elif score >= 2:
            signal_type = TechnicalSignal.SELL
        else:
            signal_type = TechnicalSignal.STRONG_SELL
        
        return signal_type, score
    
    def _evaluate_rsi_signal(self, rsi: float) -> Tuple[TechnicalSignal, float]:
        """Evaluate RSI signal and score."""
        if rsi >= 70:
            # Overbought
            score = 2.0
            signal_type = TechnicalSignal.SELL
        elif rsi >= 60:
            score = 4.0
            signal_type = TechnicalSignal.HOLD
        elif rsi >= 40:
            score = 5.0
            signal_type = TechnicalSignal.HOLD
        elif rsi >= 30:
            score = 6.0
            signal_type = TechnicalSignal.HOLD
        else:
            # Oversold
            score = 8.0
            signal_type = TechnicalSignal.BUY
        
        return signal_type, score
    
    def _evaluate_ma_signal(self, price: float, sma_20: Optional[float], sma_50: Optional[float], 
                           sma_200: Optional[float], ema_12: Optional[float], ema_26: Optional[float]) -> Tuple[TechnicalSignal, float, str]:
        """Evaluate moving averages signal and score."""
        score = 5.0  # Start neutral
        bullish_signals = 0
        bearish_signals = 0
        
        # Price vs SMAs
        if sma_20 is not None:
            if price > sma_20:
                bullish_signals += 1
                score += 0.5
            else:
                bearish_signals += 1
                score -= 0.5
        
        if sma_50 is not None:
            if price > sma_50:
                bullish_signals += 1
                score += 0.5
            else:
                bearish_signals += 1
                score -= 0.5
        
        if sma_200 is not None:
            if price > sma_200:
                bullish_signals += 2  # Long-term trend is more important
                score += 1.0
            else:
                bearish_signals += 2
                score -= 1.0
        
        # EMA crossover
        if ema_12 is not None and ema_26 is not None:
            if ema_12 > ema_26:
                bullish_signals += 1
                score += 0.5
            else:
                bearish_signals += 1
                score -= 0.5
        
        # SMA alignment
        if sma_20 is not None and sma_50 is not None and sma_200 is not None:
            if sma_20 > sma_50 > sma_200:
                bullish_signals += 1
                score += 1.0
            elif sma_20 < sma_50 < sma_200:
                bearish_signals += 1
                score -= 1.0
        
        # Clamp score
        score = max(0, min(10, score))
        
        # Determine signal
        if score >= 8:
            signal_type = TechnicalSignal.STRONG_BUY
            trend_strength = "Strong Uptrend"
        elif score >= 6:
            signal_type = TechnicalSignal.BUY
            trend_strength = "Uptrend"
        elif score >= 4:
            signal_type = TechnicalSignal.HOLD
            trend_strength = "Sideways"
        elif score >= 2:
            signal_type = TechnicalSignal.SELL
            trend_strength = "Downtrend"
        else:
            signal_type = TechnicalSignal.STRONG_SELL
            trend_strength = "Strong Downtrend"
        
        return signal_type, score, trend_strength
    
    def _evaluate_bb_signal(self, price: float, upper: float, lower: float, percent_b: float) -> Tuple[TechnicalSignal, float]:
        """Evaluate Bollinger Bands signal and score."""
        score = 5.0  # Start neutral
        
        if percent_b >= 100:
            # Price above upper band - overbought
            score = 2.0
            signal_type = TechnicalSignal.SELL
        elif percent_b >= 80:
            score = 3.0
            signal_type = TechnicalSignal.HOLD
        elif percent_b >= 20:
            score = 5.0
            signal_type = TechnicalSignal.HOLD
        elif percent_b >= 0:
            score = 7.0
            signal_type = TechnicalSignal.HOLD
        else:
            # Price below lower band - oversold
            score = 8.0
            signal_type = TechnicalSignal.BUY
        
        return signal_type, score
    
    def _calculate_overall_score(self, macd: Optional[MACDData], rsi: Optional[RSIData], 
                                ma: Optional[MovingAveragesData], bb: Optional[BollingerBandsData]) -> Tuple[float, TechnicalSignal, float]:
        """Calculate overall technical analysis score."""
        scores = []
        weights = []
        
        # Collect scores with weights
        if macd and macd.score is not None:
            scores.append(macd.score)
            weights.append(0.3)  # 30% weight
        
        if rsi and rsi.score is not None:
            scores.append(rsi.score)
            weights.append(0.2)  # 20% weight
        
        if ma and ma.score is not None:
            scores.append(ma.score)
            weights.append(0.35)  # 35% weight (most important)
        
        if bb and bb.score is not None:
            scores.append(bb.score)
            weights.append(0.15)  # 15% weight
        
        if not scores:
            return 5.0, TechnicalSignal.HOLD, 0.0
        
        # Calculate weighted average
        weighted_score = sum(score * weight for score, weight in zip(scores, weights)) / sum(weights)
        
        # Calculate confidence based on number of indicators
        confidence = (len(scores) / 4) * 100  # 4 is max number of indicators
        
        # Determine overall signal
        if weighted_score >= 8:
            signal = TechnicalSignal.STRONG_BUY
        elif weighted_score >= 6:
            signal = TechnicalSignal.BUY
        elif weighted_score >= 4:
            signal = TechnicalSignal.HOLD
        elif weighted_score >= 2:
            signal = TechnicalSignal.SELL
        else:
            signal = TechnicalSignal.STRONG_SELL
        
        return weighted_score, signal, confidence
    
    def _count_signals(self, macd: Optional[MACDData], rsi: Optional[RSIData], 
                      ma: Optional[MovingAveragesData], bb: Optional[BollingerBandsData]) -> Tuple[int, int, int]:
        """Count bullish, bearish, and neutral signals."""
        bullish = 0
        bearish = 0
        neutral = 0
        
        indicators = [macd, rsi, ma, bb]
        
        for indicator in indicators:
            if indicator and indicator.signal:
                if indicator.signal in [TechnicalSignal.STRONG_BUY, TechnicalSignal.BUY]:
                    bullish += 1
                elif indicator.signal in [TechnicalSignal.STRONG_SELL, TechnicalSignal.SELL]:
                    bearish += 1
                else:
                    neutral += 1
        
        return bullish, bearish, neutral