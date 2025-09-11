#!/usr/bin/env python3

from real_sentiment_analyzer import real_sentiment_analyzer
import time

def test_real_analyzer():
    """Test the real sentiment analyzer with various inputs"""
    
    test_cases = [
        'I love this product! It works amazingly well.',
        'This is terrible and I hate it completely.',
        'The weather is okay today, nothing special.',
        'This movie was absolutely fantastic and amazing!',
        'I am feeling quite neutral about this situation.'
    ]
    
    print("🧪 Testing Real Sentiment Analyzer")
    print("=" * 50)
    
    for i, text in enumerate(test_cases):
        try:
            result = real_sentiment_analyzer.analyze_sentiment(text)
            print(f'{i+1}. "{text[:45]}..."')
            print(f'   -> {result.sentiment} ({result.confidence:.3f}) [{result.method}]')
            print(f'   -> Scores: {result.scores}')
            print()
            time.sleep(0.1)
        except Exception as e:
            print(f'{i+1}. ERROR: {e}')
    
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_real_analyzer()
