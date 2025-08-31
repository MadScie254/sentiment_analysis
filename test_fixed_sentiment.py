#!/usr/bin/env python3
"""
Test the fixed sentiment analyzer
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sentiment_analyzer():
    print("🧪 Testing Fixed Sentiment Analyzer")
    print("=" * 40)
    
    try:
        from real_sentiment_analyzer import real_sentiment_analyzer
        
        # Test positive sentiment
        print("\n➕ Testing Positive Sentiment:")
        result = real_sentiment_analyzer.analyze_sentiment("I love this amazing product! It works perfectly and makes me so happy!", 'roberta')
        print(f"   Text: {result.text[:50]}...")
        print(f"   Sentiment: {result.sentiment}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Model: {result.model_used}")
        
        # Test negative sentiment
        print("\n➖ Testing Negative Sentiment:")
        result = real_sentiment_analyzer.analyze_sentiment("I hate this terrible product! It's broken, awful, and completely useless!", 'roberta')
        print(f"   Text: {result.text[:50]}...")
        print(f"   Sentiment: {result.sentiment}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Model: {result.model_used}")
        
        # Test neutral sentiment
        print("\n⚖️ Testing Neutral Sentiment:")
        result = real_sentiment_analyzer.analyze_sentiment("This is a product. It has features.", 'roberta')
        print(f"   Text: {result.text[:50]}...")
        print(f"   Sentiment: {result.sentiment}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Model: {result.model_used}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing sentiment analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_sentiment_analyzer()
