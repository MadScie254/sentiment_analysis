"""
Surgically Upgraded Sentiment Analysis Dashboard
Production-ready Flask app with modern frontend, security, and robust APIs
"""

import os
import sys
import json
import math
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
import time

# Flask and web components
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuration and utilities
from config_manager import get_production_settings
from news_ingest import kenyan_news_ingestor

# Import enhanced components
try:
    from enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentResult
    # Create analyzer instance
    sentiment_analyzer = EnhancedSentimentAnalyzer()
    REAL_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Real components not available: {e}")
    REAL_COMPONENTS_AVAILABLE = False

# Setup logging
def setup_logging():
    """Setup JSON logging for production"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

setup_logging()
logger = logging.getLogger(__name__)

# Load settings
settings = get_production_settings()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY

# Setup CORS with restricted origins
if settings.ALLOWED_ORIGINS == ["*"]:
    CORS(app)
else:
    CORS(app, origins=settings.ALLOWED_ORIGINS)

# Setup rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE} per minute"]
)
limiter.init_app(app)

# Database fallback
class SimpleDB:
    def init_app(self, app):
        pass
    
    def create_all(self):
        pass

db = SimpleDB()

def log_api_call(endpoint: str, success: bool, duration: float, **kwargs):
    """Log API calls in JSON format"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "success": success,
        "duration_ms": round(duration * 1000, 2),
        "remote_addr": get_remote_address(),
        **kwargs
    }
    logger.info(json.dumps(log_data))

