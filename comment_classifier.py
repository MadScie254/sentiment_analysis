from typing import Dict, List, Tuple
import re
from sentiment_engine import SentimentAnalyzer
from emotion_detector import EmotionDetector

class CommentClassifier:
    """
    Classifies comments into categories: funny, hateful, supportive, spam, insightful
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_detector = EmotionDetector()
        
        # Classification patterns and keywords
        self.classification_patterns = {
            'funny': {
                'keywords': [
                    'lol', 'lmao', 'rofl', 'haha', 'funny', 'hilarious',
                    'comedy', 'joke', 'laughing', 'dead', 'dying',
                    'can\'t stop laughing', 'too funny', 'cracking up'
                ],
                'emojis': ['😂', '🤣', '😆', '😹', '💀'],
                'patterns': [r'ha+ha+', r'he+he+', r'lmao+', r'lol+']
            },
            'hateful': {
                'keywords': [
                    'hate', 'stupid', 'idiot', 'moron', 'loser', 'pathetic',
                    'disgusting', 'trash', 'garbage', 'worthless', 'kill yourself',
                    'die', 'kys', 'retard', 'gay', 'homo', 'slut', 'whore'
                ],
                'patterns': [r'f+u+c+k+ you+', r'go+ die+', r'[A-Z]{5,}.*!{2,}']
            },
            'supportive': {
                'keywords': [
                    'support', 'love', 'amazing', 'keep going', 'you got this',
                    'proud', 'inspiring', 'motivational', 'encourage',
                    'believe', 'strong', 'brave', 'respect', 'admire',
                    'karibu', 'pole', 'poa', 'asante', 'baraka'
                ],
                'emojis': ['❤️', '💕', '🙏', '👏', '🤝', '💪', '🌟'],
                'patterns': [r'you.{0,10}(can|will|got)', r'keep.{0,10}(going|up)']
            },
            'spam': {
                'keywords': [
                    'click here', 'free money', 'win now', 'limited offer',
                    'act now', 'special deal', 'make money', 'work from home',
                    'bitcoin', 'crypto', 'investment opportunity', 'guaranteed'
                ],
                'patterns': [
                    r'http[s]?://[^\s]+',
                    r'www\.[^\s]+',
                    r'\$\d+',
                    r'FREE.{0,20}NOW',
                    r'CLICK.{0,20}HERE'
                ]
            },
            'insightful': {
                'keywords': [
                    'analysis', 'perspective', 'interesting', 'thoughtful',
                    'insight', 'understand', 'explain', 'research', 'study',
                    'data', 'evidence', 'consider', 'however', 'although',
                    'because', 'therefore', 'consequently', 'furthermore'
                ],
                'patterns': [
                    r'i think.{10,}',
                    r'in my opinion.{10,}',
                    r'from.{0,10}perspective',
                    r'research shows',
                    r'studies indicate'
                ]
            }
        }
    
    def classify_comment(self, text: str) -> Dict[str, any]:
        """
        Classify a comment into categories with confidence scores
        """
        if not text or text.strip() == "":
            return {
                "tag": "neutral",
                "confidence": 0.0,
                "scores": {}
            }
        
        text_lower = text.lower()
        classification_scores = {}
        
        # Calculate scores for each classification
        for category, patterns in self.classification_patterns.items():
            score = self._calculate_category_score(text, text_lower, patterns)
            classification_scores[category] = score
        
        # Special handling for spam detection
        spam_result = self.sentiment_analyzer.detect_spam(text)
        if spam_result['is_spam']:
            classification_scores['spam'] = max(classification_scores.get('spam', 0), 
                                              spam_result['confidence'])
        
        # Get sentiment and emotions for additional context
        sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)
        emotions = self.emotion_detector.detect_emotions(text)
        
        # Adjust scores based on sentiment and emotions
        classification_scores = self._adjust_scores_with_context(
            classification_scores, sentiment_result, emotions
        )
        
        # Determine primary classification
        if max(classification_scores.values()) < 0.2:
            primary_tag = "neutral"
            confidence = 0.8
        else:
            primary_tag = max(classification_scores, key=classification_scores.get)
            confidence = classification_scores[primary_tag]
        
        return {
            "tag": primary_tag,
            "confidence": round(confidence, 3),
            "scores": {k: round(v, 3) for k, v in classification_scores.items()}
        }
    
    def _calculate_category_score(self, text: str, text_lower: str, patterns: Dict) -> float:
        """Calculate score for a specific category"""
        score = 0.0
        total_words = len(text_lower.split())
        
        # Keyword matching
        keyword_matches = 0
        if 'keywords' in patterns:
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    keyword_matches += 1
        
        # Emoji matching
        emoji_matches = 0
        if 'emojis' in patterns:
            for emoji in patterns['emojis']:
                if emoji in text:
                    emoji_matches += 1
        
        # Pattern matching
        pattern_matches = 0
        if 'patterns' in patterns:
            for pattern in patterns['patterns']:
                if re.search(pattern, text_lower):
                    pattern_matches += 1
        
        # Calculate weighted score
        if total_words > 0:
            score = (keyword_matches * 0.6 + emoji_matches * 0.3 + pattern_matches * 0.4) / total_words
        else:
            score = emoji_matches * 0.2 + pattern_matches * 0.3
        
        return min(score, 1.0)
    
    def _adjust_scores_with_context(self, scores: Dict[str, float], 
                                  sentiment_result: Dict, emotions: List[str]) -> Dict[str, float]:
        """Adjust classification scores based on sentiment and emotions"""
        adjusted_scores = scores.copy()
        
        # Sentiment-based adjustments
        sentiment = sentiment_result['sentiment']
        confidence = sentiment_result['confidence']
        
        if sentiment == 'positive' and confidence > 0.7:
            adjusted_scores['supportive'] = max(adjusted_scores.get('supportive', 0), 0.3)
            adjusted_scores['funny'] = adjusted_scores.get('funny', 0) * 1.2
        elif sentiment == 'negative' and confidence > 0.7:
            adjusted_scores['hateful'] = adjusted_scores.get('hateful', 0) * 1.3
        
        # Emotion-based adjustments
        if 'joy' in emotions:
            adjusted_scores['funny'] = adjusted_scores.get('funny', 0) * 1.3
            adjusted_scores['supportive'] = adjusted_scores.get('supportive', 0) * 1.1
        
        if 'anger' in emotions:
            adjusted_scores['hateful'] = adjusted_scores.get('hateful', 0) * 1.4
        
        if 'sarcasm' in emotions:
            adjusted_scores['funny'] = adjusted_scores.get('funny', 0) * 1.2
            adjusted_scores['hateful'] = adjusted_scores.get('hateful', 0) * 0.8
        
        # Normalize scores
        max_score = max(adjusted_scores.values()) if adjusted_scores.values() else 0
        if max_score > 1.0:
            factor = 1.0 / max_score
            adjusted_scores = {k: v * factor for k, v in adjusted_scores.items()}
        
        return adjusted_scores
    
    def get_comment_toxicity(self, text: str) -> Dict[str, any]:
        """
        Assess toxicity level of a comment
        """
        if not text:
            return {"toxicity_level": "safe", "confidence": 1.0, "reasons": []}
        
        toxic_indicators = []
        text_lower = text.lower()
        
        # Check for explicit hate speech
        hate_words = [
            'hate', 'kill', 'die', 'murder', 'violence', 'hurt', 'harm',
            'stupid', 'idiot', 'moron', 'retard', 'gay', 'homo'
        ]
        found_hate = [word for word in hate_words if word in text_lower]
        if found_hate:
            toxic_indicators.extend(found_hate)
        
        # Check for threats
        threat_patterns = [
            r'i.{0,10}kill.{0,10}you',
            r'you.{0,10}die',
            r'go.{0,10}kill.{0,10}yourself',
            r'kys'
        ]
        for pattern in threat_patterns:
            if re.search(pattern, text_lower):
                toxic_indicators.append("threat_detected")
        
        # Check for excessive profanity
        profanity = ['fuck', 'shit', 'damn', 'bitch', 'ass', 'hell']
        profanity_count = sum(text_lower.count(word) for word in profanity)
        if profanity_count > 2:
            toxic_indicators.append("excessive_profanity")
        
        # Determine toxicity level
        if len(toxic_indicators) >= 3:
            toxicity_level = "high"
            confidence = 0.9
        elif len(toxic_indicators) >= 1:
            toxicity_level = "moderate"
            confidence = 0.7
        else:
            toxicity_level = "safe"
            confidence = 0.8
        
        return {
            "toxicity_level": toxicity_level,
            "confidence": confidence,
            "reasons": toxic_indicators
        }
