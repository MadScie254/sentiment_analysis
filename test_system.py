#!/usr/bin/env python3
"""
Test suite for the sentiment analysis system
"""

import sys
import os
import json
import unittest
from typing import Dict, List

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp_engine import NLPEngine
from sentiment_engine import SentimentAnalyzer
from emotion_detector import EmotionDetector
from comment_classifier import CommentClassifier
from utils import TextPreprocessor, DataValidator

class TestSentimentEngine(unittest.TestCase):
    """Test the sentiment analysis engine"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        text = "I love this place! It's amazing and wonderful!"
        result = self.analyzer.analyze_sentiment(text)
        self.assertEqual(result["sentiment"], "positive")
        self.assertGreater(result["confidence"], 0.5)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        text = "This is terrible and I hate it. Very disappointed."
        result = self.analyzer.analyze_sentiment(text)
        self.assertEqual(result["sentiment"], "negative")
        self.assertGreater(result["confidence"], 0.5)
    
    def test_swahili_sentiment(self):
        """Test Swahili sentiment detection"""
        text = "Karibu Kenya! Hapa ni poa sana asante"
        result = self.analyzer.analyze_sentiment(text)
        self.assertEqual(result["sentiment"], "positive")
    
    def test_spam_detection(self):
        """Test spam detection"""
        spam_text = "Click here for free money! www.scam.com"
        result = self.analyzer.detect_spam(spam_text)
        self.assertTrue(result["is_spam"])
        
        normal_text = "Just sharing my thoughts about this video"
        result = self.analyzer.detect_spam(normal_text)
        self.assertFalse(result["is_spam"])

class TestEmotionDetector(unittest.TestCase):
    """Test the emotion detection system"""
    
    def setUp(self):
        self.detector = EmotionDetector()
    
    def test_joy_detection(self):
        """Test joy emotion detection"""
        text = "I'm so happy and excited! 😂😍"
        emotions = self.detector.detect_emotions(text)
        self.assertIn("joy", emotions)
    
    def test_anger_detection(self):
        """Test anger emotion detection"""
        text = "I'm so angry and frustrated! This is stupid!!!"
        emotions = self.detector.detect_emotions(text)
        self.assertIn("anger", emotions)
    
    def test_sarcasm_detection(self):
        """Test sarcasm detection"""
        text = "Oh great, another 'amazing' idea..."
        emotions = self.detector.detect_emotions(text)
        self.assertIn("sarcasm", emotions)
    
    def test_emoji_emotions(self):
        """Test emoji-based emotion detection"""
        text = "😭😭😭"
        emotions = self.detector.detect_emotions(text)
        self.assertIn("sadness", emotions)

class TestCommentClassifier(unittest.TestCase):
    """Test the comment classification system"""
    
    def setUp(self):
        self.classifier = CommentClassifier()
    
    def test_funny_classification(self):
        """Test funny comment classification"""
        text = "haha this is hilarious! 😂 I'm dying"
        result = self.classifier.classify_comment(text)
        self.assertEqual(result["tag"], "funny")
    
    def test_supportive_classification(self):
        """Test supportive comment classification"""
        text = "You're amazing! Keep going, we believe in you! ❤️"
        result = self.classifier.classify_comment(text)
        self.assertEqual(result["tag"], "supportive")
    
    def test_spam_classification(self):
        """Test spam comment classification"""
        text = "Free crypto! Click here: www.fakecrypto.com"
        result = self.classifier.classify_comment(text)
        self.assertEqual(result["tag"], "spam")
    
    def test_toxicity_detection(self):
        """Test toxicity detection"""
        toxic_text = "You're an idiot and I hate you"
        result = self.classifier.get_comment_toxicity(toxic_text)
        self.assertIn(result["toxicity_level"], ["moderate", "high"])
        
        safe_text = "Nice video, thanks for sharing"
        result = self.classifier.get_comment_toxicity(safe_text)
        self.assertEqual(result["toxicity_level"], "safe")

class TestNLPEngine(unittest.TestCase):
    """Test the main NLP engine"""
    
    def setUp(self):
        self.engine = NLPEngine()
    
    def test_video_analysis(self):
        """Test complete video analysis"""
        video_title = "Amazing day in Nairobi 🔥"
        video_description = "Had such a great time exploring the city!"
        comments = [
            "Love this! 😍",
            "This sucks",
            "lol so funny 😂",
            "Click here: www.spam.com"
        ]
        
        result = self.engine.analyze_video_data(video_title, video_description, comments)
        
        # Check structure
        self.assertIn("video_sentiment", result)
        self.assertIn("video_emotion", result)
        self.assertIn("comments", result)
        self.assertIn("summary", result)
        
        # Check comments analysis
        self.assertEqual(len(result["comments"]), 4)
        for comment in result["comments"]:
            self.assertIn("text", comment)
            self.assertIn("sentiment", comment)
            self.assertIn("emotion", comment)
            self.assertIn("tag", comment)
    
    def test_quick_analyze(self):
        """Test quick text analysis"""
        text = "This is amazing! I love it so much 😍"
        result = self.engine.quick_analyze(text)
        
        self.assertIn("sentiment", result)
        self.assertIn("emotions", result)
        self.assertIn("tag", result)
        self.assertEqual(result["sentiment"], "positive")

class TestTextPreprocessor(unittest.TestCase):
    """Test the text preprocessing utilities"""
    
    def setUp(self):
        self.preprocessor = TextPreprocessor()
    
    def test_emoji_processing(self):
        """Test emoji to text conversion"""
        text = "I'm happy 😊 and excited 🎉"
        cleaned = self.preprocessor.clean_text(text)
        self.assertIn("smiling", cleaned.lower())
    
    def test_slang_expansion(self):
        """Test slang and abbreviation expansion"""
        text = "lol that's so poa bro"
        cleaned = self.preprocessor.clean_text(text)
        self.assertIn("laugh", cleaned.lower())
        self.assertIn("cool", cleaned.lower())
    
    def test_feature_extraction(self):
        """Test feature extraction"""
        text = "OMG this is AMAZING!!! 😍🔥"
        features = self.preprocessor.extract_features(text)
        
        self.assertGreater(features["emoji_count"], 0)
        self.assertGreater(features["exclamation_count"], 0)
        self.assertGreater(features["caps_ratio"], 0)
    
    def test_language_detection(self):
        """Test language mixing detection"""
        text = "Hello how are you na habari yako"
        result = self.preprocessor.detect_language_mix(text)
        
        self.assertGreater(result["english"], 0)
        self.assertGreater(result["swahili"], 0)

class TestDataValidator(unittest.TestCase):
    """Test data validation"""
    
    def test_text_validation(self):
        """Test text input validation"""
        # Valid text
        valid, msg = DataValidator.validate_text_input("Hello world")
        self.assertTrue(valid)
        
        # Empty text
        valid, msg = DataValidator.validate_text_input("")
        self.assertFalse(valid)
        
        # Too long text
        long_text = "a" * 6000
        valid, msg = DataValidator.validate_text_input(long_text)
        self.assertFalse(valid)
    
    def test_comment_list_validation(self):
        """Test comment list validation"""
        # Valid comments
        valid, msg = DataValidator.validate_comment_list(["comment1", "comment2"])
        self.assertTrue(valid)
        
        # Empty list
        valid, msg = DataValidator.validate_comment_list([])
        self.assertFalse(valid)
        
        # Too many comments
        many_comments = ["comment"] * 200
        valid, msg = DataValidator.validate_comment_list(many_comments)
        self.assertFalse(valid)

def run_example_test():
    """Run the example from the user prompt"""
    print("\n🧪 Running Example Analysis Test")
    print("=" * 50)
    
    engine = NLPEngine()
    
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
    
    # Format as requested
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
    
    print("📊 Analysis Result:")
    print(json.dumps(formatted_result, indent=2, ensure_ascii=False))
    
    # Verify expected results
    assert result["video_sentiment"] in ["positive", "mixed"], "Video sentiment should be positive or mixed"
    assert len(result["comments"]) == 5, "Should analyze all 5 comments"
    
    # Check specific comment classifications
    spam_comment = next((c for c in result["comments"] if "spam" in c["text"].lower()), None)
    assert spam_comment and spam_comment["tag"] == "spam", "Should detect spam comment"
    
    supportive_comment = next((c for c in result["comments"] if "karibu" in c["text"].lower()), None)
    assert supportive_comment and supportive_comment["tag"] in ["supportive", "funny"], "Should classify Karibu comment appropriately"
    
    print("✅ All example tests passed!")

if __name__ == "__main__":
    print("🚀 Sentiment Analysis System - Test Suite")
    print("=" * 50)
    
    # Run example test first
    run_example_test()
    
    # Run unit tests
    print("\n🧪 Running Unit Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestCommentClassifier))
    suite.addTests(loader.loadTestsFromTestCase(TestNLPEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestTextPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed! System is ready to use.")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
    print("\n📝 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
