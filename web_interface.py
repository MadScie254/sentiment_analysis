"""
Epic web interface for testing the sentiment analysis system
Now with link analysis capabilities and immersive demo dashboard
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

# Import our NLP engine with link analysis
from nlp_engine import NLPEngine

app = Flask(__name__)
app.secret_key = "sentiment_test_2025_epic"

# Initialize NLP engine
nlp_engine = NLPEngine()

@app.route('/')
def home():
    """Epic main testing interface with link analysis"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Epic Sentiment Analysis - Link & Content Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            animation: backgroundShift 10s ease-in-out infinite alternate;
        }
        
        @keyframes backgroundShift {
            0% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            50% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            100% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        }
        
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 3rem; 
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255,255,255,0.1) 10px,
                rgba(255,255,255,0.1) 20px
            );
            animation: headerPattern 20s linear infinite;
        }
        
        @keyframes headerPattern {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .header h1 { 
            margin-bottom: 0.5rem; 
            font-size: 3rem; 
            position: relative; 
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p { 
            opacity: 0.9; 
            font-size: 1.3rem; 
            position: relative; 
            z-index: 1;
        }
        
        .content { padding: 2rem; }
        
        .demo-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 0.5rem;
        }
        
        .tab-button {
            padding: 1rem 2rem;
            border: none;
            background: transparent;
            cursor: pointer;
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.3s;
            margin: 0 0.25rem;
        }
        
        .tab-button.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .tab-content {
            display: none;
            animation: fadeIn 0.5s ease-in;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .demo-section { 
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
            border-radius: 15px; 
            padding: 2rem; 
            margin: 1rem 0; 
            border-left: 5px solid #667eea;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .epic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .input-group { margin: 1rem 0; }
        .input-group label { 
            display: block; 
            font-weight: bold; 
            margin-bottom: 0.5rem; 
            color: #333;
            font-size: 1.1rem;
        }
        
        .input-group input, .input-group textarea { 
            width: 100%; 
            padding: 1rem; 
            border: 2px solid #ddd; 
            border-radius: 12px; 
            font-family: inherit;
            font-size: 1rem;
            transition: all 0.3s;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .input-group input:focus, .input-group textarea:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            transform: translateY(-2px);
        }
        
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            border: none; 
            padding: 1rem 2rem; 
            border-radius: 12px; 
            cursor: pointer; 
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s;
            margin: 0.5rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .btn:active { transform: translateY(-1px); }
        
        .btn-epic { 
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
        }
        
        .btn-epic:hover {
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.6);
        }
        
        .btn-secondary { 
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%); 
        }
        
        .results { 
            margin-top: 2rem; 
            padding: 2rem; 
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
            border-radius: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .results h3 { 
            color: #333; 
            margin-bottom: 1rem; 
            font-size: 1.5rem;
        }
        
        .result-json { 
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); 
            color: #e2e8f0; 
            padding: 1.5rem; 
            border-radius: 12px; 
            font-family: 'Courier New', monospace;
            white-space: pre-wrap; 
            max-height: 600px; 
            overflow-y: auto;
            font-size: 0.9rem;
            border: 1px solid #4a5568;
        }
        
        .loading { 
            text-align: center; 
            color: #667eea; 
            font-style: italic;
            font-size: 1.2rem;
        }
        
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 1rem; 
            margin: 1rem 0;
        }
        
        .stat-card { 
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
            padding: 1.5rem; 
            border-radius: 12px; 
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .stat-number { 
            font-size: 2rem; 
            font-weight: bold; 
            color: #667eea; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .stat-label { 
            color: #666; 
            font-size: 0.9rem; 
            margin-top: 0.5rem;
        }
        
        .example-btn { 
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
            padding: 0.75rem 1.5rem; 
            font-size: 0.9rem;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
        }
        
        .example-btn:hover {
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.6);
        }
        
        .error { 
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
            color: #721c24; 
            padding: 1rem; 
            border-radius: 12px; 
            border-left: 4px solid #dc3545;
        }
        
        .platform-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin: 0.25rem;
        }
        
        .badge-youtube { background: #ff0000; color: white; }
        .badge-twitter { background: #1da1f2; color: white; }
        .badge-instagram { background: #e4405f; color: white; }
        .badge-tiktok { background: #000000; color: white; }
        .badge-facebook { background: #1877f2; color: white; }
        .badge-linkedin { background: #0077b5; color: white; }
        .badge-website { background: #6c757d; color: white; }
        
        .link-preview {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.3s;
        }
        
        .link-preview:hover {
            border-color: #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        }
        
        .url-input {
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            border: 2px solid #2196f3;
        }
        
        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
    </style>
</head>
<body>
    <div class="floating-particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1>🚀 Epic Sentiment Analysis</h1>
            <p>Advanced AI-powered content analysis with link extraction & social media integration</p>
        </div>
        
        <div class="content">
            <!-- Epic Tab Navigation -->
            <div class="demo-tabs">
                <button class="tab-button active" onclick="switchTab('basic')">📝 Basic Analysis</button>
                <button class="tab-button" onclick="switchTab('links')">🔗 Link Analysis</button>
                <button class="tab-button" onclick="switchTab('bulk')">📊 Bulk Analysis</button>
                <button class="tab-button" onclick="switchTab('samples')">🎯 Sample Links</button>
            </div>
            
            <!-- Basic Analysis Tab -->
            <div id="basic-tab" class="tab-content active">
                <div class="demo-section">
                    <h3 style="color: #333; margin-bottom: 1rem;">🎯 Quick Test Examples</h3>
                    <p style="margin-bottom: 1rem;">Try these epic examples to see the power of our system:</p>
                    <button class="btn example-btn" onclick="loadExample()">🇰🇪 Nairobi Adventure</button>
                    <button class="btn example-btn" onclick="loadExample2()">🥩 Food Review</button>
                    <button class="btn example-btn" onclick="loadExample3()">🐍 Tech Tutorial</button>
                    <button class="btn example-btn" onclick="loadExample4()">🎵 Music Video</button>
                    <button class="btn example-btn" onclick="loadExample5()">🏀 Sports Commentary</button>
                </div>
                
                <div class="epic-grid">
                    <div class="demo-section">
                        <h3 style="color: #333; margin-bottom: 1rem;">📝 Content Analysis</h3>
                        
                        <div class="input-group">
                            <label for="video_title">📹 Video/Post Title:</label>
                            <input type="text" id="video_title" placeholder="Enter your content title...">
                        </div>
                        
                        <div class="input-group">
                            <label for="video_description">📝 Description:</label>
                            <textarea id="video_description" rows="3" placeholder="Enter content description..."></textarea>
                        </div>
                        
                        <div class="input-group">
                            <label for="comments">💬 Comments (one per line):</label>
                            <textarea id="comments" rows="8" placeholder="Enter comments, one per line..."></textarea>
                        </div>
                        
                        <button class="btn btn-epic" onclick="analyzeContent()">🧠 Analyze Sentiment</button>
                        <button class="btn btn-secondary" onclick="clearForm()">🗑️ Clear</button>
                    </div>
                </div>
            </div>
            
            <!-- Link Analysis Tab -->
            <div id="links-tab" class="tab-content">
                <div class="demo-section">
                    <h3 style="color: #333; margin-bottom: 1rem;">🔗 Epic Link Analysis</h3>
                    <p style="margin-bottom: 1rem;">Analyze content directly from social media links! Supports YouTube, Twitter, Instagram, TikTok, Facebook, LinkedIn & more!</p>
                    
                    <div class="input-group">
                        <label for="url_input">🌐 Enter URL to Analyze:</label>
                        <input type="url" id="url_input" class="url-input" placeholder="https://www.youtube.com/watch?v=... or any social media link">
                    </div>
                    
                    <button class="btn btn-epic" onclick="analyzeUrl()">🔗 Analyze Link</button>
                    <button class="btn example-btn" onclick="loadSampleUrl()">📱 Load Sample URL</button>
                </div>
                
                <div class="demo-section">
                    <h3 style="color: #333; margin-bottom: 1rem;">📝 Text with Embedded Links</h3>
                    <p style="margin-bottom: 1rem;">Analyze text content and automatically extract and analyze any URLs found within!</p>
                    
                    <div class="input-group">
                        <label for="text_with_urls">📄 Text Content (with URLs):</label>
                        <textarea id="text_with_urls" rows="6" placeholder="Enter text with embedded URLs... Our AI will find and analyze them automatically!"></textarea>
                    </div>
                    
                    <button class="btn btn-epic" onclick="analyzeTextWithUrls()">🤖 AI Auto-Extract & Analyze</button>
                    <button class="btn example-btn" onclick="loadTextWithUrls()">📋 Load Example Text</button>
                </div>
            </div>
            
            <!-- Bulk Analysis Tab -->
            <div id="bulk-tab" class="tab-content">
                <div class="demo-section">
                    <h3 style="color: #333; margin-bottom: 1rem;">📊 Bulk URL Analysis</h3>
                    <p style="margin-bottom: 1rem;">Analyze multiple URLs at once and get aggregated insights across platforms!</p>
                    
                    <div class="input-group">
                        <label for="bulk_urls">🔗 Multiple URLs (one per line):</label>
                        <textarea id="bulk_urls" rows="10" placeholder="https://www.youtube.com/watch?v=example1&#10;https://twitter.com/user/status/example2&#10;https://www.instagram.com/p/example3/&#10;..."></textarea>
                    </div>
                    
                    <button class="btn btn-epic" onclick="analyzeBulkUrls()">📊 Bulk Analyze</button>
                    <button class="btn example-btn" onclick="loadBulkSamples()">📁 Load Sample URLs</button>
                </div>
            </div>
            
            <!-- Sample Links Tab -->
            <div id="samples-tab" class="tab-content">
                <div class="demo-section">
                    <h3 style="color: #333; margin-bottom: 1rem;">🎯 Platform Sample Links</h3>
                    <p style="margin-bottom: 1rem;">Try our sample links from different social media platforms:</p>
                    
                    <div class="epic-grid" id="sample-links-grid">
                        <!-- Will be populated by JavaScript -->
                    </div>
                </div>
            </div>
            
            <!-- Results Section -->
            <div id="results" style="display: none;">
                <div class="results">
                    <h3>🎉 Epic Analysis Results</h3>
                    <div id="stats" class="stats"></div>
                    <div id="result_json" class="result-json"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 10 + 5 + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDelay = Math.random() * 6 + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        // Initialize particles
        createParticles();
        
        // Tab switching
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            // Load sample links for samples tab
            if (tabName === 'samples') {
                loadSampleLinks();
            }
        }
        
        // Example loaders
        function loadExample() {
            document.getElementById('video_title').value = 'My first day in Nairobi 🚖🔥';
            document.getElementById('video_description').value = 'Trying out local food and matatus, what an adventure!';
            document.getElementById('comments').value = `😂😂 bro you look lost but it's vibes
This city will eat you alive, trust me.
Matatu rides >>> Uber any day
Spam link: www.fakecrypto.com
Karibu Kenya! We love you ❤️`;
        }
        
        function loadExample2() {
            document.getElementById('video_title').value = 'Best Nyama Choma in Nairobi! 🥩🔥';
            document.getElementById('video_description').value = 'Testing the most popular meat spots in the city';
            document.getElementById('comments').value = `This place is absolutely amazing! 😍
Overpriced tourist trap if you ask me
I've been coming here for years, best meat in town
Where exactly is this located?
🤤🤤 Making me hungry just watching
The ambiance is perfect for dates 💕`;
        }
        
        function loadExample3() {
            document.getElementById('video_title').value = 'Python Tutorial: Build Your First API 🐍';
            document.getElementById('video_description').value = 'Complete beginner guide to creating REST APIs with Flask';
            document.getElementById('comments').value = `Great tutorial! Very clear explanations
This is too advanced for beginners
Thanks! Finally understand APIs now 🙏
Could you do a MongoDB tutorial next?
Subscribe here: www.spam-link.com/subscribe
The code examples are really helpful
I'm a complete newbie and this helped so much!`;
        }
        
        function loadExample4() {
            document.getElementById('video_title').value = 'Burna Boy - Last Last (Official Music Video) 🎵';
            document.getElementById('video_description').value = 'New hit single from the African Giant himself!';
            document.getElementById('comments').value = `This song is fire! 🔥🔥🔥
Burna Boy never disappoints! 🎵
African music to the world! 🌍
The beat is absolutely insane
This is going to be song of the year
Love from Kenya! 🇰🇪
The video quality is top notch 📹`;
        }
        
        function loadExample5() {
            document.getElementById('video_title').value = 'Real Madrid vs Barcelona - El Clasico Highlights ⚽';
            document.getElementById('video_description').value = 'Epic match highlights from the biggest rivalry in football!';
            document.getElementById('comments').value = `What a match! Incredible goals ⚽
Messi is the GOAT 🐐
Real Madrid played better tbh
The referee was terrible today 😤
Best El Clasico in years!
Vamos Real Madrid! 👑
Football at its finest level`;
        }
        
        function loadSampleUrl() {
            document.getElementById('url_input').value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
        }
        
        function loadTextWithUrls() {
            document.getElementById('text_with_urls').value = `Check out this amazing video about African tech innovation: https://www.youtube.com/watch?v=jNQXAC9IVRw

Also, this Twitter thread about Kenya's startup scene is incredible: https://twitter.com/user/status/1234567890

And don't miss this Instagram post showcasing beautiful African fashion: https://www.instagram.com/p/ABC123/

The future of African technology is so bright! 🌟`;
        }
        
        function loadBulkSamples() {
            document.getElementById('bulk_urls').value = `https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://twitter.com/user/status/1234567890
https://www.instagram.com/p/ABC123/
https://www.tiktok.com/@user/video/1234567890
https://www.linkedin.com/posts/user-activity-1234567890`;
        }
        
        function clearForm() {
            document.getElementById('video_title').value = '';
            document.getElementById('video_description').value = '';
            document.getElementById('comments').value = '';
            document.getElementById('results').style.display = 'none';
        }
        
        // Analysis functions
        function analyzeContent() {
            const title = document.getElementById('video_title').value;
            const description = document.getElementById('video_description').value;
            const commentsText = document.getElementById('comments').value;
            const comments = commentsText.split('\\n').filter(c => c.trim());
            
            if (!title && !description && comments.length === 0) {
                alert('Please enter some content to analyze! 🚨');
                return;
            }
            
            showLoading('🧠 Analyzing content with AI...');
            
            fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    video_title: title,
                    video_description: description,
                    comments: comments
                })
            })
            .then(response => response.json())
            .then(data => displayResults(data))
            .catch(error => showError('Analysis failed: ' + error.message));
        }
        
        function analyzeUrl() {
            const url = document.getElementById('url_input').value;
            
            if (!url) {
                alert('Please enter a URL to analyze! 🔗');
                return;
            }
            
            showLoading('🔗 Extracting content from URL...');
            
            fetch('/api/analyze-url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => displayResults(data))
            .catch(error => showError('URL analysis failed: ' + error.message));
        }
        
        function analyzeTextWithUrls() {
            const text = document.getElementById('text_with_urls').value;
            
            if (!text) {
                alert('Please enter some text to analyze! 📝');
                return;
            }
            
            showLoading('🤖 Auto-extracting URLs and analyzing...');
            
            fetch('/api/analyze-text-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => displayResults(data))
            .catch(error => showError('Text analysis failed: ' + error.message));
        }
        
        function analyzeBulkUrls() {
            const urlsText = document.getElementById('bulk_urls').value;
            const urls = urlsText.split('\\n').filter(u => u.trim());
            
            if (urls.length === 0) {
                alert('Please enter some URLs to analyze! 📊');
                return;
            }
            
            showLoading(`📊 Bulk analyzing ${urls.length} URLs...`);
            
            fetch('/api/analyze-bulk-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: urls })
            })
            .then(response => response.json())
            .then(data => displayResults(data))
            .catch(error => showError('Bulk analysis failed: ' + error.message));
        }
        
        function showLoading(message) {
            document.getElementById('results').style.display = 'block';
            document.getElementById('result_json').innerHTML = `<div class="loading">${message}</div>`;
            document.getElementById('stats').innerHTML = '';
        }
        
        function showError(message) {
            document.getElementById('result_json').innerHTML = `<div class="error">${message}</div>`;
        }
        
        function displayResults(data) {
            document.getElementById('result_json').innerHTML = JSON.stringify(data, null, 2);
            const stats = createStats(data);
            document.getElementById('stats').innerHTML = stats;
        }
        
        function createStats(data) {
            // Handle different types of results
            if (data.summary) {
                // Bulk analysis results
                return createBulkStats(data);
            } else if (data.url_analysis) {
                // URL analysis results
                return createUrlStats(data);
            } else if (data.text_analysis) {
                // Text with URLs analysis
                return createTextUrlStats(data);
            } else {
                // Regular content analysis
                return createRegularStats(data);
            }
        }
        
        function createRegularStats(data) {
            const comments = data.comments || [];
            const videoSentiment = data.video_sentiment || 'unknown';
            
            const sentimentCounts = {};
            const emotionCounts = {};
            const tagCounts = {};
            
            comments.forEach(comment => {
                const sentiment = comment.sentiment || 'unknown';
                const tag = comment.tag || 'unknown';
                const emotions = comment.emotion || [];
                
                sentimentCounts[sentiment] = (sentimentCounts[sentiment] || 0) + 1;
                tagCounts[tag] = (tagCounts[tag] || 0) + 1;
                
                emotions.forEach(emotion => {
                    emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;
                });
            });
            
            return `
                <div class="stat-card">
                    <div class="stat-number">${videoSentiment}</div>
                    <div class="stat-label">Overall Sentiment</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${comments.length}</div>
                    <div class="stat-label">Comments Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Object.keys(emotionCounts).length}</div>
                    <div class="stat-label">Emotions Detected</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${tagCounts.spam || 0}</div>
                    <div class="stat-label">Spam Comments</div>
                </div>
            `;
        }
        
        function createUrlStats(data) {
            const urlAnalysis = data.url_analysis || {};
            const platform = urlAnalysis.platform || 'unknown';
            const comments = data.comments || [];
            
            return `
                <div class="stat-card">
                    <div class="stat-number">
                        <span class="platform-badge badge-${platform}">${platform.toUpperCase()}</span>
                    </div>
                    <div class="stat-label">Platform Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${comments.length}</div>
                    <div class="stat-label">Comments Extracted</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.video_sentiment || 'N/A'}</div>
                    <div class="stat-label">Content Sentiment</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">✅</div>
                    <div class="stat-label">Content Extracted</div>
                </div>
            `;
        }
        
        function createBulkStats(data) {
            const summary = data.summary || {};
            const platforms = data.platform_distribution || {};
            
            return `
                <div class="stat-card">
                    <div class="stat-number">${summary.total_urls_analyzed || 0}</div>
                    <div class="stat-label">URLs Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${summary.successful_analyses || 0}</div>
                    <div class="stat-label">Successful Extractions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${summary.total_comments || 0}</div>
                    <div class="stat-label">Total Comments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Object.keys(platforms).length}</div>
                    <div class="stat-label">Platforms Covered</div>
                </div>
            `;
        }
        
        function createTextUrlStats(data) {
            const embeddedUrls = data.embedded_urls || {};
            const textAnalysis = data.text_analysis || {};
            
            return `
                <div class="stat-card">
                    <div class="stat-number">${embeddedUrls.url_count || 0}</div>
                    <div class="stat-label">URLs Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${textAnalysis.sentiment || 'N/A'}</div>
                    <div class="stat-label">Text Sentiment</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${(textAnalysis.emotion || []).length}</div>
                    <div class="stat-label">Emotions in Text</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">🤖</div>
                    <div class="stat-label">AI Auto-Analysis</div>
                </div>
            `;
        }
        
        function loadSampleLinks() {
            fetch('/api/sample-links')
                .then(response => response.json())
                .then(data => {
                    const grid = document.getElementById('sample-links-grid');
                    grid.innerHTML = '';
                    
                    Object.entries(data).forEach(([platform, links]) => {
                        const platformDiv = document.createElement('div');
                        platformDiv.className = 'demo-section';
                        platformDiv.innerHTML = `
                            <h4><span class="platform-badge badge-${platform}">${platform.toUpperCase()}</span></h4>
                            ${links.map(link => `
                                <div class="link-preview" onclick="analyzeSpecificUrl('${link}')">
                                    <div style="font-family: monospace; font-size: 0.8rem; color: #666; margin-bottom: 0.5rem;">${link}</div>
                                    <button class="btn btn-epic" style="padding: 0.5rem 1rem; font-size: 0.8rem;">🔗 Analyze This Link</button>
                                </div>
                            `).join('')}
                        `;
                        grid.appendChild(platformDiv);
                    });
                })
                .catch(error => console.error('Failed to load sample links:', error));
        }
        
        function analyzeSpecificUrl(url) {
            document.getElementById('url_input').value = url;
            switchTab('links');
            analyzeUrl();
        }
    </script>
</body>
</html>
    """


@app.route('/api/analyze-url', methods=['POST'])
def api_analyze_url():
    """API endpoint for URL analysis"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        # Analyze URL
        result = nlp_engine.analyze_url(url)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-text-urls', methods=['POST'])
def api_analyze_text_urls():
    """API endpoint for analyzing text with embedded URLs"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Analyze text with URLs
        result = nlp_engine.analyze_text_with_urls(text, analyze_embedded_urls=True)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-bulk-urls', methods=['POST'])
def api_analyze_bulk_urls():
    """API endpoint for bulk URL analysis"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({"error": "No URLs provided"}), 400
        
        # Analyze multiple URLs
        result = nlp_engine.analyze_multiple_urls(urls)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sample-links')
def api_sample_links():
    """Get sample links for testing"""
    try:
        sample_links = nlp_engine.get_sample_urls()
        return jsonify(sample_links)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        video_title = data.get('video_title', '')
        video_description = data.get('video_description', '')
        comments = data.get('comments', []);
        
        # Perform analysis
        result = nlp_engine.analyze_video_data(video_title, video_description, comments)
        
        # Add metadata
        result['metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'total_comments': len(comments),
            'analysis_engine': 'NLPEngine v1.0'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Sentiment Analysis API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/demo')
def demo_endpoint():
    """Demo endpoint with example data"""
    try:
        result = nlp_engine.analyze_video_data(
            "My first day in Nairobi 🚖🔥",
            "Trying out local food and matatus, what an adventure!",
            [
                "😂😂 bro you look lost but it's vibes",
                "This city will eat you alive, trust me.",
                "Matatu rides >>> Uber any day",
                "Spam link: www.fakecrypto.com",
                "Karibu Kenya! We love you ❤️"
            ]
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Sentiment Analysis Web Interface...")
    print("📊 Loading NLP engine...")
    print("✅ System ready!")
    print(f"🌐 Open your browser to: http://localhost:5001")
    print(f"🔗 API endpoint: http://localhost:5001/api/analyze")
    print(f"🩺 Health check: http://localhost:5001/api/health")
    print(f"🎯 Demo endpoint: http://localhost:5001/api/demo")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)
