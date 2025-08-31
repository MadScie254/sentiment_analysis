"""
Comprehensive News Aggregator with 10+ Free APIs
Real implementation using the provided API keys
"""

import os
import requests
import feedparser
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
import time
from urllib.parse import urljoin, quote

logger = logging.getLogger(__name__)

class ComprehensiveNewsAggregator:
    """Real news aggregator using 10+ free news APIs"""
    
    def __init__(self):
        # API Keys from environment
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.gnews_key = os.getenv('GNEWS_API_KEY') 
        self.currents_key = os.getenv('CURRENTS_API_KEY')
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SentimentAnalysisDashboard/1.0 (Real News Aggregator)'
        })
        
        # Rate limiting
        self.last_request_time = {}
        self.min_request_interval = 1.0  # 1 second between requests
        
    def get_comprehensive_news(self, limit=50, category=None):
        """Get news from all available sources"""
        all_articles = []
        
        try:
            # 1. NewsAPI.org (Primary)
            if self.newsapi_key:
                articles = self._fetch_from_newsapi(limit//4, category)
                all_articles.extend(articles)
                logger.info(f"NewsAPI: Retrieved {len(articles)} articles")
            
            # 2. GNews.io 
            if self.gnews_key:
                articles = self._fetch_from_gnews(limit//4, category)
                all_articles.extend(articles)
                logger.info(f"GNews: Retrieved {len(articles)} articles")
                
            # 3. CurrentsAPI
            if self.currents_key:
                articles = self._fetch_from_currents(limit//4, category)
                all_articles.extend(articles)
                logger.info(f"Currents: Retrieved {len(articles)} articles")
            
            # 4. RSS Feeds (Multiple sources)
            rss_articles = self._fetch_from_rss_feeds(limit//4)
            all_articles.extend(rss_articles)
            logger.info(f"RSS Feeds: Retrieved {len(rss_articles)} articles")
            
            # 5. Free JSON APIs
            json_articles = self._fetch_from_json_apis(limit//10)
            all_articles.extend(json_articles)
            logger.info(f"JSON APIs: Retrieved {len(json_articles)} articles")
            
            # 6. MediaStack (Free tier)
            mediastack_articles = self._fetch_from_mediastack(limit//10)
            all_articles.extend(mediastack_articles)
            logger.info(f"MediaStack: Retrieved {len(mediastack_articles)} articles")
            
            # Remove duplicates and sort by timestamp
            unique_articles = self._deduplicate_articles(all_articles)
            unique_articles.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            logger.info(f"Total unique articles retrieved: {len(unique_articles)}")
            return unique_articles[:limit]
            
        except Exception as e:
            logger.error(f"Error in comprehensive news fetch: {e}")
            return self._get_fallback_news()
    
    def _fetch_from_newsapi(self, limit, category=None):
        """Fetch from NewsAPI.org"""
        try:
            self._rate_limit('newsapi')
            
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.newsapi_key,
                'country': 'us',
                'pageSize': min(limit, 100),
                'sortBy': 'publishedAt'
            }
            
            if category:
                params['category'] = category
                
            response = self._make_request(url, params)
            if not response:
                return []
                
            articles = []
            for article in response.get('articles', []):
                if self._is_valid_article(article):
                    articles.append({
                        'title': article['title'],
                        'summary': self._clean_text(article.get('description', '')),
                        'url': article.get('url', ''),
                        'source': f"NewsAPI - {article.get('source', {}).get('name', 'Unknown')}",
                        'timestamp': self._parse_timestamp(article.get('publishedAt')),
                        'image_url': article.get('urlToImage', ''),
                        'author': article.get('author', ''),
                        'category': category or 'general'
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []
    
    def _fetch_from_gnews(self, limit, category=None):
        """Fetch from GNews.io"""
        try:
            self._rate_limit('gnews')
            
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': self.gnews_key,
                'lang': 'en',
                'country': 'us',
                'max': min(limit, 10),  # GNews free tier limit
                'sortby': 'publishedAt'
            }
            
            if category:
                params['category'] = category
                
            response = self._make_request(url, params)
            if not response:
                return []
                
            articles = []
            for article in response.get('articles', []):
                if self._is_valid_article(article):
                    articles.append({
                        'title': article['title'],
                        'summary': self._clean_text(article.get('description', '')),
                        'url': article.get('url', ''),
                        'source': f"GNews - {article.get('source', {}).get('name', 'Unknown')}",
                        'timestamp': self._parse_timestamp(article.get('publishedAt')),
                        'image_url': article.get('image', ''),
                        'author': '',
                        'category': category or 'general'
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"GNews error: {e}")
            return []
    
    def _fetch_from_currents(self, limit, category=None):
        """Fetch from CurrentsAPI"""
        try:
            self._rate_limit('currents')
            
            url = "https://api.currentsapi.services/v1/latest-news"
            params = {
                'apiKey': self.currents_key,
                'language': 'en',
                'page_size': min(limit, 200)
            }
            
            if category:
                params['category'] = category
                
            response = self._make_request(url, params)
            if not response:
                return []
                
            articles = []
            for article in response.get('news', []):
                if self._is_valid_article(article):
                    articles.append({
                        'title': article['title'],
                        'summary': self._clean_text(article.get('description', '')),
                        'url': article.get('url', ''),
                        'source': f"Currents - {article.get('author', 'Unknown')}",
                        'timestamp': self._parse_timestamp(article.get('published')),
                        'image_url': article.get('image', ''),
                        'author': article.get('author', ''),
                        'category': category or 'general'
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"Currents error: {e}")
            return []
    
    def _fetch_from_rss_feeds(self, limit):
        """Fetch from multiple RSS feeds (Free sources)"""
        rss_feeds = [
            'https://feeds.reuters.com/reuters/topNews',
            'https://feeds.bbci.co.uk/news/rss.xml',
            'https://rss.cnn.com/rss/edition.rss',
            'https://feeds.npr.org/1001/rss.xml',
            'https://feeds.washingtonpost.com/rss/national',
            'https://feeds.foxnews.com/foxnews/latest',
            'https://feeds.abcnews.go.com/abcnews/topstories',
            'https://feeds.nbcnews.com/nbcnews/public/news',
            'https://feeds.skynews.com/feeds/rss/home.xml',
            'https://feeds.feedburner.com/time/topstories'
        ]
        
        all_articles = []
        articles_per_feed = max(1, limit // len(rss_feeds))
        
        for feed_url in rss_feeds:
            try:
                self._rate_limit(f'rss_{feed_url}')
                
                feed = feedparser.parse(feed_url)
                source_name = feed.feed.get('title', 'RSS Feed')
                
                for entry in feed.entries[:articles_per_feed]:
                    if hasattr(entry, 'title') and hasattr(entry, 'summary'):
                        all_articles.append({
                            'title': entry.title,
                            'summary': self._clean_text(entry.summary),
                            'url': entry.get('link', ''),
                            'source': f"RSS - {source_name}",
                            'timestamp': self._parse_timestamp(entry.get('published')),
                            'image_url': '',
                            'author': entry.get('author', ''),
                            'category': 'rss'
                        })
                        
            except Exception as e:
                logger.error(f"RSS feed error for {feed_url}: {e}")
                continue
        
        return all_articles
    
    def _fetch_from_json_apis(self, limit):
        """Fetch from free JSON news APIs"""
        apis = [
            'https://jsonplaceholder.typicode.com/posts',  # Mock API for testing
            'https://hacker-news.firebaseio.com/v0/topstories.json'  # Hacker News API
        ]
        
        articles = []
        
        # Hacker News API
        try:
            self._rate_limit('hackernews')
            
            # Get top story IDs
            response = self._make_request('https://hacker-news.firebaseio.com/v0/topstories.json')
            if response and isinstance(response, list):
                story_ids = response[:limit]
                
                for story_id in story_ids:
                    try:
                        story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
                        story = self._make_request(story_url)
                        
                        if story and story.get('type') == 'story' and story.get('title'):
                            articles.append({
                                'title': story['title'],
                                'summary': story.get('text', story['title'])[:200] + '...',
                                'url': story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                                'source': 'Hacker News',
                                'timestamp': self._parse_timestamp(story.get('time')),
                                'image_url': '',
                                'author': story.get('by', ''),
                                'category': 'tech'
                            })
                    except Exception as e:
                        continue
                        
        except Exception as e:
            logger.error(f"Hacker News API error: {e}")
        
        return articles
    
    def _fetch_from_mediastack(self, limit):
        """Fetch from MediaStack (free tier available)"""
        # MediaStack requires registration for API key
        # This is a placeholder for when you get a free API key
        try:
            # Free tier: 500 requests/month
            # Register at: https://mediastack.com/
            mediastack_key = os.getenv('MEDIASTACK_API_KEY')
            
            if not mediastack_key:
                return []
                
            self._rate_limit('mediastack')
            
            url = "http://api.mediastack.com/v1/news"
            params = {
                'access_key': mediastack_key,
                'countries': 'us',
                'limit': min(limit, 25),  # Free tier limit
                'sort': 'published_desc'
            }
            
            response = self._make_request(url, params)
            if not response:
                return []
                
            articles = []
            for article in response.get('data', []):
                if self._is_valid_article(article):
                    articles.append({
                        'title': article['title'],
                        'summary': self._clean_text(article.get('description', '')),
                        'url': article.get('url', ''),
                        'source': f"MediaStack - {article.get('source', 'Unknown')}",
                        'timestamp': self._parse_timestamp(article.get('published_at')),
                        'image_url': article.get('image', ''),
                        'author': article.get('author', ''),
                        'category': article.get('category', 'general')
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"MediaStack error: {e}")
            return []
    
    def _make_request(self, url, params=None):
        """Make HTTP request with error handling"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Request error for {url}: {e}")
            return None
    
    def _rate_limit(self, source):
        """Simple rate limiting"""
        now = time.time()
        last_time = self.last_request_time.get(source, 0)
        
        if now - last_time < self.min_request_interval:
            time.sleep(self.min_request_interval - (now - last_time))
        
        self.last_request_time[source] = time.time()
    
    def _is_valid_article(self, article):
        """Check if article has required fields"""
        return (
            article.get('title') and 
            len(article.get('title', '')) > 10 and
            article.get('title') != '[Removed]'
        )
    
    def _clean_text(self, text):
        """Clean and truncate text"""
        if not text:
            return ''
        
        # Remove HTML tags and clean up
        import re
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        text = ' '.join(text.split())  # Normalize whitespace
        
        # Truncate if too long
        if len(text) > 300:
            text = text[:297] + '...'
        
        return text
    
    def _parse_timestamp(self, timestamp):
        """Parse various timestamp formats"""
        if not timestamp:
            return datetime.now().isoformat()
        
        try:
            # Unix timestamp
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp).isoformat()
            
            # ISO format
            if isinstance(timestamp, str):
                # Try different formats
                formats = [
                    '%Y-%m-%dT%H:%M:%SZ',
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                    '%Y-%m-%d %H:%M:%S',
                    '%a, %d %b %Y %H:%M:%S %Z',
                    '%a, %d %b %Y %H:%M:%S %z'
                ]
                
                for fmt in formats:
                    try:
                        return datetime.strptime(timestamp, fmt).isoformat()
                    except:
                        continue
            
            return datetime.now().isoformat()
            
        except Exception:
            return datetime.now().isoformat()
    
    def _deduplicate_articles(self, articles):
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').lower().strip()
            
            # Create a simple hash for similarity checking
            title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
            
            if title_hash not in seen_titles and len(title) > 10:
                seen_titles.add(title_hash)
                unique_articles.append(article)
        
        return unique_articles
    
    def _get_fallback_news(self):
        """Fallback news when APIs fail"""
        return [
            {
                'title': 'Global Markets Show Mixed Signals',
                'summary': 'International markets display varied performance as investors react to recent economic indicators and policy changes.',
                'url': 'https://example.com/market-news',
                'source': 'Fallback News',
                'timestamp': datetime.now().isoformat(),
                'image_url': '',
                'author': 'News Team',
                'category': 'business'
            },
            {
                'title': 'Technology Sector Advances Continue',
                'summary': 'Leading technology companies report strong quarterly results, driving continued optimism in the sector.',
                'url': 'https://example.com/tech-news',
                'source': 'Fallback News',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'image_url': '',
                'author': 'Tech Reporter',
                'category': 'technology'
            }
        ]

# Create global instance
comprehensive_news_aggregator = ComprehensiveNewsAggregator()
