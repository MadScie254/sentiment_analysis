"""
Advanced Sentiment Analysis Features
Enhanced sentiment analysis capabilities with multiple models, emotion detection, and advanced analytics
"""

import re
import emoji
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import logging
from collections import Counter, defaultdict
import json

logger = logging.getLogger(__name__)

class AdvancedSentimentAnalyzer:
    """Advanced sentiment analysis with multiple models and emotion detection"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Emotion lexicons
        self.emotion_lexicons = {
            'joy': ['happy', 'joy', 'cheerful', 'delighted', 'ecstatic', 'elated', 'glad', 'pleased', 'excited', 'thrilled'],
            'sadness': ['sad', 'depressed', 'melancholy', 'sorrowful', 'grief', 'mourning', 'despair', 'dejected'],
            'anger': ['angry', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated', 'outraged', 'livid'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous', 'panic', 'frightened'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'startled', 'stunned', 'bewildered'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened', 'appalled', 'nauseated'],
            'trust': ['trust', 'faith', 'confidence', 'belief', 'reliable', 'dependable', 'loyal'],
            'anticipation': ['excited', 'eager', 'hopeful', 'optimistic', 'looking forward', 'anticipating']
        }
        
        # Enhanced Swahili lexicon
        self.swahili_emotions = {
            'furaha': ('joy', 0.8),
            'huzuni': ('sadness', 0.8),
            'hasira': ('anger', 0.9),
            'hofu': ('fear', 0.7),
            'mshangao': ('surprise', 0.6),
            'chuki': ('disgust', 0.8),
            'imani': ('trust', 0.7),
            'matumaini': ('anticipation', 0.8),
            'poa': ('joy', 0.6),
            'sawa': ('joy', 0.5),
            'vibaya': ('sadness', 0.7),
            'nzuri': ('joy', 0.6),
            'mbaya': ('sadness', 0.7)
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'very': 1.5, 'extremely': 2.0, 'really': 1.3, 'quite': 1.2, 'somewhat': 0.8,
            'slightly': 0.6, 'barely': 0.4, 'absolutely': 2.0, 'totally': 1.8, 'completely': 2.0
        }
        
        # Context patterns
        self.negation_patterns = [
            r'\b(?:not|never|no|nothing|nowhere|neither|nobody|none|without)\b',
            r"\b(?:isn't|aren't|wasn't|weren't|won't|wouldn't|shouldn't|couldn't|can't|don't|doesn't|didn't|haven't|hasn't|hadn't)\b"
        ]
        
    def analyze_comprehensive(self, text: str, include_emotions: bool = True) -> Dict[str, Any]:
        """
        Comprehensive sentiment and emotion analysis
        """
        if not text or text.strip() == "":
            return self._empty_analysis()
        
        processed_text = self.preprocess_text(text)
        
        # Multiple sentiment approaches
        vader_analysis = self._analyze_vader(processed_text)
        textblob_analysis = self._analyze_textblob(processed_text)
        custom_analysis = self._analyze_custom_rules(processed_text)
        
        # Emotion detection
        emotions = {}
        if include_emotions:
            emotions = self.detect_emotions(processed_text)
        
        # Combine analyses with weighted approach
        combined_sentiment = self._combine_sentiment_scores(
            vader_analysis, textblob_analysis, custom_analysis
        )
        
        # Advanced features
        linguistic_features = self._extract_linguistic_features(text)
        intensity_score = self._calculate_intensity(processed_text)
        
        return {
            'sentiment': combined_sentiment,
            'emotions': emotions,
            'linguistic_features': linguistic_features,
            'intensity_score': intensity_score,
            'confidence': self._calculate_confidence(combined_sentiment, emotions),
            'individual_analyses': {
                'vader': vader_analysis,
                'textblob': textblob_analysis,
                'custom': custom_analysis
            },
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'processed_text_length': len(processed_text)
        }
    
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect specific emotions in text"""
        emotions = {emotion: 0.0 for emotion in self.emotion_lexicons.keys()}
        words = text.lower().split()
        
        # English emotion detection
        for emotion, emotion_words in self.emotion_lexicons.items():
            matches = sum(1 for word in words if any(ew in word for ew in emotion_words))
            if matches > 0:
                emotions[emotion] = min(matches / len(words) * 10, 1.0)  # Normalize
        
        # Swahili emotion detection
        for word in words:
            if word in self.swahili_emotions:
                emotion, intensity = self.swahili_emotions[word]
                if emotion in emotions:
                    emotions[emotion] = max(emotions[emotion], intensity)
        
        # Apply intensity modifiers
        emotions = self._apply_intensity_modifiers(text, emotions)
        
        return emotions
    
    def analyze_batch(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze multiple texts efficiently"""
        if not texts:
            return {'analyses': [], 'summary': {}}
        
        analyses = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0}
        emotion_totals = defaultdict(float)
        
        for i, text in enumerate(texts):
            try:
                analysis = self.analyze_comprehensive(text)
                analyses.append({
                    'index': i,
                    'text_preview': text[:100] + '...' if len(text) > 100 else text,
                    'analysis': analysis
                })
                
                # Aggregate for summary
                sentiment_counts[analysis['sentiment']['label']] += 1
                for emotion, score in analysis['emotions'].items():
                    emotion_totals[emotion] += score
                    
            except Exception as e:
                logger.error(f"Failed to analyze text {i}: {e}")
                analyses.append({
                    'index': i,
                    'text_preview': text[:100] + '...' if len(text) > 100 else text,
                    'analysis': self._empty_analysis(),
                    'error': str(e)
                })
        
        # Calculate summary statistics
        total_texts = len(texts)
        summary = {
            'total_texts': total_texts,
            'sentiment_distribution': {
                k: v/total_texts for k, v in sentiment_counts.items()
            },
            'dominant_sentiment': max(sentiment_counts.items(), key=lambda x: x[1])[0],
            'average_emotions': {
                emotion: score/total_texts for emotion, score in emotion_totals.items()
            },
            'most_prominent_emotion': max(emotion_totals.items(), key=lambda x: x[1])[0] if emotion_totals else 'neutral'
        }
        
        return {
            'analyses': analyses,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_sentiment_trends(self, analyses: List[Dict], time_window: str = 'hourly') -> Dict[str, Any]:
        """Analyze sentiment trends over time"""
        if not analyses:
            return {}
        
        trends = defaultdict(list)
        emotion_trends = defaultdict(lambda: defaultdict(list))
        
        for analysis in analyses:
            timestamp = datetime.fromisoformat(analysis.get('timestamp', datetime.now().isoformat()))
            sentiment = analysis.get('sentiment', {}).get('label', 'neutral')
            emotions = analysis.get('emotions', {})
            
            # Group by time window
            if time_window == 'hourly':
                time_key = timestamp.strftime('%Y-%m-%d %H:00')
            elif time_window == 'daily':
                time_key = timestamp.strftime('%Y-%m-%d')
            else:  # minute
                time_key = timestamp.strftime('%Y-%m-%d %H:%M')
            
            trends[time_key].append(sentiment)
            for emotion, score in emotions.items():
                emotion_trends[time_key][emotion].append(score)
        
        # Calculate trend statistics
        trend_data = {}
        for time_key, sentiments in trends.items():
            sentiment_counts = Counter(sentiments)
            avg_emotions = {}
            for emotion in self.emotion_lexicons.keys():
                scores = emotion_trends[time_key][emotion]
                avg_emotions[emotion] = sum(scores) / len(scores) if scores else 0.0
            
            trend_data[time_key] = {
                'sentiment_distribution': dict(sentiment_counts),
                'total_count': len(sentiments),
                'dominant_sentiment': sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral',
                'average_emotions': avg_emotions
            }
        
        return trend_data
    
    def preprocess_text(self, text: str) -> str:
        """Advanced text preprocessing"""
        if not text:
            return ""
        
        # Convert emojis to text with emotion context
        text = emoji.demojize(text, delimiters=(" ", " "))
        
        # Enhanced slang and Kenyan context
        replacements = {
            # Kenyan slang
            'sawa sawa': 'very good',
            'poa kabisa': 'very cool',
            'mambo vipi': 'how are things',
            'hakuna matata': 'no problem',
            'harambee': 'unity cooperation',
            'iko sawa': 'it is good',
            'si sawa': 'not good',
            
            # Internet slang
            'omg': 'oh my god',
            'lol': 'laughing',
            'rofl': 'laughing very much',
            'smh': 'disappointed',
            'fml': 'frustrated',
            'wtf': 'confused angry',
            'imo': 'in my opinion',
            'tbh': 'to be honest',
            'ngl': 'not gonna lie',
            'fr': 'for real',
            'rn': 'right now',
            
            # Emotion intensifiers
            '!!!': ' very excited',
            '???': ' very confused',
            '😊': ' happy',
            '😢': ' sad',
            '😠': ' angry',
            '😱': ' shocked',
            '👍': ' positive',
            '👎': ' negative'
        }
        
        text_lower = text.lower()
        for old, new in replacements.items():
            text_lower = text_lower.replace(old, new)
        
        return text_lower
    
    def _analyze_vader(self, text: str) -> Dict[str, Any]:
        """VADER sentiment analysis"""
        scores = self.vader.polarity_scores(text)
        return {
            'scores': scores,
            'label': self._scores_to_label(scores['pos'], scores['neg'], scores['neu'])
        }
    
    def _analyze_textblob(self, text: str) -> Dict[str, Any]:
        """TextBlob sentiment analysis"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Convert polarity to pos/neg/neu format
        if polarity > 0.1:
            pos, neg, neu = polarity, 0, 1-polarity
        elif polarity < -0.1:
            pos, neg, neu = 0, abs(polarity), 1-abs(polarity)
        else:
            pos, neg, neu = 0, 0, 1
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'scores': {'pos': pos, 'neg': neg, 'neu': neu},
            'label': self._scores_to_label(pos, neg, neu)
        }
    
    def _analyze_custom_rules(self, text: str) -> Dict[str, Any]:
        """Custom rule-based analysis"""
        words = text.lower().split()
        
        # Swahili sentiment
        swahili_positive = sum(1 for word in words if word in ['poa', 'sawa', 'nzuri', 'vizuri', 'furaha'])
        swahili_negative = sum(1 for word in words if word in ['mbaya', 'vibaya', 'huzuni', 'hasira'])
        
        # Negation detection
        negation_count = sum(1 for pattern in self.negation_patterns 
                           if re.search(pattern, text, re.IGNORECASE))
        
        # Calculate scores
        total_sentiment_words = swahili_positive + swahili_negative
        if total_sentiment_words > 0:
            pos = swahili_positive / len(words)
            neg = swahili_negative / len(words)
            neu = 1 - (pos + neg)
            
            # Apply negation modifier
            if negation_count > 0:
                pos, neg = neg, pos  # Flip sentiment
        else:
            pos, neg, neu = 0, 0, 1
        
        return {
            'swahili_positive': swahili_positive,
            'swahili_negative': swahili_negative,
            'negation_count': negation_count,
            'scores': {'pos': pos, 'neg': neg, 'neu': neu},
            'label': self._scores_to_label(pos, neg, neu)
        }
    
    def _combine_sentiment_scores(self, vader: Dict, textblob: Dict, custom: Dict) -> Dict[str, Any]:
        """Combine multiple sentiment analyses with weighted approach"""
        # Weights for different methods
        weights = {'vader': 0.4, 'textblob': 0.3, 'custom': 0.3}
        
        # Combine scores
        combined_pos = (
            vader['scores']['pos'] * weights['vader'] +
            textblob['scores']['pos'] * weights['textblob'] +
            custom['scores']['pos'] * weights['custom']
        )
        combined_neg = (
            vader['scores']['neg'] * weights['vader'] +
            textblob['scores']['neg'] * weights['textblob'] +
            custom['scores']['neg'] * weights['custom']
        )
        combined_neu = (
            vader['scores']['neu'] * weights['vader'] +
            textblob['scores']['neu'] * weights['textblob'] +
            custom['scores']['neu'] * weights['custom']
        )
        
        # Normalize
        total = combined_pos + combined_neg + combined_neu
        if total > 0:
            combined_pos /= total
            combined_neg /= total
            combined_neu /= total
        
        return {
            'positive': round(combined_pos, 3),
            'negative': round(combined_neg, 3),
            'neutral': round(combined_neu, 3),
            'label': self._scores_to_label(combined_pos, combined_neg, combined_neu),
            'compound': combined_pos - combined_neg
        }
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Extract linguistic features from text"""
        words = text.split()
        
        return {
            'word_count': len(words),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'exclamation_marks': text.count('!'),
            'question_marks': text.count('?'),
            'caps_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'punctuation_density': sum(1 for c in text if not c.isalnum() and not c.isspace()) / len(text) if text else 0,
            'unique_words': len(set(words)),
            'repetition_ratio': (len(words) - len(set(words))) / len(words) if words else 0
        }
    
    def _calculate_intensity(self, text: str) -> float:
        """Calculate emotional intensity of text"""
        intensity = 0.0
        words = text.lower().split()
        
        # Intensity from modifiers
        for word in words:
            if word in self.intensity_modifiers:
                intensity += self.intensity_modifiers[word]
        
        # Intensity from punctuation
        intensity += text.count('!') * 0.3
        intensity += text.count('?') * 0.1
        
        # Caps intensity
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        intensity += caps_ratio * 2
        
        # Normalize to 0-1 range
        return min(intensity / 5, 1.0)
    
    def _apply_intensity_modifiers(self, text: str, emotions: Dict[str, float]) -> Dict[str, float]:
        """Apply intensity modifiers to emotion scores"""
        words = text.lower().split()
        
        for word in words:
            if word in self.intensity_modifiers:
                modifier = self.intensity_modifiers[word]
                for emotion in emotions:
                    emotions[emotion] *= modifier
                    emotions[emotion] = min(emotions[emotion], 1.0)  # Cap at 1.0
        
        return emotions
    
    def _calculate_confidence(self, sentiment: Dict, emotions: Dict) -> float:
        """Calculate confidence score for the analysis"""
        # Confidence based on score distribution
        scores = [sentiment['positive'], sentiment['negative'], sentiment['neutral']]
        max_score = max(scores)
        score_variance = np.var(scores)
        
        # Confidence from emotion consistency
        emotion_consistency = 1.0 - np.var(list(emotions.values())) if emotions else 0.5
        
        # Combine factors
        confidence = (max_score + emotion_consistency) / 2
        return round(confidence, 3)
    
    def _scores_to_label(self, pos: float, neg: float, neu: float) -> str:
        """Convert scores to sentiment label"""
        if pos > 0.6:
            return 'positive'
        elif neg > 0.6:
            return 'negative'
        elif abs(pos - neg) < 0.1:
            return 'mixed'
        else:
            return 'neutral'
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            'sentiment': {
                'positive': 0.0, 'negative': 0.0, 'neutral': 1.0,
                'label': 'neutral', 'compound': 0.0
            },
            'emotions': {emotion: 0.0 for emotion in self.emotion_lexicons.keys()},
            'linguistic_features': {},
            'intensity_score': 0.0,
            'confidence': 0.0,
            'individual_analyses': {},
            'timestamp': datetime.now().isoformat(),
            'text_length': 0,
            'processed_text_length': 0
        }

# Global instance for use in dashboard
advanced_sentiment_analyzer = AdvancedSentimentAnalyzer()