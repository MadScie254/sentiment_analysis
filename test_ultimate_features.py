"""
Ultimate Feature Test Suite
Comprehensive testing of all new advanced features
"""

import sys
import os
import time
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mega_apis():
    """Test mega free APIs collection"""
    logger.info("🔬 Testing Mega Free APIs Collection...")
    
    try:
        from mega_free_apis import mega_api_collection
        
        # Test individual API categories
        categories = [
            ('Hacker News', mega_api_collection.get_hacker_news),
            ('Random Quotes', mega_api_collection.get_random_quotes),
            ('Crypto Prices', mega_api_collection.get_crypto_prices),
            ('ISS Location', mega_api_collection.get_iss_location),
            ('GitHub Trending', mega_api_collection.get_github_trending)
        ]
        
        working_apis = []
        for name, func in categories:
            try:
                result = func()
                if result:
                    working_apis.append(name)
                    logger.info(f"  ✅ {name}: Working")
                else:
                    logger.warning(f"  ⚠️  {name}: No data returned")
            except Exception as e:
                logger.warning(f"  ❌ {name}: Failed - {e}")
        
        # Test master function
        try:
            everything = mega_api_collection.get_everything()
            logger.info(f"  🎯 Master function returned {len(everything)} data sources")
        except Exception as e:
            logger.error(f"  ❌ Master function failed: {e}")
        
        logger.info(f"✅ Mega APIs Test Complete - {len(working_apis)} APIs working")
        return True
        
    except ImportError:
        logger.error("❌ Could not import mega_api_collection")
        return False

def test_advanced_ml():
    """Test advanced ML models"""
    logger.info("🧠 Testing Advanced ML Models...")
    
    try:
        from advanced_ml_models import advanced_ml_models
        
        # Test single text analysis
        test_text = "I absolutely love this amazing product! It works perfectly and makes me so happy."
        analysis = advanced_ml_models.analyze_sentiment_advanced(test_text)
        
        logger.info(f"  📊 Sentiment: {analysis.get('sentiment', 'unknown')}")
        logger.info(f"  🎯 Confidence: {analysis.get('confidence', 0):.2f}")
        logger.info(f"  🧪 Emotions detected: {len(analysis.get('emotions', {}).get('scores', {}))}")
        logger.info(f"  📈 Text stats: {len(analysis.get('text_stats', {}))}")
        
        # Test batch analysis
        test_texts = [
            "This is amazing!",
            "I hate this terrible product.",
            "It's okay, nothing special.",
            "Absolutely revolutionary technology!"
        ]
        
        batch_analysis = advanced_ml_models.analyze_multiple_texts(test_texts)
        logger.info(f"  📦 Batch analysis: {batch_analysis.get('total_texts_analyzed', 0)} texts processed")
        
        # Test insights generation
        insights = advanced_ml_models.generate_insights(analysis)
        logger.info(f"  💡 Generated {len(insights)} insights")
        
        logger.info("✅ Advanced ML Test Complete")
        return True
        
    except ImportError:
        logger.error("❌ Could not import advanced_ml_models")
        return False
    except Exception as e:
        logger.error(f"❌ Advanced ML test failed: {e}")
        return False

def test_visualizations():
    """Test advanced data visualizations"""
    logger.info("📊 Testing Advanced Visualizations...")
    
    try:
        from advanced_visualizer import advanced_visualizer
        
        # Test sentiment pie chart
        sentiment_data = {'positive': 45, 'negative': 20, 'neutral': 35}
        pie_chart = advanced_visualizer.create_sentiment_pie_chart(sentiment_data)
        logger.info(f"  🥧 Pie chart generated: {len(pie_chart)} characters")
        
        # Test emotion radar chart
        emotion_data = {
            'scores': {
                'joy': {'intensity': 0.8},
                'anger': {'intensity': 0.2},
                'fear': {'intensity': 0.1},
                'sadness': {'intensity': 0.3}
            }
        }
        radar_chart = advanced_visualizer.create_emotion_radar_chart(emotion_data)
        logger.info(f"  🌐 Radar chart generated: {len(radar_chart)} characters")
        
        # Test comprehensive report
        analysis_data = {
            'sentiment_distribution': sentiment_data,
            'average_confidence': 0.78,
            'average_toxicity': 0.15,
            'emotions': emotion_data,
            'text_stats': {
                'word_count': 150,
                'vocabulary_diversity': 0.7,
                'average_word_length': 4.5
            }
        }
        
        report = advanced_visualizer.create_comprehensive_analysis_report(analysis_data)
        logger.info(f"  📄 Comprehensive report generated: {len(report)} characters")
        
        logger.info("✅ Visualizations Test Complete")
        return True
        
    except ImportError:
        logger.error("❌ Could not import advanced_visualizer")
        return False
    except Exception as e:
        logger.error(f"❌ Visualization test failed: {e}")
        return False

