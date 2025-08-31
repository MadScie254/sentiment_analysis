#!/usr/bin/env python3
"""
Quick test to debug the issues
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_components():
    print("🔧 Testing Components...")
    
    # Test 1: News Aggregator
    try:
        from real_news_aggregator import comprehensive_news_aggregator
        articles = comprehensive_news_aggregator.get_comprehensive_news(5)
        print(f"✅ News Aggregator: {len(articles)} articles")
    except Exception as e:
        print(f"❌ News Aggregator error: {e}")
    
    # Test 2: Sentiment Analyzer  
    try:
        from real_sentiment_analyzer import real_sentiment_analyzer
        result = real_sentiment_analyzer.analyze_sentiment("I love this product!", 'vader')
        print(f"✅ Sentiment Analyzer: {result.sentiment}")
    except Exception as e:
        print(f"❌ Sentiment Analyzer error: {e}")
    
    # Test 3: API Keys
    print(f"\n🔑 API Keys:")
    print(f"Hugging Face: {'✅' if os.getenv('HUGGINGFACE_API_KEY') else '❌'}")
    print(f"NewsAPI: {'✅' if os.getenv('NEWSAPI_KEY') else '❌'}")

if __name__ == '__main__':
    test_components()
