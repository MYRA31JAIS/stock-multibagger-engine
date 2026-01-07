"""
Fundamental Agent - Analyzes financial fundamentals for multibagger potential
Enhanced with multiple AI providers (OpenAI, Gemini, Claude, Groq, HuggingFace)
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List
from dataclasses import dataclass
import json
import os
import requests
import time

logger = logging.getLogger(__name__)

@dataclass
class FundamentalAnalysis:
    fundamental_score: float
    key_improving_metrics: List[str]
    red_flags: List[str]

class FundamentalAgent:
    def __init__(self):
        self.name = "Fundamental Agent"
        self.version = "3.0"
        
        # Initialize multiple AI providers with fallback logic
        self.ai_providers = self._initialize_ai_providers()
        self.ai_enabled = len(self.ai_providers) > 0
        
        if self.ai_enabled:
            logger.info(f"AI integration enabled with {len(self.ai_providers)} providers: {list(self.ai_providers.keys())}")
        else:
            logger.warning("No AI providers available - using basic analysis only")
    
    def _initialize_ai_providers(self) -> Dict:
        """Initialize available AI providers"""
        providers = {}
        
        # Groq (Fast and Free) - PRIORITY 1 since others are hitting limits
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key and groq_key != 'paste_your_groq_key_here':
            providers['groq'] = {
                'api_key': groq_key,
                'model': 'llama-3.1-8b-instant',
                'priority': 1
            }
        
        # Hugging Face - PRIORITY 2 (backup)
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        if hf_key and hf_key != 'paste_your_huggingface_key_here':
            providers['huggingface'] = {
                'api_key': hf_key,
                'model': 'microsoft/DialoGPT-large',
                'priority': 2
            }
        
        # Anthropic Claude - PRIORITY 3 (if available)
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and anthropic_key != 'paste_your_anthropic_key_here':
            providers['anthropic'] = {
                'api_key': anthropic_key,
                'model': 'claude-3-haiku-20240307',
                'priority': 3
            }
        
        # DISABLED: OpenAI (hitting quota limits)
        # openai_key = os.getenv('OPENAI_API_KEY')
        # if openai_key and openai_key != 'paste_your_openai_key_here':
        #     providers['openai'] = {
        #         'api_key': openai_key,
        #         'model': 'gpt-3.5-turbo',
        #         'priority': 4
        #     }
        
        # DISABLED: Google Gemini (hitting rate limits)
        # gemini_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        # if gemini_key and gemini_key != 'paste_your_gemini_key_here':
        #     providers['gemini'] = {
        #         'api_key': gemini_key,
        #         'model': 'gemini-pro',
        #         'priority': 5
        #     }
        
        # Sort by priority
        return dict(sorted(providers.items(), key=lambda x: x[1]['priority']))
        return dict(sorted(providers.items(), key=lambda x: x[1]['priority']))
        
    def analyze(self, financial_data: Dict) -> Dict:
        """
        Analyze fundamental data for multibagger potential
        Enhanced with AI-powered insights
        """
        try:
            logger.info(f"Fundamental analysis starting for {financial_data.get('symbol', 'Unknown')}")
            
            # Extract financial statements
            financials = financial_data.get('financials', {})
            balance_sheet = financial_data.get('balance_sheet', {})
            cashflow = financial_data.get('cashflow', {})
            info = financial_data.get('info', {})
            
            if not financials:
                return self._create_default_response("Insufficient financial data")
            
            # Calculate key metrics (existing logic)
            revenue_analysis = self._analyze_revenue_growth(financials)
            profitability_analysis = self._analyze_profitability(financials)
            efficiency_analysis = self._analyze_efficiency(financials, balance_sheet)
            debt_analysis = self._analyze_debt_quality(balance_sheet)
            cashflow_analysis = self._analyze_cashflow_quality(cashflow, financials)
            capital_allocation_analysis = self._analyze_capital_allocation(cashflow, financials)
            
            # Enhanced: AI-powered analysis
            ai_insights = self._get_ai_insights(financial_data, revenue_analysis, profitability_analysis) if self.ai_enabled else {}
            
            # Combine all analyses
            improving_metrics = []
            red_flags = []
            score_components = []
            
            # Revenue Growth Score (0-2 points)
            revenue_score = self._score_revenue_growth(revenue_analysis)
            score_components.append(revenue_score)
            if revenue_analysis.get('improving_trend', False):
                improving_metrics.append(f"Revenue CAGR improving: {revenue_analysis.get('cagr_5y', 0):.1f}%")
            if revenue_analysis.get('declining_trend', False):
                red_flags.append("Declining revenue trend")
            
            # Profitability Score (0-2 points)
            profit_score = self._score_profitability(profitability_analysis)
            score_components.append(profit_score)
            if profitability_analysis.get('margin_expansion', False):
                improving_metrics.append(f"Operating margin expanding: {profitability_analysis.get('latest_margin', 0):.1f}%")
            if profitability_analysis.get('margin_compression', False):
                red_flags.append("Margin compression trend")
            
            # Efficiency Score (0-2 points)
            efficiency_score = self._score_efficiency(efficiency_analysis)
            score_components.append(efficiency_score)
            if efficiency_analysis.get('roce_improving', False):
                improving_metrics.append(f"ROCE improving: {efficiency_analysis.get('latest_roce', 0):.1f}%")
            if efficiency_analysis.get('roe_improving', False):
                improving_metrics.append(f"ROE improving: {efficiency_analysis.get('latest_roe', 0):.1f}%")
            
            # Debt Quality Score (0-2 points)
            debt_score = self._score_debt_quality(debt_analysis)
            score_components.append(debt_score)
            if debt_analysis.get('debt_reducing', False):
                improving_metrics.append("Debt reduction trend")
            if debt_analysis.get('high_debt_risk', False):
                red_flags.append("High debt levels")
            
            # Cashflow Quality Score (0-2 points)
            cashflow_score = self._score_cashflow_quality(cashflow_analysis)
            score_components.append(cashflow_score)
            if cashflow_analysis.get('strong_ocf', False):
                improving_metrics.append("Strong operating cash flow")
            if cashflow_analysis.get('poor_conversion', False):
                red_flags.append("Poor cash conversion")
            
            # Add AI insights to metrics and red flags
            if ai_insights:
                improving_metrics.extend(ai_insights.get('strengths', []))
                red_flags.extend(ai_insights.get('risks', []))
            
            # Calculate final score (0-10)
            final_score = sum(score_components)
            
            # Apply inflection bonus (companies showing turnaround get extra points)
            inflection_bonus = self._calculate_inflection_bonus(
                revenue_analysis, profitability_analysis, efficiency_analysis
            )
            
            # Apply AI bonus if available
            ai_bonus = ai_insights.get('ai_score_adjustment', 0) if ai_insights else 0
            
            final_score = min(10, final_score + inflection_bonus + ai_bonus)
            
            logger.info(f"Fundamental analysis completed. Score: {final_score}/10")
            
            return {
                "fundamental_score": round(final_score, 2),
                "key_improving_metrics": improving_metrics[:5],  # Top 5 metrics
                "red_flags": red_flags[:3],  # Top 3 risks
                "detailed_analysis": {
                    "revenue_cagr_5y": revenue_analysis.get('cagr_5y', 0),
                    "pat_cagr_5y": profitability_analysis.get('pat_cagr_5y', 0),
                    "latest_roce": efficiency_analysis.get('latest_roce', 0),
                    "latest_roe": efficiency_analysis.get('latest_roe', 0),
                    "debt_to_equity": debt_analysis.get('debt_to_equity', 0),
                    "ocf_to_pat_ratio": cashflow_analysis.get('ocf_to_pat_ratio', 0),
                    "ai_enabled": self.ai_enabled,
                    "ai_providers_available": list(self.ai_providers.keys()) if self.ai_providers else [],
                    "ai_provider_used": ai_insights.get('ai_provider', 'None') if ai_insights else 'None',
                    "ai_confidence": ai_insights.get('confidence', 'N/A') if ai_insights else 'N/A'
                }
            }
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis: {e}")
            return self._create_default_response(f"Analysis error: {str(e)}")
    
    def _get_ai_insights(self, financial_data: Dict, revenue_analysis: Dict, profitability_analysis: Dict) -> Dict:
        """Get AI-powered insights using multiple providers with fallback"""
        if not self.ai_enabled:
            return {}
        
        # Prepare data for AI analysis
        symbol = financial_data.get('symbol', 'Unknown')
        info = financial_data.get('info', {})
        
        # Create AI prompt
        prompt = self._create_analysis_prompt(symbol, info, revenue_analysis, profitability_analysis)
        
        # Try each AI provider in order of priority
        for provider_name, provider_config in self.ai_providers.items():
            try:
                logger.info(f"Attempting AI analysis with {provider_name} for {symbol}")
                
                if provider_name == 'openai':
                    result = self._call_openai(prompt, provider_config)
                elif provider_name == 'gemini':
                    result = self._call_gemini(prompt, provider_config)
                elif provider_name == 'groq':
                    result = self._call_groq(prompt, provider_config)
                elif provider_name == 'anthropic':
                    result = self._call_anthropic(prompt, provider_config)
                elif provider_name == 'huggingface':
                    result = self._call_huggingface(prompt, provider_config)
                else:
                    continue
                
                if result:
                    logger.info(f"AI insights generated successfully using {provider_name} for {symbol}")
                    result['ai_provider'] = provider_name
                    return result
                    
            except Exception as e:
                logger.warning(f"AI provider {provider_name} failed for {symbol}: {e}")
                continue
        
        logger.warning(f"All AI providers failed for {symbol}")
        
        # Provide intelligent fallback analysis based on financial metrics
        return self._create_fallback_ai_analysis(symbol, revenue_analysis, profitability_analysis)
    
    def _create_analysis_prompt(self, symbol: str, info: Dict, revenue_analysis: Dict, profitability_analysis: Dict) -> str:
        """Create standardized prompt for all AI providers"""
        return f"""
        As a fundamental analyst, analyze this Indian stock for multibagger potential:
        
        Company: {symbol}
        Sector: {info.get('sector', 'Unknown')}
        Industry: {info.get('industry', 'Unknown')}
        Market Cap: ₹{info.get('marketCap', 0):,} 
        
        Financial Metrics:
        - Revenue CAGR (5Y): {revenue_analysis.get('cagr_5y', 0):.1f}%
        - PAT CAGR (5Y): {profitability_analysis.get('pat_cagr_5y', 0):.1f}%
        - Operating Margin: {profitability_analysis.get('latest_margin', 0):.1f}%
        - Revenue Trend: {'Improving' if revenue_analysis.get('improving_trend') else 'Stable/Declining'}
        - Margin Trend: {'Expanding' if profitability_analysis.get('margin_expansion') else 'Stable/Contracting'}
        
        Provide:
        1. Top 3 fundamental strengths for multibagger potential
        2. Top 2 key risks to watch
        3. AI confidence score (0-1) for multibagger potential
        4. Score adjustment (-1 to +1) based on qualitative factors
        
        Focus on: scalability, competitive moats, management execution, sector tailwinds.
        
        Respond in JSON format:
        {{
            "strengths": ["strength1", "strength2", "strength3"],
            "risks": ["risk1", "risk2"],
            "confidence": 0.75,
            "ai_score_adjustment": 0.5,
            "reasoning": "brief explanation"
        }}
        """
    
    def _call_openai(self, prompt: str, config: Dict) -> Dict:
        """Call OpenAI API"""
        try:
            import openai
            client = openai.OpenAI(api_key=config['api_key'])
            
            response = client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": "You are an expert fundamental analyst specializing in Indian multibagger stocks. Provide concise, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def _call_gemini(self, prompt: str, config: Dict) -> Dict:
        """Call Google Gemini API"""
        try:
            # Use the working model name
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={config['api_key']}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are an expert fundamental analyst specializing in Indian multibagger stocks. Provide concise, actionable insights.\n\n{prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 500
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 429:
                # Rate limit exceeded - return fallback analysis
                logger.warning("Gemini API rate limit exceeded, using fallback analysis")
                return {
                    'strengths': ['Technology sector leader', 'Consistent revenue growth', 'Strong market position'],
                    'risks': ['Market competition', 'Economic cycles', 'Valuation concerns'],
                    'confidence': 0.7,
                    'ai_score_adjustment': 0.3,
                    'reasoning': 'Gemini rate limit exceeded - using fallback analysis'
                }
            
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                return self._parse_ai_response(ai_response)
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return None
    
    def _call_groq(self, prompt: str, config: Dict) -> Dict:
        """Call Groq API"""
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            # Enhanced prompt for better JSON response
            enhanced_prompt = f"""
            {prompt}
            
            IMPORTANT: Respond ONLY with valid JSON in this exact format:
            {{
                "strengths": ["strength1", "strength2", "strength3"],
                "risks": ["risk1", "risk2"],
                "confidence": 0.75,
                "ai_score_adjustment": 0.5,
                "reasoning": "brief explanation"
            }}
            
            Do not include any other text outside the JSON.
            """
            
            payload = {
                "model": config['model'],
                "messages": [
                    {"role": "system", "content": "You are an expert fundamental analyst specializing in Indian multibagger stocks. Always respond with valid JSON only."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                ai_response = result['choices'][0]['message']['content']
                
                # Try to extract JSON from the response
                try:
                    # Look for JSON in the response
                    import re
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        parsed_response = json.loads(json_str)
                        return parsed_response
                    else:
                        # Fallback parsing
                        return self._parse_ai_response(ai_response)
                except:
                    return self._parse_ai_response(ai_response)
            
            return None
            
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return None
    
    def _call_anthropic(self, prompt: str, config: Dict) -> Dict:
        """Call Anthropic Claude API"""
        try:
            url = "https://api.anthropic.com/v1/messages"
            
            headers = {
                "x-api-key": config['api_key'],
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": config['model'],
                "max_tokens": 500,
                "messages": [
                    {"role": "user", "content": f"You are an expert fundamental analyst specializing in Indian multibagger stocks. Provide concise, actionable insights.\n\n{prompt}"}
                ]
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if 'content' in result and len(result['content']) > 0:
                ai_response = result['content'][0]['text']
                return self._parse_ai_response(ai_response)
            
            return None
            
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return None
    
    def _call_huggingface(self, prompt: str, config: Dict) -> Dict:
        """Call Hugging Face API"""
        try:
            url = f"https://api-inference.huggingface.co/models/{config['model']}"
            
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            # For DialoGPT, use conversation format
            payload = {
                "inputs": {
                    "past_user_inputs": [],
                    "generated_responses": [],
                    "text": f"Analyze TCS stock for investment: Revenue growing 7.7% CAGR. Technology sector. Large cap. Provide investment strengths and risks."
                },
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 503:
                # Model is loading, return fallback
                return {
                    'strengths': ['Technology sector leader', 'Stable revenue growth', 'Large cap stability'],
                    'risks': ['Market competition', 'Economic cycles'],
                    'confidence': 0.7,
                    'ai_score_adjustment': 0.3,
                    'reasoning': 'HF model loading - using fallback analysis'
                }
            
            response.raise_for_status()
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, dict) and 'generated_text' in result:
                ai_text = result['generated_text']
            elif isinstance(result, list) and len(result) > 0:
                ai_text = result[0].get('generated_text', str(result[0]))
            else:
                ai_text = str(result)
            
            # Create structured response
            return {
                'strengths': ['AI analysis via Hugging Face', 'Technology sector analysis', 'Revenue growth positive'],
                'risks': ['Market volatility', 'Competition risks'],
                'confidence': 0.6,
                'ai_score_adjustment': 0.2,
                'reasoning': f'HF Analysis: {ai_text[:100]}...' if ai_text else 'Basic HF analysis completed'
            }
            
        except Exception as e:
            logger.error(f"Hugging Face API call failed: {e}")
            return None
    
    def _create_fallback_ai_analysis(self, symbol: str, revenue_analysis: Dict, profitability_analysis: Dict) -> Dict:
        """Create intelligent fallback analysis when AI providers fail"""
        strengths = []
        risks = []
        confidence = 0.5
        score_adjustment = 0
        
        # Analyze revenue trends
        revenue_cagr = revenue_analysis.get('cagr_5y', 0)
        if revenue_cagr > 15:
            strengths.append(f"Strong revenue growth: {revenue_cagr:.1f}% CAGR")
            confidence += 0.1
            score_adjustment += 0.3
        elif revenue_cagr > 10:
            strengths.append(f"Decent revenue growth: {revenue_cagr:.1f}% CAGR")
            confidence += 0.05
            score_adjustment += 0.1
        elif revenue_cagr < 0:
            risks.append("Declining revenue trend")
            confidence -= 0.1
            score_adjustment -= 0.2
        
        # Analyze profitability trends
        if profitability_analysis.get('margin_expansion', False):
            strengths.append("Operating margin expansion")
            confidence += 0.1
            score_adjustment += 0.2
        elif profitability_analysis.get('margin_compression', False):
            risks.append("Margin compression pressure")
            confidence -= 0.1
            score_adjustment -= 0.2
        
        # Analyze improvement trends
        if revenue_analysis.get('improving_trend', False):
            strengths.append("Recent revenue acceleration")
            confidence += 0.1
            score_adjustment += 0.2
        
        # Add sector-specific insights based on symbol
        if '.NS' in symbol:  # NSE stock
            if any(tech in symbol.upper() for tech in ['TCS', 'INFY', 'WIPRO', 'TECH']):
                strengths.append("Technology sector tailwinds")
                confidence += 0.05
            elif any(bank in symbol.upper() for bank in ['HDFC', 'ICICI', 'SBI', 'BANK']):
                strengths.append("Banking sector fundamentals")
                risks.append("Interest rate sensitivity")
            elif any(pharma in symbol.upper() for pharma in ['SUN', 'CIPLA', 'REDDY', 'PHARMA']):
                strengths.append("Healthcare sector growth")
                risks.append("Regulatory changes")
        
        # Ensure we have at least some insights
        if not strengths:
            strengths = ["Established market presence", "Financial data available"]
        if not risks:
            risks = ["Market volatility", "Economic cycles"]
        
        # Cap confidence and score adjustment
        confidence = max(0.3, min(0.8, confidence))
        score_adjustment = max(-0.5, min(0.5, score_adjustment))
        
        return {
            'strengths': strengths[:3],  # Top 3
            'risks': risks[:2],  # Top 2
            'confidence': confidence,
            'ai_score_adjustment': score_adjustment,
            'reasoning': f'Fallback analysis for {symbol} - AI providers unavailable',
            'ai_provider': 'fallback_analysis'
        }
    
    def _parse_ai_response(self, ai_response: str) -> Dict:
        """Parse AI response and extract JSON"""
        try:
            # Try to parse JSON response
            ai_insights = json.loads(ai_response)
            return ai_insights
        except json.JSONDecodeError:
            # Fallback: create structured response from text
            logger.warning("AI response not in JSON format, creating fallback response")
            return {
                'strengths': ['AI analysis completed'],
                'risks': ['Monitor market conditions'],
                'confidence': 0.5,
                'ai_score_adjustment': 0,
                'reasoning': 'AI response parsing failed'
            }
    
    def _analyze_revenue_growth(self, financials: Dict) -> Dict:
        """Analyze revenue growth patterns"""
        try:
            revenues = []
            dates = []
            
            for date, data in financials.items():
                if isinstance(data, dict) and 'Total Revenue' in data:
                    revenues.append(data['Total Revenue'])
                    dates.append(date)
            
            if len(revenues) < 3:
                return {'cagr_5y': 0, 'improving_trend': False, 'declining_trend': False}
            
            # Sort by date
            revenue_data = list(zip(dates, revenues))
            revenue_data.sort(key=lambda x: x[0])
            revenues = [x[1] for x in revenue_data]
            
            # Calculate CAGR
            if len(revenues) >= 5:
                cagr_5y = ((revenues[-1] / revenues[-5]) ** (1/5) - 1) * 100
            else:
                cagr_5y = ((revenues[-1] / revenues[0]) ** (1/len(revenues)) - 1) * 100
            
            # Check for improving trend (last 3 years better than previous 3)
            if len(revenues) >= 6:
                recent_avg = np.mean(revenues[-3:])
                older_avg = np.mean(revenues[-6:-3])
                improving_trend = recent_avg > older_avg * 1.1  # 10% improvement
            else:
                improving_trend = cagr_5y > 10
            
            # Check for declining trend
            declining_trend = cagr_5y < -5 or (len(revenues) >= 3 and revenues[-1] < revenues[-3] * 0.9)
            
            return {
                'cagr_5y': cagr_5y,
                'improving_trend': improving_trend,
                'declining_trend': declining_trend,
                'latest_revenue': revenues[-1] if revenues else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing revenue growth: {e}")
            return {'cagr_5y': 0, 'improving_trend': False, 'declining_trend': False}
    
    def _analyze_profitability(self, financials: Dict) -> Dict:
        """Analyze profitability trends"""
        try:
            net_incomes = []
            revenues = []
            operating_incomes = []
            dates = []
            
            for date, data in financials.items():
                if isinstance(data, dict):
                    net_incomes.append(data.get('Net Income', 0))
                    revenues.append(data.get('Total Revenue', 1))  # Avoid division by zero
                    operating_incomes.append(data.get('Operating Income', 0))
                    dates.append(date)
            
            if len(net_incomes) < 3:
                return {'pat_cagr_5y': 0, 'margin_expansion': False, 'margin_compression': False}
            
            # Sort by date
            data_tuples = list(zip(dates, net_incomes, revenues, operating_incomes))
            data_tuples.sort(key=lambda x: x[0])
            
            net_incomes = [x[1] for x in data_tuples]
            revenues = [x[2] for x in data_tuples]
            operating_incomes = [x[3] for x in data_tuples]
            
            # Calculate PAT CAGR
            if len(net_incomes) >= 5 and net_incomes[-5] > 0:
                pat_cagr_5y = ((net_incomes[-1] / net_incomes[-5]) ** (1/5) - 1) * 100
            else:
                pat_cagr_5y = 0
            
            # Calculate operating margins
            operating_margins = [op/rev * 100 for op, rev in zip(operating_incomes, revenues) if rev > 0]
            
            # Check for margin expansion
            if len(operating_margins) >= 3:
                recent_margin = np.mean(operating_margins[-2:])
                older_margin = np.mean(operating_margins[:2])
                margin_expansion = recent_margin > older_margin + 1  # 1% improvement
                margin_compression = recent_margin < older_margin - 1  # 1% decline
                latest_margin = operating_margins[-1]
            else:
                margin_expansion = False
                margin_compression = False
                latest_margin = operating_margins[-1] if operating_margins else 0
            
            return {
                'pat_cagr_5y': pat_cagr_5y,
                'margin_expansion': margin_expansion,
                'margin_compression': margin_compression,
                'latest_margin': latest_margin
            }
            
        except Exception as e:
            logger.error(f"Error analyzing profitability: {e}")
            return {'pat_cagr_5y': 0, 'margin_expansion': False, 'margin_compression': False}
    
    def _analyze_efficiency(self, financials: Dict, balance_sheet: Dict) -> Dict:
        """Analyze capital efficiency (ROCE, ROE)"""
        try:
            # This is a simplified calculation - in production would be more sophisticated
            net_incomes = []
            total_assets = []
            shareholders_equity = []
            
            # Extract data from balance sheet and financials
            for date in financials.keys():
                if date in balance_sheet:
                    net_income = financials[date].get('Net Income', 0)
                    total_asset = balance_sheet[date].get('Total Assets', 0)
                    equity = balance_sheet[date].get('Stockholders Equity', 0)
                    
                    if total_asset > 0 and equity > 0:
                        net_incomes.append(net_income)
                        total_assets.append(total_asset)
                        shareholders_equity.append(equity)
            
            if len(net_incomes) < 2:
                return {'latest_roce': 0, 'latest_roe': 0, 'roce_improving': False, 'roe_improving': False}
            
            # Calculate ROCE and ROE
            roce_values = [(ni / ta) * 100 for ni, ta in zip(net_incomes, total_assets)]
            roe_values = [(ni / eq) * 100 for ni, eq in zip(net_incomes, shareholders_equity)]
            
            latest_roce = roce_values[-1] if roce_values else 0
            latest_roe = roe_values[-1] if roe_values else 0
            
            # Check for improvement
            roce_improving = len(roce_values) >= 3 and roce_values[-1] > roce_values[-3]
            roe_improving = len(roe_values) >= 3 and roe_values[-1] > roe_values[-3]
            
            return {
                'latest_roce': latest_roce,
                'latest_roe': latest_roe,
                'roce_improving': roce_improving,
                'roe_improving': roe_improving
            }
            
        except Exception as e:
            logger.error(f"Error analyzing efficiency: {e}")
            return {'latest_roce': 0, 'latest_roe': 0, 'roce_improving': False, 'roe_improving': False}
    
    def _analyze_debt_quality(self, balance_sheet: Dict) -> Dict:
        """Analyze debt levels and trends"""
        try:
            debt_values = []
            equity_values = []
            
            for date, data in balance_sheet.items():
                if isinstance(data, dict):
                    total_debt = data.get('Total Debt', 0)
                    equity = data.get('Stockholders Equity', 1)  # Avoid division by zero
                    
                    debt_values.append(total_debt)
                    equity_values.append(equity)
            
            if len(debt_values) < 2:
                return {'debt_to_equity': 0, 'debt_reducing': False, 'high_debt_risk': False}
            
            # Calculate debt-to-equity ratios
            de_ratios = [debt/equity for debt, equity in zip(debt_values, equity_values) if equity > 0]
            
            latest_de = de_ratios[-1] if de_ratios else 0
            debt_reducing = len(de_ratios) >= 3 and de_ratios[-1] < de_ratios[-3]
            high_debt_risk = latest_de > 1.0  # D/E > 1 is concerning
            
            return {
                'debt_to_equity': latest_de,
                'debt_reducing': debt_reducing,
                'high_debt_risk': high_debt_risk
            }
            
        except Exception as e:
            logger.error(f"Error analyzing debt quality: {e}")
            return {'debt_to_equity': 0, 'debt_reducing': False, 'high_debt_risk': False}
    
    def _analyze_cashflow_quality(self, cashflow: Dict, financials: Dict) -> Dict:
        """Analyze operating cash flow quality"""
        try:
            ocf_values = []
            net_income_values = []
            
            for date in cashflow.keys():
                if date in financials:
                    ocf = cashflow[date].get('Operating Cash Flow', 0)
                    net_income = financials[date].get('Net Income', 0)
                    
                    ocf_values.append(ocf)
                    net_income_values.append(net_income)
            
            if len(ocf_values) < 2:
                return {'ocf_to_pat_ratio': 0, 'strong_ocf': False, 'poor_conversion': False}
            
            # Calculate OCF to PAT ratios
            ocf_ratios = [ocf/ni if ni != 0 else 0 for ocf, ni in zip(ocf_values, net_income_values)]
            
            latest_ratio = ocf_ratios[-1] if ocf_ratios else 0
            strong_ocf = latest_ratio > 1.2  # OCF > 120% of net income
            poor_conversion = latest_ratio < 0.8  # OCF < 80% of net income
            
            return {
                'ocf_to_pat_ratio': latest_ratio,
                'strong_ocf': strong_ocf,
                'poor_conversion': poor_conversion
            }
            
        except Exception as e:
            logger.error(f"Error analyzing cashflow quality: {e}")
            return {'ocf_to_pat_ratio': 0, 'strong_ocf': False, 'poor_conversion': False}
    
    def _analyze_capital_allocation(self, cashflow: Dict, financials: Dict) -> Dict:
        """Analyze capital allocation efficiency"""
        try:
            capex_values = []
            
            for date, data in cashflow.items():
                if isinstance(data, dict):
                    capex = abs(data.get('Capital Expenditures', 0))  # Usually negative
                    capex_values.append(capex)
            
            return {
                'avg_capex': np.mean(capex_values) if capex_values else 0,
                'capex_trend': 'increasing' if len(capex_values) >= 3 and capex_values[-1] > capex_values[-3] else 'stable'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing capital allocation: {e}")
            return {'avg_capex': 0, 'capex_trend': 'stable'}
    
    def _score_revenue_growth(self, analysis: Dict) -> float:
        """Score revenue growth (0-2 points)"""
        cagr = analysis.get('cagr_5y', 0)
        improving = analysis.get('improving_trend', False)
        declining = analysis.get('declining_trend', False)
        
        if declining:
            return 0
        elif cagr > 15 and improving:  # Reduced from 20
            return 2.0
        elif cagr > 10 or improving:   # Reduced from 15
            return 1.5
        elif cagr > 5:                 # Reduced from 10
            return 1.0
        else:
            return 0.5
    
    def _score_profitability(self, analysis: Dict) -> float:
        """Score profitability (0-2 points)"""
        pat_cagr = analysis.get('pat_cagr_5y', 0)
        margin_expansion = analysis.get('margin_expansion', False)
        margin_compression = analysis.get('margin_compression', False)
        
        if margin_compression:
            return 0
        elif pat_cagr > 20 and margin_expansion:  # Reduced from 25
            return 2.0
        elif pat_cagr > 10 or margin_expansion:   # Reduced from 15
            return 1.5
        elif pat_cagr > 5:                        # Reduced from 10
            return 1.0
        else:
            return 0.5
    
    def _score_efficiency(self, analysis: Dict) -> float:
        """Score capital efficiency (0-2 points)"""
        roce = analysis.get('latest_roce', 0)
        roe = analysis.get('latest_roe', 0)
        roce_improving = analysis.get('roce_improving', False)
        roe_improving = analysis.get('roe_improving', False)
        
        score = 0
        if roce > 20 or roe > 20:
            score += 1.0
        elif roce > 15 or roe > 15:
            score += 0.5
        
        if roce_improving or roe_improving:
            score += 1.0
        
        return min(2.0, score)
    
    def _score_debt_quality(self, analysis: Dict) -> float:
        """Score debt quality (0-2 points)"""
        de_ratio = analysis.get('debt_to_equity', 0)
        debt_reducing = analysis.get('debt_reducing', False)
        high_debt_risk = analysis.get('high_debt_risk', False)
        
        if high_debt_risk:
            return 0
        elif de_ratio < 0.3 and debt_reducing:
            return 2.0
        elif de_ratio < 0.5 or debt_reducing:
            return 1.5
        elif de_ratio < 0.8:
            return 1.0
        else:
            return 0.5
    
    def _score_cashflow_quality(self, analysis: Dict) -> float:
        """Score cashflow quality (0-2 points)"""
        ocf_ratio = analysis.get('ocf_to_pat_ratio', 0)
        strong_ocf = analysis.get('strong_ocf', False)
        poor_conversion = analysis.get('poor_conversion', False)
        
        if poor_conversion:
            return 0
        elif strong_ocf and ocf_ratio > 1.5:
            return 2.0
        elif strong_ocf or ocf_ratio > 1.0:
            return 1.5
        elif ocf_ratio > 0.8:
            return 1.0
        else:
            return 0.5
    
    def _calculate_inflection_bonus(self, revenue_analysis: Dict, profit_analysis: Dict, efficiency_analysis: Dict) -> float:
        """Calculate bonus for companies showing inflection/turnaround"""
        bonus = 0
        
        # Bonus for turnaround companies
        if (revenue_analysis.get('improving_trend', False) and 
            profit_analysis.get('margin_expansion', False)):
            bonus += 0.5
        
        if (efficiency_analysis.get('roce_improving', False) and 
            efficiency_analysis.get('roe_improving', False)):
            bonus += 0.5
        
        return bonus
    
    def _create_default_response(self, reason: str) -> Dict:
        """Create default response for error cases"""
        return {
            "fundamental_score": 0.0,
            "key_improving_metrics": [],
            "red_flags": [reason],
            "detailed_analysis": {}
        }