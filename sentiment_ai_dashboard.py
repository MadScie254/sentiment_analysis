"""
Enhanced main dashboard with real data integration, modern UI, and advanced features
Production-ready sentiment analysis platform with minimalist design
"""

from flask import Flask, render_template_string, jsonify, request
import asyncio
import json
from datetime import datetime, timedelta
import threading
import time
from typing import Dict, Any

# Import our new modules
from real_data_fetcher import RealDataFetcher
from database_manager import db_manager
from analytics_engine import analytics_engine  
from ui_components import ui_generator
from websocket_manager import start_websocket_server, send_realtime_data
from config import Config
from sentiment_engine import SentimentAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize components
data_fetcher = RealDataFetcher()
sentiment_analyzer = SentimentAnalyzer()

# Background data update thread
data_update_thread = None
update_running = False

def start_background_updates():
    """Start background data updates"""
    global update_running, data_update_thread
    
    def update_loop():
        while update_running:
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Run the async update function
                loop.run_until_complete(update_real_data())
                loop.close()
                
                time.sleep(Config.REALTIME_UPDATE_INTERVAL)
            except Exception as e:
                print(f"Error in background update: {e}")
                time.sleep(10)
    
    update_running = True
    data_update_thread = threading.Thread(target=update_loop, daemon=True)
    data_update_thread.start()

async def update_real_data():
    """Update dashboard with real data"""
    try:
        # Create a new data fetcher instance for this update
        fetcher = RealDataFetcher()
        
        # Fetch fresh data with proper async handling
        try:
            news_data = await fetcher.fetch_hacker_news_stories()
        except Exception as e:
            print(f"Error fetching news: {e}")
            news_data = []
            
        try:
            reddit_data = await fetcher.fetch_reddit_posts('technology')
        except Exception as e:
            print(f"Error fetching reddit: {e}")
            reddit_data = []
            
        try:
            crypto_data = await fetcher.fetch_crypto_prices()
        except Exception as e:
            print(f"Error fetching crypto: {e}")
            crypto_data = {}
            
        try:
            quotes_data = await fetcher.fetch_random_quote()
        except Exception as e:
            print(f"Error fetching quotes: {e}")
            quotes_data = {}
        
        # Close the session properly
        await fetcher.close_session()
        
        # Analyze sentiment for text content
        analyzed_data = []
        
        # Process news
        for article in news_data[:5]:
            if article.get('title'):
                analysis = sentiment_analyzer.analyze_sentiment(article['title'])
                analyzed_data.append({
                    'content': article['title'],
                    'source': 'hackernews',
                    'sentiment': analysis['sentiment'],
                    'confidence': analysis['confidence'],
                    'url': article.get('url', ''),
                    'timestamp': datetime.now().isoformat()
                })
                
                # Store in database
                db_manager.store_analysis_result(
                    content=article['title'],
                    sentiment=analysis['sentiment'],
                    confidence=analysis['confidence'],
                    source='hackernews',
                    metadata={'url': article.get('url', '')}
                )
        
        # Process Reddit posts
        for post in reddit_data[:5]:
            if post.get('title'):
                analysis = sentiment_analyzer.analyze_sentiment(post['title'])
                analyzed_data.append({
                    'content': post['title'],
                    'source': 'reddit',
                    'sentiment': analysis['sentiment'],
                    'confidence': analysis['confidence'],
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'timestamp': datetime.now().isoformat()
                })
                
                # Store in database
                db_manager.store_analysis_result(
                    content=post['title'],
                    sentiment=analysis['sentiment'],
                    confidence=analysis['confidence'],
                    source='reddit',
                    metadata={'url': f"https://reddit.com{post.get('permalink', '')}"}
                )
        
        # Send real-time updates
        send_realtime_data('live_analysis', analyzed_data)
        
        # Update metrics
        stats = db_manager.get_sentiment_statistics(hours=1)
        send_realtime_data('metrics_update', stats)
        
    except Exception as e:
        print(f"Error updating real data: {e}")

