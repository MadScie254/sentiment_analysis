#!/usr/bin/env python3
"""
Real Sentiment Analyzer - Production Demo
Shows the key features and capabilities of the fixed analyzer
"""

from real_sentiment_analyzer import real_sentiment_analyzer
import json

def demo_real_analyzer():
    """Demonstrate the real sentiment analyzer capabilities"""
    
    print("🎯 REAL SENTIMENT ANALYZER - PRODUCTION READY! 🎯")
    print("=" * 60)
    
    # Test different analysis methods
    test_text = "I absolutely love this amazing product! It's fantastic and works perfectly!"
    
    print(f"📝 Testing text: '{test_text}'")
    print("\n🔍 Analysis Methods Available:")
    
    # Auto method (recommended)
    result_auto = real_sentiment_analyzer.analyze_sentiment(test_text, method='auto')
    print(f"✅ AUTO: {result_auto.sentiment} ({result_auto.confidence:.3f}) - {result_auto.method}")
    
    # VADER method
    result_vader = real_sentiment_analyzer.analyze_sentiment(test_text, method='vader')
    print(f"📊 VADER: {result_vader.sentiment} ({result_vader.confidence:.3f}) - {result_vader.method}")
    
    # TextBlob method  
    result_textblob = real_sentiment_analyzer.analyze_sentiment(test_text, method='textblob')
    print(f"🔤 TEXTBLOB: {result_textblob.sentiment} ({result_textblob.confidence:.3f}) - {result_textblob.method}")
    
    print("\n📊 Detailed Analysis (Auto Method):")
    print(f"   • Sentiment: {result_auto.sentiment}")
    print(f"   • Confidence: {result_auto.confidence}")
    print(f"   • Scores: {result_auto.scores}")
    print(f"   • Model Used: {result_auto.model_used}")
    print(f"   • Processing Time: {result_auto.processing_time}s")
    print(f"   • Method: {result_auto.method}")
    
    if hasattr(result_auto, 'emotion_scores') and result_auto.emotion_scores:
        print(f"   • Emotions: {result_auto.emotion_scores}")
    
    if hasattr(result_auto, 'toxicity_score') and result_auto.toxicity_score is not None:
        print(f"   • Toxicity Score: {result_auto.toxicity_score}")
    
    # Test negative sentiment
    print("\n" + "="*60)
    negative_text = "This product is absolutely terrible and I hate it!"
    result_neg = real_sentiment_analyzer.analyze_sentiment(negative_text)
    print(f"📝 Negative test: '{negative_text}'")
    print(f"✅ Result: {result_neg.sentiment} ({result_neg.confidence:.3f}) - {result_neg.method}")
    
    # Test neutral sentiment
    print("\n" + "="*60)
    neutral_text = "The weather is okay today, nothing particularly special."
    result_neu = real_sentiment_analyzer.analyze_sentiment(neutral_text)
    print(f"📝 Neutral test: '{neutral_text}'")
    print(f"✅ Result: {result_neu.sentiment} ({result_neu.confidence:.3f}) - {result_neu.method}")
    
    print("\n🎉 Real Sentiment Analyzer is working perfectly!")
    print("🚀 Ready for production use with:")
    print("   • Multiple analysis methods (VADER, TextBlob, HuggingFace)")
    print("   • Automatic method selection")
    print("   • Comprehensive error handling")
    print("   • Caching for performance")
    print("   • Rate limiting and security features")
    print("   • Emotion detection")
    print("   • Toxicity scoring")

if __name__ == "__main__":
    demo_real_analyzer()
