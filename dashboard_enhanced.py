#!/usr/bin/env python3
"""
Enhanced Sentiment Analysis Dashboard with Stable Charts and Video Metadata Extraction
Fixed: Scroll/Graph Growing & Infinite Auto-scroll Bug
Added: Video Metadata Extractor for URLs and Files
Added: Comprehensive Tabbed Layout with Pagination
"""

import os
import math
import json
import tempfile
from datetime import datetime, timedelta
from threading import Lock
from functools import lru_cache
from flask import Flask, render_template_string, request, jsonify
from video_metadata import extract_video_metadata

# Enhanced imports for better functionality
try:
    from ui_generator import UIGenerator
    from database_manager import DatabaseManager
    from nlp_engine import NLPEngine
    from config import Config
except ImportError as e:
    print(f"Warning: Could not import module: {e}")
    # Create mock classes for testing
    class UIGenerator:
        @staticmethod
        def generate_dashboard_html(*args, **kwargs):
            return "<div>Mock Dashboard</div>"
    
    class DatabaseManager:
        def get_dashboard_summary(self):
            return {'today': {'total_analyses': 42, 'avg_confidence': 0.85, 'unique_sources': 4, 'ai_insights': 23}}
    
    class NLPEngine:
        def analyze_sentiment(self, text):
            return {'sentiment': 'positive', 'confidence': 0.85, 'toxicity': 0.1}
    
    class Config:
        SECRET_KEY = 'dev-key-change-in-production'
        ENVIRONMENT = 'development'

# Initialize Flask app with enhanced configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file upload

# Initialize components
db_manager = DatabaseManager()
nlp_engine = NLPEngine()
ui_generator = UIGenerator()

# Thread-safe cache for performance
cache_lock = Lock()
sentiment_cache = {}

@lru_cache(maxsize=128)
def get_cached_sentiment_data(cache_key):
    """Get cached sentiment data with enhanced analytics"""
    return {
        'sentiment_distribution': {
            'positive': 0.65,
            'negative': 0.15,
            'neutral': 0.20
        },
        'toxicity_scores': [0.05, 0.12, 0.08, 0.15, 0.09],
        'emotion_scores': [0.7, 0.1, 0.05, 0.1, 0.03, 0.02],  # Joy, Anger, Fear, Sadness, Surprise, Disgust
        'anomalies': [
            {
                'timestamp': '2024-01-15 14:30:00',
                'type': 'sentiment_spike',
                'severity': 'medium',
                'description': 'Unusual positive sentiment spike detected'
            },
            {
                'timestamp': '2024-01-15 13:45:00',
                'type': 'toxicity_alert',
                'severity': 'low',
                'description': 'Toxicity level slightly elevated'
            }
        ]
    }

def generate_trend_analysis():
    """Generate enhanced trend analysis with hourly data"""
    hours = [f"{i:02d}:00" for i in range(24)]
    sentiment_scores = [0.4 + 0.3 * math.sin(i * math.pi / 12) + 0.1 * math.sin(i * math.pi / 6) for i in range(24)]
    volumes = [50 + 30 * math.sin(i * math.pi / 8) + 20 * math.sin(i * math.pi / 4) for i in range(24)]
    
    return {
        'hourly_data': {
            'hours': hours,
            'sentiment_scores': sentiment_scores,
            'volumes': volumes
        },
        'momentum': {
            'direction': 'positive',
            'strength': 'strong'
        },
        'volatility': {
            'risk_level': 'low'
        },
        'prediction': {
            'confidence': 0.87
        }
    }

def generate_anomalies_html(anomalies):
    """Generate HTML for anomaly display"""
    if not anomalies:
        return '<p class="text-muted">No anomalies detected</p>'
    
    html = ''
    for anomaly in anomalies:
        severity_class = f"severity-{anomaly['severity']}"
        html += f"""
        <div class="anomaly-item {severity_class}">
            <div class="anomaly-header">
                <span class="anomaly-type">{anomaly['type'].replace('_', ' ').title()}</span>
                <span class="anomaly-time">{anomaly['timestamp']}</span>
            </div>
            <p class="anomaly-description">{anomaly['description']}</p>
        </div>
        """
    return html

