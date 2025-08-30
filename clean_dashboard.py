"""
Clean Quick Start Sentiment Analysis Dashboard
No external dependencies to avoid conflicts
"""

import os
import sys
import json
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Flask and web components
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Clean sentiment analysis engine
class CleanSentimentEngine:
    """Clean sentiment analysis with no external dependencies"""
    
    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment and return a dictionary"""
        
        # Simple keyword-based sentiment analysis
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
        
        # Return a simple dictionary
        return {
            'text': text[:200],
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': {
                'positive': confidence if sentiment == 'positive' else (1-confidence) * 0.3,
                'negative': confidence if sentiment == 'negative' else (1-confidence) * 0.3,
                'neutral': confidence if sentiment == 'neutral' else (1-confidence) * 0.4
            },
            'model_used': 'clean-mock',
            'processing_time': 0.02,
            'language': 'en',
            'emotion_scores': {'joy': 0.7, 'anger': 0.1, 'fear': 0.1, 'sadness': 0.1},
            'toxicity_score': random.uniform(0, 0.3),
            'bias_score': random.uniform(0, 0.2)
        }

# Initialize components
sentiment_engine = CleanSentimentEngine()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/')
def dashboard():
    """Clean Dashboard"""
    return render_template_string(CLEAN_DASHBOARD_HTML)

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment endpoint"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Analyze sentiment
        result = sentiment_engine.analyze_sentiment(text)
        
        # Add success flag
        result['success'] = True
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/news')
def get_news():
    """Mock news endpoint"""
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
        }
    ]
    
    return jsonify({
        'items': sample_news,
        'page': 1,
        'limit': 10,
        'total_items': len(sample_news),
        'sources_used': ['TechNews', 'MarketWatch']
    })

@app.route('/api/social/tweets')
def get_tweets():
    """Mock tweets endpoint"""
    sample_tweets = [
        {
            'text': 'Just witnessed an amazing breakthrough in AI technology! The future is looking bright!',
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
        }
    ]
    
    return jsonify({
        'tweets': sample_tweets,
        'total': len(sample_tweets),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-clean'
    })

# Clean Dashboard HTML Template
CLEAN_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clean Sentiment Analysis Dashboard</title>
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Clean Sentiment Dashboard</h1>
            <p>Fast sentiment analysis without conflicts</p>
            <span class="status-badge">Ready & Working</span>
        </div>

        <div class="glass-card">
            <h2><i class="fas fa-brain"></i> Sentiment Analysis</h2>
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

    <script>
        let sentimentChart;

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
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    alert('Analysis failed: ' + result.error);
                }
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

        function clearInput() {
            document.getElementById('textInput').value = '';
            document.getElementById('results').style.display = 'none';
        }

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
    logger.info("Starting Clean Sentiment Analysis Dashboard")
    logger.info("Ready to go! Opening at http://localhost:5004")
    
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5004
    )
