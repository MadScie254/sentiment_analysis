"""
Production-Ready Sentiment Analyzer
Enhanced version with robust error handling, security, and multiple fallback methods
"""

import os
import json
import requests
import logging
import time
import hashlib
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import lru_cache
import threading

# External libraries with fallback handling
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Enhanced result object for sentiment analysis"""
    text: str
    sentiment: str
    confidence: float
    scores: Dict[str, float]
    model_used: str
    processing_time: float
    emotion_scores: Optional[Dict[str, float]] = None
    toxicity_score: float = 0.0
    method: str = 'unknown'
    timestamp: Optional[str] = None
    text_length: int = 0
    word_count: int = 0
    error_details: Optional[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if not self.text_length:
            self.text_length = len(self.text)
        if not self.word_count:
            self.word_count = len(self.text.split())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class EnhancedSentimentAnalyzer:
    """Production-grade sentiment analyzer with comprehensive error handling"""
    
    def __init__(self, cache_size: int = 1000, request_timeout: int = 30):
        # API Configuration
        self.hf_api_key = self._get_secure_api_key()
        self.hf_api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        
        # Security settings
        self.max_text_length = 5000
        self.min_text_length = 1
        self.request_timeout = request_timeout
        self.max_retries = 3
        
        # Initialize components
        self._initialize_analyzers()
        self._setup_session()
        
        # Threading and caching
        self.thread_lock = threading.Lock()
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Rate limiting
        self.last_request_time = 0
        self.rate_limit_delay = 0.1
        
        logger.info("✅ Enhanced Sentiment Analyzer initialized")
    
    def _get_secure_api_key(self) -> Optional[str]:
        """Securely retrieve and validate API key"""
        api_key = (
            os.getenv('HUGGINGFACE_API_KEY') or 
            os.getenv('HUGGING_FACE_API_KEY') or
            os.getenv('HF_API_KEY')
        )
        
        if api_key and len(api_key) > 10:
            logger.info("✅ Hugging Face API key found")
            return api_key
        else:
            logger.warning("⚠️  No valid Hugging Face API key - using fallback methods")
            return None
    
    def _initialize_analyzers(self):
        """Initialize available sentiment analyzers"""
        self.analyzers_available = {
            'huggingface_api': bool(self.hf_api_key),
            'vader': VADER_AVAILABLE,
            'textblob': TEXTBLOB_AVAILABLE
        }
        
        # Initialize VADER
        if VADER_AVAILABLE:
            try:
                self.vader_analyzer = SentimentIntensityAnalyzer()
                logger.info("✅ VADER analyzer ready")
            except Exception as e:
                logger.error(f"❌ VADER initialization failed: {e}")
                self.analyzers_available['vader'] = False
        
        available_methods = [k for k, v in self.analyzers_available.items() if v]
        logger.info(f"📊 Available methods: {available_methods}")
    
    def _setup_session(self):
        """Setup HTTP session with security headers"""
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.hf_api_key}' if self.hf_api_key else '',
            'Content-Type': 'application/json',
            'User-Agent': 'SentimentAnalyzer/2.0'
        })
    
    def _validate_input(self, text: str):
        """Validate input text for security and format"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        if len(text.strip()) < self.min_text_length:
            raise ValueError(f"Text too short (minimum {self.min_text_length} characters)")
        
        if len(text) > self.max_text_length:
            raise ValueError(f"Text too long (maximum {self.max_text_length} characters)")
    
    def _apply_rate_limiting(self):
        """Apply rate limiting for API requests"""
        with self.thread_lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Basic HTML entity decoding
        html_entities = {
            '&amp;': '&', '&lt;': '<', '&gt;': '>', 
            '&quot;': '"', '&#39;': "'", '&nbsp;': ' '
        }
        for entity, char in html_entities.items():
            text = text.replace(entity, char)
        
        return text
    
    def analyze_sentiment(self, text: str, method: str = 'auto') -> SentimentResult:
        """
        Enhanced sentiment analysis with comprehensive error handling
        
        Args:
            text: Text to analyze (1-5000 characters)
            method: Analysis method ('auto', 'huggingface', 'vader', 'textblob', 'ensemble')
        
        Returns:
            SentimentResult object with analysis results
        """
        start_time = time.time()
        
        try:
            # Input validation
            self._validate_input(text)
            text = text.strip()
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Backward compatibility mappings
            if method == 'roberta':
                method = 'huggingface'
            
            # Determine method to use
            if method == 'auto':
                method = self._select_best_method()
            
            # Perform analysis
            result = self._perform_analysis(cleaned_text, method, start_time)
            
            logger.info(f"✅ Analysis completed: {method} -> {result.sentiment} ({result.confidence:.3f})")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Analysis failed: {e}")
            
            # Return fallback result
            return SentimentResult(
                text=text[:200] if text else "",
                sentiment="neutral",
                confidence=0.0,
                scores={"positive": 0.33, "negative": 0.33, "neutral": 0.34},
                model_used="fallback",
                processing_time=processing_time,
                method="error_fallback",
                error_details=str(e)
            )
    
    def _select_best_method(self) -> str:
        """Select the best available analysis method"""
        if self.analyzers_available['huggingface_api'] and self.hf_api_key:
            return 'huggingface'
        elif self.analyzers_available['vader']:
            return 'vader'
        elif self.analyzers_available['textblob']:
            return 'textblob'
        else:
            return 'basic_fallback'
    
    def _perform_analysis(self, text: str, method: str, start_time: float) -> SentimentResult:
        """Perform sentiment analysis with specified method"""
        try:
            if method == 'huggingface':
                return self._analyze_with_huggingface(text, start_time)
            elif method == 'vader':
                return self._analyze_with_vader(text, start_time)
            elif method == 'textblob':
                return self._analyze_with_textblob(text, start_time)
            elif method == 'ensemble':
                return self._analyze_with_ensemble(text, start_time)
            else:
                return self._analyze_with_basic_fallback(text, start_time)
                
        except Exception as e:
            logger.warning(f"⚠️  Method {method} failed: {e}. Trying fallback...")
            if method != 'vader' and self.analyzers_available['vader']:
                return self._analyze_with_vader(text, start_time)
            else:
                return self._analyze_with_basic_fallback(text, start_time)
    
    def _analyze_with_huggingface(self, text: str, start_time: float) -> SentimentResult:
        """Analyze using Hugging Face API"""
        if not self.hf_api_key:
            raise ValueError("No Hugging Face API key available")
        
        try:
            self._apply_rate_limiting()
            
            payload = {
                "inputs": text,
                "options": {"wait_for_model": True}
            }
            
            response = self.session.post(
                self.hf_api_url, 
                json=payload, 
                timeout=self.request_timeout
            )
            
            if response.status_code == 503:
                logger.info("🔄 Model loading, waiting...")
                time.sleep(10)
                response = self.session.post(self.hf_api_url, json=payload, timeout=self.request_timeout)
            
            response.raise_for_status()
            result_data = response.json()
            
            if isinstance(result_data, list) and len(result_data) > 0:
                return self._parse_huggingface_result(result_data, text, start_time)
            else:
                raise ValueError("Invalid API response format")
                
        except requests.exceptions.Timeout:
            logger.error("⏰ Hugging Face API timeout")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"🌐 HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Hugging Face API error: {e}")
            raise
    
    def _parse_huggingface_result(self, result_data: List, text: str, start_time: float) -> SentimentResult:
        """Parse Hugging Face API response"""
        sentiment_scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        
        for item in result_data[0]:
            label = item['label'].upper()
            score = float(item['score'])
            
            # Correct mapping for cardiffnlp model
            if label in ['LABEL_0', 'NEGATIVE']:
                sentiment_scores['negative'] = score
            elif label in ['LABEL_1', 'NEUTRAL']:
                sentiment_scores['neutral'] = score
            elif label in ['LABEL_2', 'POSITIVE']:
                sentiment_scores['positive'] = score
        
        # Determine primary sentiment
        primary_sentiment = max(sentiment_scores.keys(), key=lambda k: sentiment_scores[k])
        confidence = sentiment_scores[primary_sentiment]
        
        processing_time = time.time() - start_time
        
        return SentimentResult(
            text=text[:200],
            sentiment=primary_sentiment,
            confidence=round(confidence, 3),
            scores=sentiment_scores,
            model_used="cardiffnlp/twitter-roberta-base-sentiment-latest",
            processing_time=round(processing_time, 3),
            method="huggingface"
        )
    
    def _analyze_with_vader(self, text: str, start_time: float) -> SentimentResult:
        """Analyze using VADER sentiment analyzer"""
        if not VADER_AVAILABLE or not hasattr(self, 'vader_analyzer'):
            raise ValueError("VADER analyzer not available")
        
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            processing_time = time.time() - start_time
            
            # Convert VADER scores to consistent format
            sentiment_scores = {
                'positive': max(0.0, scores['pos']),
                'negative': max(0.0, scores['neg']),
                'neutral': max(0.0, scores['neu'])
            }
            
            # Determine sentiment from compound score
            compound = scores['compound']
            if compound >= 0.05:
                primary_sentiment = 'positive'
                confidence = abs(compound)
            elif compound <= -0.05:
                primary_sentiment = 'negative'
                confidence = abs(compound)
            else:
                primary_sentiment = 'neutral'
                confidence = 1 - abs(compound)
            
            return SentimentResult(
                text=text[:200],
                sentiment=primary_sentiment,
                confidence=round(min(confidence, 1.0), 3),
                scores=sentiment_scores,
                model_used="vader",
                processing_time=round(processing_time, 3),
                method="vader"
            )
            
        except Exception as e:
            logger.error(f"❌ VADER analysis failed: {e}")
            raise
    
    def _analyze_with_textblob(self, text: str, start_time: float) -> SentimentResult:
        """Analyze using TextBlob"""
        if not TEXTBLOB_AVAILABLE:
            raise ValueError("TextBlob not available")
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            processing_time = time.time() - start_time
            
            # Convert polarity to sentiment categories
            if polarity > 0.1:
                primary_sentiment = 'positive'
                confidence = abs(polarity)
            elif polarity < -0.1:
                primary_sentiment = 'negative'
                confidence = abs(polarity)
            else:
                primary_sentiment = 'neutral'
                confidence = 1 - abs(polarity)
            
            # Create consistent score format
            pos_score = max(0, polarity)
            neg_score = max(0, -polarity)
            neu_score = 1 - abs(polarity)
            
            sentiment_scores = {
                'positive': pos_score,
                'negative': neg_score,
                'neutral': neu_score
            }
            
            return SentimentResult(
                text=text[:200],
                sentiment=primary_sentiment,
                confidence=round(confidence, 3),
                scores=sentiment_scores,
                model_used="textblob",
                processing_time=round(processing_time, 3),
                method="textblob"
            )
            
        except Exception as e:
            logger.error(f"❌ TextBlob analysis failed: {e}")
            raise
    
    def _analyze_with_ensemble(self, text: str, start_time: float) -> SentimentResult:
        """Ensemble analysis using multiple methods"""
        results = []
        methods_tried = []
        
        # Try available methods
        for method in ['huggingface', 'vader', 'textblob']:
            if self.analyzers_available.get(method.replace('huggingface', 'huggingface_api'), False):
                try:
                    result = self._perform_analysis(text, method, start_time)
                    results.append(result)
                    methods_tried.append(method)
                except Exception as e:
                    logger.warning(f"⚠️  Ensemble method {method} failed: {e}")
        
        if not results:
            raise ValueError("No methods available for ensemble")
        
        # Combine results using weighted average
        weights = {'huggingface': 0.5, 'vader': 0.3, 'textblob': 0.2}
        
        combined_scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        total_weight = 0.0
        
        for result in results:
            method_weight = weights.get(result.method, 0.1)
            total_weight += method_weight
            
            for sentiment, score in result.scores.items():
                combined_scores[sentiment] += score * method_weight
        
        # Normalize scores
        if total_weight > 0:
            for sentiment in combined_scores:
                combined_scores[sentiment] /= total_weight
        
        # Determine primary sentiment
        primary_sentiment = max(combined_scores.keys(), key=lambda k: combined_scores[k])
        confidence = combined_scores[primary_sentiment]
        
        processing_time = time.time() - start_time
        
        return SentimentResult(
            text=text[:200],
            sentiment=primary_sentiment,
            confidence=round(confidence, 3),
            scores=combined_scores,
            model_used=f"ensemble({', '.join(methods_tried)})",
            processing_time=round(processing_time, 3),
            method="ensemble"
        )
    
    def _analyze_with_basic_fallback(self, text: str, start_time: float) -> SentimentResult:
        """Basic keyword-based fallback analysis"""
        processing_time = time.time() - start_time
        
        # Simple keyword lists
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'awesome', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'disgusting', 'pathetic', 'useless', 'disappointing']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            confidence = min(0.7, 0.5 + (pos_count - neg_count) * 0.1)
        elif neg_count > pos_count:
            sentiment = 'negative'
            confidence = min(0.7, 0.5 + (neg_count - pos_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        # Create score distribution
        if sentiment == 'positive':
            scores = {'positive': confidence, 'negative': (1-confidence)/2, 'neutral': (1-confidence)/2}
        elif sentiment == 'negative':
            scores = {'negative': confidence, 'positive': (1-confidence)/2, 'neutral': (1-confidence)/2}
        else:
            scores = {'neutral': confidence, 'positive': (1-confidence)/2, 'negative': (1-confidence)/2}
        
        return SentimentResult(
            text=text[:200],
            sentiment=sentiment,
            confidence=round(confidence, 3),
            scores=scores,
            model_used="basic_keyword_fallback",
            processing_time=round(processing_time, 3),
            method="basic_fallback"
        )
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """Get current analyzer status and capabilities"""
        return {
            "analyzers_available": self.analyzers_available,
            "api_key_configured": bool(self.hf_api_key),
            "cache_size": len(getattr(self, 'cache', {})),
            "request_timeout": self.request_timeout,
            "version": "2.0.0"
        }
    
    def get_model_info(self):
        """Get model information for compatibility with dashboard"""
        return {
            'available_models': self.available_methods,
            'device': 'cpu',  # We're using API-based models
            'primary_method': self.available_methods[0] if self.available_methods else 'unknown',
            'fallback_methods': self.available_methods[1:] if len(self.available_methods) > 1 else [],
            'api_integration': True,
            'cache_enabled': True
        }

# Create global instance for backward compatibility
real_sentiment_analyzer = EnhancedSentimentAnalyzer()

# Export for backward compatibility
__all__ = ['EnhancedSentimentAnalyzer', 'SentimentResult', 'real_sentiment_analyzer']
