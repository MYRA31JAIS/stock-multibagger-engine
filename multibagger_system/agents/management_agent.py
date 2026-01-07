"""
Management & Promoter Change Agent - Analyzes management quality and governance changes
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ManagementAnalysis:
    management_quality_score: float
    evidence_of_change: List[str]
    minority_shareholder_alignment: str

class ManagementAgent:
    def __init__(self):
        self.name = "Management & Promoter Change Agent"
        self.version = "1.0"
        
    def analyze(self, financial_data: Dict, shareholding_data: Dict) -> Dict:
        """
        Analyze management quality and governance changes
        Focus on detecting management credibility upgrades
        """
        try:
            logger.info(f"Management analysis starting for {financial_data.get('symbol', 'Unknown')}")
            
            info = financial_data.get('info', {})
            symbol = financial_data.get('symbol', 'Unknown')
            
            # Analyze different aspects of management quality
            promoter_analysis = self._analyze_promoter_changes(shareholding_data, info)
            governance_analysis = self._analyze_governance_quality(info)
            management_track_record = self._analyze_management_track_record(info)
            transparency_analysis = self._analyze_transparency(info)
            
            # Combine analyses
            evidence_of_change = []
            score_components = []
            
            # Promoter holding changes (0-2.5 points)
            promoter_score = self._score_promoter_quality(promoter_analysis)
            score_components.append(promoter_score)
            if promoter_analysis.get('stable_holding', False):
                evidence_of_change.append("Stable promoter holding indicates confidence")
            if promoter_analysis.get('strategic_investor', False):
                evidence_of_change.append("Strategic investor entry detected")
            
            # Governance quality (0-2.5 points)
            governance_score = self._score_governance(governance_analysis)
            score_components.append(governance_score)
            if governance_analysis.get('professional_management', False):
                evidence_of_change.append("Professional management team in place")
            if governance_analysis.get('board_independence', False):
                evidence_of_change.append("Independent board structure")
            
            # Management track record (0-2.5 points)
            track_record_score = self._score_track_record(management_track_record)
            score_components.append(track_record_score)
            if management_track_record.get('experienced_team', False):
                evidence_of_change.append("Experienced management team")
            
            # Transparency and communication (0-2.5 points)
            transparency_score = self._score_transparency(transparency_analysis)
            score_components.append(transparency_score)
            if transparency_analysis.get('good_disclosure', False):
                evidence_of_change.append("Good disclosure practices")
            
            # Calculate final score (0-10)
            final_score = sum(score_components)
            
            # Determine minority shareholder alignment
            alignment = self._determine_shareholder_alignment(
                promoter_analysis, governance_analysis, transparency_analysis
            )
            
            logger.info(f"Management analysis completed. Score: {final_score}/10")
            
            return {
                "management_quality_score": round(final_score, 2),
                "evidence_of_change": evidence_of_change,
                "minority_shareholder_alignment": alignment,
                "detailed_analysis": {
                    "promoter_holding_percent": promoter_analysis.get('promoter_holding', 0),
                    "institutional_holding_percent": promoter_analysis.get('institutional_holding', 0),
                    "governance_score": governance_score,
                    "transparency_score": transparency_score
                }
            }
            
        except Exception as e:
            logger.error(f"Error in management analysis: {e}")
            return self._create_default_response(f"Analysis error: {str(e)}")
    
    def _analyze_promoter_changes(self, shareholding_data: Dict, info: Dict) -> Dict:
        """Analyze promoter holding patterns and changes"""
        try:
            promoter_holding = shareholding_data.get('promoter_holding', 0)
            institutional_holding = shareholding_data.get('institutional_holding', 0)
            
            # Analyze promoter holding stability
            stable_holding = 40 <= promoter_holding <= 75  # Optimal range
            high_promoter_holding = promoter_holding > 75
            low_promoter_holding = promoter_holding < 25
            
            # Check for strategic investors
            strategic_investor = institutional_holding > 20
            
            # Check for PE/VC presence (simplified check)
            pe_vc_presence = 'private equity' in str(info.get('longBusinessSummary', '')).lower()
            
            return {
                'promoter_holding': promoter_holding,
                'institutional_holding': institutional_holding,
                'stable_holding': stable_holding,
                'high_promoter_holding': high_promoter_holding,
                'low_promoter_holding': low_promoter_holding,
                'strategic_investor': strategic_investor,
                'pe_vc_presence': pe_vc_presence
            }
            
        except Exception as e:
            logger.error(f"Error analyzing promoter changes: {e}")
            return {'promoter_holding': 0, 'stable_holding': False}
    
    def _analyze_governance_quality(self, info: Dict) -> Dict:
        """Analyze corporate governance quality"""
        try:
            # Check for professional management indicators
            business_summary = str(info.get('longBusinessSummary', '')).lower()
            
            professional_management = any(keyword in business_summary for keyword in [
                'professional management', 'experienced leadership', 'industry veteran',
                'former ceo', 'ex-', 'iim', 'iit', 'mba'
            ])
            
            # Check board independence (simplified)
            board_independence = info.get('governanceEpochDate') is not None
            
            # Check for related party transaction concerns
            rpt_concerns = 'related party' in business_summary
            
            # Check company age (older companies might have better governance)
            company_age = 2024 - info.get('foundingYear', 2020) if info.get('foundingYear') else 4
            established_company = company_age > 10
            
            return {
                'professional_management': professional_management,
                'board_independence': board_independence,
                'rpt_concerns': rpt_concerns,
                'established_company': established_company,
                'company_age': company_age
            }
            
        except Exception as e:
            logger.error(f"Error analyzing governance quality: {e}")
            return {'professional_management': False, 'board_independence': False}
    
    def _analyze_management_track_record(self, info: Dict) -> Dict:
        """Analyze management track record and experience"""
        try:
            business_summary = str(info.get('longBusinessSummary', '')).lower()
            
            # Look for experience indicators
            experienced_team = any(keyword in business_summary for keyword in [
                'years of experience', 'decades', 'veteran', 'expertise',
                'track record', 'proven', 'established'
            ])
            
            # Check for industry expertise
            industry_expertise = any(keyword in business_summary for keyword in [
                'industry leader', 'market leader', 'pioneer', 'innovator'
            ])
            
            # Check for past success indicators
            past_success = any(keyword in business_summary for keyword in [
                'successful', 'growth', 'expansion', 'turnaround'
            ])
            
            return {
                'experienced_team': experienced_team,
                'industry_expertise': industry_expertise,
                'past_success': past_success
            }
            
        except Exception as e:
            logger.error(f"Error analyzing management track record: {e}")
            return {'experienced_team': False}
    
    def _analyze_transparency(self, info: Dict) -> Dict:
        """Analyze transparency and communication quality"""
        try:
            # Check for good disclosure practices
            has_website = info.get('website') is not None
            has_business_summary = len(str(info.get('longBusinessSummary', ''))) > 100
            
            # Check for regular communication
            regular_updates = info.get('lastFiscalYearEnd') is not None
            
            # Check for investor relations
            good_disclosure = has_website and has_business_summary and regular_updates
            
            return {
                'has_website': has_website,
                'has_business_summary': has_business_summary,
                'regular_updates': regular_updates,
                'good_disclosure': good_disclosure
            }
            
        except Exception as e:
            logger.error(f"Error analyzing transparency: {e}")
            return {'good_disclosure': False}
    
    def _score_promoter_quality(self, analysis: Dict) -> float:
        """Score promoter quality (0-2.5 points)"""
        score = 0
        
        if analysis.get('stable_holding', False):
            score += 1.5
        elif analysis.get('high_promoter_holding', False):
            score += 1.0
        elif analysis.get('low_promoter_holding', False):
            score += 0.5
        
        if analysis.get('strategic_investor', False):
            score += 0.5
        
        if analysis.get('pe_vc_presence', False):
            score += 0.5
        
        return min(2.5, score)
    
    def _score_governance(self, analysis: Dict) -> float:
        """Score governance quality (0-2.5 points)"""
        score = 0
        
        if analysis.get('professional_management', False):
            score += 1.0
        
        if analysis.get('board_independence', False):
            score += 0.5
        
        if analysis.get('established_company', False):
            score += 0.5
        
        if not analysis.get('rpt_concerns', True):  # No RPT concerns is good
            score += 0.5
        
        return min(2.5, score)
    
    def _score_track_record(self, analysis: Dict) -> float:
        """Score management track record (0-2.5 points)"""
        score = 0
        
        if analysis.get('experienced_team', False):
            score += 1.0
        
        if analysis.get('industry_expertise', False):
            score += 0.75
        
        if analysis.get('past_success', False):
            score += 0.75
        
        return min(2.5, score)
    
    def _score_transparency(self, analysis: Dict) -> float:
        """Score transparency (0-2.5 points)"""
        score = 0
        
        if analysis.get('good_disclosure', False):
            score += 1.5
        
        if analysis.get('has_website', False):
            score += 0.5
        
        if analysis.get('regular_updates', False):
            score += 0.5
        
        return min(2.5, score)
    
    def _determine_shareholder_alignment(self, promoter_analysis: Dict, 
                                       governance_analysis: Dict, 
                                       transparency_analysis: Dict) -> str:
        """Determine minority shareholder alignment level"""
        
        alignment_score = 0
        
        # Promoter factors
        if promoter_analysis.get('stable_holding', False):
            alignment_score += 2
        if promoter_analysis.get('strategic_investor', False):
            alignment_score += 1
        
        # Governance factors
        if governance_analysis.get('professional_management', False):
            alignment_score += 2
        if not governance_analysis.get('rpt_concerns', True):
            alignment_score += 1
        
        # Transparency factors
        if transparency_analysis.get('good_disclosure', False):
            alignment_score += 2
        
        if alignment_score >= 6:
            return "HIGH"
        elif alignment_score >= 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _create_default_response(self, reason: str) -> Dict:
        """Create default response for error cases"""
        return {
            "management_quality_score": 0.0,
            "evidence_of_change": [],
            "minority_shareholder_alignment": "LOW",
            "detailed_analysis": {"error": reason}
        }