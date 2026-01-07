#!/usr/bin/env python3
"""
Test real API integration with actual data
"""
import sys
import os
import requests
import json

# Add the multibagger_system to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'multibagger_system'))

def test_api_integration():
    """Test if APIs are working with real data"""
    print("🧪 Testing Real API Integration")
    print("=" * 50)
    
    try:
        from data_sources.nse_data_fetcher import NSEDataFetcher
        
        # Initialize data fetcher
        fetcher = NSEDataFetcher()
        
        # Test 1: Stock list fetching
        print("\n📊 Testing Stock List Fetching...")
        stocks = fetcher.get_nse_stock_list()
        print(f"✅ Fetched {len(stocks)} stocks")
        print(f"   Sample stocks: {stocks[:5]}")
        
        # Test 2: Real bulk deals data
        print("\n💰 Testing Bulk Deals Data...")
        test_symbol = "RELIANCE.NS"
        bulk_deals = fetcher.get_bulk_block_deals(test_symbol)
        print(f"✅ Bulk deals for {test_symbol}: {len(bulk_deals)} deals")
        if bulk_deals:
            print(f"   Sample deal: {bulk_deals[0]}")
        else:
            print("   No recent bulk deals found (this is normal)")
        
        # Test 3: News sentiment
        print("\n📰 Testing News Sentiment...")
        news_sentiment = fetcher.get_news_sentiment(test_symbol, "Reliance Industries")
        print(f"✅ News sentiment: {news_sentiment.get('sentiment', 'unknown')}")
        print(f"   Data source: {news_sentiment.get('data_source', 'unknown')}")
        if news_sentiment.get('recent_headlines'):
            print(f"   Sample headline: {news_sentiment['recent_headlines'][0]}")
        
        # Test 4: FII/DII data
        print("\n🏦 Testing FII/DII Data...")
        fii_dii = fetcher.get_fii_dii_data(test_symbol)
        print(f"✅ FII/DII data source: {fii_dii.get('data_source', 'unknown')}")
        print(f"   FII net investment: {fii_dii.get('fii_net_investment_30d', 'N/A')}")
        
        # Test 5: Enhanced technical indicators
        print("\n📈 Testing Enhanced Technical Data...")
        technical = fetcher.get_technical_indicators(test_symbol)
        print(f"✅ Technical data source: {technical.get('data_source', 'unknown')}")
        print(f"   Current price: ₹{technical.get('current_price', 'N/A')}")
        print(f"   RSI: {technical.get('rsi', 'N/A')}")
        print(f"   Volatility (30d): {technical.get('volatility_30d', 'N/A'):.2f}%" if technical.get('volatility_30d') else "   Volatility: N/A")
        
        print("\n🎉 API Integration Test Completed!")
        print("\n📋 Summary:")
        print(f"   • Stock Universe: {len(stocks)} stocks (vs 28 hardcoded)")
        print(f"   • Bulk Deals: {'Real NSE data' if bulk_deals else 'No recent deals'}")
        print(f"   • News Sentiment: {news_sentiment.get('data_source', 'Not available')}")
        print(f"   • FII/DII Flows: {fii_dii.get('data_source', 'Not available')}")
        print(f"   • Technical Data: Enhanced with volatility metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ API Integration test failed: {e}")
        return False

def test_backend_api():
    """Test the Flask backend API"""
    print("\n🌐 Testing Backend API...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend health: {health_data.get('status')}")
            print(f"   System initialized: {health_data.get('system_initialized')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test system status
        response = requests.get("http://localhost:5000/api/system-status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ System status: {status_data.get('status')}")
            print(f"   Agents active: {status_data.get('agents_active', 0)}")
        else:
            print(f"❌ System status check failed: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - make sure Python server is running")
        return False
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Enhanced Multibagger System with Real APIs")
    print("=" * 60)
    
    # Test API integration
    api_success = test_api_integration()
    
    # Test backend API
    backend_success = test_backend_api()
    
    if api_success and backend_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n🚀 Your system is ready for real multibagger analysis!")
        print("\n📱 Next steps:")
        print("   1. Open http://localhost:3001 in your browser")
        print("   2. Click 'Initialize AI System'")
        print("   3. Select stocks and run analysis")
        print("   4. Watch the 6 AI agents find multibaggers!")
    else:
        print("\n⚠️  Some tests failed - check the errors above")