#!/usr/bin/env python3
"""
Test API endpoints to verify fixes
"""

import requests
import json

def test_dashboard_endpoints():
    print("🔧 Testing Dashboard Endpoints")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Test sentiment analysis with negative text
    print("\n➖ Testing Negative Sentiment Analysis:")
    try:
        data = {"text": "I hate this terrible product! It's awful and completely broken!"}
        response = requests.post(f"{base_url}/api/analyze", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Sentiment: {result.get('sentiment')}")
            print(f"   🎯 Confidence: {result.get('confidence')}")
            print(f"   🤖 Model: {result.get('model_used')}")
            
            # Check if negative sentiment is correctly identified
            if result.get('sentiment') == 'negative':
                print(f"   ✅ Correctly identified as NEGATIVE")
            else:
                print(f"   ❌ ERROR: Should be negative but got {result.get('sentiment')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   📝 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test sentiment analysis with positive text
    print("\n➕ Testing Positive Sentiment Analysis:")
    try:
        data = {"text": "I love this amazing product! It works perfectly and makes me so happy!"}
        response = requests.post(f"{base_url}/api/analyze", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Sentiment: {result.get('sentiment')}")
            print(f"   🎯 Confidence: {result.get('confidence')}")
            print(f"   🤖 Model: {result.get('model_used')}")
            
            # Check if positive sentiment is correctly identified
            if result.get('sentiment') == 'positive':
                print(f"   ✅ Correctly identified as POSITIVE")
            else:
                print(f"   ❌ ERROR: Should be positive but got {result.get('sentiment')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test news endpoint
    print("\n📰 Testing News Endpoint:")
    try:
        response = requests.get(f"{base_url}/api/news?limit=5", timeout=15)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📰 Articles: {len(result.get('items', []))}")
            print(f"   📡 Sources: {result.get('sources_used', [])}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == '__main__':
    test_dashboard_endpoints()
