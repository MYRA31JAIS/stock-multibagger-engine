#!/usr/bin/env python3
"""
Test script to verify AI providers are working
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
load_dotenv('multibagger_system/.env', override=True)

# Add the multibagger_system directory to Python path
sys.path.append('multibagger_system')

from agents.fundamental_agent import FundamentalAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ai_providers():
    """Test all available AI providers"""
    print("🤖 Testing AI Providers for Multibagger System")
    print("=" * 50)
    
    # Initialize the agent
    agent = FundamentalAgent()
    
    print(f"Agent Version: {agent.version}")
    print(f"AI Enabled: {agent.ai_enabled}")
    print(f"Available Providers: {list(agent.ai_providers.keys()) if agent.ai_providers else 'None'}")
    print()
    
    if not agent.ai_enabled:
        print("❌ No AI providers available!")
        print("\nTo enable AI providers, add API keys to .env files:")
        print("- GOOGLE_GEMINI_API_KEY (FREE)")
        print("- GROQ_API_KEY (FREE)")
        print("- ANTHROPIC_API_KEY (FREE tier)")
        print("- HUGGINGFACE_API_KEY (FREE)")
        print("- OPENAI_API_KEY (paid)")
        return
    
    # Test data
    test_financial_data = {
        'symbol': 'TCS.NS',
        'info': {
            'sector': 'Technology',
            'industry': 'Information Technology Services',
            'marketCap': 1500000000000  # 15 lakh crores
        },
        'financials': {
            '2023': {'Total Revenue': 100000, 'Net Income': 20000, 'Operating Income': 25000},
            '2022': {'Total Revenue': 90000, 'Net Income': 18000, 'Operating Income': 22000},
            '2021': {'Total Revenue': 80000, 'Net Income': 16000, 'Operating Income': 20000}
        }
    }
    
    # Test revenue analysis
    revenue_analysis = agent._analyze_revenue_growth(test_financial_data['financials'])
    profitability_analysis = agent._analyze_profitability(test_financial_data['financials'])
    
    print("📊 Testing AI Analysis...")
    print(f"Revenue CAGR: {revenue_analysis.get('cagr_5y', 0):.1f}%")
    print(f"Profitability improving: {profitability_analysis.get('margin_expansion', False)}")
    print()
    
    # Test AI insights
    ai_insights = agent._get_ai_insights(test_financial_data, revenue_analysis, profitability_analysis)
    
    if ai_insights:
        print("✅ AI Analysis Successful!")
        print(f"Provider Used: {ai_insights.get('ai_provider', 'Unknown')}")
        print(f"Confidence: {ai_insights.get('confidence', 'N/A')}")
        print(f"Strengths: {ai_insights.get('strengths', [])}")
        print(f"Risks: {ai_insights.get('risks', [])}")
        print(f"Reasoning: {ai_insights.get('reasoning', 'N/A')}")
    else:
        print("❌ AI Analysis Failed!")
        print("All providers failed or returned empty results")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_ai_providers()