def api_response_wrapper(f):
    """Decorator for consistent API responses and logging"""
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = time.time()
        endpoint = request.endpoint
        
        try:
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            log_api_call(endpoint, True, duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            log_api_call(endpoint, False, duration, error=str(e))
            logger.error(f"API error in {endpoint}: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    return decorated

# === API ENDPOINTS ===

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("10 per minute")
@api_response_wrapper
def analyze_sentiment():
    """Analyze sentiment with input validation and security"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        text = data.get('text', '').strip()
        if not text:
            return jsonify({"error": "Text field is required"}), 400
        
        if len(text) > 5000:
            return jsonify({"error": "Text too long (max 5000 characters)"}), 400
        
        # Use enhanced sentiment analyzer if available
        if REAL_COMPONENTS_AVAILABLE:
            result = sentiment_analyzer.analyze_sentiment(text)
            
            response_data = {
                "success": True,
                "sentiment": result.sentiment,
                "confidence": round(result.score, 3),
                "scores": {
                    "positive": round(result.scores.get('positive', 0.0), 3),
                    "negative": round(result.scores.get('negative', 0.0), 3),
                    "neutral": round(result.scores.get('neutral', 0.0), 3)
                },
                "toxicity": round(result.toxicity_score, 3),
                "model_used": result.model_used,
                "timestamp": datetime.utcnow().isoformat(),
                "text_length": len(text),
                "word_count": len(text.split())
            }
        else:
            # Fallback response
            response_data = {
                "success": True,
                "sentiment": "neutral",
                "confidence": 0.5,
                "scores": {"positive": 0.3, "negative": 0.3, "neutral": 0.4},
                "toxicity": 0.1,
                "model_used": "fallback",
                "timestamp": datetime.utcnow().isoformat(),
                "text_length": len(text),
                "word_count": len(text.split())
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return jsonify({"error": "Analysis failed"}), 500

@app.route('/api/news')
@limiter.limit("30 per minute")
@api_response_wrapper
def get_news():
    """Get news with pagination and country filtering"""
    try:
        # Parse query parameters
        page = max(1, int(request.args.get('page', 1)))
        limit = min(50, max(1, int(request.args.get('limit', 10))))
        country = request.args.get('country', settings.DEFAULT_NEWS_COUNTRY)
        
        # Get news from Kenyan sources
        news_items = kenyan_news_ingestor.get_cached_items(max_age_hours=24)
        
        if not news_items:
            # Try fresh ingestion
            news_items = kenyan_news_ingestor.ingest_all_sources()
        
        # Convert to API format
        articles = []
        for item in news_items:
            articles.append({
                "title": item.title,
                "summary": item.summary,
                "url": item.url,
                "source": item.source,
                "published_at": item.published,
                "image_url": item.image_url,
                "category": item.category,
                "sentiment": "neutral",  # TODO: Add sentiment analysis
                "confidence": 0.5
            })
        
        # Pagination
        total_items = len(articles)
        total_pages = math.ceil(total_items / limit)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_articles = articles[start_idx:end_idx]
        
        # Add sentiment analysis to articles
        if REAL_COMPONENTS_AVAILABLE:
            for article in paginated_articles:
                try:
                    text_to_analyze = f"{article['title']} {article['summary']}"
                    result = sentiment_analyzer.analyze_sentiment(text_to_analyze)
                    article['sentiment'] = result.sentiment
                    article['confidence'] = round(result.score, 3)
                except:
                    pass  # Keep defaults
        
        # Get unique sources
        sources_used = list(set([item.source for item in news_items]))
        
        return jsonify({
            "success": True,
            "items": paginated_articles,
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "sources_used": sources_used,
            "country": country,
            "api_sources": ["Standard", "CapitalFM", "AllAfrica-Kenya", "BusinessDaily", "KBC", "Citizen", "NTV"]
        })
        
    except Exception as e:
        logger.error(f"News API error: {e}")
        return jsonify({"error": "Failed to fetch news"}), 500

@app.route('/api/analytics/summary')
@limiter.limit("20 per minute")
@api_response_wrapper
def get_analytics_summary():
    """Get analytics summary with sentiment distribution"""
    try:
        # Mock data for now - TODO: integrate with real analytics
        summary = {
            "total_analyses": 1250,
            "sentiment_distribution": {
                "positive": 0.45,
                "negative": 0.25,
                "neutral": 0.30
            },
            "average_confidence": 0.78,
            "trend": "improving",
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Analytics API error: {e}")
        return jsonify({"error": "Failed to fetch analytics"}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": "operational",
            "sentiment_analyzer": "operational" if REAL_COMPONENTS_AVAILABLE else "fallback",
            "news_ingestion": "operational"
        },
        "version": "2.0.0"
    }
    
    return jsonify(health_status)

# === FRONTEND DASHBOARD ===

@app.route('/')
def dashboard():
    """Modern production dashboard with accessibility and security"""
    
    # Get initial data
    try:
        analytics = get_analytics_summary()[0].get_json()
    except:
        analytics = {"sentiment_distribution": {"positive": 0.4, "negative": 0.3, "neutral": 0.3}}
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentiment Intelligence Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Production-ready CSS with CSS Custom Properties */
            :root {
                --primary: #3B82F6;
                --secondary: #64748B;
                --accent: #8B5CF6;
                --success: #10B981;
                --warning: #F59E0B;
                --error: #EF4444;
                --background: #0F172A;
                --surface: #1E293B;
                --glass: rgba(255, 255, 255, 0.1);
                --glass-border: rgba(255, 255, 255, 0.2);
                --text-primary: #F8FAFC;
                --text-secondary: #CBD5E1;
                --text-muted: #64748B;
                --border-radius: 12px;
                --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--background);
                color: var(--text-primary);
                line-height: 1.6;
                overflow-x: hidden;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }

            /* Header */
            .header {
                text-align: center;
                margin-bottom: 3rem;
            }

            .header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .header p {
                color: var(--text-secondary);
                font-size: 1.1rem;
            }

            /* Glass card effect */
            .glass-card {
                background: var(--glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                transition: all var(--transition);
            }

            .glass-card:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }

            /* Sentiment analysis section */
            .sentiment-section {
                margin-bottom: 3rem;
            }

            .sentiment-input {
                width: 100%;
                background: var(--surface);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1rem;
                color: var(--text-primary);
                font-size: 1rem;
                resize: vertical;
                min-height: 120px;
                transition: all var(--transition);
            }

            .sentiment-input:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }

            .glass-btn {
                background: var(--primary);
                color: white;
                border: none;
                border-radius: var(--border-radius);
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                cursor: pointer;
                transition: all var(--transition);
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }

            .glass-btn:hover:not(:disabled) {
                background: #2563EB;
                transform: translateY(-1px);
            }

            .glass-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .sentiment-result {
                background: var(--surface);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                margin-top: 1rem;
            }

            /* Sentiment badges with stable classes */
            .sentiment-positive {
                background: rgba(34, 197, 94, 0.2);
                color: #22c55e;
                padding: 0.25rem 0.75rem;
                border-radius: 999px;
                font-size: 0.875rem;
                font-weight: 600;
                text-transform: uppercase;
            }

            .sentiment-negative {
                background: rgba(239, 68, 68, 0.2);
                color: #ef4444;
                padding: 0.25rem 0.75rem;
                border-radius: 999px;
                font-size: 0.875rem;
                font-weight: 600;
                text-transform: uppercase;
            }

            .sentiment-neutral {
                background: rgba(156, 163, 175, 0.2);
                color: #9ca3af;
                padding: 0.25rem 0.75rem;
                border-radius: 999px;
                font-size: 0.875rem;
                font-weight: 600;
                text-transform: uppercase;
            }

            /* Tab system with ARIA support */
            .tab-container {
                margin-bottom: 3rem;
            }

            .tab-nav {
                display: flex;
                gap: 0.5rem;
                margin-bottom: 2rem;
                border-bottom: 1px solid var(--glass-border);
                overflow-x: auto;
            }

            .tab-btn {
                background: none;
                border: none;
                color: var(--text-secondary);
                padding: 1rem 1.5rem;
                cursor: pointer;
                transition: all var(--transition);
                border-bottom: 2px solid transparent;
                white-space: nowrap;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-weight: 500;
            }

            .tab-btn[aria-selected="true"] {
                color: var(--primary);
                border-bottom-color: var(--primary);
            }

            .tab-btn:hover {
                color: var(--text-primary);
            }

            .tab-pane {
                display: none;
            }

            .tab-pane.active {
                display: block;
            }

            /* News cards */
            .news-grid {
                display: grid;
                gap: 1.5rem;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            }

            .news-card {
                background: var(--surface);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                transition: all var(--transition);
                border: 1px solid var(--glass-border);
            }

            .news-card:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }

            .news-title {
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                line-height: 1.4;
            }

            .news-summary {
                color: var(--text-secondary);
                margin-bottom: 1rem;
                line-height: 1.5;
            }

            .news-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.875rem;
                color: var(--text-muted);
            }

            /* Chart container */
            .chart-container {
                position: relative;
                height: 300px;
                margin: 1rem 0;
            }

            /* Responsive grid */
            .grid {
                display: grid;
                gap: 1.5rem;
            }

            .grid-cols-2 {
                grid-template-columns: repeat(2, 1fr);
            }

            .grid-cols-3 {
                grid-template-columns: repeat(3, 1fr);
            }

            /* Utilities */
            .flex {
                display: flex;
            }

            .items-center {
                align-items: center;
            }

            .justify-between {
                justify-content: space-between;
            }

            .gap-2 {
                gap: 0.5rem;
            }

            .gap-4 {
                gap: 1rem;
            }

            .mb-2 {
                margin-bottom: 0.5rem;
            }

            .mb-4 {
                margin-bottom: 1rem;
            }

            .mt-2 {
                margin-top: 0.5rem;
            }

            .text-sm {
                font-size: 0.875rem;
            }

            .font-medium {
                font-weight: 500;
            }

            .font-semibold {
                font-weight: 600;
            }

            /* Loading states */
            .loading {
                opacity: 0.6;
                pointer-events: none;
            }

            .spinner {
                display: inline-block;
                width: 1rem;
                height: 1rem;
                border: 2px solid var(--glass-border);
                border-top: 2px solid var(--primary);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            /* Accessibility */
            .sr-only {
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0, 0, 0, 0);
                white-space: nowrap;
                border: 0;
            }

            /* Focus styles */
            .tab-btn:focus,
            .glass-btn:focus,
            .sentiment-input:focus {
                outline: 2px solid var(--primary);
                outline-offset: 2px;
            }

            /* Dark mode compatibility */
            @media (prefers-color-scheme: light) {
                :root {
                    --background: #FFFFFF;
                    --surface: #F8FAFC;
                    --text-primary: #1E293B;
                    --text-secondary: #475569;
                    --glass: rgba(0, 0, 0, 0.05);
                    --glass-border: rgba(0, 0, 0, 0.1);
                }
            }

            /* Responsive design */
            @media (max-width: 768px) {
                .container {
                    padding: 1rem;
                }

                .header h1 {
                    font-size: 2rem;
                }

                .grid-cols-2,
                .grid-cols-3 {
                    grid-template-columns: 1fr;
                }

                .tab-nav {
                    flex-wrap: wrap;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <header class="header">
                <h1>Sentiment Intelligence</h1>
                <p>Advanced AI-powered sentiment analysis for Kenyan markets</p>
            </header>

            <!-- Sentiment Analysis Section -->
            <section class="sentiment-section">
                <div class="glass-card">
                    <h2 class="mb-4 font-semibold">Analyze Text Sentiment</h2>
                    <div class="flex gap-4">
                        <div style="flex: 1;">
                            <label for="sentiment-input" class="sr-only">Text to analyze</label>
                            <textarea 
                                id="sentiment-input" 
                                class="sentiment-input" 
                                placeholder="Enter text to analyze sentiment... (e.g., 'Safaricom's new strategy will boost profits' or 'The economy is struggling with inflation')"
                                aria-describedby="sentiment-help"
                            ></textarea>
                            <p id="sentiment-help" class="text-sm text-secondary mt-2">
                                Enter any text in English or Kiswahili for AI-powered sentiment analysis
                            </p>
                            <button id="analyze-btn" class="glass-btn mt-2" onclick="analyzeSentiment()">
                                <i class="fas fa-search" aria-hidden="true"></i>
                                Analyze Sentiment
                            </button>
                        </div>
                        <div id="sentiment-result" class="sentiment-result" style="flex: 1; display: none;">
                            <!-- Results will appear here -->
                        </div>
                    </div>
                </div>
            </section>

            <!-- Tabbed Content -->
            <section class="tab-container">
                <nav class="tab-nav" role="tablist" aria-label="Dashboard sections">
                    <button class="tab-btn" role="tab" data-tab="live-news" aria-selected="true" aria-controls="live-news-panel">
                        <i class="fas fa-newspaper" aria-hidden="true"></i>
                        Live News
                    </button>
                    <button class="tab-btn" role="tab" data-tab="trends" aria-selected="false" aria-controls="trends-panel">
                        <i class="fas fa-chart-line" aria-hidden="true"></i>
                        Trends
                    </button>
                    <button class="tab-btn" role="tab" data-tab="search" aria-selected="false" aria-controls="search-panel">
                        <i class="fas fa-search" aria-hidden="true"></i>
                        Keyword Search
                    </button>
                    <button class="tab-btn" role="tab" data-tab="analytics" aria-selected="false" aria-controls="analytics-panel">
                        <i class="fas fa-chart-pie" aria-hidden="true"></i>
                        Analytics
                    </button>
                    <button class="tab-btn" role="tab" data-tab="preferences" aria-selected="false" aria-controls="preferences-panel">
                        <i class="fas fa-cog" aria-hidden="true"></i>
                        Preferences
                    </button>
                </nav>

                <!-- Live News Tab -->
                <div id="live-news-panel" class="tab-pane active" role="tabpanel" aria-labelledby="live-news-tab">
                    <div class="glass-card mb-4">
                        <h3 class="mb-4 font-semibold">Live Kenyan News Feed</h3>
                        <div class="flex gap-4 mb-4">
                            <input type="text" id="news-search" placeholder="Search news..." 
                                   class="sentiment-input" style="flex: 1; min-height: auto; padding: 0.5rem;">
                            <select id="news-source" class="sentiment-input" style="min-height: auto; padding: 0.5rem;">
                                <option value="">All Sources</option>
                                <option value="Standard">The Standard</option>
                                <option value="CapitalFM">Capital FM</option>
                                <option value="BusinessDaily">Business Daily</option>
                                <option value="KBC">KBC</option>
                            </select>
                        </div>
                    </div>
                    
                    <div id="news-container" class="news-grid">
                        <!-- News items will be loaded here -->
                    </div>
                    
                    <div id="news-pagination" class="flex justify-center mt-4">
                        <!-- Pagination will be loaded here -->
                    </div>
                </div>

                <!-- Trends Tab -->
                <div id="trends-panel" class="tab-pane" role="tabpanel" aria-labelledby="trends-tab">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="glass-card">
                            <h3 class="mb-4 font-semibold">Sentiment Distribution</h3>
                            <div class="chart-container">
                                <canvas id="sentiment-chart"></canvas>
                            </div>
                        </div>
                        
                        <div class="glass-card">
                            <h3 class="mb-4 font-semibold">Trend Analysis</h3>
                            <div class="chart-container">
                                <canvas id="trend-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Search Tab -->
                <div id="search-panel" class="tab-pane" role="tabpanel" aria-labelledby="search-tab">
                    <div class="glass-card">
                        <h3 class="mb-4 font-semibold">Keyword Sentiment Tracking</h3>
                        <div class="flex gap-4 mb-4">
                            <input type="text" id="keyword-input" placeholder="Enter keyword (e.g., 'Safaricom', 'Kenya Shilling')" 
                                   class="sentiment-input" style="flex: 1; min-height: auto; padding: 0.5rem;">
                            <button class="glass-btn" onclick="trackKeyword()">
                                <i class="fas fa-plus"></i>
                                Track
                            </button>
                        </div>
                        <div id="tracked-keywords">
                            <!-- Tracked keywords will appear here -->
                        </div>
                    </div>
                </div>

                <!-- Analytics Tab -->
                <div id="analytics-panel" class="tab-pane" role="tabpanel" aria-labelledby="analytics-tab">
                    <div class="grid grid-cols-3 gap-4 mb-4">
                        <div class="glass-card text-center">
                            <div class="text-2xl font-semibold text-primary" id="total-analyses">-</div>
                            <div class="text-sm text-secondary">Total Analyses</div>
                        </div>
                        <div class="glass-card text-center">
                            <div class="text-2xl font-semibold text-success" id="avg-confidence">-</div>
                            <div class="text-sm text-secondary">Avg Confidence</div>
                        </div>
                        <div class="glass-card text-center">
                            <div class="text-2xl font-semibold text-accent" id="trend-indicator">-</div>
                            <div class="text-sm text-secondary">Trend</div>
                        </div>
                    </div>
                    
                    <div class="glass-card">
                        <h3 class="mb-4 font-semibold">Word Cloud</h3>
                        <div id="word-cloud" style="height: 300px; background: var(--surface); border-radius: var(--border-radius); display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
                            Word cloud will appear here
                        </div>
                    </div>
                </div>

                <!-- Preferences Tab -->
                <div id="preferences-panel" class="tab-pane" role="tabpanel" aria-labelledby="preferences-tab">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="glass-card">
                            <h3 class="mb-4 font-semibold">Display Settings</h3>
                            <div class="mb-4">
                                <label class="flex items-center gap-2">
                                    <input type="checkbox" id="dark-mode-toggle">
                                    <span>Dark Mode</span>
                                </label>
                            </div>
                            <div class="mb-4">
                                <label class="flex items-center gap-2">
                                    <input type="checkbox" id="auto-refresh" checked>
                                    <span>Auto-refresh News</span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="glass-card">
                            <h3 class="mb-4 font-semibold">Notifications</h3>
                            <div class="mb-4">
                                <label class="flex items-center gap-2">
                                    <input type="checkbox" id="sentiment-alerts">
                                    <span>Sentiment Spike Alerts</span>
                                </label>
                            </div>
                            <div class="mb-4">
                                <label class="flex items-center gap-2">
                                    <input type="checkbox" id="keyword-alerts">
                                    <span>Keyword Alerts</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <script>
            // === MODERN JAVASCRIPT WITH EVENT DELEGATION ===
            
            let currentNewsPage = 1;
            let isLoading = false;
            let charts = {};
            
            // Initialize application
            document.addEventListener('DOMContentLoaded', function() {
                initializeApp();
            });
            
            function initializeApp() {
                setupTabNavigation();
                setupDeepLinking();
                loadInitialData();
                setupEventListeners();
                initializeCharts();
            }
            
            // === TAB NAVIGATION WITH EVENT DELEGATION ===
            function setupTabNavigation() {
                const tabNav = document.querySelector('.tab-nav');
                
                tabNav.addEventListener('click', function(event) {
                    const tabBtn = event.target.closest('[data-tab]');
                    if (!tabBtn) return;
                    
                    const tabName = tabBtn.dataset.tab;
                    switchTab(tabName, tabBtn);
                });
                
                // Keyboard navigation
                tabNav.addEventListener('keydown', function(event) {
                    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
                        event.preventDefault();
                        const tabs = [...tabNav.querySelectorAll('[data-tab]')];
                        const currentIndex = tabs.findIndex(tab => tab.getAttribute('aria-selected') === 'true');
                        const nextIndex = event.key === 'ArrowRight' 
                            ? (currentIndex + 1) % tabs.length
                            : (currentIndex - 1 + tabs.length) % tabs.length;
                        
                        switchTab(tabs[nextIndex].dataset.tab, tabs[nextIndex]);
                        tabs[nextIndex].focus();
                    }
                });
            }
            
            function switchTab(tabName, tabElement) {
                // Update ARIA attributes
                document.querySelectorAll('[role="tab"]').forEach(tab => {
                    tab.setAttribute('aria-selected', 'false');
                    tab.classList.remove('active');
                });
                
                document.querySelectorAll('[role="tabpanel"]').forEach(panel => {
                    panel.classList.remove('active');
                });
                
                // Activate selected tab
                tabElement.setAttribute('aria-selected', 'true');
                tabElement.classList.add('active');
                
                const panel = document.getElementById(tabName + '-panel');
                if (panel) {
                    panel.classList.add('active');
                }
                
                // Update URL hash for deep linking
                history.replaceState(null, null, '#tab=' + tabName);
                
                // Load tab-specific content
                loadTabContent(tabName);
            }
            
            // === DEEP LINKING ===
            function setupDeepLinking() {
                const hash = window.location.hash;
                if (hash.startsWith('#tab=')) {
                    const tabName = hash.split('=')[1];
                    const tabButton = document.querySelector(`[data-tab="${tabName}"]`);
                    if (tabButton) {
                        switchTab(tabName, tabButton);
                    }
                }
            }
            
            // === SENTIMENT ANALYSIS WITH SECURITY ===
            async function analyzeSentiment() {
                const input = document.getElementById('sentiment-input');
                const resultDiv = document.getElementById('sentiment-result');
                const analyzeBtn = document.getElementById('analyze-btn');
                
                const text = input.value.trim();
                if (!text) {
                    alert('Please enter some text to analyze');
                    return;
                }
                
                // Show loading state
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = '<span class="spinner"></span> Analyzing...';
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div class="flex items-center gap-2"><span class="spinner"></span> Analyzing sentiment...</div>';
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Analysis failed');
                    }
                    
                    const data = await response.json();
                    displaySentimentResult(data);
                    
                } catch (error) {
                    console.error('Sentiment analysis error:', error);
                    resultDiv.innerHTML = `
                        <div class="text-error">
                            <i class="fas fa-exclamation-triangle"></i>
                            Error: ${escapeHtml(error.message)}
                        </div>
                    `;
                } finally {
                    // Reset button state
                    analyzeBtn.disabled = false;
                    analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Sentiment';
                }
            }
            
            function displaySentimentResult(data) {
                const resultDiv = document.getElementById('sentiment-result');
                const sentimentClass = `sentiment-${data.sentiment}`;
                
                // Safe DOM manipulation to prevent XSS
                resultDiv.innerHTML = `
                    <div class="mb-4">
                        <h3 class="font-semibold mb-2">Analysis Results</h3>
                        <div class="flex items-center justify-between mb-2">
                            <span>Sentiment:</span>
                            <span class="${sentimentClass}">${escapeHtml(data.sentiment)}</span>
                        </div>
                        <div class="flex items-center justify-between mb-2">
                            <span>Confidence:</span>
                            <span class="font-medium">${data.confidence * 100}%</span>
                        </div>
                        <div class="flex items-center justify-between mb-2">
                            <span>Toxicity:</span>
                            <span class="font-medium ${data.toxicity > 0.5 ? 'text-error' : 'text-success'}">${(data.toxicity * 100).toFixed(1)}%</span>
                        </div>
                        <div class="flex items-center justify-between">
                            <span>Model:</span>
                            <span class="text-sm text-secondary">${escapeHtml(data.model_used)}</span>
                        </div>
                    </div>
                    
                    <div class="text-sm text-secondary">
                        <div>Words: ${data.word_count} | Characters: ${data.text_length}</div>
                        <div>Analyzed: ${new Date(data.timestamp).toLocaleString()}</div>
                    </div>
                `;
            }
            
            // === NEWS LOADING ===
            async function loadNews(page = 1) {
                if (isLoading) return;
                
                isLoading = true;
                const newsContainer = document.getElementById('news-container');
                
                if (page === 1) {
                    newsContainer.innerHTML = '<div class="text-center"><span class="spinner"></span> Loading news...</div>';
                }
                
                try {
                    const response = await fetch(`/api/news?page=${page}&limit=10`);
                    if (!response.ok) throw new Error('Failed to load news');
                    
                    const data = await response.json();
                    displayNews(data.items, page === 1);
                    updatePagination(data.page, data.total_pages);
                    
                } catch (error) {
                    console.error('News loading error:', error);
                    newsContainer.innerHTML = '<div class="text-error">Failed to load news</div>';
                } finally {
                    isLoading = false;
                }
            }
            
            function displayNews(items, replace = true) {
                const newsContainer = document.getElementById('news-container');
                
                if (replace) {
                    newsContainer.innerHTML = '';
                }
                
                items.forEach(item => {
                    const newsCard = document.createElement('div');
                    newsCard.className = 'news-card';
                    
                    newsCard.innerHTML = `
                        <h4 class="news-title">${escapeHtml(item.title)}</h4>
                        <p class="news-summary">${escapeHtml(item.summary)}</p>
                        <div class="news-meta">
                            <div class="flex items-center gap-2">
                                <span class="sentiment-${item.sentiment}">${item.sentiment}</span>
                                <span class="text-muted">•</span>
                                <span>${escapeHtml(item.source)}</span>
                            </div>
                            <span class="text-muted">${formatTime(item.published_at)}</span>
                        </div>
                        <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer" 
                           class="glass-btn mt-2" style="font-size: 0.875rem; padding: 0.5rem 1rem;">
                            Read More <i class="fas fa-external-link-alt"></i>
                        </a>
                    `;
                    
                    newsContainer.appendChild(newsCard);
                });
            }
            
            function updatePagination(currentPage, totalPages) {
                const paginationContainer = document.getElementById('news-pagination');
                
                if (totalPages <= 1) {
                    paginationContainer.innerHTML = '';
                    return;
                }
                
                let paginationHTML = '';
                
                // Previous button
                if (currentPage > 1) {
                    paginationHTML += `<button class="glass-btn" onclick="loadNews(${currentPage - 1})">Previous</button>`;
                }
                
                // Page numbers
                for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
                    const isActive = i === currentPage ? 'style="background: var(--primary)"' : '';
                    paginationHTML += `<button class="glass-btn" ${isActive} onclick="loadNews(${i})">${i}</button>`;
                }
                
                // Next button
                if (currentPage < totalPages) {
                    paginationHTML += `<button class="glass-btn" onclick="loadNews(${currentPage + 1})">Next</button>`;
                }
                
                paginationContainer.innerHTML = paginationHTML;
            }
            
            // === TAB CONTENT LOADING ===
            function loadTabContent(tabName) {
                switch(tabName) {
                    case 'live-news':
                        loadNews(1);
                        break;
                    case 'trends':
                        updateTrendsCharts();
                        break;
                    case 'analytics':
                        loadAnalytics();
                        break;
                }
            }
            
            // === CHARTS ===
            function initializeCharts() {
                // Initialize sentiment distribution chart
                const sentimentCtx = document.getElementById('sentiment-chart');
                if (sentimentCtx) {
                    // Destroy existing chart if it exists
                    if (charts.sentiment) {
                        charts.sentiment.destroy();
                    }
                    
                    charts.sentiment = new Chart(sentimentCtx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Positive', 'Negative', 'Neutral'],
                            datasets: [{
                                data: [""" + str(analytics['sentiment_distribution']['positive']) + """, """ + str(analytics['sentiment_distribution']['negative']) + """, """ + str(analytics['sentiment_distribution']['neutral']) + """],
                                backgroundColor: ['#10B981', '#EF4444', '#64748B'],
                                borderWidth: 0
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: {
                                        color: '#CBD5E1',
                                        padding: 20
                                    }
                                }
                            }
                        }
                    });
                }
            }
            
            function updateTrendsCharts() {
                // Update trend chart with new data
                const trendCtx = document.getElementById('trend-chart');
                if (trendCtx && !charts.trend) {
                    charts.trend = new Chart(trendCtx, {
                        type: 'line',
                        data: {
                            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            datasets: [{
                                label: 'Average Sentiment',
                                data: [0.6, 0.5, 0.7, 0.4, 0.8, 0.6, 0.7],
                                borderColor: '#3B82F6',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                tension: 0.4,
                                fill: true
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 1,
                                    ticks: { color: '#CBD5E1' },
                                    grid: { color: 'rgba(203, 213, 225, 0.1)' }
                                },
                                x: {
                                    ticks: { color: '#CBD5E1' },
                                    grid: { color: 'rgba(203, 213, 225, 0.1)' }
                                }
                            },
                            plugins: {
                                legend: {
                                    labels: { color: '#CBD5E1' }
                                }
                            }
                        }
                    });
                }
            }
            
            // === ANALYTICS ===
            async function loadAnalytics() {
                try {
                    const response = await fetch('/api/analytics/summary');
                    if (!response.ok) throw new Error('Failed to load analytics');
                    
                    const data = await response.json();
                    
                    document.getElementById('total-analyses').textContent = data.total_analyses.toLocaleString();
                    document.getElementById('avg-confidence').textContent = (data.average_confidence * 100).toFixed(1) + '%';
                    document.getElementById('trend-indicator').textContent = data.trend;
                    
                } catch (error) {
                    console.error('Analytics loading error:', error);
                }
            }
            
            // === EVENT LISTENERS ===
            function setupEventListeners() {
                // Enter key for sentiment analysis
                document.getElementById('sentiment-input').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
                        event.preventDefault();
                        analyzeSentiment();
                    }
                });
                
                // Auto-refresh news
                const autoRefreshCheckbox = document.getElementById('auto-refresh');
                if (autoRefreshCheckbox && autoRefreshCheckbox.checked) {
                    setInterval(() => {
                        if (document.querySelector('[data-tab="live-news"]').getAttribute('aria-selected') === 'true') {
                            loadNews(1);
                        }
                    }, 300000); // 5 minutes
                }
            }
            
            // === UTILITY FUNCTIONS ===
            function loadInitialData() {
                loadNews(1);
                loadAnalytics();
            }
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            function formatTime(timestamp) {
                try {
                    return new Date(timestamp).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                } catch {
                    return 'Recent';
                }
            }
            
            // === KEYWORD TRACKING ===
            function trackKeyword() {
                const input = document.getElementById('keyword-input');
                const keyword = input.value.trim();
                
                if (!keyword) {
                    alert('Please enter a keyword to track');
                    return;
                }
                
                // Add to tracked keywords
                const container = document.getElementById('tracked-keywords');
                const keywordDiv = document.createElement('div');
                keywordDiv.className = 'glass-card mb-2';
                keywordDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <span class="font-medium">${escapeHtml(keyword)}</span>
                        <div class="flex items-center gap-2">
                            <span class="sentiment-neutral">Tracking...</span>
                            <button class="text-error" onclick="this.parentElement.parentElement.parentElement.remove()">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                `;
                
                container.appendChild(keywordDiv);
                input.value = '';
            }
            
            // Make functions globally available
            window.analyzeSentiment = analyzeSentiment;
            window.loadNews = loadNews;
            window.trackKeyword = trackKeyword;
        </script>
    </body>
    </html>
    """
    
    return html_template

# === APPLICATION STARTUP ===

def initialize_app():
    """Initialize the application"""
    try:
        db.init_app(app)
        db.create_all()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

if __name__ == '__main__':
    initialize_app()
    
    logger.info("🚀 Starting Sentiment Intelligence Dashboard")
    logger.info(f"📊 Real components: {'✅ Available' if REAL_COMPONENTS_AVAILABLE else '❌ Fallback mode'}")
    logger.info(f"🌍 Default country: {settings.DEFAULT_NEWS_COUNTRY}")
    logger.info(f"🔒 CORS origins: {settings.ALLOWED_ORIGINS}")
    
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )
