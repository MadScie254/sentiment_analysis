"""
Production-Ready Sentiment Analyzer
Enterprise-grade sentiment analysis with comprehensive error handling, security, and fallbacks
"""

import os
import sys
import json
import requests
import logging
import time
import hashlib
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from functools import wraps, lru_cache
import threading

# External libraries with fallback imports
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    HF_TRANSFORMERS_AVAILABLE = True
except ImportError:
    HF_TRANSFORMERS_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Enhanced result object for sentiment analysis with comprehensive metadata"""
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
    language_detected: Optional[str] = None
    error_details: Optional[str] = None
    
    def __post_init__(self):
        """Auto-populate metadata fields"""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if not self.text_length:
            self.text_length = len(self.text)
        if not self.word_count:
            self.word_count = len(self.text.split())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

class EnhancedSentimentAnalyzer:
    """
    Production-grade sentiment analyzer with comprehensive error handling,
    multiple fallback methods, caching, and security features
    """
    
    def __init__(self, cache_size: int = 1000, request_timeout: int = 30):
        """Initialize with enhanced configuration and security"""
        
        # API Configuration with validation
        self.hf_api_key = self._get_secure_api_key()
        self.hf_api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        
        # Security settings
        self.max_text_length = 5000
        self.min_text_length = 1
        self.request_timeout = request_timeout
        self.max_retries = 3
        self.retry_delay = 1.0
        
        # Performance settings
        self.cache_size = cache_size
        self.rate_limit_delay = 0.1  # Minimum delay between requests
        
        # Initialize components with error handling
        self._initialize_analyzers()
        self._setup_session()
        self._setup_caching()
        
        # Threading for concurrent processing
        self.thread_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Rate limiting
        self.last_request_time = 0
        self.request_count = 0
        self.start_time = time.time()
        
        logger.info("✅ Enhanced Sentiment Analyzer initialized successfully")
    
    def _get_secure_api_key(self) -> Optional[str]:
        """Securely retrieve API key with validation"""
        api_key = (
            os.getenv('HUGGINGFACE_API_KEY') or 
            os.getenv('HUGGING_FACE_API_KEY') or
            os.getenv('HF_API_KEY')
        )
        
        if api_key:
            # Basic validation
            if len(api_key) < 10 or not api_key.startswith(('hf_', 'api_')):
                logger.warning("⚠️  API key format appears invalid")
            else:
                logger.info("✅ Hugging Face API key found and validated")
        else:
            logger.warning("⚠️  No Hugging Face API key found - using fallback methods only")
        
        return api_key
    
    def _initialize_analyzers(self) -> None:
        """Initialize all available sentiment analyzers with error handling"""
        self.analyzers_available = {
            'huggingface_api': bool(self.hf_api_key),
            'huggingface_local': HF_TRANSFORMERS_AVAILABLE,
            'vader': VADER_AVAILABLE,
            'textblob': TEXTBLOB_AVAILABLE
        }
        
        # Initialize VADER
        try:
            if VADER_AVAILABLE:
                self.vader_analyzer = SentimentIntensityAnalyzer()
                logger.info("✅ VADER analyzer initialized")
            else:
                logger.warning("⚠️  VADER not available")
        except Exception as e:
            logger.error(f"❌ Failed to initialize VADER: {e}")
            self.analyzers_available['vader'] = False
        
        # Initialize local HuggingFace model (optional)
        self.local_model = None
        self.local_tokenizer = None
        if HF_TRANSFORMERS_AVAILABLE:
            try:
                # Load model in background to avoid blocking
                self.executor.submit(self._load_local_model)
            except Exception as e:
                logger.warning(f"⚠️  Local HF model loading scheduled with potential issues: {e}")
        
        logger.info(f"📊 Available analyzers: {[k for k, v in self.analyzers_available.items() if v]}")
    
    def _load_local_model(self) -> None:
        """Load local HuggingFace model for offline analysis"""
        try:
            model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
            self.local_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.local_model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.analyzers_available['huggingface_local'] = True
            logger.info("✅ Local HuggingFace model loaded successfully")
        except Exception as e:
            logger.warning(f"⚠️  Could not load local HF model: {e}")
            self.analyzers_available['huggingface_local'] = False
    
    def _setup_session(self) -> None:
        """Setup HTTP session with security headers and timeouts"""
        self.session = requests.Session()
        
        # Security headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.hf_api_key}' if self.hf_api_key else '',
            'Content-Type': 'application/json',
            'User-Agent': 'SentimentAnalyzer/2.0 (Production)',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        })
        
        # Configure adapters for retry logic
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def _setup_caching(self) -> None:
        """Setup LRU cache for frequent requests"""
        self.cache = {}
        self.cache_order = []
        self.cache_timestamps = {}
        self.cache_ttl = 3600  # 1 hour TTL
    
    def _cache_key(self, text: str, method: str) -> str:
        """Generate cache key for text and method"""
        return hashlib.md5(f"{text}_{method}".encode()).hexdigest()
    
    def _get_from_cache(self, text: str, method: str) -> Optional[SentimentResult]:
        """Retrieve from cache if available and valid"""
        cache_key = self._cache_key(text, method)
        
        if cache_key in self.cache:
            # Check TTL
            if time.time() - self.cache_timestamps[cache_key] < self.cache_ttl:
                return self.cache[cache_key]
            else:
                # Remove expired entry
                self._remove_from_cache(cache_key)
        
        return None
    
    def _add_to_cache(self, text: str, method: str, result: SentimentResult) -> None:
        """Add result to cache with LRU eviction"""
        cache_key = self._cache_key(text, method)
        
        # Evict if cache is full
        if len(self.cache) >= self.cache_size:
            oldest_key = self.cache_order.pop(0)
            self._remove_from_cache(oldest_key)
        
        self.cache[cache_key] = result
        self.cache_timestamps[cache_key] = time.time()
        self.cache_order.append(cache_key)
    
    def _remove_from_cache(self, cache_key: str) -> None:
        """Remove item from cache"""
        if cache_key in self.cache:
            del self.cache[cache_key]
            del self.cache_timestamps[cache_key]
            if cache_key in self.cache_order:
                self.cache_order.remove(cache_key)
    
    def _validate_input(self, text: str) -> None:
        """Validate input text for security and format"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        if len(text.strip()) < self.min_text_length:
            raise ValueError(f"Text too short (minimum {self.min_text_length} characters)")
        
        if len(text) > self.max_text_length:
            raise ValueError(f"Text too long (maximum {self.max_text_length} characters)")
        
        # Basic security check for potential injection
        suspicious_patterns = ['<script', 'javascript:', 'data:', 'vbscript:']
        text_lower = text.lower()
        for pattern in suspicious_patterns:
            if pattern in text_lower:
                logger.warning(f"⚠️  Suspicious pattern detected: {pattern}")
    
    def _apply_rate_limiting(self) -> None:
        """Apply rate limiting to API requests"""
        with self.thread_lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
            self.request_count += 1
        self.min_request_interval = 0.1  # 100ms between requests
        
        logger.info("✅ Enhanced Sentiment Analyzer initialized successfully")
    
    def analyze_sentiment(self, text: str, method: str = 'auto') -> SentimentResult:
        """
        Enhanced sentiment analysis with comprehensive error handling and fallbacks
        
        Args:
            text: Text to analyze (1-5000 characters)
            method: Analysis method ('auto', 'huggingface_api', 'huggingface_local', 'vader', 'textblob', 'ensemble')
        
        Returns:
            SentimentResult object with comprehensive analysis results
        """
        
        Args:
            text: Text to analyze (1-5000 characters)
            method: Analysis method ('auto', 'huggingface_api', 'huggingface_local', 'vader', 'textblob', 'ensemble')
        
        Returns:
            SentimentResult object with comprehensive analysis results
        """
        start_time = time.time()
        
        try:
            # Input validation and security checks
            self._validate_input(text)
            text = text.strip()
            
            # Check cache first
            cached_result = self._get_from_cache(text, method)
            if cached_result:
                logger.debug(f"📋 Cache hit for method: {method}")
                return cached_result
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Determine method to use
            if method == 'auto':
                method = self._select_best_method()
            
            # Perform analysis with chosen method
            result = self._perform_analysis(cleaned_text, method, start_time)
            
            # Add to cache
            self._add_to_cache(text, method, result)
            
            # Log successful analysis
            logger.info(f"✅ Analysis completed: {method} -> {result.sentiment} ({result.confidence:.3f})")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Analysis failed: {e}")
            
            # Return fallback result with error details
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
        """Intelligently select the best available analysis method"""
        if self.analyzers_available['huggingface_api'] and self.hf_api_key:
            return 'huggingface_api'
        elif self.analyzers_available['huggingface_local'] and self.local_model:
            return 'huggingface_local'
        elif self.analyzers_available['vader']:
            return 'vader'
        elif self.analyzers_available['textblob']:
            return 'textblob'
        else:
            return 'basic_fallback'
    
    def _perform_analysis(self, text: str, method: str, start_time: float) -> SentimentResult:
        """Perform sentiment analysis with the specified method"""
        try:
            if method == 'huggingface_api':
                return self._analyze_with_huggingface_api(text, start_time)
            elif method == 'huggingface_local':
                return self._analyze_with_huggingface_local(text, start_time)
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
            # Try fallback method
            if method != 'vader' and self.analyzers_available['vader']:
                return self._analyze_with_vader(text, start_time)
            else:
                return self._analyze_with_basic_fallback(text, start_time)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove or replace problematic characters
        text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        
        # Basic HTML entity decoding
        html_entities = {
            '&amp;': '&', '&lt;': '<', '&gt;': '>', 
            '&quot;': '"', '&#39;': "'", '&nbsp;': ' '
        }
        for entity, char in html_entities.items():
            text = text.replace(entity, char)
        
        return text
    
    def _analyze_with_huggingface_api(self, text: str, start_time: float) -> SentimentResult:
        """Enhanced Hugging Face API analysis with better error handling"""
        if not self.hf_api_key:
            raise ValueError("No Hugging Face API key available")
        
        try:
            self._apply_rate_limiting()
            
            payload = {
                "inputs": text,
                "options": {
                    "wait_for_model": True,
                    "use_cache": False
                }
            }
            
            response = self.session.post(
                self.hf_api_url, 
                json=payload, 
                timeout=self.request_timeout
            )
            
            if response.status_code == 503:
                # Model loading, wait and retry
                logger.info("🔄 Model loading, retrying in 10 seconds...")
                time.sleep(10)
                response = self.session.post(self.hf_api_url, json=payload, timeout=self.request_timeout)
            
            response.raise_for_status()
            result_data = response.json()
            
            if isinstance(result_data, list) and len(result_data) > 0:
                return self._parse_huggingface_result(result_data, text, start_time, 'huggingface_api')
            else:
                raise ValueError("Invalid response format from API")
                
        except requests.exceptions.Timeout:
            logger.error("⏰ Hugging Face API timeout")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"🌐 HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Hugging Face API analysis failed: {e}")
            raise
    
    def _analyze_with_huggingface_local(self, text: str, start_time: float) -> SentimentResult:
        """Analyze using local Hugging Face model"""
        if not self.local_model or not self.local_tokenizer:
            raise ValueError("Local model not available")
        
        try:
            # Tokenize and predict
            inputs = self.local_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.local_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Convert to list format for parsing
            scores = predictions[0].tolist()
            result_data = [[
                {"label": "LABEL_0", "score": scores[0]},  # Negative
                {"label": "LABEL_1", "score": scores[1]},  # Neutral  
                {"label": "LABEL_2", "score": scores[2]}   # Positive
            ]]
            
            return self._parse_huggingface_result(result_data, text, start_time, 'huggingface_local')
            
        except Exception as e:
            logger.error(f"❌ Local Hugging Face analysis failed: {e}")
            raise
    
    def _parse_huggingface_result(self, result_data: List, text: str, start_time: float, model_type: str) -> SentimentResult:
        """Parse Hugging Face result format"""
        sentiment_scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        
        for item in result_data[0]:
            label = item['label'].upper()
            score = float(item['score'])
            
            # Correct mapping for sentiment labels
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
            model_used=model_type,
            processing_time=round(processing_time, 3),
            method=model_type,
            toxicity_score=self._estimate_toxicity(text)
        )
    
    def _analyze_with_vader(self, text: str, start_time: float) -> SentimentResult:
        """Enhanced VADER analysis"""
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
        """Enhanced TextBlob analysis"""
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
        
        # Try all available methods
        for method in ['huggingface_api', 'huggingface_local', 'vader', 'textblob']:
            if self.analyzers_available.get(method, False):
                try:
                    result = self._perform_analysis(text, method, start_time)
                    results.append(result)
                    methods_tried.append(method)
                except Exception as e:
                    logger.warning(f"⚠️  Ensemble method {method} failed: {e}")
        
        if not results:
            raise ValueError("No methods available for ensemble analysis")
        
        # Combine results using weighted average
        weights = {'huggingface_api': 0.4, 'huggingface_local': 0.35, 'vader': 0.15, 'textblob': 0.1}
        
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
        """Basic fallback analysis using simple keyword matching"""
        processing_time = time.time() - start_time
        
        # Simple keyword-based sentiment
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
            model_used="basic_fallback",
            processing_time=round(processing_time, 3),
            method="basic_fallback"
        )
    
    def _estimate_toxicity(self, text: str) -> float:
        """Basic toxicity estimation using keyword detection"""
        toxic_words = [
            'hate', 'stupid', 'idiot', 'moron', 'pathetic', 'disgusting', 
            'trash', 'garbage', 'worthless', 'useless', 'loser'
        ]
        
        text_lower = text.lower()
        toxic_count = sum(1 for word in toxic_words if word in text_lower)
        
        # Simple toxicity score based on toxic word frequency
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        toxicity_ratio = toxic_count / word_count
        return min(1.0, toxicity_ratio * 5)  # Scale and cap at 1.0
                        scores={k: round(v, 3) for k, v in sentiment_scores.items()},
                        model_used='huggingface-roberta',
                        processing_time=0.1,
                        emotion_scores=self._extract_emotions(text),
                        toxicity_score=self._estimate_toxicity(text),
                        method='huggingface_api'
                    )
            
            else:
                logger.warning(f"Hugging Face API error: {response.status_code} - {response.text}")
                return self._analyze_with_vader(text)
                
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            return self._analyze_with_vader(text)
    
    def _analyze_with_vader(self, text: str) -> SentimentResult:
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
            
            return SentimentResult(
                text=text[:200],
                sentiment=sentiment,
                confidence=round(min(confidence, 0.99), 3),
                scores={
                    'positive': round(scores['pos'], 3),
                    'negative': round(scores['neg'], 3),
                    'neutral': round(scores['neu'], 3)
                },
                model_used='vader',
                processing_time=0.01,
                emotion_scores=self._extract_emotions(text),
                toxicity_score=self._estimate_toxicity(text),
                method='vader'
            )
            
        except Exception as e:
            logger.error(f"VADER analysis error: {e}")
            return self._create_neutral_result(text)
    
    def _analyze_with_textblob(self, text: str) -> SentimentResult:
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
            
            return SentimentResult(
                text=text[:200],
                sentiment=sentiment,
                confidence=round(confidence, 3),
                scores={
                    'positive': round(pos_score, 3),
                    'negative': round(neg_score, 3),
                    'neutral': round(neu_score, 3)
                },
                model_used='textblob',
                processing_time=0.02,
                emotion_scores=self._extract_emotions(text),
                toxicity_score=self._estimate_toxicity(text),
                method='textblob'
            )
            
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
    
    def _create_neutral_result(self, text: str) -> SentimentResult:
        """Create a neutral result for fallback"""
        return SentimentResult(
            text=text[:200],
            sentiment='neutral',
            confidence=0.5,
            scores={
                'positive': 0.2,
                'negative': 0.2,
                'neutral': 0.6
            },
            model_used='fallback',
            processing_time=0.01,
            emotion_scores={'neutral': 0.8},
            toxicity_score=0.0,
            method='fallback'
        )

# Create global instance
real_sentiment_analyzer = RealSentimentAnalyzer()
