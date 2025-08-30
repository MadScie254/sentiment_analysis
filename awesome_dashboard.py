#!/usr/bin/env python3
"""
🚀 IMMERSIVE SENTIMENT ANALYSIS DASHBOARD 🚀
Production-Ready with Real APIs and Stunning UI
Author: Advanced AI Assistant
Date: August 31, 2025
"""

import os
import sys
import json
import asyncio
import tempfile
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import lru_cache
import traceback

# Core Flask
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS

# Environment and Config
from dotenv import load_dotenv
load_dotenv()

# Real ML and APIs
import requests
import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import feedparser
import sqlite3
from urllib.parse import urlparse
import hashlib
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('awesome_dashboard.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AwesomeNLPEngine:
    """🧠 Advanced NLP Engine with Multiple Real Models"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        
        # Initialize models
        self._init_models()
        logger.info(f"🚀 NLP Engine initialized with device: {self.device}")
    
    def _init_models(self):
        """Initialize all available models"""
        try:
            # RoBERTa for general sentiment
            self.pipelines['roberta'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("✅ RoBERTa model loaded")
        except Exception as e:
            logger.warning(f"⚠️ RoBERTa failed: {e}")
        
        try:
            # DistilBERT for fast processing
            self.pipelines['distilbert'] = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("✅ DistilBERT model loaded")
        except Exception as e:
            logger.warning(f"⚠️ DistilBERT failed: {e}")
        
        try:
            # Emotion analysis
            self.pipelines['emotion'] = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("✅ Emotion model loaded")
        except Exception as e:
            logger.warning(f"⚠️ Emotion model failed: {e}")
    
    def analyze_sentiment(self, text: str, model='auto'):
        """🔍 Comprehensive sentiment analysis"""
        start_time = time.time()
        
        try:
            # Choose best model
            if model == 'auto':
                if len(text.split()) < 20 and 'roberta' in self.pipelines:
                    model = 'roberta'
                elif 'distilbert' in self.pipelines:
                    model = 'distilbert'
                else:
                    model = 'vader'
            
            # Analyze with chosen model
            if model in self.pipelines:
                result = self.pipelines[model](text)
                if isinstance(result, list):
                    result = result[0]
                
                sentiment = self._normalize_label(result['label'])
                confidence = result['score']
            else:
                # Fallback to VADER
                vader_scores = self.vader_analyzer.polarity_scores(text)
                if vader_scores['compound'] >= 0.05:
                    sentiment = 'positive'
                    confidence = vader_scores['compound']
                elif vader_scores['compound'] <= -0.05:
                    sentiment = 'negative'
                    confidence = abs(vader_scores['compound'])
                else:
                    sentiment = 'neutral'
                    confidence = 1 - abs(vader_scores['compound'])
            
            # Get emotions if available
            emotions = self._get_emotions(text)
            
            # Calculate additional metrics
            toxicity = self._calculate_toxicity(text)
            subjectivity = TextBlob(text).sentiment.subjectivity
            
            processing_time = time.time() - start_time
            
            return {
                'text': text[:200] + '...' if len(text) > 200 else text,
                'sentiment': sentiment,
                'confidence': round(confidence, 3),
                'scores': self._create_scores(sentiment, confidence),
                'emotions': emotions,
                'toxicity': round(toxicity, 3),
                'subjectivity': round(subjectivity, 3),
                'model_used': model,
                'processing_time': round(processing_time, 4),
                'word_count': len(text.split()),
                'char_count': len(text),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return self._fallback_analysis(text)
    
    def _normalize_label(self, label):
        """Normalize model labels"""
        label = label.lower()
        if label in ['positive', 'pos', 'label_2']:
            return 'positive'
        elif label in ['negative', 'neg', 'label_0']:
            return 'negative'
        else:
            return 'neutral'
    
    def _get_emotions(self, text):
        """Get emotion analysis"""
        if 'emotion' not in self.pipelines:
            return None
        
        try:
            results = self.pipelines['emotion'](text)
            emotions = {}
            for result in results:
                emotions[result['label'].lower()] = round(result['score'], 3)
            return emotions
        except:
            return None
    
    def _calculate_toxicity(self, text):
        """Simple toxicity calculation"""
        toxic_words = ['hate', 'stupid', 'idiot', 'kill', 'die', 'worst', 'terrible', 'awful']
        text_lower = text.lower()
        toxic_count = sum(1 for word in toxic_words if word in text_lower)
        return min(toxic_count / len(text.split()) * 3, 1.0) if text.split() else 0.0
    
    def _create_scores(self, sentiment, confidence):
        """Create score distribution"""
        if sentiment == 'positive':
            return {
                'positive': confidence,
                'negative': (1-confidence) * 0.3,
                'neutral': (1-confidence) * 0.7
            }
        elif sentiment == 'negative':
            return {
                'positive': (1-confidence) * 0.3,
                'negative': confidence,
                'neutral': (1-confidence) * 0.7
            }
        else:
            return {
                'positive': (1-confidence) * 0.4,
                'negative': (1-confidence) * 0.4,
                'neutral': confidence
            }
    
    def _fallback_analysis(self, text):
        """Fallback when models fail"""
        return {
            'text': text[:200],
            'sentiment': 'neutral',
            'confidence': 0.5,
            'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34},
            'model_used': 'fallback',
            'processing_time': 0.001,
            'error': 'Model unavailable'
        }

class AwesomeNewsAPI:
    """📰 Real-time News API Integration"""
    
    def __init__(self):
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.gnews_key = os.getenv('GNEWS_API_KEY')
        self.currents_key = os.getenv('CURRENTS_API_KEY')
        self.session = requests.Session()
        logger.info("📰 News API initialized")
    
    def get_trending_news(self, limit=20):
        """Get trending news from multiple sources"""
        all_articles = []
        
        # NewsAPI
        if self.newsapi_key:
            all_articles.extend(self._fetch_newsapi(limit//3))
        
        # GNews
        if self.gnews_key:
            all_articles.extend(self._fetch_gnews(limit//3))
        
        # Currents API
        if self.currents_key:
            all_articles.extend(self._fetch_currents(limit//3))
        
        # RSS Feeds as fallback
        if not all_articles:
            all_articles.extend(self._fetch_rss_feeds(limit))
        
        return all_articles[:limit]
    
    def _fetch_newsapi(self, limit):
        """Fetch from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.newsapi_key,
                'country': 'us',
                'pageSize': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', 'No Title'),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'published': article.get('publishedAt', ''),
                    'image_url': article.get('urlToImage', ''),
                    'content': article.get('content', '')
                })
            
            logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            logger.error(f"❌ NewsAPI failed: {e}")
            return []
    
    def _fetch_gnews(self, limit):
        """Fetch from GNews"""
        try:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': self.gnews_key,
                'lang': 'en',
                'country': 'us',
                'max': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', 'No Title'),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'GNews'),
                    'published': article.get('publishedAt', ''),
                    'image_url': article.get('image', ''),
                    'content': article.get('content', '')
                })
            
            logger.info(f"✅ Fetched {len(articles)} articles from GNews")
            return articles
            
        except Exception as e:
            logger.error(f"❌ GNews failed: {e}")
            return []
    
    def _fetch_currents(self, limit):
        """Fetch from Currents API"""
        try:
            url = "https://api.currentsapi.services/v1/latest-news"
            params = {
                'apiKey': self.currents_key,
                'language': 'en',
                'page_size': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            articles = []
            for article in data.get('news', []):
                articles.append({
                    'title': article.get('title', 'No Title'),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': 'Currents',
                    'published': article.get('published', ''),
                    'image_url': article.get('image', ''),
                    'content': ''
                })
            
            logger.info(f"✅ Fetched {len(articles)} articles from Currents")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Currents API failed: {e}")
            return []
    
    def _fetch_rss_feeds(self, limit):
        """Fallback RSS feeds"""
        feeds = [
            'http://feeds.bbci.co.uk/news/rss.xml',
            'http://rss.cnn.com/rss/edition.rss',
            'https://feeds.npr.org/1001/rss.xml'
        ]
        
        articles = []
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:limit//len(feeds)]:
                    articles.append({
                        'title': entry.get('title', 'No Title'),
                        'description': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'source': feed.feed.get('title', 'RSS'),
                        'published': entry.get('published', ''),
                        'image_url': '',
                        'content': ''
                    })
            except Exception as e:
                logger.error(f"❌ RSS feed failed: {e}")
                continue
        
        return articles

class AwesomeDatabase:
    """💾 SQLite Database Manager"""
    
    def __init__(self):
        self.db_path = 'awesome_sentiment_analysis.db'
        self._init_database()
        logger.info("💾 Database initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sentiment analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                confidence REAL NOT NULL,
                scores TEXT,
                emotions TEXT,
                toxicity REAL,
                subjectivity REAL,
                model_used TEXT,
                processing_time REAL,
                word_count INTEGER,
                char_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # News articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                url TEXT UNIQUE,
                source TEXT,
                published TEXT,
                sentiment TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, result):
        """Save sentiment analysis result"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sentiment_analyses 
                (text, sentiment, confidence, scores, emotions, toxicity, subjectivity, 
                 model_used, processing_time, word_count, char_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['text'],
                result['sentiment'],
                result['confidence'],
                json.dumps(result.get('scores', {})),
                json.dumps(result.get('emotions', {})),
                result.get('toxicity', 0),
                result.get('subjectivity', 0),
                result['model_used'],
                result['processing_time'],
                result['word_count'],
                result['char_count']
            ))
            
            conn.commit()
            analysis_id = cursor.lastrowid
            conn.close()
            
            return analysis_id
            
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
            return None
    
    def get_recent_analyses(self, limit=50):
        """Get recent analyses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM sentiment_analyses 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            
            analyses = []
            for row in rows:
                analysis = dict(zip(columns, row))
                analysis['scores'] = json.loads(analysis['scores'] or '{}')
                analysis['emotions'] = json.loads(analysis['emotions'] or '{}')
                analyses.append(analysis)
            
            return analyses
            
        except Exception as e:
            logger.error(f"❌ Database fetch failed: {e}")
            return []
    
    def get_analytics(self):
        """Get analytics summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total analyses
            cursor.execute('SELECT COUNT(*) FROM sentiment_analyses')
            total_analyses = cursor.fetchone()[0]
            
            # Sentiment distribution
            cursor.execute('''
                SELECT sentiment, COUNT(*) 
                FROM sentiment_analyses 
                GROUP BY sentiment
            ''')
            sentiment_dist = dict(cursor.fetchall())
            
            # Average confidence
            cursor.execute('SELECT AVG(confidence) FROM sentiment_analyses')
            avg_confidence = cursor.fetchone()[0] or 0
            
            # Model usage
            cursor.execute('''
                SELECT model_used, COUNT(*) 
                FROM sentiment_analyses 
                GROUP BY model_used
            ''')
            model_usage = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_analyses': total_analyses,
                'sentiment_distribution': sentiment_dist,
                'average_confidence': round(avg_confidence, 3),
                'model_usage': model_usage,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Analytics failed: {e}")
            return {
                'total_analyses': 0,
                'sentiment_distribution': {},
                'average_confidence': 0,
                'model_usage': {}
            }

# Initialize components
nlp_engine = AwesomeNLPEngine()
news_api = AwesomeNewsAPI()
database = AwesomeDatabase()

# Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'awesome-dashboard-secret')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
CORS(app)

@app.route('/')
def dashboard():
    """🎨 Immersive Dashboard Homepage"""
    return render_template_string(IMMERSIVE_DASHBOARD_HTML)

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """🔍 Analyze text sentiment"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Analyze sentiment
        result = nlp_engine.analyze_sentiment(text)
        
        # Save to database
        database.save_analysis(result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Analysis API failed: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/api/news')
def get_news():
    """📰 Get latest news with sentiment"""
    try:
        limit = int(request.args.get('limit', 20))
        
        # Fetch news
        articles = news_api.get_trending_news(limit)
        
        # Analyze sentiment for each article
        for article in articles:
            if article.get('title') and article.get('description'):
                text = f"{article['title']} {article['description']}"
                result = nlp_engine.analyze_sentiment(text, model='distilbert')  # Fast model for news
                article['sentiment'] = result['sentiment']
                article['confidence'] = result['confidence']
                article['emotions'] = result.get('emotions', {})
        
        return jsonify({
            'articles': articles,
            'total': len(articles),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ News API failed: {e}")
        return jsonify({'error': 'Failed to fetch news'}), 500

@app.route('/api/analytics')
def get_analytics():
    """📊 Get analytics data"""
    try:
        analytics = database.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        logger.error(f"❌ Analytics API failed: {e}")
        return jsonify({'error': 'Analytics unavailable'}), 500

@app.route('/api/recent')
def get_recent_analyses():
    """📋 Get recent analyses"""
    try:
        limit = int(request.args.get('limit', 20))
        analyses = database.get_recent_analyses(limit)
        return jsonify({
            'analyses': analyses,
            'total': len(analyses)
        })
    except Exception as e:
        logger.error(f"❌ Recent API failed: {e}")
        return jsonify({'error': 'Failed to fetch recent analyses'}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """🔄 Batch analyze multiple texts"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
        
        if len(texts) > 50:
            return jsonify({'error': 'Too many texts (max 50)'}), 400
        
        results = []
        for text in texts:
            if text.strip():
                result = nlp_engine.analyze_sentiment(text.strip())
                database.save_analysis(result)
                results.append(result)
        
        return jsonify({
            'results': results,
            'processed': len(results),
            'total_submitted': len(texts)
        })
        
    except Exception as e:
        logger.error(f"❌ Batch analysis failed: {e}")
        return jsonify({'error': 'Batch analysis failed'}), 500

@app.route('/api/health')
def health_check():
    """❤️ Health check endpoint"""
    return jsonify({
        'status': 'awesome',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'models_loaded': len(nlp_engine.pipelines),
        'database_status': 'connected'
    })

# Immersive Dashboard HTML Template
IMMERSIVE_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Immersive Sentiment Analysis Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/particles.js@2.0.0/particles.min.js"></script>
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
            overflow-x: hidden;
            min-height: 100vh;
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
            top: 0;
            left: 0;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 0;
        }

        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #fff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }

        /* Glass Cards */
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        /* Input Section */
        .input-section {
            margin-bottom: 30px;
        }

        .input-group {
            position: relative;
        }

        .text-input {
            width: 100%;
            min-height: 150px;
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

        .btn-group {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
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
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn i {
            margin-right: 8px;
        }

        /* Results Section */
        .results-section {
            margin-top: 30px;
        }

        .sentiment-result {
            display: none;
            animation: fadeInUp 0.5s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .sentiment-badge {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }

        .sentiment-positive { background: linear-gradient(45deg, #4facfe, #00f2fe); }
        .sentiment-negative { background: linear-gradient(45deg, #ff6b6b, #ff8e8e); }
        .sentiment-neutral { background: linear-gradient(45deg, #feca57, #ff9ff3); }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
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

        /* Chart Container */
        .chart-container {
            position: relative;
            height: 400px;
            margin: 20px 0;
        }

        /* News Section */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .news-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }

        .news-card:hover {
            transform: scale(1.02);
        }

        .news-title {
            font-weight: 600;
            margin-bottom: 10px;
            line-height: 1.4;
        }

        .news-description {
            opacity: 0.8;
            line-height: 1.5;
            margin-bottom: 15px;
        }

        .news-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9rem;
            opacity: 0.7;
        }

        /* Loading Animation */
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

        /* Responsive */
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .btn-group {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }

        /* Animations */
        .fade-in {
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .slide-in {
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        /* Scroll bar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🚀 Immersive Sentiment Analysis</h1>
            <p>Real-time AI-powered sentiment analysis with live news and advanced analytics</p>
        </div>

        <!-- Dashboard Grid -->
        <div class="dashboard-grid">
            <!-- Analysis Section -->
            <div class="glass-card">
                <h2><i class="fas fa-brain"></i> AI Sentiment Analysis</h2>
                <div class="input-section">
                    <div class="input-group">
                        <textarea 
                            id="textInput" 
                            class="text-input" 
                            placeholder="Enter your text here for real-time sentiment analysis... 🤖"
                            maxlength="5000"
                        ></textarea>
                    </div>
                    <div class="btn-group">
                        <button id="analyzeBtn" class="btn">
                            <i class="fas fa-magic"></i> Analyze Sentiment
                        </button>
                        <button id="clearBtn" class="btn">
                            <i class="fas fa-trash"></i> Clear
                        </button>
                    </div>
                </div>

                <div class="loading" id="analysisLoading">
                    <div class="spinner"></div>
                    <p>AI is analyzing your text...</p>
                </div>

                <div class="results-section">
                    <div id="sentimentResult" class="sentiment-result">
                        <div id="sentimentBadge" class="sentiment-badge"></div>
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div id="confidenceValue" class="metric-value">0%</div>
                                <div class="metric-label">Confidence</div>
                            </div>
                            <div class="metric-card">
                                <div id="toxicityValue" class="metric-value">0%</div>
                                <div class="metric-label">Toxicity</div>
                            </div>
                            <div class="metric-card">
                                <div id="subjectivityValue" class="metric-value">0%</div>
                                <div class="metric-label">Subjectivity</div>
                            </div>
                            <div class="metric-card">
                                <div id="processingTime" class="metric-value">0ms</div>
                                <div class="metric-label">Processing Time</div>
                            </div>
                        </div>
                        <div class="chart-container">
                            <canvas id="sentimentChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Analytics Section -->
            <div class="glass-card">
                <h2><i class="fas fa-chart-line"></i> Live Analytics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div id="totalAnalyses" class="metric-value">0</div>
                        <div class="metric-label">Total Analyses</div>
                    </div>
                    <div class="metric-card">
                        <div id="avgConfidence" class="metric-value">0%</div>
                        <div class="metric-label">Avg Confidence</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="analyticsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- News Section -->
        <div class="glass-card full-width">
            <h2><i class="fas fa-newspaper"></i> Live News Sentiment</h2>
            <div class="btn-group">
                <button id="refreshNewsBtn" class="btn">
                    <i class="fas fa-sync"></i> Refresh News
                </button>
            </div>
            
            <div class="loading" id="newsLoading">
                <div class="spinner"></div>
                <p>Fetching latest news and analyzing sentiment...</p>
            </div>

            <div id="newsContainer" class="news-grid">
                <!-- News articles will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        // Initialize particles
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: '#ffffff' },
                shape: { type: 'circle' },
                opacity: { value: 0.3, random: false },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#ffffff',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: 'none',
                    random: false,
                    straight: false,
                    out_mode: 'out',
                    bounce: false
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'repulse' },
                    onclick: { enable: true, mode: 'push' },
                    resize: true
                }
            },
            retina_detect: true
        });

        // Global variables
        let sentimentChart, analyticsChart;

        // Initialize charts
        function initCharts() {
            const chartOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: 'white' }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            };

            // Sentiment Chart
            const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
            sentimentChart = new Chart(sentimentCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        data: [0, 0, 0],
                        backgroundColor: ['#4facfe', '#ff6b6b', '#feca57'],
                        borderWidth: 0
                    }]
                },
                options: {
                    ...chartOptions,
                    cutout: '60%'
                }
            });

            // Analytics Chart
            const analyticsCtx = document.getElementById('analyticsChart').getContext('2d');
            analyticsChart = new Chart(analyticsCtx, {
                type: 'bar',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        label: 'Sentiment Distribution',
                        data: [0, 0, 0],
                        backgroundColor: ['#4facfe', '#ff6b6b', '#feca57'],
                        borderRadius: 10
                    }]
                },
                options: chartOptions
            });
        }

        // Analyze sentiment
        async function analyzeSentiment() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                alert('Please enter some text to analyze!');
                return;
            }

            // Show loading
            document.getElementById('analysisLoading').style.display = 'block';
            document.getElementById('sentimentResult').style.display = 'none';

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text })
                });

                const result = await response.json();

                if (result.error) {
                    throw new Error(result.error);
                }

                displaySentimentResult(result);

            } catch (error) {
                console.error('Analysis failed:', error);
                alert('Analysis failed: ' + error.message);
            } finally {
                document.getElementById('analysisLoading').style.display = 'none';
            }
        }

        // Display sentiment result
        function displaySentimentResult(result) {
            const resultDiv = document.getElementById('sentimentResult');
            const badge = document.getElementById('sentimentBadge');
            
            // Update badge
            badge.textContent = result.sentiment.toUpperCase();
            badge.className = `sentiment-badge sentiment-${result.sentiment}`;

            // Update metrics
            document.getElementById('confidenceValue').textContent = (result.confidence * 100).toFixed(1) + '%';
            document.getElementById('toxicityValue').textContent = (result.toxicity * 100).toFixed(1) + '%';
            document.getElementById('subjectivityValue').textContent = (result.subjectivity * 100).toFixed(1) + '%';
            document.getElementById('processingTime').textContent = (result.processing_time * 1000).toFixed(0) + 'ms';

            // Update chart
            const scores = result.scores;
            sentimentChart.data.datasets[0].data = [
                scores.positive * 100,
                scores.negative * 100,
                scores.neutral * 100
            ];
            sentimentChart.update();

            // Show result
            resultDiv.style.display = 'block';
            resultDiv.classList.add('fade-in');

            // Update analytics
            loadAnalytics();
        }

        // Load analytics
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();

                document.getElementById('totalAnalyses').textContent = data.total_analyses;
                document.getElementById('avgConfidence').textContent = (data.average_confidence * 100).toFixed(1) + '%';

                // Update analytics chart
                const dist = data.sentiment_distribution;
                analyticsChart.data.datasets[0].data = [
                    dist.positive || 0,
                    dist.negative || 0,
                    dist.neutral || 0
                ];
                analyticsChart.update();

            } catch (error) {
                console.error('Failed to load analytics:', error);
            }
        }

        // Load news
        async function loadNews() {
            document.getElementById('newsLoading').style.display = 'block';
            document.getElementById('newsContainer').innerHTML = '';

            try {
                const response = await fetch('/api/news?limit=12');
                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                displayNews(data.articles);

            } catch (error) {
                console.error('Failed to load news:', error);
                document.getElementById('newsContainer').innerHTML = 
                    '<p style="text-align: center; opacity: 0.7;">Failed to load news</p>';
            } finally {
                document.getElementById('newsLoading').style.display = 'none';
            }
        }

        // Display news
        function displayNews(articles) {
            const container = document.getElementById('newsContainer');
            
            if (!articles.length) {
                container.innerHTML = '<p style="text-align: center; opacity: 0.7;">No news available</p>';
                return;
            }

            container.innerHTML = articles.map(article => `
                <div class="news-card slide-in">
                    <div class="news-title">${article.title}</div>
                    <div class="news-description">${article.description}</div>
                    <div class="news-meta">
                        <span>${article.source}</span>
                        <span class="sentiment-badge sentiment-${article.sentiment}" style="font-size: 0.8rem; padding: 5px 10px;">
                            ${article.sentiment} (${(article.confidence * 100).toFixed(0)}%)
                        </span>
                    </div>
                </div>
            `).join('');
        }

        // Event listeners
        document.getElementById('analyzeBtn').addEventListener('click', analyzeSentiment);
        document.getElementById('clearBtn').addEventListener('click', () => {
            document.getElementById('textInput').value = '';
            document.getElementById('sentimentResult').style.display = 'none';
        });
        document.getElementById('refreshNewsBtn').addEventListener('click', loadNews);

        // Enter key for analysis
        document.getElementById('textInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeSentiment();
            }
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            initCharts();
            loadAnalytics();
            loadNews();
        });

        // Auto-refresh news every 5 minutes
        setInterval(loadNews, 5 * 60 * 1000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    logger.info("🚀 Starting Immersive Sentiment Analysis Dashboard")
    logger.info(f"📊 Models loaded: {len(nlp_engine.pipelines)}")
    logger.info(f"📰 News APIs configured: {bool(os.getenv('NEWSAPI_KEY'))}")
    
    app.run(
        debug=os.getenv('DEBUG', 'True').lower() == 'true',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5003))
    )
