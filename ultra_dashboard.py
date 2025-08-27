"""
Ultra Modern React-Level Dashboard with Free APIs & Font Awesome Icons
Professional grade UI that rivals the best React applications
"""

from flask import Flask, render_template, request, jsonify
import json
import requests
import random
from datetime import datetime
from nlp_engine import NLPEngine

app = Flask(__name__)
app.secret_key = "ultra_sentiment_2025"

# Initialize NLP engine
nlp_engine = NLPEngine()

# Free API configurations
FREE_APIS = {
    "news": {
        "newsapi": "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo",
        "guardian": "https://content.guardianapis.com/search?api-key=test"
    },
    "quotes": "https://api.quotable.io/random",
    "weather": "https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo",
    "crypto": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd",
    "cat_facts": "https://catfact.ninja/fact",
    "jokes": "https://official-joke-api.appspot.com/random_joke",
    "advice": "https://api.adviceslip.com/advice"
}

@app.route('/')
def ultra_dashboard():
    """Ultra modern React-level dashboard"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultra Sentiment Analysis Platform</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Particles.js -->
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    
    <style>
        :root {
            --primary: #6366f1;
            --primary-light: #8b5cf6;
            --primary-dark: #4f46e5;
            --secondary: #06b6d4;
            --accent: #f59e0b;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --dark: #0f172a;
            --dark-light: #1e293b;
            --gray: #64748b;
            --gray-light: #f1f5f9;
            --white: #ffffff;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-lg: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }
        
        .app-container {
            display: flex;
            min-height: 100vh;
        }
        
        /* Sidebar */
        .sidebar {
            width: 280px;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--glass-border);
            padding: 2rem;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow);
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--glass-border);
        }
        
        .logo i {
            font-size: 2rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .logo h1 {
            font-weight: 800;
            font-size: 1.5rem;
            color: var(--white);
        }
        
        .nav-menu {
            list-style: none;
        }
        
        .nav-item {
            margin-bottom: 0.5rem;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .nav-link:hover, .nav-link.active {
            background: var(--glass);
            color: var(--white);
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }
        
        .nav-link i {
            font-size: 1.2rem;
            width: 20px;
            text-align: center;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            margin-left: 280px;
            padding: 2rem;
        }
        
        .header {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }
        
        .header-top {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .header h2 {
            color: var(--white);
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: var(--white);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--white);
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .stat-change {
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
        }
        
        .stat-change.positive {
            background: rgba(16, 185, 129, 0.2);
            color: var(--success);
        }
        
        .stat-change.negative {
            background: rgba(239, 68, 68, 0.2);
            color: var(--error);
        }
        
        /* Tabs */
        .tabs-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow);
        }
        
        .tabs-nav {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            background: rgba(255, 255, 255, 0.05);
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .tab-btn {
            flex: 1;
            padding: 1rem 2rem;
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .tab-btn.active {
            background: var(--primary);
            color: var(--white);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }
        
        .tab-content {
            display: none;
            animation: fadeInUp 0.5s ease;
        }
        
        .tab-content.active {
            display: block;
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
        
        /* Form Elements */
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            display: block;
            color: var(--white);
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        
        .form-control {
            width: 100%;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: var(--white);
            font-size: 1rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
        }
        
        .form-control::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        
        /* Buttons */
        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1rem;
            text-decoration: none;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: var(--white);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, var(--gray), var(--dark-light));
            color: var(--white);
        }
        
        .btn-success {
            background: linear-gradient(135deg, var(--success), #059669);
            color: var(--white);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, var(--warning), #d97706);
            color: var(--white);
        }
        
        /* Results */
        .results-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: var(--shadow);
        }
        
        .results-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .results-header h3 {
            color: var(--white);
            font-size: 1.5rem;
            font-weight: 700;
        }
        
        .json-viewer {
            background: var(--dark);
            border: 1px solid var(--dark-light);
            border-radius: 12px;
            padding: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            color: #e2e8f0;
            font-size: 0.9rem;
            line-height: 1.6;
            max-height: 500px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        
        /* Charts */
        .chart-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* Loading States */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 3rem;
            color: var(--white);
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .sidebar {
                transform: translateX(-100%);
            }
            
            .main-content {
                margin-left: 0;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
        }
        
        @media (max-width: 768px) {
            .header h2 {
                font-size: 2rem;
            }
            
            .tabs-nav {
                flex-direction: column;
            }
            
            .tab-btn {
                justify-content: flex-start;
            }
        }
        
        /* API Data Cards */
        .api-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .api-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }
        
        .api-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .api-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: var(--white);
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .floating {
            animation: floating 3s ease-in-out infinite;
        }
        
        @keyframes floating {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <i class="fas fa-brain"></i>
                <h1>SentimentAI</h1>
            </div>
            
            <nav>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a href="#" class="nav-link active" onclick="switchTab('dashboard')">
                            <i class="fas fa-chart-line"></i>
                            Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('analysis')">
                            <i class="fas fa-microscope"></i>
                            Analysis
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('links')">
                            <i class="fas fa-link"></i>
                            Link Analysis
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('bulk')">
                            <i class="fas fa-layer-group"></i>
                            Bulk Processing
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('apis')">
                            <i class="fas fa-database"></i>
                            Live Data
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('insights')">
                            <i class="fas fa-lightbulb"></i>
                            Insights
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link" onclick="switchTab('settings')">
                            <i class="fas fa-cog"></i>
                            Settings
                        </a>
                    </li>
                </ul>
            </nav>
        </aside>
        
        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="header">
                <div class="header-top">
                    <div>
                        <h2 class="floating">Ultra Sentiment Platform</h2>
                        <p>Advanced AI-powered content analysis with real-time insights</p>
                    </div>
                </div>
            </header>
            
            <!-- Stats Grid -->
            <div class="stats-grid" id="stats-grid">
                <div class="stat-card pulse">
                    <div class="stat-header">
                        <div class="stat-icon" style="background: linear-gradient(135deg, var(--primary), var(--primary-light));">
                            <i class="fas fa-chart-bar"></i>
                        </div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> +12%
                        </div>
                    </div>
                    <div class="stat-number" id="total-analyzed">0</div>
                    <div class="stat-label">Total Analyzed</div>
                </div>
                
                <div class="stat-card pulse">
                    <div class="stat-header">
                        <div class="stat-icon" style="background: linear-gradient(135deg, var(--success), #059669);">
                            <i class="fas fa-smile"></i>
                        </div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> +8%
                        </div>
                    </div>
                    <div class="stat-number" id="positive-sentiment">0%</div>
                    <div class="stat-label">Positive Sentiment</div>
                </div>
                
                <div class="stat-card pulse">
                    <div class="stat-header">
                        <div class="stat-icon" style="background: linear-gradient(135deg, var(--secondary), #0891b2);">
                            <i class="fas fa-link"></i>
                        </div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> +25%
                        </div>
                    </div>
                    <div class="stat-number" id="links-processed">0</div>
                    <div class="stat-label">Links Processed</div>
                </div>
                
                <div class="stat-card pulse">
                    <div class="stat-header">
                        <div class="stat-icon" style="background: linear-gradient(135deg, var(--warning), #d97706);">
                            <i class="fas fa-rocket"></i>
                        </div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> +18%
                        </div>
                    </div>
                    <div class="stat-number" id="processing-speed">98%</div>
                    <div class="stat-label">Processing Speed</div>
                </div>
            </div>
            
            <!-- Main Tabs Container -->
            <div class="tabs-container">
                <!-- Dashboard Tab -->
                <div id="dashboard-content" class="tab-content active">
                    <div class="chart-container">
                        <canvas id="sentimentChart" width="400" height="200"></canvas>
                    </div>
                    
                    <div class="api-card">
                        <div class="api-header">
                            <div class="api-icon" style="background: linear-gradient(135deg, var(--primary), var(--secondary));">
                                <i class="fas fa-chart-pie"></i>
                            </div>
                            <h3 style="color: var(--white);">Real-time Analytics</h3>
                        </div>
                        <p style="color: rgba(255, 255, 255, 0.8);">Live sentiment tracking across multiple platforms with AI-powered insights.</p>
                    </div>
                </div>
                
                <!-- Analysis Tab -->
                <div id="analysis-content" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-file-text"></i> Content Title
                        </label>
                        <input type="text" class="form-control" id="content-title" placeholder="Enter your content title...">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-align-left"></i> Description
                        </label>
                        <textarea class="form-control" id="content-description" rows="4" placeholder="Enter content description..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-comments"></i> Comments (one per line)
                        </label>
                        <textarea class="form-control" id="content-comments" rows="6" placeholder="Enter comments..."></textarea>
                    </div>
                    
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <button class="btn btn-primary" onclick="analyzeContent()">
                            <i class="fas fa-play"></i> Analyze Content
                        </button>
                        <button class="btn btn-success" onclick="loadSampleData()">
                            <i class="fas fa-magic"></i> Load Sample
                        </button>
                        <button class="btn btn-secondary" onclick="clearForm()">
                            <i class="fas fa-trash"></i> Clear
                        </button>
                    </div>
                </div>
                
                <!-- Links Tab -->
                <div id="links-content" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-globe"></i> URL to Analyze
                        </label>
                        <input type="url" class="form-control" id="url-input" placeholder="https://www.youtube.com/watch?v=...">
                    </div>
                    
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem;">
                        <button class="btn btn-primary" onclick="analyzeUrl()">
                            <i class="fas fa-search"></i> Analyze URL
                        </button>
                        <button class="btn btn-success" onclick="loadSampleUrl()">
                            <i class="fas fa-link"></i> Sample URL
                        </button>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-file-alt"></i> Text with Embedded URLs
                        </label>
                        <textarea class="form-control" id="text-with-urls" rows="6" placeholder="Paste text containing URLs..."></textarea>
                    </div>
                    
                    <button class="btn btn-warning" onclick="extractAndAnalyze()">
                        <i class="fas fa-magic"></i> Auto-Extract & Analyze
                    </button>
                </div>
                
                <!-- Bulk Tab -->
                <div id="bulk-content" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-list"></i> Multiple URLs (one per line)
                        </label>
                        <textarea class="form-control" id="bulk-urls" rows="8" placeholder="https://www.youtube.com/watch?v=example1&#10;https://twitter.com/user/status/example2&#10;https://www.instagram.com/p/example3/"></textarea>
                    </div>
                    
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <button class="btn btn-primary" onclick="bulkAnalyze()">
                            <i class="fas fa-rocket"></i> Bulk Analyze
                        </button>
                        <button class="btn btn-success" onclick="loadBulkSample()">
                            <i class="fas fa-list-ul"></i> Load Samples
                        </button>
                    </div>
                </div>
                
                <!-- APIs Tab -->
                <div id="apis-content" class="tab-content">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                        <div class="api-card" onclick="fetchApiData('quotes')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--primary), var(--primary-light));">
                                    <i class="fas fa-quote-left"></i>
                                </div>
                                <h4 style="color: var(--white);">Inspirational Quotes</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Get random motivational quotes and analyze their sentiment</p>
                        </div>
                        
                        <div class="api-card" onclick="fetchApiData('crypto')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--warning), #d97706);">
                                    <i class="fab fa-bitcoin"></i>
                                </div>
                                <h4 style="color: var(--white);">Crypto Prices</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Live cryptocurrency prices from CoinGecko</p>
                        </div>
                        
                        <div class="api-card" onclick="fetchApiData('cat_facts')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--secondary), #0891b2);">
                                    <i class="fas fa-cat"></i>
                                </div>
                                <h4 style="color: var(--white);">Cat Facts</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Random cat facts for sentiment analysis</p>
                        </div>
                        
                        <div class="api-card" onclick="fetchApiData('jokes')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--success), #059669);">
                                    <i class="fas fa-laugh"></i>
                                </div>
                                <h4 style="color: var(--white);">Random Jokes</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Funny jokes to analyze humor sentiment</p>
                        </div>
                        
                        <div class="api-card" onclick="fetchApiData('advice')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--error), #dc2626);">
                                    <i class="fas fa-lightbulb"></i>
                                </div>
                                <h4 style="color: var(--white);">Life Advice</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Random life advice for analysis</p>
                        </div>
                    </div>
                </div>
                
                <!-- Insights Tab -->
                <div id="insights-content" class="tab-content">
                    <div class="chart-container">
                        <canvas id="insightsChart" width="400" height="200"></canvas>
                    </div>
                    
                    <div id="insights-data"></div>
                </div>
                
                <!-- Settings Tab -->
                <div id="settings-content" class="tab-content">
                    <div class="api-card">
                        <div class="api-header">
                            <div class="api-icon" style="background: linear-gradient(135deg, var(--gray), var(--dark-light));">
                                <i class="fas fa-sliders-h"></i>
                            </div>
                            <h4 style="color: var(--white);">Analysis Settings</h4>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Sentiment Threshold</label>
                            <input type="range" class="form-control" min="0" max="1" step="0.1" value="0.5">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Language Detection</label>
                            <select class="form-control">
                                <option>Auto-detect</option>
                                <option>English</option>
                                <option>Swahili</option>
                                <option>French</option>
                            </select>
                        </div>
                        
                        <button class="btn btn-primary">
                            <i class="fas fa-save"></i> Save Settings
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Results Container -->
            <div id="results-container" class="results-container" style="display: none;">
                <div class="results-header">
                    <i class="fas fa-chart-bar"></i>
                    <h3>Analysis Results</h3>
                </div>
                <div id="results-stats"></div>
                <div id="results-json" class="json-viewer"></div>
            </div>
        </main>
    </div>

    <script>
        // Initialize particles
        particlesJS('particles-js', {
            particles: {
                number: { value: 50, density: { enable: true, value_area: 800 } },
                color: { value: '#ffffff' },
                shape: { type: 'circle' },
                opacity: { value: 0.1, random: false },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 150, color: '#ffffff', opacity: 0.1, width: 1 },
                move: { enable: true, speed: 1, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
            },
            interactivity: {
                detect_on: 'canvas',
                events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
                modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
            },
            retina_detect: true
        });

        // Global variables
        let analysisCount = 0;
        let positiveCount = 0;
        let linksProcessed = 0;
        let sentimentChart;
        let insightsChart;

        // Initialize charts
        function initCharts() {
            // Sentiment Chart
            const ctx1 = document.getElementById('sentimentChart').getContext('2d');
            sentimentChart = new Chart(ctx1, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{
                        data: [45, 25, 30],
                        backgroundColor: ['#10b981', '#ef4444', '#6b7280'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#ffffff' } }
                    }
                }
            });

            // Insights Chart
            const ctx2 = document.getElementById('insightsChart').getContext('2d');
            insightsChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Sentiment Trend',
                        data: [65, 59, 80, 81, 56, 75],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#ffffff' } }
                    },
                    scales: {
                        y: { ticks: { color: '#ffffff' } },
                        x: { ticks: { color: '#ffffff' } }
                    }
                }
            });
        }

        // Tab switching
        function switchTab(tabName) {
            // Update nav
            document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
            event.target.classList.add('active');

            // Update content
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById(tabName + '-content').classList.add('active');

            if (tabName === 'dashboard' || tabName === 'insights') {
                setTimeout(initCharts, 100);
            }
        }

        // Update stats
        function updateStats() {
            document.getElementById('total-analyzed').textContent = analysisCount;
            document.getElementById('positive-sentiment').textContent = 
                analysisCount > 0 ? Math.round((positiveCount / analysisCount) * 100) + '%' : '0%';
            document.getElementById('links-processed').textContent = linksProcessed;
        }

        // Analysis functions
        function analyzeContent() {
            const title = document.getElementById('content-title').value;
            const description = document.getElementById('content-description').value;
            const comments = document.getElementById('content-comments').value.split('\\n').filter(c => c.trim());

            if (!title && !description && !comments.length) {
                alert('Please enter some content!');
                return;
            }

            showLoading('Analyzing content...');

            fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    video_title: title,
                    video_description: description,
                    comments: comments
                })
            })
            .then(r => r.json())
            .then(data => {
                analysisCount++;
                if (data.video_sentiment === 'positive') positiveCount++;
                updateStats();
                showResults(data);
            })
            .catch(e => showError('Analysis failed: ' + e.message));
        }

        function analyzeUrl() {
            const url = document.getElementById('url-input').value;
            if (!url) {
                alert('Please enter a URL!');
                return;
            }

            showLoading('Extracting content from URL...');

            fetch('/api/analyze-url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            })
            .then(r => r.json())
            .then(data => {
                analysisCount++;
                linksProcessed++;
                if (data.video_sentiment === 'positive') positiveCount++;
                updateStats();
                showResults(data);
            })
            .catch(e => showError('URL analysis failed: ' + e.message));
        }

        function extractAndAnalyze() {
            const text = document.getElementById('text-with-urls').value;
            if (!text) {
                alert('Please enter some text!');
                return;
            }

            showLoading('Extracting URLs and analyzing...');

            fetch('/api/analyze-text-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(r => r.json())
            .then(data => {
                analysisCount++;
                linksProcessed += data.urls_found || 0;
                updateStats();
                showResults(data);
            })
            .catch(e => showError('Text analysis failed: ' + e.message));
        }

        function bulkAnalyze() {
            const urls = document.getElementById('bulk-urls').value.split('\\n').filter(u => u.trim());
            if (!urls.length) {
                alert('Please enter some URLs!');
                return;
            }

            showLoading(`Analyzing ${urls.length} URLs...`);

            fetch('/api/analyze-bulk-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: urls })
            })
            .then(r => r.json())
            .then(data => {
                analysisCount += urls.length;
                linksProcessed += urls.length;
                updateStats();
                showResults(data);
            })
            .catch(e => showError('Bulk analysis failed: ' + e.message));
        }

        // API data fetching
        function fetchApiData(apiType) {
            showLoading(`Fetching ${apiType} data...`);

            fetch(`/api/fetch-data/${apiType}`)
                .then(r => r.json())
                .then(data => {
                    analysisCount++;
                    updateStats();
                    showResults(data);
                })
                .catch(e => showError(`Failed to fetch ${apiType} data: ` + e.message));
        }

        // Utility functions
        function showLoading(message) {
            const container = document.getElementById('results-container');
            container.style.display = 'block';
            container.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <span>${message}</span>
                </div>
            `;
        }

        function showResults(data) {
            const container = document.getElementById('results-container');
            container.style.display = 'block';
            container.innerHTML = `
                <div class="results-header">
                    <i class="fas fa-chart-bar"></i>
                    <h3>Analysis Results</h3>
                </div>
                <div id="results-stats">${generateStatsHtml(data)}</div>
                <div id="results-json" class="json-viewer">${JSON.stringify(data, null, 2)}</div>
            `;
        }

        function showError(message) {
            const container = document.getElementById('results-container');
            container.style.display = 'block';
            container.innerHTML = `
                <div style="color: var(--error); text-align: center; padding: 2rem;">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>${message}</p>
                </div>
            `;
        }

        function generateStatsHtml(data) {
            return `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    <div class="api-card">
                        <div class="api-header">
                            <div class="api-icon" style="background: var(--success);">
                                <i class="fas fa-thumbs-up"></i>
                            </div>
                            <h4 style="color: var(--white);">Sentiment</h4>
                        </div>
                        <p style="color: var(--white); font-size: 1.2rem; font-weight: bold;">
                            ${data.video_sentiment || 'N/A'}
                        </p>
                    </div>
                    <div class="api-card">
                        <div class="api-header">
                            <div class="api-icon" style="background: var(--primary);">
                                <i class="fas fa-comments"></i>
                            </div>
                            <h4 style="color: var(--white);">Comments</h4>
                        </div>
                        <p style="color: var(--white); font-size: 1.2rem; font-weight: bold;">
                            ${(data.comments || []).length}
                        </p>
                    </div>
                </div>
            `;
        }

        // Sample data functions
        function loadSampleData() {
            document.getElementById('content-title').value = 'Epic AI Tutorial - Machine Learning in 2025';
            document.getElementById('content-description').value = 'Complete guide to building AI applications with modern tools';
            document.getElementById('content-comments').value = 'This is amazing! Great tutorial\\nThanks for sharing this\\nVery helpful content\\nLove the explanations';
        }

        function loadSampleUrl() {
            document.getElementById('url-input').value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
        }

        function loadBulkSample() {
            document.getElementById('bulk-urls').value = 'https://www.youtube.com/watch?v=example1\\nhttps://twitter.com/user/status/example2\\nhttps://www.instagram.com/p/example3/';
        }

        function clearForm() {
            document.getElementById('content-title').value = '';
            document.getElementById('content-description').value = '';
            document.getElementById('content-comments').value = '';
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            updateStats();
        });
    </script>
</body>
</html>"""

