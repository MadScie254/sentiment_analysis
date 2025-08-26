# Sentiment Analysis Dashboard API

A comprehensive sentiment analysis system designed for social media content, supporting English and Swahili (code-switching), with advanced emotion detection and comment classification.

## 🚀 Features

### Core Analysis Capabilities
- **Sentiment Analysis**: Positive, negative, neutral, mixed sentiment detection
- **Emotion Detection**: Anger, joy, sadness, excitement, sarcasm, fear, surprise, disgust
- **Comment Classification**: Funny, hateful, supportive, spam, insightful categorization
- **Toxicity Assessment**: Safe, moderate, high toxicity levels
- **Language Support**: English, Swahili, and code-switching detection

### Advanced Features
- **Social Media Optimized**: Handles emojis, slang, abbreviations
- **Kenyan Context**: Specialized for Kenyan internet culture and Swahili
- **Spam Detection**: URL detection, suspicious patterns, keyword filtering
- **Batch Processing**: Analyze multiple comments efficiently
- **JSON API**: Clean JSON output for easy integration

## 📦 Installation

### Quick Setup
```bash
# Clone or download the project
git clone <repository-url>
cd sentiment_analysis

# Run automated setup
python setup.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

# Run tests
python test_system.py
```

## 🔧 Usage

### 1. Simple JSON API (No dependencies)
```python
from simple_api import SimpleAPI

api = SimpleAPI()

# Analyze video data
request_data = '''{
    "video_title": "My first day in Nairobi 🚖🔥",
    "video_description": "Trying out local food and matatus, what an adventure!",
    "comments": [
        "😂😂 bro you look lost but it's vibes",
        "This city will eat you alive, trust me.",
        "Matatu rides >>> Uber any day",
        "Spam link: www.fakecrypto.com",
        "Karibu Kenya! We love you ❤️"
    ]
}'''

result = api.process_video_request(request_data)
print(result)
```

### 2. Direct Engine Usage
```python
from nlp_engine import NLPEngine

engine = NLPEngine()

# Quick text analysis
result = engine.quick_analyze("This is amazing! 😍")
print(result)

# Video data analysis
result = engine.analyze_video_data(
    video_title="Amazing day!",
    video_description="Had so much fun",
    comments=["Great video!", "Not bad", "Spam: www.fake.com"]
)
```

### 3. FastAPI Web Server
```bash
# Start the web server
python api_server.py

# Access API at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

### 4. Example Output Format
The system returns JSON in this format:
```json
{
  "video_sentiment": "positive",
  "video_emotion": ["excitement", "joy"],
  "comments": [
    {
      "text": "😂😂 bro you look lost but it's vibes",
      "sentiment": "positive",
      "emotion": ["joy", "sarcasm"],
      "tag": "funny"
    },
    {
      "text": "This city will eat you alive, trust me.",
      "sentiment": "negative",
      "emotion": ["fear"],
      "tag": "neutral"
    },
    {
      "text": "Spam link: www.fakecrypto.com",
      "sentiment": "neutral",
      "emotion": [],
      "tag": "spam"
    }
  ]
}
```

## 🏗️ System Architecture

### Core Components
1. **`sentiment_engine.py`** - Main sentiment analysis with VADER and TextBlob
2. **`emotion_detector.py`** - Multi-emotion detection with emoji support
3. **`comment_classifier.py`** - Comment categorization and toxicity assessment
4. **`nlp_engine.py`** - Main orchestrator combining all components
5. **`utils.py`** - Text preprocessing and validation utilities

### API Layers
- **`simple_api.py`** - Lightweight JSON processor
- **`api_server.py`** - Full FastAPI web server
- **`config.py`** - Configuration and settings

## 🌍 Language Support

### Swahili Integration
The system includes specialized support for:
- Common Swahili words and phrases
- Kenyan internet slang (poa, sawa, mambo, etc.)
- Code-switching detection
- Cultural context understanding

### Supported Expressions
- **Positive**: poa, sawa, karibu, asante, furaha
- **Negative**: mbaya, hasira, huzuni, hatari
- **Slang**: mambo vipi, niaje, si mchezo, kuna noma

## 🔍 Testing

### Run All Tests
```bash
python test_system.py
```

### Individual Component Tests
```bash
# Test specific components
python -m unittest test_system.TestSentimentEngine
python -m unittest test_system.TestEmotionDetector
python -m unittest test_system.TestCommentClassifier
```

### Example Data Test
```bash
# Run the exact example from the prompt
python example_usage.py
```

## 📊 Classification Categories

### Sentiment Types
- **Positive**: Happy, satisfied, excited content
- **Negative**: Angry, disappointed, sad content  
- **Neutral**: Factual, balanced content
- **Mixed**: Content with both positive and negative elements

### Emotion Labels
- **Joy**: Happiness, excitement, love
- **Anger**: Frustration, rage, annoyance
- **Sadness**: Disappointment, grief, melancholy
- **Fear**: Worry, anxiety, concern
- **Surprise**: Shock, amazement, confusion
- **Disgust**: Revulsion, disapproval
- **Sarcasm**: Irony, mocking tone
- **Excitement**: High energy, enthusiasm

### Comment Tags
- **Funny**: Humorous, entertaining content
- **Supportive**: Encouraging, positive reinforcement
- **Hateful**: Toxic, offensive, harmful content
- **Spam**: Promotional, scam, irrelevant content
- **Insightful**: Thoughtful, analytical, valuable content
- **Neutral**: Standard, unremarkable content

## 🛠️ API Endpoints

### FastAPI Server Endpoints
- `POST /analyze/video` - Complete video data analysis
- `POST /analyze/text` - Single text analysis
- `POST /analyze/comments` - Batch comment analysis
- `POST /analyze/sentiment` - Sentiment only
- `POST /analyze/emotions` - Emotions only
- `POST /analyze/classification` - Classification only
- `POST /analyze/spam` - Spam detection only
- `POST /analyze/toxicity` - Toxicity assessment only
- `GET /example` - Demo with example data
- `GET /health` - System health check

## ⚙️ Configuration

### Environment Variables
```bash
ENVIRONMENT=development  # or production
MAX_TEXT_LENGTH=5000
MAX_COMMENTS_BATCH=100
API_HOST=0.0.0.0
API_PORT=8000
```

### Customization
Edit `config.py` to adjust:
- Sentiment thresholds
- Classification weights  
- Language dictionaries
- Processing limits

## 🚦 Performance Notes

### Optimizations
- Lightweight models for speed
- Batch processing support
- Minimal dependencies for core functionality
- Efficient text preprocessing

### Scalability
- Stateless design for horizontal scaling
- JSON-based communication
- Configurable limits and thresholds
- Background processing ready

## 🔒 Safety Features

### Content Moderation
- Toxicity level assessment
- Hate speech detection
- Spam filtering
- Threat identification

### Data Validation
- Input sanitization
- Length limits
- Type checking
- Error handling

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Run tests: `python test_system.py`
4. Submit pull request

### Adding Languages
1. Update `config.py` with new language words
2. Add language detection in `utils.py`
3. Update preprocessing rules
4. Add test cases

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Support

### Common Issues
1. **Import Errors**: Run `python setup.py` to install dependencies
2. **NLTK Data Missing**: Run `python -c "import nltk; nltk.download('vader_lexicon')"`
3. **API Not Starting**: Check if FastAPI is installed: `pip install fastapi uvicorn`

### Getting Help
- Check the test file for usage examples
- Run `python example_usage.py` for demos
- Review the API documentation at `/docs` when server is running

---

**Built for Kenyan social media analysis with global applicability** 🇰🇪🌍
