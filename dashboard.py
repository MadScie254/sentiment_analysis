"""
Advanced web dashboard for sentiment analysis system
Real-time monitoring, analytics visualization, and system management
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import time

# Import our modules
from nlp_engine import NLPEngine
from analytics import SentimentAnalytics
from database import DatabaseManager
from monitoring import SystemMonitor, PerformanceTracker

app = Flask(__name__)
app.secret_key = "sentiment_analysis_dashboard_2025"

# Initialize components
nlp_engine = NLPEngine()
analytics_engine = SentimentAnalytics()
db_manager = DatabaseManager()
system_monitor = SystemMonitor()
performance_tracker = PerformanceTracker(system_monitor)

# Start monitoring
system_monitor.start_monitoring(interval=30)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/analyze', methods=['POST'])
@performance_tracker.track_api_call('/api/analyze')
def analyze_content():
    """Analyze video content and comments"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        video_title = data.get('video_title', '')
        video_description = data.get('video_description', '')
        comments = data.get('comments', [])
        
        with performance_tracker.track_analysis() as tracker:
            tracker.set_comment_count(len(comments))
            
            # Perform analysis
            result = nlp_engine.analyze_video_data(video_title, video_description, comments)
            
            # Add to analytics history
            analytics_engine.add_analysis(result)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/quick-analyze', methods=['POST'])
