"""
Kenyan News Ingestion System
Discovers and parses RSS feeds for major Kenyan news sources
Includes deduplication, caching, and fallback scraping
"""

import os
import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse
import feedparser
import requests
from bs4 import BeautifulSoup
import aiohttp
import aiofiles

logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    """Standardized news item structure"""
    title: str
    summary: str
    url: str
    source: str
    published: str  # ISO 8601
    image_url: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    content_hash: str = ""
    
    def __post_init__(self):
        """Generate content hash for deduplication"""
        if not self.content_hash:
            content = f"{self.title}{self.source}".lower().strip()
            self.content_hash = hashlib.md5(content.encode()).hexdigest()


class KenyanNewsIngestor:
    """Ingests news from major Kenyan sources"""
    
    # Major Kenyan news RSS feeds
    RSS_FEEDS = {
        "Standard": "https://www.standardmedia.co.ke/rss/headlines.php",
        "CapitalFM": "https://www.capitalfm.co.ke/news/feed/",
        "AllAfrica-Kenya": "https://allafrica.com/tools/headlines/rdf/kenya/headlines.rdf",
        "BusinessDaily": "https://www.businessdailyafrica.com/bd/corporate/lifestyle/feed",
        "KBC": "https://www.kbc.co.ke/feed/",
        "Citizen": "https://citizentv.co.ke/feed/",
        "NTV": "https://ntvkenya.co.ke/feed/",
        "PesaCheck": "https://pesacheck.org/feed/",
    }
    
    # Backup scraping URLs if RSS fails
    BACKUP_URLS = {
        "Standard": "https://www.standardmedia.co.ke/",
        "CapitalFM": "https://www.capitalfm.co.ke/news/",
        "BusinessDaily": "https://www.businessdailyafrica.com/",
    }
    
    def __init__(self, cache_file: str = "news_cache.jsonl"):
        self.cache_file = cache_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SentimentBot/1.0)'
        })
        self.seen_hashes: Set[str] = set()
        self.load_cache()
    
    def load_cache(self):
        """Load existing cache to avoid duplicates"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            item = json.loads(line.strip())
                            self.seen_hashes.add(item.get('content_hash', ''))
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
    
    def normalize_timestamp(self, timestamp_str: str) -> str:
        """Normalize timestamp to ISO 8601"""
        try:
            # Parse various timestamp formats
            if timestamp_str:
                # Try feedparser's parsed time first
                if hasattr(timestamp_str, 'tm_year'):
                    dt = datetime(*timestamp_str[:6], tzinfo=timezone.utc)
                else:
                    # Try common formats
                    from dateutil.parser import parse
                    dt = parse(timestamp_str)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                
                return dt.isoformat()
        except:
            pass
        
        # Fallback to current time
        return datetime.now(timezone.utc).isoformat()
    
    def parse_rss_feed(self, url: str, source: str) -> List[NewsItem]:
        """Parse RSS feed and return normalized news items"""
        items = []
        
        try:
            logger.info(f"Fetching RSS feed: {source}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:20]:  # Limit to 20 recent items
                try:
                    # Extract basic info
                    title = entry.get('title', '').strip()
                    summary = entry.get('summary', entry.get('description', '')).strip()
                    link = entry.get('link', '')
                    
                    if not title or not link:
                        continue
                    
                    # Clean HTML from summary
                    if summary:
                        soup = BeautifulSoup(summary, 'html.parser')
                        summary = soup.get_text().strip()
                    
                    # Get published time
                    published_parsed = entry.get('published_parsed')
                    published = entry.get('published', '')
                    published_iso = self.normalize_timestamp(published_parsed or published)
                    
                    # Extract image
                    image_url = None
                    if hasattr(entry, 'media_content'):
                        image_url = entry.media_content[0].get('url')
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                        image_url = entry.enclosures[0].href
                    
                    # Extract category
                    category = None
                    if hasattr(entry, 'tags') and entry.tags:
                        category = entry.tags[0].term
                    
                    # Create news item
                    news_item = NewsItem(
                        title=title,
                        summary=summary[:500],  # Limit summary length
                        url=link,
                        source=source,
                        published=published_iso,
                        image_url=image_url,
                        category=category,
                        author=entry.get('author', '')
                    )
                    
                    # Check for duplicates
                    if news_item.content_hash not in self.seen_hashes:
                        items.append(news_item)
                        self.seen_hashes.add(news_item.content_hash)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse RSS entry from {source}: {e}")
                    continue
            
            logger.info(f"Parsed {len(items)} new items from {source}")
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed for {source}: {e}")
        
        return items
    
    def scrape_fallback(self, url: str, source: str) -> List[NewsItem]:
        """Fallback HTML scraping if RSS fails"""
        items = []
        
        try:
            logger.info(f"Attempting fallback scraping: {source}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic article selectors (can be customized per source)
            article_selectors = [
                'article h2 a',
                '.headline a',
                '.post-title a',
                'h1 a', 'h2 a', 'h3 a'
            ]
            
            links = []
            for selector in article_selectors:
                found = soup.select(selector)
                if found:
                    links.extend(found[:10])  # Limit results
                    break
            
            for link in links[:10]:  # Limit to 10 items
                try:
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    if not title or not href:
                        continue
                    
                    # Ensure absolute URL
                    if href.startswith('/'):
                        href = urljoin(url, href)
                    
                    news_item = NewsItem(
                        title=title,
                        summary=f"Article from {source}",
                        url=href,
                        source=source,
                        published=datetime.now(timezone.utc).isoformat()
                    )
                    
                    if news_item.content_hash not in self.seen_hashes:
                        items.append(news_item)
                        self.seen_hashes.add(news_item.content_hash)
                
                except Exception as e:
                    logger.warning(f"Failed to parse scraped item: {e}")
                    continue
            
            logger.info(f"Scraped {len(items)} items from {source}")
            
        except Exception as e:
            logger.error(f"Fallback scraping failed for {source}: {e}")
        
        return items
    
    def cache_items(self, items: List[NewsItem]):
        """Cache items to JSONL file"""
        try:
            with open(self.cache_file, 'a', encoding='utf-8') as f:
                for item in items:
                    f.write(json.dumps(asdict(item)) + '\n')
        except Exception as e:
            logger.error(f"Failed to cache items: {e}")
    
    def ingest_all_sources(self) -> List[NewsItem]:
        """Ingest from all configured sources"""
        all_items = []
        
        # Try RSS feeds first
        for source, rss_url in self.RSS_FEEDS.items():
            items = self.parse_rss_feed(rss_url, source)
            if items:
                all_items.extend(items)
            elif source in self.BACKUP_URLS:
                # Fallback to scraping
                items = self.scrape_fallback(self.BACKUP_URLS[source], source)
                all_items.extend(items)
        
        # Cache new items
        if all_items:
            self.cache_items(all_items)
        
        logger.info(f"Total ingested: {len(all_items)} news items")
        return all_items
    
    def get_cached_items(self, max_age_hours: int = 24) -> List[NewsItem]:
        """Get cached items within max age"""
        items = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            published = datetime.fromisoformat(data['published'].replace('Z', '+00:00'))
                            
                            if published > cutoff_time:
                                items.append(NewsItem(**data))
                        except (json.JSONDecodeError, ValueError, KeyError):
                            continue
        except Exception as e:
            logger.error(f"Failed to read cached items: {e}")
        
        return items


# Global instance
kenyan_news_ingestor = KenyanNewsIngestor()


if __name__ == '__main__':
    # Test the ingestion system
    print("🔍 Testing Kenyan News Ingestion")
    
    ingestor = KenyanNewsIngestor()
    items = ingestor.ingest_all_sources()
    
    print(f"✅ Ingested {len(items)} news items")
    
    # Show samples
    for item in items[:3]:
        print(f"\n📰 {item.source}: {item.title}")
        print(f"   🔗 {item.url}")
        print(f"   📅 {item.published}")