# Add new API endpoints for free data
@app.route('/api/fetch-data/<data_type>')
def fetch_free_data(data_type):
    """Fetch data from free APIs"""
    try:
        data = {}
        
        if data_type == 'quotes':
            response = requests.get("https://api.quotable.io/random")
            if response.status_code == 200:
                quote_data = response.json()
                text = f"{quote_data['content']} - {quote_data['author']}"
                data = nlp_engine.analyze_video_data("Inspirational Quote", text, [])
                data['api_source'] = 'quotable.io'
                data['original_data'] = quote_data
        
        elif data_type == 'crypto':
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
            if response.status_code == 200:
                crypto_data = response.json()
                text = f"Bitcoin price: ${crypto_data['bitcoin']['usd']}, Ethereum price: ${crypto_data['ethereum']['usd']}"
                data = nlp_engine.analyze_video_data("Crypto Prices", text, [])
                data['api_source'] = 'coingecko.com'
                data['original_data'] = crypto_data
        
        elif data_type == 'cat_facts':
            response = requests.get("https://catfact.ninja/fact")
            if response.status_code == 200:
                fact_data = response.json()
                text = fact_data['fact']
                data = nlp_engine.analyze_video_data("Cat Fact", text, [])
                data['api_source'] = 'catfact.ninja'
                data['original_data'] = fact_data
        
        elif data_type == 'jokes':
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            if response.status_code == 200:
                joke_data = response.json()
                text = f"{joke_data['setup']} {joke_data['punchline']}"
                data = nlp_engine.analyze_video_data("Random Joke", text, [])
                data['api_source'] = 'official-joke-api'
                data['original_data'] = joke_data
        
        elif data_type == 'advice':
            response = requests.get("https://api.adviceslip.com/advice")
            if response.status_code == 200:
                advice_data = response.json()
                text = advice_data['slip']['advice']
                data = nlp_engine.analyze_video_data("Life Advice", text, [])
                data['api_source'] = 'adviceslip.com'
                data['original_data'] = advice_data
        
        else:
            return jsonify({"error": "Unknown data type"}), 400
        
        data['metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'data_type': data_type,
            'analysis_engine': 'Ultra NLP Engine v3.0'
        }
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep existing API endpoints
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Regular content analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        video_title = data.get('video_title', '')
        video_description = data.get('video_description', '')
        comments = data.get('comments', [])
        
        result = nlp_engine.analyze_video_data(video_title, video_description, comments)
        
        result['metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'total_comments': len(comments),
            'analysis_engine': 'Ultra NLP Engine v3.0'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-url', methods=['POST'])
def api_analyze_url():
    """Analyze content from a URL"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        result = nlp_engine.analyze_url(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-text-urls', methods=['POST'])
def api_analyze_text_urls():
    """Analyze text with embedded URLs"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = nlp_engine.analyze_text_with_urls(text, analyze_embedded_urls=True)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-bulk-urls', methods=['POST'])
def api_analyze_bulk_urls():
    """Bulk analyze multiple URLs"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({"error": "No URLs provided"}), 400
        
        result = nlp_engine.analyze_multiple_urls(urls)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Ultra Sentiment Analysis Platform",
        "features": ["basic_analysis", "link_analysis", "bulk_analysis", "free_apis", "real_time_insights"],
        "version": "3.0",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Ultra Modern Sentiment Analysis Platform...")
    print("📊 Loading React-level UI with Font Awesome icons...")
    print("🔗 Integrating free APIs for diverse data sources...")
    print("✨ Professional grade interface activated...")
    print("=" * 60)
    print(f"🌐 Ultra Dashboard: http://localhost:5003")
    print(f"🔗 Link Analysis: http://localhost:5003/api/analyze-url")
    print(f"📊 Bulk Analysis: http://localhost:5003/api/analyze-bulk-urls")
    print(f"🤖 Auto-Extract: http://localhost:5003/api/analyze-text-urls")
    print(f"📡 Free APIs: http://localhost:5003/api/fetch-data/quotes")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=5003, debug=True, threaded=True)
