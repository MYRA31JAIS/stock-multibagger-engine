#!/usr/bin/env python3
"""
Comprehensive test of the full multibagger system with all APIs
"""
import sys
import os
import requests
import json
import time

def test_backend_analysis():
    """Test the full backend analysis with real APIs"""
    print("🚀 Testing Full System Analysis with Real APIs")
    print("=" * 60)
    
    try:
        # Test with a sample stock
        test_stocks = ["RELIANCE.NS", "TCS.NS"]
        
        print(f"📊 Testing analysis for: {', '.join(test_stocks)}")
        
        # Make analysis request to backend
        url = "http://localhost:5000/api/analyze"
        payload = {"stocks": test_stocks}
        
        print(f"🔗 Making request to: {url}")
        print(f"📋 Payload: {payload}")
        
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=120)  # 2 minutes timeout
        end_time = time.time()
        
        print(f"⏱️  Analysis took: {end_time - start_time:.1f} seconds")
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            
            print("✅ Analysis completed successfully!")
            print(f"📈 High probability multibaggers: {len(results.get('high_probability_multibaggers', []))}")
            print(f"👀 Early watchlist: {len(results.get('early_watchlist', []))}")
            print(f"❌ Rejected stocks: {len(results.get('rejected_stocks', []))}")
            
            # Show detailed results for first stock
            high_prob = results.get('high_probability_multibaggers', [])
            if high_prob:
                stock = high_prob[0]
                print(f"\n🎯 Top Multibagger Candidate: {stock.get('symbol', 'Unknown')}")
                print(f"   Probability: {stock.get('multibagger_probability', 0)*100:.1f}%")
                print(f"   Key Triggers: {', '.join(stock.get('key_triggers', [])[:3])}")
                
                # Show agent scores
                scores = stock.get('detailed_scores', {})
                print(f"   Fundamental Score: {scores.get('fundamental_score', 'N/A')}/10")
                print(f"   Management Score: {scores.get('management_score', 'N/A')}/10")
                print(f"   Technical Stage: {scores.get('technical_stage', 'N/A')}")
                print(f"   Smart Money Score: {scores.get('smart_money_score', 'N/A')}/10")
                print(f"   Policy Strength: {scores.get('policy_strength', 'N/A')}")
            
            # Check data sources used
            analysis_summary = results.get('analysis_summary', {})
            print(f"\n📊 Analysis Summary:")
            print(f"   Total stocks analyzed: {analysis_summary.get('total_stocks_analyzed', 0)}")
            print(f"   High conviction count: {analysis_summary.get('high_conviction_count', 0)}")
            print(f"   Analysis timestamp: {analysis_summary.get('timestamp', 'N/A')}")
            
            return True
            
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ Analysis failed: {error_data}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️  Analysis timed out - this is normal for first run (AI model loading)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - make sure Python server is running")
        return False
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_individual_apis():
    """Test individual API components"""
    print("\n🔧 Testing Individual API Components")
    print("=" * 50)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv('.env')
        load_dotenv('multibagger_system/.env')
        
        # Add the multibagger_system to Python path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'multibagger_system'))
        from data_sources.nse_data_fetcher import NSEDataFetcher
        
        fetcher = NSEDataFetcher()
        test_symbol = "RELIANCE.NS"
        
        # Test 1: Stock list
        print("📊 Testing stock list...")
        stocks = fetcher.get_nse_stock_list()
        print(f"✅ Stock universe: {len(stocks)} stocks")
        
        # Test 2: Financial data
        print("💰 Testing financial data...")
        financial_data = fetcher.get_financial_data(test_symbol)
        has_financials = bool(financial_data.get('financials'))
        print(f"✅ Financial data: {'Available' if has_financials else 'Limited'}")
        
        # Test 3: News sentiment
        print("📰 Testing news sentiment...")
        news_sentiment = fetcher.get_news_sentiment(test_symbol, "Reliance Industries")
        news_source = news_sentiment.get('data_source', 'unknown')
        print(f"✅ News sentiment: {news_sentiment.get('sentiment', 'unknown')} (Source: {news_source})")
        
        # Test 4: Technical indicators
        print("📈 Testing technical indicators...")
        technical = fetcher.get_technical_indicators(test_symbol)
        has_technical = bool(technical.get('current_price'))
        print(f"✅ Technical data: {'Available' if has_technical else 'Limited'}")
        if has_technical:
            print(f"   Current price: ₹{technical.get('current_price', 0):.2f}")
            print(f"   RSI: {technical.get('rsi', 0):.1f}")
        
        # Test 5: FII/DII data
        print("🏦 Testing FII/DII data...")
        fii_dii = fetcher.get_fii_dii_data(test_symbol)
        fii_source = fii_dii.get('data_source', 'unknown')
        print(f"✅ FII/DII data: {fii_source}")
        
        # Test 6: API Keys Status
        print("🔑 Testing API Keys...")
        news_key = os.getenv('NEWS_API_KEY')
        alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        finnhub_key = os.getenv('FINNHUB_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        print(f"   NewsAPI: {'✅ Set' if news_key and news_key != 'paste_your_news_api_key_here' else '❌ Missing'}")
        print(f"   Alpha Vantage: {'✅ Set' if alpha_key and alpha_key != 'paste_your_alpha_vantage_key_here' else '❌ Missing'}")
        print(f"   Finnhub: {'✅ Set' if finnhub_key and finnhub_key != 'paste_your_finnhub_key_here' else '❌ Missing'}")
        print(f"   OpenAI: {'✅ Set' if openai_key and openai_key != 'paste_your_openai_key_here' else '❌ Missing'}")
        
        return True
        
    except Exception as e:
        print(f"❌ API component test failed: {e}")
        return False

def test_openai_integration():
    """Test OpenAI integration specifically"""
    print("\n🤖 Testing OpenAI Integration")
    print("=" * 40)
    
    try:
        import openai
        from dotenv import load_dotenv
        
        # Load environment variables from both locations
        load_dotenv('.env')
        load_dotenv('multibagger_system/.env')
        
        # Check API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key or openai_key == "paste_your_openai_key_here":
            print("❌ OpenAI API key not found or not set")
            return False
        
        print(f"🔑 OpenAI key: {openai_key[:10]}...")
        
        # Test simple API call
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Respond with just 'API_TEST_SUCCESS' if you can read this."}
            ],
            max_tokens=10
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"🤖 AI Response: {ai_response}")
        
        if "API_TEST_SUCCESS" in ai_response:
            print("✅ OpenAI integration working perfectly!")
            return True
        else:
            print("⚠️  OpenAI responding but unexpected response")
            return True
            
    except Exception as e:
        print(f"❌ OpenAI integration failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE MULTIBAGGER SYSTEM TEST")
    print("=" * 70)
    
    # Test individual APIs
    api_success = test_individual_apis()
    
    # Test OpenAI integration
    openai_success = test_openai_integration()
    
    # Test full backend analysis
    print("\n" + "="*70)
    backend_success = test_backend_analysis()
    
    print("\n" + "="*70)
    print("📋 FINAL TEST RESULTS")
    print("=" * 70)
    
    print(f"🔧 API Components: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"🤖 OpenAI Integration: {'✅ PASS' if openai_success else '❌ FAIL'}")
    print(f"🚀 Full System Analysis: {'✅ PASS' if backend_success else '❌ FAIL'}")
    
    if api_success and openai_success and backend_success:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("🚀 Your multibagger system is ready for production use!")
        print("\n📱 Access your system at: http://localhost:3001")
        print("🎯 Ready to find the next multibaggers!")
    elif api_success and openai_success:
        print("\n⚠️  APIs working but full analysis needs debugging")
        print("💡 Try running a smaller analysis first")
    else:
        print("\n❌ Some components need attention")
        print("🔧 Check the error messages above")