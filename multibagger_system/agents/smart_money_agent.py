"""
Smart Money Agent - Tracks institutional investor flows and accumulation patterns
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SmartMoneyAgent:
    def __init__(self):
        self.name = "Smart Money Agent"
        self.version = "1.0"
        
    def analyze(self, financial_data: Dict, fii_dii_data: Dict, 
                mf_holdings: List[Dict], bulk_deals: List[Dict]) -> Dict:
        """
        Analyze smart money flows and institutional accumulation
        Focus on identifying early institutional footprints
        """
        try:
            logger.info(f"Smart money analysis starting for {financial_data.get('symbol', 'Unknown')}")
            
            symbol = financial_data.get('symbol', 'Unknown')
            
            # Analyze different smart money indicators
            fii_dii_analysis = self._analyze_fii_dii_flows(fii_dii_data)
            mf_analysis = self._analyze_mutual_fund_activity(mf_holdings)
            bulk_deal_analysis = self._analyze_bulk_deals(bulk_deals)
            pe_vc_analysis = self._analyze_pe_vc_activity(financial_data)
            promoter_buying_analysis = self._analyze_promoter_buying(bulk_deals)
            
            # Combine analyses
            investors_detected = []
            score_components = []
            
            # FII/DII Flow Score (0-2 points)
            fii_dii_score = self._score_fii_dii_activity(fii_dii_analysis)
            score_components.append(fii_dii_score)
            if fii_dii_analysis.get('net_positive_flow', False):
                investors_detected.append("FII/DII net buyers")
            
            # Mutual Fund Score (0-2 points)
            mf_score = self._score_mutual_fund_activity(mf_analysis)
            score_components.append(mf_score)
            if mf_analysis.get('increasing_holdings', False):
                investors_detected.extend(mf_analysis.get('active_funds', []))
            
            # Bulk Deal Score (0-2 points)
            bulk_deal_score = self._score_bulk_deal_activity(bulk_deal_analysis)
            score_components.append(bulk_deal_score)
            if bulk_deal_analysis.get('institutional_buying', False):
                investors_detected.append("Institutional bulk buyers")
            
            # PE/VC Score (0-2 points)
            pe_vc_score = self._score_pe_vc_activity(pe_vc_analysis)
            score_components.append(pe_vc_score)
            if pe_vc_analysis.get('pe_vc_presence', False):
                investors_detected.append("PE/VC investors")
            
            # Promoter Buying Score (0-2 points)
            promoter_score = self._score_promoter_buying(promoter_buying_analysis)
            score_components.append(promoter_score)
            if promoter_buying_analysis.get('promoter_buying', False):
                investors_detected.append("Promoter buying")
            
            # Calculate final score (0-10)
            final_score = sum(score_components)
            
            # Determine accumulation trend
            accumulation_trend = self._determine_accumulation_trend(
                fii_dii_analysis, mf_analysis, bulk_deal_analysis
            )
            
            logger.info(f"Smart money analysis completed. Score: {final_score}/10")
            
            return {
                "smart_money_conviction_score": round(final_score, 2),
                "investors_detected": investors_detected,
                "accumulation_trend": accumulation_trend,
                "detailed_analysis": {
                    "fii_net_investment_30d": fii_dii_analysis.get('fii_net_30d', 0),
                    "dii_net_investment_30d": fii_dii_analysis.get('dii_net_30d', 0),
                    "mf_holding_count": len(mf_holdings),
                    "bulk_deals_30d": len([d for d in bulk_deals if self._is_recent_deal(d)]),
                    "institutional_holding_percent": fii_dii_analysis.get('total_institutional_holding', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in smart money analysis: {e}")
            return self._create_default_response(f"Analysis error: {str(e)}")
    
    def _analyze_fii_dii_flows(self, fii_dii_data: Dict) -> Dict:
        """Analyze FII/DII investment flows"""
        try:
            fii_net_30d = fii_dii_data.get('fii_net_investment_30d', 0)
            dii_net_30d = fii_dii_data.get('dii_net_investment_30d', 0)
            fii_holding = fii_dii_data.get('fii_holding_percent', 0)
            dii_holding = fii_dii_data.get('dii_holding_percent', 0)
            
            # Analyze flow patterns
            net_positive_flow = (fii_net_30d + dii_net_30d) > 0
            strong_fii_flow = fii_net_30d > 10  # > 10 Cr net investment
            strong_dii_flow = dii_net_30d > 5   # > 5 Cr net investment
            
            # Analyze holding levels
            significant_fii_holding = fii_holding > 10
            significant_dii_holding = dii_holding > 15
            
            total_institutional_holding = fii_holding + dii_holding
            
            return {
                'fii_net_30d': fii_net_30d,
                'dii_net_30d': dii_net_30d,
                'net_positive_flow': net_positive_flow,
                'strong_fii_flow': strong_fii_flow,
                'strong_dii_flow': strong_dii_flow,
                'significant_fii_holding': significant_fii_holding,
                'significant_dii_holding': significant_dii_holding,
                'total_institutional_holding': total_institutional_holding
            }
            
        except Exception as e:
            logger.error(f"Error analyzing FII/DII flows: {e}")
            return {'net_positive_flow': False, 'total_institutional_holding': 0}
    
    def _analyze_mutual_fund_activity(self, mf_holdings: List[Dict]) -> Dict:
        """Analyze mutual fund holding patterns"""
        try:
            if not mf_holdings:
                return {'increasing_holdings': False, 'active_funds': [], 'total_mf_holding': 0}
            
            # Calculate total MF holding
            total_mf_holding = sum(holding.get('holding_percent', 0) for holding in mf_holdings)
            
            # Identify active funds (holding > 1%)
            active_funds = [
                holding['fund_name'] for holding in mf_holdings 
                if holding.get('holding_percent', 0) > 1.0
            ]
            
            # Check for quality fund presence
            quality_funds = []
            quality_keywords = ['hdfc', 'icici', 'sbi', 'axis', 'kotak', 'franklin', 'dsp']
            
            for holding in mf_holdings:
                fund_name = holding.get('fund_name', '').lower()
                if any(keyword in fund_name for keyword in quality_keywords):
                    quality_funds.append(holding['fund_name'])
            
            # Assume increasing holdings if multiple quality funds present
            increasing_holdings = len(quality_funds) >= 2 and total_mf_holding > 5
            
            return {
                'increasing_holdings': increasing_holdings,
                'active_funds': active_funds[:3],  # Top 3 funds
                'quality_funds': quality_funds,
                'total_mf_holding': total_mf_holding,
                'fund_count': len(mf_holdings)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing mutual fund activity: {e}")
            return {'increasing_holdings': False, 'active_funds': [], 'total_mf_holding': 0}
    
    def _analyze_bulk_deals(self, bulk_deals: List[Dict]) -> Dict:
        """Analyze bulk and block deal patterns"""
        try:
            if not bulk_deals:
                return {'institutional_buying': False, 'recent_activity': False}
            
            # Filter recent deals (last 30 days)
            recent_deals = [deal for deal in bulk_deals if self._is_recent_deal(deal)]
            
            # Analyze deal patterns
            buy_deals = [deal for deal in recent_deals if deal.get('buy_sell', '').upper() == 'BUY']
            sell_deals = [deal for deal in recent_deals if deal.get('buy_sell', '').upper() == 'SELL']
            
            # Check for institutional buyers
            institutional_keywords = ['mutual fund', 'insurance', 'pms', 'aif', 'fund']
            institutional_buying = False
            
            for deal in buy_deals:
                client_name = deal.get('client_name', '').lower()
                if any(keyword in client_name for keyword in institutional_keywords):
                    institutional_buying = True
                    break
            
            # Calculate net buying pressure
            total_buy_value = sum(deal.get('quantity', 0) * deal.get('price', 0) for deal in buy_deals)
            total_sell_value = sum(deal.get('quantity', 0) * deal.get('price', 0) for deal in sell_deals)
            
            net_buying = total_buy_value > total_sell_value
            recent_activity = len(recent_deals) > 0
            
            return {
                'institutional_buying': institutional_buying,
                'recent_activity': recent_activity,
                'net_buying': net_buying,
                'recent_deals_count': len(recent_deals),
                'buy_deals_count': len(buy_deals),
                'sell_deals_count': len(sell_deals)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing bulk deals: {e}")
            return {'institutional_buying': False, 'recent_activity': False}
    
    def _analyze_pe_vc_activity(self, financial_data: Dict) -> Dict:
        """Analyze PE/VC investor presence"""
        try:
            info = financial_data.get('info', {})
            business_summary = str(info.get('longBusinessSummary', '')).lower()
            
            # Look for PE/VC keywords
            pe_vc_keywords = [
                'private equity', 'venture capital', 'pe fund', 'vc fund',
                'investment fund', 'capital partners', 'equity partners'
            ]
            
            pe_vc_presence = any(keyword in business_summary for keyword in pe_vc_keywords)
            
            # Check for recent PE/VC entry (simplified)
            recent_pe_entry = 'recent investment' in business_summary or 'funding' in business_summary
            
            return {
                'pe_vc_presence': pe_vc_presence,
                'recent_pe_entry': recent_pe_entry
            }
            
        except Exception as e:
            logger.error(f"Error analyzing PE/VC activity: {e}")
            return {'pe_vc_presence': False, 'recent_pe_entry': False}
    
    def _analyze_promoter_buying(self, bulk_deals: List[Dict]) -> Dict:
        """Analyze promoter buying activity"""
        try:
            if not bulk_deals:
                return {'promoter_buying': False, 'promoter_deals_count': 0}
            
            # Look for promoter-related deals
            promoter_keywords = ['promoter', 'director', 'founder', 'chairman', 'managing director']
            promoter_deals = []
            
            for deal in bulk_deals:
                client_name = deal.get('client_name', '').lower()
                if any(keyword in client_name for keyword in promoter_keywords):
                    promoter_deals.append(deal)
            
            # Check for recent promoter buying
            recent_promoter_deals = [
                deal for deal in promoter_deals 
                if self._is_recent_deal(deal) and deal.get('buy_sell', '').upper() == 'BUY'
            ]
            
            promoter_buying = len(recent_promoter_deals) > 0
            
            return {
                'promoter_buying': promoter_buying,
                'promoter_deals_count': len(recent_promoter_deals),
                'total_promoter_deals': len(promoter_deals)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing promoter buying: {e}")
            return {'promoter_buying': False, 'promoter_deals_count': 0}
    
    def _score_fii_dii_activity(self, analysis: Dict) -> float:
        """Score FII/DII activity (0-2 points)"""
        score = 0
        
        if analysis.get('net_positive_flow', False):
            score += 0.5
        
        if analysis.get('strong_fii_flow', False):
            score += 0.5
        
        if analysis.get('strong_dii_flow', False):
            score += 0.5
        
        if analysis.get('significant_fii_holding', False) or analysis.get('significant_dii_holding', False):
            score += 0.5
        
        return min(2.0, score)
    
    def _score_mutual_fund_activity(self, analysis: Dict) -> float:
        """Score mutual fund activity (0-2 points)"""
        score = 0
        
        if analysis.get('increasing_holdings', False):
            score += 1.0
        
        if analysis.get('total_mf_holding', 0) > 10:
            score += 0.5
        
        if len(analysis.get('quality_funds', [])) >= 2:
            score += 0.5
        
        return min(2.0, score)
    
    def _score_bulk_deal_activity(self, analysis: Dict) -> float:
        """Score bulk deal activity (0-2 points)"""
        score = 0
        
        if analysis.get('institutional_buying', False):
            score += 1.0
        
        if analysis.get('net_buying', False):
            score += 0.5
        
        if analysis.get('recent_activity', False):
            score += 0.5
        
        return min(2.0, score)
    
    def _score_pe_vc_activity(self, analysis: Dict) -> float:
        """Score PE/VC activity (0-2 points)"""
        score = 0
        
        if analysis.get('pe_vc_presence', False):
            score += 1.0
        
        if analysis.get('recent_pe_entry', False):
            score += 1.0
        
        return min(2.0, score)
    
    def _score_promoter_buying(self, analysis: Dict) -> float:
        """Score promoter buying (0-2 points)"""
        score = 0
        
        if analysis.get('promoter_buying', False):
            score += 1.5
        
        if analysis.get('promoter_deals_count', 0) > 1:
            score += 0.5
        
        return min(2.0, score)
    
    def _determine_accumulation_trend(self, fii_dii_analysis: Dict, 
                                    mf_analysis: Dict, bulk_deal_analysis: Dict) -> str:
        """Determine overall accumulation trend"""
        
        positive_indicators = 0
        
        if fii_dii_analysis.get('net_positive_flow', False):
            positive_indicators += 1
        
        if mf_analysis.get('increasing_holdings', False):
            positive_indicators += 1
        
        if bulk_deal_analysis.get('institutional_buying', False):
            positive_indicators += 1
        
        if positive_indicators >= 2:
            return "YES"
        else:
            return "NO"
    
    def _is_recent_deal(self, deal: Dict) -> bool:
        """Check if deal is within last 30 days"""
        try:
            deal_date = datetime.strptime(deal.get('date', '2020-01-01'), '%Y-%m-%d')
            cutoff_date = datetime.now() - timedelta(days=30)
            return deal_date >= cutoff_date
        except:
            return False
    
    def _create_default_response(self, reason: str) -> Dict:
        """Create default response for error cases"""
        return {
            "smart_money_conviction_score": 0.0,
            "investors_detected": [],
            "accumulation_trend": "NO",
            "detailed_analysis": {"error": reason}
        }