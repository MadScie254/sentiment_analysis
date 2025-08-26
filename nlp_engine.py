from typing import Dict, List, Optional, Union
import json
from datetime import datetime
from sentiment_engine import SentimentAnalyzer
from emotion_detector import EmotionDetector
from comment_classifier import CommentClassifier

class NLPEngine:
    """
    Main NLP Engine that orchestrates all sentiment analysis components
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_detector = EmotionDetector()
        self.comment_classifier = CommentClassifier()
    
    def analyze_video_data(self, video_title: str, video_description: str, 
                          comments: List[str]) -> Dict[str, any]:
        """
        Complete analysis of video data including title, description, and comments
        """
        # Analyze video content (title + description)
        video_text = f"{video_title} {video_description}".strip()
        video_analysis = self._analyze_video_content(video_text)
        
        # Analyze individual comments
        comment_analyses = []
        for comment_text in comments:
            if comment_text and comment_text.strip():
                comment_analysis = self._analyze_single_comment(comment_text)
                comment_analyses.append(comment_analysis)
        
        return {
            "video_sentiment": video_analysis["sentiment"],
            "video_emotion": video_analysis["emotions"],
            "video_confidence": video_analysis["confidence"],
            "comments": comment_analyses,
            "summary": self._generate_summary(video_analysis, comment_analyses),
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_video_content(self, video_text: str) -> Dict[str, any]:
        """Analyze video title and description"""
        if not video_text:
            return {
                "sentiment": "neutral",
                "emotions": [],
                "confidence": 0.0
            }
        
        # Get sentiment analysis
        sentiment_result = self.sentiment_analyzer.analyze_sentiment(video_text)
        
        # Get emotion detection
        emotions = self.emotion_detector.detect_emotions(video_text)
        
        return {
            "sentiment": sentiment_result["sentiment"],
            "emotions": emotions,
            "confidence": sentiment_result["confidence"],
            "sentiment_scores": sentiment_result["scores"]
        }
    
    def _analyze_single_comment(self, comment_text: str) -> Dict[str, any]:
        """Comprehensive analysis of a single comment"""
        if not comment_text or comment_text.strip() == "":
            return {
                "text": comment_text,
                "sentiment": "neutral",
                "emotion": [],
                "tag": "neutral",
                "confidence": 0.0
            }
        
        # Get sentiment analysis
        sentiment_result = self.sentiment_analyzer.analyze_sentiment(comment_text)
        
        # Get emotion detection
        emotions = self.emotion_detector.detect_emotions(comment_text)
        
        # Get comment classification
        classification_result = self.comment_classifier.classify_comment(comment_text)
        
        # Check for spam
        spam_result = self.sentiment_analyzer.detect_spam(comment_text)
        
        # Get toxicity assessment
        toxicity_result = self.comment_classifier.get_comment_toxicity(comment_text)
        
        # Determine final tag (prioritize spam detection)
        final_tag = "spam" if spam_result["is_spam"] else classification_result["tag"]
        
        return {
            "text": comment_text,
            "sentiment": sentiment_result["sentiment"],
            "emotion": emotions,
            "tag": final_tag,
            "confidence": classification_result["confidence"],
            "details": {
                "sentiment_scores": sentiment_result["scores"],
                "classification_scores": classification_result["scores"],
                "spam_detection": spam_result,
                "toxicity": toxicity_result
            }
        }
    
    def _generate_summary(self, video_analysis: Dict, comment_analyses: List[Dict]) -> Dict[str, any]:
        """Generate summary statistics"""
        if not comment_analyses:
            return {
                "total_comments": 0,
                "sentiment_distribution": {},
                "emotion_distribution": {},
                "tag_distribution": {},
                "toxicity_summary": {}
            }
        
        # Count sentiments
        sentiments = [c["sentiment"] for c in comment_analyses]
        sentiment_counts = {
            "positive": sentiments.count("positive"),
            "negative": sentiments.count("negative"),
            "neutral": sentiments.count("neutral"),
            "mixed": sentiments.count("mixed")
        }
        
        # Count emotions
        all_emotions = []
        for comment in comment_analyses:
            all_emotions.extend(comment["emotion"])
        emotion_counts = {}
        for emotion in set(all_emotions):
            emotion_counts[emotion] = all_emotions.count(emotion)
        
        # Count tags
        tags = [c["tag"] for c in comment_analyses]
        tag_counts = {
            "funny": tags.count("funny"),
            "hateful": tags.count("hateful"),
            "supportive": tags.count("supportive"),
            "spam": tags.count("spam"),
            "insightful": tags.count("insightful"),
            "neutral": tags.count("neutral")
        }
        
        # Toxicity summary
        toxicity_levels = []
        for comment in comment_analyses:
            if "details" in comment and "toxicity" in comment["details"]:
                toxicity_levels.append(comment["details"]["toxicity"]["toxicity_level"])
        
        toxicity_summary = {
            "safe": toxicity_levels.count("safe"),
            "moderate": toxicity_levels.count("moderate"),
            "high": toxicity_levels.count("high")
        }
        
        return {
            "total_comments": len(comment_analyses),
            "sentiment_distribution": sentiment_counts,
            "emotion_distribution": emotion_counts,
            "tag_distribution": tag_counts,
            "toxicity_summary": toxicity_summary
        }
    
    def quick_analyze(self, text: str) -> Dict[str, any]:
        """Quick analysis for single text input"""
        if not text:
            return {
                "sentiment": "neutral",
                "emotions": [],
                "tag": "neutral",
                "confidence": 0.0
            }
        
        sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)
        emotions = self.emotion_detector.detect_emotions(text)
        classification = self.comment_classifier.classify_comment(text)
        
        return {
            "text": text,
            "sentiment": sentiment_result["sentiment"],
            "emotions": emotions,
            "tag": classification["tag"],
            "confidence": classification["confidence"],
            "sentiment_scores": sentiment_result["scores"]
        }
    
    def batch_analyze_comments(self, comments: List[str]) -> List[Dict[str, any]]:
        """Batch analysis for multiple comments"""
        results = []
        for comment in comments:
            analysis = self._analyze_single_comment(comment)
            results.append(analysis)
        return results
    
    def export_analysis(self, analysis_result: Dict, format_type: str = "json") -> str:
        """Export analysis results in specified format"""
        if format_type.lower() == "json":
            return json.dumps(analysis_result, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

# Example usage function for the specific request
def process_example_data():
    """Process the example data from the user request"""
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
    
    return formatted_result

if __name__ == "__main__":
    # Test the engine with the example data
    result = process_example_data()
    print(json.dumps(result, indent=2, ensure_ascii=False))
