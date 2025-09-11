"""
Simple Ultimate Dashboard Launcher
Launch the enhanced sentiment analysis dashboard with dependency checking
"""

import sys
import os
import subprocess
import logging

# Simple logging without emojis
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def install_required_packages():
    """Install only the most essential packages"""
    essential_packages = [
        "flask==2.3.3",
        "flask-cors==4.0.0", 
        "requests==2.31.0",
        "nltk==3.8.1",
        "vaderSentiment==3.3.2",
        "textblob==0.17.1",
        "numpy==1.24.3",
        "matplotlib==3.7.2",
        "seaborn==0.12.2",
        "textstat==0.7.3",
        "feedparser==6.0.10",
        "beautifulsoup4==4.12.2"
    ]
    
    logger.info("Installing essential packages...")
    
    for package in essential_packages:
        try:
            logger.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            logger.warning(f"Failed to install {package}, continuing...")
    
    logger.info("Essential packages installation completed")

def test_basic_imports():
    """Test if we can import basic components"""
    logger.info("Testing basic imports...")
    
    try:
        import flask
        logger.info("Flask: OK")
        
        import nltk
        logger.info("NLTK: OK")
        
        import matplotlib
        logger.info("Matplotlib: OK")
        
        # Download NLTK data
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logger.info("NLTK data: OK")
        
        logger.info("Basic imports: SUCCESS")
        return True
        
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False

def launch_dashboard():
    """Launch the dashboard"""
    logger.info("Starting Ultimate Sentiment Analysis Dashboard...")
    
    try:
        # Import and run the dashboard
        from dashboard import app
        
        logger.info("Dashboard loaded successfully!")
        logger.info("Starting server on http://localhost:5000")
        logger.info("Features available:")
        logger.info("  - Enhanced Sentiment Analysis")
        logger.info("  - Advanced ML Models (if dependencies available)")
        logger.info("  - Data Visualizations")
        logger.info("  - Multiple Free APIs")
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        logger.error(f"Could not import dashboard: {e}")
        logger.info("Try running: pip install -r requirements.txt")
    except Exception as e:
        logger.error(f"Dashboard launch failed: {e}")

def main():
    """Main launcher"""
    print("=" * 60)
    print("ULTIMATE SENTIMENT ANALYSIS DASHBOARD")
    print("=" * 60)
    
    # Step 1: Install essential packages
    install_required_packages()
    
    # Step 2: Test basic imports
    if not test_basic_imports():
        logger.error("Basic imports failed. Please install dependencies manually.")
        logger.info("Try: pip install flask nltk matplotlib requests")
        return
    
    # Step 3: Launch dashboard
    logger.info("All systems ready!")
    launch_dashboard()

if __name__ == "__main__":
    main()
