"""
Immersive API Integrator
Comprehensive collection of the best FREE NO-SIGNUP APIs for maximum dashboard features
Constantly updated with working APIs and fallbacks
"""

import os
import json
import time
import random
import hashlib
import logging
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class ImmersiveAPIIntegrator:
    """
    Mega collection of free APIs - No signup required!
    Each category has multiple fallbacks for maximum reliability
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Rate limiting
        self.last_call_times = {}
        self.min_delay = 1  # seconds between calls
    
    def _rate_limit(self, api_name: str):
        """Simple rate limiting"""
        now = time.time()
        if api_name in self.last_call_times:
            time_diff = now - self.last_call_times[api_name]
            if time_diff < self.min_delay:
                time.sleep(self.min_delay - time_diff)
        self.last_call_times[api_name] = time.time()
    
    def _safe_request(self, url: str, params: dict = None, timeout: int = 10) -> Optional[dict]:
        """Safe HTTP request with error handling"""
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Request failed for {url}: {e}")
            return None

    # ========== NEWS APIS - Free and Functioning ==========
    
    def get_world_news(self) -> List[Dict]:
        """Get world news from multiple free sources"""
        news_items = []
        
        # 1. JSONFeed.com aggregator - NO SIGNUP
        self._rate_limit('jsonfeed')
        try:
            url = "https://jsonfeed.org/feed.json"
            data = self._safe_request(url)
            if data and 'items' in data:
                for item in data['items'][:10]:
                    news_items.append({
                        'title': item.get('title', ''),
                        'summary': item.get('summary', item.get('content_text', ''))[:200],
                        'url': item.get('url', ''),
                        'source': 'JSONFeed',
                        'published': item.get('date_published', ''),
                        'category': 'Tech'
                    })
        except Exception as e:
            logger.warning(f"JSONFeed failed: {e}")
        
        # 2. Hacker News - NO SIGNUP, very reliable
        self._rate_limit('hackernews')
        try:
            # Get top stories
            top_stories = self._safe_request("https://hacker-news.firebaseio.com/v0/topstories.json")
            if top_stories:
                for story_id in top_stories[:10]:
                    story = self._safe_request(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                    if story and story.get('title'):
                        news_items.append({
                            'title': story['title'],
                            'summary': story.get('text', '')[:200] if story.get('text') else 'No summary',
                            'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'source': 'Hacker News',
                            'published': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                            'category': 'Technology',
                            'score': story.get('score', 0)
                        })
        except Exception as e:
            logger.warning(f"Hacker News failed: {e}")
        
        # 3. Reddit JSON feeds - NO SIGNUP
        self._rate_limit('reddit')
        try:
            subreddits = ['worldnews', 'news', 'technology', 'science']
            for sub in subreddits[:2]:  # Limit to prevent overload
                data = self._safe_request(f"https://www.reddit.com/r/{sub}/hot.json", {'limit': 5})
                if data and 'data' in data and 'children' in data['data']:
                    for post in data['data']['children']:
                        post_data = post.get('data', {})
                        if post_data.get('title'):
                            news_items.append({
                                'title': post_data['title'],
                                'summary': post_data.get('selftext', '')[:200],
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'source': f'Reddit r/{sub}',
                                'published': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                                'category': sub.title(),
                                'score': post_data.get('ups', 0)
                            })
                time.sleep(2)  # Reddit rate limiting
        except Exception as e:
            logger.warning(f"Reddit failed: {e}")
        
        # 4. RSS Feed aggregator - Multiple sources
        rss_feeds = {
            'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
            'Reuters': 'http://feeds.reuters.com/reuters/topNews',
            'TechCrunch': 'https://techcrunch.com/feed/',
            'Wired': 'https://www.wired.com/feed',
            'The Verge': 'https://www.theverge.com/rss/index.xml'
        }
        
        for source, feed_url in list(rss_feeds.items())[:3]:  # Limit sources
            self._rate_limit(f'rss_{source}')
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    news_items.append({
                        'title': entry.get('title', ''),
                        'summary': entry.get('summary', '')[:200],
                        'url': entry.get('link', ''),
                        'source': source,
                        'published': entry.get('published', ''),
                        'category': 'News'
                    })
                time.sleep(1)
            except Exception as e:
                logger.warning(f"RSS {source} failed: {e}")
        
        return news_items[:50]  # Limit total items
    
    def get_crypto_news(self) -> List[Dict]:
        """Get cryptocurrency news - Free APIs"""
        crypto_news = []
        
        # CoinGecko - Free tier, no signup
        self._rate_limit('coingecko')
        try:
            # Get trending coins
            trending = self._safe_request("https://api.coingecko.com/api/v3/search/trending")
            if trending and 'coins' in trending:
                for coin in trending['coins'][:5]:
                    coin_data = coin.get('item', {})
                    crypto_news.append({
                        'title': f"📈 {coin_data.get('name', '')} is trending",
                        'summary': f"Market rank: #{coin_data.get('market_cap_rank', 'N/A')} - Price BTC: {coin_data.get('price_btc', 'N/A')}",
                        'url': f"https://www.coingecko.com/en/coins/{coin_data.get('id', '')}",
                        'source': 'CoinGecko',
                        'published': datetime.now().isoformat(),
                        'category': 'Cryptocurrency'
                    })
        except Exception as e:
            logger.warning(f"CoinGecko failed: {e}")
        
        return crypto_news
    
    def get_weather_data(self, city: str = "Nairobi") -> Dict:
        """Get weather data from free APIs"""
        weather_data = {}
        
        # Open-Meteo - Completely free, no API key
        self._rate_limit('openmeteo')
        try:
            # Get coordinates for city (using a free geocoding service)
            geo_url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': -1.2921,  # Nairobi coordinates
                'longitude': 36.8219,
                'current_weather': 'true',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
                'timezone': 'auto'
            }
            
            data = self._safe_request(geo_url, params)
            if data:
                current = data.get('current_weather', {})
                weather_data = {
                    'city': city,
                    'temperature': current.get('temperature'),
                    'windspeed': current.get('windspeed'),
                    'weather_code': current.get('weathercode'),
                    'time': current.get('time'),
                    'source': 'Open-Meteo'
                }
        except Exception as e:
            logger.warning(f"Weather API failed: {e}")
        
        return weather_data
    
    def get_quotes_and_facts(self) -> List[Dict]:
        """Get inspirational quotes and fun facts"""
        quotes_facts = []
        
        # Quotable - Free quotes API
        self._rate_limit('quotable')
        try:
            quote_data = self._safe_request("https://api.quotable.io/random")
            if quote_data:
                quotes_facts.append({
                    'type': 'quote',
                    'content': quote_data.get('content', ''),
                    'author': quote_data.get('author', ''),
                    'source': 'Quotable'
                })
        except Exception as e:
            logger.warning(f"Quotable failed: {e}")
        
        # Cat Facts - Free and fun
        self._rate_limit('catfacts')
        try:
            cat_fact = self._safe_request("https://catfact.ninja/fact")
            if cat_fact:
                quotes_facts.append({
                    'type': 'fact',
                    'content': cat_fact.get('fact', ''),
                    'source': 'Cat Facts'
                })
        except Exception as e:
            logger.warning(f"Cat Facts failed: {e}")
        
        # Random Facts
        self._rate_limit('randomfacts')
        try:
            fact_data = self._safe_request("https://uselessfacts.jsph.pl/random.json?language=en")
            if fact_data:
                quotes_facts.append({
                    'type': 'fact',
                    'content': fact_data.get('text', ''),
                    'source': 'Random Facts'
                })
        except Exception as e:
            logger.warning(f"Random Facts failed: {e}")
        
        return quotes_facts
    
    def get_color_palette(self) -> Dict:
        """Get random color palette for UI theming"""
        self._rate_limit('colormind')
        try:
            # Colormind - Free color palette generator
            response = requests.post("http://colormind.io/api/", 
                                   json={"model": "default"},
                                   timeout=5)
            if response.status_code == 200:
                colors = response.json().get('result', [])
                return {
                    'palette': ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors],
                    'source': 'Colormind'
                }
        except Exception as e:
            logger.warning(f"Color API failed: {e}")
        
        # Fallback: Generate random colors
        return {
            'palette': [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(5)],
            'source': 'Generated'
        }
    
    def get_memes_and_jokes(self) -> List[Dict]:
        """Get memes and jokes for entertainment"""
        entertainment = []
        
        # JokeAPI - Free programming jokes
        self._rate_limit('jokeapi')
        try:
            joke_data = self._safe_request("https://v2.jokeapi.dev/joke/Programming?safe-mode")
            if joke_data:
                if joke_data.get('type') == 'single':
                    content = joke_data.get('joke', '')
                else:
                    content = f"{joke_data.get('setup', '')} - {joke_data.get('delivery', '')}"
                
                entertainment.append({
                    'type': 'joke',
                    'content': content,
                    'category': joke_data.get('category', 'Programming'),
                    'source': 'JokeAPI'
                })
        except Exception as e:
            logger.warning(f"JokeAPI failed: {e}")
        
        # Chuck Norris jokes
        self._rate_limit('chucknorris')
        try:
            chuck_joke = self._safe_request("https://api.chucknorris.io/jokes/random")
            if chuck_joke:
                entertainment.append({
                    'type': 'joke',
                    'content': chuck_joke.get('value', ''),
                    'category': 'Chuck Norris',
                    'source': 'Chuck Norris API'
                })
        except Exception as e:
            logger.warning(f"Chuck Norris API failed: {e}")
        
        return entertainment
    
    def get_github_trending(self) -> List[Dict]:
        """Get trending GitHub repositories"""
        self._rate_limit('github')
        try:
            # GitHub trending (public API, no auth needed)
            url = "https://api.github.com/search/repositories"
            params = {
                'q': 'created:>2024-01-01',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            
            data = self._safe_request(url, params)
            if data and 'items' in data:
                trending = []
                for repo in data['items']:
                    trending.append({
                        'name': repo.get('full_name', ''),
                        'description': repo.get('description', ''),
                        'stars': repo.get('stargazers_count', 0),
                        'language': repo.get('language', 'Unknown'),
                        'url': repo.get('html_url', ''),
                        'updated': repo.get('updated_at', '')
                    })
                return trending
        except Exception as e:
            logger.warning(f"GitHub trending failed: {e}")
        
        return []
    
    def get_space_data(self) -> Dict:
        """Get space-related data"""
        space_data = {}
        
        # NASA API - some endpoints don't require API key
        self._rate_limit('nasa')
        try:
            # ISS location
            iss_data = self._safe_request("http://api.open-notify.org/iss-now.json")
            if iss_data and iss_data.get('iss_position'):
                space_data['iss_location'] = iss_data['iss_position']
            
            # People in space
            people_data = self._safe_request("http://api.open-notify.org/astros.json")
            if people_data:
                space_data['people_in_space'] = people_data.get('number', 0)
                space_data['astronauts'] = people_data.get('people', [])
        except Exception as e:
            logger.warning(f"Space API failed: {e}")
        
        return space_data
    
    def get_comprehensive_data(self) -> Dict:
        """Get all data in one comprehensive call"""
        logger.info("Fetching comprehensive data from all free APIs...")
        
        comprehensive_data = {
            'timestamp': datetime.now().isoformat(),
            'news': self.get_world_news(),
            'crypto': self.get_crypto_news(),
            'weather': self.get_weather_data(),
            'quotes_facts': self.get_quotes_and_facts(),
            'entertainment': self.get_memes_and_jokes(),
            'github_trending': self.get_github_trending(),
            'space': self.get_space_data(),
            'ui_theme': self.get_color_palette(),
            'api_status': {
                'total_apis_called': len(self.last_call_times),
                'last_update': datetime.now().isoformat(),
                'status': 'active'
            }
        }
        
        return comprehensive_data

# Additional specialized integrators

class SocialMediaAggregator:
    """Social media content aggregator - NO SIGNUP required"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from multiple platforms"""
        trending = []
        
        # Reddit trending
        try:
            data = self.session.get("https://www.reddit.com/r/popular.json?limit=10").json()
            for post in data.get('data', {}).get('children', [])[:5]:
                post_data = post.get('data', {})
                trending.append({
                    'title': post_data.get('title', ''),
                    'platform': 'Reddit',
                    'score': post_data.get('ups', 0),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'subreddit': post_data.get('subreddit', '')
                })
        except Exception as e:
            logger.warning(f"Reddit trending failed: {e}")
        
        return trending

class FinanceDataAggregator:
    """Financial data from free APIs"""
    
    def get_crypto_prices(self) -> List[Dict]:
        """Get cryptocurrency prices"""
        try:
            # CoinGecko free API
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,cardano,polkadot,chainlink',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                prices = []
                for coin, info in data.items():
                    prices.append({
                        'name': coin.title(),
                        'price': info.get('usd', 0),
                        'change_24h': info.get('usd_24h_change', 0)
                    })
                return prices
        except Exception as e:
            logger.warning(f"Crypto prices failed: {e}")
        
        return []

# Initialize global integrator
api_integrator = ImmersiveAPIIntegrator()
social_aggregator = SocialMediaAggregator()
finance_aggregator = FinanceDataAggregator()