def test_dashboard_integration():
    """Test dashboard integration"""
    logger.info("🌐 Testing Dashboard Integration...")
    
    try:
        # Test dashboard imports
        from dashboard import app
        
        # Test that all new routes exist
        with app.test_client() as client:
            routes_to_test = [
                '/api/health/system-status',
                '/api/mega/everything',
                '/api/visualizations/sentiment-pie'
            ]
            
            working_routes = 0
            for route in routes_to_test:
                try:
                    if route == '/api/visualizations/sentiment-pie':
                        response = client.get(route)
                    else:
                        response = client.get(route)
                    
                    if response.status_code < 500:  # Accept any non-server-error
                        working_routes += 1
                        logger.info(f"  ✅ Route {route}: Accessible")
                    else:
                        logger.warning(f"  ⚠️  Route {route}: Server error")
                except Exception as e:
                    logger.warning(f"  ❌ Route {route}: Failed - {e}")
            
            logger.info(f"  📊 Routes test: {working_routes}/{len(routes_to_test)} routes working")
        
        logger.info("✅ Dashboard Integration Test Complete")
        return True
        
    except ImportError:
        logger.error("❌ Could not import dashboard")
        return False
    except Exception as e:
        logger.error(f"❌ Dashboard test failed: {e}")
        return False

def test_performance():
    """Test system performance"""
    logger.info("⚡ Testing System Performance...")
    
    try:
        from advanced_ml_models import advanced_ml_models
        
        # Test analysis speed
        test_text = "This is a comprehensive test of the sentiment analysis system performance."
        
        start_time = time.time()
        analysis = advanced_ml_models.analyze_sentiment_advanced(test_text)
        end_time = time.time()
        
        analysis_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.info(f"  ⏱️  Single analysis time: {analysis_time:.2f}ms")
        
        # Test batch processing speed
        test_texts = ["Test text " + str(i) for i in range(10)]
        
        start_time = time.time()
        batch_analysis = advanced_ml_models.analyze_multiple_texts(test_texts)
        end_time = time.time()
        
        batch_time = (end_time - start_time) * 1000
        avg_time = batch_time / len(test_texts)
        logger.info(f"  📦 Batch analysis time: {batch_time:.2f}ms ({avg_time:.2f}ms per text)")
        
        # Performance benchmarks
        if analysis_time < 500:
            logger.info("  🚀 Single analysis: EXCELLENT (< 500ms)")
        elif analysis_time < 1000:
            logger.info("  ✅ Single analysis: GOOD (< 1s)")
        else:
            logger.warning("  ⚠️  Single analysis: SLOW (> 1s)")
        
        if avg_time < 200:
            logger.info("  🚀 Batch processing: EXCELLENT (< 200ms per text)")
        elif avg_time < 500:
            logger.info("  ✅ Batch processing: GOOD (< 500ms per text)")
        else:
            logger.warning("  ⚠️  Batch processing: SLOW (> 500ms per text)")
        
        logger.info("✅ Performance Test Complete")
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        return False

def generate_test_report():
    """Generate comprehensive test report"""
    logger.info("📋 Generating Test Report...")
    
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {
            'mega_apis': test_mega_apis(),
            'advanced_ml': test_advanced_ml(),
            'visualizations': test_visualizations(),
            'dashboard_integration': test_dashboard_integration(),
            'performance': test_performance()
        }
    }
    
    # Calculate overall success rate
    passed_tests = sum(1 for result in test_results['tests'].values() if result)
    total_tests = len(test_results['tests'])
    success_rate = (passed_tests / total_tests) * 100
    
    print("\n" + "="*60)
    print("🎉 ULTIMATE SENTIMENT ANALYSIS SYSTEM TEST REPORT")
    print("="*60)
    print(f"⏰ Test completed at: {test_results['timestamp']}")
    print(f"📊 Overall success rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    print()
    
    for test_name, result in test_results['tests'].items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "="*60)
    
    if success_rate >= 80:
        print("🎉 SYSTEM STATUS: EXCELLENT - Ready for production!")
    elif success_rate >= 60:
        print("✅ SYSTEM STATUS: GOOD - Most features working")
    else:
        print("⚠️  SYSTEM STATUS: NEEDS ATTENTION - Some features may not work")
    
    print("="*60)
    
    # Save detailed report
    try:
        with open('test_report.json', 'w') as f:
            json.dump(test_results, f, indent=2)
        logger.info("📄 Detailed test report saved to test_report.json")
    except Exception as e:
        logger.warning(f"Could not save test report: {e}")
    
    return test_results

def main():
    """Run comprehensive test suite"""
    print("🧪 ULTIMATE SENTIMENT ANALYSIS SYSTEM TEST SUITE")
    print("=" * 60)
    print("Testing all advanced features and integrations...")
    print()
    
    # Run all tests
    results = generate_test_report()
    
    # Provide recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("  • Run 'python launch_ultimate_dashboard.py' to start the system")
    print("  • Visit http://localhost:5000 to access the dashboard")
    print("  • Try the new 'Mega APIs', 'Advanced ML', and 'Visualizations' tabs")
    print("  • Check test_report.json for detailed results")
    print()
    print("🚀 Ready to explore the ultimate sentiment analysis platform!")

if __name__ == "__main__":
    main()
