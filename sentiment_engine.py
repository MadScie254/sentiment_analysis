import re
import emoji
from typing import Dict, List, Tuple, Optional
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

class SentimentAnalyzer:
    """
    Advanced sentiment analysis engine supporting multiple languages and slang
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.swahili_positive = [
            'poa', 'sawa', 'vizuri', 'nzuri', 'karibu', 'asante', 'baraka',
            'furaha', 'raha', 'upendo', 'mapenzi', 'heri', 'amani'
        ]
        self.swahili_negative = [
            'mbaya', 'vibaya', 'hasira', 'uchungu', 'mateso', 'maumivu',
            'machozi', 'huzuni', 'wasiwasi', 'hofu', 'hatari'
        ]
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
            
        # Convert emojis to text
        text = emoji.demojize(text, delimiters=(" ", " "))
        
        # Handle common Kenyan/internet slang
        slang_replacements = {
            'bro': 'brother',
            'vibes': 'good feelings',
            'sawa': 'okay good',
            'poa': 'cool good',
            'karibu': 'welcome',
            'matatu': 'public transport',
            'nairobi': 'city',
            'mzee': 'elder',
            'jambo': 'hello',
            'mambo': 'what is up',
            'frfr': 'for real for real',
            'ngl': 'not gonna lie',
            'tbh': 'to be honest',
            'imo': 'in my opinion',
            'lowkey': 'somewhat',
            'highkey': 'obviously'
        }
        
        text_lower = text.lower()
        for slang, replacement in slang_replacements.items():
            text_lower = text_lower.replace(slang, replacement)
            
        return text_lower
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Comprehensive sentiment analysis
        Returns: sentiment label, confidence scores, and reasoning
        """
        if not text or text.strip() == "":
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "scores": {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
            }
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # VADER analysis (good for social media text)
        vader_scores = self.vader.polarity_scores(processed_text)
        
        # TextBlob analysis
        blob = TextBlob(processed_text)
        textblob_polarity = blob.sentiment.polarity
        
        # Swahili sentiment boost
        swahili_boost = self._calculate_swahili_sentiment(processed_text)
        
        # Combine scores
        combined_positive = (vader_scores['pos'] + max(0, textblob_polarity) + max(0, swahili_boost)) / 3
        combined_negative = (vader_scores['neg'] + max(0, -textblob_polarity) + max(0, -swahili_boost)) / 3
        combined_neutral = vader_scores['neu']
        
        # Normalize scores
        total = combined_positive + combined_negative + combined_neutral
        if total > 0:
            combined_positive /= total
            combined_negative /= total
            combined_neutral /= total
        
        # Determine final sentiment
        if combined_positive > 0.6:
            sentiment = "positive"
            confidence = combined_positive
        elif combined_negative > 0.6:
            sentiment = "negative"
            confidence = combined_negative
        elif abs(combined_positive - combined_negative) < 0.1:
            sentiment = "mixed"
            confidence = 1 - combined_neutral
        else:
            sentiment = "neutral"
            confidence = combined_neutral
            
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": {
                "positive": round(combined_positive, 3),
                "negative": round(combined_negative, 3),
                "neutral": round(combined_neutral, 3)
            }
        }
    
    def _calculate_swahili_sentiment(self, text: str) -> float:
        """Calculate sentiment boost for Swahili words"""
        positive_count = sum(1 for word in self.swahili_positive if word in text)
        negative_count = sum(1 for word in self.swahili_negative if word in text)
        
        if positive_count == 0 and negative_count == 0:
            return 0.0
            
        total_words = len(text.split())
        sentiment_ratio = (positive_count - negative_count) / max(total_words, 1)
        
        return min(max(sentiment_ratio, -1.0), 1.0)
    
    def detect_spam(self, text: str) -> Dict[str, any]:
        """Detect if text is spam"""
        if not text:
            return {"is_spam": False, "confidence": 0.0, "reasons": []}
        
        spam_indicators = []
        text_lower = text.lower()
        
        # URL patterns
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.search(url_pattern, text):
            spam_indicators.append("contains_url")
        
        # Suspicious words
        spam_words = ['free', 'click', 'win', 'prize', 'offer', 'deal', 'crypto', 'bitcoin', 'investment']
        found_spam_words = [word for word in spam_words if word in text_lower]
        if found_spam_words:
            spam_indicators.append(f"spam_words: {', '.join(found_spam_words)}")
        
        # Excessive punctuation or caps
        if len(re.findall(r'[!]{2,}', text)) > 0 or len(re.findall(r'[A-Z]{5,}', text)) > 0:
            spam_indicators.append("excessive_formatting")
        
        # Calculate spam probability
        spam_score = len(spam_indicators) / 5.0  # Max 5 indicators
        is_spam = spam_score > 0.4
        
        return {
            "is_spam": is_spam,
            "confidence": min(spam_score, 1.0),
            "reasons": spam_indicators
        }
