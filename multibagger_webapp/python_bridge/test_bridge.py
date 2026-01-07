#!/usr/bin/env python3
"""
Test script for the Enhanced Python Bridge Server
Tests all endpoints and functionality
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_STOCKS = ["RELIANCE.NS", "TCS.NS"]
TEST_SINGLE_STOCK = "TANLA.NS"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return True, response.json() if response.content else {}
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False, {}
            
    except requests.exceptions.Timeout:
        print(f"⏰ {method} {endpoint} - Timeout (30s)")
        return False, {}
    except requests.exceptions.ConnectionError:
        print(f"🔌 {method} {endpoint} - Connection Error (Server not running?)")
        return False, {}
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False, {}

def main():
    """Run comprehensive tests"""
    print("🧪 ENHANCED PYTHON BRIDGE SERVER TESTS")
    print("=" * 60)
    print(f"🎯 Target: {BASE_URL}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    # 1. Health Checks
    print("🏥 HEALTH & STATUS TESTS")
    print("-" * 30)
    
    success, data = test_endpoint('GET', '/health')
    results.append(('Simple Health Check', success))
    
    success, data = test_endpoint('GET', '/api/health')
    results.append(('Comprehensive Health Check', success))
    if success:
        print(f"   System Available: {data.get('system_available')}")
        print(f"   System Initialized: {data.get('system_initialized')}")
        print(f"   Environment Variables: {sum(data.get('environment_variables', {}).values())}/6 set")
    
    success, data = test_endpoint('GET', '/api/system-status')
    results.append(('System Status', success))
    if success and 'status' in data:
        print(f"   Status: {data.get('status')}")
        print(f"   Agents: {len(data.get('agents', {}))}")
    
    print()
    
    # 2. System Initialization
    print("🚀 INITIALIZATION TESTS")
    print("-" * 30)
    
    success, data = test_endpoint('POST', '/api/initialize')
    results.append(('System Initialization', success))
    if success:
        print(f"   Success: {data.get('success')}")
        print(f"   Message: {data.get('message')}")
    
    print()
    
    # 3. Configuration & Data
    print("⚙️  CONFIGURATION & DATA TESTS")
    print("-" * 30)
    
    success, data = test_endpoint('GET', '/api/config')
    results.append(('Configuration', success))
    if success:
        print(f"   Agent Weights: {len(data.get('agent_weights', {}))}")
        print(f"   Thresholds: {len(data.get('thresholds', {}))}")
    
    success, data = test_endpoint('GET', '/api/predefined-sets')
    results.append(('Predefined Sets', success))
    if success:
        print(f"   Stock Sets: {len(data.get('sets', []))}")
    
    success, data = test_endpoint('GET', '/api/trending-stocks')
    results.append(('Trending Stocks', success))
    if success:
        print(f"   Categories: {len(data)}")
    
    success, data = test_endpoint('GET', '/api/stock-list')
    results.append(('Stock List', success))
    if success:
        print(f"   Available Stocks: {data.get('count', 0)}")
    
    print()
    
    # 4. Stock Data
    print("📊 STOCK DATA TESTS")
    print("-" * 30)
    
    success, data = test_endpoint('GET', f'/api/stock-data/{TEST_SINGLE_STOCK}')
    results.append(('Individual Stock Data', success))
    if success:
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Data Components: {len([k for k in data.keys() if k != 'symbol'])}")
    
    print()
    
    # 5. Analysis Tests
    print("🔍 ANALYSIS TESTS")
    print("-" * 30)
    
    # Single stock analysis
    success, data = test_endpoint('POST', '/api/analyze-single', {'symbol': TEST_SINGLE_STOCK})
    results.append(('Single Stock Analysis', success))
    if success:
        multibaggers = data.get('high_probability_multibaggers', [])
        watchlist = data.get('early_watchlist', [])
        print(f"   High Probability: {len(multibaggers)}")
        print(f"   Watchlist: {len(watchlist)}")
        if multibaggers:
            stock = multibaggers[0]
            print(f"   Top Result: {stock.get('symbol')} ({stock.get('multibagger_probability', 0):.1%})")
    
    # Multiple stocks analysis
    print(f"\n   Testing multiple stocks: {TEST_STOCKS}")
    start_time = time.time()
    success, data = test_endpoint('POST', '/api/analyze', {'stocks': TEST_STOCKS})
    analysis_time = time.time() - start_time
    results.append(('Multiple Stock Analysis', success))
    if success:
        multibaggers = data.get('high_probability_multibaggers', [])
        watchlist = data.get('early_watchlist', [])
        print(f"   Analysis Time: {analysis_time:.1f}s")
        print(f"   High Probability: {len(multibaggers)}")
        print(f"   Watchlist: {len(watchlist)}")
        print(f"   Total Analyzed: {data.get('analysis_summary', {}).get('total_stocks_analyzed', 0)}")
    
    print()
    
    # 6. History & Misc
    print("📈 HISTORY & MISC TESTS")
    print("-" * 30)
    
    success, data = test_endpoint('GET', '/api/analysis-history')
    results.append(('Analysis History', success))
    if success:
        print(f"   Recent Analyses: {len(data.get('recent_analyses', []))}")
        print(f"   Success Rate: {data.get('success_rate', 0)}%")
    
    print()
    
    # 7. Error Handling Tests
    print("🚨 ERROR HANDLING TESTS")
    print("-" * 30)
    
    # Test invalid endpoints
    success, data = test_endpoint('GET', '/api/nonexistent', expected_status=404)
    results.append(('404 Error Handling', success))
    
    # Test invalid methods
    success, data = test_endpoint('DELETE', '/api/health', expected_status=405)
    results.append(('405 Error Handling', success))
    
    # Test invalid data
    success, data = test_endpoint('POST', '/api/analyze', {'invalid': 'data'}, expected_status=400)
    results.append(('400 Error Handling', success))
    
    print()
    
    # Summary
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
    print(f"❌ Failed: {total - passed}/{total}")
    print()
    
    if success_rate >= 80:
        print("🎉 PYTHON BRIDGE SERVER IS READY FOR DEPLOYMENT!")
    elif success_rate >= 60:
        print("⚠️  Python Bridge Server has some issues but is mostly functional")
    else:
        print("🚨 Python Bridge Server has significant issues")
    
    print()
    print("Failed Tests:")
    for test_name, success in results:
        if not success:
            print(f"   ❌ {test_name}")
    
    print(f"\n⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()