# Sentiment Analysis Configuration
import os

class Config:
    """Configuration settings for the sentiment analysis system"""
    
    # Model settings
    SENTIMENT_THRESHOLD_POSITIVE = 0.6
    SENTIMENT_THRESHOLD_NEGATIVE = 0.6
    EMOTION_CONFIDENCE_THRESHOLD = 0.3
    SPAM_DETECTION_THRESHOLD = 0.4
    
    # Language settings
    SUPPORTED_LANGUAGES = ['en', 'sw']  # English and Swahili
    DEFAULT_LANGUAGE = 'en'
    
    # Processing settings
    MAX_TEXT_LENGTH = 5000
    MAX_COMMENTS_BATCH = 100
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG_MODE = True
    
    # Swahili language support
    SWAHILI_WORDS = {
        'positive': [
            'poa', 'sawa', 'vizuri', 'nzuri', 'karibu', 'asante', 'baraka',
            'furaha', 'raha', 'upendo', 'mapenzi', 'heri', 'amani', 'mzuri',
            'safi', 'bomba', 'top', 'fresh', 'kali', 'sweet'
        ],
        'negative': [
            'mbaya', 'vibaya', 'hasira', 'uchungu', 'mateso', 'maumivu',
            'machozi', 'huzuni', 'wasiwasi', 'hofu', 'hatari', 'ovu',
            'chafu', 'mbovu', 'bure'
        ],
        'neutral': [
            'sawa tu', 'normal', 'kawaida', 'si vibaya', 'si nzuri'
        ]
    }
    
    # Kenyan internet slang
    KENYAN_SLANG = {
        'poa': 'cool good',
        'sawa': 'okay good',
        'mambo': 'what is up',
        'niaje': 'how are you',
        'vipi': 'how',
        'uko poa': 'you are cool',
        'mzee': 'elder person',
        'kijana': 'young person',
        'msee': 'person guy',
        'dem': 'girl lady',
        'buda': 'friend buddy',
        'maze': 'friend buddy',
        'kuna noma': 'there is trouble',
        'si mchezo': 'not a joke serious',
        'wacha mchezo': 'stop joking',
        'umenishinda': 'you have defeated me',
        'utanipea': 'will you give me'
    }
    
    # Comment classification weights
    CLASSIFICATION_WEIGHTS = {
        'keyword_weight': 0.6,
        'emoji_weight': 0.3,
        'pattern_weight': 0.4,
        'sentiment_boost': 0.2,
        'emotion_boost': 0.15
    }
    
    # Toxicity levels
    TOXICITY_LEVELS = {
        'safe': {'min': 0.0, 'max': 0.3},
        'moderate': {'min': 0.3, 'max': 0.7},
        'high': {'min': 0.7, 'max': 1.0}
    }

# Environment-specific configuration
class DevelopmentConfig(Config):
    DEBUG_MODE = True
    API_HOST = "127.0.0.1"

class ProductionConfig(Config):
    DEBUG_MODE = False
    API_HOST = "0.0.0.0"
    MAX_COMMENTS_BATCH = 500

# Configuration factory
def get_config():
    env = os.getenv('ENVIRONMENT', 'development').lower()
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()
