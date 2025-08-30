"""
Real NLP Engine with Multiple Models for Sentiment Analysis
Supports BERT, RoBERTa, VADER, TextBlob, and Custom Models
"""

import os
import torch
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass

# Core NLP Libraries
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    pipeline, BertTokenizer, BertForSequenceClassification
)

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

# Language Detection
from langdetect import detect
import emoji

@dataclass
class SentimentResult:
    """Structured sentiment analysis result"""
    text: str
    sentiment: str
    confidence: float
    scores: Dict[str, float]
    model_used: str
    processing_time: float
    language: str
    emotion_scores: Optional[Dict[str, float]] = None
    toxicity_score: Optional[float] = None
    bias_score: Optional[float] = None
    metadata: Optional[Dict] = None

class RealNLPEngine:
    """
    Production-ready NLP Engine with multiple models
    """
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Model configurations
        self.model_configs = {
            'roberta': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
            'bert': 'nlptown/bert-base-multilingual-uncased-sentiment',
            'distilbert': 'distilbert-base-uncased-finetuned-sst-2-english',
            'finbert': 'ProsusAI/finbert',  # Financial sentiment
            'emotion': 'j-hartmann/emotion-english-distilroberta-base'
        }
        
        self.initialize_models()
        
    def initialize_models(self):
        """Initialize all available models"""
        self.logger.info("Initializing NLP models...")
        
        try:
            # Initialize lightweight models first
            self._init_vader()
            self._init_textblob()
            
            # Initialize transformer models
            self._init_transformer_models()
            
            self.logger.info("All models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing models: {str(e)}")
            # Fallback to basic models
            self._init_fallback_models()
    
    def _init_vader(self):
        """Initialize VADER sentiment analyzer"""
        self.models['vader'] = self.vader_analyzer
        self.logger.info("VADER model initialized")
    
    def _init_textblob(self):
        """Initialize TextBlob analyzer"""
        self.models['textblob'] = TextBlob
        self.logger.info("TextBlob model initialized")
    
    def _init_transformer_models(self):
        """Initialize transformer-based models"""
        
        # RoBERTa for general sentiment
        try:
            self.pipelines['roberta'] = pipeline(
                "sentiment-analysis",
                model=self.model_configs['roberta'],
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("RoBERTa model initialized")
        except Exception as e:
            self.logger.warning(f"Failed to load RoBERTa: {e}")
        
        # DistilBERT for fast inference
        try:
            self.pipelines['distilbert'] = pipeline(
                "sentiment-analysis",
                model=self.model_configs['distilbert'],
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("DistilBERT model initialized")
        except Exception as e:
            self.logger.warning(f"Failed to load DistilBERT: {e}")
        
        # Emotion analysis
        try:
            self.pipelines['emotion'] = pipeline(
                "text-classification",
                model=self.model_configs['emotion'],
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("Emotion model initialized")
        except Exception as e:
            self.logger.warning(f"Failed to load Emotion model: {e}")
    
    def _init_fallback_models(self):
        """Initialize fallback models if transformers fail"""
        self.logger.info("Using fallback models only")
        self.models['fallback'] = True
    
    def analyze_sentiment(self, text: str, model_preference: str = 'auto') -> SentimentResult:
        """
        Comprehensive sentiment analysis with multiple models
        
        Args:
            text: Input text to analyze
            model_preference: Preferred model ('auto', 'roberta', 'bert', 'vader', 'textblob')
        
        Returns:
            SentimentResult object with comprehensive analysis
        """
        start_time = datetime.now()
        
        # Preprocessing
        text = self._preprocess_text(text)
        language = self._detect_language(text)
        
        # Choose model based on preference and availability
        if model_preference == 'auto':
            model_to_use = self._select_best_model(text, language)
        else:
            model_to_use = model_preference if model_preference in self.models or model_preference in self.pipelines else 'vader'
        
        # Perform analysis
        try:
            if model_to_use in self.pipelines:
                result = self._analyze_with_transformer(text, model_to_use)
            elif model_to_use == 'vader':
                result = self._analyze_with_vader(text)
            elif model_to_use == 'textblob':
                result = self._analyze_with_textblob(text)
            else:
                result = self._analyze_with_vader(text)  # Fallback
            
            # Add emotion analysis if available
            emotion_scores = self._analyze_emotions(text)
            
            # Calculate additional metrics
            toxicity_score = self._calculate_toxicity(text)
            bias_score = self._calculate_bias(text)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return SentimentResult(
                text=text[:200] + "..." if len(text) > 200 else text,
                sentiment=result['sentiment'],
                confidence=result['confidence'],
                scores=result['scores'],
                model_used=model_to_use,
                processing_time=processing_time,
                language=language,
                emotion_scores=emotion_scores,
                toxicity_score=toxicity_score,
                bias_score=bias_score,
                metadata={
                    'text_length': len(text),
                    'word_count': len(text.split()),
                    'has_emoji': bool(emoji.emoji_count(text)),
                    'device_used': str(self.device)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            # Return fallback result
            return self._fallback_analysis(text, start_time)
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Handle special characters but preserve emoji
        text = text.strip()
        
        return text
    
    def _detect_language(self, text: str) -> str:
        """Detect text language"""
        try:
            return detect(text)
        except:
            return 'en'  # Default to English
    
    def _select_best_model(self, text: str, language: str) -> str:
        """Select the best model based on text characteristics"""
        
        # For financial text, use FinBERT if available
        financial_keywords = ['stock', 'market', 'price', 'investment', 'profit', 'loss', 'revenue']
        if any(keyword in text.lower() for keyword in financial_keywords) and 'finbert' in self.pipelines:
            return 'finbert'
        
        # For short text (like tweets), prefer RoBERTa
        if len(text.split()) < 20 and 'roberta' in self.pipelines:
            return 'roberta'
        
        # For longer text, prefer DistilBERT for speed
        if len(text.split()) > 100 and 'distilbert' in self.pipelines:
            return 'distilbert'
        
        # Default priority order
        for model in ['roberta', 'distilbert', 'bert']:
            if model in self.pipelines:
                return model
        
        return 'vader'  # Final fallback
    
    def _analyze_with_transformer(self, text: str, model_name: str) -> Dict:
        """Analyze with transformer model"""
        try:
            pipeline_result = self.pipelines[model_name](text)
            
            if isinstance(pipeline_result, list):
                result = pipeline_result[0]
            else:
                result = pipeline_result
            
            # Normalize labels
            sentiment = self._normalize_sentiment_label(result['label'])
            confidence = result['score']
            
            # Create score distribution
            scores = self._create_score_distribution(sentiment, confidence)
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'scores': scores
            }
            
        except Exception as e:
            self.logger.error(f"Error with {model_name}: {e}")
            return self._analyze_with_vader(text)
    
    def _analyze_with_vader(self, text: str) -> Dict:
        """Analyze with VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Determine primary sentiment
        if scores['compound'] >= 0.05:
            sentiment = 'positive'
            confidence = scores['compound']
        elif scores['compound'] <= -0.05:
            sentiment = 'negative'
            confidence = abs(scores['compound'])
        else:
            sentiment = 'neutral'
            confidence = 1 - abs(scores['compound'])
        
        return {
            'sentiment': sentiment,
            'confidence': min(confidence, 1.0),
            'scores': {
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        }
    
    def _analyze_with_textblob(self, text: str) -> Dict:
        """Analyze with TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
            confidence = polarity
        elif polarity < -0.1:
            sentiment = 'negative'
            confidence = abs(polarity)
        else:
            sentiment = 'neutral'
            confidence = 1 - abs(polarity)
        
        scores = self._create_score_distribution(sentiment, confidence)
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': scores
        }
    
    def _analyze_emotions(self, text: str) -> Optional[Dict[str, float]]:
        """Analyze emotions in text"""
        if 'emotion' not in self.pipelines:
            return None
        
        try:
            results = self.pipelines['emotion'](text)
            emotions = {}
            
            for result in results:
                emotions[result['label'].lower()] = result['score']
            
            return emotions
            
        except Exception as e:
            self.logger.error(f"Error in emotion analysis: {e}")
            return None
    
    def _calculate_toxicity(self, text: str) -> float:
        """Calculate toxicity score (simplified)"""
        toxic_words = [
            'hate', 'stupid', 'idiot', 'kill', 'die', 'worst', 'terrible',
            'awful', 'disgusting', 'pathetic', 'useless', 'garbage'
        ]
        
        text_lower = text.lower()
        toxic_count = sum(1 for word in toxic_words if word in text_lower)
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        toxicity = min(toxic_count / word_count * 5, 1.0)  # Scale to 0-1
        return round(toxicity, 3)
    
    def _calculate_bias(self, text: str) -> float:
        """Calculate potential bias score (simplified)"""
        bias_indicators = [
            'always', 'never', 'all', 'none', 'every', 'totally',
            'completely', 'absolutely', 'definitely', 'obviously'
        ]
        
        text_lower = text.lower()
        bias_count = sum(1 for word in bias_indicators if word in text_lower)
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        bias = min(bias_count / word_count * 3, 1.0)  # Scale to 0-1
        return round(bias, 3)
    
    def _normalize_sentiment_label(self, label: str) -> str:
        """Normalize different model labels to standard format"""
        label = label.lower()
        
        if label in ['positive', 'pos', 'label_2']:
            return 'positive'
        elif label in ['negative', 'neg', 'label_0']:
            return 'negative'
        elif label in ['neutral', 'neu', 'label_1']:
            return 'neutral'
        else:
            return 'neutral'
    
    def _create_score_distribution(self, sentiment: str, confidence: float) -> Dict[str, float]:
        """Create normalized score distribution"""
        if sentiment == 'positive':
            positive = confidence
            remaining = 1 - confidence
            negative = remaining * 0.3
            neutral = remaining * 0.7
        elif sentiment == 'negative':
            negative = confidence
            remaining = 1 - confidence
            positive = remaining * 0.3
            neutral = remaining * 0.7
        else:
            neutral = confidence
            remaining = 1 - confidence
            positive = remaining * 0.5
            negative = remaining * 0.5
        
        return {
            'positive': round(positive, 3),
            'negative': round(negative, 3),
            'neutral': round(neutral, 3)
        }
    
    def _fallback_analysis(self, text: str, start_time: datetime) -> SentimentResult:
        """Fallback analysis when all models fail"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return SentimentResult(
            text=text[:200] + "..." if len(text) > 200 else text,
            sentiment='neutral',
            confidence=0.5,
            scores={'positive': 0.33, 'negative': 0.33, 'neutral': 0.34},
            model_used='fallback',
            processing_time=processing_time,
            language='unknown',
            metadata={'error': 'All models failed, using fallback'}
        )
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            'available_models': list(self.models.keys()) + list(self.pipelines.keys()),
            'device': str(self.device),
            'cuda_available': torch.cuda.is_available(),
            'model_configs': self.model_configs
        }
    
    def batch_analyze(self, texts: List[str], model_preference: str = 'auto') -> List[SentimentResult]:
        """Analyze multiple texts in batch"""
        results = []
        for text in texts:
            result = self.analyze_sentiment(text, model_preference)
            results.append(result)
        return results

# Global instance
nlp_engine = RealNLPEngine()
