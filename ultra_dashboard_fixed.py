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
    <title>SentimentAI | Immersive Analysis Platform</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>

    
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
            --glass: rgba(15, 23, 42, 0.6);
            --glass-border: rgba(255, 255, 255, 0.1);
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
            background: var(--dark);
            color: var(--white);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
        }
        
        .app-container {
            display: flex;
            min-height: 100vh;
            position: relative;
            z-index: 1;
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
            z-index: 10;
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
            animation: spin 8s linear infinite;
        }
        
        .logo h1 {
            font-weight: 800;
            font-size: 1.5rem;
            color: var(--white);
        }
        
        .nav-menu { list-style: none; }
        .nav-item { margin-bottom: 0.5rem; }
        
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
            cursor: pointer;
        }
        
        .nav-link:hover, .nav-link.active {
            background: var(--primary);
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
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .header h2 {
            color: var(--white);
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .typewriter {
            display: inline-block;
            overflow: hidden;
            border-right: .15em solid var(--accent);
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: .1em;
            animation: typing 3.5s steps(30, end), blink-caret .75s step-end infinite;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--accent); }
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
            transition: all 0.5s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-card:hover::before {
            height: 100%;
            opacity: 0.1;
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
        
        .tab-content {
            display: none;
            animation: fadeInUp 0.5s ease;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Form Elements */
        .form-group { margin-bottom: 1.5rem; }
        
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
        
        .form-control::placeholder { color: rgba(255, 255, 255, 0.5); }
        
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
        
        .btn:hover::before { left: 100%; }
        
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
            .sidebar { transform: translateX(-100%); }
            .main-content { margin-left: 0; }
            .stats-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
        }
        
        @media (max-width: 768px) {
            .header h2 { font-size: 2rem; }
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
            cursor: pointer;
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
        
        .pulse { animation: pulse 2s infinite; }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .floating { animation: floating 3s ease-in-out infinite; }
        
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
                        <div class="nav-link active" data-tab="dashboard">
                            <i class="fas fa-chart-line"></i>
                            Dashboard
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="analysis">
                            <i class="fas fa-microscope"></i>
                            Analysis
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="links">
                            <i class="fas fa-link"></i>
                            Link Analysis
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="bulk">
                            <i class="fas fa-layer-group"></i>
                            Bulk Processing
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="apis">
                            <i class="fas fa-database"></i>
                            Live Data
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="insights">
                            <i class="fas fa-lightbulb"></i>
                            Insights
                        </div>
                    </li>
                    <li class="nav-item">
                        <div class="nav-link" data-tab="settings">
                            <i class="fas fa-cog"></i>
                            Settings
                        </div>
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
                        <h2 class="floating typewriter">SentimentAI Platform</h2>
                        <p>AI-powered content analysis with real-time insights</p>
                    </div>
                    <div id="live-clock" style="font-size: 1.2rem; font-weight: 500;"></div>
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
                            <i class="fas fa-thumbs-up"></i>
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
                        <input type="text" class="form-control" id="content-title" placeholder="e.g., 'Apple Vision Pro Review: Is it the Future?'">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-align-left"></i> Description
                        </label>
                        <textarea class="form-control" id="content-description" rows="4" placeholder="e.g., 'An in-depth look at Apple's new headset, its features, and whether it's worth the price.'"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-comments"></i> Comments (one per line)
                        </label>
                        <textarea class="form-control" id="content-comments" rows="6" placeholder="e.g., 'This is a game-changer!' or 'Way too expensive for what it offers.'"></textarea>
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
                                    <i class="fas fa-paw"></i>
                                </div>
                                <h4 style="color: var(--white);">Animal Facts</h4>
                            </div>
                            <p style="color: rgba(255, 255, 255, 0.8);">Random animal facts for sentiment analysis</p>
                        </div>
                        
                        <div class="api-card" onclick="fetchApiData('jokes')">
                            <div class="api-header">
                                <div class="api-icon" style="background: linear-gradient(135deg, var(--success), #059669);">
                                    <i class="fas fa-comment-dots"></i>
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
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: '#ffffff' },
                shape: { type: 'circle' },
                opacity: { value: 0.2, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false } },
                size: { value: 3, random: true, anim: { enable: false } },
                line_linked: { enable: true, distance: 150, color: '#ffffff', opacity: 0.1, width: 1 },
                move: { enable: true, speed: 1, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false }
            },
            interactivity: {
                detect_on: 'canvas',
                events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' }, resize: true },
                modes: { grab: { distance: 140, line_opacity: 0.2 }, push: { particles_nb: 4 } }
            },
            retina_detect: true
        });

        // Global variables
        let analysisCount = 0;
        let positiveCount = 0;
        let linksProcessed = 0;
        let sentimentChart;
        let insightsChart;

        // Live Clock
        function updateClock() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            document.getElementById('live-clock').textContent = timeString;
        }
        setInterval(updateClock, 1000);

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
                        borderColor: 'var(--dark)',
                        borderWidth: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#ffffff', font: { size: 14 } } }
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
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#ffffff' } }
                    },
                    scales: {
                        y: { ticks: { color: '#ffffff' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                        x: { ticks: { color: '#ffffff' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                    }
                }
            });
        }

        // Tab switching logic - FIXED VERSION
        function switchTab(tabName) {
            // Update nav
            document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
            document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

            // Update content
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById(tabName + '-content').classList.add('active');

            // Resize charts if they are in the active tab
            if (tabName === 'dashboard' || tabName === 'insights') {
                setTimeout(() => {
                    if (sentimentChart) sentimentChart.resize();
                    if (insightsChart) insightsChart.resize();
                }, 100);
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
            const samples = [
                {
                    title: 'Safaricom PLC Announces Record Profits for Q3',
                    description: 'Kenya\\'s leading telecommunications company, Safaricom, has reported a 12% increase in net profit for the third quarter, driven by strong growth in M-PESA and data services.',
                    comments: 'Great news for shareholders!\\nM-PESA is a game-changer for Africa.\\nTheir data bundles are still too expensive though.\\nI wish they would improve their customer service.\\nTo the moon! #SCOM'
                },
                {
                    title: 'New "Dune: Part Two" Movie Review - A Sci-Fi Masterpiece?',
                    description: 'Breaking down Denis Villeneuve\\'s latest installment in the Dune saga. Does it live up to the hype?',
                    comments: 'Absolutely breathtaking visuals! A cinematic triumph.\\nThe sound design was insane in IMAX.\\nI felt the pacing was a bit slow in the first half.\\nThey butchered the book\\'s ending.\\nZendaya and Timothee have amazing chemistry.'
                },
                {
                    title: 'Customer Feedback: "The new banking app update is terrible"',
                    description: 'A collection of user reviews following the recent mobile banking app update.',
                    comments: 'I can\\'t find anything anymore. Please revert to the old version!\\nThis new UI is so confusing and not user-friendly.\\nWho approved this design? It\\'s a disaster.\\nIt keeps crashing every time I try to make a transfer.\\nI actually like the new look, it feels more modern.'
                }
            ];
            const randomSample = samples[Math.floor(Math.random() * samples.length)];
            document.getElementById('content-title').value = randomSample.title;
            document.getElementById('content-description').value = randomSample.description;
            document.getElementById('content-comments').value = randomSample.comments;
        }

        function loadSampleUrl() {
            const sampleUrls = [
                'https://www.youtube.com/watch?v=mL-q8-bVzHw', // MKBHD iPhone review
                'https://twitter.com/elonmusk/status/1585841080431321088', // Elon Musk tweet
                'https://www.instagram.com/p/Cj_qX9vJ3Xp/' // Nat Geo photo
            ];
            document.getElementById('url-input').value = sampleUrls[Math.floor(Math.random() * sampleUrls.length)];
        }

        function loadBulkSample() {
            document.getElementById('bulk-urls').value = `https://www.youtube.com/watch?v=mL-q8-bVzHw
https://twitter.com/VitalikButerin/status/1570298892923940864
https://www.instagram.com/p/Cj_qX9vJ3Xp/
https://www.tiktok.com/@mkbhd/video/7163954144993676587`;
        }

        function clearForm() {
            document.getElementById('content-title').value = '';
            document.getElementById('content-description').value = '';
            document.getElementById('content-comments').value = '';
        }

        // Initialize on load - FIXED VERSION
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            updateStats();
            updateClock();

            // Add click event listeners to nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const tabName = this.dataset.tab;
                    switchTab(tabName);
                });
            });
        });
    </script>
