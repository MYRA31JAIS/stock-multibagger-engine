"""
Final Multibagger Synthesis Agent (Supervisor) - Aggregates all agent outputs and ranks companies
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class SupervisorAgent:
    def __init__(self, agent_weights: Dict = None):
        self.name = "Multibagger Synthesis Supervisor"
        self.version = "1.0"
        
        # Default weights if not provided
        self.agent_weights = agent_weights or {
            'fundamentals': 0.35,
            'management': 0.15,
            'policy_macro': 0.20,
            'smart_money': 0.15,
            'technicals': 0.15
        }
        
        # Scoring thresholds
        self.multibagger_threshold = 0.60  # Reduced from 0.75 to 0.60
        self.watchlist_threshold = 0.45    # Reduced from 0.60 to 0.45
        self.rejection_threshold = 0.30    # Reduced from 0.40 to 0.30
        
    def synthesize_analysis(self, stock_analyses: List[Dict]) -> Dict:
        """
        Aggregate outputs from all agents and create final ranking
        Apply weighted scoring and normalize results
        """
        try:
            logger.info(f"Starting synthesis of {len(stock_analyses)} stock analyses")
            
            high_probability_multibaggers = []
            early_watchlist = []
            rejected_stocks = []
            
            for stock_analysis in stock_analyses:
                try:
                    # Extract individual agent scores
                    symbol = stock_analysis.get('symbol', 'Unknown')
                    
                    # Get agent outputs
                    fundamental_output = stock_analysis.get('fundamental_analysis', {})
                    management_output = stock_analysis.get('management_analysis', {})
                    technical_output = stock_analysis.get('technical_analysis', {})
                    smart_money_output = stock_analysis.get('smart_money_analysis', {})
                    policy_output = stock_analysis.get('policy_analysis', {})
                    
                    # Calculate weighted score
                    weighted_score = self._calculate_weighted_score(
                        fundamental_output, management_output, technical_output,
                        smart_money_output, policy_output
                    )
                    
                    # Determine category and create stock entry
                    stock_entry = self._create_stock_entry(
                        stock_analysis, weighted_score, fundamental_output,
                        management_output, technical_output, smart_money_output, policy_output
                    )
                    
                    # Categorize based on score
                    if weighted_score >= self.multibagger_threshold:
                        high_probability_multibaggers.append(stock_entry)
                    elif weighted_score >= self.watchlist_threshold:
                        early_watchlist.append(stock_entry)
                    else:
                        rejected_stocks.append(stock_entry)
                        
                except Exception as e:
                    logger.error(f"Error processing stock analysis: {e}")
                    continue
            
            # Sort by probability score (descending)
            high_probability_multibaggers.sort(key=lambda x: x['multibagger_probability'], reverse=True)
            early_watchlist.sort(key=lambda x: x['multibagger_probability'], reverse=True)
            
            # Create final output
            final_output = {
                "high_probability_multibaggers": high_probability_multibaggers,
                "early_watchlist": early_watchlist,
                "rejected_stocks": rejected_stocks[:10],  # Top 10 rejected for reference
                "analysis_summary": {
                    "total_stocks_analyzed": len(stock_analyses),
                    "high_conviction_count": len(high_probability_multibaggers),
                    "watchlist_count": len(early_watchlist),
                    "rejected_count": len(rejected_stocks),
                    "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "disclaimer": "For research & learning only. Not financial advice."
            }
            
            logger.info(f"Synthesis completed. High conviction: {len(high_probability_multibaggers)}, "
                       f"Watchlist: {len(early_watchlist)}, Rejected: {len(rejected_stocks)}")
            
            return final_output
            
        except Exception as e:
            logger.error(f"Error in synthesis: {e}")
            return self._create_default_output()
    
    def _calculate_weighted_score(self, fundamental_output: Dict, management_output: Dict,
                                technical_output: Dict, smart_money_output: Dict,
                                policy_output: Dict) -> float:
        """Calculate weighted score from all agent outputs"""
        try:
            # Extract normalized scores (0-10 scale)
            fundamental_score = fundamental_output.get('fundamental_score', 0) / 10
            management_score = management_output.get('management_quality_score', 0) / 10
            smart_money_score = smart_money_output.get('smart_money_conviction_score', 0) / 10
            
            # Technical score needs special handling
            technical_score = self._normalize_technical_score(technical_output)
            
            # Policy score needs special handling
            policy_score = self._normalize_policy_score(policy_output)
            
            # Calculate weighted average
            weighted_score = (
                fundamental_score * self.agent_weights['fundamentals'] +
                management_score * self.agent_weights['management'] +
                technical_score * self.agent_weights['technicals'] +
                smart_money_score * self.agent_weights['smart_money'] +
                policy_score * self.agent_weights['policy_macro']
            )
            
            return min(1.0, max(0.0, weighted_score))  # Ensure 0-1 range
            
        except Exception as e:
            logger.error(f"Error calculating weighted score: {e}")
            return 0.0
    
    def _normalize_technical_score(self, technical_output: Dict) -> float:
        """Normalize technical analysis to 0-1 score"""
        try:
            technical_stage = technical_output.get('technical_stage', 'BASE')
            risk_reward = technical_output.get('risk_reward_ratio', '1:1')
            
            # Base score from technical stage - made more generous
            stage_scores = {
                'BREAKOUT': 0.9,  # Increased from 0.8
                'BASE': 0.7,      # Increased from 0.6
                'EXTENDED': 0.4   # Increased from 0.3
            }
            
            base_score = stage_scores.get(technical_stage, 0.6)
            
            # Adjust based on risk-reward ratio
            rr_multipliers = {
                '1:3+': 1.2,
                '1:2': 1.1,
                '1:1.5': 1.0,
                '1:1': 0.95  # Less penalty for 1:1 ratio
            }
            
            multiplier = rr_multipliers.get(risk_reward, 1.0)
            final_score = base_score * multiplier
            
            return min(1.0, final_score)
            
        except Exception as e:
            logger.error(f"Error normalizing technical score: {e}")
            return 0.6  # Higher default score
    
    def _normalize_policy_score(self, policy_output: Dict) -> float:
        """Normalize policy analysis to 0-1 score"""
        try:
            policy_strength = policy_output.get('policy_tailwind_strength', 'WEAK')
            time_horizon = policy_output.get('time_horizon', 'SHORT')
            
            # Base score from policy strength - increased scores
            strength_scores = {
                'STRONG': 0.9,    # Increased from 0.8
                'MODERATE': 0.7,  # Increased from 0.6
                'WEAK': 0.4       # Increased from 0.3
            }
            
            base_score = strength_scores.get(policy_strength, 0.4)
            
            # Adjust based on time horizon
            horizon_multipliers = {
                'LONG': 1.1,      # Slightly reduced from 1.2
                'MEDIUM': 1.0,
                'SHORT': 0.9      # Increased from 0.8
            }
            
            multiplier = horizon_multipliers.get(time_horizon, 1.0)
            final_score = base_score * multiplier
            
            return min(1.0, final_score)
            
        except Exception as e:
            logger.error(f"Error normalizing policy score: {e}")
            return 0.4
    
    def _create_stock_entry(self, stock_analysis: Dict, weighted_score: float,
                          fundamental_output: Dict, management_output: Dict,
                          technical_output: Dict, smart_money_output: Dict,
                          policy_output: Dict) -> Dict:
        """Create standardized stock entry for output"""
        try:
            symbol = stock_analysis.get('symbol', 'Unknown')
            
            # Debug: Check what's in stock_analysis
            logger.debug(f"Stock analysis keys for {symbol}: {list(stock_analysis.keys())}")
            
            # Try to get financial data and info
            financial_data = stock_analysis.get('financial_data', {})
            info = financial_data.get('info', {}) if financial_data else {}
            
            logger.debug(f"Financial data available for {symbol}: {len(financial_data) > 0}")
            logger.debug(f"Info data available for {symbol}: {len(info) > 0}")
            
            # If no info, let's see what keys are in financial_data
            if not info and financial_data:
                logger.debug(f"Financial data keys for {symbol}: {list(financial_data.keys())}")
            
            # Extract key information with better fallback
            sector = info.get('sector', 'Unknown')
            market_cap_usd = info.get('marketCap', 0)
            
            # Better market cap handling
            if market_cap_usd and market_cap_usd > 0:
                market_cap_inr = f"₹{market_cap_usd / 83:.0f} Cr"
                logger.debug(f"Market cap for {symbol}: ${market_cap_usd:,} USD = {market_cap_inr}")
            else:
                market_cap_inr = "Unknown"
                logger.warning(f"No market cap data available for {symbol}")
            
            # Determine expected timeframe
            expected_timeframe = self._determine_timeframe(
                fundamental_output, technical_output, policy_output
            )
            
            # Extract key triggers
            key_triggers = self._extract_key_triggers(
                fundamental_output, management_output, smart_money_output, policy_output
            )
            
            # Extract major risks
            major_risks = self._extract_major_risks(
                fundamental_output, management_output, technical_output
            )
            
            # Determine agent consensus
            agent_consensus = self._determine_consensus(weighted_score)
            
            return {
                "symbol": symbol,
                "sector": sector,
                "market_cap": market_cap_inr,
                "multibagger_probability": round(weighted_score, 3),
                "expected_timeframe": expected_timeframe,
                "key_triggers": key_triggers,
                "major_risks": major_risks,
                "agent_consensus": agent_consensus,
                "detailed_scores": {
                    "fundamental_score": fundamental_output.get('fundamental_score', 0),
                    "management_score": management_output.get('management_quality_score', 0),
                    "technical_stage": technical_output.get('technical_stage', 'BASE'),
                    "smart_money_score": smart_money_output.get('smart_money_conviction_score', 0),
                    "policy_strength": policy_output.get('policy_tailwind_strength', 'WEAK')
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating stock entry: {e}")
            return {
                "symbol": stock_analysis.get('symbol', 'Unknown'),
                "sector": "Unknown",
                "market_cap": "Unknown",
                "multibagger_probability": weighted_score,
                "expected_timeframe": "3-5 years",
                "key_triggers": ["Analysis error"],
                "major_risks": ["Data insufficient"],
                "agent_consensus": "LOW CONVICTION"
            }
    
    def _determine_timeframe(self, fundamental_output: Dict, technical_output: Dict,
                           policy_output: Dict) -> str:
        """Determine expected multibagger timeframe"""
        try:
            # Check fundamental momentum
            fundamental_score = fundamental_output.get('fundamental_score', 0)
            
            # Check technical stage
            technical_stage = technical_output.get('technical_stage', 'BASE')
            
            # Check policy horizon
            policy_horizon = policy_output.get('time_horizon', 'SHORT')
            
            # Determine timeframe based on combination
            if (fundamental_score >= 7 and technical_stage == 'BREAKOUT' and 
                policy_horizon in ['MEDIUM', 'LONG']):
                return "2-3 years"
            elif fundamental_score >= 6 and technical_stage in ['BREAKOUT', 'BASE']:
                return "3-5 years"
            else:
                return "5+ years"
                
        except Exception as e:
            logger.error(f"Error determining timeframe: {e}")
            return "3-5 years"
    
    def _extract_key_triggers(self, fundamental_output: Dict, management_output: Dict,
                            smart_money_output: Dict, policy_output: Dict) -> List[str]:
        """Extract key positive triggers"""
        triggers = []
        
        try:
            # Fundamental triggers
            improving_metrics = fundamental_output.get('key_improving_metrics', [])
            triggers.extend(improving_metrics[:2])  # Top 2
            
            # Management triggers
            management_changes = management_output.get('evidence_of_change', [])
            triggers.extend(management_changes[:1])  # Top 1
            
            # Smart money triggers
            investors = smart_money_output.get('investors_detected', [])
            if investors:
                triggers.append(f"Smart money: {', '.join(investors[:2])}")
            
            # Policy triggers
            policy_strength = policy_output.get('policy_tailwind_strength', 'WEAK')
            if policy_strength in ['STRONG', 'MODERATE']:
                triggers.append(f"Policy tailwinds: {policy_strength.lower()}")
            
            return triggers[:5]  # Max 5 triggers
            
        except Exception as e:
            logger.error(f"Error extracting triggers: {e}")
            return ["Analysis incomplete"]
    
    def _extract_major_risks(self, fundamental_output: Dict, management_output: Dict,
                           technical_output: Dict) -> List[str]:
        """Extract major risk factors"""
        risks = []
        
        try:
            # Fundamental risks
            red_flags = fundamental_output.get('red_flags', [])
            risks.extend(red_flags[:2])  # Top 2
            
            # Management risks
            alignment = management_output.get('minority_shareholder_alignment', 'MEDIUM')
            if alignment == 'LOW':
                risks.append("Poor minority shareholder alignment")
            
            # Technical risks
            technical_stage = technical_output.get('technical_stage', 'BASE')
            if technical_stage == 'EXTENDED':
                risks.append("Technically extended levels")
            
            # Generic risks if none found
            if not risks:
                risks.append("Market volatility")
                risks.append("Execution risk")
            
            return risks[:4]  # Max 4 risks
            
        except Exception as e:
            logger.error(f"Error extracting risks: {e}")
            return ["Analysis incomplete"]
    
    def _determine_consensus(self, weighted_score: float) -> str:
        """Determine agent consensus level"""
        if weighted_score >= 0.85:
            return "STRONG BUY (High Conviction)"
        elif weighted_score >= 0.75:
            return "BUY (High Conviction)"
        elif weighted_score >= 0.65:
            return "BUY (Medium Conviction)"
        elif weighted_score >= 0.55:
            return "HOLD (Low Conviction)"
        else:
            return "AVOID (Low Conviction)"
    
    def _create_default_output(self) -> Dict:
        """Create default output for error cases"""
        return {
            "high_probability_multibaggers": [],
            "early_watchlist": [],
            "rejected_stocks": [],
            "analysis_summary": {
                "total_stocks_analyzed": 0,
                "high_conviction_count": 0,
                "watchlist_count": 0,
                "rejected_count": 0,
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": "Analysis failed"
            },
            "disclaimer": "For research & learning only. Not financial advice."
        }