"""
Enhanced Immersive Dashboard - Production Ready
Stable charts, paginated news, video metadata extraction, modular design
"""

from flask import Flask, render_template_string, jsonify, request, Response
import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import random
import os
import hashlib
import time
from functools import lru_cache
from collections import Counter
import threading

# Import our core modules
from database_manager import db_manager
from ui_components import ui_generator
from config import Config
from nlp_engine import SentimentAnalyzer
from video_metadata import VideoMetadataExtractor

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize components with enhanced caching
sentiment_analyzer = SentimentAnalyzer()
video_metadata_extractor = VideoMetadataExtractor()

# Application cache for performance
_cache = {}
_cache_lock = threading.Lock()
CACHE_TIMEOUT = 300  # 5 minutes

# Enhanced sample data with more diversity
SAMPLE_ANALYSES = [
    {
        'id': 1,
        'content': 'Revolutionary AI breakthrough announced at tech conference',
        'source': 'tech_news',
        'sentiment': 'positive',
        'confidence': 0.92,
        'toxicity': 0.05,
        'emotion': ['excitement', 'optimism'],
        'timestamp': datetime.now().isoformat(),
        'language': 'en',
        'location': 'USA'
    },
    {
        'id': 2,
        'content': 'New sustainable energy solution shows promising results',
        'source': 'science_news',
        'sentiment': 'positive',
        'confidence': 0.87,
        'toxicity': 0.02,
        'emotion': ['hope', 'interest'],
        'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
        'language': 'en',
        'location': 'Europe'
    },
    {
        'id': 3,
        'content': 'Market volatility creates uncertainty for investors',
        'source': 'finance_news',
        'sentiment': 'negative',
        'confidence': 0.78,
        'toxicity': 0.15,
        'emotion': ['anxiety', 'concern'],
        'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat(),
        'language': 'en',
        'location': 'Asia'
    },
    {
        'id': 4,
        'content': 'Standard quarterly earnings report released',
        'source': 'business_news',
        'sentiment': 'neutral',
        'confidence': 0.65,
        'toxicity': 0.08,
        'emotion': ['neutral'],
        'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat(),
        'language': 'en',
        'location': 'USA'
    },
    {
        'id': 5,
        'content': 'Amazing new features in latest software update!',
        'source': 'social_media',
        'sentiment': 'positive',
        'confidence': 0.89,
        'toxicity': 0.03,
        'emotion': ['joy', 'excitement'],
        'timestamp': (datetime.now() - timedelta(minutes=20)).isoformat(),
        'language': 'en',
        'location': 'Global'
    }
]

@lru_cache(maxsize=128)
def get_cached_sentiment_data(cache_key: str) -> Dict[str, Any]:
    """Generate and cache sentiment data"""
    with _cache_lock:
        current_time = time.time()
        cache_entry = _cache.get(cache_key)
        
        if cache_entry and (current_time - cache_entry['timestamp']) < CACHE_TIMEOUT:
            return cache_entry['data']
        
        # Generate new data
        data = generate_sentiment_data()
        _cache[cache_key] = {
            'timestamp': current_time,
            'data': data
        }
        return data

def generate_sentiment_data() -> Dict[str, Any]:
    """Generate comprehensive sentiment data"""
    now = datetime.now()
    timestamps = [(now - timedelta(hours=i)).strftime("%H:%M") for i in range(24, 0, -1)]
    
    # Generate time series data with trends and anomalies
    base_positive = 0.6
    base_negative = 0.2
    base_neutral = 0.2
    
    positive_scores = []
    negative_scores = []
    neutral_scores = []
    
    for i in range(24):
        # Add some realistic variation
        noise = random.uniform(-0.1, 0.1)
        trend = 0.05 * math.sin(i * math.pi / 12)  # Daily cycle
        
        pos = max(0.1, min(0.9, base_positive + trend + noise))
        neg = max(0.05, min(0.4, base_negative - trend/2 + noise/2))
        neu = 1.0 - pos - neg
        
        positive_scores.append(round(pos, 3))
        negative_scores.append(round(neg, 3))
        neutral_scores.append(round(neu, 3))
    
    return {
        'timestamps': timestamps,
        'sentiment_scores': {
            'positive': positive_scores,
            'negative': negative_scores,
            'neutral': neutral_scores
        },
        'toxicity_scores': [random.uniform(0.05, 0.3) for _ in range(24)],
        'volume': [random.randint(50, 200) for _ in range(24)],
        'total_analyzed': random.randint(5000, 15000),
        'sentiment_distribution': {
            'positive': round(sum(positive_scores) / len(positive_scores), 3),
            'negative': round(sum(negative_scores) / len(negative_scores), 3),
            'neutral': round(sum(neutral_scores) / len(neutral_scores), 3)
        },
        'top_sources': [
            {'name': 'Twitter', 'count': random.randint(1000, 3000), 'sentiment': 0.6},
            {'name': 'YouTube', 'count': random.randint(500, 2000), 'sentiment': 0.7},
            {'name': 'Instagram', 'count': random.randint(300, 1500), 'sentiment': 0.8},
            {'name': 'Facebook', 'count': random.randint(200, 1000), 'sentiment': 0.5},
            {'name': 'TikTok', 'count': random.randint(100, 800), 'sentiment': 0.75}
        ],
        'top_emotions': [
            {'emotion': 'joy', 'count': random.randint(800, 1200)},
            {'emotion': 'excitement', 'count': random.randint(600, 1000)},
            {'emotion': 'concern', 'count': random.randint(400, 800)},
            {'emotion': 'anger', 'count': random.randint(200, 600)},
            {'emotion': 'surprise', 'count': random.randint(300, 700)}
        ],
        'anomalies': [
            {
                'timestamp': timestamps[random.randint(0, 23)],
                'type': 'sentiment_spike',
                'severity': 'medium',
                'description': 'Unusual increase in positive sentiment detected'
            },
            {
                'timestamp': timestamps[random.randint(0, 23)],
                'type': 'volume_spike',
                'severity': 'high',
                'description': 'Significant increase in comment volume'
            }
        ]
    }

def get_word_cloud_data() -> List[Dict[str, Any]]:
    """Generate word cloud data"""
    words = [
        {'text': 'amazing', 'size': 40, 'sentiment': 'positive'},
        {'text': 'love', 'size': 35, 'sentiment': 'positive'},
        {'text': 'great', 'size': 32, 'sentiment': 'positive'},
        {'text': 'awesome', 'size': 30, 'sentiment': 'positive'},
        {'text': 'excellent', 'size': 28, 'sentiment': 'positive'},
        {'text': 'fantastic', 'size': 25, 'sentiment': 'positive'},
        {'text': 'disappointed', 'size': 22, 'sentiment': 'negative'},
        {'text': 'terrible', 'size': 20, 'sentiment': 'negative'},
        {'text': 'bad', 'size': 18, 'sentiment': 'negative'},
        {'text': 'okay', 'size': 16, 'sentiment': 'neutral'},
        {'text': 'fine', 'size': 14, 'sentiment': 'neutral'},
        {'text': 'good', 'size': 26, 'sentiment': 'positive'},
        {'text': 'nice', 'size': 24, 'sentiment': 'positive'},
        {'text': 'horrible', 'size': 15, 'sentiment': 'negative'},
        {'text': 'mediocre', 'size': 12, 'sentiment': 'neutral'}
    ]
    return words