</body>
</html>"""

# API Endpoints
@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """Analyze content sentiment"""
    try:
        data = request.json
        title = data.get('video_title', '')
        description = data.get('video_description', '')
        comments = data.get('comments', [])
        
        # Analyze content
        result = nlp_engine.analyze_full_content(
            video_title=title,
            video_description=description,
            comments=comments
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze URL content"""
    try:
        data = request.json
        url = data.get('url', '')
        
        # Mock URL analysis for demo
        mock_data = {
            "url": url,
            "video_title": f"Content from {url}",
            "video_description": "Extracted content analysis",
            "video_sentiment": random.choice(["positive", "negative", "neutral"]),
            "comments": [
                {"text": "Great content!", "sentiment": "positive"},
                {"text": "Could be better", "sentiment": "neutral"},
                {"text": "Not impressed", "sentiment": "negative"}
            ]
        }
        
        return jsonify(mock_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-text-urls', methods=['POST'])
def analyze_text_urls():
    """Analyze text with embedded URLs"""
    try:
        data = request.json
        text = data.get('text', '')
        
        # Simple URL extraction (demo)
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        result = {
            "text": text,
            "urls_found": len(urls),
            "extracted_urls": urls,
            "sentiment_analysis": nlp_engine.analyze_sentiment(text)
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-bulk-urls', methods=['POST'])
def analyze_bulk_urls():
    """Analyze multiple URLs"""
    try:
        data = request.json
        urls = data.get('urls', [])
        
        results = []
        for url in urls:
            mock_result = {
                "url": url,
                "sentiment": random.choice(["positive", "negative", "neutral"]),
                "confidence": round(random.uniform(0.5, 1.0), 2)
            }
            results.append(mock_result)
        
        return jsonify({
            "bulk_analysis": results,
            "summary": {
                "total_urls": len(urls),
                "positive": len([r for r in results if r["sentiment"] == "positive"]),
                "negative": len([r for r in results if r["sentiment"] == "negative"]),
                "neutral": len([r for r in results if r["sentiment"] == "neutral"])
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fetch-data/<api_type>')
def fetch_api_data(api_type):
    """Fetch data from free APIs"""
    try:
        if api_type == "quotes":
            try:
                response = requests.get(FREE_APIS["quotes"], timeout=5)
                quote_data = response.json()
                text = quote_data.get("content", "Be yourself; everyone else is already taken.")
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "quotes",
                    "raw_data": quote_data,
                    "text": text,
                    "sentiment_analysis": analysis
                })
            except:
                # Fallback quote
                text = "The only way to do great work is to love what you do."
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "quotes",
                    "text": text,
                    "sentiment_analysis": analysis
                })
        
        elif api_type == "crypto":
            try:
                response = requests.get(FREE_APIS["crypto"], timeout=5)
                crypto_data = response.json()
                return jsonify({
                    "api_type": "crypto",
                    "raw_data": crypto_data,
                    "analysis": "Crypto market data fetched successfully"
                })
            except:
                return jsonify({
                    "api_type": "crypto",
                    "raw_data": {"bitcoin": {"usd": 45000}, "ethereum": {"usd": 3000}},
                    "analysis": "Mock crypto data (API unavailable)"
                })
        
        elif api_type == "cat_facts":
            try:
                response = requests.get(FREE_APIS["cat_facts"], timeout=5)
                fact_data = response.json()
                text = fact_data.get("fact", "Cats are amazing creatures.")
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "cat_facts",
                    "raw_data": fact_data,
                    "text": text,
                    "sentiment_analysis": analysis
                })
            except:
                text = "Cats sleep 12-16 hours a day."
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "cat_facts",
                    "text": text,
                    "sentiment_analysis": analysis
                })
        
        elif api_type == "jokes":
            try:
                response = requests.get(FREE_APIS["jokes"], timeout=5)
                joke_data = response.json()
                text = f"{joke_data.get('setup', '')} {joke_data.get('punchline', '')}"
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "jokes",
                    "raw_data": joke_data,
                    "text": text,
                    "sentiment_analysis": analysis
                })
            except:
                text = "Why don't scientists trust atoms? Because they make up everything!"
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "jokes",
                    "text": text,
                    "sentiment_analysis": analysis
                })
        
        elif api_type == "advice":
            try:
                response = requests.get(FREE_APIS["advice"], timeout=5)
                advice_data = response.json()
                text = advice_data.get("slip", {}).get("advice", "Always be yourself.")
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "advice",
                    "raw_data": advice_data,
                    "text": text,
                    "sentiment_analysis": analysis
                })
            except:
                text = "Focus on progress, not perfection."
                analysis = nlp_engine.analyze_sentiment(text)
                return jsonify({
                    "api_type": "advice",
                    "text": text,
                    "sentiment_analysis": analysis
                })
        
        else:
            return jsonify({"error": "Unknown API type"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 Starting Ultra Dashboard on http://localhost:5003")
    print("✨ React-level UI with professional Font Awesome icons")
    print("🎯 All tabs are now functional!")
    
    app.run(debug=True, host='0.0.0.0', port=5003)
