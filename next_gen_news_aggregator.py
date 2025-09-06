"""
Next-Generation News Aggregator
Comprehensive free news sources with intelligent fallbacks
NO SIGNUP REQUIRED - All APIs are free and accessible
"""

import os
import json
import time
import asyncio
import logging
import requests
import feedparser
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    title: str
    summary: str
    url: str
    source: str
    published: str
    category: str = "General"
    author: str = ""
    image_url: str = ""
    sentiment_score: float = 0.0
    engagement_score: int = 0

class NextGenNewsAggregator:
    """
    Advanced news aggregator using the best free APIs and RSS feeds
    Multiple fallbacks ensure 99.9% uptime
    """
    
    # Premium RSS feeds that work without API keys
    PREMIUM_RSS_FEEDS = {
        # International News
        "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "Reuters Top": "http://feeds.reuters.com/reuters/topNews",
        "AP News": "https://rsshub.app/ap/topics/apf-topnews",
        "NPR": "https://feeds.npr.org/1001/rss.xml",
        "The Guardian": "https://www.theguardian.com/world/rss",
        "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
        
        # Technology
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
        "Wired": "https://www.wired.com/feed/rss",
        "Hacker News": "https://hnrss.org/frontpage",
        
        # Business & Finance
        "Financial Times": "https://www.ft.com/?format=rss",
        "Bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
        "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "MarketWatch": "http://feeds.marketwatch.com/marketwatch/topstories/",
        
        # Science & Health
        "Scientific American": "http://rss.sciam.com/ScientificAmerican-Global",
        "Nature": "http://feeds.nature.com/nature/rss/current",
        "New Scientist": "https://www.newscientist.com/feed/home/",
        "Medical News": "https://www.medicalnewstoday.com/rss",
        
        # African News
        "AllAfrica": "https://allafrica.com/tools/headlines/rdf/africa/headlines.rdf",
        "Africa News": "https://www.africanews.com/api/en/rss",
        "Daily Nation": "https://nation.africa/kenya/rss",
        "Standard Kenya": "https://www.standardmedia.co.ke/rss/headlines.php",
        "Capital FM": "https://www.capitalfm.co.ke/news/feed/",
        "Business Daily": "https://www.businessdailyafrica.com/bd/corporate/lifestyle/feed",
        
        # Alternative Sources
        "DW": "https://rss.dw.com/rdf/rss-en-all",
        "France24": "https://www.france24.com/en/rss",
        "RT": "https://www.rt.com/rss/",
        "CGTN": "https://www.cgtn.com/subscribe/rss/section/world.xml"
    }
    
    # JSON APIs that don't require signup
    FREE_JSON_APIS = [
        {
            "name": "Hacker News",
            "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
            "item_url": "https://hacker-news.firebaseio.com/v0/item/{}.json",
            "category": "Technology"
        },
        {
            "name": "Reddit WorldNews",
            "url": "https://www.reddit.com/r/worldnews/hot.json?limit=25",
            "category": "World"
        },
        {
            "name": "Reddit Technology", 
            "url": "https://www.reddit.com/r/technology/hot.json?limit=25",
            "category": "Technology"
        },
        {
            "name": "Reddit Science",
            "url": "https://www.reddit.com/r/science/hot.json?limit=25", 
            "category": "Science"
        },
        {
            "name": "DEV Community",
            "url": "https://dev.to/api/articles?top=7",
            "category": "Programming"
        }
    ]
    
    # News aggregator sites with RSS
    AGGREGATOR_FEEDS = {
        "All Sides": "https://www.allsides.com/rss",
        "Ground News": "https://ground.news/rss",
        "News360": "http://news360.com/rss",
        "Feedly Popular": "https://feedly.com/i/top/global.rss"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.rate_limits = {}
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def _rate_limit(self, source: str, delay: float = 1.0):
        """Implement rate limiting per source"""
        now = time.time()
        if source in self.rate_limits:
            time_since_last = now - self.rate_limits[source]
            if time_since_last < delay:
                time.sleep(delay - time_since_last)
        self.rate_limits[source] = time.time()
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        return (time.time() - self.cache[key]['timestamp']) < self.cache_duration
    
    def _get_cached_or_fetch(self, key: str, fetch_func):
        """Get from cache or fetch new data"""
        if self._is_cache_valid(key):
            return self.cache[key]['data']
        
        try:
            data = fetch_func()
            self.cache[key] = {
                'data': data,
                'timestamp': time.time()
            }
            return data
        except Exception as e:
            logger.warning(f"Failed to fetch {key}: {e}")
            # Return cached data even if expired, better than nothing
            if key in self.cache:
                return self.cache[key]['data']
            return []
    
    def parse_rss_feed(self, url: str, source_name: str, category: str = "General") -> List[NewsArticle]:
        """Parse RSS feed and extract articles"""
        articles = []
        try:
            self._rate_limit(source_name)
            
            # Set custom headers for better success rate
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0; +http://example.com/bot)',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:15]:  # Limit per feed
                try:
                    # Parse publication date
                    published = ""
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6]).isoformat()
                    elif hasattr(entry, 'published'):
                        published = entry.published
                    else:
                        published = datetime.now().isoformat()
                    
                    # Extract summary
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = BeautifulSoup(entry.summary, 'html.parser').get_text()[:300]
                    elif hasattr(entry, 'description'):
                        summary = BeautifulSoup(entry.description, 'html.parser').get_text()[:300]
                    
                    # Extract image
                    image_url = ""
                    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                        image_url = entry.media_thumbnail[0].get('url', '')
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                        for enclosure in entry.enclosures:
                            if 'image' in enclosure.get('type', ''):
                                image_url = enclosure.get('href', '')
                                break
                    
                    article = NewsArticle(
                        title=entry.get('title', '').strip(),
                        summary=summary.strip(),
                        url=entry.get('link', ''),
                        source=source_name,
                        published=published,
                        category=category,
                        author=entry.get('author', ''),
                        image_url=image_url
                    )
                    
                    if article.title and article.url:
                        articles.append(article)
                        
                except Exception as e:
                    logger.debug(f"Error parsing entry from {source_name}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(articles)} articles from {source_name}")
            
        except Exception as e:
            logger.warning(f"Failed to parse RSS feed {source_name}: {e}")
        
        return articles
    
    def fetch_hacker_news(self) -> List[NewsArticle]:
        """Fetch from Hacker News API"""
        articles = []
        try:
            self._rate_limit("HackerNews")
            
            # Get top stories
            top_stories = self.session.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=10
            ).json()
            
            # Fetch details for top 20 stories
            for story_id in top_stories[:20]:
                try:
                    story_response = self.session.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_response.json()
                    
                    if story and story.get('title'):
                        article = NewsArticle(
                            title=story['title'],
                            summary=story.get('text', 'No summary available')[:300],
                            url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            source="Hacker News",
                            published=datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                            category="Technology",
                            author=story.get('by', ''),
                            engagement_score=story.get('score', 0)
                        )
                        articles.append(article)
                    
                    time.sleep(0.1)  # Small delay between requests
                    
                except Exception as e:
                    logger.debug(f"Error fetching HN story {story_id}: {e}")
                    continue
            
        except Exception as e:
            logger.warning(f"Failed to fetch Hacker News: {e}")
        
        return articles
    
    def fetch_reddit_news(self, subreddit: str, category: str) -> List[NewsArticle]:
        """Fetch news from Reddit"""
        articles = []
        try:
            self._rate_limit(f"Reddit_{subreddit}")
            
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            params = {'limit': 25}
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                try:
                    post_data = post.get('data', {})
                    
                    if post_data.get('title') and not post_data.get('is_self', False):
                        article = NewsArticle(
                            title=post_data['title'],
                            summary=post_data.get('selftext', '')[:300] or "Reddit discussion",
                            url=post_data.get('url', f"https://reddit.com{post_data.get('permalink', '')}"),
                            source=f"Reddit r/{subreddit}",
                            published=datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                            category=category,
                            author=post_data.get('author', ''),
                            engagement_score=post_data.get('ups', 0)
                        )
                        articles.append(article)
                        
                except Exception as e:
                    logger.debug(f"Error parsing Reddit post: {e}")
                    continue
            
        except Exception as e:
            logger.warning(f"Failed to fetch Reddit r/{subreddit}: {e}")
        
        return articles
    
    def fetch_dev_community(self) -> List[NewsArticle]:
        """Fetch articles from DEV Community"""
        articles = []
        try:
            self._rate_limit("DevCommunity")
            
            response = self.session.get(
                "https://dev.to/api/articles?top=7&per_page=25",
                timeout=10
            )
            response.raise_for_status()
            posts = response.json()
            
            for post in posts:
                article = NewsArticle(
                    title=post.get('title', ''),
                    summary=post.get('description', '')[:300],
                    url=post.get('url', ''),
                    source="DEV Community",
                    published=post.get('published_at', ''),
                    category="Programming",
                    author=post.get('user', {}).get('name', ''),
                    image_url=post.get('cover_image', ''),
                    engagement_score=post.get('positive_reactions_count', 0)
                )
                articles.append(article)
                
        except Exception as e:
            logger.warning(f"Failed to fetch DEV Community: {e}")
        
        return articles
    
    def get_all_news(self, max_articles: int = 200) -> List[NewsArticle]:
        """Fetch news from all available sources"""
        all_articles = []
        
        logger.info("Starting comprehensive news fetch...")
        
        # 1. Fetch from RSS feeds
        rss_articles = self._get_cached_or_fetch(
            "rss_feeds",
            lambda: self._fetch_all_rss_feeds()
        )
        all_articles.extend(rss_articles[:100])
        
        # 2. Fetch from Hacker News
        hn_articles = self._get_cached_or_fetch(
            "hacker_news", 
            self.fetch_hacker_news
        )
        all_articles.extend(hn_articles[:20])
        
        # 3. Fetch from Reddit
        reddit_subs = [
            ("worldnews", "World"),
            ("technology", "Technology"),
            ("science", "Science"),
            ("news", "General")
        ]
        
        for sub, category in reddit_subs[:2]:  # Limit to prevent overload
            reddit_articles = self._get_cached_or_fetch(
                f"reddit_{sub}",
                lambda s=sub, c=category: self.fetch_reddit_news(s, c)
            )
            all_articles.extend(reddit_articles[:15])
        
        # 4. Fetch from DEV Community
        dev_articles = self._get_cached_or_fetch(
            "dev_community",
            self.fetch_dev_community
        )
        all_articles.extend(dev_articles[:15])
        
        # Remove duplicates and sort by engagement/freshness
        unique_articles = self._deduplicate_articles(all_articles)
        sorted_articles = sorted(
            unique_articles,
            key=lambda x: (x.engagement_score, x.published),
            reverse=True
        )
        
        logger.info(f"Collected {len(sorted_articles)} unique articles from all sources")
        
        return sorted_articles[:max_articles]
    
    def _fetch_all_rss_feeds(self) -> List[NewsArticle]:
        """Fetch from all RSS feeds"""
        all_articles = []
        
        # Priority feeds (most reliable)
        priority_feeds = [
            ("BBC World", "World"),
            ("Reuters Top", "World"), 
            ("TechCrunch", "Technology"),
            ("The Verge", "Technology"),
            ("Standard Kenya", "Kenya"),
            ("Capital FM", "Kenya")
        ]
        
        for source, category in priority_feeds:
            if source in self.PREMIUM_RSS_FEEDS:
                articles = self.parse_rss_feed(
                    self.PREMIUM_RSS_FEEDS[source],
                    source,
                    category
                )
                all_articles.extend(articles[:10])  # Limit per source
                time.sleep(1)  # Be nice to servers
        
        return all_articles
    
    def _deduplicate_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove duplicate articles based on title similarity"""
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            # Normalize title for comparison
            normalized_title = article.title.lower().strip()
            
            # Check for duplicates
            is_duplicate = False
            for seen_title in seen_titles:
                if self._similarity(normalized_title, seen_title) > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_articles.append(article)
                seen_titles.add(normalized_title)
        
        return unique_articles
    
    def _similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings"""
        if not s1 or not s2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(s1.split())
        words2 = set(s2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def get_categorized_news(self) -> Dict[str, List[NewsArticle]]:
        """Get news organized by categories"""
        all_news = self.get_all_news()
        
        categorized = {
            "World": [],
            "Technology": [],
            "Science": [],
            "Business": [],
            "Kenya": [],
            "General": []
        }
        
        for article in all_news:
            category = article.category
            if category in categorized:
                categorized[category].append(article)
            else:
                categorized["General"].append(article)
        
        # Limit articles per category
        for category in categorized:
            categorized[category] = categorized[category][:20]
        
        return categorized
    
    def get_trending_topics(self) -> List[Dict]:
        """Extract trending topics from headlines"""
        articles = self.get_all_news(100)
        
        # Simple keyword extraction from titles
        word_count = {}
        for article in articles:
            words = article.title.lower().split()
            for word in words:
                if len(word) > 4 and word.isalpha():  # Filter meaningful words
                    word_count[word] = word_count.get(word, 0) + 1
        
        # Get top trending words
        trending = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [{"topic": word, "count": count} for word, count in trending]

# Initialize the next-gen aggregator
next_gen_news = NextGenNewsAggregator()
