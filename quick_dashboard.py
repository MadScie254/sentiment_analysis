"""
Quick Start Sentiment Analysis Dashboard
Simplified version that starts faster with mock components
"""

import os
import sys
import json
import math
import tempfile
import logging
from datetime import datetime, timedelta
from threading import Lock
from functools import lru_cache
from typing import Dict, List, Optional

# Flask and web components
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import requests for API calls
import requests
import feedparser
from urllib.parse import urljoin, urlparse

# Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///sentiment_analysis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 104857600))  # 100MB
    
    # News API Keys
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')
    CURRENTS_API_KEY = os.getenv('CURRENTS_API_KEY')
    
    # Social Media API Keys
    X_API_KEY = os.getenv('X_API_KEY')
    X_API_SECRET = os.getenv('X_API_SECRET')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    
    # AI/ML API Keys
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Quick Mock Components for Fast Startup
class QuickNLPEngine:
    """Fast mock NLP engine with realistic responses"""
    
    def analyze_sentiment(self, text, model_preference='auto'):
        import random
        
        # Simple keyword-based sentiment analysis for demo
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'happy', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'disappointed', 'worst', 'horrible']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            confidence = min(0.6 + (pos_count * 0.1), 0.95)
        elif neg_count > pos_count:
            sentiment = 'negative'
            confidence = min(0.6 + (neg_count * 0.1), 0.95)
        else:
            sentiment = 'neutral'
            confidence = 0.6 + random.uniform(0, 0.2)
        
        class Result:
            def __init__(self, sentiment_val, confidence_val, text_val):
                self.text = text_val[:200]
                self.sentiment = sentiment_val
                self.confidence = confidence_val
                self.scores = {
                    'positive': confidence_val if sentiment_val == 'positive' else (1-confidence_val) * 0.3,
                    'negative': confidence_val if sentiment_val == 'negative' else (1-confidence_val) * 0.3,
                    'neutral': confidence_val if sentiment_val == 'neutral' else (1-confidence_val) * 0.4
                }
                self.model_used = 'quick-mock'
                self.processing_time = 0.05
                self.language = 'en'
                self.emotion_scores = {'joy': 0.7, 'anger': 0.1, 'fear': 0.1, 'sadness': 0.1}
                self.toxicity_score = random.uniform(0, 0.3)
                self.bias_score = random.uniform(0, 0.2)
                self.analysis_metadata = {'mock': True}
        
        return Result(sentiment, confidence, text)
    
    def get_model_info(self):
        return {'available_models': ['quick-mock'], 'device': 'cpu'}

class QuickDatabaseManager:
    """Fast mock database"""
    
    def save_sentiment_analysis(self, result, **kwargs):
        return 1
    
    def get_recent_analyses(self, limit=50, offset=0):
        return []
    
    def get_analytics_summary(self, days=7):
        return {
            'total_analyses': 42,
            'sentiment_distribution': {'positive': 25, 'negative': 8, 'neutral': 9},
            'average_confidence': 0.75,
            'daily_trends': []
        }
    
    def get_dashboard_summary(self):
        return {
            'today': {'total_analyses': 15, 'avg_confidence': 0.78, 'top_model': 'quick-mock'},
            'week': {'total_analyses': 42, 'avg_confidence': 0.75, 'top_model': 'quick-mock'}
        }

