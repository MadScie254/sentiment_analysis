"""
Data models and database integration for sentiment analysis system
Supports SQLite, PostgreSQL, and MongoDB backends
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class SentimentType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"

class CommentTag(Enum):
    FUNNY = "funny"
    SUPPORTIVE = "supportive"
    HATEFUL = "hateful"
    SPAM = "spam"
    INSIGHTFUL = "insightful"
    NEUTRAL = "neutral"

class ToxicityLevel(Enum):
    SAFE = "safe"
    MODERATE = "moderate"
    HIGH = "high"

@dataclass
class CommentAnalysis:
    """Data model for individual comment analysis"""
    comment_id: str
    text: str
    sentiment: SentimentType
    sentiment_confidence: float
    emotions: List[str]
    tag: CommentTag
    tag_confidence: float
    toxicity_level: ToxicityLevel
    toxicity_confidence: float
    language_detected: str
    word_count: int
    emoji_count: int
    created_at: datetime
    video_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['sentiment'] = self.sentiment.value
        data['tag'] = self.tag.value
        data['toxicity_level'] = self.toxicity_level.value
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommentAnalysis':
        """Create instance from dictionary"""
        data['sentiment'] = SentimentType(data['sentiment'])
        data['tag'] = CommentTag(data['tag'])
        data['toxicity_level'] = ToxicityLevel(data['toxicity_level'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

@dataclass
class VideoAnalysis:
    """Data model for video analysis"""
    video_id: str
    title: str
    description: str
    video_sentiment: SentimentType
    video_emotions: List[str]
    video_confidence: float
    total_comments: int
    analyzed_comments: int
    average_comment_sentiment: float
    dominant_emotion: Optional[str]
    engagement_score: float
    toxicity_score: float
    spam_ratio: float
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['video_sentiment'] = self.video_sentiment.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VideoAnalysis':
        """Create instance from dictionary"""
        data['video_sentiment'] = SentimentType(data['video_sentiment'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)

class DatabaseManager:
    """
    Database manager supporting multiple backends
    """
    
    def __init__(self, db_type: str = "sqlite", connection_string: str = "sentiment_analysis.db"):
        self.db_type = db_type
        self.connection_string = connection_string
        self.setup_database()
    
    def setup_database(self):
        """Initialize database tables"""
        if self.db_type == "sqlite":
            self._setup_sqlite()
        else:
            raise ValueError(f"Database type {self.db_type} not supported yet")
    
    def _setup_sqlite(self):
        """Setup SQLite database and tables"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            
            # Create video_analyses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_analyses (
                    video_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    video_sentiment TEXT NOT NULL,
                    video_emotions TEXT,  -- JSON array
                    video_confidence REAL,
                    total_comments INTEGER,
                    analyzed_comments INTEGER,
                    average_comment_sentiment REAL,
                    dominant_emotion TEXT,
                    engagement_score REAL,
                    toxicity_score REAL,
                    spam_ratio REAL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create comment_analyses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comment_analyses (
                    comment_id TEXT PRIMARY KEY,
                    video_id TEXT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    sentiment_confidence REAL,
                    emotions TEXT,  -- JSON array
                    tag TEXT NOT NULL,
                    tag_confidence REAL,
                    toxicity_level TEXT NOT NULL,
                    toxicity_confidence REAL,
                    language_detected TEXT,
                    word_count INTEGER,
                    emoji_count INTEGER,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES video_analyses (video_id)
                )
            ''')
            
            # Create analytics_reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_reports (
                    report_id TEXT PRIMARY KEY,
                    report_type TEXT NOT NULL,
                    date_range TEXT,
                    report_data TEXT,  -- JSON
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create system_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    log_id TEXT PRIMARY KEY,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    module TEXT,
                    details TEXT,  -- JSON
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_video_created_at ON video_analyses(created_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_comment_video_id ON comment_analyses(video_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_comment_sentiment ON comment_analyses(sentiment)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_comment_tag ON comment_analyses(tag)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_created_at ON system_logs(created_at)')
            
            conn.commit()
    
    def save_video_analysis(self, video_analysis: VideoAnalysis) -> bool:
        """Save video analysis to database"""
        try:
            if self.db_type == "sqlite":
                return self._save_video_analysis_sqlite(video_analysis)
        except Exception as e:
            self.log_error(f"Failed to save video analysis: {e}")
            return False
    
    def _save_video_analysis_sqlite(self, video_analysis: VideoAnalysis) -> bool:
        """Save video analysis to SQLite"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO video_analyses 
                (video_id, title, description, video_sentiment, video_emotions, 
                 video_confidence, total_comments, analyzed_comments, 
                 average_comment_sentiment, dominant_emotion, engagement_score, 
                 toxicity_score, spam_ratio, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_analysis.video_id,
                video_analysis.title,
                video_analysis.description,
                video_analysis.video_sentiment.value,
                json.dumps(video_analysis.video_emotions),
                video_analysis.video_confidence,
                video_analysis.total_comments,
                video_analysis.analyzed_comments,
                video_analysis.average_comment_sentiment,
                video_analysis.dominant_emotion,
                video_analysis.engagement_score,
                video_analysis.toxicity_score,
                video_analysis.spam_ratio,
                video_analysis.created_at.isoformat(),
                video_analysis.updated_at.isoformat()
            ))
            
            conn.commit()
            return True
    
    def save_comment_analysis(self, comment_analysis: CommentAnalysis) -> bool:
        """Save comment analysis to database"""
        try:
            if self.db_type == "sqlite":
                return self._save_comment_analysis_sqlite(comment_analysis)
        except Exception as e:
            self.log_error(f"Failed to save comment analysis: {e}")
            return False
    
    def _save_comment_analysis_sqlite(self, comment_analysis: CommentAnalysis) -> bool:
        """Save comment analysis to SQLite"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO comment_analyses 
                (comment_id, video_id, text, sentiment, sentiment_confidence, 
                 emotions, tag, tag_confidence, toxicity_level, toxicity_confidence, 
                 language_detected, word_count, emoji_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                comment_analysis.comment_id,
                comment_analysis.video_id,
                comment_analysis.text,
                comment_analysis.sentiment.value,
                comment_analysis.sentiment_confidence,
                json.dumps(comment_analysis.emotions),
                comment_analysis.tag.value,
                comment_analysis.tag_confidence,
                comment_analysis.toxicity_level.value,
                comment_analysis.toxicity_confidence,
                comment_analysis.language_detected,
                comment_analysis.word_count,
                comment_analysis.emoji_count,
                comment_analysis.created_at.isoformat()
            ))
            
            conn.commit()
            return True
    
    def get_video_analysis(self, video_id: str) -> Optional[VideoAnalysis]:
        """Retrieve video analysis by ID"""
        if self.db_type == "sqlite":
            return self._get_video_analysis_sqlite(video_id)
    
    def _get_video_analysis_sqlite(self, video_id: str) -> Optional[VideoAnalysis]:
        """Get video analysis from SQLite"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM video_analyses WHERE video_id = ?', (video_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                data = dict(zip(columns, row))
                data['video_emotions'] = json.loads(data['video_emotions'])
                return VideoAnalysis.from_dict(data)
        
        return None
    
    def get_comments_for_video(self, video_id: str) -> List[CommentAnalysis]:
        """Get all comments for a specific video"""
        if self.db_type == "sqlite":
            return self._get_comments_for_video_sqlite(video_id)
    
    def _get_comments_for_video_sqlite(self, video_id: str) -> List[CommentAnalysis]:
        """Get comments from SQLite"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM comment_analyses WHERE video_id = ?', (video_id,))
            rows = cursor.fetchall()
            
            comments = []
            columns = [description[0] for description in cursor.description]
            
            for row in rows:
                data = dict(zip(columns, row))
                data['emotions'] = json.loads(data['emotions'])
                comments.append(CommentAnalysis.from_dict(data))
            
            return comments
    
    def get_recent_analyses(self, limit: int = 50) -> List[VideoAnalysis]:
        """Get recent video analyses"""
        if self.db_type == "sqlite":
            return self._get_recent_analyses_sqlite(limit)
    
    def _get_recent_analyses_sqlite(self, limit: int) -> List[VideoAnalysis]:
        """Get recent analyses from SQLite"""
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM video_analyses 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            
            analyses = []
            columns = [description[0] for description in cursor.description]
            
            for row in rows:
                data = dict(zip(columns, row))
                data['video_emotions'] = json.loads(data['video_emotions'])
                analyses.append(VideoAnalysis.from_dict(data))
            
            return analyses
    
    def save_analytics_report(self, report_type: str, report_data: Dict[str, Any], 
                            date_range: str = None) -> str:
        """Save analytics report"""
        report_id = str(uuid.uuid4())
        
        if self.db_type == "sqlite":
            with sqlite3.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO analytics_reports 
                    (report_id, report_type, date_range, report_data, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    report_id,
                    report_type,
                    date_range,
                    json.dumps(report_data),
                    datetime.now().isoformat()
                ))
                conn.commit()
        
        return report_id
    
    def log_system_event(self, level: str, message: str, module: str = None, 
                        details: Dict[str, Any] = None):
        """Log system events"""
        log_id = str(uuid.uuid4())
        
        if self.db_type == "sqlite":
            with sqlite3.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_logs 
                    (log_id, level, message, module, details, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    log_id,
                    level,
                    message,
                    module,
                    json.dumps(details) if details else None,
                    datetime.now().isoformat()
                ))
                conn.commit()
    
    def log_error(self, message: str, module: str = None, details: Dict[str, Any] = None):
        """Log error message"""
        self.log_system_event("ERROR", message, module, details)
    
    def log_info(self, message: str, module: str = None, details: Dict[str, Any] = None):
        """Log info message"""
        self.log_system_event("INFO", message, module, details)
    
    def log_warning(self, message: str, module: str = None, details: Dict[str, Any] = None):
        """Log warning message"""
        self.log_system_event("WARNING", message, module, details)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        if self.db_type == "sqlite":
            with sqlite3.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                
                # Count total videos
                cursor.execute('SELECT COUNT(*) FROM video_analyses')
                total_videos = cursor.fetchone()[0]
                
                # Count total comments
                cursor.execute('SELECT COUNT(*) FROM comment_analyses')
                total_comments = cursor.fetchone()[0]
                
                # Count by sentiment
                cursor.execute('''
                    SELECT sentiment, COUNT(*) 
                    FROM video_analyses 
                    GROUP BY sentiment
                ''')
                sentiment_stats = dict(cursor.fetchall())
                
                # Count by comment tags
                cursor.execute('''
                    SELECT tag, COUNT(*) 
                    FROM comment_analyses 
                    GROUP BY tag
                ''')
                tag_stats = dict(cursor.fetchall())
                
                # Recent activity (last 24 hours)
                cursor.execute('''
                    SELECT COUNT(*) FROM video_analyses 
                    WHERE datetime(created_at) > datetime('now', '-1 day')
                ''')
                recent_videos = cursor.fetchone()[0]
                
                return {
                    "total_videos_analyzed": total_videos,
                    "total_comments_analyzed": total_comments,
                    "sentiment_distribution": sentiment_stats,
                    "comment_tag_distribution": tag_stats,
                    "recent_activity_24h": recent_videos,
                    "database_type": self.db_type,
                    "last_updated": datetime.now().isoformat()
                }
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> int:
        """Clean up old data beyond specified days"""
        if self.db_type == "sqlite":
            with sqlite3.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                
                # Delete old logs
                cursor.execute('''
                    DELETE FROM system_logs 
                    WHERE datetime(created_at) < datetime('now', '-{} days')
                '''.format(days_to_keep))
                
                deleted_logs = cursor.rowcount
                
                # Delete old reports
                cursor.execute('''
                    DELETE FROM analytics_reports 
                    WHERE datetime(created_at) < datetime('now', '-{} days')
                '''.format(days_to_keep))
                
                deleted_reports = cursor.rowcount
                
                conn.commit()
                
                total_deleted = deleted_logs + deleted_reports
                self.log_info(f"Cleaned up {total_deleted} old records", "DatabaseManager")
                
                return total_deleted
    
    def export_data(self, output_file: str, format_type: str = "json") -> bool:
        """Export all data to file"""
        try:
            if format_type.lower() == "json":
                return self._export_json(output_file)
            else:
                raise ValueError(f"Export format {format_type} not supported")
        except Exception as e:
            self.log_error(f"Failed to export data: {e}")
            return False
    
    def _export_json(self, output_file: str) -> bool:
        """Export data as JSON"""
        if self.db_type == "sqlite":
            with sqlite3.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                
                # Get all video analyses
                cursor.execute('SELECT * FROM video_analyses')
                video_columns = [description[0] for description in cursor.description]
                videos = [dict(zip(video_columns, row)) for row in cursor.fetchall()]
                
                # Get all comment analyses
                cursor.execute('SELECT * FROM comment_analyses')
                comment_columns = [description[0] for description in cursor.description]
                comments = [dict(zip(comment_columns, row)) for row in cursor.fetchall()]
                
                # Get all reports
                cursor.execute('SELECT * FROM analytics_reports')
                report_columns = [description[0] for description in cursor.description]
                reports = [dict(zip(report_columns, row)) for row in cursor.fetchall()]
                
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "database_type": self.db_type,
                    "video_analyses": videos,
                    "comment_analyses": comments,
                    "analytics_reports": reports
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                return True
    
    def get_database_size(self) -> Dict[str, Any]:
        """Get database size information"""
        if self.db_type == "sqlite":
            size_bytes = os.path.getsize(self.connection_string) if os.path.exists(self.connection_string) else 0
            size_mb = size_bytes / (1024 * 1024)
            
            return {
                "database_file": self.connection_string,
                "size_bytes": size_bytes,
                "size_mb": round(size_mb, 2),
                "exists": os.path.exists(self.connection_string)
            }
