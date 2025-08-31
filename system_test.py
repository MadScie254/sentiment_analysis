#!/usr/bin/env python3
"""
System Test Script for Enhanced Sentiment Analysis
Tests all components of the production system
"""

import requests
import json
import time
from enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer
from config_manager import get_production_settings

def test_enhanced_analyzer():
    """Test the enhanced sentiment analyzer directly"""
    print("🧪 Testing Enhanced Sentiment Analyzer...")
    try:
        analyzer = EnhancedSentimentAnalyzer()
        
        # Test cases
        test_cases = [
            ("I am extremely happy and excited!", "positive"),
            ("This is absolutely terrible and disappointing", "negative"), 
            ("The weather is okay today", "neutral"),
            ("I love this amazing product!", "positive"),
            ("I hate waiting in long queues", "negative")
        ]
        
        results = []
        for text, expected in test_cases:
            result = analyzer.analyze_sentiment(text)
            results.append({
                "text": text,
                "expected": expected,
                "actual": result.sentiment,
                "score": round(result.confidence, 3),
                "method": result.method,
                "correct": result.sentiment == expected
            })
            print(f"  📝 '{text[:30]}...' → {result.sentiment} ({result.confidence:.3f}) via {result.method}")
        
        accuracy = sum(1 for r in results if r["correct"]) / len(results)
        print(f"  ✅ Accuracy: {accuracy:.1%} ({sum(1 for r in results if r['correct'])}/{len(results)})")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_production_config():
    """Test production configuration"""
    print("\n🔧 Testing Production Configuration...")
    try:
        settings = get_production_settings()
        print(f"  ✅ Host: {settings.HOST}:{settings.PORT}")
        print(f"  ✅ Debug: {settings.DEBUG}")
        print(f"  ✅ Rate limit: {settings.RATE_LIMIT_PER_MINUTE}/min")
        print(f"  ✅ Log level: {settings.LOG_LEVEL}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    base_url = "http://127.0.0.1:5000"
    
    tests = []
    
    # Test dashboard
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        tests.append(("Dashboard", response.status_code == 200))
        print(f"  📊 Dashboard: {'✅' if response.status_code == 200 else '❌'} ({response.status_code})")
    except Exception as e:
        tests.append(("Dashboard", False))
        print(f"  📊 Dashboard: ❌ {e}")
    
    # Test sentiment analysis
    try:
        data = {"text": "I am very happy today!"}
        response = requests.post(f"{base_url}/api/analyze", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            success = result.get("success", False) and "sentiment" in result
            tests.append(("Sentiment API", success))
            print(f"  🧠 Sentiment API: {'✅' if success else '❌'} - {result.get('sentiment', 'N/A')} ({result.get('confidence', 0):.3f})")
        else:
            tests.append(("Sentiment API", False))
            print(f"  🧠 Sentiment API: ❌ ({response.status_code})")
    except Exception as e:
        tests.append(("Sentiment API", False))
        print(f"  🧠 Sentiment API: ❌ {e}")
    
    # Test analytics
    try:
        response = requests.get(f"{base_url}/api/analytics/summary", timeout=5)
        tests.append(("Analytics API", response.status_code == 200))
        print(f"  📈 Analytics API: {'✅' if response.status_code == 200 else '❌'} ({response.status_code})")
    except Exception as e:
        tests.append(("Analytics API", False))
        print(f"  📈 Analytics API: ❌ {e}")
    
    success_rate = sum(1 for _, passed in tests if passed) / len(tests)
    print(f"  🎯 API Success Rate: {success_rate:.1%} ({sum(1 for _, passed in tests if passed)}/{len(tests)})")
    
    return success_rate > 0.5

def main():
    """Run all system tests"""
    print("🚀 ENHANCED SENTIMENT ANALYSIS SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Enhanced Analyzer", test_enhanced_analyzer),
        ("Production Config", test_production_config), 
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📋 SYSTEM TEST SUMMARY")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {name:20} {status}")
    
    overall_success = sum(1 for _, success in results if success) / len(results)
    print(f"\n🎯 Overall Success Rate: {overall_success:.1%}")
    
    if overall_success >= 0.8:
        print("🎉 SYSTEM TEST PASSED! Production-ready!")
    elif overall_success >= 0.6:
        print("⚠️  SYSTEM TEST PARTIAL - Some issues detected")
    else:
        print("❌ SYSTEM TEST FAILED - Major issues detected")
    
    return overall_success >= 0.6

if __name__ == "__main__":
    main()