class QuickNewsAPI:
    """Fast mock news API"""
    
    def get_trending_news(self, limit=20, page=1):
        sample_news = [
            {
                'title': 'AI Technology Advances Rapidly in 2025',
                'summary': 'New breakthroughs in artificial intelligence are transforming industries worldwide...',
                'url': 'https://example.com/news/1',
                'source': 'TechNews',
                'timestamp': '2025-08-31 12:00:00',
                'sentiment': 'positive',
                'confidence': 0.85
            },
            {
                'title': 'Market Volatility Continues Amid Economic Uncertainty',
                'summary': 'Global markets show mixed signals as investors react to recent policy changes...',
                'url': 'https://example.com/news/2',
                'source': 'MarketWatch',
                'timestamp': '2025-08-31 11:30:00',
                'sentiment': 'neutral',
                'confidence': 0.72
            },
            {
                'title': 'Climate Change Report Shows Concerning Trends',
                'summary': 'Latest scientific data reveals accelerating environmental challenges that require immediate attention...',
                'url': 'https://example.com/news/3',
                'source': 'EnvironmentNews',
                'timestamp': '2025-08-31 10:45:00',
                'sentiment': 'negative',
                'confidence': 0.78
            },
            {
                'title': 'Revolutionary Medical Treatment Shows Promise',
                'summary': 'Breakthrough therapy demonstrates remarkable success in clinical trials...',
                'url': 'https://example.com/news/4',
                'source': 'HealthNews',
                'timestamp': '2025-08-31 09:15:00',
                'sentiment': 'positive',
                'confidence': 0.91
            }
        ] * (limit // 4 + 1)
        
        return sample_news[:limit]

class QuickTwitterAPI:
    """Fast mock Twitter API"""
    
    def get_trending_tweets(self, limit=20):
        sample_tweets = [
            {
                'text': 'Just witnessed an amazing breakthrough in AI technology! The future is looking bright! 🚀',
                'author': 'TechEnthusiast',
                'timestamp': datetime.now().isoformat(),
                'likes': 234,
                'retweets': 45,
                'sentiment': 'positive',
                'confidence': 0.92
            },
            {
                'text': 'Market conditions are quite uncertain these days. Need to stay cautious with investments.',
                'author': 'InvestorWatch',
                'timestamp': datetime.now().isoformat(),
                'likes': 78,
                'retweets': 12,
                'sentiment': 'neutral',
                'confidence': 0.68
            },
            {
                'text': 'This weather is absolutely terrible. Rain for the past week straight! 😔',
                'author': 'WeatherWatcher',
                'timestamp': datetime.now().isoformat(),
                'likes': 23,
                'retweets': 5,
                'sentiment': 'negative',
                'confidence': 0.84
            }
        ] * (limit // 3 + 1)
        
        return sample_tweets[:limit]

# Initialize components
nlp_engine = QuickNLPEngine()
real_db_manager = QuickDatabaseManager()
real_news_api = QuickNewsAPI()
twitter_api = QuickTwitterAPI()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quick_dashboard.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/')
def dashboard():
    """Quick Start Dashboard"""
    return render_template_string(QUICK_DASHBOARD_HTML)

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment quickly"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Analyze sentiment
        result = nlp_engine.analyze_sentiment(text)
        
        # Debug: print result attributes
        logger.info(f"Result type: {type(result)}")
        logger.info(f"Result attributes: {dir(result)}")
        
        # Save to database (mock) - skip for now to isolate the issue
        # real_db_manager.save_sentiment_analysis(result)
        
        return jsonify({
            'success': True,
            'text': result.text,
            'sentiment': result.sentiment,
            'confidence': result.confidence,
            'scores': result.scores,
            'model_used': result.model_used,
            'processing_time': result.processing_time,
            'emotion_scores': result.emotion_scores,
            'toxicity_score': result.toxicity_score
        })
        
    except Exception as e:
        logger.error(f"Analysis API failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/news')
def get_news():
    """Get news with sentiment analysis"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        articles = real_news_api.get_trending_news(limit, page)
        
        return jsonify({
            'items': articles,
            'page': page,
            'limit': limit,
            'total_items': len(articles) * 5,
            'total_pages': 5,
            'sources_used': ['TechNews', 'MarketWatch', 'EnvironmentNews', 'HealthNews']
        })
        
    except Exception as e:
        logger.error(f"News API failed: {e}")
        return jsonify({'error': 'Failed to fetch news'}), 500

@app.route('/api/social/tweets')
def get_tweets():
    """Get tweets with sentiment analysis"""
    try:
        limit = int(request.args.get('limit', 10))
        tweets = twitter_api.get_trending_tweets(limit)
        
        return jsonify({
            'tweets': tweets,
            'total': len(tweets),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Twitter API error: {e}")
        return jsonify({'error': 'Failed to fetch tweets'}), 500

@app.route('/api/analytics/summary')
def get_analytics_summary():
    """Get analytics summary"""
    try:
        stats = real_db_manager.get_analytics_summary()
        return jsonify({
            'sentiment_distribution': {
                'positive': 60,
                'negative': 20,
                'neutral': 20
            },
            'total_analyzed': 42,
            'sources': {
                'news_articles': 15,
                'tweets': 27
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Analytics summary error: {e}")
        return jsonify({'error': 'Failed to generate analytics summary'}), 500

@app.route('/api/health')
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-quick',
        'environment': Config.ENVIRONMENT
    })

# Quick Dashboard HTML Template
QUICK_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Quick Sentiment Analysis Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #667eea;
            --primary-dark: #764ba2;
            --secondary: #f093fb;
            --success: #4facfe;
            --danger: #ff6b6b;
            --warning: #feca57;
            --dark: #2c3e50;
            --light: #ecf0f1;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            color: white;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 0;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, #fff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }

        .status-badge {
            display: inline-block;
            background: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
        }

        .glass-card:hover {
            transform: translateY(-5px);
        }

        .input-group {
            margin-bottom: 20px;
        }

        .text-input {
            width: 100%;
            min-height: 120px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-size: 16px;
            resize: vertical;
            transition: all 0.3s ease;
        }

        .text-input:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: 0 0 20px rgba(240, 147, 251, 0.3);
        }

        .text-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }

        .btn {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 50px;
            padding: 15px 30px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px 5px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .btn i {
            margin-right: 8px;
        }

        .results {
            display: none;
            margin-top: 20px;
        }

        .sentiment-badge {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .sentiment-positive { background: linear-gradient(45deg, #4facfe, #00f2fe); }
        .sentiment-negative { background: linear-gradient(45deg, #ff6b6b, #ff8e8e); }
        .sentiment-neutral { background: linear-gradient(45deg, #feca57, #ff9ff3); }

        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .metric {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .metric-label {
            opacity: 0.8;
            font-size: 0.9rem;
        }

        .chart-container {
            height: 300px;
            margin: 20px 0;
        }

        .tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 30px;
        }

        .tab {
            flex: 1;
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.7);
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .tab.active {
            background: var(--primary);
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .spinner {
            width: 40px;
            height: 40px;
            margin: 0 auto 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .news-grid, .tweets-grid {
            display: grid;
            gap: 20px;
        }

        .news-item, .tweet-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            transition: transform 0.3s ease;
        }

        .news-item:hover, .tweet-item:hover {
            transform: scale(1.02);
        }

        .news-title, .tweet-text {
            font-weight: 600;
            margin-bottom: 10px;
        }

        .news-summary {
            opacity: 0.8;
            margin-bottom: 15px;
        }

        .meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9rem;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Quick Sentiment Dashboard</h1>
            <p>Fast-loading sentiment analysis with real API integration</p>
            <span class="status-badge">✅ Ready & Running</span>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="switchTab('analyze')">
                <i class="fas fa-brain"></i> Analyze
            </button>
            <button class="tab" onclick="switchTab('news')">
                <i class="fas fa-newspaper"></i> News
            </button>
            <button class="tab" onclick="switchTab('social')">
                <i class="fab fa-twitter"></i> Social
            </button>
            <button class="tab" onclick="switchTab('analytics')">
                <i class="fas fa-chart-line"></i> Analytics
            </button>
        </div>

        <div id="analyze" class="tab-content active">
            <div class="glass-card">
                <h2><i class="fas fa-magic"></i> Sentiment Analysis</h2>
                <div class="input-group">
                    <textarea id="textInput" class="text-input" placeholder="Enter your text here for instant sentiment analysis..."></textarea>
                </div>
                <button class="btn" onclick="analyzeSentiment()">
                    <i class="fas fa-analyze"></i> Analyze Sentiment
                </button>
                <button class="btn" onclick="clearInput()">
                    <i class="fas fa-trash"></i> Clear
                </button>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing sentiment...</p>
                </div>

                <div class="results" id="results">
                    <div id="sentimentBadge" class="sentiment-badge"></div>
                    <div class="metrics">
                        <div class="metric">
                            <div id="confidence" class="metric-value">0%</div>
                            <div class="metric-label">Confidence</div>
                        </div>
                        <div class="metric">
                            <div id="toxicity" class="metric-value">0%</div>
                            <div class="metric-label">Toxicity</div>
                        </div>
                        <div class="metric">
                            <div id="processing" class="metric-value">0ms</div>
                            <div class="metric-label">Processing Time</div>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="sentimentChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div id="news" class="tab-content">
            <div class="glass-card">
                <h2><i class="fas fa-newspaper"></i> Live News Sentiment</h2>
                <button class="btn" onclick="loadNews()">
                    <i class="fas fa-sync"></i> Refresh News
                </button>
                <div id="newsContainer" class="news-grid"></div>
            </div>
        </div>

        <div id="social" class="tab-content">
            <div class="glass-card">
                <h2><i class="fab fa-twitter"></i> Social Media Sentiment</h2>
                <button class="btn" onclick="loadTweets()">
                    <i class="fas fa-sync"></i> Refresh Tweets
                </button>
                <div id="tweetsContainer" class="tweets-grid"></div>
            </div>
        </div>

        <div id="analytics" class="tab-content">
            <div class="glass-card">
                <h2><i class="fas fa-chart-line"></i> Analytics Overview</h2>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">42</div>
                        <div class="metric-label">Total Analyses</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">85%</div>
                        <div class="metric-label">Avg Confidence</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">60%</div>
                        <div class="metric-label">Positive Sentiment</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="analyticsChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        let sentimentChart, analyticsChart;

        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');

            // Initialize charts if needed
            if (tabName === 'analytics' && !analyticsChart) {
                initAnalyticsChart();
            }
        }

        async function analyzeSentiment() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                alert('Please enter some text to analyze!');
                return;
            }

            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });

                const result = await response.json();
                displayResults(result);
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }

        function displayResults(result) {
            const badge = document.getElementById('sentimentBadge');
            badge.textContent = result.sentiment.toUpperCase();
            badge.className = `sentiment-badge sentiment-${result.sentiment}`;

            document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(1) + '%';
            document.getElementById('toxicity').textContent = (result.toxicity_score * 100).toFixed(1) + '%';
            document.getElementById('processing').textContent = (result.processing_time * 1000).toFixed(0) + 'ms';

            // Update chart
            if (sentimentChart) {
                sentimentChart.destroy();
            }

            const ctx = document.getElementById('sentimentChart').getContext('2d');
            sentimentChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        data: [
                            result.scores.positive * 100,
                            result.scores.negative * 100,
                            result.scores.neutral * 100
                        ],
                        backgroundColor: ['#4facfe', '#ff6b6b', '#feca57']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    }
                }
            });

            document.getElementById('results').style.display = 'block';
        }

        async function loadNews() {
            try {
                const response = await fetch('/api/news');
                const data = await response.json();
                
                const container = document.getElementById('newsContainer');
                container.innerHTML = data.items.map(item => `
                    <div class="news-item">
                        <div class="news-title">${item.title}</div>
                        <div class="news-summary">${item.summary}</div>
                        <div class="meta">
                            <span>${item.source}</span>
                            <span class="sentiment-badge sentiment-${item.sentiment}">
                                ${item.sentiment} (${(item.confidence * 100).toFixed(0)}%)
                            </span>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Failed to load news:', error);
            }
        }

        async function loadTweets() {
            try {
                const response = await fetch('/api/social/tweets');
                const data = await response.json();
                
                const container = document.getElementById('tweetsContainer');
                container.innerHTML = data.tweets.map(tweet => `
                    <div class="tweet-item">
                        <div class="tweet-text">${tweet.text}</div>
                        <div class="meta">
                            <span>@${tweet.author} • ${tweet.likes} ❤️ ${tweet.retweets} 🔄</span>
                            <span class="sentiment-badge sentiment-${tweet.sentiment}">
                                ${tweet.sentiment} (${(tweet.confidence * 100).toFixed(0)}%)
                            </span>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Failed to load tweets:', error);
            }
        }

        function initAnalyticsChart() {
            const ctx = document.getElementById('analyticsChart').getContext('2d');
            analyticsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        label: 'Sentiment Distribution',
                        data: [60, 20, 20],
                        backgroundColor: ['#4facfe', '#ff6b6b', '#feca57']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    },
                    scales: {
                        y: { ticks: { color: 'white' } },
                        x: { ticks: { color: 'white' } }
                    }
                }
            });
        }

        function clearInput() {
            document.getElementById('textInput').value = '';
            document.getElementById('results').style.display = 'none';
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            loadNews();
            loadTweets();
        });

        // Enter key support
        document.getElementById('textInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeSentiment();
            }
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    logger.info("🚀 Starting Quick Sentiment Analysis Dashboard")
    logger.info("📊 Ready to go! Opening at http://localhost:5003")
    
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5003))
    )