def get_paginated_news(page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Get paginated news with no infinite scroll"""
    # Simulate news data
    all_news = []
    for i in range(100):  # Total of 100 news items
        all_news.append({
            'id': i + 1,
            'title': f'Breaking News Item {i + 1}',
            'summary': f'This is a summary of news item {i + 1} with important information.',
            'source': random.choice(['Reuters', 'BBC', 'CNN', 'TechCrunch', 'The Verge']),
            'timestamp': (datetime.now() - timedelta(hours=i)).isoformat(),
            'sentiment': random.choice(['positive', 'negative', 'neutral']),
            'confidence': round(random.uniform(0.6, 0.95), 3),
            'url': f'https://example.com/news/{i + 1}'
        })
    
    # Paginate
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = all_news[start_idx:end_idx]
    
    return {
        'items': page_items,
        'page': page,
        'per_page': per_page,
        'total': len(all_news),
        'total_pages': (len(all_news) + per_page - 1) // per_page,
        'has_next': end_idx < len(all_news),
        'has_prev': page > 1
    }

@app.route('/')
def dashboard():
    """Enhanced immersive dashboard with stable charts and tabbed layout"""
    
    # Get cached data for better performance
    sentiment_data = get_cached_sentiment_data("main_dashboard")
    stats = db_manager.get_dashboard_summary()
    
    # Enhanced trend analysis
    trend_analysis = {
        'momentum': {
            'direction': 'positive' if sentiment_data['sentiment_distribution']['positive'] > 0.5 else 'negative',
            'strength': 'strong' if abs(sentiment_data['sentiment_distribution']['positive'] - 0.5) > 0.2 else 'moderate'
        },
        'volatility': {
            'risk_level': 'low' if max(sentiment_data['toxicity_scores']) < 0.3 else 'medium'
        },
        'prediction': {
            'confidence': round(sentiment_data['sentiment_distribution']['positive'], 2)
        }
    }
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{Config.APP_NAME} - Enhanced Sentiment Intelligence</title>
        
        <!-- External Libraries -->
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/jasondavies/d3-cloud@v1.2.5/d3.layout.cloud.js"></script>
        
        <style>
            {ui_generator.generate_complete_css()}
            
            /* STABLE CHART FIXES - No resize on scroll */
            .chart-container {{
                position: relative;
                width: 100%;
                height: 400px !important; /* FIXED HEIGHT */
                overflow: hidden;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1rem;
            }}
            
            .chart-container canvas {{
                max-width: 100% !important;
                max-height: 380px !important; /* FIXED MAX HEIGHT */
                width: auto !important;
                height: auto !important;
            }}
            
            /* Prevent any scroll-based resizing */
            .chart-wrapper {{
                position: relative;
                height: 100%;
                width: 100%;
                overflow: hidden;
            }}
            
            /* Mini charts also fixed */
            .chart-mini {{
                height: 120px !important;
                width: 100%;
                position: relative;
                overflow: hidden;
            }}
            
            .chart-mini canvas {{
                max-height: 100px !important;
            }}
            
            /* Word cloud container - FIXED SIZE */
            .word-cloud-container {{
                height: 400px !important;
                width: 100%;
                overflow: hidden;
                position: relative;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
            }}
            
            .word-cloud-container svg {{
                width: 100% !important;
                height: 100% !important;
                max-width: 100%;
                max-height: 100%;
            }}
            
            /* Enhanced tab system */
            .tab-container {{
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                overflow: hidden;
                margin: 2rem 0;
                box-shadow: var(--shadow-lg);
            }}
            
            .tab-nav {{
                display: flex;
                background: var(--surface);
                border-bottom: 1px solid var(--glass-border);
                overflow-x: auto;
                scrollbar-width: none;
            }}
            
            .tab-nav::-webkit-scrollbar {{
                display: none;
            }}
            
            .tab-btn {{
                flex: 1;
                min-width: max-content;
                background: transparent;
                border: none;
                color: var(--text-secondary);
                padding: 1rem 1.5rem;
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-weight: 500;
                white-space: nowrap;
                position: relative;
            }}
            
            .tab-btn::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                transform: scaleX(0);
                transition: transform var(--transition-normal) var(--ease);
            }}
            
            .tab-btn:hover {{
                color: var(--text-primary);
                background: rgba(255, 255, 255, 0.05);
            }}
            
            .tab-btn.active {{
                color: var(--primary);
                background: rgba(99, 102, 241, 0.1);
            }}
            
            .tab-btn.active::after {{
                transform: scaleX(1);
            }}
            
            .tab-content {{
                padding: 2rem;
                min-height: 500px;
            }}
            
            .tab-pane {{
                display: none;
                animation: fadeInUp var(--transition-normal) var(--ease);
            }}
            
            .tab-pane.active {{
                display: block;
            }}
            
            /* Pagination styles - NO INFINITE SCROLL */
            .pagination-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.5rem;
                margin: 2rem 0;
                padding: 1rem;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
            }}
            
            .pagination-btn {{
                background: var(--glass);
                border: 1px solid var(--glass-border);
                color: var(--text-primary);
                padding: 0.5rem 1rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                min-width: 40px;
                text-align: center;
            }}
            
            .pagination-btn:hover:not(:disabled) {{
                background: var(--primary);
                border-color: var(--primary);
                transform: translateY(-1px);
            }}
            
            .pagination-btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .pagination-btn.active {{
                background: var(--primary);
                border-color: var(--primary);
                font-weight: 600;
            }}
            
            .load-more-btn {{
                background: linear-gradient(135deg, var(--primary), var(--accent));
                border: none;
                color: white;
                padding: 0.75rem 2rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-weight: 600;
                transition: all var(--transition-normal) var(--ease);
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin: 1rem auto;
            }}
            
            .load-more-btn:hover {{
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }}
            
            /* Media panel styles */
            .media-panel {{
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                margin-bottom: 1rem;
            }}
            
            .media-input-toggle {{
                display: flex;
                background: var(--glass);
                border-radius: var(--border-radius);
                padding: 0.25rem;
                margin-bottom: 1rem;
            }}
            
            .media-toggle-btn {{
                flex: 1;
                background: transparent;
                border: none;
                color: var(--text-secondary);
                padding: 0.5rem 1rem;
                border-radius: calc(var(--border-radius) - 0.25rem);
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
            }}
            
            .media-toggle-btn.active {{
                background: var(--primary);
                color: white;
            }}
            
            .metadata-card {{
                background: var(--surface);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                margin-top: 1rem;
            }}
            
            .metadata-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-bottom: 1rem;
            }}
            
            .metadata-item {{
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }}
            
            .metadata-label {{
                font-size: 0.75rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-weight: 500;
            }}
            
            .metadata-value {{
                color: var(--text-primary);
                font-weight: 500;
            }}
            
            /* News item styles */
            .news-item {{
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                margin-bottom: 1rem;
                transition: all var(--transition-normal) var(--ease);
            }}
            
            .news-item:hover {{
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
                border-color: rgba(255, 255, 255, 0.3);
            }}
            
            .news-title {{
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }}
            
            .news-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
            }}
            
            .sentiment-badge {{
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.75rem;
                font-weight: 500;
                text-transform: uppercase;
            }}
            
            .sentiment-positive {{
                background: var(--success);
                color: white;
            }}
            
            .sentiment-negative {{
                background: var(--error);
                color: white;
            }}
            
            .sentiment-neutral {{
                background: var(--neutral);
                color: white;
            }}
        </style>
    </head>
    <body>
        <div id="particles-js" class="particles-bg"></div>
        
        <!-- Enhanced Dashboard Header -->
        <div class="dashboard-header" data-animate="fade-down">
            <div class="container">
                <h1 class="dashboard-title">{Config.APP_NAME}</h1>
                <p class="dashboard-subtitle">
                    Enhanced sentiment intelligence platform with stable charts, video metadata extraction, 
                    and comprehensive analysis capabilities
                </p>
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>System Operational</span>
                </div>
            </div>
        </div>
        
        <!-- Main Dashboard Content -->
        <div class="container">
            <!-- Enhanced Metrics Grid -->
            <div class="metric-grid stagger-fade-in">
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="metric-value" id="total-analyses">{stats.get('today', {{}}).get('total_analyses', 0)}</div>
                    <div class="metric-label">Today's Analyses</div>
                    <div class="chart-mini">
                        <canvas id="analyses-trend"></canvas>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-smile"></i>
                    </div>
                    <div class="metric-value" id="avg-confidence">{sentiment_data['sentiment_distribution']['positive']:.1%}</div>
                    <div class="metric-label">Positive Sentiment</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {sentiment_data['sentiment_distribution']['positive'] * 100}%"></div>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div class="metric-value" id="toxicity-level">{max(sentiment_data['toxicity_scores']):.1%}</div>
                    <div class="metric-label">Max Toxicity Level</div>
                    <div class="real-time-badge">
                        <i class="fas fa-check"></i>
                        <span>Safe</span>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="metric-value" id="ai-insights">{len(sentiment_data['anomalies'])}</div>
                    <div class="metric-label">AI Insights</div>
                    <div class="chart-mini">
                        <canvas id="sentiment-distribution"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Enhanced Tabbed Layout -->
            <div class="tab-container" data-animate="fade-up">
                <div class="tab-nav">
                    <button class="tab-btn active" onclick="switchTab('overview', this)">
                        <i class="fas fa-tachometer-alt"></i>
                        Overview
                    </button>
                    <button class="tab-btn" onclick="switchTab('trends', this)">
                        <i class="fas fa-chart-area"></i>
                        Trends
                    </button>
                    <button class="tab-btn" onclick="switchTab('segments', this)">
                        <i class="fas fa-puzzle-piece"></i>
                        Segments
                    </button>
                    <button class="tab-btn" onclick="switchTab('news', this)">
                        <i class="fas fa-newspaper"></i>
                        News
                    </button>
                    <button class="tab-btn" onclick="switchTab('media', this)">
                        <i class="fas fa-video"></i>
                        Media
                    </button>
                    <button class="tab-btn" onclick="switchTab('admin', this)">
                        <i class="fas fa-cog"></i>
                        Admin
                    </button>
                </div>
                
                <div class="tab-content">
                    <!-- Overview Tab -->
                    <div id="overview" class="tab-pane active">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-pie text-primary"></i>
                                    Sentiment Distribution
                                </h3>
                                <div class="chart-container">
                                    <canvas id="sentiment-pie-chart"></canvas>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-exclamation-triangle text-warning"></i>
                                    Toxicity Gauge
                                </h3>
                                <div class="chart-container">
                                    <canvas id="toxicity-gauge"></canvas>
                                </div>
                            </div>
                        </div>
                        
                        <div class="glass-card mt-6">
                            <h3 class="mb-4">
                                <i class="fas fa-lightbulb text-accent"></i>
                                Quick Insights
                            </h3>
                            <div class="grid grid-cols-3 gap-4">
                                <div class="insight-card">
                                    <h4>Momentum</h4>
                                    <div class="text-2xl font-bold text-{trend_analysis['momentum']['direction']}">
                                        {trend_analysis['momentum']['direction'].title()}
                                    </div>
                                    <p class="text-sm text-secondary">
                                        {trend_analysis['momentum']['strength'].title()} strength
                                    </p>
                                </div>
                                
                                <div class="insight-card">
                                    <h4>Risk Level</h4>
                                    <div class="text-2xl font-bold text-success">
                                        {trend_analysis['volatility']['risk_level'].title()}
                                    </div>
                                    <p class="text-sm text-secondary">Toxicity assessment</p>
                                </div>
                                
                                <div class="insight-card">
                                    <h4>Confidence</h4>
                                    <div class="text-2xl font-bold text-accent">
                                        {trend_analysis['prediction']['confidence']:.0%}
                                    </div>
                                    <p class="text-sm text-secondary">Model confidence</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Trends Tab -->
                    <div id="trends" class="tab-pane">
                        <div class="glass-card">
                            <h3 class="mb-4">
                                <i class="fas fa-chart-line text-primary"></i>
                                24-Hour Sentiment Trends
                            </h3>
                            <div class="chart-container">
                                <canvas id="trends-chart"></canvas>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-6 mt-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-bar text-accent"></i>
                                    Volume by Hour
                                </h3>
                                <div class="chart-container">
                                    <canvas id="volume-chart"></canvas>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-exclamation-circle text-warning"></i>
                                    Anomaly Detection
                                </h3>
                                <div id="anomalies-list">
                                    {generate_anomalies_html(sentiment_data['anomalies'])}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Segments Tab -->
                    <div id="segments" class="tab-pane">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-cloud text-primary"></i>
                                    Word Cloud
                                </h3>
                                <div class="word-cloud-container">
                                    <div id="word-cloud"></div>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-pie text-accent"></i>
                                    Sources Distribution
                                </h3>
                                <div class="chart-container">
                                    <canvas id="sources-chart"></canvas>
                                </div>
                            </div>
                        </div>
                        
                        <div class="glass-card mt-6">
                            <h3 class="mb-4">
                                <i class="fas fa-heart text-error"></i>
                                Top Emotions
                            </h3>
                            <div class="chart-container">
                                <canvas id="emotions-chart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <!-- News Tab - WITH PAGINATION -->
                    <div id="news" class="tab-pane">
                        <div class="glass-card">
                            <h3 class="mb-4">
                                <i class="fas fa-newspaper text-primary"></i>
                                Curated News Feed
                            </h3>
                            <div id="news-container">
                                <!-- News items will be loaded here via AJAX -->
                            </div>
                            <div class="pagination-container" id="news-pagination">
                                <!-- Pagination will be loaded here -->
                            </div>
                        </div>
                    </div>
                    
                    <!-- Media Tab - Video Metadata Extractor -->
                    <div id="media" class="tab-pane">
                        <div class="media-panel">
                            <h3 class="mb-4">
                                <i class="fas fa-video text-primary"></i>
                                Video Metadata Extractor
                            </h3>
                            
                            <div class="media-input-toggle">
                                <button class="media-toggle-btn active" onclick="toggleMediaInput('url')">
                                    <i class="fas fa-link"></i> URL
                                </button>
                                <button class="media-toggle-btn" onclick="toggleMediaInput('file')">
                                    <i class="fas fa-upload"></i> File Upload
                                </button>
                            </div>
                            
                            <div class="url-input-container active" id="url-input">
                                <label class="block text-sm font-medium mb-2">Video URL:</label>
                                <div class="flex gap-2">
                                    <input type="url" id="video-url" 
                                           class="media-url-input"
                                           placeholder="https://youtube.com/watch?v=... or any video URL">
                                    <button onclick="extractFromURL()" class="glass-btn primary">
                                        <i class="fas fa-download"></i> Extract
                                    </button>
                                </div>
                            </div>
                            
                            <div class="file-input-container" id="file-input">
                                <label class="block text-sm font-medium mb-2">Upload Video File:</label>
                                <div class="file-drop-zone" onclick="document.getElementById('video-file').click()">
                                    <i class="fas fa-cloud-upload-alt text-4xl mb-2"></i>
                                    <p>Click to select or drag and drop video file</p>
                                    <input type="file" id="video-file" accept="video/*" style="display: none;" onchange="extractFromFile(this)">
                                </div>
                            </div>
                            
                            <div id="metadata-result" style="display: none;">
                                <!-- Metadata results will be displayed here -->
                            </div>
                        </div>
                    </div>
                    
                    <!-- Admin Tab -->
                    <div id="admin" class="tab-pane">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-heart-pulse text-success"></i>
                                    System Health
                                </h3>
                                <div class="space-y-4">
                                    <div class="health-item">
                                        <span class="health-label">API Status:</span>
                                        <span class="health-value text-success">Operational</span>
                                    </div>
                                    <div class="health-item">
                                        <span class="health-label">Database:</span>
                                        <span class="health-value text-success">Connected</span>
                                    </div>
                                    <div class="health-item">
                                        <span class="health-label">NLP Engine:</span>
                                        <span class="health-value text-success">Ready</span>
                                    </div>
                                    <div class="health-item">
                                        <span class="health-label">Cache:</span>
                                        <span class="health-value text-success">Active</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-sliders-h text-primary"></i>
                                    Configuration
                                </h3>
                                <div class="space-y-4">
                                    <div class="config-item">
                                        <label class="config-label">Sentiment Threshold:</label>
                                        <input type="range" min="0" max="1" step="0.1" value="0.7" class="config-slider">
                                    </div>
                                    <div class="config-item">
                                        <label class="config-label">Toxicity Alert Level:</label>
                                        <input type="range" min="0" max="1" step="0.1" value="0.8" class="config-slider">
                                    </div>
                                    <div class="config-item">
                                        <label class="config-label">Cache Duration (minutes):</label>
                                        <input type="number" min="1" max="60" value="5" class="config-input">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Enhanced JavaScript with Chart.js Stability -->
        <script>
        // Global chart instances to prevent recreation
        let chartInstances = {{}};
        
        // Chart configuration with stability features
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.responsive = false;  // CRITICAL: Prevent auto-resizing
        Chart.defaults.maintainAspectRatio = false;  // Allow fixed dimensions
        
        // Enhanced Tab Switching with Animation
        function switchTab(tabName, element) {{
            // Remove active from all tabs and buttons
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            
            // Add active to current tab and button
            element.classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            // Load tab-specific content
            switch(tabName) {{
                case 'news':
                    loadNews(1);  // Load page 1 with pagination
                    break;
                case 'media':
                    initializeMediaExtractor();
                    break;
                case 'overview':
                    initializeOverviewCharts();
                    break;
                case 'trends':
                    initializeTrendsCharts();
                    break;
                case 'segments':
                    initializeSegmentsCharts();
                    break;
            }}
        }}
        
        // Initialize Overview Charts with FIXED DIMENSIONS
        function initializeOverviewCharts() {{
            // Sentiment Pie Chart - FIXED SIZE
            if (!chartInstances.sentimentPie) {{
                const ctx = document.getElementById('sentiment-pie-chart');
                if (ctx) {{
                    ctx.width = 400;
                    ctx.height = 300;
                    chartInstances.sentimentPie = new Chart(ctx, {{
                        type: 'doughnut',
                        data: {{
                            labels: ['Positive', 'Negative', 'Neutral'],
                            datasets: [{{
                                data: [{sentiment_data['sentiment_distribution']['positive']:.2f}, 
                                       {sentiment_data['sentiment_distribution']['negative']:.2f}, 
                                       {sentiment_data['sentiment_distribution']['neutral']:.2f}],
                                backgroundColor: ['#10B981', '#EF4444', '#6B7280'],
                                borderWidth: 0
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{
                                    position: 'bottom'
                                }}
                            }}
                        }}
                    }});
                }}
            }}
            
            // Toxicity Gauge - FIXED SIZE
            if (!chartInstances.toxicityGauge) {{
                const ctx = document.getElementById('toxicity-gauge');
                if (ctx) {{
                    ctx.width = 400;
                    ctx.height = 300;
                    const maxToxicity = {max(sentiment_data['toxicity_scores']):.2f};
                    chartInstances.toxicityGauge = new Chart(ctx, {{
                        type: 'doughnut',
                        data: {{
                            datasets: [{{
                                data: [maxToxicity, 1 - maxToxicity],
                                backgroundColor: ['#EF4444', '#E5E7EB'],
                                borderWidth: 0,
                                circumference: 180,
                                rotation: 270
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false,
                            cutout: '70%',
                            plugins: {{
                                legend: {{
                                    display: false
                                }},
                                tooltip: {{
                                    enabled: false
                                }}
                            }}
                        }}
                    }});
                }}
            }}
        }}
        
        // Initialize Trends Charts with FIXED DIMENSIONS
        function initializeTrendsCharts() {{
            // Trends Line Chart - FIXED SIZE
            if (!chartInstances.trendsChart) {{
                const ctx = document.getElementById('trends-chart');
                if (ctx) {{
                    ctx.width = 800;
                    ctx.height = 400;
                    chartInstances.trendsChart = new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: {trend_analysis['hourly_data']['hours']},
                            datasets: [{{
                                label: 'Sentiment Score',
                                data: {trend_analysis['hourly_data']['sentiment_scores']},
                                borderColor: '#3B82F6',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                tension: 0.4,
                                fill: true
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    max: 1
                                }}
                            }}
                        }}
                    }});
                }}
            }}
            
            // Volume Bar Chart - FIXED SIZE
            if (!chartInstances.volumeChart) {{
                const ctx = document.getElementById('volume-chart');
                if (ctx) {{
                    ctx.width = 400;
                    ctx.height = 300;
                    chartInstances.volumeChart = new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: {trend_analysis['hourly_data']['hours']},
                            datasets: [{{
                                label: 'Message Volume',
                                data: {trend_analysis['hourly_data']['volumes']},
                                backgroundColor: '#10B981'
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {{
                                y: {{
                                    beginAtZero: true
                                }}
                            }}
                        }}
                    }});
                }}
            }}
        }}
        
        // Initialize Segments Charts
        function initializeSegmentsCharts() {{
            // Sources Pie Chart
            if (!chartInstances.sourcesChart) {{
                const ctx = document.getElementById('sources-chart');
                if (ctx) {{
                    ctx.width = 400;
                    ctx.height = 300;
                    chartInstances.sourcesChart = new Chart(ctx, {{
                        type: 'pie',
                        data: {{
                            labels: ['Social Media', 'News', 'Forums', 'Reviews'],
                            datasets: [{{
                                data: [45, 25, 20, 10],
                                backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false
                        }}
                    }});
                }}
            }}
            
            // Emotions Radar Chart
            if (!chartInstances.emotionsChart) {{
                const ctx = document.getElementById('emotions-chart');
                if (ctx) {{
                    ctx.width = 600;
                    ctx.height = 400;
                    chartInstances.emotionsChart = new Chart(ctx, {{
                        type: 'radar',
                        data: {{
                            labels: ['Joy', 'Anger', 'Fear', 'Sadness', 'Surprise', 'Disgust'],
                            datasets: [{{
                                label: 'Emotion Intensity',
                                data: {sentiment_data['emotion_scores']},
                                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                                borderColor: '#3B82F6',
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {{
                                r: {{
                                    beginAtZero: true,
                                    max: 1
                                }}
                            }}
                        }}
                    }});
                }}
            }}
        }}
        
        // News Loading with Pagination (NO INFINITE SCROLL!)
        function loadNews(page = 1) {{
            fetch(`/api/news?page=${{page}}&limit=10`)
                .then(response => response.json())
                .then(data => {{
                    const container = document.getElementById('news-container');
                    container.innerHTML = data.items.map(item => `
                        <div class="news-item">
                            <h4>${{item.title}}</h4>
                            <p>${{item.summary}}</p>
                            <div class="news-meta">
                                <span class="sentiment-badge sentiment-${{item.sentiment}}">${{item.sentiment}}</span>
                                <span class="timestamp">${{item.timestamp}}</span>
                            </div>
                        </div>
                    `).join('');
                    
                    // Update pagination
                    updatePagination(page, data.total_pages, 'news');
                }})
                .catch(error => {{
                    console.error('Error loading news:', error);
                    document.getElementById('news-container').innerHTML = '<p class="error">Failed to load news.</p>';
                }});
        }}
        
        // Pagination Helper (REPLACES INFINITE SCROLL)
        function updatePagination(currentPage, totalPages, context) {{
            const container = document.getElementById(`${{context}}-pagination`);
            let paginationHTML = '';
            
            if (totalPages > 1) {{
                paginationHTML = '<div class="pagination">';
                
                // Previous button
                if (currentPage > 1) {{
                    paginationHTML += `<button onclick="loadNews(${{currentPage - 1}})" class="pagination-btn">Previous</button>`;
                }}
                
                // Page numbers
                for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {{
                    const activeClass = i === currentPage ? 'active' : '';
                    paginationHTML += `<button onclick="loadNews(${{i}})" class="pagination-btn ${{activeClass}}">${{i}}</button>`;
                }}
                
                // Next button
                if (currentPage < totalPages) {{
                    paginationHTML += `<button onclick="loadNews(${{currentPage + 1}})" class="pagination-btn">Next</button>`;
                }}
                
                paginationHTML += '</div>';
            }}
            
            container.innerHTML = paginationHTML;
        }}
        
        // Video Metadata Extractor Functions
        function toggleMediaInput(type) {{
            document.querySelectorAll('.media-toggle-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.url-input-container, .file-input-container').forEach(container => container.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(`${{type}}-input`).classList.add('active');
        }}
        
        function extractFromURL() {{
            const url = document.getElementById('video-url').value;
            if (!url) return;
            
            showLoader('Extracting metadata from URL...');
            
            fetch('/api/media/extract-url', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{'url': url}})
            }})
            .then(response => response.json())
            .then(data => {{
                hideLoader();
                displayMetadata(data);
            }})
            .catch(error => {{
                hideLoader();
                showError('Failed to extract metadata: ' + error.message);
            }});
        }}
        
        function extractFromFile(input) {{
            const file = input.files[0];
            if (!file) return;
            
            showLoader('Extracting metadata from file...');
            
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/api/media/extract', {{
                method: 'POST',
                body: formData
            }})
            .then(response => response.json())
            .then(data => {{
                hideLoader();
                displayMetadata(data);
            }})
            .catch(error => {{
                hideLoader();
                showError('Failed to extract metadata: ' + error.message);
            }});
        }}
        
        function displayMetadata(data) {{
            const container = document.getElementById('metadata-result');
            container.style.display = 'block';
            container.innerHTML = `
                <div class="metadata-card">
                    <h4>Video Metadata</h4>
                    <div class="metadata-grid">
                        <div class="metadata-item">
                            <label>Title:</label>
                            <span>${{data.title || 'N/A'}}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Duration:</label>
                            <span>${{data.duration || 'N/A'}}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Format:</label>
                            <span>${{data.format || 'N/A'}}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Size:</label>
                            <span>${{data.size || 'N/A'}}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Resolution:</label>
                            <span>${{data.resolution || 'N/A'}}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Quality:</label>
                            <span>${{data.quality || 'N/A'}}</span>
                        </div>
                    </div>
                </div>
            `;
        }}
        
        // Utility Functions
        function showLoader(message) {{
            // Implementation for loading indicator
            console.log('Loading:', message);
        }}
        
        function hideLoader() {{
            // Implementation for hiding loader
            console.log('Loading complete');
        }}
        
        function showError(message) {{
            alert('Error: ' + message);
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Initialize overview charts by default
            initializeOverviewCharts();
            
            // Load news data for the news tab
            loadNews(1);
            
            // Add resize event listener with debouncing to prevent chart recreation
            let resizeTimeout;
            window.addEventListener('resize', function() {{
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {{
                    // Only update chart scales, don't recreate charts
                    Object.values(chartInstances).forEach(chart => {{
                        if (chart && chart.update) {{
                            chart.update('none'); // Update without animation
                        }}
                    }});
                }}, 250);
            }});
        }});
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_template.format(
        stats=stats,
        sentiment_data=sentiment_data,
        trend_analysis=trend_analysis,
        generate_anomalies_html=generate_anomalies_html
    ))
            <!-- Metrics Grid -->
            <div class="metric-grid stagger-fade-in">
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="metric-value" id="total-analyses">{stats.get('today', {{}}).get('total_analyses', 0)}</div>
                    <div class="metric-label">Today's Analyses</div>
                    <div class="chart-mini">
                        <canvas id="analyses-trend"></canvas>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-smile"></i>
                    </div>
                    <div class="metric-value" id="avg-confidence">{stats.get('today', {{}}).get('avg_confidence', 0.75):.1%}</div>
                    <div class="metric-label">Average Confidence</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {stats.get('today', {{}}).get('avg_confidence', 0.75) * 100}%"></div>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="metric-value" id="data-sources">{stats.get('today', {{}}).get('unique_sources', 4)}</div>
                    <div class="metric-label">Active Data Sources</div>
                    <div class="real-time-badge">
                        <i class="fas fa-check"></i>
                        <span>Active</span>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="metric-value" id="ai-insights">
                        {len(trend_analysis.get('recommendations', []))}
                    </div>
                    <div class="metric-label">AI Insights</div>
                    <div class="chart-mini">
                        <canvas id="sentiment-distribution"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Main Content Tabs -->
            <div class="tab-container" data-animate="fade-up">
                <div class="tab-nav">
                    <button class="tab-btn active" onclick="switchTab('live-analysis', this)">
                        <i class="fas fa-broadcast-tower"></i>
                        Live Analysis
                    </button>
                    <button class="tab-btn" onclick="switchTab('trends', this)">
                        <i class="fas fa-chart-area"></i>
                        Trends & Insights
                    </button>
                    <button class="tab-btn" onclick="switchTab('test-analysis', this)">
                        <i class="fas fa-keyboard"></i>
                        Test Analysis
                    </button>
                    <button class="tab-btn" onclick="switchTab('segments', this)">
                        <i class="fas fa-puzzle-piece"></i>
                        Segments
                    </button>
                    <button class="tab-btn" onclick="switchTab('video-analysis', this)">
                        <i class="fas fa-video"></i>
                        Video Analysis
                    </button>
                </div>
                
                <div class="tab-content">
                    <!-- Live Analysis Tab -->
                    <div id="live-analysis" class="tab-pane active">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-stream text-primary"></i>
                                    Sample Analysis Stream
                                </h3>
                                <div id="live-feed" class="live-feed">
                                    {generate_sample_feed()}
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-pie text-accent"></i>
                                    Sentiment Distribution
                                </h3>
                                <canvas id="sentiment-pie-chart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Trends Tab -->
                    <div id="trends" class="tab-pane">
                        <div class="grid grid-cols-1 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-line text-primary"></i>
                                    24-Hour Sentiment Trends
                                </h3>
                                <canvas id="trends-chart" style="height: 400px;"></canvas>
                            </div>
                            
                            <div class="grid grid-cols-3 gap-4">
                                <div class="glass-card text-center">
                                    <h4>Momentum</h4>
                                    <div class="text-2xl font-bold sentiment-{trend_analysis.get('trend_analysis', {{}}).get('momentum', {{}}).get('direction', 'neutral')}">
                                        {trend_analysis.get('trend_analysis', {{}}).get('momentum', {{}}).get('direction', 'stable').title()}
                                    </div>
                                    <p class="text-sm text-secondary">
                                        {trend_analysis.get('trend_analysis', {{}}).get('momentum', {{}}).get('strength', 'weak').title()} strength
                                    </p>
                                </div>
                                
                                <div class="glass-card text-center">
                                    <h4>Volatility</h4>
                                    <div class="text-2xl font-bold text-warning">
                                        {trend_analysis.get('trend_analysis', {{}}).get('volatility', {{}}).get('risk_level', 'low').title()}
                                    </div>
                                    <p class="text-sm text-secondary">Risk level</p>
                                </div>
                                
                                <div class="glass-card text-center">
                                    <h4>Prediction</h4>
                                    <div class="text-2xl font-bold text-accent">
                                        {trend_analysis.get('trend_analysis', {{}}).get('prediction', {{}}).get('confidence', 0):.1%}
                                    </div>
                                    <p class="text-sm text-secondary">Confidence</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Test Analysis Tab -->
                    <div id="test-analysis" class="tab-pane">
                        <div class="glass-card">
                            <h3 class="mb-4">
                                <i class="fas fa-keyboard text-primary"></i>
                                Test Sentiment Analysis
                            </h3>
                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium mb-2">Enter text to analyze:</label>
                                    <textarea id="test-text" class="w-full p-3 bg-glass border border-glass-border rounded-lg text-white placeholder-gray-400" 
                                              placeholder="Type your text here..." rows="4"></textarea>
                                </div>
                                <button onclick="analyzeText()" class="glass-btn primary">
                                    <i class="fas fa-search"></i>
                                    Analyze Sentiment
                                </button>
                                <div id="analysis-result" class="mt-4"></div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Segments Tab -->
                    <div id="segments" class="tab-pane">
                        <div class="glass-card">
                            <h3 class="mb-4">
                                <i class="fas fa-puzzle-piece text-primary"></i>
                                Keyword Segments
                            </h3>
                            <div id="word-cloud-container" style="height: 400px; width: 100%;">
                                <div id="word-cloud"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Video Analysis Tab -->
                    <div id="video-analysis" class="tab-pane">
                        <div class="glass-card">
                            <h3 class="mb-4">
                                <i class="fas fa-video text-primary"></i>
                                Video Metadata Extractor
                            </h3>
                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium mb-2">Upload a video file:</label>
                                    <input type="file" id="video-file" accept="video/*" class="w-full p-3 bg-glass border border-glass-border rounded-lg text-white">
                                </div>
                                <div id="video-metadata-container" class="video-metadata-container">
                                    <div class="video-metadata-card">
                                        <h3>Video Metadata</h3>
                                        <pre id="video-metadata-output"></pre>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            {ui_generator.generate_javascript_animations()}
            
            // Dashboard-specific JavaScript
            let sentimentChart, trendsChart, pieChart;
            
            // Initialize dashboard
            document.addEventListener('DOMContentLoaded', function() {{
                initializeCharts();
                
                // Animate numbers on load
                setTimeout(() => {{
                    animateMetrics();
                }}, 500);
                
                // Video metadata extraction
                const videoFileInput = document.getElementById('video-file');
                videoFileInput.addEventListener('change', handleVideoFile);

                // Initial word cloud for the default active tab if it's 'segments'
                if (document.querySelector('.tab-btn.active').getAttribute('onclick').includes('segments')) {{
                    initializeWordCloud();
                }}
            }});
            
            // Tab switching functionality
            function switchTab(tabName, element) {{
                // Hide all tab panes
                document.querySelectorAll('.tab-pane').forEach(pane => {{
                    pane.classList.remove('active');
                }});
                
                // Remove active class from all tab buttons
                document.querySelectorAll('.tab-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                
                // Show selected tab pane
                document.getElementById(tabName).classList.add('active');
                
                // Add active class to clicked button
                element.classList.add('active');
                
                // Trigger animations for new content
                const activePane = document.getElementById(tabName);
                activePane.style.opacity = '0';
                setTimeout(() => {{
                    activePane.style.opacity = '1';
                    activePane.style.animation = 'fadeInUp 0.3s ease forwards';
                }}, 50);

                if (tabName === 'segments') {{
                    const wordCloudContainer = document.getElementById('word-cloud');
                    if (wordCloudContainer) {{
                        wordCloudContainer.innerHTML = ''; // Clear previous cloud
                    }}
                    initializeWordCloud();
                }}
            }}
            
            // Initialize charts
            function initializeCharts() {{
                // Sentiment pie chart
                const pieCtx = document.getElementById('sentiment-pie-chart').getContext('2d');
                pieChart = new Chart(pieCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Positive', 'Neutral', 'Negative'],
                        datasets: [{{
                            data: [55, 30, 15],
                            backgroundColor: [
                                'rgba(16, 185, 129, 0.8)',
                                'rgba(107, 114, 128, 0.8)',
                                'rgba(239, 68, 68, 0.8)'
                            ],
                            borderWidth: 0
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    color: '#cbd5e1',
                                    padding: 20
                                }}
                            }}
                        }}
                    }}
                }});
                
                // Trends chart
                const trendsCtx = document.getElementById('trends-chart').getContext('2d');
                trendsChart = new Chart(trendsCtx, {{
                    type: 'line',
                    data: {{
                        labels: Array.from({{length: 24}}, (_, i) => `${{i}}:00`),
                        datasets: [{{
                            label: 'Sentiment Score',
                            data: {json.dumps(trend_analysis.get('hourly_trends', {{}}).get('avg_sentiment', [0]*24))},
                            borderColor: 'rgba(99, 102, 241, 1)',
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            tension: 0.4,
                            fill: true
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                grid: {{
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }},
                                ticks: {{
                                    color: '#cbd5e1'
                                }}
                            }},
                            x: {{
                                grid: {{
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }},
                                ticks: {{
                                    color: '#cbd5e1'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                labels: {{
                                    color: '#cbd5e1'
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Word Cloud
            function initializeWordCloud() {{
                const container = document.getElementById('word-cloud-container');
                if (!container) return;
                const width = container.offsetWidth;
                const height = container.offsetHeight;

                fetch('/api/word-cloud')
                    .then(response => response.json())
                    .then(words => {{
                        if (!words || words.length === 0) return;
                        const layout = d3.layout.cloud()
                            .size([width, height])
                            .words(words.map(d => ({{text: d.text, size: d.size}})))
                            .padding(5)
                            .rotate(() => (~~(Math.random() * 2) * 90)) // 0 or 90 degrees
                            .font("Inter")
                            .fontSize(d => d.size)
                            .on("end", draw);

                        layout.start();

                        function draw(words) {{
                            d3.select("#word-cloud").html(""); // Clear previous
                            d3.select("#word-cloud").append("svg")
                                .attr("width", layout.size()[0])
                                .attr("height", layout.size()[1])
                                .append("g")
                                .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                                .selectAll("text")
                                .data(words)
                                .enter().append("text")
                                .style("font-size", d => d.size + "px")
                                .style("font-family", "Inter")
                                .style("fill", (d, i) => d3.schemeCategory10[i % 10])
                                .attr("text-anchor", "middle")
                                .attr("transform", d => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")")
                                .text(d => d.text);
                        }}
                    }});
            }}
            
            // Animate metrics on load
            function animateMetrics() {{
                const metrics = document.querySelectorAll('.metric-value');
                metrics.forEach((metric, index) => {{
                    setTimeout(() => {{
                        metric.style.animation = 'bounce 0.6s ease';
                    }}, index * 200);
                }});
            }}
            
            // Analyze text function
            async function analyzeText() {{
                const textInput = document.getElementById('test-text');
                const resultDiv = document.getElementById('analysis-result');
                const text = textInput.value.trim();
                
                if (!text) {{
                    resultDiv.innerHTML = '<div class="notification error">Please enter some text to analyze.</div>';
                    return;
                }}
                
                resultDiv.innerHTML = '<div class="loading-spinner"></div>';
                
                try {{
                    const response = await fetch('/api/analyze', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify({{ text: text, source: 'user_input' }})
                    }});
                    
                    const result = await response.json();
                    
                    if (result.error) {{
                        resultDiv.innerHTML = `<div class="notification error">Error: ${{result.error}}</div>`;
                    }} else {{
                        const analysis = result.analysis;
                        resultDiv.innerHTML = `
                            <div class="glass-card">
                                <h4 class="mb-3">Analysis Results</h4>
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <label class="text-sm font-medium">Sentiment:</label>
                                        <div class="text-lg font-bold sentiment-${{analysis.sentiment}}">
                                            ${{analysis.sentiment.charAt(0).toUpperCase() + analysis.sentiment.slice(1)}}
                                        </div>
                                    </div>
                                    <div>
                                        <label class="text-sm font-medium">Confidence:</label>
                                        <div class="text-lg font-bold text-accent">
                                            ${{(analysis.confidence * 100).toFixed(1)}}%
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-4">
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${{analysis.confidence * 100}}%"></div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }}
                }} catch (error) {{
                    resultDiv.innerHTML = `<div class="notification error">Error: ${{error.message}}</div>`;
                }}
            }}
            
            // Video metadata extraction
            function handleVideoFile(event) {{
                const file = event.target.files[0];
                if (!file) {{
                    return;
                }}
                
                const metadataContainer = document.getElementById('video-metadata-container');
                const metadataOutput = document.getElementById('video-metadata-output');
                
                metadataContainer.style.display = 'block';
                metadataOutput.textContent = 'Analyzing video...';
                
                const mediaInfo = MediaInfo({{ format: 'JSON' }}, (mediainfo) => {{
                    const getSize = () => file.size;
                    const readChunk = (chunkSize, offset) =>
                        new Promise((resolve, reject) => {{
                            const reader = new FileReader();
                            reader.onload = (event) => {{
                                if (event.target.error) {{
                                    reject(event.target.error);
                                }}
                                resolve(new Uint8Array(event.target.result));
                            }};
                            reader.readAsArrayBuffer(file.slice(offset, offset + chunkSize));
                        }});
                    
                    mediainfo
                        .analyzeData(getSize, readChunk)
                        .then((result) => {{
                            metadataOutput.textContent = JSON.stringify(result, null, 2);
                        }})
                        .catch((error) => {{
                            metadataOutput.textContent = `Error analyzing file: \n${{error.stack}}`;
                        }});
                }});
            }}
            
            // Initialize particles background
            particlesJS('particles-js', {{
                particles: {{
                    number: {{ value: 50 }},
                    color: {{ value: '#6366f1' }},
                    shape: {{ type: 'circle' }},
                    opacity: {{ value: 0.3 }},
                    size: {{ value: 3 }},
                    move: {{
                        enable: true,
                        speed: 1,
                        direction: 'none',
                        random: true,
                        out_mode: 'out'
                    }}
                }},
                interactivity: {{
                    detect_on: 'canvas',
                    events: {{
                        onhover: {{ enable: true, mode: 'repulse' }},
                        onclick: {{ enable: true, mode: 'push' }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

def generate_sample_feed():
    """Generate sample feed items for display"""
    feed_html = ""
    for analysis in SAMPLE_ANALYSES:
        feed_html += f"""
        <div class="feed-item animate-fade-in-left">
            <div class="flex items-start gap-3">
                <div class="sentiment-indicator sentiment-{analysis['sentiment']}">
                    <i class="fas fa-{get_sentiment_icon(analysis['sentiment'])}"></i>
                </div>
                <div class="flex-1">
                    <p class="font-medium text-sm mb-1">{analysis['content']}</p>
                    <div class="flex justify-between items-center text-xs text-secondary">
                        <span class="sentiment-{analysis['sentiment']}">{analysis['sentiment']} ({analysis['confidence']:.1%})</span>
                        <span>{analysis['source']}</span>
                    </div>
                </div>
            </div>
        </div>
        """
    return feed_html

def get_sentiment_icon(sentiment):
    """Get appropriate icon for sentiment"""
    icons = {
        'positive': 'smile',
        'negative': 'frown',
        'neutral': 'meh'
    }
    return icons.get(sentiment, 'meh')

@app.route('/api/analyze', methods=['POST'])
def analyze_text_route():
    """Analyze text sentiment with enhanced features"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        source = data.get('source', 'user_input')
        
        if not text:
            return jsonify({{'error': 'No text provided'}}), 400
        
        # Perform sentiment analysis
        analysis = sentiment_analyzer.analyze_sentiment(text)
        
        # Store in database
        analysis_id = db_manager.store_analysis_result(
            content=text,
            sentiment=analysis['sentiment'],
            confidence=analysis['confidence'],
            source=source,
            metadata=data.get('metadata', {{}})
        )
        
        return jsonify({{
            'id': analysis_id,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }})
        
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get comprehensive statistics"""
    try:
        hours = request.args.get('hours', 24, type=int)
        stats = db_manager.get_sentiment_statistics(hours=hours)
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({{
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': Config.APP_VERSION,
                'environment': Config.ENVIRONMENT
    })

@app.route('/api/news')
def get_news():
    """Get paginated news with sentiment analysis"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Sample news data - replace with actual news fetching
        sample_news = [
            {
                'title': 'Breaking: AI Breakthrough in Sentiment Analysis',
                'summary': 'Researchers achieve 99% accuracy in real-time emotion detection...',
                'sentiment': 'positive',
                'timestamp': '2024-01-15 14:30:00',
                'url': 'https://example.com/news/1'
            },
            {
                'title': 'Market Update: Tech Stocks Show Mixed Signals',
                'summary': 'Technology sector experiences volatility amid regulatory concerns...',
                'sentiment': 'neutral',
                'timestamp': '2024-01-15 13:45:00',
                'url': 'https://example.com/news/2'
            },
            {
                'title': 'Study: Social Media Impact on Mental Health',
                'summary': 'New research reveals concerning trends in digital wellness...',
                'sentiment': 'negative',
                'timestamp': '2024-01-15 12:20:00',
                'url': 'https://example.com/news/3'
            }
        ] * 10  # Simulate more news items
        
        # Calculate pagination
        total_items = len(sample_news)
        total_pages = math.ceil(total_items / limit)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_news = sample_news[start_idx:end_idx]
        
        return jsonify({
            'items': paginated_news,
            'page': page,
            'limit': limit,
            'total_items': total_items,
            'total_pages': total_pages
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/extract-url', methods=['POST'])
def extract_metadata_from_url():
    """Extract video metadata from URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Use the enhanced video metadata extractor
        metadata = extract_video_metadata(url)
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/extract', methods=['POST'])
def extract_metadata_from_file():
    """Extract video metadata from uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            
            # Extract metadata from file
            metadata = extract_video_metadata(tmp_file.name)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    }})

@app.route('/api/word-cloud')
def get_word_cloud_data():
    """Get data for word cloud visualization"""
    try:
        # In a real application, this would be derived from recent analysis
        words = [
            {{"text": "AI", "size": 40}}, {{"text": "Python", "size": 30}},
            {{"text": "Data", "size": 25}}, {{"text": "Sentiment", "size": 35}},
            {{"text": "Flask", "size": 20}}, {{"text": "JavaScript", "size": 28}},
            {{"text": "Cloud", "size": 18}}, {{"text": "API", "size": 22}},
            {{"text": "Real-time", "size": 26}}, {{"text": "Dashboard", "size": 32}},
            {{"text": "Analytics", "size": 29}}, {{"text": "Machine Learning", "size": 24}}
        ]
        return jsonify(words)
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5003)))
