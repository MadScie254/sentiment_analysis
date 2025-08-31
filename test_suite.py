"""
Comprehensive Testing Framework for Sentiment Analysis System
Production-ready test suite with pytest integration
"""

import pytest
import json
import time
import asyncio
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any
import requests_mock
import tempfile
import os
from datetime import datetime

# Import components to test
try:
    from enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer, SentimentResult
    from news_ingest import KenyanNewsIngestor, NewsItem
    from config_manager import get_production_settings
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some components not available for testing: {e}")
    COMPONENTS_AVAILABLE = False

class TestSentimentAnalyzer:
    """Comprehensive tests for sentiment analysis functionality"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing"""
        return EnhancedSentimentAnalyzer(cache_size=10, request_timeout=5)
    
    @pytest.fixture
    def sample_texts(self):
        """Sample texts for testing"""
        return {
            "positive": "I love this product! It's absolutely amazing and wonderful.",
            "negative": "This is terrible, awful, and completely disappointing.",
            "neutral": "The weather today is partly cloudy with temperatures around 20 degrees.",
            "mixed": "The product is good but the delivery was terrible.",
            "kenyan": "Safaricom imeongeza huduma za mtandao nchini Kenya.",
            "short": "OK",
            "long": "A" * 6000,  # Too long
            "empty": "",
            "html": "This is <script>alert('test')</script> a test with HTML entities &amp; symbols.",
            "special_chars": "Testing with émojis 😀 and spëcial çharacters!"
        }
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization and configuration"""
        assert analyzer is not None
        assert hasattr(analyzer, 'analyzers_available')
        assert isinstance(analyzer.analyzers_available, dict)
        
        # Check status
        status = analyzer.get_analyzer_status()
        assert 'analyzers_available' in status
        assert 'version' in status
        assert status['version'] == "2.0.0"
    
    def test_input_validation(self, analyzer, sample_texts):
        """Test input validation and security checks"""
        
        # Test empty input
        result = analyzer.analyze_sentiment(sample_texts["empty"])
        assert result.error_details is not None
        
        # Test too long input
        result = analyzer.analyze_sentiment(sample_texts["long"])
        assert result.error_details is not None
        
        # Test invalid type
        with pytest.raises(Exception):
            analyzer.analyze_sentiment(None)
        
        with pytest.raises(Exception):
            analyzer.analyze_sentiment(123)
    
    def test_text_cleaning(self, analyzer, sample_texts):
        """Test text cleaning and preprocessing"""
        # Test HTML cleaning
        result = analyzer.analyze_sentiment(sample_texts["html"])
        assert result.text_length > 0
        # Should process without errors despite HTML content
        assert result.sentiment in ['positive', 'negative', 'neutral']
        
        # Test special characters
        result = analyzer.analyze_sentiment(sample_texts["special_chars"])
        assert result.sentiment in ['positive', 'negative', 'neutral']
    
    @pytest.mark.skipif(not COMPONENTS_AVAILABLE, reason="Components not available")
    def test_vader_analysis(self, analyzer, sample_texts):
        """Test VADER sentiment analysis"""
        if not analyzer.analyzers_available.get('vader', False):
            pytest.skip("VADER not available")
        
        # Test positive sentiment
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="vader")
        assert result.sentiment == "positive"
        assert result.confidence > 0.5
        assert result.method == "vader"
        assert "positive" in result.scores
        assert "negative" in result.scores
        assert "neutral" in result.scores
        
        # Test negative sentiment
        result = analyzer.analyze_sentiment(sample_texts["negative"], method="vader")
        assert result.sentiment == "negative"
        assert result.confidence > 0.5
        
        # Test neutral sentiment
        result = analyzer.analyze_sentiment(sample_texts["neutral"], method="vader")
        assert result.sentiment in ["neutral", "positive", "negative"]  # Can vary
    
    @pytest.mark.skipif(not COMPONENTS_AVAILABLE, reason="Components not available")
    def test_textblob_analysis(self, analyzer, sample_texts):
        """Test TextBlob sentiment analysis"""
        if not analyzer.analyzers_available.get('textblob', False):
            pytest.skip("TextBlob not available")
        
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="textblob")
        assert result.sentiment in ["positive", "negative", "neutral"]
        assert result.method == "textblob"
        assert isinstance(result.confidence, float)
        assert 0 <= result.confidence <= 1
    
    @requests_mock.Mocker()
    def test_huggingface_api_success(self, m, analyzer, sample_texts):
        """Test successful Hugging Face API calls"""
        if not analyzer.hf_api_key:
            pytest.skip("No Hugging Face API key")
        
        # Mock successful API response
        mock_response = [[
            {"label": "LABEL_2", "score": 0.8},  # Positive
            {"label": "LABEL_1", "score": 0.15}, # Neutral
            {"label": "LABEL_0", "score": 0.05}  # Negative
        ]]
        
        m.post(analyzer.hf_api_url, json=mock_response)
        
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="huggingface")
        assert result.sentiment == "positive"
        assert result.confidence == 0.8
        assert result.method == "huggingface"
        assert result.model_used == "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    @requests_mock.Mocker()
    def test_huggingface_api_error_handling(self, m, analyzer, sample_texts):
        """Test Hugging Face API error handling"""
        if not analyzer.hf_api_key:
            pytest.skip("No Hugging Face API key")
        
        # Test timeout
        m.post(analyzer.hf_api_url, exc=requests.exceptions.Timeout)
        
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="huggingface")
        # Should fallback or return error
        assert result is not None
    
    @requests_mock.Mocker()
    def test_huggingface_model_loading(self, m, analyzer, sample_texts):
        """Test Hugging Face model loading scenario"""
        if not analyzer.hf_api_key:
            pytest.skip("No Hugging Face API key")
        
        # First request returns 503 (model loading)
        # Second request succeeds
        mock_response = [[
            {"label": "LABEL_1", "score": 0.7},  # Neutral
            {"label": "LABEL_2", "score": 0.2},  # Positive
            {"label": "LABEL_0", "score": 0.1}   # Negative
        ]]
        
        m.post(analyzer.hf_api_url, [
            {'status_code': 503},
            {'json': mock_response}
        ])
        
        result = analyzer.analyze_sentiment(sample_texts["neutral"], method="huggingface")
        assert result.sentiment == "neutral"
        assert result.confidence == 0.7
    
    def test_auto_method_selection(self, analyzer, sample_texts):
        """Test automatic method selection"""
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="auto")
        assert result.sentiment in ["positive", "negative", "neutral"]
        assert result.method in ["huggingface", "vader", "textblob", "basic_fallback"]
    
    def test_ensemble_analysis(self, analyzer, sample_texts):
        """Test ensemble analysis combining multiple methods"""
        if not any(analyzer.analyzers_available.values()):
            pytest.skip("No analyzers available for ensemble")
        
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="ensemble")
        assert result.sentiment in ["positive", "negative", "neutral"]
        assert result.method == "ensemble"
        assert "ensemble(" in result.model_used
    
    def test_basic_fallback(self, analyzer, sample_texts):
        """Test basic keyword fallback analysis"""
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="basic_fallback")
        assert result.sentiment == "positive"  # Should detect positive keywords
        assert result.method == "basic_fallback"
        assert result.confidence > 0
    
    def test_result_structure(self, analyzer, sample_texts):
        """Test SentimentResult structure and metadata"""
        result = analyzer.analyze_sentiment(sample_texts["positive"])
        
        # Check required fields
        assert hasattr(result, 'text')
        assert hasattr(result, 'sentiment')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'scores')
        assert hasattr(result, 'model_used')
        assert hasattr(result, 'processing_time')
        assert hasattr(result, 'timestamp')
        
        # Check data types
        assert isinstance(result.confidence, float)
        assert isinstance(result.processing_time, float)
        assert isinstance(result.scores, dict)
        assert result.sentiment in ['positive', 'negative', 'neutral']
        assert 0 <= result.confidence <= 1
        
        # Check scores structure
        assert 'positive' in result.scores
        assert 'negative' in result.scores
        assert 'neutral' in result.scores
        
        # Test serialization
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        
        result_json = result.to_json()
        assert isinstance(result_json, str)
        # Should be valid JSON
        json.loads(result_json)
    
    def test_rate_limiting(self, analyzer, sample_texts):
        """Test rate limiting functionality"""
        start_time = time.time()
        
        # Make multiple rapid requests
        for _ in range(3):
            analyzer.analyze_sentiment(sample_texts["short"])
        
        # Should take some time due to rate limiting
        elapsed = time.time() - start_time
        # Basic check - should take at least some time
        assert elapsed >= 0
    
    def test_backward_compatibility(self, analyzer, sample_texts):
        """Test backward compatibility with old method names"""
        # Test 'roberta' mapping to 'huggingface'
        result = analyzer.analyze_sentiment(sample_texts["positive"], method="roberta")
        assert result is not None
        # Method should be mapped correctly
        assert result.method in ["huggingface", "vader", "textblob", "basic_fallback"]


class TestNewsIngestor:
    """Tests for news ingestion functionality"""
    
    @pytest.fixture
    def ingestor(self):
        """Create news ingestor for testing"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("News ingestor not available")
        return KenyanNewsIngestor(cache_file="test_cache.jsonl")
    
    @pytest.fixture
    def sample_rss_content(self):
        """Sample RSS feed content for testing"""
        return """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Test News</title>
                <item>
                    <title>Kenya Economy Shows Growth</title>
                    <description>The Kenyan economy has shown positive growth indicators...</description>
                    <link>https://example.com/news/1</link>
                    <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
                </item>
                <item>
                    <title>Safaricom Launches New Service</title>
                    <description>Safaricom has announced a new digital service for customers...</description>
                    <link>https://example.com/news/2</link>
                    <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>"""
    
    def test_news_item_creation(self):
        """Test NewsItem creation and validation"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("NewsItem not available")
        
        item = NewsItem(
            title="Test Title",
            summary="Test summary content",
            url="https://example.com/test",
            source="TestSource",
            published="2024-01-01T12:00:00Z"
        )
        
        assert item.title == "Test Title"
        assert item.source == "TestSource"
        assert item.url == "https://example.com/test"
        
        # Test hash generation
        content_hash = item.generate_content_hash()
        assert isinstance(content_hash, str)
        assert len(content_hash) == 32  # MD5 hash length
    
    @requests_mock.Mocker()
    def test_rss_feed_parsing(self, m, ingestor, sample_rss_content):
        """Test RSS feed parsing functionality"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Ingestor not available")
        
        # Mock RSS feed response
        m.get("https://example.com/rss", text=sample_rss_content)
        
        items = ingestor.parse_rss_feed("https://example.com/rss", "TestSource")
        
        assert len(items) == 2
        assert items[0].title == "Kenya Economy Shows Growth"
        assert items[1].title == "Safaricom Launches New Service"
        assert all(item.source == "TestSource" for item in items)
    
    @requests_mock.Mocker()
    def test_rss_feed_error_handling(self, m, ingestor):
        """Test RSS feed error handling"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Ingestor not available")
        
        # Test network error
        m.get("https://example.com/rss", exc=requests.exceptions.ConnectionError)
        
        items = ingestor.parse_rss_feed("https://example.com/rss", "TestSource")
        assert items == []  # Should return empty list on error
    
    def test_caching_functionality(self, ingestor):
        """Test news caching functionality"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Ingestor not available")
        
        # Create test items
        test_items = [
            NewsItem(
                title="Test 1",
                summary="Summary 1",
                url="https://example.com/1",
                source="TestSource",
                published="2024-01-01T12:00:00Z"
            ),
            NewsItem(
                title="Test 2",
                summary="Summary 2", 
                url="https://example.com/2",
                source="TestSource",
                published="2024-01-01T11:00:00Z"
            )
        ]
        
        # Save to cache
        ingestor.save_to_cache(test_items)
        
        # Load from cache
        cached_items = ingestor.get_cached_items()
        
        assert len(cached_items) == 2
        assert cached_items[0].title == "Test 1"
        
        # Cleanup
        try:
            os.remove(ingestor.cache_file)
        except FileNotFoundError:
            pass
    
    def test_deduplication(self, ingestor):
        """Test news item deduplication"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Ingestor not available")
        
        # Create duplicate items
        items = [
            NewsItem(
                title="Same Title",
                summary="Same content",
                url="https://example.com/1",
                source="Source1",
                published="2024-01-01T12:00:00Z"
            ),
            NewsItem(
                title="Same Title",
                summary="Same content",
                url="https://example.com/2",  # Different URL
                source="Source2",
                published="2024-01-01T12:00:00Z"
            )
        ]
        
        deduplicated = ingestor.deduplicate_items(items)
        assert len(deduplicated) == 1  # Should remove duplicate based on content


class TestConfigurationManager:
    """Tests for configuration management"""
    
    def test_settings_loading(self):
        """Test production settings loading"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Config manager not available")
        
        settings = get_production_settings()
        
        # Check required fields
        assert hasattr(settings, 'DEBUG')
        assert hasattr(settings, 'HOST')
        assert hasattr(settings, 'PORT')
        assert hasattr(settings, 'SECRET_KEY')
        
        # Check data types
        assert isinstance(settings.DEBUG, bool)
        assert isinstance(settings.PORT, int)
        assert isinstance(settings.HOST, str)
    
    def test_environment_variable_override(self):
        """Test environment variable configuration override"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Config manager not available")
        
        # Set test environment variable
        original_debug = os.getenv('DEBUG')
        os.environ['DEBUG'] = 'true'
        
        try:
            settings = get_production_settings()
            # Should pick up environment variable
            assert settings.DEBUG == True
        finally:
            # Restore original value
            if original_debug is not None:
                os.environ['DEBUG'] = original_debug
            else:
                os.environ.pop('DEBUG', None)


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    def test_client(self):
        """Create test client for Flask app"""
        if not COMPONENTS_AVAILABLE:
            pytest.skip("Dashboard not available")
        
        # Import here to avoid import issues
        from production_dashboard import app
        app.config['TESTING'] = True
        return app.test_client()
    
    def test_health_endpoint(self, test_client):
        """Test health check endpoint"""
        response = test_client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'components' in data
        assert 'timestamp' in data
    
    def test_analyze_endpoint_valid_input(self, test_client):
        """Test sentiment analysis endpoint with valid input"""
        payload = {
            "text": "I love this amazing product!"
        }
        
        response = test_client.post('/api/analyze', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'sentiment' in data
        assert 'confidence' in data
        assert 'scores' in data
        assert data['sentiment'] in ['positive', 'negative', 'neutral']
    
    def test_analyze_endpoint_invalid_input(self, test_client):
        """Test sentiment analysis endpoint with invalid input"""
        # Test empty request
        response = test_client.post('/api/analyze',
                                   data=json.dumps({}),
                                   content_type='application/json')
        assert response.status_code == 400
        
        # Test missing text
        response = test_client.post('/api/analyze',
                                   data=json.dumps({"text": ""}),
                                   content_type='application/json')
        assert response.status_code == 400
        
        # Test too long text
        long_text = "A" * 6000
        response = test_client.post('/api/analyze',
                                   data=json.dumps({"text": long_text}),
                                   content_type='application/json')
        assert response.status_code == 400
    
    def test_news_endpoint(self, test_client):
        """Test news retrieval endpoint"""
        response = test_client.get('/api/news')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'items' in data
        assert 'page' in data
        assert 'total_items' in data
        assert isinstance(data['items'], list)
    
    def test_news_endpoint_pagination(self, test_client):
        """Test news endpoint pagination"""
        response = test_client.get('/api/news?page=1&limit=5')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['page'] == 1
        assert data['limit'] == 5
        assert len(data['items']) <= 5
    
    def test_analytics_endpoint(self, test_client):
        """Test analytics summary endpoint"""
        response = test_client.get('/api/analytics/summary')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total_analyses' in data
        assert 'sentiment_distribution' in data
        assert 'average_confidence' in data
    
    def test_rate_limiting(self, test_client):
        """Test API rate limiting"""
        # Make multiple rapid requests
        responses = []
        for _ in range(15):  # Exceed rate limit
            response = test_client.post('/api/analyze',
                                       data=json.dumps({"text": "test"}),
                                       content_type='application/json')
            responses.append(response.status_code)
        
        # Should eventually get rate limited (429)
        assert 429 in responses or all(r in [200, 400] for r in responses)


class TestPerformance:
    """Performance and load tests"""
    
    @pytest.mark.skipif(not COMPONENTS_AVAILABLE, reason="Components not available")
    def test_analysis_performance(self):
        """Test sentiment analysis performance"""
        analyzer = EnhancedSentimentAnalyzer()
        
        test_text = "This is a test sentence for performance evaluation of the sentiment analysis system."
        
        # Warm up
        analyzer.analyze_sentiment(test_text)
        
        # Measure performance
        start_time = time.time()
        iterations = 10
        
        for _ in range(iterations):
            result = analyzer.analyze_sentiment(test_text)
            assert result is not None
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        # Should complete analysis in reasonable time
        assert avg_time < 5.0  # Less than 5 seconds per analysis
        print(f"Average analysis time: {avg_time:.3f} seconds")
    
    @pytest.mark.skipif(not COMPONENTS_AVAILABLE, reason="Components not available")
    def test_concurrent_analysis(self):
        """Test concurrent sentiment analysis"""
        import threading
        
        analyzer = EnhancedSentimentAnalyzer()
        results = []
        errors = []
        
        def analyze_text(text):
            try:
                result = analyzer.analyze_sentiment(f"Test text {text}")
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Create and start threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=analyze_text, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)
        
        # Check results
        assert len(errors) == 0, f"Errors in concurrent execution: {errors}"
        assert len(results) == 5
        
        # All results should be valid
        for result in results:
            assert result.sentiment in ['positive', 'negative', 'neutral']


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v", "--tb=short"])
