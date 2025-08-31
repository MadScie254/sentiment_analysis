#!/usr/bin/env python3
"""
Simple test for real APIs
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_news_api():
    """Test NewsAPI"""
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("❌ NewsAPI key not found")
        return False
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ NewsAPI: Fetched {len(articles)} articles")
            if articles:
                print(f"   Sample: {articles[0]['title'][:50]}...")
            return True
        else:
            print(f"❌ NewsAPI error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ NewsAPI exception: {e}")
        return False

def test_huggingface_api():
    """Test Hugging Face API"""
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        print("❌ Hugging Face API key not found")
        return False
    
    try:
        url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"inputs": "I love this amazing product!"}
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                sentiment_data = result[0]
                print(f"✅ Hugging Face API: Working")
                print(f"   Sample result: {sentiment_data}")
                return True
        else:
            print(f"❌ Hugging Face API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Hugging Face API exception: {e}")
        return False

def main():
    print("🧪 Simple API Test")
    print("=" * 30)
    
    news_ok = test_news_api()
    hf_ok = test_huggingface_api()
    
    print("\n📊 Results:")
    print(f"NewsAPI: {'✅ PASS' if news_ok else '❌ FAIL'}")
    print(f"Hugging Face: {'✅ PASS' if hf_ok else '❌ FAIL'}")
    
    if news_ok and hf_ok:
        print("\n🎉 All APIs working!")
    else:
        print("\n⚠️ Some APIs failed")

if __name__ == '__main__':
    main()
