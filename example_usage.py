#!/usr/bin/env python3
"""
Example usage of the sentiment analysis system
"""

import json
from nlp_engine import NLPEngine

def main():
    print("🚀 Sentiment Analysis System - Example Usage")
    print("=" * 50)
    
    # Initialize the NLP engine
    engine = NLPEngine()
    
    # Example 1: Quick text analysis
    print("\n📝 Example 1: Quick Text Analysis")
    text = "I love this place! It's amazing 😍"
    result = engine.quick_analyze(text)
    print(f"Text: {text}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Example 2: Video data analysis (from the prompt)
    print("\n📺 Example 2: Video Data Analysis")
    video_title = "My first day in Nairobi 🚖🔥"
    video_description = "Trying out local food and matatus, what an adventure!"
    comments = [
        "😂😂 bro you look lost but it's vibes",
        "This city will eat you alive, trust me.",
        "Matatu rides >>> Uber any day",
        "Spam link: www.fakecrypto.com",
        "Karibu Kenya! We love you ❤️"
    ]
    
    result = engine.analyze_video_data(video_title, video_description, comments)
    
    # Format as requested in the prompt
    formatted_result = {
        "video_sentiment": result["video_sentiment"],
        "video_emotion": result["video_emotion"],
        "comments": [
            {
                "text": comment["text"],
                "sentiment": comment["sentiment"],
                "emotion": comment["emotion"],
                "tag": comment["tag"]
            }
            for comment in result["comments"]
        ]
    }
    
    print("Result:")
    print(json.dumps(formatted_result, indent=2, ensure_ascii=False))
    
    # Example 3: Batch comment analysis
    print("\n💬 Example 3: Batch Comment Analysis")
    test_comments = [
        "This is hilarious! 😂😂😂",
        "You're amazing, keep it up! ❤️",
        "This is terrible and stupid",
        "Free money here: www.scam.com",
        "Very insightful analysis, thanks for sharing your perspective"
    ]
    
    batch_results = engine.batch_analyze_comments(test_comments)
    for i, result in enumerate(batch_results):
        print(f"Comment {i+1}: {result['tag']} ({result['sentiment']})")
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()
