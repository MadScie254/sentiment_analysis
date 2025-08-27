"""
Simple web interface for testing the sentiment analysis system
Lightweight Flask server with HTML interface - no complex dependencies
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

# Import our NLP engine
from nlp_engine import NLPEngine

app = Flask(__name__)
app.secret_key = "sentiment_test_2025"

# Initialize NLP engine
nlp_engine = NLPEngine()

@app.route('/')
def home():
    """Main testing interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Sentiment Analysis - Test Interface</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 2rem; 
            text-align: center;
        }
        .header h1 { margin-bottom: 0.5rem; font-size: 2.5rem; }
        .header p { opacity: 0.9; font-size: 1.1rem; }
        .content { padding: 2rem; }
        .demo-section { 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 1.5rem; 
            margin: 1rem 0; 
        }
        .input-group { margin: 1rem 0; }
        .input-group label { 
            display: block; 
            font-weight: bold; 
            margin-bottom: 0.5rem; 
            color: #333;
        }
        .input-group input, .input-group textarea { 
            width: 100%; 
            padding: 0.75rem; 
            border: 2px solid #ddd; 
            border-radius: 8px; 
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        .input-group input:focus, .input-group textarea:focus { 
            outline: none; 
            border-color: #667eea; 
        }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            border: none; 
            padding: 1rem 2rem; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 1rem;
            font-weight: bold;
            transition: transform 0.2s;
            margin: 0.5rem;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn:active { transform: translateY(0); }
        .btn-secondary { 
            background: #6c757d; 
        }
        .results { 
            margin-top: 2rem; 
            padding: 1.5rem; 
            background: #f8f9fa; 
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }
        .results h3 { color: #333; margin-bottom: 1rem; }
        .result-json { 
            background: #2d3748; 
            color: #e2e8f0; 
            padding: 1rem; 
            border-radius: 8px; 
            font-family: 'Courier New', monospace;
            white-space: pre-wrap; 
            max-height: 500px; 
            overflow-y: auto;
            font-size: 0.9rem;
        }
        .loading { 
            text-align: center; 
            color: #667eea; 
            font-style: italic;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 1rem; 
            margin: 1rem 0;
        }
        .stat-card { 
            background: white; 
            padding: 1rem; 
            border-radius: 8px; 
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-number { font-size: 1.5rem; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; font-size: 0.9rem; }
        .example-btn { 
            background: #28a745; 
            padding: 0.5rem 1rem; 
            font-size: 0.9rem;
        }
        .error { 
            background: #f8d7da; 
            color: #721c24; 
            padding: 1rem; 
            border-radius: 8px; 
            border-left: 4px solid #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Sentiment Analysis Test</h1>
            <p>Test your social media content sentiment analysis system</p>
        </div>
        
        <div class="content">
            <!-- Quick Example Section -->
            <div class="demo-section">
                <h3 style="color: #333; margin-bottom: 1rem;">🎯 Quick Test</h3>
                <p style="margin-bottom: 1rem;">Click to test with your example data:</p>
                <button class="btn example-btn" onclick="loadExample()">Load "Nairobi" Example</button>
                <button class="btn example-btn" onclick="loadExample2()">Load "Food Review" Example</button>
                <button class="btn example-btn" onclick="loadExample3()">Load "Tech Tutorial" Example</button>
            </div>
            
            <!-- Analysis Form -->
            <div class="demo-section">
                <h3 style="color: #333; margin-bottom: 1rem;">📝 Custom Analysis</h3>
                
                <div class="input-group">
                    <label for="video_title">📹 Video Title:</label>
                    <input type="text" id="video_title" placeholder="Enter your video title...">
                </div>
                
                <div class="input-group">
                    <label for="video_description">📝 Video Description:</label>
                    <textarea id="video_description" rows="3" placeholder="Enter your video description..."></textarea>
                </div>
                
                <div class="input-group">
                    <label for="comments">💬 Comments (one per line):</label>
                    <textarea id="comments" rows="8" placeholder="Enter comments, one per line..."></textarea>
                </div>
                
                <button class="btn" onclick="analyzeContent()">🧠 Analyze Sentiment</button>
                <button class="btn btn-secondary" onclick="clearForm()">🗑️ Clear</button>
            </div>
            
            <!-- Results Section -->
            <div id="results" style="display: none;">
                <div class="results">
                    <h3>📊 Analysis Results</h3>
                    <div id="stats" class="stats"></div>
                    <div id="result_json" class="result-json"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
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
🤤🤤 Making me hungry just watching`;
        }
        
        function loadExample3() {
            document.getElementById('video_title').value = 'Python Tutorial: Build Your First API 🐍';
            document.getElementById('video_description').value = 'Complete beginner guide to creating REST APIs with Flask';
            document.getElementById('comments').value = `Great tutorial! Very clear explanations
This is too advanced for beginners
Thanks! Finally understand APIs now 🙏
Could you do a MongoDB tutorial next?
Subscribe here: www.spam-link.com/subscribe
The code examples are really helpful`;
        }
        
        function clearForm() {
            document.getElementById('video_title').value = '';
            document.getElementById('video_description').value = '';
            document.getElementById('comments').value = '';
            document.getElementById('results').style.display = 'none';
        }
        
        function analyzeContent() {
            const title = document.getElementById('video_title').value;
            const description = document.getElementById('video_description').value;
            const commentsText = document.getElementById('comments').value;
            const comments = commentsText.split('\\n').filter(c => c.trim());
            
            if (!title && !description && comments.length === 0) {
                alert('Please enter some content to analyze!');
                return;
            }
            
            // Show loading
            document.getElementById('results').style.display = 'block';
            document.getElementById('result_json').innerHTML = 'Analyzing... 🧠';
            document.getElementById('stats').innerHTML = '';
            
            // Make API call
            fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_title: title,
                    video_description: description,
                    comments: comments
                })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                document.getElementById('result_json').innerHTML = 
                    '<div class="error">Error: ' + error.message + '</div>';
            });
        }
        
        function displayResults(data) {
            // Display JSON
            document.getElementById('result_json').innerHTML = JSON.stringify(data, null, 2);
            
            // Create stats
            const stats = createStats(data);
            document.getElementById('stats').innerHTML = stats;
        }
        
        function createStats(data) {
            const comments = data.comments || [];
            const videoSentiment = data.video_sentiment || 'unknown';
            
            // Count sentiments
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
                    <div class="stat-label">Video Sentiment</div>
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
    </script>
</body>
</html>
    """

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        video_title = data.get('video_title', '')
        video_description = data.get('video_description', '')
        comments = data.get('comments', [])
        
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
