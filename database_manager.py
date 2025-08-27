"""
Advanced database operations for SentimentAI platform
SQLite with SQLAlchemy for better performance and data management
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid
from dataclasses import dataclass

@dataclass
class AnalysisRecord:
    id: str
    content: str
    sentiment: str
    confidence: float
    source: str
    timestamp: datetime
    metadata: Dict

class DatabaseManager:
    def __init__(self, db_path: str = "sentiment_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Analysis results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    metadata TEXT
                )
            """)
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time DATETIME NOT NULL,
                    last_activity DATETIME NOT NULL,
                    actions_count INTEGER DEFAULT 0,
                    user_agent TEXT
                )
            """)
            
            # API usage statistics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    response_time REAL,
                    status_code INTEGER,
                    error_message TEXT
                )
            """)
            
            # Real-time metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp DATETIME NOT NULL,
                    category TEXT
                )
            """)
            
            # Content cache
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_cache (
                    cache_key TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    expiry_time DATETIME NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """)
            
            conn.commit()
    
    def store_analysis_result(self, content: str, sentiment: str, confidence: float, 
                            source: str, metadata: Dict = None) -> str:
        """Store analysis result in database"""
        analysis_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_results 
                (id, content, sentiment, confidence, source, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_id,
                content,
                sentiment,
                confidence,
                source,
                datetime.now(),
                json.dumps(metadata or {})
            ))
            conn.commit()
        
        return analysis_id
    
    def get_recent_analyses(self, limit: int = 100, hours: int = 24) -> List[AnalysisRecord]:
        """Get recent analysis results"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, content, sentiment, confidence, source, timestamp, metadata
                FROM analysis_results
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (cutoff_time, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append(AnalysisRecord(
                    id=row[0],
                    content=row[1],
                    sentiment=row[2],
                    confidence=row[3],
                    source=row[4],
                    timestamp=datetime.fromisoformat(row[5]),
                    metadata=json.loads(row[6]) if row[6] else {}
                ))
            
            return results
    
    def get_sentiment_statistics(self, hours: int = 24) -> Dict:
        """Get sentiment statistics for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Overall sentiment distribution
            cursor.execute("""
                SELECT sentiment, COUNT(*) as count, AVG(confidence) as avg_confidence
                FROM analysis_results
                WHERE timestamp > ?
                GROUP BY sentiment
            """, (cutoff_time,))
            
            sentiment_dist = {}
            total_analyses = 0
            
            for row in cursor.fetchall():
                sentiment, count, avg_conf = row
                sentiment_dist[sentiment] = {
                    'count': count,
                    'avg_confidence': round(avg_conf, 3)
                }
                total_analyses += count
            
            # Source breakdown
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM analysis_results
                WHERE timestamp > ?
                GROUP BY source
                ORDER BY count DESC
            """, (cutoff_time,))
            
            source_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Hourly trend
            cursor.execute("""
                SELECT 
                    strftime('%H', timestamp) as hour,
                    sentiment,
                    COUNT(*) as count
                FROM analysis_results
                WHERE timestamp > ?
                GROUP BY hour, sentiment
                ORDER BY hour
            """, (cutoff_time,))
            
            hourly_trend = {}
            for row in cursor.fetchall():
                hour, sentiment, count = row
                if hour not in hourly_trend:
                    hourly_trend[hour] = {}
                hourly_trend[hour][sentiment] = count
            
            return {
                'total_analyses': total_analyses,
                'sentiment_distribution': sentiment_dist,
                'source_breakdown': source_breakdown,
                'hourly_trend': hourly_trend,
                'time_range_hours': hours
            }
    
    def store_metric(self, metric_name: str, value: float, category: str = None):
        """Store a metric value"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO metrics (metric_name, metric_value, timestamp, category)
                VALUES (?, ?, ?, ?)
            """, (metric_name, value, datetime.now(), category))
            conn.commit()
    
    def get_metrics_history(self, metric_name: str, hours: int = 24) -> List[Dict]:
        """Get metric history"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT metric_value, timestamp
                FROM metrics
                WHERE metric_name = ? AND timestamp > ?
                ORDER BY timestamp
            """, (metric_name, cutoff_time))
            
            return [
                {'value': row[0], 'timestamp': row[1]}
                for row in cursor.fetchall()
            ]
    
    def log_api_usage(self, endpoint: str, response_time: float = None, 
                     status_code: int = None, error_message: str = None):
        """Log API usage statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_usage (endpoint, timestamp, response_time, status_code, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (endpoint, datetime.now(), response_time, status_code, error_message))
            conn.commit()
    
    def get_api_statistics(self, hours: int = 24) -> Dict:
        """Get API usage statistics"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Request count by endpoint
            cursor.execute("""
                SELECT endpoint, COUNT(*) as count, AVG(response_time) as avg_response_time
                FROM api_usage
                WHERE timestamp > ?
                GROUP BY endpoint
                ORDER BY count DESC
            """, (cutoff_time,))
            
            endpoint_stats = {}
            for row in cursor.fetchall():
                endpoint, count, avg_time = row
                endpoint_stats[endpoint] = {
                    'requests': count,
                    'avg_response_time': round(avg_time, 3) if avg_time else None
                }
            
            # Error rate
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as error_requests
                FROM api_usage
                WHERE timestamp > ?
            """, (cutoff_time,))
            
            total, errors = cursor.fetchone()
            error_rate = (errors / total * 100) if total > 0 else 0
            
            return {
                'endpoint_statistics': endpoint_stats,
                'total_requests': total,
                'error_requests': errors,
                'error_rate_percent': round(error_rate, 2),
                'time_range_hours': hours
            }
    
    def cache_content(self, cache_key: str, content: str, expiry_hours: int = 1):
        """Cache content with expiry"""
        expiry_time = datetime.now() + timedelta(hours=expiry_hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO content_cache 
                (cache_key, content, expiry_time, created_at)
                VALUES (?, ?, ?, ?)
            """, (cache_key, content, expiry_time, datetime.now()))
            conn.commit()
    
    def get_cached_content(self, cache_key: str) -> Optional[str]:
        """Get cached content if not expired"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT content FROM content_cache
                WHERE cache_key = ? AND expiry_time > ?
            """, (cache_key, datetime.now()))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def cleanup_expired_data(self):
        """Clean up expired cache and old data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Remove expired cache
            cursor.execute("DELETE FROM content_cache WHERE expiry_time < ?", (datetime.now(),))
            
            # Remove old analysis results (older than 30 days)
            cutoff = datetime.now() - timedelta(days=30)
            cursor.execute("DELETE FROM analysis_results WHERE timestamp < ?", (cutoff,))
            
            # Remove old metrics (older than 7 days)
            metrics_cutoff = datetime.now() - timedelta(days=7)
            cursor.execute("DELETE FROM metrics WHERE timestamp < ?", (metrics_cutoff,))
            
            conn.commit()
    
    def get_dashboard_summary(self) -> Dict:
        """Get comprehensive dashboard summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Today's stats
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_today,
                    AVG(confidence) as avg_confidence,
                    COUNT(DISTINCT source) as unique_sources
                FROM analysis_results
                WHERE timestamp >= ?
            """, (today,))
            
            today_stats = cursor.fetchone()
            
            # Recent sentiment trend
            cursor.execute("""
                SELECT sentiment, COUNT(*) as count
                FROM analysis_results
                WHERE timestamp >= ?
                GROUP BY sentiment
            """, (today,))
            
            sentiment_today = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                'today': {
                    'total_analyses': today_stats[0] or 0,
                    'avg_confidence': round(today_stats[1], 3) if today_stats[1] else 0,
                    'unique_sources': today_stats[2] or 0,
                    'sentiment_breakdown': sentiment_today
                },
                'timestamp': datetime.now().isoformat()
            }

# Global database instance
db_manager = DatabaseManager()
