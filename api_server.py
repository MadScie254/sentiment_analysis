from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import json
import uvicorn
import tempfile
import os
from nlp_engine import NLPEngine
from video_metadata import VideoMetadataExtractor

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="Advanced NLP backend for sentiment analysis, emotion detection, comment classification, and media metadata extraction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
nlp_engine = NLPEngine()
video_metadata_extractor = VideoMetadataExtractor()

# Pydantic models for request/response
class VideoData(BaseModel):
    video_title: str
    video_description: str
    comments: List[str]

class TextInput(BaseModel):
    text: str

class MediaURLInput(BaseModel):
    url: str

class CommentBatch(BaseModel):
    comments: List[str]

class AnalysisResponse(BaseModel):
    video_sentiment: str
    video_emotion: List[str]
    comments: List[Dict[str, Any]]

class MediaMetadataResponse(BaseModel):
    success: bool
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Sentiment Analysis API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/analyze/video", response_model=Dict[str, Any])
async def analyze_video_data(data: VideoData):
    """
    Analyze video data including title, description, and comments
    
    Returns comprehensive sentiment analysis with emotions and comment classifications
    """
    try:
        result = nlp_engine.analyze_video_data(
            video_title=data.video_title,
            video_description=data.video_description,
            comments=data.comments
        )
        
        # Format response as requested
        formatted_response = {
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
            ],
            "summary": result["summary"],
            "timestamp": result["timestamp"]
        }
        
        return formatted_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/text")
async def analyze_single_text(data: TextInput):
    """
    Quick analysis for single text input
    """
    try:
        result = nlp_engine.quick_analyze(data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/comments")
async def analyze_comment_batch(data: CommentBatch):
    """
    Batch analysis for multiple comments
    """
    try:
        results = nlp_engine.batch_analyze_comments(data.comments)
        return {
            "comments": results,
            "total_analyzed": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@app.post("/analyze/sentiment")
async def get_sentiment_only(data: TextInput):
    """
    Get only sentiment analysis for text
    """
    try:
        sentiment_result = nlp_engine.sentiment_analyzer.analyze_sentiment(data.text)
        return sentiment_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@app.post("/analyze/emotions")
async def get_emotions_only(data: TextInput):
    """
    Get only emotion detection for text
    """
    try:
        emotions = nlp_engine.emotion_detector.detect_emotions(data.text)
        return {"emotions": emotions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")

@app.post("/analyze/classification")
async def get_classification_only(data: TextInput):
    """
    Get only comment classification for text
    """
    try:
        classification = nlp_engine.comment_classifier.classify_comment(data.text)
        return classification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/analyze/spam")
async def detect_spam(data: TextInput):
    """
    Spam detection for text
    """
    try:
        spam_result = nlp_engine.sentiment_analyzer.detect_spam(data.text)
        return spam_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spam detection failed: {str(e)}")

@app.post("/analyze/toxicity")
async def get_toxicity(data: TextInput):
    """
    Toxicity assessment for text
    """
    try:
        toxicity_result = nlp_engine.comment_classifier.get_comment_toxicity(data.text)
        return toxicity_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Toxicity analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "api_status": "healthy",
        "nlp_engine": "initialized",
        "components": {
            "sentiment_analyzer": "ready",
            "emotion_detector": "ready",
            "comment_classifier": "ready"
        }
    }

@app.get("/example")
async def get_example_analysis():
    """
    Returns the analysis for the example data from the prompt
    """
    try:
        from nlp_engine import process_example_data
        result = process_example_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Example analysis failed: {str(e)}")

@app.post("/media/extract")
async def extract_media_metadata(
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
) -> MediaMetadataResponse:
    """
    Extract metadata from video URL or uploaded file
    
    Args:
        url: Video URL (YouTube, TikTok, Vimeo, etc.)
        file: Video file upload
        
    Returns:
        MediaMetadataResponse with extracted metadata or error
    """
    if not url and not file:
        raise HTTPException(status_code=400, detail="Either URL or file must be provided")
    
    if url and file:
        raise HTTPException(status_code=400, detail="Provide either URL or file, not both")
    
    try:
        if url:
            # Extract from URL
            metadata = video_metadata_extractor.extract_from_url(url)
            if "error" in metadata:
                return MediaMetadataResponse(success=False, error=metadata["error"])
            return MediaMetadataResponse(success=True, metadata=metadata)
            
        elif file:
            # Save uploaded file temporarily and extract metadata
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                metadata = video_metadata_extractor.extract_from_file(tmp_file_path)
                if "error" in metadata:
                    return MediaMetadataResponse(success=False, error=metadata["error"])
                return MediaMetadataResponse(success=True, metadata=metadata)
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_file_path)
                except OSError:
                    pass  # File cleanup failed, but metadata was extracted
                    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media extraction failed: {str(e)}")

@app.post("/media/extract-url")
async def extract_media_from_url(data: MediaURLInput) -> MediaMetadataResponse:
    """
    Extract metadata from video URL (alternative JSON endpoint)
    """
    try:
        metadata = video_metadata_extractor.extract_from_url(data.url)
        if "error" in metadata:
            return MediaMetadataResponse(success=False, error=metadata["error"])
        return MediaMetadataResponse(success=True, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL metadata extraction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
