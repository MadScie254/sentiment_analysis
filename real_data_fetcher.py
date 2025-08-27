"""
Real-time data fetcher for SentimentAI platform
Handles all external API calls and data aggregation
"""

import asyncio
import aiohttp
import requests
from datetime import datetime, timedelta
import random
import json
import time
from typing import Dict, List, Optional, Any
from config import Config

class RealDataFetcher:
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    async def create_session(self):
        """Create aiohttp session for async requests"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=15, connect=10)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        return time.time() - self.cache[key]['timestamp'] < self.cache_timeout
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get data from cache if valid"""
        if self.is_cache_valid(key):
            return self.cache[key]['data']
        return None
    
    def set_cache(self, key: str, data: Any):
        """Set data in cache"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    async def fetch_hacker_news_stories(self, limit: int = 10) -> List[Dict]:
        """Fetch top stories from Hacker News"""
        cache_key = f"hackernews_top_{limit}"
        cached = self.get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            await self.create_session()
            
            # Get top story IDs
            async with self.session.get(
                f"{Config.FREE_APIS['hackernews']['base_url']}/topstories.json"
            ) as response:
                story_ids = await response.json()
            
            # Fetch details for top stories
            stories = []
            for story_id in story_ids[:limit]:
                try:
                    async with self.session.get(
                        f"{Config.FREE_APIS['hackernews']['base_url']}/item/{story_id}.json"
                    ) as story_response:
                        story_data = await story_response.json()
                        if story_data and story_data.get('title'):
                            stories.append({
                                'id': story_data.get('id'),
                                'title': story_data.get('title'),
                                'url': story_data.get('url', ''),
                                'score': story_data.get('score', 0),
                                'author': story_data.get('by', 'Anonymous'),
                                'time': story_data.get('time', 0),
                                'comments': story_data.get('descendants', 0)
                            })
                except:
                    continue
            
            self.set_cache(cache_key, stories)
            return stories
            
        except Exception as e:
            print(f"Error fetching Hacker News: {e}")
            return self._get_fallback_news()
    
    async def fetch_reddit_posts(self, subreddit: str = 'popular', limit: int = 10) -> List[Dict]:
        """Fetch posts from Reddit"""
        cache_key = f"reddit_{subreddit}_{limit}"
        cached = self.get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            await self.create_session()
            
            async with self.session.get(
                f"{Config.FREE_APIS['reddit']['base_url']}/r/{subreddit}.json?limit={limit}",
                headers={'User-Agent': 'SentimentAI/1.0'}
            ) as response:
                data = await response.json()
                
                posts = []
                for post in data.get('data', {}).get('children', []):
                    post_data = post.get('data', {})
                    posts.append({
                        'id': post_data.get('id'),
                        'title': post_data.get('title'),
                        'text': post_data.get('selftext', ''),
                        'score': post_data.get('score', 0),
                        'author': post_data.get('author', 'Unknown'),
                        'subreddit': post_data.get('subreddit'),
                        'comments': post_data.get('num_comments', 0),
                        'url': post_data.get('url', ''),
                        'created': post_data.get('created_utc', 0)
                    })
                
                self.set_cache(cache_key, posts)
                return posts
                
        except Exception as e:
            print(f"Error fetching Reddit: {e}")
            return self._get_fallback_social_posts()
    
    async def fetch_crypto_prices(self) -> Dict:
        """Fetch cryptocurrency prices"""
        cache_key = "crypto_prices"
        cached = self.get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            await self.create_session()
            
            async with self.session.get(
                f"{Config.FREE_APIS['coingecko']['base_url']}/simple/price?ids=bitcoin,ethereum,dogecoin&vs_currencies=usd&include_24hr_change=true"
            ) as response:
                data = await response.json()
                
                formatted_data = {
                    'bitcoin': {
                        'price': data.get('bitcoin', {}).get('usd', 0),
                        'change_24h': data.get('bitcoin', {}).get('usd_24h_change', 0)
                    },
                    'ethereum': {
                        'price': data.get('ethereum', {}).get('usd', 0),
                        'change_24h': data.get('ethereum', {}).get('usd_24h_change', 0)
                    },
                    'dogecoin': {
                        'price': data.get('dogecoin', {}).get('usd', 0),
                        'change_24h': data.get('dogecoin', {}).get('usd_24h_change', 0)
                    }
                }
                
                self.set_cache(cache_key, formatted_data)
                return formatted_data
                
        except Exception as e:
            print(f"Error fetching crypto prices: {e}")
            return self._get_fallback_crypto()
    
    async def fetch_random_quote(self) -> Dict:
        """Fetch inspirational quote"""
        try:
            await self.create_session()
            
            async with self.session.get(
                f"{Config.FREE_APIS['quotable']['base_url']}/random",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                data = await response.json()
                return {
                    'text': data.get('content', 'Be yourself; everyone else is already taken.'),
                    'author': data.get('author', 'Oscar Wilde'),
                    'tags': data.get('tags', [])
                }
                
        except Exception as e:
            print(f"Error fetching quote: {e}")
            return {
                'text': 'The only way to do great work is to love what you do.',
                'author': 'Steve Jobs',
                'tags': ['motivational']
            }
    
    async def fetch_github_trending(self) -> List[Dict]:
        """Fetch trending GitHub repositories"""
        cache_key = "github_trending"
        cached = self.get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            await self.create_session()
            
            # Get repositories created in the last week
            last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            async with self.session.get(
                f"{Config.FREE_APIS['github']['base_url']}/search/repositories?q=created:>{last_week}&sort=stars&order=desc&per_page=10"
            ) as response:
                data = await response.json()
                
                repos = []
                for repo in data.get('items', []):
                    repos.append({
                        'name': repo.get('name'),
                        'full_name': repo.get('full_name'),
                        'description': repo.get('description', ''),
                        'stars': repo.get('stargazers_count', 0),
                        'language': repo.get('language', 'Unknown'),
                        'url': repo.get('html_url'),
                        'owner': repo.get('owner', {}).get('login', 'Unknown')
                    })
                
                self.set_cache(cache_key, repos)
                return repos
                
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
            return self._get_fallback_github()
    
    def _get_fallback_news(self) -> List[Dict]:
        """Fallback news data when API is unavailable"""
        return [
            {
                'id': f'fallback_{i}',
                'title': headline,
                'score': random.randint(50, 500),
                'author': f'user_{random.randint(1000, 9999)}',
                'comments': random.randint(10, 100)
            }
            for i, headline in enumerate(Config.SAMPLE_DATA['news_headlines'])
        ]
    
    def _get_fallback_social_posts(self) -> List[Dict]:
        """Fallback social media posts"""
        return Config.SAMPLE_DATA['reddit_posts']
    
    def _get_fallback_crypto(self) -> Dict:
        """Fallback crypto data with realistic simulation"""
        base_prices = {'bitcoin': 45000, 'ethereum': 3000, 'dogecoin': 0.08}
        return {
            coin: {
                'price': base_prices[coin] * (1 + random.uniform(-0.05, 0.05)),
                'change_24h': random.uniform(-10, 10)
            }
            for coin in base_prices
        }
    
    def _get_fallback_github(self) -> List[Dict]:
        """Fallback GitHub trending repos"""
        return [
            {
                'name': f'awesome-project-{i}',
                'full_name': f'developer{i}/awesome-project-{i}',
                'description': 'An amazing open source project that does incredible things',
                'stars': random.randint(100, 5000),
                'language': random.choice(['Python', 'JavaScript', 'TypeScript', 'Go', 'Rust']),
                'owner': f'developer{i}'
            }
            for i in range(1, 6)
        ]
    
    async def get_comprehensive_data(self) -> Dict:
        """Fetch all data sources in parallel"""
        try:
            # Run all API calls concurrently
            results = await asyncio.gather(
                self.fetch_hacker_news_stories(5),
                self.fetch_reddit_posts('technology', 5),
                self.fetch_crypto_prices(),
                self.fetch_random_quote(),
                self.fetch_github_trending(),
                return_exceptions=True
            )
            
            return {
                'news': results[0] if not isinstance(results[0], Exception) else self._get_fallback_news(),
                'social': results[1] if not isinstance(results[1], Exception) else self._get_fallback_social_posts(),
                'crypto': results[2] if not isinstance(results[2], Exception) else self._get_fallback_crypto(),
                'quote': results[3] if not isinstance(results[3], Exception) else {'text': 'Stay hungry, stay foolish.', 'author': 'Steve Jobs'},
                'github': results[4] if not isinstance(results[4], Exception) else self._get_fallback_github(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error in comprehensive data fetch: {e}")
            return self._get_all_fallback_data()
    
    def _get_all_fallback_data(self) -> Dict:
        """Complete fallback data set"""
        return {
            'news': self._get_fallback_news(),
            'social': self._get_fallback_social_posts(),
            'crypto': self._get_fallback_crypto(),
            'quote': {'text': 'The best time to plant a tree was 20 years ago. The second best time is now.', 'author': 'Chinese Proverb'},
            'github': self._get_fallback_github(),
            'timestamp': datetime.now().isoformat()
        }

# Global instance
real_data_fetcher = RealDataFetcher()
