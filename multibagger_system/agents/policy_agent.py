"""
Government & Sector Policy Agent - Analyzes policy tailwinds and sector benefits
Enhanced with real news sentiment analysis
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import re
import os

logger = logging.getLogger(__name__)

class PolicyAgent:
    def __init__(self):
        self.name = "Government & Sector Policy Agent"
        self.version = "2.0"
        
        # Define policy schemes and their beneficiary sectors
        self.policy_schemes = {
            'PLI': {
                'sectors': ['electronics', 'semiconductor', 'telecom', 'pharma', 'auto', 'textile'],
                'strength': 'STRONG',
                'horizon': 'LONG'
            },
            'Make_in_India': {
                'sectors': ['manufacturing', 'defense', 'electronics', 'auto'],
                'strength': 'MODERATE',
                'horizon': 'LONG'
            },
            'Digital_India': {
                'sectors': ['it', 'telecom', 'fintech', 'electronics'],
                'strength': 'STRONG',
                'horizon': 'MEDIUM'
            },
            'Green_Energy': {
                'sectors': ['renewable', 'solar', 'wind', 'battery', 'ev'],
                'strength': 'STRONG',
                'horizon': 'LONG'
            },
            'Infrastructure': {
                'sectors': ['construction', 'cement', 'steel', 'power', 'railways'],
                'strength': 'STRONG',
                'horizon': 'LONG'
            },
            'Defense_Modernization': {
                'sectors': ['defense', 'aerospace', 'electronics'],
                'strength': 'STRONG',
                'horizon': 'LONG'
            },
            'Import_Substitution': {
                'sectors': ['chemicals', 'pharma', 'electronics', 'textiles'],
                'strength': 'MODERATE',
                'horizon': 'MEDIUM'
            }
        }
        
    def analyze(self, financial_data: Dict, news_sentiment: Dict = None) -> Dict:
        """
        Analyze government policy tailwinds for the company
        Enhanced with real news sentiment analysis
        """
        try:
            logger.info(f"Policy analysis starting for {financial_data.get('symbol', 'Unknown')}")
            
            info = financial_data.get('info', {})
            symbol = financial_data.get('symbol', 'Unknown')
            
            # Identify company sector and business
            sector_analysis = self._identify_company_sector(info)
            policy_mapping = self._map_policies_to_company(sector_analysis)
            psu_analysis = self._analyze_psu_benefits(info, symbol)
            capex_benefits = self._analyze_capex_benefits(sector_analysis)
            
            # Enhanced: Analyze news sentiment for policy impact
            news_analysis = self._analyze_news_sentiment(news_sentiment, sector_analysis)
            
            # Calculate policy strength (enhanced with news sentiment)
            policy_strength = self._calculate_policy_strength(policy_mapping, news_analysis)
            time_horizon = self._determine_time_horizon(policy_mapping)
            
            logger.info(f"Policy analysis completed. Strength: {policy_strength}")
            
            return {
                "policy_tailwind_strength": policy_strength,
                "time_horizon": time_horizon,
                "detailed_analysis": {
                    "primary_sector": sector_analysis.get('primary_sector', 'Unknown'),
                    "applicable_policies": policy_mapping.get('applicable_policies', []),
                    "psu_benefits": psu_analysis.get('is_psu_beneficiary', False),
                    "capex_exposure": capex_benefits.get('capex_exposure_level', 'LOW'),
                    "policy_score": policy_mapping.get('total_score', 0),
                    "news_sentiment": news_analysis.get('policy_sentiment', 'neutral'),
                    "recent_policy_news": news_analysis.get('policy_headlines', [])
                }
            }
            
        except Exception as e:
            logger.error(f"Error in policy analysis: {e}")
            return self._create_default_response(f"Analysis error: {str(e)}")
    
    def _identify_company_sector(self, info: Dict) -> Dict:
        """Identify company's primary sector and business activities"""
        try:
            sector = info.get('sector', '').lower()
            industry = info.get('industry', '').lower()
            business_summary = str(info.get('longBusinessSummary', '')).lower()
            
            # Define sector keywords
            sector_keywords = {
                'defense': ['defense', 'defence', 'military', 'aerospace', 'missile', 'radar'],
                'power': ['power', 'electricity', 'energy', 'grid', 'transmission', 'generation'],
                'railways': ['railway', 'rail', 'locomotive', 'wagon', 'signaling'],
                'infrastructure': ['infrastructure', 'construction', 'roads', 'bridges', 'buildings'],
                'electronics': ['electronics', 'semiconductor', 'chips', 'pcb', 'components'],
                'telecom': ['telecom', 'telecommunications', 'network', '5g', 'broadband'],
                'pharma': ['pharmaceutical', 'pharma', 'drugs', 'medicine', 'healthcare'],
                'chemicals': ['chemicals', 'specialty chemicals', 'petrochemicals'],
                'auto': ['automotive', 'automobile', 'auto', 'vehicles', 'components'],
                'renewable': ['solar', 'wind', 'renewable', 'green energy', 'clean energy'],
                'it': ['software', 'information technology', 'it services', 'digital'],
                'manufacturing': ['manufacturing', 'industrial', 'machinery', 'equipment'],
                'textiles': ['textiles', 'garments', 'apparel', 'fabric'],
                'steel': ['steel', 'iron', 'metals', 'alloys'],
                'cement': ['cement', 'concrete', 'building materials']
            }
            
            # Identify primary sector
            identified_sectors = []
            text_to_search = f"{sector} {industry} {business_summary}"
            
            for sector_name, keywords in sector_keywords.items():
                if any(keyword in text_to_search for keyword in keywords):
                    identified_sectors.append(sector_name)
            
            primary_sector = identified_sectors[0] if identified_sectors else 'others'
            
            return {
                'primary_sector': primary_sector,
                'all_sectors': identified_sectors,
                'sector_confidence': 'HIGH' if len(identified_sectors) >= 1 else 'LOW'
            }
            
        except Exception as e:
            logger.error(f"Error identifying company sector: {e}")
            return {'primary_sector': 'others', 'all_sectors': [], 'sector_confidence': 'LOW'}
    
    def _map_policies_to_company(self, sector_analysis: Dict) -> Dict:
        """Map relevant government policies to the company"""
        try:
            primary_sector = sector_analysis.get('primary_sector', 'others')
            all_sectors = sector_analysis.get('all_sectors', [])
            
            applicable_policies = []
            total_score = 0
            
            # Check each policy scheme
            for policy_name, policy_info in self.policy_schemes.items():
                policy_sectors = policy_info['sectors']
                
                # Check if company sector matches policy sectors
                sector_match = False
                for company_sector in [primary_sector] + all_sectors:
                    if any(policy_sector in company_sector or company_sector in policy_sector 
                          for policy_sector in policy_sectors):
                        sector_match = True
                        break
                
                if sector_match:
                    applicable_policies.append({
                        'policy': policy_name,
                        'strength': policy_info['strength'],
                        'horizon': policy_info['horizon'],
                        'relevance': 'HIGH' if primary_sector in policy_sectors else 'MEDIUM'
                    })
                    
                    # Add to score based on strength
                    if policy_info['strength'] == 'STRONG':
                        total_score += 3
                    elif policy_info['strength'] == 'MODERATE':
                        total_score += 2
                    else:
                        total_score += 1
            
            return {
                'applicable_policies': applicable_policies,
                'policy_count': len(applicable_policies),
                'total_score': total_score
            }
            
        except Exception as e:
            logger.error(f"Error mapping policies: {e}")
            return {'applicable_policies': [], 'policy_count': 0, 'total_score': 0}
    
    def _analyze_psu_benefits(self, info: Dict, symbol: str) -> Dict:
        """Analyze PSU reform and privatization benefits"""
        try:
            business_summary = str(info.get('longBusinessSummary', '')).lower()
            company_name = str(info.get('longName', '')).lower()
            
            # Check if company is PSU or PSU beneficiary
            psu_keywords = ['public sector', 'government', 'psu', 'state owned']
            is_psu = any(keyword in business_summary or keyword in company_name 
                        for keyword in psu_keywords)
            
            # Check for PSU beneficiary sectors
            psu_beneficiary_keywords = [
                'defense contractor', 'government contracts', 'public procurement',
                'railway supplier', 'power equipment', 'infrastructure projects'
            ]
            
            is_psu_beneficiary = any(keyword in business_summary 
                                   for keyword in psu_beneficiary_keywords)
            
            # Special handling for known PSU stocks
            psu_symbols = ['HAL.NS', 'BEL.NS', 'IRFC.NS', 'RVNL.NS', 'RAILTEL.NS']
            is_known_psu = symbol in psu_symbols
            
            return {
                'is_psu': is_psu or is_known_psu,
                'is_psu_beneficiary': is_psu_beneficiary or is_known_psu,
                'privatization_candidate': is_psu and not is_known_psu
            }
            
        except Exception as e:
            logger.error(f"Error analyzing PSU benefits: {e}")
            return {'is_psu': False, 'is_psu_beneficiary': False}
    
    def _analyze_capex_benefits(self, sector_analysis: Dict) -> Dict:
        """Analyze government capex beneficiary potential"""
        try:
            primary_sector = sector_analysis.get('primary_sector', 'others')
            
            # Define capex-heavy sectors
            high_capex_sectors = ['defense', 'railways', 'power', 'infrastructure']
            medium_capex_sectors = ['telecom', 'renewable', 'manufacturing']
            
            if primary_sector in high_capex_sectors:
                capex_exposure_level = 'HIGH'
                capex_score = 3
            elif primary_sector in medium_capex_sectors:
                capex_exposure_level = 'MEDIUM'
                capex_score = 2
            else:
                capex_exposure_level = 'LOW'
                capex_score = 1
            
            return {
                'capex_exposure_level': capex_exposure_level,
                'capex_score': capex_score,
                'multi_year_visibility': capex_exposure_level in ['HIGH', 'MEDIUM']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing capex benefits: {e}")
            return {'capex_exposure_level': 'LOW', 'capex_score': 1}
    
    def _analyze_news_sentiment(self, news_sentiment: Dict, sector_analysis: Dict) -> Dict:
        """Analyze news sentiment for policy-related developments"""
        try:
            if not news_sentiment or news_sentiment.get('error'):
                return {
                    'policy_sentiment': 'neutral',
                    'policy_headlines': [],
                    'sentiment_boost': 0
                }
            
            primary_sector = sector_analysis.get('primary_sector', 'others')
            headlines = news_sentiment.get('recent_headlines', [])
            overall_sentiment = news_sentiment.get('sentiment', 'neutral')
            
            # Look for policy-related keywords in headlines
            policy_keywords = [
                'policy', 'government', 'budget', 'scheme', 'pli', 'make in india',
                'infrastructure', 'capex', 'allocation', 'ministry', 'cabinet'
            ]
            
            policy_headlines = []
            policy_sentiment_score = 0
            
            for headline in headlines:
                headline_lower = headline.lower()
                
                # Check if headline is policy-related
                if any(keyword in headline_lower for keyword in policy_keywords):
                    policy_headlines.append(headline)
                    
                    # Analyze sentiment of policy headlines
                    positive_words = ['boost', 'increase', 'support', 'benefit', 'growth', 'expansion']
                    negative_words = ['cut', 'reduce', 'delay', 'concern', 'challenge']
                    
                    for word in positive_words:
                        if word in headline_lower:
                            policy_sentiment_score += 1
                    
                    for word in negative_words:
                        if word in headline_lower:
                            policy_sentiment_score -= 1
            
            # Determine policy sentiment
            if policy_sentiment_score > 1:
                policy_sentiment = 'positive'
                sentiment_boost = 1
            elif policy_sentiment_score < -1:
                policy_sentiment = 'negative'
                sentiment_boost = -1
            else:
                policy_sentiment = 'neutral'
                sentiment_boost = 0
            
            return {
                'policy_sentiment': policy_sentiment,
                'policy_headlines': policy_headlines[:3],  # Top 3 policy headlines
                'sentiment_boost': sentiment_boost
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {e}")
            return {
                'policy_sentiment': 'neutral',
                'policy_headlines': [],
                'sentiment_boost': 0
            }
    
    def _calculate_policy_strength(self, policy_mapping: Dict, news_analysis: Dict = None) -> str:
        """Calculate overall policy tailwind strength (enhanced with news sentiment)"""
        try:
            total_score = policy_mapping.get('total_score', 0)
            policy_count = policy_mapping.get('policy_count', 0)
            
            # Add news sentiment boost
            if news_analysis:
                sentiment_boost = news_analysis.get('sentiment_boost', 0)
                total_score += sentiment_boost
            
            # Determine strength based on score and policy count
            if total_score >= 7 and policy_count >= 2:
                return "STRONG"
            elif total_score >= 4 or policy_count >= 1:
                return "MODERATE"
            else:
                return "WEAK"
                
        except Exception as e:
            logger.error(f"Error calculating policy strength: {e}")
            return "WEAK"
    
    def _determine_time_horizon(self, policy_mapping: Dict) -> str:
        """Determine policy benefit time horizon"""
        try:
            applicable_policies = policy_mapping.get('applicable_policies', [])
            
            if not applicable_policies:
                return "SHORT"
            
            # Count horizon types
            long_count = sum(1 for policy in applicable_policies if policy['horizon'] == 'LONG')
            medium_count = sum(1 for policy in applicable_policies if policy['horizon'] == 'MEDIUM')
            
            if long_count >= 2:
                return "LONG"
            elif long_count >= 1 or medium_count >= 2:
                return "MEDIUM"
            else:
                return "SHORT"
                
        except Exception as e:
            logger.error(f"Error determining time horizon: {e}")
            return "SHORT"
    
    def _create_default_response(self, reason: str) -> Dict:
        """Create default response for error cases"""
        return {
            "policy_tailwind_strength": "WEAK",
            "time_horizon": "SHORT",
            "detailed_analysis": {"error": reason}
        }