@app.route('/')
def dashboard():
    """Enhanced immersive dashboard with stable charts and tabbed layout"""
    
    # Get cached data for better performance
    sentiment_data = get_cached_sentiment_data("main_dashboard")
    stats = db_manager.get_dashboard_summary()
    trend_analysis = generate_trend_analysis()
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced Sentiment Analysis Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Enhanced CSS Variables for Dark Mode */
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
                --transition-fast: 0.15s;
                --transition-normal: 0.3s;
                --transition-slow: 0.5s;
                --ease: cubic-bezier(0.4, 0, 0.2, 1);
            }

            /* Global Styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, var(--background) 0%, #1a202c 100%);
                color: var(--text-primary);
                line-height: 1.6;
                min-height: 100vh;
            }

            /* CRITICAL: Chart Container Styles - NO AUTO-RESIZE! */
            .chart-container {
                position: relative;
                width: 100% !important;
                height: 300px !important;  /* FIXED HEIGHT - NO RESIZING */
                max-height: 300px !important;
                overflow: hidden;
                background: var(--glass);
                border-radius: var(--border-radius);
                padding: 1rem;
            }

            .chart-container canvas {
                max-width: 100% !important;
                max-height: 270px !important;  /* FIXED HEIGHT */
                width: 100% !important;
                height: 270px !important;  /* PREVENT GROWTH */
            }

            /* Enhanced Glass Morphism */
            .glass-card {
                background: var(--glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                box-shadow: var(--shadow);
                transition: all var(--transition-normal) var(--ease);
                position: relative;
                overflow: hidden;
            }

            .glass-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
            }

            .glass-card:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
                border-color: var(--primary);
            }

            /* Enhanced Header */
            .header {
                background: var(--glass);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--glass-border);
                padding: 1rem 2rem;
                position: sticky;
                top: 0;
                z-index: 100;
            }

            .header-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1400px;
                margin: 0 auto;
            }

            .logo {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--primary);
            }

            .nav-links {
                display: flex;
                gap: 2rem;
                list-style: none;
            }

            .nav-links a {
                color: var(--text-secondary);
                text-decoration: none;
                transition: color var(--transition-fast) var(--ease);
                position: relative;
            }

            .nav-links a:hover {
                color: var(--primary);
            }

            .nav-links a::after {
                content: '';
                position: absolute;
                bottom: -4px;
                left: 0;
                width: 0;
                height: 2px;
                background: var(--primary);
                transition: width var(--transition-normal) var(--ease);
            }

            .nav-links a:hover::after {
                width: 100%;
            }

            /* Container & Layout */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }

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

            .grid-cols-4 {
                grid-template-columns: repeat(4, 1fr);
            }

            /* Enhanced Metrics Grid */
            .metric-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .metric-card {
                background: var(--glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                position: relative;
                overflow: hidden;
                transition: all var(--transition-normal) var(--ease);
            }

            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }

            .metric-icon {
                font-size: 2rem;
                color: var(--primary);
                margin-bottom: 1rem;
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }

            .metric-label {
                color: var(--text-secondary);
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            /* Enhanced Tab System */
            .tab-container {
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                overflow: hidden;
                margin: 2rem 0;
            }

            .tab-nav {
                display: flex;
                background: rgba(255, 255, 255, 0.05);
                border-bottom: 1px solid var(--glass-border);
                overflow-x: auto;
            }

            .tab-btn {
                background: transparent;
                border: none;
                color: var(--text-secondary);
                padding: 1rem 1.5rem;
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                position: relative;
                white-space: nowrap;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-weight: 500;
            }

            .tab-btn::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 0;
                height: 2px;
                background: var(--primary);
                transition: width var(--transition-normal) var(--ease);
            }

            .tab-btn:hover {
                color: var(--text-primary);
                background: rgba(99, 102, 241, 0.1);
            }

            .tab-btn.active {
                color: var(--primary);
                background: rgba(99, 102, 241, 0.1);
            }

            .tab-btn.active::after {
                width: 100%;
            }

            .tab-content {
                padding: 2rem;
                min-height: 500px;
            }

            .tab-pane {
                display: none;
                animation: fadeInUp var(--transition-normal) var(--ease);
            }

            .tab-pane.active {
                display: block;
            }

            /* Pagination styles - NO INFINITE SCROLL */
            .pagination-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.5rem;
                margin: 2rem 0;
                padding: 1rem;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
            }

            .pagination-btn {
                background: var(--glass);
                border: 1px solid var(--glass-border);
                color: var(--text-primary);
                padding: 0.5rem 1rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                min-width: 40px;
                text-align: center;
            }

            .pagination-btn:hover:not(:disabled) {
                background: var(--primary);
                border-color: var(--primary);
                transform: translateY(-1px);
            }

            .pagination-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            .pagination-btn.active {
                background: var(--primary);
                border-color: var(--primary);
                font-weight: 600;
            }

            /* Media panel styles */
            .media-panel {
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                margin-bottom: 1rem;
            }

            .media-input-toggle {
                display: flex;
                background: var(--glass);
                border-radius: var(--border-radius);
                padding: 0.25rem;
                margin-bottom: 1rem;
            }

            .media-toggle-btn {
                flex: 1;
                background: transparent;
                border: none;
                color: var(--text-secondary);
                padding: 0.75rem 1rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            }

            .media-toggle-btn.active {
                background: var(--primary);
                color: white;
            }

            .url-input-container,
            .file-input-container {
                display: none;
            }

            .url-input-container.active,
            .file-input-container.active {
                display: block;
            }

            .media-url-input {
                flex: 1;
                background: var(--glass);
                border: 1px solid var(--glass-border);
                border-radius: var(--border-radius);
                padding: 0.75rem;
                color: var(--text-primary);
                font-size: 1rem;
            }

            .file-drop-zone {
                border: 2px dashed var(--glass-border);
                border-radius: var(--border-radius);
                padding: 3rem;
                text-align: center;
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                background: var(--glass);
            }

            .file-drop-zone:hover {
                border-color: var(--primary);
                background: rgba(59, 130, 246, 0.1);
            }

            .glass-btn {
                background: var(--glass);
                border: 1px solid var(--glass-border);
                color: var(--text-primary);
                padding: 0.75rem 1.5rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                transition: all var(--transition-normal) var(--ease);
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .glass-btn.primary {
                background: var(--primary);
                border-color: var(--primary);
                color: white;
            }

            .glass-btn:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }

            /* Utility Classes */
            .flex {
                display: flex;
            }

            .gap-2 {
                gap: 0.5rem;
            }

            .gap-4 {
                gap: 1rem;
            }

            .gap-6 {
                gap: 1.5rem;
            }

            .mb-2 {
                margin-bottom: 0.5rem;
            }

            .mb-4 {
                margin-bottom: 1rem;
            }

            .mt-6 {
                margin-top: 1.5rem;
            }

            .text-primary {
                color: var(--primary);
            }

            .text-secondary {
                color: var(--text-secondary);
            }

            .text-accent {
                color: var(--accent);
            }

            .text-success {
                color: var(--success);
            }

            .text-warning {
                color: var(--warning);
            }

            .text-error {
                color: var(--error);
            }

            .text-sm {
                font-size: 0.875rem;
            }

            .text-2xl {
                font-size: 1.5rem;
            }

            .font-bold {
                font-weight: 700;
            }

            .font-medium {
                font-weight: 500;
            }

            .block {
                display: block;
            }

            .space-y-4 > * + * {
                margin-top: 1rem;
            }

            /* Responsive Design */
            @media (max-width: 768px) {
                .container {
                    padding: 1rem;
                }

                .metric-grid {
                    grid-template-columns: 1fr;
                }

                .grid-cols-2,
                .grid-cols-3 {
                    grid-template-columns: 1fr;
                }

                .tab-nav {
                    flex-wrap: wrap;
                }

                .tab-btn {
                    flex: 1;
                    min-width: 120px;
                }
            }

            /* Animation Classes */
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

            .fade-in {
                animation: fadeInUp 0.6s ease forwards;
            }

            .stagger-fade-in > * {
                animation: fadeInUp 0.6s ease forwards;
            }

            .stagger-fade-in > *:nth-child(2) {
                animation-delay: 0.1s;
            }

            .stagger-fade-in > *:nth-child(3) {
                animation-delay: 0.2s;
            }

            .stagger-fade-in > *:nth-child(4) {
                animation-delay: 0.3s;
            }
        </style>
    </head>
    <body>
        <!-- Enhanced Header -->
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-brain"></i>
                    <span>Sentiment AI Dashboard</span>
                </div>
                <nav>
                    <ul class="nav-links">
                        <li><a href="#overview">Overview</a></li>
                        <li><a href="#trends">Trends</a></li>
                        <li><a href="#segments">Segments</a></li>
                        <li><a href="#news">News</a></li>
                        <li><a href="#media">Media</a></li>
                        <li><a href="#admin">Admin</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <!-- Main Dashboard Content -->
        <div class="container">
            <!-- Enhanced Metrics Grid -->
            <div class="metric-grid stagger-fade-in">
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="metric-value" id="total-analyses">""" + str(stats.get('today', {}).get('total_analyses', 0)) + """</div>
                    <div class="metric-label">Today's Analyses</div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-smile"></i>
                    </div>
                    <div class="metric-value" id="avg-confidence">""" + f"{sentiment_data['sentiment_distribution']['positive']:.1%}" + """</div>
                    <div class="metric-label">Positive Sentiment</div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div class="metric-value" id="toxicity-level">""" + f"{max(sentiment_data['toxicity_scores']):.1%}" + """</div>
                    <div class="metric-label">Max Toxicity Level</div>
                </div>
                
                <div class="metric-card" data-animate="scale">
                    <div class="metric-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="metric-value" id="ai-insights">""" + str(len(sentiment_data['anomalies'])) + """</div>
                    <div class="metric-label">AI Insights</div>
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
                                <div class="glass-card">
                                    <h4>Momentum</h4>
                                    <div class="text-2xl font-bold text-""" + trend_analysis['momentum']['direction'] + """">
                                        """ + trend_analysis['momentum']['direction'].title() + """
                                    </div>
                                    <p class="text-sm text-secondary">
                                        """ + trend_analysis['momentum']['strength'].title() + """ strength
                                    </p>
                                </div>
                                
                                <div class="glass-card">
                                    <h4>Risk Level</h4>
                                    <div class="text-2xl font-bold text-success">
                                        """ + trend_analysis['volatility']['risk_level'].title() + """
                                    </div>
                                    <p class="text-sm text-secondary">Toxicity assessment</p>
                                </div>
                                
                                <div class="glass-card">
                                    <h4>Confidence</h4>
                                    <div class="text-2xl font-bold text-accent">
                                        """ + f"{trend_analysis['prediction']['confidence']:.0%}" + """
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
                                    """ + generate_anomalies_html(sentiment_data['anomalies']) + """
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
                                <div class="chart-container">
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
                                    <div class="flex justify-between">
                                        <span>API Status:</span>
                                        <span class="text-success">Operational</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>Database:</span>
                                        <span class="text-success">Connected</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>NLP Engine:</span>
                                        <span class="text-success">Ready</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>Cache:</span>
                                        <span class="text-success">Active</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="glass-card">
                                <h3 class="mb-4">
                                    <i class="fas fa-sliders-h text-primary"></i>
                                    Configuration
                                </h3>
                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-sm font-medium mb-2">Sentiment Threshold:</label>
                                        <input type="range" min="0" max="1" step="0.1" value="0.7" class="w-full">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium mb-2">Toxicity Alert Level:</label>
                                        <input type="range" min="0" max="1" step="0.1" value="0.8" class="w-full">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium mb-2">Cache Duration (minutes):</label>
                                        <input type="number" min="1" max="60" value="5" class="glass-btn">
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
        let chartInstances = {};
        
        // Chart configuration with stability features
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.responsive = false;  // CRITICAL: Prevent auto-resizing
        Chart.defaults.maintainAspectRatio = false;  // Allow fixed dimensions
        
        // Enhanced Tab Switching with Animation
        function switchTab(tabName, element) {
            // Remove active from all tabs and buttons
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            
            // Add active to current tab and button
            element.classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            // Load tab-specific content
            switch(tabName) {
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
            }
        }
        
        // Initialize Overview Charts with FIXED DIMENSIONS
        function initializeOverviewCharts() {
            // Sentiment Pie Chart - FIXED SIZE
            if (!chartInstances.sentimentPie) {
                const ctx = document.getElementById('sentiment-pie-chart');
                if (ctx) {
                    ctx.width = 400;
                    ctx.height = 270;
                    chartInstances.sentimentPie = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Positive', 'Negative', 'Neutral'],
                            datasets: [{
                                data: [""" + f"{sentiment_data['sentiment_distribution']['positive']:.2f}" + """, 
                                       """ + f"{sentiment_data['sentiment_distribution']['negative']:.2f}" + """, 
                                       """ + f"{sentiment_data['sentiment_distribution']['neutral']:.2f}" + """],
                                backgroundColor: ['#10B981', '#EF4444', '#6B7280'],
                                borderWidth: 0
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom'
                                }
                            }
                        }
                    });
                }
            }
            
            // Toxicity Gauge - FIXED SIZE
            if (!chartInstances.toxicityGauge) {
                const ctx = document.getElementById('toxicity-gauge');
                if (ctx) {
                    ctx.width = 400;
                    ctx.height = 270;
                    const maxToxicity = """ + f"{max(sentiment_data['toxicity_scores']):.2f}" + """;
                    chartInstances.toxicityGauge = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: [maxToxicity, 1 - maxToxicity],
                                backgroundColor: ['#EF4444', '#E5E7EB'],
                                borderWidth: 0,
                                circumference: 180,
                                rotation: 270
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            cutout: '70%',
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    enabled: false
                                }
                            }
                        }
                    });
                }
            }
        }
        
        // Initialize Trends Charts with FIXED DIMENSIONS
        function initializeTrendsCharts() {
            // Trends Line Chart - FIXED SIZE
            if (!chartInstances.trendsChart) {
                const ctx = document.getElementById('trends-chart');
                if (ctx) {
                    ctx.width = 800;
                    ctx.height = 270;
                    chartInstances.trendsChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: """ + str(trend_analysis['hourly_data']['hours']) + """,
                            datasets: [{
                                label: 'Sentiment Score',
                                data: """ + str(trend_analysis['hourly_data']['sentiment_scores']) + """,
                                borderColor: '#3B82F6',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                tension: 0.4,
                                fill: true
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 1
                                }
                            }
                        }
                    });
                }
            }
            
            // Volume Bar Chart - FIXED SIZE
            if (!chartInstances.volumeChart) {
                const ctx = document.getElementById('volume-chart');
                if (ctx) {
                    ctx.width = 400;
                    ctx.height = 270;
                    chartInstances.volumeChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: """ + str(trend_analysis['hourly_data']['hours']) + """,
                            datasets: [{
                                label: 'Message Volume',
                                data: """ + str(trend_analysis['hourly_data']['volumes']) + """,
                                backgroundColor: '#10B981'
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
            }
        }
        
        // Initialize Segments Charts
        function initializeSegmentsCharts() {
            // Sources Pie Chart
            if (!chartInstances.sourcesChart) {
                const ctx = document.getElementById('sources-chart');
                if (ctx) {
                    ctx.width = 400;
                    ctx.height = 270;
                    chartInstances.sourcesChart = new Chart(ctx, {
                        type: 'pie',
                        data: {
                            labels: ['Social Media', 'News', 'Forums', 'Reviews'],
                            datasets: [{
                                data: [45, 25, 20, 10],
                                backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false
                        }
                    });
                }
            }
            
            // Emotions Radar Chart
            if (!chartInstances.emotionsChart) {
                const ctx = document.getElementById('emotions-chart');
                if (ctx) {
                    ctx.width = 600;
                    ctx.height = 270;
                    chartInstances.emotionsChart = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: ['Joy', 'Anger', 'Fear', 'Sadness', 'Surprise', 'Disgust'],
                            datasets: [{
                                label: 'Emotion Intensity',
                                data: """ + str(sentiment_data['emotion_scores']) + """,
                                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                                borderColor: '#3B82F6',
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: false,
                            maintainAspectRatio: false,
                            scales: {
                                r: {
                                    beginAtZero: true,
                                    max: 1
                                }
                            }
                        }
                    });
                }
            }
        }
        
        // News Loading with Pagination (NO INFINITE SCROLL!)
        function loadNews(page = 1) {
            fetch(`/api/news?page=${page}&limit=10`)
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('news-container');
                    container.innerHTML = data.items.map(item => `
                        <div class="glass-card mb-4">
                            <h4 class="font-medium mb-2">${item.title}</h4>
                            <p class="text-secondary mb-2">${item.summary}</p>
                            <div class="flex justify-between items-center">
                                <span class="text-sm px-2 py-1 rounded bg-${item.sentiment === 'positive' ? 'success' : item.sentiment === 'negative' ? 'error' : 'secondary'}">${item.sentiment}</span>
                                <span class="text-sm text-secondary">${item.timestamp}</span>
                            </div>
                        </div>
                    `).join('');
                    
                    // Update pagination
                    updatePagination(page, data.total_pages, 'news');
                })
                .catch(error => {
                    console.error('Error loading news:', error);
                    document.getElementById('news-container').innerHTML = '<p class="text-error">Failed to load news.</p>';
                });
        }
        
        // Pagination Helper (REPLACES INFINITE SCROLL)
        function updatePagination(currentPage, totalPages, context) {
            const container = document.getElementById(`${context}-pagination`);
            let paginationHTML = '';
            
            if (totalPages > 1) {
                paginationHTML = '<div class="flex gap-2">';
                
                // Previous button
                if (currentPage > 1) {
                    paginationHTML += `<button onclick="loadNews(${currentPage - 1})" class="pagination-btn">Previous</button>`;
                }
                
                // Page numbers
                for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
                    const activeClass = i === currentPage ? 'active' : '';
                    paginationHTML += `<button onclick="loadNews(${i})" class="pagination-btn ${activeClass}">${i}</button>`;
                }
                
                // Next button
                if (currentPage < totalPages) {
                    paginationHTML += `<button onclick="loadNews(${currentPage + 1})" class="pagination-btn">Next</button>`;
                }
                
                paginationHTML += '</div>';
            }
            
            container.innerHTML = paginationHTML;
        }
        
        // Video Metadata Extractor Functions
        function toggleMediaInput(type) {
            document.querySelectorAll('.media-toggle-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.url-input-container, .file-input-container').forEach(container => container.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(`${type}-input`).classList.add('active');
        }
        
        function extractFromURL() {
            const url = document.getElementById('video-url').value;
            if (!url) return;
            
            showLoader('Extracting metadata from URL...');
            
            fetch('/api/media/extract-url', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'url': url})
            })
            .then(response => response.json())
            .then(data => {
                hideLoader();
                displayMetadata(data);
            })
            .catch(error => {
                hideLoader();
                showError('Failed to extract metadata: ' + error.message);
            });
        }
        
        function extractFromFile(input) {
            const file = input.files[0];
            if (!file) return;
            
            showLoader('Extracting metadata from file...');
            
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/api/media/extract', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                hideLoader();
                displayMetadata(data);
            })
            .catch(error => {
                hideLoader();
                showError('Failed to extract metadata: ' + error.message);
            });
        }
        
        function displayMetadata(data) {
            const container = document.getElementById('metadata-result');
            container.style.display = 'block';
            container.innerHTML = `
                <div class="glass-card mt-4">
                    <h4 class="font-medium mb-4">Video Metadata</h4>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="text-sm font-medium">Title:</label>
                            <p class="text-secondary">${data.title || 'N/A'}</p>
                        </div>
                        <div>
                            <label class="text-sm font-medium">Duration:</label>
                            <p class="text-secondary">${data.duration || 'N/A'}</p>
                        </div>
                        <div>
                            <label class="text-sm font-medium">Format:</label>
                            <p class="text-secondary">${data.format || 'N/A'}</p>
                        </div>
                        <div>
                            <label class="text-sm font-medium">Size:</label>
                            <p class="text-secondary">${data.size || 'N/A'}</p>
                        </div>
                        <div>
                            <label class="text-sm font-medium">Resolution:</label>
                            <p class="text-secondary">${data.resolution || 'N/A'}</p>
                        </div>
                        <div>
                            <label class="text-sm font-medium">Quality:</label>
                            <p class="text-secondary">${data.quality || 'N/A'}</p>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Utility Functions
        function showLoader(message) {
            console.log('Loading:', message);
            // Could add actual loading UI here
        }
        
        function hideLoader() {
            console.log('Loading complete');
        }
        
        function showError(message) {
            alert('Error: ' + message);
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize overview charts by default
            initializeOverviewCharts();
            
            // Load news data for the news tab
            loadNews(1);
            
            // Add resize event listener with debouncing to prevent chart recreation
            let resizeTimeout;
            window.addEventListener('resize', function() {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    // Only update chart scales, don't recreate charts
                    Object.values(chartInstances).forEach(chart => {
                        if (chart && chart.update) {
                            chart.update('none'); // Update without animation
                        }
                    });
                }, 250);
            });
        });
        </script>
    </body>
    </html>
    """
    
    return html_template

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
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            
            # Extract metadata from file
            metadata = extract_video_metadata(tmp_file.name)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text_route():
    """Analyze text sentiment with enhanced features"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Use NLP engine for analysis
        result = nlp_engine.analyze_sentiment(text)
        
        # Add timestamp and enhanced metadata
        result['timestamp'] = datetime.now().isoformat()
        result['text_length'] = len(text)
        result['word_count'] = len(text.split())
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get enhanced dashboard statistics"""
    try:
        stats = db_manager.get_dashboard_summary()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Enhanced health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'environment': Config.ENVIRONMENT
    })

@app.route('/api/word-cloud')
def get_word_cloud_data():
    """Get data for word cloud visualization"""
    try:
        # Sample word cloud data
        words = [
            {"text": "AI", "size": 40}, {"text": "Python", "size": 30},
            {"text": "Data", "size": 25}, {"text": "Sentiment", "size": 35},
            {"text": "Flask", "size": 20}, {"text": "JavaScript", "size": 28},
            {"text": "Cloud", "size": 18}, {"text": "API", "size": 22},
            {"text": "Real-time", "size": 26}, {"text": "Dashboard", "size": 32},
            {"text": "Analytics", "size": 29}, {"text": "Machine Learning", "size": 24}
        ]
        return jsonify(words)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5003)))
