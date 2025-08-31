#!/usr/bin/env python3
"""
Minimal Dashboard Test - Real APIs
"""

import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Simple sentiment analyzer using Hugging Face API
def analyze_sentiment_simple(text):
    """Simple sentiment analysis using Hugging Face API"""
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        return {"error": "No API key"}
    
    try:
        url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"inputs": text}
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                sentiment_data = result[0]
                # Convert to our format
                sentiment_map = {
                    'LABEL_0': 'negative',
                    'LABEL_1': 'neutral', 
                    'LABEL_2': 'positive'
                }
                
                best_result = max(sentiment_data, key=lambda x: x['score'])
                sentiment = sentiment_map.get(best_result['label'], 'neutral')
                
                return {
                    "sentiment": sentiment,
                    "confidence": round(best_result['score'], 3),
                    "text": text,
                    "model_used": "huggingface_api",
                    "scores": {item['label']: round(item['score'], 3) for item in sentiment_data}
                }
        
        return {"error": f"API error: {response.status_code}"}
    
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

# Simple news fetcher using NewsAPI
def get_news_simple():
    """Simple news fetcher using NewsAPI"""
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        return {"error": "No NewsAPI key"}
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            # Format articles
            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'title': article.get('title', 'No title'),
                    'summary': article.get('description', 'No description'),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'published_at': article.get('publishedAt', ''),
                    'image_url': article.get('urlToImage', '')
                })
            
            return {"articles": formatted_articles, "count": len(formatted_articles)}
        
        return {"error": f"NewsAPI error: {response.status_code}"}
    
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>🎯 Real API Sentiment Dashboard</h1>
    <p>Test endpoints:</p>
    <ul>
        <li><a href="/api/test">/api/test</a> - Test API connection</li>
        <li><a href="/api/news">/api/news</a> - Get real news</li>
        <li>POST /api/analyze - Analyze sentiment</li>
    </ul>
    
    <h3>Test Sentiment Analysis:</h3>
    <script>
    function testSentiment() {
        const text = document.getElementById('textInput').value;
        fetch('/api/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        })
        .then(r => r.json())
        .then(data => {
            document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        });
    }
    </script>
    
    <input type="text" id="textInput" placeholder="Enter text to analyze" value="I love this product!">
    <button onclick="testSentiment()">Analyze</button>
    <div id="result"></div>
    """

@app.route('/api/test')
def api_test():
    """Test API keys and connectivity"""
    keys = {
        'HUGGINGFACE_API_KEY': bool(os.getenv('HUGGINGFACE_API_KEY')),
        'NEWSAPI_KEY': bool(os.getenv('NEWSAPI_KEY')),
        'GNEWS_API_KEY': bool(os.getenv('GNEWS_API_KEY')),
        'CURRENTS_API_KEY': bool(os.getenv('CURRENTS_API_KEY')),
        'TWITTER_API_KEY': bool(os.getenv('TWITTER_API_KEY'))
    }
    
    return jsonify({
        'status': 'ok',
        'api_keys_present': keys,
        'message': 'Real API Dashboard is working!'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze sentiment using real Hugging Face API"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = analyze_sentiment_simple(text)
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'text': result['text'],
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'model_used': result['model_used'],
            'scores': result.get('scores', {}),
            'api_used': 'huggingface'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news')
def news():
    """Get real news using NewsAPI"""
    try:
        result = get_news_simple()
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'items': result['articles'],
            'total_items': result['count'],
            'source': 'NewsAPI'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Real API Dashboard...")
    print(f"🔑 API Keys Available:")
    print(f"   Hugging Face: {'✅' if os.getenv('HUGGINGFACE_API_KEY') else '❌'}")
    print(f"   NewsAPI: {'✅' if os.getenv('NEWSAPI_KEY') else '❌'}")
    print(f"   GNews: {'✅' if os.getenv('GNEWS_API_KEY') else '❌'}")
    print(f"   Currents: {'✅' if os.getenv('CURRENTS_API_KEY') else '❌'}")
    print(f"   Twitter: {'✅' if os.getenv('TWITTER_API_KEY') else '❌'}")
    print("\n🌐 Dashboard will be available at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