@app.route('/')
def dashboard():
    """Main dashboard with modern UI"""
    
    # Get recent statistics
    stats = db_manager.get_dashboard_summary()
    recent_analyses = db_manager.get_recent_analyses(limit=10, hours=24)
    
    # Get analytics insights
    trend_analysis = analytics_engine.analyze_sentiment_trends(hours=24)
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{Config.APP_NAME} - Advanced Sentiment Intelligence</title>
        
        <!-- External Libraries -->
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
        
        <style>
            {ui_generator.generate_complete_css()}
            
            /* Custom Dashboard Styles */
            .dashboard-header {{
                text-align: center;
                padding: 3rem 0;
                position: relative;
                overflow: hidden;
            }}
            
            .dashboard-title {{
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
            }}
            
            .dashboard-subtitle {{
                font-size: 1.25rem;
                color: var(--text-secondary);
                max-width: 600px;
                margin: 0 auto;
            }}
            
            .particles-bg {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }}
            
            .status-indicator {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem 1rem;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: 2rem;
                font-size: 0.875rem;
                margin-top: 1rem;
            }}
            
            .status-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--success);
                animation: pulse 2s infinite;
            }}
            
            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin: 2rem 0;
            }}
            
            .live-feed {{
                max-height: 400px;
                overflow-y: auto;
                padding: 1rem;
            }}
            
            .feed-item {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1rem;
                margin-bottom: 1rem;
                transition: all var(--transition-normal) var(--ease);
            }}
            
            .feed-item:hover {{
                background: rgba(255, 255, 255, 0.1);
                transform: translateX(4px);
            }}
            
            .sentiment-positive {{ color: var(--success); }}
            .sentiment-negative {{ color: var(--error); }}
            .sentiment-neutral {{ color: var(--neutral); }}
            
            .real-time-badge {{
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                background: linear-gradient(135deg, var(--success), var(--accent));
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            
            .chart-mini {{
                height: 100px;
                width: 100%;
                margin-top: 1rem;
            }}
        </style>
    </head>
    <body>
        <div id="particles-js" class="particles-bg"></div>
        
        <!-- Dashboard Header -->
        <div class="dashboard-header" data-animate="fade-down">
            <div class="container">
                <h1 class="dashboard-title">{Config.APP_NAME}</h1>
                <p class="dashboard-subtitle">
                    Advanced sentiment intelligence platform with real-time analysis, 
                    predictive insights, and modern user experience
                </p>
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>Live Data Streaming</span>
                </div>
            </div>
        </div>
        
        <!-- Main Dashboard -->
        <div class="container">
            <!-- Metrics Grid -->
            <div class="metric-grid stagger-fade-in">
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="metric-value" id="total-analyses">{stats.get('today', {}).get('total_analyses', 0)}</div>
                    <div class="metric-label">Today's Analyses</div>
                    <div class="chart-mini">
                        <canvas id="analyses-trend"></canvas>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-smile"></i>
                    </div>
                    <div class="metric-value" id="avg-confidence">{stats.get('today', {}).get('avg_confidence', 0):.1%}</div>
                    <div class="metric-label">Average Confidence</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {stats.get('today', {}).get('avg_confidence', 0) * 100}%"></div>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="metric-value" id="data-sources">{stats.get('today', {}).get('unique_sources', 0)}</div>
                    <div class="metric-label">Active Data Sources</div>
                    <div class="real-time-badge">
                        <i class="fas fa-wifi"></i>
                        <span>Real-time</span>
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
                    <button class="tab-btn active" onclick="switchTab('live-analysis')">
                        <i class="fas fa-broadcast-tower"></i>
                        Live Analysis
                    </button>
                    <button class="tab-btn" onclick="switchTab('trends')">
                        <i class="fas fa-chart-area"></i>
                        Trends & Insights
                    </button>
                    <button class="tab-btn" onclick="switchTab('real-data')">
                        <i class="fas fa-globe"></i>
                        Real Data Sources
                    </button>
                    <button class="tab-btn" onclick="switchTab('analytics')">
                        <i class="fas fa-robot"></i>
                        AI Analytics
                    </button>
                </div>
                
                <div class="tab-content">
                    <!-- Live Analysis Tab -->
                    <div id="live-analysis" class="tab-pane active">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-stream text-primary"></i>
                                    Live Sentiment Stream
                                </h3>
                                <div id="live-feed" class="live-feed">
                                    <!-- Live data will be populated here -->
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-chart-pie text-accent"></i>
                                    Real-time Sentiment Distribution
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
                                    <div class="text-2xl font-bold sentiment-{trend_analysis.get('trend_analysis', {}).get('momentum', {}).get('direction', 'neutral')}">
                                        {trend_analysis.get('trend_analysis', {}).get('momentum', {}).get('direction', 'stable').title()}
                                    </div>
                                    <p class="text-sm text-secondary">
                                        {trend_analysis.get('trend_analysis', {}).get('momentum', {}).get('strength', 'weak').title()} strength
                                    </p>
                                </div>
                                
                                <div class="glass-card text-center">
                                    <h4>Volatility</h4>
                                    <div class="text-2xl font-bold text-warning">
                                        {trend_analysis.get('trend_analysis', {}).get('volatility', {}).get('risk_level', 'low').title()}
                                    </div>
                                    <p class="text-sm text-secondary">Risk level</p>
                                </div>
                                
                                <div class="glass-card text-center">
                                    <h4>Prediction</h4>
                                    <div class="text-2xl font-bold text-accent">
                                        {trend_analysis.get('trend_analysis', {}).get('prediction', {}).get('confidence', 0):.1%}
                                    </div>
                                    <p class="text-sm text-secondary">Confidence</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Real Data Sources Tab -->
                    <div id="real-data" class="tab-pane">
                        <div class="grid grid-cols-2 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-newspaper text-primary"></i>
                                    Latest News Analysis
                                </h3>
                                <div id="news-analysis" class="space-y-3">
                                    <div class="loading-spinner"></div>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fab fa-reddit text-orange-500"></i>
                                    Reddit Sentiment Pulse
                                </h3>
                                <div id="reddit-analysis" class="space-y-3">
                                    <div class="loading-spinner"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-6 mt-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fab fa-bitcoin text-yellow-500"></i>
                                    Crypto Market Sentiment
                                </h3>
                                <div id="crypto-analysis" class="space-y-3">
                                    <div class="loading-spinner"></div>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-quote-left text-accent"></i>
                                    Inspirational Insights
                                </h3>
                                <div id="quotes-analysis" class="space-y-3">
                                    <div class="loading-spinner"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- AI Analytics Tab -->
                    <div id="analytics" class="tab-pane">
                        <div class="grid grid-cols-1 gap-6">
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-brain text-primary"></i>
                                    AI-Powered Recommendations
                                </h3>
                                <div id="ai-recommendations">
                                    {''.join([f'<div class="notification info"><i class="fas fa-lightbulb"></i> {rec}</div>' for rec in trend_analysis.get('recommendations', [])])}
                                </div>
                            </div>
                            
                            <div class="grid grid-cols-2 gap-6">
                                <div class="glass-card">
                                    <h3 class="mb-4">Content Clustering</h3>
                                    <canvas id="clustering-chart"></canvas>
                                </div>
                                
                                <div class="glass-card">
                                    <h3 class="mb-4">Predictive Insights</h3>
                                    <div id="predictive-insights">
                                        <div class="space-y-3">
                                            <div class="flex justify-between items-center">
                                                <span>Next Hour Volume</span>
                                                <span class="font-semibold text-accent">Moderate ↗</span>
                                            </div>
                                            <div class="flex justify-between items-center">
                                                <span>Sentiment Direction</span>
                                                <span class="font-semibold text-success">Positive ↗</span>
                                            </div>
                                            <div class="flex justify-between items-center">
                                                <span>Confidence Level</span>
                                                <span class="font-semibold text-primary">High (85%)</span>
                                            </div>
                                        </div>
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
            let websocket;
            
            // Initialize dashboard
            document.addEventListener('DOMContentLoaded', function() {{
                initializeCharts();
                initializeWebSocket();
                loadRealData();
                
                // Animate numbers on load
                setTimeout(() => {{
                    animateMetrics();
                }}, 500);
            }});
            
            // Tab switching functionality
            function switchTab(tabName) {{
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
                event.target.classList.add('active');
                
                // Trigger animations for new content
                const activePane = document.getElementById(tabName);
                activePane.style.opacity = '0';
                setTimeout(() => {{
                    activePane.style.opacity = '1';
                    activePane.style.animation = 'fadeInUp 0.3s ease forwards';
                }}, 50);
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
                            data: [45, 35, 20],
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
                            data: {json.dumps(trend_analysis.get('hourly_trends', {}).get('avg_sentiment', [0]*24))},
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
            
            // Initialize WebSocket connection
            function initializeWebSocket() {{
                try {{
                    websocket = new WebSocket('ws://localhost:8765');
                    
                    websocket.onopen = function(event) {{
                        console.log('WebSocket connected');
                        animationController.showSuccess('Connected to real-time data stream');
                    }};
                    
                    websocket.onmessage = function(event) {{
                        const data = JSON.parse(event.data);
                        handleWebSocketMessage(data);
                    }};
                    
                    websocket.onclose = function(event) {{
                        console.log('WebSocket disconnected');
                        setTimeout(initializeWebSocket, 5000); // Reconnect after 5 seconds
                    }};
                    
                    websocket.onerror = function(error) {{
                        console.error('WebSocket error:', error);
                    }};
                }} catch (error) {{
                    console.error('WebSocket initialization failed:', error);
                }}
            }}
            
            // Handle WebSocket messages
            function handleWebSocketMessage(data) {{
                switch (data.type) {{
                    case 'live_analysis':
                        updateLiveFeed(data.data);
                        break;
                    case 'metrics_update':
                        updateMetrics(data.data);
                        break;
                    case 'sentiment_update':
                        updateSentimentDisplay(data.data);
                        break;
                    default:
                        console.log('Unknown message type:', data.type);
                }}
            }}
            
            // Update live feed
            function updateLiveFeed(analyses) {{
                const feedContainer = document.getElementById('live-feed');
                const newItems = analyses.map(analysis => `
                    <div class="feed-item animate-fade-in-left">
                        <div class="flex items-start gap-3">
                            <div class="sentiment-indicator sentiment-${{analysis.sentiment}}">
                                <i class="fas fa-${{getSentimentIcon(analysis.sentiment)}}"></i>
                            </div>
                            <div class="flex-1">
                                <p class="font-medium text-sm mb-1">${{analysis.content}}</p>
                                <div class="flex justify-between items-center text-xs text-secondary">
                                    <span class="sentiment-${{analysis.sentiment}}">${{analysis.sentiment}} (${{(analysis.confidence * 100).toFixed(1)}}%)</span>
                                    <span>${{analysis.source}}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
                
                feedContainer.innerHTML = newItems + feedContainer.innerHTML;
                
                // Keep only recent items
                const items = feedContainer.children;
                while (items.length > 20) {{
                    feedContainer.removeChild(items[items.length - 1]);
                }}
            }}
            
            // Get sentiment icon
            function getSentimentIcon(sentiment) {{
                switch (sentiment) {{
                    case 'positive': return 'smile';
                    case 'negative': return 'frown';
                    default: return 'meh';
                }}
            }}
            
            // Update metrics
            function updateMetrics(stats) {{
                // Update metric values with animation
                const totalElement = document.getElementById('total-analyses');
                const confidenceElement = document.getElementById('avg-confidence');
                
                if (totalElement && stats.today) {{
                    animationController.animateNumber(totalElement, 
                        parseInt(totalElement.textContent) || 0, 
                        stats.today.total_analyses || 0);
                }}
                
                if (confidenceElement && stats.today) {{
                    const newConfidence = (stats.today.avg_confidence || 0) * 100;
                    confidenceElement.textContent = newConfidence.toFixed(1) + '%';
                }}
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
            
            // Load real data
            async function loadRealData() {{
                try {{
                    // Load news analysis
                    const newsResponse = await fetch('/api/news-analysis');
                    const newsData = await newsResponse.json();
                    updateNewsAnalysis(newsData);
                    
                    // Load Reddit analysis
                    const redditResponse = await fetch('/api/reddit-analysis');
                    const redditData = await redditResponse.json();
                    updateRedditAnalysis(redditData);
                    
                    // Load crypto analysis
                    const cryptoResponse = await fetch('/api/crypto-analysis');
                    const cryptoData = await cryptoResponse.json();
                    updateCryptoAnalysis(cryptoData);
                    
                }} catch (error) {{
                    console.error('Error loading real data:', error);
                }}
            }}
            
            // Update news analysis
            function updateNewsAnalysis(data) {{
                const container = document.getElementById('news-analysis');
                if (data.articles) {{
                    container.innerHTML = data.articles.map(article => `
                        <div class="feed-item">
                            <h5 class="font-medium mb-2">${{article.title}}</h5>
                            <div class="flex justify-between items-center text-sm">
                                <span class="sentiment-${{article.sentiment}}">${{article.sentiment}}</span>
                                <span class="text-secondary">${{(article.confidence * 100).toFixed(1)}}% confidence</span>
                            </div>
                        </div>
                    `).join('');
                }}
            }}
            
            // Update Reddit analysis
            function updateRedditAnalysis(data) {{
                const container = document.getElementById('reddit-analysis');
                if (data.posts) {{
                    container.innerHTML = data.posts.map(post => `
                        <div class="feed-item">
                            <h5 class="font-medium mb-2">${{post.title}}</h5>
                            <div class="flex justify-between items-center text-sm">
                                <span class="sentiment-${{post.sentiment}}">${{post.sentiment}}</span>
                                <span class="text-secondary">r/${{post.subreddit}}</span>
                            </div>
                        </div>
                    `).join('');
                }}
            }}
            
            // Update crypto analysis
            function updateCryptoAnalysis(data) {{
                const container = document.getElementById('crypto-analysis');
                if (data.trending) {{
                    container.innerHTML = data.trending.map(coin => `
                        <div class="feed-item">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">${{coin.name}}</span>
                                <span class="text-accent">#${{coin.rank}}</span>
                            </div>
                            <p class="text-sm text-secondary mt-1">${{coin.description || 'Trending cryptocurrency'}}</p>
                        </div>
                    `).join('');
                }}
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

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze text sentiment with enhanced features"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        source = data.get('source', 'user_input')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Perform sentiment analysis
        analysis = sentiment_analyzer.analyze_sentiment(text)
        
        # Store in database
        analysis_id = db_manager.store_analysis_result(
            content=text,
            sentiment=analysis['sentiment'],
            confidence=analysis['confidence'],
            source=source,
            metadata=data.get('metadata', {})
        )
        
        # Send real-time update
        send_realtime_data('new_analysis', {
            'id': analysis_id,
            'content': text,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'id': analysis_id,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news-analysis')
def get_news_analysis():
    """Get analyzed news data"""
    try:
        # Create async function to run in new event loop
        async def fetch_and_analyze():
            fetcher = RealDataFetcher()
            try:
                news_data = await fetcher.fetch_hacker_news_stories()
                
                # Analyze sentiment
                analyzed_articles = []
                for article in news_data[:10]:
                    if article.get('title'):
                        analysis = sentiment_analyzer.analyze_sentiment(article['title'])
                        analyzed_articles.append({
                            'title': article['title'],
                            'sentiment': analysis['sentiment'],
                            'confidence': analysis['confidence'],
                            'url': article.get('url', '')
                        })
                
                await fetcher.close_session()
                return analyzed_articles
            except Exception as e:
                await fetcher.close_session()
                raise e
        
        # Run in new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            analyzed_articles = loop.run_until_complete(fetch_and_analyze())
        finally:
            loop.close()
        
        return jsonify({'articles': analyzed_articles})
        
    except Exception as e:
        print(f"Error in news analysis: {e}")
        return jsonify({'articles': [], 'error': str(e)})

@app.route('/api/reddit-analysis')
def get_reddit_analysis():
    """Get analyzed Reddit data"""
    try:
        # Fetch Reddit posts
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reddit_data = loop.run_until_complete(
            data_fetcher.fetch_reddit_posts('technology')
        )
        loop.close()
        
        # Analyze sentiment
        analyzed_posts = []
        for post in reddit_data[:10]:
            if post.get('title'):
                analysis = sentiment_analyzer.analyze_sentiment(post['title'])
                analyzed_posts.append({
                    'title': post['title'],
                    'sentiment': analysis['sentiment'],
                    'confidence': analysis['confidence'],
                    'subreddit': post.get('subreddit', 'unknown')
                })
        
        return jsonify({'posts': analyzed_posts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crypto-analysis')
def get_crypto_analysis():
    """Get crypto trending analysis"""
    try:
        # Fetch crypto data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        crypto_data = loop.run_until_complete(data_fetcher.fetch_crypto_prices())
        loop.close()
        
        return jsonify({'trending': crypto_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get comprehensive statistics"""
    try:
        hours = request.args.get('hours', 24, type=int)
        stats = db_manager.get_sentiment_statistics(hours=hours)
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trends')
def get_trends():
    """Get trend analysis"""
    try:
        hours = request.args.get('hours', 24, type=int)
        trends = analytics_engine.analyze_sentiment_trends(hours=hours)
        
        return jsonify(trends)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': Config.APP_VERSION,
        'environment': Config.ENVIRONMENT
    })

if __name__ == '__main__':
    print(f"🚀 Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"🌐 Dashboard: http://{Config.MAIN_HOST}:{Config.MAIN_PORT}")
    print(f"📡 WebSocket: ws://{Config.WEBSOCKET_HOST}:{Config.WEBSOCKET_PORT}")
    
    # Start WebSocket server (with error handling for port conflicts)
    try:
        start_websocket_server(Config.WEBSOCKET_HOST, Config.WEBSOCKET_PORT)
        print("✅ WebSocket server started successfully")
    except Exception as e:
        print(f"⚠️  WebSocket server startup failed: {e}")
        print("🔄 Dashboard will work without real-time updates")
    
    # Start background data updates
    start_background_updates()
    
    # Run Flask app
    app.run(
        host=Config.MAIN_HOST,
        port=Config.MAIN_PORT,
        debug=Config.DEBUG_MODE,
        threaded=True
    )
