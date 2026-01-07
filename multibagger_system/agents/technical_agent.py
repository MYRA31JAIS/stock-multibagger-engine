"""
Technical & Market Structure Agent - Analyzes technical patterns and market structure
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import yfinance as yf

logger = logging.getLogger(__name__)

class TechnicalAgent:
    def __init__(self):
        self.name = "Technical & Market Structure Agent"
        self.version = "1.0"
        
    def analyze(self, financial_data: Dict, technical_data: Dict) -> Dict:
        """
        Analyze technical patterns and market structure
        Focus on confirming if market agrees with fundamentals
        """
        try:
            logger.info(f"Technical analysis starting for {financial_data.get('symbol', 'Unknown')}")
            
            symbol = financial_data.get('symbol', 'Unknown')
            
            # Get additional price data for comprehensive analysis
            extended_price_data = self._get_extended_price_data(symbol)
            
            # Analyze different technical aspects
            base_formation_analysis = self._analyze_base_formation(extended_price_data)
            breakout_analysis = self._analyze_breakout_patterns(extended_price_data, technical_data)
            relative_strength_analysis = self._analyze_relative_strength(extended_price_data)
            volume_analysis = self._analyze_volume_patterns(extended_price_data)
            trend_analysis = self._analyze_trend_change(extended_price_data, technical_data)
            
            # Determine technical stage
            technical_stage = self._determine_technical_stage(
                base_formation_analysis, breakout_analysis, extended_price_data
            )
            
            # Calculate risk-reward ratio
            risk_reward_ratio = self._calculate_risk_reward(
                extended_price_data, technical_data, breakout_analysis
            )
            
            logger.info(f"Technical analysis completed. Stage: {technical_stage}")
            
            return {
                "technical_stage": technical_stage,
                "risk_reward_ratio": risk_reward_ratio,
                "detailed_analysis": {
                    "base_formation_months": base_formation_analysis.get('base_duration_months', 0),
                    "breakout_confirmed": breakout_analysis.get('breakout_confirmed', False),
                    "relative_strength_vs_nifty": relative_strength_analysis.get('rs_ratio', 0),
                    "volume_expansion": volume_analysis.get('volume_expansion', False),
                    "trend_direction": trend_analysis.get('trend_direction', 'SIDEWAYS'),
                    "support_level": technical_data.get('support_level', 0),
                    "resistance_level": breakout_analysis.get('resistance_level', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return self._create_default_response(f"Analysis error: {str(e)}")
    
    def _get_extended_price_data(self, symbol: str) -> pd.DataFrame:
        """Get extended price data for comprehensive analysis"""
        try:
            stock = yf.Ticker(symbol)
            hist_data = stock.history(period="5y", interval="1d")
            
            if hist_data.empty:
                return pd.DataFrame()
            
            # Calculate additional technical indicators
            hist_data['SMA_20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['SMA_50'] = hist_data['Close'].rolling(window=50).mean()
            hist_data['SMA_200'] = hist_data['Close'].rolling(window=200).mean()
            
            # Calculate Bollinger Bands
            hist_data['BB_Middle'] = hist_data['Close'].rolling(window=20).mean()
            bb_std = hist_data['Close'].rolling(window=20).std()
            hist_data['BB_Upper'] = hist_data['BB_Middle'] + (bb_std * 2)
            hist_data['BB_Lower'] = hist_data['BB_Middle'] - (bb_std * 2)
            
            # Calculate RSI
            hist_data['RSI'] = self._calculate_rsi(hist_data['Close'])
            
            # Calculate MACD
            macd_data = self._calculate_macd(hist_data['Close'])
            hist_data['MACD'] = macd_data['MACD']
            hist_data['MACD_Signal'] = macd_data['Signal']
            
            return hist_data
            
        except Exception as e:
            logger.error(f"Error getting extended price data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _analyze_base_formation(self, price_data: pd.DataFrame) -> Dict:
        """Analyze base formation patterns (3-5 year consolidation)"""
        try:
            if price_data.empty or len(price_data) < 252:  # Less than 1 year data
                return {'base_duration_months': 0, 'base_quality': 'POOR'}
            
            # Look for consolidation periods
            high_prices = price_data['High'].rolling(window=252).max()  # 1-year rolling high
            low_prices = price_data['Low'].rolling(window=252).min()   # 1-year rolling low
            
            # Calculate price range compression
            price_ranges = (high_prices - low_prices) / low_prices * 100
            
            # Find periods of tight consolidation (< 30% range)
            consolidation_periods = price_ranges < 30
            
            # Count consecutive consolidation months
            base_duration_months = 0
            current_streak = 0
            max_streak = 0
            
            for is_consolidating in consolidation_periods:
                if is_consolidating:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    current_streak = 0
            
            base_duration_months = max_streak / 21  # Convert days to months (approx)
            
            # Determine base quality
            if base_duration_months >= 36:  # 3+ years
                base_quality = 'EXCELLENT'
            elif base_duration_months >= 24:  # 2+ years
                base_quality = 'GOOD'
            elif base_duration_months >= 12:  # 1+ year
                base_quality = 'FAIR'
            else:
                base_quality = 'POOR'
            
            return {
                'base_duration_months': base_duration_months,
                'base_quality': base_quality,
                'consolidation_range': price_ranges.iloc[-1] if not price_ranges.empty else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing base formation: {e}")
            return {'base_duration_months': 0, 'base_quality': 'POOR'}
    
    def _analyze_breakout_patterns(self, price_data: pd.DataFrame, technical_data: Dict) -> Dict:
        """Analyze breakout patterns and confirmation"""
        try:
            if price_data.empty:
                return {'breakout_confirmed': False, 'breakout_strength': 'WEAK'}
            
            current_price = technical_data.get('current_price', 0)
            if current_price == 0:
                current_price = price_data['Close'].iloc[-1]
            
            # Calculate resistance levels (52-week high, previous peaks)
            resistance_52w = price_data['High'].tail(252).max()
            resistance_level = resistance_52w
            
            # Check for breakout
            breakout_confirmed = current_price > resistance_level * 1.02  # 2% above resistance
            
            # Analyze breakout strength
            if breakout_confirmed:
                breakout_percentage = ((current_price - resistance_level) / resistance_level) * 100
                
                if breakout_percentage > 10:
                    breakout_strength = 'STRONG'
                elif breakout_percentage > 5:
                    breakout_strength = 'MODERATE'
                else:
                    breakout_strength = 'WEAK'
            else:
                breakout_strength = 'NO_BREAKOUT'
            
            # Check for false breakouts (price falling back below resistance)
            recent_prices = price_data['Close'].tail(10)
            false_breakout = breakout_confirmed and any(price < resistance_level * 0.98 for price in recent_prices)
            
            return {
                'breakout_confirmed': breakout_confirmed and not false_breakout,
                'breakout_strength': breakout_strength,
                'resistance_level': resistance_level,
                'false_breakout': false_breakout
            }
            
        except Exception as e:
            logger.error(f"Error analyzing breakout patterns: {e}")
            return {'breakout_confirmed': False, 'breakout_strength': 'WEAK'}
    
    def _analyze_relative_strength(self, price_data: pd.DataFrame) -> Dict:
        """Analyze relative strength vs NIFTY"""
        try:
            if price_data.empty:
                return {'rs_ratio': 0, 'outperforming_nifty': False}
            
            # Get NIFTY data for comparison
            nifty = yf.Ticker("^NSEI")
            nifty_data = nifty.history(period="1y")
            
            if nifty_data.empty:
                return {'rs_ratio': 0, 'outperforming_nifty': False}
            
            # Calculate 1-year returns
            stock_return_1y = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[-252]) / 
                              price_data['Close'].iloc[-252]) * 100
            
            nifty_return_1y = ((nifty_data['Close'].iloc[-1] - nifty_data['Close'].iloc[-252]) / 
                              nifty_data['Close'].iloc[-252]) * 100
            
            # Calculate relative strength ratio
            rs_ratio = stock_return_1y - nifty_return_1y
            outperforming_nifty = rs_ratio > 0
            
            return {
                'rs_ratio': rs_ratio,
                'outperforming_nifty': outperforming_nifty,
                'stock_return_1y': stock_return_1y,
                'nifty_return_1y': nifty_return_1y
            }
            
        except Exception as e:
            logger.error(f"Error analyzing relative strength: {e}")
            return {'rs_ratio': 0, 'outperforming_nifty': False}
    
    def _analyze_volume_patterns(self, price_data: pd.DataFrame) -> Dict:
        """Analyze volume expansion patterns"""
        try:
            if price_data.empty or 'Volume' not in price_data.columns:
                return {'volume_expansion': False, 'volume_trend': 'FLAT'}
            
            # Calculate average volumes
            avg_volume_3m = price_data['Volume'].tail(63).mean()  # 3 months
            avg_volume_1y = price_data['Volume'].tail(252).mean()  # 1 year
            
            # Check for volume expansion
            volume_expansion = avg_volume_3m > avg_volume_1y * 1.5  # 50% increase
            
            # Analyze recent volume trend
            recent_volumes = price_data['Volume'].tail(21)  # Last 21 days
            older_volumes = price_data['Volume'].tail(42).head(21)  # Previous 21 days
            
            if recent_volumes.mean() > older_volumes.mean() * 1.2:
                volume_trend = 'INCREASING'
            elif recent_volumes.mean() < older_volumes.mean() * 0.8:
                volume_trend = 'DECREASING'
            else:
                volume_trend = 'FLAT'
            
            return {
                'volume_expansion': volume_expansion,
                'volume_trend': volume_trend,
                'avg_volume_3m': avg_volume_3m,
                'avg_volume_1y': avg_volume_1y
            }
            
        except Exception as e:
            logger.error(f"Error analyzing volume patterns: {e}")
            return {'volume_expansion': False, 'volume_trend': 'FLAT'}
    
    def _analyze_trend_change(self, price_data: pd.DataFrame, technical_data: Dict) -> Dict:
        """Analyze trend change validation"""
        try:
            if price_data.empty:
                return {'trend_direction': 'SIDEWAYS', 'trend_strength': 'WEAK'}
            
            current_price = technical_data.get('current_price', price_data['Close'].iloc[-1])
            sma_50 = technical_data.get('sma_50', price_data['SMA_50'].iloc[-1])
            sma_200 = technical_data.get('sma_200', price_data['SMA_200'].iloc[-1])
            
            # Determine trend direction
            if current_price > sma_50 > sma_200:
                trend_direction = 'UPTREND'
            elif current_price < sma_50 < sma_200:
                trend_direction = 'DOWNTREND'
            else:
                trend_direction = 'SIDEWAYS'
            
            # Calculate trend strength using ADX-like logic
            price_changes = price_data['Close'].diff().abs()
            trend_strength_value = price_changes.tail(14).mean()
            
            if trend_strength_value > price_data['Close'].iloc[-1] * 0.02:  # 2% average daily move
                trend_strength = 'STRONG'
            elif trend_strength_value > price_data['Close'].iloc[-1] * 0.01:  # 1% average daily move
                trend_strength = 'MODERATE'
            else:
                trend_strength = 'WEAK'
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'price_vs_sma50': ((current_price - sma_50) / sma_50) * 100,
                'price_vs_sma200': ((current_price - sma_200) / sma_200) * 100
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trend change: {e}")
            return {'trend_direction': 'SIDEWAYS', 'trend_strength': 'WEAK'}
    
    def _determine_technical_stage(self, base_analysis: Dict, breakout_analysis: Dict, 
                                 price_data: pd.DataFrame) -> str:
        """Determine the current technical stage"""
        
        base_quality = base_analysis.get('base_quality', 'POOR')
        breakout_confirmed = breakout_analysis.get('breakout_confirmed', False)
        
        if breakout_confirmed and base_quality in ['GOOD', 'EXCELLENT']:
            # Check if price has extended too much
            if not price_data.empty:
                current_price = price_data['Close'].iloc[-1]
                resistance_level = breakout_analysis.get('resistance_level', current_price)
                extension = ((current_price - resistance_level) / resistance_level) * 100
                
                if extension > 50:  # More than 50% above breakout
                    return "EXTENDED"
                else:
                    return "BREAKOUT"
            else:
                return "BREAKOUT"
        elif base_quality in ['GOOD', 'EXCELLENT']:
            return "BASE"
        else:
            return "BASE"  # Default to base formation stage
    
    def _calculate_risk_reward(self, price_data: pd.DataFrame, technical_data: Dict, 
                             breakout_analysis: Dict) -> str:
        """Calculate risk-reward ratio"""
        try:
            if price_data.empty:
                return "1:1"
            
            current_price = technical_data.get('current_price', price_data['Close'].iloc[-1])
            support_level = technical_data.get('support_level', price_data['Low'].tail(252).min())
            resistance_level = breakout_analysis.get('resistance_level', price_data['High'].tail(252).max())
            
            # Calculate risk (current price to support)
            risk = current_price - support_level
            
            # Calculate reward (resistance + 20% to current price)
            target_price = resistance_level * 1.2  # 20% above resistance
            reward = target_price - current_price
            
            if risk <= 0:
                return "1:1"
            
            risk_reward_ratio = reward / risk
            
            if risk_reward_ratio >= 3:
                return "1:3+"
            elif risk_reward_ratio >= 2:
                return "1:2"
            elif risk_reward_ratio >= 1.5:
                return "1:1.5"
            else:
                return "1:1"
                
        except Exception as e:
            logger.error(f"Error calculating risk-reward: {e}")
            return "1:1"
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD indicator"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        
        return {
            'MACD': macd,
            'Signal': macd_signal,
            'Histogram': macd - macd_signal
        }
    
    def _create_default_response(self, reason: str) -> Dict:
        """Create default response for error cases"""
        return {
            "technical_stage": "BASE",
            "risk_reward_ratio": "1:1",
            "detailed_analysis": {"error": reason}
        }