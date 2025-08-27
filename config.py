# Advanced Configuration for SentimentAI Platform
import os
from datetime import timedelta

class Config:
    """Comprehensive configuration settings for the sentiment analysis system"""
    
    # === CORE APPLICATION SETTINGS ===
    APP_NAME = "SentimentAI"
    APP_VERSION = "2.0.0"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    
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
    
    # === SERVER CONFIGURATION ===
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    MAIN_HOST = "localhost"
    MAIN_PORT = 5003
    WEBSOCKET_HOST = "localhost"
    WEBSOCKET_PORT = 8765
    DEBUG_MODE = True
    
    # === DATABASE SETTINGS ===
    DATABASE_PATH = os.getenv("DATABASE_PATH", "sentiment_analytics.db")
    DB_POOL_SIZE = 10
    DB_TIMEOUT = 30
    
    # === CACHE CONFIGURATION ===
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_LONG_TIMEOUT = 3600    # 1 hour
    CACHE_SHORT_TIMEOUT = 60     # 1 minute
    
    # === API INTEGRATION SETTINGS ===
    API_RATE_LIMIT = 100  # requests per minute
    API_TIMEOUT = 30      # seconds
    API_RETRY_ATTEMPTS = 3
    
    # === EXTERNAL API ENDPOINTS ===
    EXTERNAL_APIS = {
        'hackernews': {
            'base_url': 'https://hacker-news.firebaseio.com/v0',
            'endpoints': {
                'top_stories': '/topstories.json',
                'item': '/item/{}.json'
            }
        },
        'reddit': {
            'base_url': 'https://www.reddit.com',
            'endpoints': {
                'hot': '/r/{}/hot.json',
                'new': '/r/{}/new.json'
            }
        },
        'github': {
            'base_url': 'https://api.github.com',
            'endpoints': {
                'trending': '/search/repositories'
            }
        },
        'coingecko': {
            'base_url': 'https://api.coingecko.com/api/v3',
            'endpoints': {
                'trending': '/search/trending',
                'prices': '/simple/price'
            }
        },
        'quotable': {
            'base_url': 'https://api.quotable.io',
            'endpoints': {
                'random': '/random',
                'quotes': '/quotes'
            }
        },
        'news': {
            'base_url': 'https://newsapi.org/v2',
            'endpoints': {
                'top_headlines': '/top-headlines',
                'everything': '/everything'
            },
            'api_key': os.getenv("NEWS_API_KEY", "")
        }
    }
    
    # === REAL-TIME FEATURES ===
    WEBSOCKET_PING_INTERVAL = 30
    WEBSOCKET_PING_TIMEOUT = 10
    REALTIME_UPDATE_INTERVAL = 5  # seconds
    
    # === UI THEME CONFIGURATION ===
    UI_THEME = {
        'primary_color': '#6366f1',
        'secondary_color': '#8b5cf6',
        'accent_color': '#06b6d4',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'glass_background': 'rgba(255, 255, 255, 0.1)',
        'glass_border': 'rgba(255, 255, 255, 0.2)',
        'text_primary': '#ffffff',
        'text_secondary': 'rgba(255, 255, 255, 0.8)',
        'success_color': '#10b981',
        'warning_color': '#f59e0b',
        'error_color': '#ef4444'
    }
    
    # === ANIMATION SETTINGS ===
    ANIMATIONS = {
        'transition_duration': '0.3s',
        'transition_timing': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'hover_scale': '1.05',
        'active_scale': '0.95',
        'fade_duration': '0.5s',
        'slide_duration': '0.4s',
        'bounce_duration': '0.6s'
    }
    
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
    
    # === FREE API CONFIGURATIONS ===
    FREE_APIS = {
        'hackernews': {
            'base_url': 'https://hacker-news.firebaseio.com/v0',
            'endpoints': {
                'top_stories': '/topstories.json',
                'item': '/item/{}.json'
            }
        },
        'reddit': {
            'base_url': 'https://www.reddit.com',
            'endpoints': {
                'hot': '/r/{}/hot.json',
                'new': '/r/{}/new.json'
            }
        },
        'github': {
            'base_url': 'https://api.github.com',
            'endpoints': {
                'trending': '/search/repositories'
            }
        },
        'coingecko': {
            'base_url': 'https://api.coingecko.com/api/v3',
            'endpoints': {
                'trending': '/search/trending',
                'prices': '/simple/price'
            }
        },
        'quotable': {
            'base_url': 'https://api.quotable.io',
            'endpoints': {
                'random': '/random',
                'quotes': '/quotes'
            }
        },
        'jsonplaceholder': {
            'base_url': 'https://jsonplaceholder.typicode.com',
            'endpoints': {
                'posts': '/posts',
                'comments': '/comments'
            }
        }
    }
    
    # === SAMPLE DATA FOR FALLBACKS ===
    SAMPLE_DATA = {
        'news_headlines': [
            {
                'title': 'Breaking: Major technological breakthrough announced',
                'url': 'https://example.com/tech-breakthrough',
                'source': 'TechNews'
            },
            {
                'title': 'Global markets show positive trends this quarter',
                'url': 'https://example.com/market-trends',
                'source': 'FinanceDaily'
            },
            {
                'title': 'New environmental protection measures implemented',
                'url': 'https://example.com/environment',
                'source': 'EcoNews'
            }
        ],
        'reddit_posts': [
            {
                'title': 'Amazing new discovery in artificial intelligence',
                'subreddit': 'technology',
                'url': 'https://reddit.com/r/technology/sample1'
            },
            {
                'title': 'Scientists make breakthrough in renewable energy',
                'subreddit': 'science',
                'url': 'https://reddit.com/r/science/sample1'
            }
        ],
        'crypto_trending': [
            {
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'rank': 1,
                'description': 'The original cryptocurrency'
            },
            {
                'name': 'Ethereum',
                'symbol': 'ETH',
                'rank': 2,
                'description': 'Smart contract platform'
            }
        ],
        'quotes': [
            {
                'content': 'Innovation distinguishes between a leader and a follower.',
                'author': 'Steve Jobs'
            },
            {
                'content': 'The future belongs to those who believe in the beauty of their dreams.',
                'author': 'Eleanor Roosevelt'
            }
        ]
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
