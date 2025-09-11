"""
Advanced ML Models Collection - Free & Open Source
Collection of free ML models and tools for enhanced analysis
No API keys required - all open source and free to use
"""

import os
import re
import json
import time
import random
import logging
import requests
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import Counter
import math

# Try to import textstat, fall back to simple calculation if not available
try:
    from textstat import flesch_reading_ease, flesch_kincaid_grade
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False
    def flesch_reading_ease(text):
        """Simple fallback flesch reading ease calculation"""
        words = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        syllables = sum(max(1, len([c for c in word if c.lower() in 'aeiouy'])) for word in text.split())
        if sentences == 0 or words == 0:
            return 0
        return 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
    
    def flesch_kincaid_grade(text):
        """Simple fallback flesch-kincaid grade calculation"""
        words = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        syllables = sum(max(1, len([c for c in word if c.lower() in 'aeiouy'])) for word in text.split())
        if sentences == 0 or words == 0:
            return 0
        return (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59

import nltk
# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

class AdvancedMLModelsCollection:
    """
    Advanced ML models and analysis tools - All free and open source
    Includes sentiment analysis, text analysis, statistics, and more
    """
    
    def __init__(self):
        # Initialize NLTK tools
        try:
            self.vader = SentimentIntensityAnalyzer()
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            self.nltk_available = True
        except Exception as e:
            logger.warning(f"NLTK initialization failed: {e}")
            self.nltk_available = False
        
        # Emotional keywords dictionary
        self.emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'cheerful', 'delighted', 'pleased', 'glad', 'thrilled'],
            'anger': ['angry', 'furious', 'mad', 'rage', 'irritated', 'annoyed', 'frustrated'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous', 'panic'],
            'sadness': ['sad', 'depressed', 'unhappy', 'grief', 'sorrow', 'melancholy', 'disappointed'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'stunned', 'startled'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened', 'nauseated'],
            'trust': ['trust', 'confidence', 'faith', 'belief', 'reliable', 'dependable'],
            'anticipation': ['excited', 'eager', 'hopeful', 'expecting', 'anticipating']
        }
        
        # Bias detection keywords
        self.bias_indicators = {
            'political': ['liberal', 'conservative', 'democrat', 'republican', 'socialist', 'capitalist'],
            'gender': ['he said', 'she said', 'typical man', 'typical woman', 'like a girl', 'man up'],
            'racial': ['all [ethnicity]', 'those people', 'their kind'],
            'age': ['millennials', 'boomers', 'too old', 'too young', 'kids these days']
        }
        
        # Toxicity patterns (simplified)
        self.toxicity_patterns = [
            r'\b(hate|stupid|idiot|moron|dumb|pathetic)\b',
            r'\b(kill|die|death|murder)\b',
            r'\b(f[*u]ck|sh[*i]t|damn|hell)\b',
            r'[A-Z]{3,}',  # All caps (aggressive tone)
            r'!{2,}',  # Multiple exclamation marks
        ]
    
    def analyze_sentiment_advanced(self, text: str) -> Dict:
        """Advanced sentiment analysis with multiple metrics"""
        if not text or not isinstance(text, str):
            return self._default_sentiment_result()
        
        analysis = {
            'text': text[:200] + '...' if len(text) > 200 else text,
            'length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(sent_tokenize(text)) if self.nltk_available else text.count('.') + 1,
            'timestamp': datetime.now().isoformat()
        }
        
        # VADER Sentiment Analysis
        if self.nltk_available:
            vader_scores = self.vader.polarity_scores(text)
            analysis['vader'] = {
                'compound': vader_scores['compound'],
                'positive': vader_scores['pos'],
                'negative': vader_scores['neg'],
                'neutral': vader_scores['neu']
            }
            
            # Determine primary sentiment
            if vader_scores['compound'] >= 0.05:
                analysis['sentiment'] = 'positive'
                analysis['confidence'] = vader_scores['compound']
            elif vader_scores['compound'] <= -0.05:
                analysis['sentiment'] = 'negative'
                analysis['confidence'] = abs(vader_scores['compound'])
            else:
                analysis['sentiment'] = 'neutral'
                analysis['confidence'] = 1 - abs(vader_scores['compound'])
        else:
            # Fallback simple sentiment
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'worst']
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                analysis['sentiment'] = 'positive'
                analysis['confidence'] = min(pos_count / (pos_count + neg_count + 1), 0.9)
            elif neg_count > pos_count:
                analysis['sentiment'] = 'negative'
                analysis['confidence'] = min(neg_count / (pos_count + neg_count + 1), 0.9)
            else:
                analysis['sentiment'] = 'neutral'
                analysis['confidence'] = 0.5
        
        # Emotion Analysis
        analysis['emotions'] = self.analyze_emotions(text)
        
        # Readability Analysis
        analysis['readability'] = self.analyze_readability(text)
        
        # Bias Detection
        analysis['bias'] = self.detect_bias(text)
        
        # Toxicity Analysis
        analysis['toxicity'] = self.analyze_toxicity(text)
        
        # Advanced Text Statistics
        analysis['text_stats'] = self.get_text_statistics(text)
        
        return analysis
    
    def analyze_emotions(self, text: str) -> Dict:
        """Analyze emotional content using keyword matching"""
        if not text:
            return {}
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    score += text_lower.count(keyword)
                    matches.append(keyword)
            
            emotion_scores[emotion] = {
                'score': score,
                'matches': matches,
                'intensity': min(score / len(text.split()) * 10, 1.0) if text.split() else 0
            }
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'scores': emotion_scores,
            'dominant_emotion': dominant_emotion[0] if dominant_emotion[1]['score'] > 0 else 'neutral',
            'emotional_intensity': sum(e['intensity'] for e in emotion_scores.values()) / len(emotion_scores)
        }
    
    def analyze_readability(self, text: str) -> Dict:
        """Analyze text readability using multiple metrics"""
        if not text or len(text.split()) < 3:
            return {'error': 'Text too short for readability analysis'}
        
        try:
            flesch_ease = flesch_reading_ease(text)
            flesch_grade = flesch_kincaid_grade(text)
            
            # Readability interpretation
            if flesch_ease >= 90:
                reading_level = "Very Easy"
            elif flesch_ease >= 80:
                reading_level = "Easy"
            elif flesch_ease >= 70:
                reading_level = "Fairly Easy"
            elif flesch_ease >= 60:
                reading_level = "Standard"
            elif flesch_ease >= 50:
                reading_level = "Fairly Difficult"
            elif flesch_ease >= 30:
                reading_level = "Difficult"
            else:
                reading_level = "Very Difficult"
            
            return {
                'flesch_reading_ease': flesch_ease,
                'flesch_kincaid_grade': flesch_grade,
                'reading_level': reading_level,
                'estimated_reading_time': len(text.split()) / 200  # Average reading speed
            }
        except Exception as e:
            logger.warning(f"Readability analysis failed: {e}")
            return {'error': str(e)}
    
    def detect_bias(self, text: str) -> Dict:
        """Detect potential bias in text"""
        if not text:
            return {}
        
        text_lower = text.lower()
        bias_detected = {}
        
        for bias_type, indicators in self.bias_indicators.items():
            matches = []
            for indicator in indicators:
                if indicator.lower() in text_lower:
                    matches.append(indicator)
            
            bias_detected[bias_type] = {
                'detected': len(matches) > 0,
                'matches': matches,
                'score': len(matches) / len(text.split()) if text.split() else 0
            }
        
        # Overall bias score
        total_bias_score = sum(b['score'] for b in bias_detected.values())
        
        return {
            'bias_types': bias_detected,
            'overall_bias_score': min(total_bias_score, 1.0),
            'bias_level': 'high' if total_bias_score > 0.1 else 'medium' if total_bias_score > 0.05 else 'low'
        }
    
    def analyze_toxicity(self, text: str) -> Dict:
        """Analyze text toxicity using pattern matching"""
        if not text:
            return {'score': 0, 'level': 'none', 'patterns': []}
        
        toxic_matches = []
        total_score = 0
        
        for pattern in self.toxicity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                toxic_matches.extend(matches)
                total_score += len(matches)
        
        # Normalize score
        toxicity_score = min(total_score / len(text.split()) * 5, 1.0) if text.split() else 0
        
        # Determine toxicity level
        if toxicity_score >= 0.7:
            level = 'high'
        elif toxicity_score >= 0.3:
            level = 'medium'
        elif toxicity_score > 0:
            level = 'low'
        else:
            level = 'none'
        
        return {
            'score': toxicity_score,
            'level': level,
            'patterns_found': len(set(toxic_matches)),
            'matches': list(set(toxic_matches))[:10]  # Limit matches shown
        }
    
    def get_text_statistics(self, text: str) -> Dict:
        """Get comprehensive text statistics"""
        if not text:
            return {}
        
        words = text.split()
        sentences = sent_tokenize(text) if self.nltk_available else text.split('.')
        
        # Basic stats
        stats = {
            'character_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(text.split('\n\n')),
            'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'average_sentence_length': len(words) / len(sentences) if sentences else 0
        }
        
        # Vocabulary diversity
        if words:
            unique_words = set(word.lower() for word in words if word.isalpha())
            stats['unique_words'] = len(unique_words)
            stats['vocabulary_diversity'] = len(unique_words) / len(words)
        
        # Most common words
        if self.nltk_available and words:
            # Filter out stop words and get word frequencies
            filtered_words = [word.lower() for word in words 
                            if word.isalpha() and word.lower() not in self.stop_words]
            word_freq = Counter(filtered_words)
            stats['most_common_words'] = word_freq.most_common(10)
        
        # POS tagging if available
        if self.nltk_available:
            try:
                pos_tags = pos_tag(word_tokenize(text))
                pos_counts = Counter(tag for word, tag in pos_tags)
                stats['pos_distribution'] = dict(pos_counts.most_common(5))
            except Exception as e:
                logger.debug(f"POS tagging failed: {e}")
        
        return stats
    
    def analyze_multiple_texts(self, texts: List[str]) -> Dict:
        """Analyze multiple texts and provide aggregate statistics"""
        if not texts:
            return {}
        
        analyses = []
        for text in texts:
            analysis = self.analyze_sentiment_advanced(text)
            analyses.append(analysis)
        
        # Aggregate statistics
        sentiments = [a.get('sentiment', 'neutral') for a in analyses]
        confidences = [a.get('confidence', 0.5) for a in analyses]
        
        sentiment_distribution = {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        }
        
        # Calculate percentages
        total = len(sentiments)
        sentiment_percentages = {
            k: (v / total * 100) if total > 0 else 0 
            for k, v in sentiment_distribution.items()
        }
        
        # Average metrics
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        avg_word_count = sum(a.get('word_count', 0) for a in analyses) / len(analyses)
        
        # Toxicity analysis
        toxicity_scores = [a.get('toxicity', {}).get('score', 0) for a in analyses]
        avg_toxicity = sum(toxicity_scores) / len(toxicity_scores) if toxicity_scores else 0
        
        # Emotion analysis
        all_emotions = {}
        for analysis in analyses:
            emotions = analysis.get('emotions', {}).get('scores', {})
            for emotion, data in emotions.items():
                if emotion not in all_emotions:
                    all_emotions[emotion] = []
                all_emotions[emotion].append(data.get('intensity', 0))
        
        avg_emotions = {
            emotion: sum(scores) / len(scores) if scores else 0
            for emotion, scores in all_emotions.items()
        }
        
        return {
            'total_texts_analyzed': len(texts),
            'sentiment_distribution': sentiment_distribution,
            'sentiment_percentages': sentiment_percentages,
            'average_confidence': avg_confidence,
            'average_word_count': avg_word_count,
            'average_toxicity': avg_toxicity,
            'average_emotions': avg_emotions,
            'analyses': analyses[:10],  # Include first 10 detailed analyses
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_insights(self, analysis_result: Dict) -> List[str]:
        """Generate human-readable insights from analysis results"""
        insights = []
        
        if not analysis_result:
            return ["No data available for analysis."]
        
        # Sentiment insights
        sentiment = analysis_result.get('sentiment', 'neutral')
        confidence = analysis_result.get('confidence', 0.5)
        
        if sentiment == 'positive' and confidence > 0.7:
            insights.append(f"😊 Strong positive sentiment detected (confidence: {confidence:.1%})")
        elif sentiment == 'negative' and confidence > 0.7:
            insights.append(f"😞 Strong negative sentiment detected (confidence: {confidence:.1%})")
        elif sentiment == 'neutral':
            insights.append("😐 Neutral sentiment - balanced emotional tone")
        
        # Emotion insights
        emotions = analysis_result.get('emotions', {})
        if emotions and 'dominant_emotion' in emotions:
            dominant = emotions['dominant_emotion']
            if dominant != 'neutral':
                insights.append(f"🎭 Dominant emotion: {dominant.title()}")
        
        # Readability insights
        readability = analysis_result.get('readability', {})
        if 'reading_level' in readability:
            level = readability['reading_level']
            insights.append(f"📖 Reading level: {level}")
        
        # Toxicity insights
        toxicity = analysis_result.get('toxicity', {})
        if toxicity.get('level', 'none') != 'none':
            level = toxicity['level']
            insights.append(f"⚠️ Toxicity level: {level.title()}")
        
        # Text statistics insights
        stats = analysis_result.get('text_stats', {})
        word_count = stats.get('word_count', 0)
        if word_count > 0:
            if word_count < 10:
                insights.append("📝 Very short text - limited analysis possible")
            elif word_count > 200:
                insights.append("📄 Long-form text - comprehensive analysis available")
        
        # Vocabulary diversity
        vocab_diversity = stats.get('vocabulary_diversity', 0)
        if vocab_diversity > 0.7:
            insights.append("🌟 Rich vocabulary - diverse word usage")
        elif vocab_diversity < 0.3:
            insights.append("🔄 Repetitive vocabulary - limited word variety")
        
        return insights if insights else ["Analysis completed - no specific insights generated."]
    
    def _default_sentiment_result(self) -> Dict:
        """Return default sentiment analysis result"""
        return {
            'sentiment': 'neutral',
            'confidence': 0.5,
            'emotions': {},
            'readability': {},
            'bias': {},
            'toxicity': {'score': 0, 'level': 'none'},
            'text_stats': {},
            'error': 'Invalid or empty text provided'
        }

# Global instance
advanced_ml_models = AdvancedMLModelsCollection()
