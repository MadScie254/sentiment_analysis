"""
Enhanced Database Manager for Sentiment Analysis Dashboard
Integrates with the existing dashboard while providing enhanced functionality
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class EnhancedDatabaseManager:
    """Enhanced database manager compatible with existing dashboard"""
    
    def __init__(self, db_path: str = "sentiment_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Sentiment analysis results table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sentiment_analyses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        sentiment TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        scores TEXT,  -- JSON string
                        model_used TEXT,
                        processing_time REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT  -- JSON string for additional data
                    )
                """)
                
                # News articles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS news_articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT,
                        url TEXT,
                        source TEXT,
                        published_date DATETIME,
                        sentiment TEXT,
                        confidence REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Analytics cache table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics_cache (
                        cache_key TEXT PRIMARY KEY,
                        cache_data TEXT,  -- JSON string
                        expires_at DATETIME
                    )
                """)
                
                # Habits tracking table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal_id TEXT NOT NULL UNIQUE,
                        title TEXT NOT NULL,
                        description TEXT,
                        target INTEGER DEFAULT 1,
                        icon TEXT DEFAULT 'fa-check',
                        category TEXT DEFAULT 'general',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        active BOOLEAN DEFAULT 1
                    )
                """)
                
                # Habit completions table for detailed tracking
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit_completions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal_id TEXT NOT NULL,
                        completed_date DATE NOT NULL,
                        progress INTEGER DEFAULT 1,
                        notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(goal_id, completed_date)
                    )
                """)
                
                # Habit streaks table for performance tracking
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit_streaks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal_id TEXT NOT NULL UNIQUE,
                        current_streak INTEGER DEFAULT 0,
                        longest_streak INTEGER DEFAULT 0,
                        last_completed DATE,
                        streak_start_date DATE,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("✅ Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    def init_app(self, app):
        """Flask app initialization compatibility"""
        pass
    
    def save_sentiment_analysis(self, result, **kwargs):
        """Save sentiment analysis result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Handle both enhanced and legacy result formats
                if hasattr(result, 'sentiment'):
                    text = result.text
                    sentiment = result.sentiment
                    confidence = getattr(result, 'confidence', getattr(result, 'score', 0.0))
                    scores = json.dumps(getattr(result, 'scores', {}))
                    model_used = getattr(result, 'model_used', getattr(result, 'method', 'unknown'))
                    processing_time = getattr(result, 'processing_time', 0.0)
                    metadata = json.dumps({
                        'emotion_scores': getattr(result, 'emotion_scores', {}),
                        'toxicity_score': getattr(result, 'toxicity_score', 0.0),
                        **kwargs
                    })
                else:
                    # Legacy dictionary format
                    text = result.get('text', '')
                    sentiment = result.get('sentiment', 'neutral')
                    confidence = result.get('confidence', 0.0)
                    scores = json.dumps(result.get('scores', {}))
                    model_used = result.get('model_used', 'unknown')
                    processing_time = result.get('processing_time', 0.0)
                    metadata = json.dumps(kwargs)
                
                cursor.execute("""
                    INSERT INTO sentiment_analyses 
                    (text, sentiment, confidence, scores, model_used, processing_time, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (text, sentiment, confidence, scores, model_used, processing_time, metadata))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Failed to save sentiment analysis: {e}")
            return None
    
    def get_recent_analyses(self, limit=50, offset=0):
        """Get recent sentiment analyses"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, text, sentiment, confidence, scores, model_used, 
                           processing_time, timestamp, metadata
                    FROM sentiment_analyses 
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                
                results = []
                for row in cursor.fetchall():
                    try:
                        scores = json.loads(row[4]) if row[4] else {}
                        metadata = json.loads(row[8]) if row[8] else {}
                    except:
                        scores = {}
                        metadata = {}
                    
                    results.append({
                        'id': row[0],
                        'text': row[1],
                        'sentiment': row[2],
                        'confidence': row[3],
                        'scores': scores,
                        'model_used': row[5],
                        'processing_time': row[6],
                        'timestamp': row[7],
                        'metadata': metadata
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Failed to get recent analyses: {e}")
            return []
    
    def get_analytics_summary(self, days=7):
        """Get analytics summary for dashboard"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get date range
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                # Total analyses
                cursor.execute("""
                    SELECT COUNT(*) FROM sentiment_analyses 
                    WHERE timestamp >= ?
                """, (start_date,))
                total_analyses = cursor.fetchone()[0]
                
                # Sentiment distribution
                cursor.execute("""
                    SELECT sentiment, COUNT(*) FROM sentiment_analyses 
                    WHERE timestamp >= ?
                    GROUP BY sentiment
                """, (start_date,))
                
                sentiment_dist = {'positive': 0, 'negative': 0, 'neutral': 0}
                for sentiment, count in cursor.fetchall():
                    sentiment_dist[sentiment] = count
                
                # Average confidence
                cursor.execute("""
                    SELECT AVG(confidence) FROM sentiment_analyses 
                    WHERE timestamp >= ?
                """, (start_date,))
                avg_confidence = cursor.fetchone()[0] or 0.0
                
                # Hourly analysis for trends
                cursor.execute("""
                    SELECT strftime('%H', timestamp) as hour, COUNT(*) 
                    FROM sentiment_analyses 
                    WHERE timestamp >= ?
                    GROUP BY hour
                    ORDER BY hour
                """, (start_date,))
                
                hourly_data = {}
                for hour, count in cursor.fetchall():
                    hourly_data[int(hour)] = count
                
                return {
                    'total_analyses': total_analyses,
                    'sentiment_distribution': sentiment_dist,
                    'average_confidence': round(avg_confidence, 3),
                    'hourly_data': hourly_data,
                    'date_range': {
                        'start': start_date.isoformat(),
                        'end': end_date.isoformat()
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to get analytics summary: {e}")
            return {
                'total_analyses': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                'average_confidence': 0.0,
                'hourly_data': {},
                'date_range': {'start': '', 'end': ''}
            }
    
    def get_dashboard_summary(self):
        """Get dashboard summary statistics"""
        try:
            analytics = self.get_analytics_summary(days=30)
            
            # Calculate additional metrics
            total = analytics['total_analyses']
            sentiment_dist = analytics['sentiment_distribution']
            
            positive_ratio = sentiment_dist['positive'] / max(total, 1)
            negative_ratio = sentiment_dist['negative'] / max(total, 1)
            
            return {
                'total_processed': total,
                'positive_ratio': round(positive_ratio, 3),
                'negative_ratio': round(negative_ratio, 3),
                'average_confidence': analytics['average_confidence'],
                'trending_sentiment': 'positive' if positive_ratio > 0.5 else 'negative' if negative_ratio > 0.3 else 'neutral',
                'daily_volume': round(total / 30, 1),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get dashboard summary: {e}")
            return {
                'total_processed': 0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'average_confidence': 0.0,
                'trending_sentiment': 'neutral',
                'daily_volume': 0.0,
                'last_updated': datetime.now().isoformat()
            }
    
    def save_news_article(self, article_data):
        """Save news article with sentiment analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO news_articles 
                    (title, content, url, source, published_date, sentiment, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    article_data.get('title', ''),
                    article_data.get('content', ''),
                    article_data.get('url', ''),
                    article_data.get('source', ''),
                    article_data.get('published_date'),
                    article_data.get('sentiment', 'neutral'),
                    article_data.get('confidence', 0.0)
                ))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Failed to save news article: {e}")
            return None
    
    def get_cached_data(self, cache_key):
        """Get cached analytics data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT cache_data FROM analytics_cache 
                    WHERE cache_key = ? AND expires_at > ?
                """, (cache_key, datetime.now()))
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                return None
                
        except Exception as e:
            logger.error(f"Failed to get cached data: {e}")
            return None
    
    def set_cached_data(self, cache_key, data, ttl_minutes=60):
        """Set cached analytics data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO analytics_cache 
                    (cache_key, cache_data, expires_at)
                    VALUES (?, ?, ?)
                """, (cache_key, json.dumps(data), expires_at))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to set cached data: {e}")
    
    def create_habit(self, goal_id: str, title: str, description: str = "", target: int = 1, 
                    icon: str = "fa-check", category: str = "general") -> Optional[int]:
        """Create a new habit"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO habits (goal_id, title, description, target, icon, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (goal_id, title, description, target, icon, category))
                
                # Initialize streak record
                cursor.execute("""
                    INSERT INTO habit_streaks (goal_id, current_streak, longest_streak)
                    VALUES (?, 0, 0)
                """, (goal_id,))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Failed to create habit: {e}")
            return None
    
    def get_habits(self, active_only: bool = True) -> List[Dict]:
        """Get all habits"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT h.goal_id, h.title, h.description, h.target, h.icon, h.category,
                           s.current_streak, s.longest_streak, s.last_completed
                    FROM habits h
                    LEFT JOIN habit_streaks s ON h.goal_id = s.goal_id
                    WHERE h.active = ?
                    ORDER BY h.created_at
                """
                
                cursor.execute(query, (1 if active_only else 0,))
                rows = cursor.fetchall()
                
                habits = []
                for row in rows:
                    habits.append({
                        'goal_id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'target': row[3],
                        'icon': row[4],
                        'category': row[5],
                        'current_streak': row[6] or 0,
                        'longest_streak': row[7] or 0,
                        'last_completed': row[8]
                    })
                
                return habits
                
        except Exception as e:
            logger.error(f"Failed to get habits: {e}")
            return []
    
    def complete_habit(self, goal_id: str, date: str = None, progress: int = 1, notes: str = "") -> bool:
        """Mark a habit as completed for a given date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert completion record
                cursor.execute("""
                    INSERT OR REPLACE INTO habit_completions 
                    (goal_id, completed_date, progress, notes)
                    VALUES (?, ?, ?, ?)
                """, (goal_id, date, progress, notes))
                
                # Update streak information
                self._update_habit_streak(cursor, goal_id, date)
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to complete habit: {e}")
            return False
    
    def _update_habit_streak(self, cursor, goal_id: str, completion_date: str):
        """Update habit streak information"""
        try:
            # Get current streak info
            cursor.execute("""
                SELECT current_streak, longest_streak, last_completed
                FROM habit_streaks
                WHERE goal_id = ?
            """, (goal_id,))
            
            result = cursor.fetchone()
            if not result:
                current_streak, longest_streak, last_completed = 0, 0, None
            else:
                current_streak, longest_streak, last_completed = result
            
            # Calculate new streak
            completion_date_obj = datetime.strptime(completion_date, '%Y-%m-%d').date()
            
            if last_completed:
                last_completed_obj = datetime.strptime(last_completed, '%Y-%m-%d').date()
                days_diff = (completion_date_obj - last_completed_obj).days
                
                if days_diff == 1:  # Consecutive day
                    current_streak += 1
                elif days_diff == 0:  # Same day (update)
                    pass  # Keep current streak
                else:  # Gap in streak
                    current_streak = 1
            else:
                current_streak = 1
            
            # Update longest streak if needed
            longest_streak = max(longest_streak, current_streak)
            
            # Update streak record
            cursor.execute("""
                UPDATE habit_streaks
                SET current_streak = ?, longest_streak = ?, 
                    last_completed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE goal_id = ?
            """, (current_streak, longest_streak, completion_date, goal_id))
            
        except Exception as e:
            logger.error(f"Failed to update habit streak: {e}")
    
    def get_habit_completions(self, goal_id: str = None, days: int = 30) -> List[Dict]:
        """Get habit completion history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
                
                if goal_id:
                    query = """
                        SELECT goal_id, completed_date, progress, notes, created_at
                        FROM habit_completions
                        WHERE goal_id = ? AND completed_date >= ?
                        ORDER BY completed_date DESC
                    """
                    cursor.execute(query, (goal_id, cutoff_date))
                else:
                    query = """
                        SELECT goal_id, completed_date, progress, notes, created_at
                        FROM habit_completions
                        WHERE completed_date >= ?
                        ORDER BY completed_date DESC
                    """
                    cursor.execute(query, (cutoff_date,))
                
                rows = cursor.fetchall()
                
                completions = []
                for row in rows:
                    completions.append({
                        'goal_id': row[0],
                        'completed_date': row[1],
                        'progress': row[2],
                        'notes': row[3],
                        'created_at': row[4]
                    })
                
                return completions
                
        except Exception as e:
            logger.error(f"Failed to get habit completions: {e}")
            return []
    
    def get_habits_summary(self) -> Dict:
        """Get habits summary statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                today = datetime.now().strftime('%Y-%m-%d')
                
                # Get total habits
                cursor.execute("SELECT COUNT(*) FROM habits WHERE active = 1")
                total_habits = cursor.fetchone()[0]
                
                # Get completed today
                cursor.execute("""
                    SELECT COUNT(*) FROM habit_completions 
                    WHERE completed_date = ?
                """, (today,))
                completed_today = cursor.fetchone()[0]
                
                # Get longest streak
                cursor.execute("SELECT MAX(longest_streak) FROM habit_streaks")
                longest_streak = cursor.fetchone()[0] or 0
                
                return {
                    'total_habits': total_habits,
                    'completed_today': completed_today,
                    'longest_streak': longest_streak,
                    'completion_rate': (completed_today / total_habits * 100) if total_habits > 0 else 0
                }
                
        except Exception as e:
            logger.error(f"Failed to get habits summary: {e}")
            return {
                'total_habits': 0,
                'completed_today': 0,
                'longest_streak': 0,
                'completion_rate': 0
            }
    
    def get_recent_sentiment_analyses(self, days: int = 7) -> List[Dict]:
        """Get recent sentiment analyses"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute("""
                    SELECT text, sentiment, confidence, created_at, result_data
                    FROM sentiment_analyses
                    WHERE created_at >= ?
                    ORDER BY created_at DESC
                    LIMIT 1000
                """, (cutoff_date,))
                
                rows = cursor.fetchall()
                
                analyses = []
                for row in rows:
                    result_data = {}
                    if row[4]:  # result_data column
                        try:
                            result_data = json.loads(row[4])
                        except:
                            pass
                    
                    analyses.append({
                        'text': row[0],
                        'sentiment': row[1],
                        'confidence': row[2],
                        'timestamp': row[3],
                        'emotions': result_data.get('emotions', {}),
                        'linguistic_features': result_data.get('linguistic_features', {})
                    })
                
                return analyses
                
        except Exception as e:
            logger.error(f"Failed to get recent sentiment analyses: {e}")
            return []

# Global instance for compatibility
real_db_manager = EnhancedDatabaseManager()

# Simple DB class for Flask compatibility
class SimpleDB:
    def init_app(self, app):
        """Initialize database with Flask app"""
        real_db_manager.init_app(app)
    
    def create_all(self):
        """Create all database tables"""
        real_db_manager.init_database()

# Export for compatibility
db = SimpleDB()
