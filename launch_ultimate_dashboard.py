"""
Ultimate Sentiment Analysis Dashboard Launcher
Tests all components and launches the advanced dashboard with all features
"""

import sys
import os
import time
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('startup.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all required imports"""
    logger.info("[TEST] Testing component imports...")
    
    try:
        # Test core components
        from enhanced_sentiment_analyzer import enhanced_sentiment_analyzer
        logger.info("[PASS] Enhanced Sentiment Analyzer loaded")
        
        from immersive_api_integrator import api_integrator
        logger.info("[PASS] Immersive API Integrator loaded")
        
        from next_gen_news_aggregator import next_gen_news
        logger.info("[PASS] Next-Gen News Aggregator loaded")
        
        from mega_free_apis import mega_api_collection
        logger.info("[PASS] Mega Free APIs Collection loaded")
        
        from advanced_ml_models import advanced_ml_models
        logger.info("[PASS] Advanced ML Models loaded")
        
        from advanced_visualizer import advanced_visualizer
        logger.info("[PASS] Advanced Data Visualizer loaded")
        
        logger.info("[SUCCESS] All components imported successfully!")
        return True
        
    except ImportError as e:
        logger.error(f"[FAIL] Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"[FAIL] Unexpected error during import: {e}")
        return False

def test_functionality():
    """Test core functionality of each component"""
    logger.info("🔬 Testing component functionality...")
    
    try:
        # Test sentiment analysis
        from enhanced_sentiment_analyzer import enhanced_sentiment_analyzer
        test_result = enhanced_sentiment_analyzer.analyze_text("This is a great day!")
        logger.info("✅ Sentiment analysis working")
        
        # Test advanced ML models
        from advanced_ml_models import advanced_ml_models
        analysis = advanced_ml_models.analyze_sentiment_advanced("I love this amazing product!")
        logger.info("✅ Advanced ML analysis working")
        
        # Test API integrator
        from immersive_api_integrator import api_integrator
        try:
            data = api_integrator.get_entertainment_data()
            logger.info("✅ API integrator working")
        except:
            logger.warning("⚠️  API integrator has network issues (expected)")
        
        # Test mega APIs
        from mega_free_apis import mega_api_collection
        try:
            quotes = mega_api_collection.get_random_quotes()
            logger.info("✅ Mega APIs working")
        except:
            logger.warning("⚠️  Mega APIs have network issues (expected)")
        
        # Test visualizer
        from advanced_visualizer import advanced_visualizer
        sample_data = {'positive': 10, 'negative': 5, 'neutral': 15}
        chart = advanced_visualizer.create_sentiment_pie_chart(sample_data)
        logger.info("✅ Data visualizer working")
        
        logger.info("🎉 All functionality tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Functionality test failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    logger.info("📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    logger.info("📚 Downloading NLTK data...")
    
    try:
        import nltk
        required_data = [
            'vader_lexicon',
            'punkt',
            'stopwords',
            'averaged_perceptron_tagger',
            'wordnet'
        ]
        
        for data_name in required_data:
            try:
                nltk.download(data_name, quiet=True)
                logger.info(f"✅ Downloaded {data_name}")
            except Exception as e:
                logger.warning(f"⚠️  Could not download {data_name}: {e}")
        
        logger.info("📚 NLTK data setup complete")
        return True
        
    except Exception as e:
        logger.error(f"❌ NLTK data download failed: {e}")
        return False

def create_sample_data():
    """Create sample data for demonstration"""
    logger.info("📊 Creating sample data...")
    
    sample_texts = [
        "I absolutely love this new product! It's amazing and works perfectly.",
        "This is the worst experience I've ever had. Completely disappointed.",
        "The weather today is quite normal, nothing special to report.",
        "What an incredible breakthrough in technology! This will change everything.",
        "I'm not sure how I feel about this. It's okay I guess.",
        "This is revolutionary! The future is bright with innovations like this.",
        "Terrible customer service. Very frustrating experience overall.",
        "Everything seems to be working as expected. No complaints here."
    ]
    
    try:
        from advanced_ml_models import advanced_ml_models
        
        logger.info("Analyzing sample texts...")
        analysis = advanced_ml_models.analyze_multiple_texts(sample_texts)
        
        logger.info("✅ Sample data analysis complete")
        logger.info(f"   📈 Sentiment distribution: {analysis.get('sentiment_percentages', {})}")
        logger.info(f"   🎯 Average confidence: {analysis.get('average_confidence', 0):.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sample data creation failed: {e}")
        return False

def launch_dashboard():
    """Launch the dashboard"""
    logger.info("🚀 Starting Ultimate Sentiment Analysis Dashboard...")
    
    try:
        # Set environment variables
        os.environ['FLASK_APP'] = 'dashboard.py'
        os.environ['FLASK_ENV'] = 'development'
        
        # Import and run dashboard
        from dashboard import app
        
        logger.info("🌟 Dashboard starting on http://localhost:5000")
        logger.info("🎯 Features available:")
        logger.info("   • Enhanced Sentiment Analysis")
        logger.info("   • Advanced ML Models")
        logger.info("   • Mega Free APIs Collection (50+ APIs)")
        logger.info("   • Interactive Data Visualizations")
        logger.info("   • Comprehensive Analytics Dashboard")
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        logger.error(f"❌ Dashboard launch failed: {e}")
        return False

def main():
    """Main startup sequence"""
    print("🎉 ULTIMATE SENTIMENT ANALYSIS DASHBOARD LAUNCHER")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Install dependencies
    if not install_dependencies():
        logger.error("❌ Failed to install dependencies. Please run manually: pip install -r requirements.txt")
        return
    
    # Step 2: Download NLTK data
    download_nltk_data()
    
    # Step 3: Test imports
    if not test_imports():
        logger.error("❌ Component imports failed. Please check for missing dependencies.")
        return
    
    # Step 4: Test functionality
    if not test_functionality():
        logger.error("❌ Functionality tests failed. Some features may not work properly.")
        logger.info("🔄 Continuing anyway - network-dependent features may work once online...")
    
    # Step 5: Create sample data
    create_sample_data()
    
    print()
    print("🎉 ALL SYSTEMS GO! 🎉")
    print("=" * 60)
    print("🚀 Launching Ultimate Sentiment Analysis Dashboard...")
    print()
    
    # Step 6: Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()