@performance_tracker.track_api_call('/api/quick-analyze')
def quick_analyze():
    """Quick analysis for single text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = nlp_engine.quick_analyze(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics/report')
@performance_tracker.track_api_call('/api/analytics/report')
def get_analytics_report():
    """Get comprehensive analytics report"""
    try:
        days_back = request.args.get('days', 7, type=int)
        report = analytics_engine.generate_comprehensive_report(days_back)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system/health')
@performance_tracker.track_api_call('/api/system/health')
def system_health():
    """Get system health status"""
    try:
        health = system_monitor.get_health_status()
        metrics = system_monitor.get_current_metrics()
        db_stats = db_manager.get_system_stats()
        
        return jsonify({
            "health": health,
            "metrics": metrics,
            "database": db_stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system/alerts')
@performance_tracker.track_api_call('/api/system/alerts')
def get_alerts():
    """Get system alerts"""
    try:
        severity = request.args.get('severity')
        resolved = request.args.get('resolved')
        limit = request.args.get('limit', 50, type=int)
        
        if resolved is not None:
            resolved = resolved.lower() == 'true'
        
        alerts = system_monitor.get_alerts(severity, resolved, limit)
        return jsonify({"alerts": alerts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system/performance')
@performance_tracker.track_api_call('/api/system/performance')
def get_performance():
    """Get performance report"""
    try:
        hours_back = request.args.get('hours', 24, type=int)
        report = system_monitor.get_performance_report(hours_back)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/export')
@performance_tracker.track_api_call('/api/data/export')
def export_data():
    """Export system data"""
    try:
        format_type = request.args.get('format', 'json')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_analysis_export_{timestamp}.{format_type}"
        
        if db_manager.export_data(filename, format_type):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({"error": "Export failed"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/example/demo')
@performance_tracker.track_api_call('/api/example/demo')
def demo_analysis():
    """Demo with example data"""
    try:
        video_title = "My first day in Nairobi 🚖🔥"
        video_description = "Trying out local food and matatus, what an adventure!"
        comments = [
            "😂😂 bro you look lost but it's vibes",
            "This city will eat you alive, trust me.",
            "Matatu rides >>> Uber any day",
            "Spam link: www.fakecrypto.com",
            "Karibu Kenya! We love you ❤️"
        ]
        
        result = nlp_engine.analyze_video_data(video_title, video_description, comments)
        analytics_engine.add_analysis(result)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system/stats')
@performance_tracker.track_api_call('/api/system/stats')
def system_stats():
    """Get comprehensive system statistics"""
    try:
        db_stats = db_manager.get_system_stats()
        health = system_monitor.get_health_status()
        
        # Get recent trends
        trend_data = {}
        try:
            trend_data = analytics_engine.get_trend_summary('sentiment')
        except:
            pass  # Trend data might not be available
        
        return jsonify({
            "database_stats": db_stats,
            "system_health": health,
            "trends": trend_data,
            "uptime": (datetime.now() - system_monitor.start_time).total_seconds(),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create templates directory and basic HTML templates
def create_dashboard_templates():
    """Create basic HTML templates for the dashboard"""
    
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Main dashboard template
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; }
        .header h1 { margin: 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card { background: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card h3 { color: #333; margin-bottom: 1rem; }
        .metric { display: flex; justify-content: space-between; margin: 0.5rem 0; }
        .metric-value { font-weight: bold; color: #667eea; }
        .status-healthy { color: #10b981; }
        .status-warning { color: #f59e0b; }
        .status-critical { color: #ef4444; }
        .btn { background: #667eea; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #5a67d8; }
        .demo-section { margin: 2rem 0; }
        .demo-input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; }
        .demo-output { background: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0; white-space: pre-wrap; font-family: monospace; max-height: 400px; overflow-y: auto; }
        .alert-item { padding: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #ef4444; background: #fef2f2; }
        .loading { text-align: center; color: #666; }
    </style>
</head>
<body>
    <header class="header">
        <h1>🧠 Sentiment Analysis Dashboard</h1>
        <p>Real-time monitoring and analytics for social media sentiment</p>
    </header>
    
    <div class="container">
        <!-- System Status -->
        <div class="grid">
            <div class="card">
                <h3>🚥 System Health</h3>
                <div id="system-health">
                    <div class="loading">Loading...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Quick Stats</h3>
                <div id="quick-stats">
                    <div class="loading">Loading...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>⚠️ Recent Alerts</h3>
                <div id="recent-alerts">
                    <div class="loading">Loading...</div>
                </div>
            </div>
        </div>
        
        <!-- Demo Section -->
        <div class="card demo-section">
            <h3>🎯 Live Demo - Analyze Content</h3>
            <p>Test the sentiment analysis with your own content or use the example below:</p>
            
            <div style="margin: 1rem 0;">
                <button class="btn" onclick="runDemo()">Run Example Analysis</button>
                <button class="btn" onclick="clearDemo()">Clear</button>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <label>Video Title:</label>
                    <input type="text" id="demo-title" class="demo-input" placeholder="Enter video title...">
                    
                    <label>Video Description:</label>
                    <textarea id="demo-description" class="demo-input" rows="3" placeholder="Enter video description..."></textarea>
                    
                    <label>Comments (one per line):</label>
                    <textarea id="demo-comments" class="demo-input" rows="6" placeholder="Enter comments, one per line..."></textarea>
                    
                    <button class="btn" onclick="analyzeCustom()">Analyze Custom Content</button>
                </div>
                
                <div>
                    <label>Analysis Result:</label>
                    <div id="demo-output" class="demo-output">Results will appear here...</div>
                </div>
            </div>
        </div>
        
        <!-- Analytics Section -->
        <div class="card">
            <h3>📈 Analytics Report</h3>
            <button class="btn" onclick="loadAnalytics()">Generate Report</button>
            <div id="analytics-output" class="demo-output" style="margin-top: 1rem;">
                Click "Generate Report" to see detailed analytics...
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh system status
        function loadSystemStatus() {
            fetch('/api/system/health')
                .then(response => response.json())
                .then(data => {
                    const healthDiv = document.getElementById('system-health');
                    const health = data.health;
                    
                    let statusClass = 'status-healthy';
                    if (health.health_status === 'warning' || health.health_status === 'degraded') {
                        statusClass = 'status-warning';
                    } else if (health.health_status === 'critical') {
                        statusClass = 'status-critical';
                    }
                    
                    healthDiv.innerHTML = `
                        <div class="metric">
                            <span>Status:</span>
                            <span class="${statusClass}">${health.health_status.toUpperCase()}</span>
                        </div>
                        <div class="metric">
                            <span>Health Score:</span>
                            <span class="metric-value">${health.health_score}/100</span>
                        </div>
                        <div class="metric">
                            <span>Active Alerts:</span>
                            <span class="metric-value">${health.critical_alerts + health.warning_alerts}</span>
                        </div>
                    `;
                })
                .catch(error => {
                    document.getElementById('system-health').innerHTML = '<div style="color: red;">Error loading status</div>';
                });
        }
        
        function loadQuickStats() {
            fetch('/api/system/stats')
                .then(response => response.json())
                .then(data => {
                    const statsDiv = document.getElementById('quick-stats');
                    const dbStats = data.database_stats;
                    
                    statsDiv.innerHTML = `
                        <div class="metric">
                            <span>Videos Analyzed:</span>
                            <span class="metric-value">${dbStats.total_videos_analyzed || 0}</span>
                        </div>
                        <div class="metric">
                            <span>Comments Processed:</span>
                            <span class="metric-value">${dbStats.total_comments_analyzed || 0}</span>
                        </div>
                        <div class="metric">
                            <span>Uptime:</span>
                            <span class="metric-value">${Math.round(data.uptime / 3600)}h</span>
                        </div>
                    `;
                })
                .catch(error => {
                    document.getElementById('quick-stats').innerHTML = '<div style="color: red;">Error loading stats</div>';
                });
        }
        
        function loadRecentAlerts() {
            fetch('/api/system/alerts?resolved=false&limit=5')
                .then(response => response.json())
                .then(data => {
                    const alertsDiv = document.getElementById('recent-alerts');
                    
                    if (data.alerts.length === 0) {
                        alertsDiv.innerHTML = '<div style="color: green;">✅ No active alerts</div>';
                    } else {
                        alertsDiv.innerHTML = data.alerts.map(alert => `
                            <div class="alert-item">
                                <strong>${alert.severity.toUpperCase()}</strong>: ${alert.title}
                            </div>
                        `).join('');
                    }
                })
                .catch(error => {
                    document.getElementById('recent-alerts').innerHTML = '<div style="color: red;">Error loading alerts</div>';
                });
        }
        
        function runDemo() {
            document.getElementById('demo-title').value = "My first day in Nairobi 🚖🔥";
            document.getElementById('demo-description').value = "Trying out local food and matatus, what an adventure!";
            document.getElementById('demo-comments').value = `😂😂 bro you look lost but it's vibes
This city will eat you alive, trust me.
Matatu rides >>> Uber any day
Spam link: www.fakecrypto.com
Karibu Kenya! We love you ❤️`;
            
            analyzeCustom();
        }
        
        function analyzeCustom() {
            const title = document.getElementById('demo-title').value;
            const description = document.getElementById('demo-description').value;
            const commentsText = document.getElementById('demo-comments').value;
            const comments = commentsText.split('\\n').filter(c => c.trim());
            
            if (!title && !description && comments.length === 0) {
                alert('Please enter some content to analyze');
                return;
            }
            
            document.getElementById('demo-output').textContent = 'Analyzing...';
            
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
            .then(data => {
                document.getElementById('demo-output').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('demo-output').textContent = 'Error: ' + error.message;
            });
        }
        
        function clearDemo() {
            document.getElementById('demo-title').value = '';
            document.getElementById('demo-description').value = '';
            document.getElementById('demo-comments').value = '';
            document.getElementById('demo-output').textContent = 'Results will appear here...';
        }
        
        function loadAnalytics() {
            document.getElementById('analytics-output').textContent = 'Generating report...';
            
            fetch('/api/analytics/report?days=7')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('analytics-output').textContent = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    document.getElementById('analytics-output').textContent = 'Error: ' + error.message;
                });
        }
        
        // Initialize dashboard
        loadSystemStatus();
        loadQuickStats();
        loadRecentAlerts();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            loadSystemStatus();
            loadQuickStats();
            loadRecentAlerts();
        }, 30000);
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

def run_dashboard(host='127.0.0.1', port=5000, debug=True):
    """Run the dashboard server"""
    print(f"🚀 Starting Sentiment Analysis Dashboard...")
    print(f"📊 Dashboard will be available at: http://{host}:{port}")
    print(f"🎯 Demo endpoint: http://{host}:{port}/api/example/demo")
    print(f"📈 Analytics endpoint: http://{host}:{port}/api/analytics/report")
    print(f"🚥 Health check: http://{host}:{port}/api/system/health")
    
    # Create templates
    create_dashboard_templates()
    
    # Run the Flask app
    app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == '__main__':
    # Start the dashboard
    run_dashboard(host='0.0.0.0', port=5000, debug=False)
