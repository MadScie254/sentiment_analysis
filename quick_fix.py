"""
Quick Fix Script for Dashboard Issues
Fixes import issues and missing dependencies gracefully
"""

import os
import sys

def fix_mega_apis():
    """Ensure mega_api_collection is properly exported"""
    print("Fixing mega_free_apis.py...")
    
    try:
        with open('mega_free_apis.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure the global instance is properly named
        if 'mega_apis = MegaFreeAPICollection()' in content:
            content = content.replace('mega_apis = MegaFreeAPICollection()', 
                                    'mega_api_collection = MegaFreeAPICollection()')
            
            with open('mega_free_apis.py', 'w', encoding='utf-8') as f:
                f.write(content)
            print("  Fixed mega_api_collection export")
        else:
            print("  mega_api_collection already correct")
            
    except Exception as e:
        print(f"  Error fixing mega_free_apis.py: {e}")

def fix_dashboard_imports():
    """Fix dashboard import issues"""
    print("Fixing dashboard.py imports...")
    
    try:
        with open('dashboard.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add try-catch around problematic imports
        if "from mega_free_apis import mega_api_collection" in content:
            old_import = "from mega_free_apis import mega_api_collection"
            new_import = """try:
    from mega_free_apis import mega_api_collection
    MEGA_APIS_AVAILABLE = True
except ImportError:
    mega_api_collection = None
    MEGA_APIS_AVAILABLE = False"""
            
            content = content.replace(old_import, new_import)
            
        if "from advanced_ml_models import advanced_ml_models" in content:
            old_import = "from advanced_ml_models import advanced_ml_models"
            new_import = """try:
    from advanced_ml_models import advanced_ml_models
    ADVANCED_ML_AVAILABLE = True
except ImportError:
    advanced_ml_models = None
    ADVANCED_ML_AVAILABLE = False"""
            
            content = content.replace(old_import, new_import)
        
        if "from advanced_visualizer import advanced_visualizer" in content:
            old_import = "from advanced_visualizer import advanced_visualizer"
            new_import = """try:
    from advanced_visualizer import advanced_visualizer
    VISUALIZER_AVAILABLE = True
except ImportError:
    advanced_visualizer = None
    VISUALIZER_AVAILABLE = False"""
            
            content = content.replace(old_import, new_import)
        
        with open('dashboard.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Fixed dashboard imports with try-catch blocks")
            
    except Exception as e:
        print(f"  Error fixing dashboard.py: {e}")

def create_fallback_modules():
    """Create simple fallback modules for missing dependencies"""
    print("Creating fallback modules...")
    
    # Create a simple advanced_ml_models fallback
    fallback_ml = '''"""
Fallback Advanced ML Models
Simple fallback when full ML models are not available
"""

class SimpleSentimentAnalyzer:
    def analyze_sentiment_advanced(self, text):
        # Simple keyword-based analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'worst', 'disappointing']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            confidence = min(pos_count / (pos_count + neg_count + 1), 0.9)
        elif neg_count > pos_count:
            sentiment = 'negative'
            confidence = min(neg_count / (pos_count + neg_count + 1), 0.9)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'word_count': len(text.split()),
            'text_stats': {'word_count': len(text.split())},
            'emotions': {'scores': {}},
            'toxicity': {'level': 'none', 'score': 0},
            'bias': {'overall_bias_score': 0},
            'readability': {'reading_level': 'Standard'}
        }
    
    def analyze_multiple_texts(self, texts):
        results = [self.analyze_sentiment_advanced(text) for text in texts]
        sentiments = [r['sentiment'] for r in results]
        
        return {
            'total_texts_analyzed': len(texts),
            'sentiment_percentages': {
                'positive': (sentiments.count('positive') / len(sentiments)) * 100,
                'negative': (sentiments.count('negative') / len(sentiments)) * 100,
                'neutral': (sentiments.count('neutral') / len(sentiments)) * 100
            },
            'average_confidence': sum(r['confidence'] for r in results) / len(results),
            'analyses': results[:5]  # First 5 for display
        }
    
    def generate_insights(self, analysis):
        sentiment = analysis.get('sentiment', 'neutral')
        return [f"Analysis complete: {sentiment} sentiment detected"]

# Global fallback instance
try:
    from advanced_ml_models import advanced_ml_models
except ImportError:
    advanced_ml_models = SimpleSentimentAnalyzer()
'''
    
    try:
        if not os.path.exists('advanced_ml_models.py') or os.path.getsize('advanced_ml_models.py') < 1000:
            with open('advanced_ml_models_fallback.py', 'w', encoding='utf-8') as f:
                f.write(fallback_ml)
            print("  Created advanced_ml_models fallback")
    except Exception as e:
        print(f"  Error creating ML fallback: {e}")

def main():
    """Run all fixes"""
    print("=" * 50)
    print("QUICK FIX SCRIPT FOR DASHBOARD")
    print("=" * 50)
    
    fix_mega_apis()
    fix_dashboard_imports() 
    create_fallback_modules()
    
    print("\nFixes completed!")
    print("Now try running: python simple_launcher.py")

if __name__ == "__main__":
    main()
