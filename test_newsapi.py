#!/usr/bin/env python3
"""
Test NewsAPI specifically
"""
import os
import sys
import requests
from datetime import datetime, timedelta

# Add the multibagger_system to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'multibagger_system'))

def test_newsapi_direct():
    """Test NewsAPI directly"""
    print("🧪 Testing NewsAPI Direct Connection")
    print("=" * 50)
    
    # Load API key
    from dotenv import load_dotenv
    load_dotenv('multibagger_system/.env')
    
    news_api_key = os.getenv('NEWS_API_KEY')
    print(f"📰 NewsAPI Key: {news_api_key[:10]}..." if news_api_key else "❌ No NewsAPI key found")
    
    if not news_api_key:
        print("❌ NewsAPI key not found in environment")
        return False
    
    try:
        # Test NewsAPI directly
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'Reliance Industries India stock',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'apiKey': news_api_key
        }
        
        print(f"🔗 Making request to: {url}")
        print(f"📋 Query: {params['q']}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ Found {len(articles)} articles")
            
            if articles:
                print(f"📰 Sample headline: {articles[0].get('title', 'No title')}")
                print(f"📅 Published: {articles[0].get('publishedAt', 'No date')}")
                print(f"🏢 Source: {articles[0].get('source', {}).get('name', 'Unknown')}")
            
            return True
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ NewsAPI error: {error_data}")
            return False
            
    except Exception as e:
        print(f"❌ NewsAPI test failed: {e}")
        return False

def test_data_fetcher_newsapi():
    """Test NewsAPI through our data fetcher"""
    print("\n🔧 Testing NewsAPI through Data Fetcher")
    print("=" * 50)
    
    try:
        from data_sources.nse_data_fetcher import NSEDataFetcher
        
        fetcher = NSEDataFetcher()
        
        # Test news sentiment
        print("📰 Testing news sentiment for Reliance...")
        news_sentiment = fetcher.get_news_sentiment("RELIANCE.NS", "Reliance Industries")
        
        print(f"✅ Sentiment: {news_sentiment.get('sentiment', 'unknown')}")
        print(f"📊 Data source: {news_sentiment.get('data_source', 'unknown')}")
        print(f"📈 Sentiment score: {news_sentiment.get('sentiment_score', 'N/A')}")
        print(f"📰 Articles count: {news_sentiment.get('articles_count', 'N/A')}")
        
        if news_sentiment.get('recent_headlines'):
            print(f"📋 Headlines found: {len(news_sentiment['recent_headlines'])}")
            for i, headline in enumerate(news_sentiment['recent_headlines'][:2]):
                print(f"   {i+1}. {headline}")
        
        if news_sentiment.get('error'):
            print(f"❌ Error: {news_sentiment['error']}")
            return False
        
        return news_sentiment.get('data_source') == 'NewsAPI'
        
    except Exception as e:
        print(f"❌ Data fetcher test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing NewsAPI Integration")
    print("=" * 60)
    
    # Test direct API
    direct_success = test_newsapi_direct()
    
    # Test through data fetcher
    fetcher_success = test_data_fetcher_newsapi()
    
    if direct_success and fetcher_success:
        print("\n🎉 NewsAPI is working perfectly!")
    elif direct_success:
        print("\n⚠️  NewsAPI works directly but not through data fetcher")
    else:
        print("\n❌ NewsAPI connection failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if NewsAPI key is correct")
        print("   2. Verify internet connection")
        print("   3. Check NewsAPI rate limits")