"""
Real Database Manager with SQLAlchemy
Handles sentiment analysis data, user interactions, and analytics
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict
import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, func, desc, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pandas as pd

# Initialize SQLAlchemy
db = SQLAlchemy()

class SentimentAnalysis(db.Model):
    """Model for storing sentiment analysis results"""
    __tablename__ = 'sentiment_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    scores = db.Column(db.JSON)  # Stores positive, negative, neutral scores
    model_used = db.Column(db.String(50), nullable=False)
    processing_time = db.Column(db.Float)
    language = db.Column(db.String(10))
    emotion_scores = db.Column(db.JSON)
    toxicity_score = db.Column(db.Float)
    bias_score = db.Column(db.Float)
    analysis_metadata = db.Column(db.JSON)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    
    # Analytics fields
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    source = db.Column(db.String(50), default='dashboard')  # dashboard, api, batch
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'scores': self.scores,
            'model_used': self.model_used,
            'processing_time': self.processing_time,
            'language': self.language,
            'emotion_scores': self.emotion_scores,
            'toxicity_score': self.toxicity_score,
            'bias_score': self.bias_score,
            'analysis_metadata': self.analysis_metadata,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class NewsArticle(db.Model):
    """Model for storing news articles for analysis"""
    __tablename__ = 'news_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    content = db.Column(db.Text)
    source = db.Column(db.String(100))
    published_date = db.Column(db.DateTime)
    sentiment = db.Column(db.String(20))
    confidence = db.Column(db.Float)
    category = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'content': self.content[:500] + "..." if self.content and len(self.content) > 500 else self.content,
            'source': self.source,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }

class VideoMetadata(db.Model):
    """Model for storing video metadata and sentiment analysis"""
    __tablename__ = 'video_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    url = db.Column(db.String(1000))
    duration = db.Column(db.Float)
    file_path = db.Column(db.String(1000))
    transcript = db.Column(db.Text)
    sentiment = db.Column(db.String(20))
    confidence = db.Column(db.Float)
    video_metadata = db.Column(db.JSON)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'duration': self.duration,
            'file_path': self.file_path,
            'transcript': self.transcript[:500] + "..." if self.transcript and len(self.transcript) > 500 else self.transcript,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'video_metadata': self.video_metadata,
            'created_at': self.created_at.isoformat()
        }

class ApiUsage(db.Model):
    """Model for tracking API usage and analytics"""
    __tablename__ = 'api_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    response_code = db.Column(db.Integer)
    processing_time = db.Column(db.Float)
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RealDatabaseManager:
    """
    Real database manager for sentiment analysis application
    """
    
    def __init__(self, app=None, database_url=None):
        self.app = app
        self.database_url = database_url or 'sqlite:///sentiment_analysis.db'
        self.logger = logging.getLogger(__name__)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            self.logger.info("Database tables created successfully")
    
    def save_sentiment_analysis(self, result, ip_address=None, user_agent=None, source='dashboard'):
        """Save sentiment analysis result to database"""
        try:
            analysis = SentimentAnalysis(
                text=result.text,
                sentiment=result.sentiment,
                confidence=result.confidence,
                scores=result.scores,
                model_used=result.model_used,
                processing_time=result.processing_time,
                language=result.language,
                emotion_scores=result.emotion_scores,
                toxicity_score=result.toxicity_score,
                bias_score=result.bias_score,
                analysis_metadata=result.analysis_metadata,
                ip_address=ip_address,
                user_agent=user_agent,
                source=source
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            self.logger.info(f"Saved sentiment analysis: {analysis.id}")
            return analysis.id
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving sentiment analysis: {str(e)}")
            return None
    
    def get_recent_analyses(self, limit=50, offset=0):
        """Get recent sentiment analyses"""
        try:
            analyses = SentimentAnalysis.query.order_by(
                desc(SentimentAnalysis.created_at)
            ).offset(offset).limit(limit).all()
            
            return [analysis.to_dict() for analysis in analyses]
            
        except Exception as e:
            self.logger.error(f"Error fetching analyses: {str(e)}")
            return []
    
    def get_analytics_summary(self, days=7):
        """Get comprehensive analytics summary"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Basic stats
            total_analyses = SentimentAnalysis.query.filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).count()
            
            # Sentiment distribution
            sentiment_dist = db.session.query(
                SentimentAnalysis.sentiment,
                func.count(SentimentAnalysis.id).label('count')
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).group_by(SentimentAnalysis.sentiment).all()
            
            sentiment_distribution = {item.sentiment: item.count for item in sentiment_dist}
            
            # Average confidence
            avg_confidence = db.session.query(
                func.avg(SentimentAnalysis.confidence)
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).scalar() or 0
            
            # Model usage
            model_usage = db.session.query(
                SentimentAnalysis.model_used,
                func.count(SentimentAnalysis.id).label('count')
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).group_by(SentimentAnalysis.model_used).all()
            
            model_distribution = {item.model_used: item.count for item in model_usage}
            
            # Language distribution
            language_dist = db.session.query(
                SentimentAnalysis.language,
                func.count(SentimentAnalysis.id).label('count')
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).group_by(SentimentAnalysis.language).all()
            
            language_distribution = {item.language: item.count for item in language_dist}
            
            # Processing time stats
            avg_processing_time = db.session.query(
                func.avg(SentimentAnalysis.processing_time)
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).scalar() or 0
            
            # Daily trends
            daily_trends = db.session.query(
                func.date(SentimentAnalysis.created_at).label('date'),
                func.count(SentimentAnalysis.id).label('count'),
                func.avg(SentimentAnalysis.confidence).label('avg_confidence')
            ).filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).group_by(func.date(SentimentAnalysis.created_at)).all()
            
            trends = [
                {
                    'date': item.date.isoformat() if item.date else None,
                    'count': item.count,
                    'avg_confidence': round(item.avg_confidence, 3) if item.avg_confidence else 0
                }
                for item in daily_trends
            ]
            
            return {
                'period_days': days,
                'total_analyses': total_analyses,
                'sentiment_distribution': sentiment_distribution,
                'average_confidence': round(avg_confidence, 3),
                'model_distribution': model_distribution,
                'language_distribution': language_distribution,
                'average_processing_time': round(avg_processing_time, 4),
                'daily_trends': trends,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating analytics: {str(e)}")
            return self._get_fallback_analytics()
    
    def save_news_article(self, title, url, content=None, source=None, published_date=None):
        """Save news article for analysis"""
        try:
            article = NewsArticle(
                title=title,
                url=url,
                content=content,
                source=source,
                published_date=published_date
            )
            
            db.session.add(article)
            db.session.commit()
            
            return article.id
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving news article: {str(e)}")
            return None
    
    def get_news_articles(self, limit=20, offset=0):
        """Get news articles with pagination"""
        try:
            articles = NewsArticle.query.order_by(
                desc(NewsArticle.created_at)
            ).offset(offset).limit(limit).all()
            
            return [article.to_dict() for article in articles]
            
        except Exception as e:
            self.logger.error(f"Error fetching news articles: {str(e)}")
            return []
    
    def save_video_metadata(self, title=None, url=None, duration=None, file_path=None, transcript=None, video_metadata=None):
        """Save video metadata"""
        try:
            video = VideoMetadata(
                title=title,
                url=url,
                duration=duration,
                file_path=file_path,
                transcript=transcript,
                video_metadata=video_metadata
            )
            
            db.session.add(video)
            db.session.commit()
            
            return video.id
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving video metadata: {str(e)}")
            return None
    
    def log_api_usage(self, endpoint, method, ip_address=None, user_agent=None, 
                     response_code=200, processing_time=None, error_message=None):
        """Log API usage for analytics"""
        try:
            usage = ApiUsage(
                endpoint=endpoint,
                method=method,
                ip_address=ip_address,
                user_agent=user_agent,
                response_code=response_code,
                processing_time=processing_time,
                error_message=error_message
            )
            
            db.session.add(usage)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error logging API usage: {str(e)}")
    
    def search_analyses(self, query, sentiment_filter=None, model_filter=None, limit=50):
        """Search sentiment analyses"""
        try:
            filters = []
            
            if query:
                filters.append(SentimentAnalysis.text.contains(query))
            
            if sentiment_filter:
                filters.append(SentimentAnalysis.sentiment == sentiment_filter)
            
            if model_filter:
                filters.append(SentimentAnalysis.model_used == model_filter)
            
            analyses = SentimentAnalysis.query.filter(
                and_(*filters) if filters else True
            ).order_by(desc(SentimentAnalysis.created_at)).limit(limit).all()
            
            return [analysis.to_dict() for analysis in analyses]
            
        except Exception as e:
            self.logger.error(f"Error searching analyses: {str(e)}")
            return []
    
    def get_dashboard_summary(self):
        """Get summary data for dashboard"""
        try:
            today = datetime.utcnow().date()
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            # Today's stats
            today_analyses = SentimentAnalysis.query.filter(
                func.date(SentimentAnalysis.created_at) == today
            ).count()
            
            # Week's stats
            week_analyses = SentimentAnalysis.query.filter(
                SentimentAnalysis.created_at >= week_ago
            ).count()
            
            # Average confidence this week
            avg_confidence = db.session.query(
                func.avg(SentimentAnalysis.confidence)
            ).filter(
                SentimentAnalysis.created_at >= week_ago
            ).scalar() or 0
            
            # Most used model this week
            top_model = db.session.query(
                SentimentAnalysis.model_used,
                func.count(SentimentAnalysis.id).label('count')
            ).filter(
                SentimentAnalysis.created_at >= week_ago
            ).group_by(
                SentimentAnalysis.model_used
            ).order_by(desc('count')).first()
            
            return {
                'today': {
                    'total_analyses': today_analyses,
                    'avg_confidence': round(avg_confidence, 3),
                    'top_model': top_model.model_used if top_model else 'N/A',
                    'date': today.isoformat()
                },
                'week': {
                    'total_analyses': week_analyses,
                    'avg_confidence': round(avg_confidence, 3),
                    'top_model': top_model.model_used if top_model else 'N/A',
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard summary: {str(e)}")
            return self._get_fallback_summary()
    
    def export_data(self, format='json', days=30):
        """Export data in various formats"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            analyses = SentimentAnalysis.query.filter(
                SentimentAnalysis.created_at >= cutoff_date
            ).all()
            
            data = [analysis.to_dict() for analysis in analyses]
            
            if format == 'json':
                return json.dumps(data, indent=2, default=str)
            elif format == 'csv':
                df = pd.DataFrame(data)
                return df.to_csv(index=False)
            else:
                return data
                
        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            return None
    
    def _get_fallback_analytics(self):
        """Fallback analytics when database fails"""
        return {
            'period_days': 7,
            'total_analyses': 0,
            'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
            'average_confidence': 0.0,
            'model_distribution': {},
            'language_distribution': {'en': 0},
            'average_processing_time': 0.0,
            'daily_trends': [],
            'generated_at': datetime.utcnow().isoformat(),
            'error': 'Database unavailable'
        }
    
    def _get_fallback_summary(self):
        """Fallback summary when database fails"""
        return {
            'today': {
                'total_analyses': 0,
                'avg_confidence': 0.0,
                'top_model': 'N/A',
                'date': datetime.utcnow().date().isoformat()
            },
            'week': {
                'total_analyses': 0,
                'avg_confidence': 0.0,
                'top_model': 'N/A',
            }
        }

# Global instance
real_db_manager = RealDatabaseManager()
