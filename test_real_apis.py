#!/usr/bin/env python3
"""
Test script for real API components
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sentiment_analyzer():
    """Test the real sentiment analyzer"""
    try:
        from real_sentiment_analyzer import real_sentiment_analyzer
        
        test_text = "I love this product! It's amazing and works perfectly."
        print(f"Testing sentiment analysis with: '{test_text}'")
        
        result = real_sentiment_analyzer.analyze_sentiment(test_text, 'roberta')
        print(f"✅ Sentiment: {result.sentiment}")
        print(f"✅ Confidence: {result.confidence}")
        print(f"✅ Model: {result.model_used}")
        
        return True
    except Exception as e:
        print(f"❌ Sentiment analyzer test failed: {e}")
        return False

def test_news_aggregator():
    """Test the comprehensive news aggregator"""
    try:
        from real_news_aggregator import comprehensive_news_aggregator
        
        print("Testing news aggregator...")
        articles = comprehensive_news_aggregator.get_trending_news(5)
        
        print(f"✅ Fetched {len(articles)} articles")
        for i, article in enumerate(articles[:3]):
            print(f"  {i+1}. {article.get('title', 'No title')[:50]}...")
            print(f"     Source: {article.get('source', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ News aggregator test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Real API Components")
    print("=" * 40)
    
    # Check API keys
    print("\n📋 Checking API Keys:")
    keys_to_check = [
        'HUGGINGFACE_API_KEY',
        'NEWSAPI_KEY', 
        'GNEWS_API_KEY',
        'CURRENTS_API_KEY',
        'TWITTER_API_KEY'
    ]
    
    for key in keys_to_check:
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: {'*' * 10}...{value[-4:]}")
        else:
            print(f"❌ {key}: Not found")
    
    # Test components
    print("\n🔬 Testing Components:")
    
    sentiment_ok = test_sentiment_analyzer()
    news_ok = test_news_aggregator()
    
    print("\n📊 Test Results:")
    print(f"Sentiment Analyzer: {'✅ PASS' if sentiment_ok else '❌ FAIL'}")
    print(f"News Aggregator: {'✅ PASS' if news_ok else '❌ FAIL'}")
    
    if sentiment_ok and news_ok:
        print("\n🎉 All tests passed! Real APIs are working.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
