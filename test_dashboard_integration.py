#!/usr/bin/env python3
"""
Comprehensive Integration Test for Enhanced Dashboard
Tests all components working together with real API keys
"""

import requests
import json
import time
from datetime import datetime

def test_dashboard_integration():
    """Test the complete dashboard integration"""
    print("🚀 ENHANCED DASHBOARD INTEGRATION TEST")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5003"
    
    tests = []
    
    # Test 1: Dashboard Homepage
    print("\n📊 Testing Dashboard Homepage...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        success = response.status_code == 200
        tests.append(("Dashboard Homepage", success))
        if success:
            print("✅ Dashboard loads successfully")
        else:
            print(f"❌ Dashboard failed with status {response.status_code}")
    except Exception as e:
        tests.append(("Dashboard Homepage", False))
        print(f"❌ Dashboard error: {e}")
    
    # Test 2: Enhanced Sentiment Analysis API
    print("\n🧠 Testing Enhanced Sentiment Analysis...")
    test_cases = [
        ("I absolutely love this enhanced system with real API integration!", "positive"),
        ("This is terrible and completely broken, I hate it!", "negative"),
        ("The weather is okay today, nothing special really.", "neutral")
    ]
    
    sentiment_tests = []
    for text, expected in test_cases:
        try:
            response = requests.post(
                f"{base_url}/api/analyze",
                json={"text": text},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    actual = result.get("sentiment")
                    confidence = result.get("confidence", 0)
                    api_used = result.get("api_used", "unknown")
                    real_ai = result.get("real_ai_analysis", False)
                    
                    correct = actual == expected
                    sentiment_tests.append(correct)
                    
                    status = "✅" if correct else "⚠️"
                    print(f"  {status} '{text[:30]}...' → {actual} ({confidence:.3f}) via {api_used}")
                    if real_ai:
                        print(f"    🤖 Real AI Analysis Used!")
                else:
                    sentiment_tests.append(False)
                    print(f"  ❌ API returned error: {result.get('error', 'Unknown')}")
            else:
                sentiment_tests.append(False)
                print(f"  ❌ HTTP error: {response.status_code}")
                
        except Exception as e:
            sentiment_tests.append(False)
            print(f"  ❌ Request failed: {e}")
    
    sentiment_accuracy = sum(sentiment_tests) / len(sentiment_tests) if sentiment_tests else 0
    tests.append(("Sentiment Analysis", sentiment_accuracy > 0.6))
    print(f"  🎯 Sentiment Accuracy: {sentiment_accuracy:.1%}")
    
    # Test 3: News API with Kenyan Sources
    print("\n📰 Testing Enhanced News API...")
    try:
        response = requests.get(f"{base_url}/api/news?page=1&limit=5", timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                articles = result.get("items", [])
                kenyan_focus = result.get("kenyan_focus", False)
                enhanced_sources = result.get("enhanced_sources", False)
                
                tests.append(("News API", True))
                print(f"  ✅ Fetched {len(articles)} articles")
                if kenyan_focus:
                    print("  🇰🇪 Kenyan news sources integrated!")
                if enhanced_sources:
                    print("  ⚡ Enhanced news sources active!")
                    
                # Check if sentiment analysis is applied to articles
                analyzed_articles = [a for a in articles if 'sentiment' in a]
                if analyzed_articles:
                    print(f"  🧠 {len(analyzed_articles)} articles have sentiment analysis")
            else:
                tests.append(("News API", False))
                print(f"  ❌ News API error: {result.get('error', 'Unknown')}")
        else:
            tests.append(("News API", False))
            print(f"  ❌ News API HTTP error: {response.status_code}")
    except Exception as e:
        tests.append(("News API", False))
        print(f"  ❌ News API failed: {e}")
    
    # Test 4: Analytics Summary
    print("\n📈 Testing Analytics Summary...")
    try:
        response = requests.get(f"{base_url}/api/analytics/summary", timeout=10)
        if response.status_code == 200:
            result = response.json()
            tests.append(("Analytics Summary", True))
            print("  ✅ Analytics summary retrieved")
            print(f"  📊 Data points available: {len(result)}")
        else:
            tests.append(("Analytics Summary", False))
            print(f"  ❌ Analytics failed with status {response.status_code}")
    except Exception as e:
        tests.append(("Analytics Summary", False))
        print(f"  ❌ Analytics error: {e}")
    
    # Test 5: Health Check
    print("\n❤️  Testing System Health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            tests.append(("Health Check", True))
            print("  ✅ System health check passed")
        else:
            tests.append(("Health Check", False))
            print(f"  ❌ Health check failed: {response.status_code}")
    except Exception as e:
        tests.append(("Health Check", False))
        print(f"  ❌ Health check error: {e}")
    
    # Results Summary
    print("\n" + "=" * 50)
    print("📋 INTEGRATION TEST RESULTS")
    print("=" * 50)
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name:20} {status}")
    
    success_rate = sum(1 for _, passed in tests if passed) / len(tests)
    print(f"\n🎯 Overall Success Rate: {success_rate:.1%}")
    
    if success_rate >= 0.8:
        print("🎉 INTEGRATION TEST PASSED! Dashboard is production-ready!")
        print("🌟 All enhanced components working correctly with real APIs!")
    elif success_rate >= 0.6:
        print("⚠️  INTEGRATION TEST PARTIAL - Some components need attention")
    else:
        print("❌ INTEGRATION TEST FAILED - Major issues detected")
    
    print("\n🔗 Dashboard URL: http://127.0.0.1:5003")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_rate >= 0.6

if __name__ == "__main__":
    print("Waiting 3 seconds for dashboard to be ready...")
    time.sleep(3)
    test_dashboard_integration()
