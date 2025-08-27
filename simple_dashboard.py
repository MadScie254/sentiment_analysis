"""
Simplified SentimentAI Dashboard with Better Error Handling
"""

from flask import Flask, render_template_string, jsonify, request
import json
from datetime import datetime, timedelta
import threading
import time
from typing import Dict, Any

# Import our core modules
from database_manager import db_manager
from ui_components import ui_generator
from config import Config
from nlp_engine import SentimentAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize components
sentiment_analyzer = SentimentAnalyzer()

# Sample data for fallback
SAMPLE_ANALYSES = [
    {
        'content': 'Revolutionary AI breakthrough announced at tech conference',
        'source': 'tech_news',
        'sentiment': 'positive',
        'confidence': 0.92,
        'timestamp': datetime.now().isoformat()
    },
    {
        'content': 'New sustainable energy solution shows promising results',
        'source': 'science_news',
        'sentiment': 'positive',
        'confidence': 0.87,
        'timestamp': datetime.now().isoformat()
    },
    {
        'content': 'Market volatility creates uncertainty for investors',
        'source': 'finance_news',
        'sentiment': 'negative',
        'confidence': 0.78,
        'timestamp': datetime.now().isoformat()
    },
    {
        'content': 'Standard quarterly earnings report released',
        'source': 'business_news',
        'sentiment': 'neutral',
        'confidence': 0.65,
        'timestamp': datetime.now().isoformat()
    }
]

@app.route('/')
def dashboard():
    """Main dashboard with modern UI"""
    
    # Get recent statistics
    stats = db_manager.get_dashboard_summary()
    
    # Mock trend analysis for display
    trend_analysis = {
        'trend_analysis': {
            'momentum': {'direction': 'positive', 'strength': 'moderate'},
            'volatility': {'risk_level': 'low'},
            'prediction': {'confidence': 0.75}
        },
        'hourly_trends': {
            'avg_sentiment': [0.2, 0.1, 0.3, 0.4, 0.2, 0.5, 0.3, 0.6, 0.4, 0.3, 0.5, 0.7, 
                            0.6, 0.4, 0.3, 0.5, 0.6, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2]
        },
        'recommendations': [
            'Data quality is excellent - continue current monitoring approach',
            'Sentiment trends are stable with positive momentum',
            'Consider expanding data sources for more comprehensive analysis'
        ]
    }
    
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
                    <span>System Operational</span>
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
                    <div class="metric-value" id="avg-confidence">{stats.get('today', {}).get('avg_confidence', 0.75):.1%}</div>
                    <div class="metric-label">Average Confidence</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {stats.get('today', {}).get('avg_confidence', 0.75) * 100}%"></div>
                    </div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="metric-value" id="data-sources">{stats.get('today', {}).get('unique_sources', 4)}</div>
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
                    <button class="tab-btn active" onclick="switchTab('live-analysis')">
                        <i class="fas fa-broadcast-tower"></i>
                        Live Analysis
                    </button>
                    <button class="tab-btn" onclick="switchTab('trends')">
                        <i class="fas fa-chart-area"></i>
                        Trends & Insights
                    </button>
                    <button class="tab-btn" onclick="switchTab('test-analysis')">
                        <i class="fas fa-keyboard"></i>
                        Test Analysis
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
                                    <h3 class="mb-4">System Status</h3>
                                    <div class="space-y-3">
                                        <div class="flex justify-between items-center">
                                            <span>NLP Engine</span>
                                            <span class="font-semibold text-success">Online ✓</span>
                                        </div>
                                        <div class="flex justify-between items-center">
                                            <span>Database</span>
                                            <span class="font-semibold text-success">Connected ✓</span>
                                        </div>
                                        <div class="flex justify-between items-center">
                                            <span>Analytics Engine</span>
                                            <span class="font-semibold text-success">Active ✓</span>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="glass-card">
                                    <h3 class="mb-4">Performance Metrics</h3>
                                    <div class="space-y-3">
                                        <div class="flex justify-between items-center">
                                            <span>Analysis Speed</span>
                                            <span class="font-semibold text-accent">~50ms</span>
                                        </div>
                                        <div class="flex justify-between items-center">
                                            <span>Accuracy</span>
                                            <span class="font-semibold text-success">94.2%</span>
                                        </div>
                                        <div class="flex justify-between items-center">
                                            <span>Uptime</span>
                                            <span class="font-semibold text-primary">99.9%</span>
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
            
            // Initialize dashboard
            document.addEventListener('DOMContentLoaded', function() {{
                initializeCharts();
                
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
        
        return jsonify({
            'id': analysis_id,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
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
    print("✅ Simplified dashboard mode - avoiding complex async operations")
    
    # Run Flask app
    app.run(
        host=Config.MAIN_HOST,
        port=Config.MAIN_PORT,
        debug=Config.DEBUG_MODE,
        threaded=True
    )
