#!/usr/bin/env python3
"""
Quick API Test for Enhanced Dashboard
"""

import requests
import json

def test_sentiment_api():
    """Test the enhanced sentiment analysis API"""
    print("🧠 Testing Enhanced Sentiment Analysis API...")
    
    test_cases = [
        "I absolutely love this enhanced sentiment analysis system!",
        "This is terrible and disappointing.",
        "The weather is okay today."
    ]
    
    for i, text in enumerate(test_cases, 1):
        try:
            response = requests.post(
                'http://127.0.0.1:5003/api/analyze',
                json={'text': text},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Test {i}: '{text[:30]}...'")
                print(f"     Sentiment: {result.get('sentiment')} ({result.get('confidence', 0):.3f})")
                print(f"     Method: {result.get('api_used')} | Real AI: {result.get('real_ai_analysis')}")
            else:
                print(f"  ❌ Test {i} failed: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Test {i} error: {e}")

def test_news_api():
    """Test the news API"""
    print("\n📰 Testing Enhanced News API...")
    
    try:
        response = requests.get('http://127.0.0.1:5003/api/news?page=1&limit=3', timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ News API working")
            print(f"     Articles: {len(result.get('items', []))}")
            print(f"     Sources: {', '.join(result.get('sources_used', []))}")
            print(f"     Enhanced: {result.get('enhanced_sources', False)}")
        else:
            print(f"  ❌ News API failed: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ News API error: {e}")

def test_health_api():
    """Test the health API"""
    print("\n❤️ Testing Health API...")
    
    try:
        response = requests.get('http://127.0.0.1:5003/api/health', timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Health API working")
            print(f"     Status: {result.get('status')}")
        else:
            print(f"  ❌ Health API failed: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Health API error: {e}")

if __name__ == "__main__":
    print("🚀 ENHANCED DASHBOARD API TEST")
    print("=" * 40)
    
    test_sentiment_api()
    test_news_api()
    test_health_api()
    
    print("\n🎉 API Testing Complete!")
