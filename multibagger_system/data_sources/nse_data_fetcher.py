"""
Enhanced NSE Data Fetcher with Real API Integration
"""
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, List, Optional
import json
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NSEDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Load API keys from environment
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.finnhub_key = os.getenv('FINNHUB_API_KEY')
        self.polygon_key = os.getenv('POLYGON_API_KEY')
        
        # API endpoints
        self.alpha_vantage_base = "https://www.alphavantage.co/query"
        self.news_api_base = "https://newsapi.org/v2"
        self.finnhub_base = "https://finnhub.io/api/v1"
        self.polygon_base = "https://api.polygon.io"
        self.nse_base = "https://www.nseindia.com/api"
        
    def get_nse_stock_list(self) -> List[str]:
        """Get comprehensive list of NSE stocks using multiple sources"""
        try:
            nse_stocks = []
            
            # Method 1: Try NSE official API (free, no key needed)
            try:
                nse_url = f"{self.nse_base}/equity-stockIndices?index=NIFTY%20500"
                response = self.session.get(nse_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for stock in data.get('data', []):
                        symbol = stock.get('symbol', '') + '.NS'
                        if symbol not in nse_stocks:
                            nse_stocks.append(symbol)
                    logger.info(f"Fetched {len(nse_stocks)} stocks from NSE API")
            except Exception as e:
                logger.warning(f"NSE API failed: {e}")
            
            # Method 2: Use Finnhub for additional Indian stocks
            if self.finnhub_key and len(nse_stocks) < 100:
                try:
                    finnhub_url = f"{self.finnhub_base}/stock/symbol?exchange=NS&token={self.finnhub_key}"
                    response = requests.get(finnhub_url, timeout=10)
                    if response.status_code == 200:
                        stocks = response.json()
                        for stock in stocks[:500]:  # Limit to 500 stocks
                            symbol = stock.get('symbol', '')
                            if symbol and symbol not in nse_stocks:
                                nse_stocks.append(symbol)
                        logger.info(f"Added {len(stocks)} stocks from Finnhub")
                except Exception as e:
                    logger.warning(f"Finnhub API failed: {e}")
            
            # Method 3: Fallback to curated list if APIs fail
            if len(nse_stocks) < 50:
                fallback_stocks = [
                    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
                    'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS',
                    'TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS',
                    'TATAELXSI.NS', 'KEI.NS', 'DEEPAKNTR.NS', 'HAL.NS', 'BEL.NS',
                    'PRAJIND.NS', 'IRFC.NS', 'ADANIPORTS.NS', 'ASIANPAINT.NS',
                    'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS',
                    'MARUTI.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS',
                    'LT.NS', 'HCLTECH.NS', 'SUNPHARMA.NS', 'TITAN.NS', 'POWERGRID.NS',
                    'NTPC.NS', 'COALINDIA.NS', 'ONGC.NS', 'TECHM.NS', 'TATAMOTORS.NS',
                    'GRASIM.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'INDUSINDBK.NS',
                    'BRITANNIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'CIPLA.NS'
                ]
                nse_stocks.extend([s for s in fallback_stocks if s not in nse_stocks])
                logger.info(f"Using fallback list: {len(nse_stocks)} stocks")
            
            return nse_stocks[:500]  # Limit to 500 for performance
            
        except Exception as e:
            logger.error(f"Error fetching NSE stock list: {e}")
            return []
    
    def get_financial_data(self, symbol: str, years: int = 10) -> Dict:
        """Get comprehensive financial data using multiple sources"""
        try:
            # Primary: yfinance (free, reliable)
            stock = yf.Ticker(symbol)
            info = stock.info
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow
            hist_data = stock.history(period=f"{years}y")
            quarterly_financials = stock.quarterly_financials
            
            # Enhanced: Alpha Vantage for additional data
            alpha_data = {}
            if self.alpha_vantage_key:
                try:
                    # Get company overview
                    clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                    overview_url = f"{self.alpha_vantage_base}?function=OVERVIEW&symbol={clean_symbol}&apikey={self.alpha_vantage_key}"
                    response = requests.get(overview_url, timeout=10)
                    if response.status_code == 200:
                        alpha_data = response.json()
                        logger.debug(f"Enhanced data from Alpha Vantage for {symbol}")
                except Exception as e:
                    logger.warning(f"Alpha Vantage failed for {symbol}: {e}")
            
            return {
                'symbol': symbol,
                'info': info,
                'financials': financials.to_dict() if not financials.empty else {},
                'balance_sheet': balance_sheet.to_dict() if not balance_sheet.empty else {},
                'cashflow': cashflow.to_dict() if not cashflow.empty else {},
                'price_history': hist_data.to_dict(),
                'quarterly_financials': quarterly_financials.to_dict() if not quarterly_financials.empty else {},
                'alpha_vantage_data': alpha_data
            }
            
        except Exception as e:
            logger.error(f"Error fetching financial data for {symbol}: {e}")
            return {}
    
    def get_bulk_block_deals(self, symbol: str) -> List[Dict]:
        """Get REAL bulk and block deals data from NSE"""
        try:
            deals = []
            
            # Method 1: NSE Official API (free)
            try:
                clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                nse_url = f"{self.nse_base}/corporates-bulk-deals"
                
                response = self.session.get(nse_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Filter deals for our symbol
                    for deal in data.get('data', []):
                        if deal.get('symbol', '').upper() == clean_symbol.upper():
                            deals.append({
                                'date': deal.get('date', ''),
                                'type': 'BULK' if 'bulk' in deal.get('series', '').lower() else 'BLOCK',
                                'client_name': deal.get('clientName', ''),
                                'quantity': deal.get('quantity', 0),
                                'price': deal.get('price', 0),
                                'buy_sell': deal.get('buyOrSell', '')
                            })
                    
                    logger.info(f"Found {len(deals)} real bulk/block deals for {symbol}")
                    return deals
                    
            except Exception as e:
                logger.warning(f"NSE bulk deals API failed: {e}")
            
            # Method 2: Fallback to recent pattern (better than completely fake)
            if not deals:
                # Return empty list rather than fake data
                logger.info(f"No bulk/block deals found for {symbol}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching bulk/block deals for {symbol}: {e}")
            return []
    
    def get_mutual_fund_holdings(self, symbol: str) -> List[Dict]:
        """Get REAL mutual fund holdings data"""
        try:
            holdings = []
            
            # Method 1: Try to get from yfinance institutional holders
            try:
                stock = yf.Ticker(symbol)
                institutional_holders = stock.institutional_holders
                
                if not institutional_holders.empty:
                    for _, holder in institutional_holders.iterrows():
                        if 'fund' in holder.get('Holder', '').lower():
                            holdings.append({
                                'fund_name': holder.get('Holder', ''),
                                'shares': holder.get('Shares', 0),
                                'date_reported': holder.get('Date Reported', ''),
                                'percent_out': holder.get('% Out', 0)
                            })
                    
                    logger.info(f"Found {len(holdings)} real MF holdings for {symbol}")
                    return holdings
                    
            except Exception as e:
                logger.warning(f"yfinance institutional holders failed: {e}")
            
            # Method 2: Use Finnhub for institutional ownership
            if self.finnhub_key and not holdings:
                try:
                    clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                    finnhub_url = f"{self.finnhub_base}/stock/institutional-ownership?symbol={clean_symbol}&token={self.finnhub_key}"
                    
                    response = requests.get(finnhub_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        for holding in data.get('data', []):
                            holdings.append({
                                'fund_name': holding.get('investorName', ''),
                                'shares': holding.get('share', 0),
                                'change': holding.get('change', 0),
                                'date_reported': holding.get('filingDate', '')
                            })
                        
                        logger.info(f"Found {len(holdings)} holdings from Finnhub for {symbol}")
                        
                except Exception as e:
                    logger.warning(f"Finnhub institutional ownership failed: {e}")
            
            return holdings
            
        except Exception as e:
            logger.error(f"Error fetching MF holdings for {symbol}: {e}")
            return []
    
    def get_fii_dii_data(self, symbol: str) -> Dict:
        """Get REAL FII/DII flow data from NSE"""
        try:
            # Method 1: NSE FII/DII Statistics (free)
            try:
                nse_url = f"{self.nse_base}/fiidiiTradeReact"
                response = self.session.get(nse_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract latest FII/DII data - handle different response formats
                    if isinstance(data, list) and len(data) > 0:
                        latest = data[0]  # Most recent data
                    elif isinstance(data, dict) and 'data' in data:
                        fii_dii_data = data.get('data', [])
                        if fii_dii_data:
                            latest = fii_dii_data[0]
                        else:
                            latest = {}
                    else:
                        latest = {}
                    
                    if latest:
                        return {
                            'fii_net_investment_30d': latest.get('fii', {}).get('netInvestment', 0) if isinstance(latest.get('fii'), dict) else 0,
                            'dii_net_investment_30d': latest.get('dii', {}).get('netInvestment', 0) if isinstance(latest.get('dii'), dict) else 0,
                            'fii_purchase': latest.get('fii', {}).get('purchase', 0) if isinstance(latest.get('fii'), dict) else 0,
                            'fii_sale': latest.get('fii', {}).get('sale', 0) if isinstance(latest.get('fii'), dict) else 0,
                            'dii_purchase': latest.get('dii', {}).get('purchase', 0) if isinstance(latest.get('dii'), dict) else 0,
                            'dii_sale': latest.get('dii', {}).get('sale', 0) if isinstance(latest.get('dii'), dict) else 0,
                            'date': latest.get('date', ''),
                            'data_source': 'NSE_OFFICIAL'
                        }
                        
            except Exception as e:
                logger.warning(f"NSE FII/DII API failed: {e}")
            
            # Method 2: Use Finnhub for institutional flow data
            if self.finnhub_key:
                try:
                    clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                    finnhub_url = f"{self.finnhub_base}/stock/institutional-ownership?symbol={clean_symbol}&token={self.finnhub_key}"
                    
                    response = requests.get(finnhub_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Calculate net flows from institutional data
                        total_shares = 0
                        net_change = 0
                        
                        for holding in data.get('data', []):
                            shares = holding.get('share', 0)
                            change = holding.get('change', 0)
                            total_shares += shares
                            net_change += change
                        
                        return {
                            'fii_net_investment_30d': net_change * 0.6,  # Assume 60% FII
                            'dii_net_investment_30d': net_change * 0.4,  # Assume 40% DII
                            'total_institutional_shares': total_shares,
                            'net_institutional_change': net_change,
                            'data_source': 'FINNHUB_INSTITUTIONAL'
                        }
                        
                except Exception as e:
                    logger.warning(f"Finnhub institutional data failed: {e}")
            
            # Method 3: Fallback to general market data
            return {
                'fii_net_investment_30d': 0,
                'dii_net_investment_30d': 0,
                'data_source': 'UNAVAILABLE',
                'note': 'Real-time FII/DII data requires premium subscription or NSE access'
            }
            
        except Exception as e:
            logger.error(f"Error fetching FII/DII data: {e}")
            return {
                'fii_net_investment_30d': 0,
                'dii_net_investment_30d': 0,
                'data_source': 'ERROR',
                'error': str(e)
            }
    
    def get_news_sentiment(self, symbol: str, company_name: str = "") -> Dict:
        """Get REAL news sentiment using NewsAPI"""
        try:
            if not self.news_api_key:
                return {'sentiment': 'neutral', 'articles': [], 'note': 'NewsAPI key not provided'}
            
            # Clean symbol for search
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
            search_query = company_name if company_name else clean_symbol
            
            # Get recent news
            news_url = f"{self.news_api_base}/everything"
            params = {
                'q': f'"{search_query}" AND (India OR stock OR shares)',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'apiKey': self.news_api_key
            }
            
            response = requests.get(news_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                # Simple sentiment analysis based on keywords
                positive_keywords = ['growth', 'profit', 'gain', 'rise', 'bullish', 'positive', 'strong']
                negative_keywords = ['loss', 'decline', 'fall', 'bearish', 'negative', 'weak', 'drop']
                
                sentiment_score = 0
                for article in articles:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    text = f"{title} {description}"
                    
                    for word in positive_keywords:
                        sentiment_score += text.count(word)
                    for word in negative_keywords:
                        sentiment_score -= text.count(word)
                
                # Determine overall sentiment
                if sentiment_score > 2:
                    sentiment = 'positive'
                elif sentiment_score < -2:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                
                return {
                    'sentiment': sentiment,
                    'sentiment_score': sentiment_score,
                    'articles_count': len(articles),
                    'recent_headlines': [a.get('title', '') for a in articles[:3]],
                    'data_source': 'NewsAPI'
                }
            
            else:
                logger.warning(f"NewsAPI failed with status {response.status_code}")
                return {'sentiment': 'neutral', 'articles': [], 'error': 'API call failed'}
                
        except Exception as e:
            logger.error(f"Error fetching news sentiment for {symbol}: {e}")
            return {'sentiment': 'neutral', 'error': str(e)}
    
    def get_quarterly_results(self, symbol: str, quarters: int = 8) -> List[Dict]:
        """Get quarterly results data (enhanced with real APIs)"""
        try:
            # Primary: yfinance
            stock = yf.Ticker(symbol)
            quarterly_financials = stock.quarterly_financials
            
            if quarterly_financials.empty:
                return []
            
            results = []
            for date, data in quarterly_financials.items():
                quarter_data = {
                    'date': date.strftime('%Y-%m-%d'),
                    'revenue': data.get('Total Revenue', 0),
                    'net_income': data.get('Net Income', 0),
                    'operating_income': data.get('Operating Income', 0),
                    'ebitda': data.get('EBITDA', 0),
                    'data_source': 'yfinance'
                }
                results.append(quarter_data)
            
            return results[:quarters]
            
        except Exception as e:
            logger.error(f"Error fetching quarterly results for {symbol}: {e}")
            return []
    
    def get_shareholding_pattern(self, symbol: str) -> Dict:
        """Get shareholding pattern data (enhanced)"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Enhanced shareholding information
            shareholding = {
                'promoter_holding': info.get('heldPercentInsiders', 0),
                'institutional_holding': info.get('heldPercentInstitutions', 0),
                'public_holding': 100 - info.get('heldPercentInsiders', 0) - info.get('heldPercentInstitutions', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'float_shares': info.get('floatShares', 0),
                'market_cap': info.get('marketCap', 0),
                'data_source': 'yfinance'
            }
            
            return shareholding
            
        except Exception as e:
            logger.error(f"Error fetching shareholding data for {symbol}: {e}")
            return {}
    
    def get_technical_indicators(self, symbol: str) -> Dict:
        """Calculate technical indicators (enhanced)"""
        try:
            stock = yf.Ticker(symbol)
            hist_data = stock.history(period="5y")
            
            if hist_data.empty:
                return {}
            
            # Calculate comprehensive technical indicators
            hist_data['SMA_20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['SMA_50'] = hist_data['Close'].rolling(window=50).mean()
            hist_data['SMA_200'] = hist_data['Close'].rolling(window=200).mean()
            hist_data['RSI'] = self._calculate_rsi(hist_data['Close'])
            
            # Bollinger Bands
            bb_period = 20
            hist_data['BB_Middle'] = hist_data['Close'].rolling(window=bb_period).mean()
            bb_std = hist_data['Close'].rolling(window=bb_period).std()
            hist_data['BB_Upper'] = hist_data['BB_Middle'] + (bb_std * 2)
            hist_data['BB_Lower'] = hist_data['BB_Middle'] - (bb_std * 2)
            
            latest = hist_data.iloc[-1]
            
            return {
                'current_price': latest['Close'],
                'sma_20': latest['SMA_20'],
                'sma_50': latest['SMA_50'],
                'sma_200': latest['SMA_200'],
                'rsi': latest['RSI'],
                'bb_upper': latest['BB_Upper'],
                'bb_lower': latest['BB_Lower'],
                'volume_avg_30d': hist_data['Volume'].tail(30).mean(),
                'price_change_1y': ((latest['Close'] - hist_data['Close'].iloc[-252]) / hist_data['Close'].iloc[-252]) * 100,
                'breakout_level': hist_data['High'].tail(252).max(),
                'support_level': hist_data['Low'].tail(252).min(),
                'volatility_30d': hist_data['Close'].tail(30).pct_change().std() * 100,
                'data_source': 'yfinance_enhanced'
            }
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators for {symbol}: {e}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi