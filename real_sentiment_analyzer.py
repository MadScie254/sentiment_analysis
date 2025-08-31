"""
Real Sentiment Analyzer using Hugging Face API
Uses the provided API key for actual sentiment analysis
"""

import os
import requests
import logging
from typing import Dict, List, Optional
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
from vadersentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

class RealSentimentAnalyzer:
    """Real sentiment analyzer using multiple methods including Hugging Face API"""
    
    def __init__(self):
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or os.getenv('HUGGING_FACE_API_KEY')
        self.hf_api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        
        # Initialize VADER for backup
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.hf_api_key}',
            'Content-Type': 'application/json'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
        logger.info("Real Sentiment Analyzer initialized with Hugging Face API")
    
    def analyze_sentiment(self, text: str, method='huggingface') -> Dict:
        """
        Analyze sentiment using real models
        
        Args:
            text: Text to analyze
            method: 'huggingface', 'vader', 'textblob', or 'ensemble'
        
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            if not text or len(text.strip()) < 3:
                return self._create_neutral_result(text)
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            if method == 'huggingface':
                return self._analyze_with_huggingface(cleaned_text)
            elif method == 'vader':
                return self._analyze_with_vader(cleaned_text)
            elif method == 'textblob':
                return self._analyze_with_textblob(cleaned_text)
            elif method == 'ensemble':
                return self._analyze_with_ensemble(cleaned_text)
            else:
                # Default to Hugging Face with VADER fallback
                result = self._analyze_with_huggingface(cleaned_text)
                if not result or result.get('confidence', 0) < 0.5:
                    logger.info("Hugging Face confidence low, using VADER fallback")
                    return self._analyze_with_vader(cleaned_text)
                return result
                
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._analyze_with_vader(text)  # Fallback to VADER
    
    def _analyze_with_huggingface(self, text: str) -> Dict:
        """Analyze using Hugging Face API"""
        try:
            self._rate_limit()
            
            payload = {
                "inputs": text,
                "options": {"wait_for_model": True}
            }
            
            response = self.session.post(self.hf_api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    # Parse Hugging Face results
                    sentiment_scores = {}
                    for item in result[0]:
                        label = item['label'].lower()
                        score = item['score']
                        
                        # Map labels to standard format
                        if 'positive' in label or label == 'label_2':
                            sentiment_scores['positive'] = score
                        elif 'negative' in label or label == 'label_0':
                            sentiment_scores['negative'] = score
                        elif 'neutral' in label or label == 'label_1':
                            sentiment_scores['neutral'] = score
                    
                    # Determine primary sentiment
                    primary_sentiment = max(sentiment_scores.keys(), key=lambda k: sentiment_scores[k])
                    confidence = sentiment_scores[primary_sentiment]
                    
                    # Ensure all sentiment scores exist
                    sentiment_scores.setdefault('positive', 0.0)
                    sentiment_scores.setdefault('negative', 0.0)
                    sentiment_scores.setdefault('neutral', 0.0)
                    
                    return {
                        'text': text[:200],
                        'sentiment': primary_sentiment,
                        'confidence': round(confidence, 3),
                        'scores': {k: round(v, 3) for k, v in sentiment_scores.items()},
                        'model_used': 'huggingface-roberta',
                        'processing_time': 0.1,
                        'emotion_scores': self._extract_emotions(text),
                        'toxicity_score': self._estimate_toxicity(text),
                        'method': 'huggingface_api'
                    }
            
            else:
                logger.warning(f"Hugging Face API error: {response.status_code} - {response.text}")
                return self._analyze_with_vader(text)
                
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            return self._analyze_with_vader(text)
    
    def _analyze_with_vader(self, text: str) -> Dict:
        """Analyze using VADER sentiment analyzer"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            
            # Determine primary sentiment
            if scores['compound'] >= 0.05:
                sentiment = 'positive'
                confidence = abs(scores['compound'])
            elif scores['compound'] <= -0.05:
                sentiment = 'negative'
                confidence = abs(scores['compound'])
            else:
                sentiment = 'neutral'
                confidence = 1 - abs(scores['compound'])
            
            return {
                'text': text[:200],
                'sentiment': sentiment,
                'confidence': round(min(confidence, 0.99), 3),
                'scores': {
                    'positive': round(scores['pos'], 3),
                    'negative': round(scores['neg'], 3),
                    'neutral': round(scores['neu'], 3)
                },
                'model_used': 'vader',
                'processing_time': 0.01,
                'emotion_scores': self._extract_emotions(text),
                'toxicity_score': self._estimate_toxicity(text),
                'method': 'vader'
            }
            
        except Exception as e:
            logger.error(f"VADER analysis error: {e}")
            return self._create_neutral_result(text)
    
    def _analyze_with_textblob(self, text: str) -> Dict:
        """Analyze using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to sentiment
            if polarity > 0.1:
                sentiment = 'positive'
                confidence = min(polarity, 0.9)
            elif polarity < -0.1:
                sentiment = 'negative'
                confidence = min(abs(polarity), 0.9)
            else:
                sentiment = 'neutral'
                confidence = 0.7
            
            # Calculate score distribution
            pos_score = max(0, polarity)
            neg_score = max(0, -polarity)
            neu_score = 1 - abs(polarity)
            
            # Normalize scores
            total = pos_score + neg_score + neu_score
            if total > 0:
                pos_score /= total
                neg_score /= total
                neu_score /= total
            
            return {
                'text': text[:200],
                'sentiment': sentiment,
                'confidence': round(confidence, 3),
                'scores': {
                    'positive': round(pos_score, 3),
                    'negative': round(neg_score, 3),
                    'neutral': round(neu_score, 3)
                },
                'model_used': 'textblob',
                'processing_time': 0.02,
                'emotion_scores': self._extract_emotions(text),
                'toxicity_score': self._estimate_toxicity(text),
                'method': 'textblob',
                'subjectivity': round(subjectivity, 3)
            }
            
        except Exception as e:
            logger.error(f"TextBlob analysis error: {e}")
            return self._create_neutral_result(text)
    
    def _analyze_with_ensemble(self, text: str) -> Dict:
        """Analyze using ensemble of methods"""
        try:
            # Get results from all methods
            hf_result = self._analyze_with_huggingface(text)
            vader_result = self._analyze_with_vader(text)
            textblob_result = self._analyze_with_textblob(text)
            
            # Combine results
            all_results = [hf_result, vader_result, textblob_result]
            valid_results = [r for r in all_results if r and r.get('sentiment')]
            
            if not valid_results:
                return self._create_neutral_result(text)
            
            # Calculate weighted average
            sentiment_votes = {'positive': 0, 'negative': 0, 'neutral': 0}
            total_confidence = 0
            
            for result in valid_results:
                sentiment = result['sentiment']
                confidence = result['confidence']
                weight = confidence
                
                sentiment_votes[sentiment] += weight
                total_confidence += confidence
            
            # Determine final sentiment
            final_sentiment = max(sentiment_votes, key=sentiment_votes.get)
            final_confidence = total_confidence / len(valid_results)
            
            # Average scores
            avg_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
            for score_type in avg_scores:
                scores = [r['scores'][score_type] for r in valid_results if score_type in r['scores']]
                avg_scores[score_type] = sum(scores) / len(scores) if scores else 0
            
            return {
                'text': text[:200],
                'sentiment': final_sentiment,
                'confidence': round(final_confidence, 3),
                'scores': {k: round(v, 3) for k, v in avg_scores.items()},
                'model_used': 'ensemble',
                'processing_time': 0.15,
                'emotion_scores': self._extract_emotions(text),
                'toxicity_score': self._estimate_toxicity(text),
                'method': 'ensemble',
                'component_results': [r['method'] for r in valid_results]
            }
            
        except Exception as e:
            logger.error(f"Ensemble analysis error: {e}")
            return self._analyze_with_vader(text)
    
    def _extract_emotions(self, text: str) -> Dict:
        """Extract basic emotions from text"""
        emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'love', 'excellent'],
            'anger': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'irritated', 'frustrated'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified'],
            'sadness': ['sad', 'depressed', 'upset', 'disappointed', 'hurt', 'sorry'],
            'disgust': ['disgusting', 'gross', 'awful', 'terrible', 'horrible', 'sick'],
            'surprise': ['surprised', 'shocked', 'amazed', 'unexpected', 'wow']
        }
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = min(score * 0.2, 1.0)  # Normalize to 0-1
        
        # Ensure at least some emotion distribution
        if all(score == 0 for score in emotion_scores.values()):
            emotion_scores['neutral'] = 0.8
        
        return emotion_scores
    
    def _estimate_toxicity(self, text: str) -> float:
        """Estimate toxicity level of text"""
        toxic_keywords = [
            'hate', 'stupid', 'idiot', 'damn', 'terrible', 'awful', 
            'horrible', 'disgusting', 'pathetic', 'useless', 'worthless'
        ]
        
        text_lower = text.lower()
        toxic_count = sum(1 for keyword in toxic_keywords if keyword in text_lower)
        
        # Normalize toxicity score
        toxicity_score = min(toxic_count * 0.15, 0.9)
        
        return round(toxicity_score, 3)
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        import re
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:]', ' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _rate_limit(self):
        """Simple rate limiting for API calls"""
        now = time.time()
        if now - self.last_request_time < self.min_request_interval:
            time.sleep(self.min_request_interval - (now - self.last_request_time))
        self.last_request_time = time.time()
    
    def _create_neutral_result(self, text: str) -> Dict:
        """Create a neutral result for fallback"""
        return {
            'text': text[:200],
            'sentiment': 'neutral',
            'confidence': 0.5,
            'scores': {
                'positive': 0.2,
                'negative': 0.2,
                'neutral': 0.6
            },
            'model_used': 'fallback',
            'processing_time': 0.01,
            'emotion_scores': {'neutral': 0.8},
            'toxicity_score': 0.0,
            'method': 'fallback'
        }

# Create global instance
real_sentiment_analyzer = RealSentimentAnalyzer()
