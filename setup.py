#!/usr/bin/env python3
"""
Setup script for the sentiment analysis system
Downloads required data and configures the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install Python packages from requirements.txt"""
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        
        # Download required NLTK data
        nltk_downloads = [
            'punkt',
            'vader_lexicon',
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger'
        ]
        
        for item in nltk_downloads:
            try:
                nltk.download(item, quiet=True)
                print(f"   ✓ Downloaded {item}")
            except Exception as e:
                print(f"   ⚠️  Warning: Could not download {item}: {e}")
        
        print("✅ NLTK data download completed!")
        return True
    except ImportError:
        print("❌ NLTK not installed. Please install requirements first.")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    required_modules = [
        'nltk',
        'textblob',
        'vaderSentiment',
        'sklearn',
        'numpy',
        'pandas',
        'emoji'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✓ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required modules imported successfully!")
        return True

def run_system_test():
    """Run a quick system test"""
    print("🧪 Running system test...")
    
    try:
        # Import our modules
        from nlp_engine import NLPEngine
        
        # Create engine instance
        engine = NLPEngine()
        
        # Test with simple input
        test_result = engine.quick_analyze("This is a test message! 😊")
        
        # Check if we got expected output structure
        required_keys = ['text', 'sentiment', 'emotions', 'tag']
        if all(key in test_result for key in required_keys):
            print("✅ System test passed!")
            print(f"   Test result: {test_result['sentiment']} sentiment detected")
            return True
        else:
            print("❌ System test failed - unexpected output structure")
            return False
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def create_example_script():
    """Create an example usage script"""
    print("📝 Creating example script...")
    
    example_script = '''#!/usr/bin/env python3
"""
Example usage of the sentiment analysis system
"""

import json
from nlp_engine import NLPEngine

def main():
    print("🚀 Sentiment Analysis System - Example Usage")
    print("=" * 50)
    
    # Initialize the NLP engine
    engine = NLPEngine()
    
    # Example 1: Quick text analysis
    print("\\n📝 Example 1: Quick Text Analysis")
    text = "I love this place! It's amazing 😍"
    result = engine.quick_analyze(text)
    print(f"Text: {text}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Example 2: Video data analysis (from the prompt)
    print("\\n📺 Example 2: Video Data Analysis")
    video_title = "My first day in Nairobi 🚖🔥"
    video_description = "Trying out local food and matatus, what an adventure!"
    comments = [
        "😂😂 bro you look lost but it's vibes",
        "This city will eat you alive, trust me.",
        "Matatu rides >>> Uber any day",
        "Spam link: www.fakecrypto.com",
        "Karibu Kenya! We love you ❤️"
    ]
    
    result = engine.analyze_video_data(video_title, video_description, comments)
    
    # Format as requested in the prompt
    formatted_result = {
        "video_sentiment": result["video_sentiment"],
        "video_emotion": result["video_emotion"],
        "comments": [
            {
                "text": comment["text"],
                "sentiment": comment["sentiment"],
                "emotion": comment["emotion"],
                "tag": comment["tag"]
            }
            for comment in result["comments"]
        ]
    }
    
    print("Result:")
    print(json.dumps(formatted_result, indent=2, ensure_ascii=False))
    
    # Example 3: Batch comment analysis
    print("\\n💬 Example 3: Batch Comment Analysis")
    test_comments = [
        "This is hilarious! 😂😂😂",
        "You're amazing, keep it up! ❤️",
        "This is terrible and stupid",
        "Free money here: www.scam.com",
        "Very insightful analysis, thanks for sharing your perspective"
    ]
    
    batch_results = engine.batch_analyze_comments(test_comments)
    for i, result in enumerate(batch_results):
        print(f"Comment {i+1}: {result['tag']} ({result['sentiment']})")
    
    print("\\n✅ Example completed!")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open("example_usage.py", "w", encoding="utf-8") as f:
            f.write(example_script)
        print("✅ Example script created: example_usage.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create example script: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Sentiment Analysis System - Setup")
    print("=" * 50)
    print("This script will set up your sentiment analysis environment.")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Please run this script from the project directory.")
        sys.exit(1)
    
    success_count = 0
    total_steps = 5
    
    # Step 1: Install requirements
    if install_requirements():
        success_count += 1
    
    # Step 2: Download NLTK data
    if download_nltk_data():
        success_count += 1
    
    # Step 3: Test imports
    if test_imports():
        success_count += 1
    
    # Step 4: Run system test
    if run_system_test():
        success_count += 1
    
    # Step 5: Create example script
    if create_example_script():
        success_count += 1
    
    # Final summary
    print("\\n" + "=" * 50)
    print(f"Setup completed: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        print("🎉 Setup completed successfully!")
        print("\\n📋 Next Steps:")
        print("1. Run the example: python example_usage.py")
        print("2. Run tests: python test_system.py")
        print("3. Start the API server: python api_server.py")
        print("4. Or use the simple API: python simple_api.py")
        print("\\n📚 Usage:")
        print("- Import NLPEngine for direct usage")
        print("- Use SimpleAPI for JSON-based processing")
        print("- Use FastAPI server for web API")
    else:
        print("⚠️  Setup completed with some issues.")
        print("Please check the error messages above and resolve them.")
        
        if success_count >= 3:
            print("\\n💡 The core system should still work. Try running:")
            print("   python test_system.py")

if __name__ == "__main__":
    main()
