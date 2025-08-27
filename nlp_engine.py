from typing import Dict, List, Optional, Union
import json
import re
from datetime import datetime
from sentiment_engine import SentimentAnalyzer
from emotion_detector import EmotionDetector
from comment_classifier import CommentClassifier
from link_analyzer import LinkAnalyzer

class NLPEngine:
    """
    Main NLP Engine that orchestrates all sentiment analysis components
    Now includes link analysis capabilities for social media content
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_detector = EmotionDetector()
        self.comment_classifier = CommentClassifier()
        self.link_analyzer = LinkAnalyzer()
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

    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze content from a URL (YouTube, Twitter, Instagram, etc.)
        
        Args:
            url (str): URL to analyze
            
        Returns:
            Dict containing analysis results
        """
        # Extract content from URL
        url_data = self.link_analyzer.analyze_url(url)
        
        if not url_data.get('success', False):
            return {
                'url': url,
                'error': url_data.get('error', 'Failed to extract content'),
                'success': False
            }
        
        # Analyze the extracted content
        title = url_data.get('title', '')
        description = url_data.get('description', '')
        comments = url_data.get('comments', [])
        
        # Perform sentiment analysis on the content
        analysis_result = self.analyze_video_data(title, description, comments)
        
        # Add URL-specific metadata
        analysis_result['url_analysis'] = {
            'original_url': url,
            'platform': url_data.get('type', 'unknown'),
            'domain': url_data.get('domain', ''),
            'metadata': url_data.get('metadata', {}),
            'extracted_at': url_data.get('extracted_at', ''),
            'content_summary': {
                'title_length': len(title),
                'description_length': len(description),
                'comments_count': len(comments),
                'has_content': bool(title or description or comments)
            }
        }
        
        return analysis_result
    
    def analyze_multiple_urls(self, urls: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple URLs and provide aggregated results
        
        Args:
            urls (List[str]): List of URLs to analyze
            
        Returns:
            Dict containing aggregated analysis results
        """
        results = []
        platform_stats = {}
        total_comments = 0
        sentiment_aggregation = {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0}
        emotion_aggregation = {}
        
        for url in urls:
            try:
                result = self.analyze_url(url)
                if result.get('url_analysis', {}).get('content_summary', {}).get('has_content', False):
                    results.append(result)
                    
                    # Track platform statistics
                    platform = result.get('url_analysis', {}).get('platform', 'unknown')
                    platform_stats[platform] = platform_stats.get(platform, 0) + 1
                    
                    # Aggregate sentiment
                    video_sentiment = result.get('video_sentiment', 'neutral')
                    if isinstance(video_sentiment, dict):
                        video_sentiment = video_sentiment.get('label', 'neutral')
                    
                    if video_sentiment in sentiment_aggregation:
                        sentiment_aggregation[video_sentiment] += 1
                    
                    # Aggregate comments
                    comments = result.get('comments', [])
                    total_comments += len(comments)
                    
                    # Aggregate emotions
                    for comment in comments:
                        emotions = comment.get('emotion', [])
                        for emotion in emotions:
                            emotion_aggregation[emotion] = emotion_aggregation.get(emotion, 0) + 1
                            
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })
        
        return {
            'summary': {
                'total_urls_analyzed': len(urls),
                'successful_analyses': len([r for r in results if r.get('success', True)]),
                'total_comments': total_comments,
                'platforms_analyzed': len(platform_stats)
            },
            'platform_distribution': platform_stats,
            'sentiment_aggregation': sentiment_aggregation,
            'emotion_aggregation': emotion_aggregation,
            'individual_results': results,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def extract_urls_from_text(self, text: str) -> List[str]:
        """
        Extract URLs from text content
        
        Args:
            text (str): Text containing potential URLs
            
        Returns:
            List of extracted URLs
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return urls
    
    def analyze_text_with_urls(self, text: str, analyze_embedded_urls: bool = True) -> Dict[str, Any]:
        """
        Analyze text content and optionally analyze any embedded URLs
        
        Args:
            text (str): Text content to analyze
            analyze_embedded_urls (bool): Whether to analyze URLs found in the text
            
        Returns:
            Dict containing comprehensive analysis results
        """
        # Extract URLs from text
        urls = self.extract_urls_from_text(text)
        
        # Analyze the text content itself
        text_analysis = self.analyze_single_comment(text)
        
        result = {
            'text_analysis': text_analysis,
            'embedded_urls': {
                'found_urls': urls,
                'url_count': len(urls),
                'analysis_results': []
            },
            'combined_insights': {},
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Analyze embedded URLs if requested
        if analyze_embedded_urls and urls:
            url_results = []
            for url in urls:
                try:
                    url_result = self.analyze_url(url)
                    url_results.append(url_result)
                except Exception as e:
                    url_results.append({
                        'url': url,
                        'error': str(e),
                        'success': False
                    })
            
            result['embedded_urls']['analysis_results'] = url_results
            
            # Create combined insights
            all_sentiments = [text_analysis.get('sentiment', 'neutral')]
            all_emotions = text_analysis.get('emotion', [])
            
            for url_result in url_results:
                if url_result.get('success', True):
                    video_sentiment = url_result.get('video_sentiment', 'neutral')
                    if isinstance(video_sentiment, dict):
                        video_sentiment = video_sentiment.get('label', 'neutral')
                    all_sentiments.append(video_sentiment)
                    
                    comments = url_result.get('comments', [])
                    for comment in comments:
                        emotions = comment.get('emotion', [])
                        all_emotions.extend(emotions)
            
            # Calculate combined sentiment
            sentiment_counts = {}
            for sentiment in all_sentiments:
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else 'neutral'
            
            # Calculate emotion distribution
            emotion_counts = {}
            for emotion in all_emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            result['combined_insights'] = {
                'dominant_sentiment': dominant_sentiment,
                'sentiment_distribution': sentiment_counts,
                'top_emotions': sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                'total_content_pieces': 1 + len(urls),
                'has_multimedia_content': len(urls) > 0
            }
        
        return result
    
    def get_sample_urls(self) -> Dict[str, List[str]]:
        """Get sample URLs for testing"""
        return self.link_analyzer.get_sample_links()

if __name__ == "__main__":
    # Test the engine with the example data
    result = process_example_data()
    print(json.dumps(result, indent=2, ensure_ascii=False))
