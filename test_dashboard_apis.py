#!/usr/bin/env python3
"""
Test the running dashboard APIs
"""

import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Running Dashboard APIs")
    print("=" * 40)
    
    # Test 1: Basic API test
    try:
        response = requests.get(f"{base_url}/api/test", timeout=10)
        print(f"✅ API Test: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ API Test failed: {e}")
    
    # Test 2: News API
    try:
        response = requests.get(f"{base_url}/api/news", timeout=15)
        print(f"📰 News API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Articles: {len(data.get('items', []))}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ News API failed: {e}")
    
    # Test 3: Sentiment Analysis with positive text
    try:
        data = {"text": "I love this amazing product! It works perfectly."}
        response = requests.post(f"{base_url}/api/analyze", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=30)
        print(f"😊 Positive Sentiment: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Sentiment: {result.get('sentiment')}")
            print(f"   Confidence: {result.get('confidence')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Positive sentiment failed: {e}")
    
    # Test 4: Sentiment Analysis with negative text
    try:
        data = {"text": "I hate this terrible product! It's broken and awful."}
        response = requests.post(f"{base_url}/api/analyze", 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=30)
        print(f"😞 Negative Sentiment: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Sentiment: {result.get('sentiment')}")
            print(f"   Confidence: {result.get('confidence')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Negative sentiment failed: {e}")

if __name__ == '__main__':
    test_api()
