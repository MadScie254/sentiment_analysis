"""
Real News Scraper for Live Sentiment Analysis
Fetches news from multiple sources and performs sentiment analysis
"""

import requests
import feedparser
import newspaper
from newspaper import Article
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin, urlparse
import json

class RealNewsScaper:
    """
    Real news scraper that fetches news from multiple sources
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # News sources with RSS feeds
        self.rss_sources = {
            'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
            'Reuters': 'http://feeds.reuters.com/reuters/topNews',
            'CNN': 'http://rss.cnn.com/rss/edition.rss',
            'Guardian': 'https://www.theguardian.com/world/rss',
            'TechCrunch': 'https://techcrunch.com/feed/',
            'Hacker News': 'https://hnrss.org/frontpage',
            'NPR': 'https://feeds.npr.org/1001/rss.xml',
            'Associated Press': 'https://feeds.apnews.com/6ca0274c90314b168eb9fee7294152eb',
            'Financial Times': 'https://www.ft.com/news-feed',
            'Bloomberg': 'https://feeds.bloomberg.com/markets/news.rss'
        }
        
        # News API sources (requires API keys)
        self.api_sources = {
            'newsapi': 'https://newsapi.org/v2/top-headlines',
            'gnews': 'https://gnews.io/api/v4/top-headlines',
            'currents': 'https://api.currentsapi.services/v1/latest-news'
        }
        
        # Request headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Cache for avoiding duplicate articles
        self.seen_urls = set()
        
    def fetch_from_rss(self, source_name: str, limit: int = 10) -> List[Dict]:
        """Fetch news from RSS feed"""
        articles = []
        
        try:
            if source_name not in self.rss_sources:
                self.logger.warning(f"Unknown RSS source: {source_name}")
                return articles
            
            rss_url = self.rss_sources[source_name]
            self.logger.info(f"Fetching from {source_name}: {rss_url}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                self.logger.warning(f"RSS feed error for {source_name}: {feed.bozo_exception}")
            
            for entry in feed.entries[:limit]:
                if entry.link in self.seen_urls:
                    continue
                
                article_data = {
                    'title': entry.get('title', 'No title'),
                    'url': entry.link,
                    'description': entry.get('summary', ''),
                    'published': self._parse_date(entry.get('published')),
                    'source': source_name,
                    'category': self._extract_category(entry),
                    'content': None,  # Will be fetched separately
                    'sentiment': None,
                    'confidence': None
                }
                
                # Try to extract full content
                try:
                    full_content = self._extract_full_content(entry.link)
                    if full_content:
                        article_data['content'] = full_content
                except Exception as e:
                    self.logger.debug(f"Could not extract content from {entry.link}: {e}")
                
                articles.append(article_data)
                self.seen_urls.add(entry.link)
                
                # Add delay to be respectful
                time.sleep(random.uniform(0.5, 1.5))
            
            self.logger.info(f"Fetched {len(articles)} articles from {source_name}")
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS from {source_name}: {str(e)}")
        
        return articles
    
    def fetch_from_newsapi(self, api_key: str, country: str = 'us', category: str = None, limit: int = 10) -> List[Dict]:
        """Fetch news from NewsAPI.org"""
        articles = []
        
        try:
            url = self.api_sources['newsapi']
            params = {
                'apiKey': api_key,
                'country': country,
                'pageSize': limit
            }
            
            if category:
                params['category'] = category
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok':
                self.logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return articles
            
            for article in data['articles']:
                if article['url'] in self.seen_urls:
                    continue
                
                article_data = {
                    'title': article.get('title', 'No title'),
                    'url': article['url'],
                    'description': article.get('description', ''),
                    'published': self._parse_date(article.get('publishedAt')),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'category': category or 'general',
                    'content': article.get('content', ''),
                    'image_url': article.get('urlToImage'),
                    'sentiment': None,
                    'confidence': None
                }
                
                articles.append(article_data)
                self.seen_urls.add(article['url'])
            
            self.logger.info(f"Fetched {len(articles)} articles from NewsAPI")
            
        except Exception as e:
            self.logger.error(f"Error fetching from NewsAPI: {str(e)}")
        
        return articles
    
    def fetch_all_sources(self, limit_per_source: int = 5) -> List[Dict]:
        """Fetch news from all available RSS sources"""
        all_articles = []
        
        for source_name in self.rss_sources.keys():
            try:
                articles = self.fetch_from_rss(source_name, limit_per_source)
                all_articles.extend(articles)
                
                # Add delay between sources
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                self.logger.error(f"Error fetching from {source_name}: {str(e)}")
                continue
        
        # Sort by publication date
        all_articles.sort(key=lambda x: x.get('published') or datetime.min, reverse=True)
        
        self.logger.info(f"Fetched total of {len(all_articles)} articles from all sources")
        return all_articles
    
    def search_news(self, query: str, language: str = 'en', limit: int = 20) -> List[Dict]:
        """Search for news articles containing specific keywords"""
        articles = []
        
        # Search in RSS feeds
        for source_name in self.rss_sources.keys():
            try:
                source_articles = self.fetch_from_rss(source_name, limit * 2)
                
                # Filter articles containing the query
                matching_articles = [
                    article for article in source_articles
                    if query.lower() in article['title'].lower() or 
                       query.lower() in article.get('description', '').lower()
                ]
                
                articles.extend(matching_articles[:limit // len(self.rss_sources)])
                
            except Exception as e:
                self.logger.error(f"Error searching in {source_name}: {str(e)}")
                continue
        
        return articles[:limit]
    
    def _extract_full_content(self, url: str) -> Optional[str]:
        """Extract full article content using newspaper3k"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            if len(article.text) > 100:  # Minimum content length
                return article.text
            
        except Exception as e:
            self.logger.debug(f"Newspaper3k failed for {url}: {e}")
        
        # Fallback to BeautifulSoup
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try common content selectors
            content_selectors = [
                'article', '.article-content', '.post-content', '.entry-content',
                '.content', '.story-content', '.article-body', 'main'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    text = content_elem.get_text(strip=True)
                    if len(text) > 200:
                        return text
            
            # Fallback to all paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            if len(text) > 200:
                return text
                
        except Exception as e:
            self.logger.debug(f"BeautifulSoup failed for {url}: {e}")
        
        return None
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_string:
            return None
        
        # Common date formats
        formats = [
            '%a, %d %b %Y %H:%M:%S %Z',
            '%a, %d %b %Y %H:%M:%S %z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_string.strip(), fmt)
            except ValueError:
                continue
        
        # Try parsing with dateutil as fallback
        try:
            from dateutil.parser import parse
            return parse(date_string)
        except:
            pass
        
        self.logger.debug(f"Could not parse date: {date_string}")
        return None
    
    def _extract_category(self, entry) -> str:
        """Extract category from RSS entry"""
        # Try to get category from tags
        if hasattr(entry, 'tags') and entry.tags:
            return entry.tags[0].get('term', 'general')
        
        # Try to get from category field
        if hasattr(entry, 'category'):
            return entry.category
        
        # Extract from URL or title
        url_lower = entry.link.lower()
        title_lower = entry.get('title', '').lower()
        
        categories = {
            'technology': ['tech', 'technology', 'digital', 'ai', 'software'],
            'business': ['business', 'finance', 'economy', 'market', 'stock'],
            'politics': ['politics', 'government', 'election', 'policy'],
            'sports': ['sport', 'football', 'basketball', 'soccer', 'tennis'],
            'health': ['health', 'medical', 'disease', 'medicine', 'covid'],
            'science': ['science', 'research', 'study', 'discovery'],
            'entertainment': ['entertainment', 'movie', 'music', 'celebrity'],
            'world': ['world', 'international', 'global', 'foreign']
        }
        
        for category, keywords in categories.items():
            if any(keyword in url_lower or keyword in title_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def get_trending_topics(self, articles: List[Dict], min_mentions: int = 3) -> List[Dict]:
        """Extract trending topics from articles"""
        word_counts = {}
        
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'says', 'said', 'news'
        }
        
        for article in articles:
            text = f"{article['title']} {article.get('description', '')}"
            words = text.lower().split()
            
            for word in words:
                # Clean word
                word = ''.join(char for char in word if char.isalnum())
                
                if len(word) > 3 and word not in stop_words:
                    word_counts[word] = word_counts.get(word, 0) + 1
        
        # Get trending topics
        trending = [
            {'topic': word, 'mentions': count}
            for word, count in word_counts.items()
            if count >= min_mentions
        ]
        
        # Sort by mentions
        trending.sort(key=lambda x: x['mentions'], reverse=True)
        
        return trending[:20]  # Top 20 trending topics
    
    def analyze_sentiment_trends(self, articles: List[Dict]) -> Dict:
        """Analyze sentiment trends across articles"""
        if not articles:
            return {'error': 'No articles to analyze'}
        
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        category_sentiment = {}
        source_sentiment = {}
        
        total_confidence = 0
        analyzed_count = 0
        
        for article in articles:
            sentiment = article.get('sentiment')
            confidence = article.get('confidence', 0)
            category = article.get('category', 'general')
            source = article.get('source', 'unknown')
            
            if sentiment:
                sentiment_counts[sentiment] += 1
                total_confidence += confidence
                analyzed_count += 1
                
                # Category sentiment
                if category not in category_sentiment:
                    category_sentiment[category] = {'positive': 0, 'negative': 0, 'neutral': 0, 'count': 0}
                category_sentiment[category][sentiment] += 1
                category_sentiment[category]['count'] += 1
                
                # Source sentiment
                if source not in source_sentiment:
                    source_sentiment[source] = {'positive': 0, 'negative': 0, 'neutral': 0, 'count': 0}
                source_sentiment[source][sentiment] += 1
                source_sentiment[source]['count'] += 1
        
        avg_confidence = total_confidence / analyzed_count if analyzed_count > 0 else 0
        
        return {
            'overall_sentiment': sentiment_counts,
            'average_confidence': round(avg_confidence, 3),
            'category_breakdown': category_sentiment,
            'source_breakdown': source_sentiment,
            'total_articles': len(articles),
            'analyzed_articles': analyzed_count
        }

# Example usage function
def get_sample_news_data(limit: int = 20) -> List[Dict]:
    """Get sample news data for testing"""
    scraper = RealNewsScaper()
    
    # Try to fetch real news, fallback to sample data
    try:
        articles = scraper.fetch_all_sources(limit_per_source=3)
        if articles:
            return articles[:limit]
    except Exception as e:
        logging.error(f"Could not fetch real news: {e}")
    
    # Fallback sample data
    sample_articles = [
        {
            'title': 'Tech Giants Report Strong Quarterly Earnings',
            'url': 'https://example.com/tech-earnings',
            'description': 'Major technology companies exceeded expectations in their latest quarterly reports.',
            'published': datetime.now() - timedelta(hours=2),
            'source': 'TechNews',
            'category': 'technology',
            'content': 'Technology companies including Apple, Google, and Microsoft have reported strong quarterly earnings that exceeded analyst expectations...',
            'sentiment': 'positive',
            'confidence': 0.87
        },
        {
            'title': 'Global Climate Summit Reaches Historic Agreement',
            'url': 'https://example.com/climate-summit',
            'description': 'World leaders agree on new measures to combat climate change.',
            'published': datetime.now() - timedelta(hours=5),
            'source': 'GlobalNews',
            'category': 'world',
            'content': 'The international climate summit concluded with a historic agreement among 195 countries to reduce carbon emissions...',
            'sentiment': 'positive',
            'confidence': 0.92
        },
        {
            'title': 'Market Volatility Concerns Investors',
            'url': 'https://example.com/market-volatility',
            'description': 'Stock markets experience significant fluctuations amid economic uncertainty.',
            'published': datetime.now() - timedelta(hours=8),
            'source': 'Financial Times',
            'category': 'business',
            'content': 'Stock markets around the world have experienced significant volatility as investors react to mixed economic signals...',
            'sentiment': 'negative',
            'confidence': 0.79
        }
    ]
    
    return sample_articles

# Global instance
news_scraper = RealNewsScaper()
