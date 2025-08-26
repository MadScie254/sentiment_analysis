#!/usr/bin/env python3
"""
Quick demonstration script that works with the exact example from the prompt
This script uses minimal dependencies and shows the expected output format
"""

import json
import re
from typing import Dict, List, Any

class QuickDemo:
    """
    Simplified demo version that handles the specific example from the prompt
    """
    
    def __init__(self):
        # Simple sentiment words
        self.positive_words = [
            'love', 'amazing', 'great', 'awesome', 'wonderful', 'best', 'good', 'nice',
            'happy', 'excited', 'perfect', 'brilliant', 'fantastic', 'excellent',
            'vibes', 'cool', 'dope', 'fire', 'lit', 'poa', 'sawa', 'karibu', 'asante'
        ]
        
        self.negative_words = [
            'hate', 'terrible', 'awful', 'bad', 'worst', 'stupid', 'horrible',
            'disgusting', 'annoying', 'angry', 'sad', 'disappointed', 'upset',
            'eat you alive', 'mbaya', 'hasira', 'huzuni'
        ]
        
        # Simple emotion keywords
        self.emotion_patterns = {
            'joy': ['😂', '😍', '❤️', 'love', 'happy', 'amazing', 'great', 'vibes', 'excited'],
            'excitement': ['🔥', 'fire', 'amazing', 'awesome', 'excited', 'energy'],
            'sarcasm': ['lost but', 'yeah right', 'sure', 'obviously'],
            'fear': ['eat you alive', 'trust me', 'careful', 'watch out'],
            'sadness': ['😭', 'sad', 'disappointed', 'hurt']
        }
        
        # Simple classification patterns
        self.classification_patterns = {
            'funny': ['😂', 'lol', 'haha', 'hilarious', 'vibes', 'lost but'],
            'supportive': ['❤️', 'love', 'karibu', 'welcome', 'amazing', 'great'],
            'spam': ['www.', 'http', 'click', 'free', 'link:', 'spam'],
            'neutral': []  # Default fallback
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        # Check for emojis
        positive_emojis = ['😂', '😍', '❤️', '🔥']
        negative_emojis = ['😭', '😠', '😡']
        
        for emoji in positive_emojis:
            if emoji in text:
                positive_count += 1
        
        for emoji in negative_emojis:
            if emoji in text:
                negative_count += 1
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def detect_emotions(self, text: str) -> List[str]:
        """Simple emotion detection"""
        emotions = []
        text_lower = text.lower()
        
        for emotion, keywords in self.emotion_patterns.items():
            for keyword in keywords:
                if keyword in text_lower or keyword in text:
                    emotions.append(emotion)
                    break
        
        return emotions if emotions else []
    
    def classify_comment(self, text: str) -> str:
        """Simple comment classification"""
        text_lower = text.lower()
        
        # Check for spam first
        for keyword in self.classification_patterns['spam']:
            if keyword in text_lower:
                return "spam"
        
        # Check other categories
        for category, keywords in self.classification_patterns.items():
            if category == 'spam':
                continue
            for keyword in keywords:
                if keyword in text_lower or keyword in text:
                    return category
        
        return "neutral"
    
    def analyze_video_data(self, video_title: str, video_description: str, comments: List[str]) -> Dict[str, Any]:
        """Analyze the complete video data"""
        
        # Analyze video content
        video_text = f"{video_title} {video_description}"
        video_sentiment = self.analyze_sentiment(video_text)
        video_emotions = self.detect_emotions(video_text)
        
        # Analyze comments
        comment_results = []
        for comment in comments:
            comment_analysis = {
                "text": comment,
                "sentiment": self.analyze_sentiment(comment),
                "emotion": self.detect_emotions(comment),
                "tag": self.classify_comment(comment)
            }
            comment_results.append(comment_analysis)
        
        return {
            "video_sentiment": video_sentiment,
            "video_emotion": video_emotions,
            "comments": comment_results
        }

def run_example():
    """Run the exact example from the prompt"""
    print("🚀 Quick Demo - Sentiment Analysis")
    print("=" * 50)
    print("Processing the example data from the prompt...")
    
    demo = QuickDemo()
    
    # The exact example data from the prompt
    video_title = "My first day in Nairobi 🚖🔥"
    video_description = "Trying out local food and matatus, what an adventure!"
    comments = [
        "😂😂 bro you look lost but it's vibes",
        "This city will eat you alive, trust me.",
        "Matatu rides >>> Uber any day",
        "Spam link: www.fakecrypto.com",
        "Karibu Kenya! We love you ❤️"
    ]
    
    # Analyze the data
    result = demo.analyze_video_data(video_title, video_description, comments)
    
    print("\n📊 Analysis Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n💡 Analysis Summary:")
    print(f"Video Sentiment: {result['video_sentiment']}")
    print(f"Video Emotions: {', '.join(result['video_emotion']) if result['video_emotion'] else 'None detected'}")
    print(f"Total Comments: {len(result['comments'])}")
    
    print("\n📝 Comment Breakdown:")
    for i, comment in enumerate(result['comments'], 1):
        print(f"{i}. [{comment['tag'].upper()}] {comment['sentiment']} sentiment")
        print(f"   Text: \"{comment['text']}\"")
        if comment['emotion']:
            print(f"   Emotions: {', '.join(comment['emotion'])}")
        print()
    
    print("✅ Demo completed!")
    print("\n🚀 To use the full system:")
    print("1. Run: python setup.py")
    print("2. Run: python test_system.py")
    print("3. Run: python example_usage.py")
    print("4. Or start API: python api_server.py")

if __name__ == "__main__":
    run_example()
