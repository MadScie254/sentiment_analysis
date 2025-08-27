"""
Epic web interface for testing the sentiment analysis system with link analysis
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

# Import our enhanced NLP engine
from nlp_engine import NLPEngine

app = Flask(__name__)
app.secret_key = "sentiment_epic_2025"

# Initialize NLP engine with link analysis
nlp_engine = NLPEngine()

@app.route('/')
def home():
    """Epic dashboard with link analysis capabilities"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Epic Sentiment Analysis Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px; color: #333;
        }
        .container { 
            max-width: 1200px; margin: 0 auto; background: white; 
            border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 2rem; text-align: center;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .content { padding: 2rem; }
        
        .tabs { display: flex; margin-bottom: 2rem; background: #f8f9fa; border-radius: 10px; padding: 0.5rem; }
        .tab { 
            flex: 1; padding: 1rem; text-align: center; cursor: pointer; 
            border-radius: 8px; font-weight: bold; transition: all 0.3s;
        }
        .tab.active { background: #667eea; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.5s; }
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .section { 
            background: #f8f9fa; padding: 1.5rem; margin: 1rem 0; 
            border-radius: 12px; border-left: 4px solid #667eea;
        }
        .input-group { margin: 1rem 0; }
        .input-group label { display: block; font-weight: bold; margin-bottom: 0.5rem; }
        .input-group input, .input-group textarea { 
            width: 100%; padding: 0.75rem; border: 2px solid #ddd; 
            border-radius: 8px; font-size: 1rem; transition: border-color 0.3s;
        }
        .input-group input:focus, .input-group textarea:focus { 
            outline: none; border-color: #667eea; 
        }
        
        .btn { 
            background: #667eea; color: white; border: none; 
            padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; 
            font-weight: bold; margin: 0.5rem; transition: all 0.3s;
        }
        .btn:hover { background: #5a6fd8; transform: translateY(-2px); }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #218838; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #545b62; }
        
        .results { 
            margin-top: 1rem; padding: 1.5rem; background: #f8f9fa; 
            border-radius: 12px; border-left: 4px solid #28a745;
        }
        .json-output { 
            background: #2d3748; color: #e2e8f0; padding: 1rem; 
            border-radius: 8px; font-family: monospace; white-space: pre-wrap; 
            max-height: 400px; overflow-y: auto; font-size: 0.9rem;
        }
        
        .stats { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 1rem; margin: 1rem 0;
        }
        .stat-card { 
            background: white; padding: 1rem; border-radius: 8px; 
            border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stat-number { font-size: 1.5rem; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; font-size: 0.9rem; margin-top: 0.25rem; }
        
        .platform-badge { 
            display: inline-block; padding: 0.25rem 0.5rem; border-radius: 15px; 
            font-size: 0.8rem; font-weight: bold; margin: 0.25rem;
        }
        .badge-youtube { background: #ff0000; color: white; }
        .badge-twitter { background: #1da1f2; color: white; }
        .badge-instagram { background: #e4405f; color: white; }
        .badge-tiktok { background: #000000; color: white; }
        .badge-facebook { background: #1877f2; color: white; }
        .badge-linkedin { background: #0077b5; color: white; }
        .badge-website { background: #6c757d; color: white; }
        
        .link-sample { 
            background: white; border: 1px solid #ddd; border-radius: 8px; 
            padding: 1rem; margin: 0.5rem 0; cursor: pointer; transition: all 0.3s;
        }
        .link-sample:hover { border-color: #667eea; box-shadow: 0 2px 8px rgba(102,126,234,0.2); }
        .link-url { font-family: monospace; font-size: 0.8rem; color: #666; margin-bottom: 0.5rem; }
        
        .loading { text-align: center; color: #667eea; font-style: italic; }
        .error { background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 8px; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        @media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Epic Sentiment Analysis Dashboard</h1>
            <p>Advanced AI-powered content analysis with link extraction & social media integration</p>
        </div>
        
        <div class="content">
            <div class="tabs">
                <div class="tab active" onclick="switchTab('basic')">📝 Basic Analysis</div>
                <div class="tab" onclick="switchTab('links')">🔗 Link Analysis</div>
                <div class="tab" onclick="switchTab('bulk')">📊 Bulk Analysis</div>
                <div class="tab" onclick="switchTab('samples')">🎯 Sample Links</div>
            </div>
            
            <!-- Basic Analysis Tab -->
            <div id="basic-tab" class="tab-content active">
                <div class="section">
                    <h3>🎯 Quick Examples</h3>
                    <p>Try these epic examples:</p>
                    <br>
                    <button class="btn btn-success" onclick="loadExample1()">🇰🇪 Nairobi Adventure</button>
                    <button class="btn btn-success" onclick="loadExample2()">🥩 Food Review</button>
                    <button class="btn btn-success" onclick="loadExample3()">🐍 Tech Tutorial</button>
                    <button class="btn btn-success" onclick="loadExample4()">🎵 Music Video</button>
                </div>
                
                <div class="grid-2">
                    <div class="section">
                        <h3>📝 Content Analysis</h3>
                        
                        <div class="input-group">
                            <label>📹 Video/Post Title:</label>
                            <input type="text" id="title" placeholder="Enter content title...">
                        </div>
                        
                        <div class="input-group">
                            <label>📝 Description:</label>
                            <textarea id="description" rows="3" placeholder="Enter description..."></textarea>
                        </div>
                        
                        <div class="input-group">
                            <label>💬 Comments (one per line):</label>
                            <textarea id="comments" rows="6" placeholder="Enter comments..."></textarea>
                        </div>
                        
                        <button class="btn" onclick="analyzeContent()">🧠 Analyze Content</button>
                        <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
                    </div>
                    
                    <div id="results" style="display: none;">
                        <div class="results">
                            <h3>📊 Analysis Results</h3>
                            <div id="stats"></div>
                            <div id="output" class="json-output"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Link Analysis Tab -->
            <div id="links-tab" class="tab-content">
                <div class="section">
                    <h3>🔗 Epic Link Analysis</h3>
                    <p>Analyze content from social media links! Supports YouTube, Twitter, Instagram, TikTok, Facebook, LinkedIn & more!</p>
                    
                    <div class="input-group">
                        <label>🌐 Enter URL to Analyze:</label>
                        <input type="url" id="url-input" placeholder="https://www.youtube.com/watch?v=... or any social media link">
                    </div>
                    
                    <button class="btn" onclick="analyzeUrl()">🔗 Analyze Link</button>
                    <button class="btn btn-success" onclick="loadSampleUrl()">📱 Load Sample</button>
                </div>
                
                <div class="section">
                    <h3>📝 Text with Links</h3>
                    <p>Analyze text and automatically extract & analyze embedded URLs!</p>
                    
                    <div class="input-group">
                        <label>📄 Text with URLs:</label>
                        <textarea id="text-urls" rows="6" placeholder="Enter text with embedded URLs..."></textarea>
                    </div>
                    
                    <button class="btn" onclick="analyzeTextUrls()">🤖 Auto-Extract & Analyze</button>
                    <button class="btn btn-success" onclick="loadTextSample()">📋 Load Example</button>
                </div>
            </div>
            
            <!-- Bulk Analysis Tab -->
            <div id="bulk-tab" class="tab-content">
                <div class="section">
                    <h3>📊 Bulk URL Analysis</h3>
                    <p>Analyze multiple URLs at once and get aggregated insights!</p>
                    
                    <div class="input-group">
                        <label>🔗 Multiple URLs (one per line):</label>
                        <textarea id="bulk-urls" rows="8" placeholder="https://www.youtube.com/watch?v=example1&#10;https://twitter.com/user/status/example2&#10;https://www.instagram.com/p/example3/"></textarea>
                    </div>
                    
                    <button class="btn" onclick="analyzeBulk()">📊 Bulk Analyze</button>
                    <button class="btn btn-success" onclick="loadBulkSample()">📁 Load Samples</button>
                </div>
            </div>
            
            <!-- Sample Links Tab -->
            <div id="samples-tab" class="tab-content">
                <div class="section">
                    <h3>🎯 Platform Sample Links</h3>
                    <p>Try sample links from different platforms:</p>
                    <div id="sample-links"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'samples') loadSampleLinks();
        }
        
        function loadExample1() {
            document.getElementById('title').value = 'My first day in Nairobi 🚖🔥';
            document.getElementById('description').value = 'Trying out local food and matatus, what an adventure!';
            document.getElementById('comments').value = 'Yooh bro you look lost but it\\'s vibes 😂😂\\nThis city will eat you alive, trust me.\\nMatatu rides >>> Uber any day\\nSpam link: www.fakecrypto.com\\nKaribu Kenya! We love you ❤️';
        }
        
        function loadExample2() {
            document.getElementById('title').value = 'Best Nyama Choma in Nairobi! 🥩🔥';
            document.getElementById('description').value = 'Testing the most popular meat spots in the city';
            document.getElementById('comments').value = 'This place is absolutely amazing! 😍\\nOverpriced tourist trap if you ask me\\nI\\'ve been coming here for years, best meat in town\\nWhere exactly is this located?\\n🤤🤤 Making me hungry just watching';
        }
        
        function loadExample3() {
            document.getElementById('title').value = 'Python Tutorial: Build Your First API 🐍';
            document.getElementById('description').value = 'Complete beginner guide to creating REST APIs with Flask';
            document.getElementById('comments').value = 'Great tutorial! Very clear explanations\\nThis is too advanced for beginners\\nThanks! Finally understand APIs now 🙏\\nCould you do a MongoDB tutorial next?\\nSubscribe here: www.spam-link.com/subscribe\\nThe code examples are really helpful';
        }
        
        function loadExample4() {
            document.getElementById('title').value = 'Burna Boy - Last Last (Official Music Video) 🎵';
            document.getElementById('description').value = 'New hit single from the African Giant himself!';
            document.getElementById('comments').value = 'This song is fire! 🔥🔥🔥\\nBurna Boy never disappoints! 🎵\\nAfrican music to the world! 🌍\\nThe beat is absolutely insane\\nThis is going to be song of the year\\nLove from Kenya! 🇰🇪';
        }
        
        function loadSampleUrl() {
            document.getElementById('url-input').value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
        }
        
        function loadTextSample() {
            document.getElementById('text-urls').value = 'Check out this amazing video: https://www.youtube.com/watch?v=jNQXAC9IVRw\\n\\nAlso this Twitter thread is incredible: https://twitter.com/user/status/1234567890\\n\\nAnd this Instagram post: https://www.instagram.com/p/ABC123/';
        }
        
        function loadBulkSample() {
            document.getElementById('bulk-urls').value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ\\nhttps://twitter.com/user/status/1234567890\\nhttps://www.instagram.com/p/ABC123/\\nhttps://www.tiktok.com/@user/video/1234567890';
        }
        
        function clearAll() {
            document.getElementById('title').value = '';
            document.getElementById('description').value = '';
            document.getElementById('comments').value = '';
            document.getElementById('results').style.display = 'none';
        }
        
        function showResults(data) {
            document.getElementById('results').style.display = 'block';
            document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            
            const stats = createStats(data);
            document.getElementById('stats').innerHTML = stats;
        }
        
        function showLoading(message) {
            document.getElementById('results').style.display = 'block';
            document.getElementById('output').innerHTML = '<div class="loading">' + message + '</div>';
            document.getElementById('stats').innerHTML = '';
        }
        
        function showError(message) {
            document.getElementById('results').style.display = 'block';
            document.getElementById('output').innerHTML = '<div class="error">' + message + '</div>';
        }
        
        function createStats(data) {
            if (data.summary) {
                // Bulk analysis
                const summary = data.summary;
                return `
                    <div class="stat-card">
                        <div class="stat-number">${summary.total_urls_analyzed || 0}</div>
                        <div class="stat-label">URLs Analyzed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${summary.successful_analyses || 0}</div>
                        <div class="stat-label">Successful</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${summary.total_comments || 0}</div>
                        <div class="stat-label">Comments</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${summary.platforms_analyzed || 0}</div>
                        <div class="stat-label">Platforms</div>
                    </div>
                `;
            } else if (data.url_analysis) {
                // URL analysis
                const platform = data.url_analysis.platform || 'unknown';
                const comments = data.comments || [];
                return `
                    <div class="stat-card">
                        <div class="stat-number"><span class="platform-badge badge-${platform}">${platform.toUpperCase()}</span></div>
                        <div class="stat-label">Platform</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${comments.length}</div>
                        <div class="stat-label">Comments</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.video_sentiment || 'N/A'}</div>
                        <div class="stat-label">Sentiment</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">✅</div>
                        <div class="stat-label">Extracted</div>
                    </div>
                `;
            } else {
                // Regular analysis
                const comments = data.comments || [];
                const sentiment = data.video_sentiment || 'unknown';
                return `
                    <div class="stat-card">
                        <div class="stat-number">${sentiment}</div>
                        <div class="stat-label">Sentiment</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${comments.length}</div>
                        <div class="stat-label">Comments</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${comments.filter(c => c.tag === 'spam').length}</div>
                        <div class="stat-label">Spam</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${comments.filter(c => (c.emotion || []).length > 0).length}</div>
                        <div class="stat-label">Emotions</div>
                    </div>
                `;
            }
        }
        
        function analyzeContent() {
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            const comments = document.getElementById('comments').value.split('\\n').filter(c => c.trim());
            
            if (!title && !description && !comments.length) {
                alert('Please enter some content!');
                return;
            }
            
            showLoading('🧠 Analyzing content...');
            
            fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_title: title, video_description: description, comments: comments })
            })
            .then(r => r.json())
            .then(showResults)
            .catch(e => showError('Analysis failed: ' + e.message));
        }
        
        function analyzeUrl() {
            const url = document.getElementById('url-input').value;
            if (!url) { alert('Please enter a URL!'); return; }
            
            showLoading('🔗 Extracting content from URL...');
            
            fetch('/api/analyze-url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            })
            .then(r => r.json())
            .then(showResults)
            .catch(e => showError('URL analysis failed: ' + e.message));
        }
        
        function analyzeTextUrls() {
            const text = document.getElementById('text-urls').value;
            if (!text) { alert('Please enter some text!'); return; }
            
            showLoading('🤖 Extracting URLs and analyzing...');
            
            fetch('/api/analyze-text-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(r => r.json())
            .then(showResults)
            .catch(e => showError('Text analysis failed: ' + e.message));
        }
        
        function analyzeBulk() {
            const urls = document.getElementById('bulk-urls').value.split('\\n').filter(u => u.trim());
            if (!urls.length) { alert('Please enter some URLs!'); return; }
            
            showLoading(`📊 Analyzing ${urls.length} URLs...`);
            
            fetch('/api/analyze-bulk-urls', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ urls: urls })
            })
            .then(r => r.json())
            .then(showResults)
            .catch(e => showError('Bulk analysis failed: ' + e.message));
        }
        
        function loadSampleLinks() {
            fetch('/api/sample-links')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('sample-links');
                    container.innerHTML = '';
                    
                    Object.entries(data).forEach(([platform, links]) => {
                        const div = document.createElement('div');
                        div.innerHTML = `
                            <h4><span class="platform-badge badge-${platform}">${platform.toUpperCase()}</span></h4>
                            ${links.map(link => `
                                <div class="link-sample" onclick="testLink('${link}')">
                                    <div class="link-url">${link}</div>
                                    <button class="btn" style="padding: 0.5rem 1rem;">🔗 Test This Link</button>
                                </div>
                            `).join('')}
                        `;
                        container.appendChild(div);
                    });
                })
                .catch(e => console.error('Failed to load samples:', e));
        }
        
        function testLink(url) {
            document.getElementById('url-input').value = url;
            switchTab('links');
            analyzeUrl();
        }
    </script>
</body>
</html>"""

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

@app.route('/api/sample-links')
def api_sample_links():
    """Get sample links for testing"""
    try:
        return jsonify(nlp_engine.get_sample_urls())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
            'analysis_engine': 'Epic NLP Engine v2.0'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Epic Sentiment Analysis API",
        "features": ["basic_analysis", "link_analysis", "bulk_analysis"],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Epic Sentiment Analysis Dashboard...")
    print("📊 Loading enhanced NLP engine with link analysis...")
    print("✅ System ready with new features!")
    print(f"🌐 Dashboard: http://localhost:5002")
    print(f"🔗 Link Analysis: http://localhost:5002/api/analyze-url")
    print(f"📊 Bulk Analysis: http://localhost:5002/api/analyze-bulk-urls")
    print(f"🤖 Auto-Extract: http://localhost:5002/api/analyze-text-urls")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5002, debug=True, threaded=True)
