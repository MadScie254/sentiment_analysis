"""
Advanced analytics and reporting module for sentiment analysis
Generates comprehensive reports, trends, and insights
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import statistics

class SentimentAnalytics:
    """
    Advanced analytics engine for sentiment data
    """
    
    def __init__(self):
        self.analysis_history = []
        self.trends_data = defaultdict(list)
        
    def add_analysis(self, analysis_result: Dict[str, Any]):
        """Add analysis result to historical data"""
        timestamp = datetime.now()
        analysis_result['timestamp'] = timestamp.isoformat()
        analysis_result['date'] = timestamp.date().isoformat()
        analysis_result['hour'] = timestamp.hour
        analysis_result['day_of_week'] = timestamp.weekday()
        
        self.analysis_history.append(analysis_result)
        
    def generate_comprehensive_report(self, days_back: int = 7) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        if not self.analysis_history:
            return {"error": "No analysis data available"}
            
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_data = [
            analysis for analysis in self.analysis_history 
            if datetime.fromisoformat(analysis['timestamp']) >= cutoff_date
        ]
        
        if not recent_data:
            return {"error": f"No data available for the last {days_back} days"}
            
        report = {
            "report_period": f"Last {days_back} days",
            "total_analyses": len(recent_data),
            "sentiment_overview": self._analyze_sentiment_trends(recent_data),
            "emotion_insights": self._analyze_emotion_patterns(recent_data),
            "comment_classification": self._analyze_comment_types(recent_data),
            "toxicity_report": self._analyze_toxicity_trends(recent_data),
            "temporal_patterns": self._analyze_temporal_patterns(recent_data),
            "language_distribution": self._analyze_language_usage(recent_data),
            "engagement_metrics": self._calculate_engagement_metrics(recent_data),
            "anomaly_detection": self._detect_anomalies(recent_data),
            "recommendations": self._generate_recommendations(recent_data),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _analyze_sentiment_trends(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze sentiment distribution and trends"""
        video_sentiments = [item.get('video_sentiment', 'neutral') for item in data]
        
        sentiment_counts = Counter(video_sentiments)
        total = len(video_sentiments)
        
        # Calculate all comment sentiments
        all_comment_sentiments = []
        for item in data:
            for comment in item.get('comments', []):
                all_comment_sentiments.append(comment.get('sentiment', 'neutral'))
        
        comment_sentiment_counts = Counter(all_comment_sentiments)
        
        # Calculate sentiment score (positive=1, neutral=0, negative=-1, mixed=0.5)
        sentiment_scores = []
        for sentiment in video_sentiments:
            if sentiment == 'positive':
                sentiment_scores.append(1)
            elif sentiment == 'negative':
                sentiment_scores.append(-1)
            elif sentiment == 'mixed':
                sentiment_scores.append(0.5)
            else:
                sentiment_scores.append(0)
        
        avg_sentiment_score = statistics.mean(sentiment_scores) if sentiment_scores else 0
        
        return {
            "video_sentiment_distribution": dict(sentiment_counts),
            "video_sentiment_percentages": {
                k: round((v/total)*100, 2) for k, v in sentiment_counts.items()
            },
            "comment_sentiment_distribution": dict(comment_sentiment_counts),
            "average_sentiment_score": round(avg_sentiment_score, 3),
            "sentiment_trend": "positive" if avg_sentiment_score > 0.2 else "negative" if avg_sentiment_score < -0.2 else "neutral",
            "total_comments_analyzed": len(all_comment_sentiments)
        }
    
    def _analyze_emotion_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze emotion patterns and co-occurrences"""
        video_emotions = []
        comment_emotions = []
        emotion_pairs = []
        
        for item in data:
            video_emots = item.get('video_emotion', [])
            video_emotions.extend(video_emots)
            
            for comment in item.get('comments', []):
                comment_emots = comment.get('emotion', [])
                comment_emotions.extend(comment_emots)
                
                # Track emotion co-occurrences
                if len(comment_emots) > 1:
                    for i in range(len(comment_emots)):
                        for j in range(i+1, len(comment_emots)):
                            emotion_pairs.append(f"{comment_emots[i]}+{comment_emots[j]}")
        
        all_emotions = video_emotions + comment_emotions
        emotion_counts = Counter(all_emotions)
        emotion_pairs_counts = Counter(emotion_pairs)
        
        return {
            "most_common_emotions": dict(emotion_counts.most_common(10)),
            "video_emotions": dict(Counter(video_emotions)),
            "comment_emotions": dict(Counter(comment_emotions)),
            "emotion_co_occurrences": dict(emotion_pairs_counts.most_common(5)),
            "total_emotion_instances": len(all_emotions),
            "emotional_diversity": len(set(all_emotions))
        }
    
    def _analyze_comment_types(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze comment classification patterns"""
        comment_tags = []
        tag_sentiment_map = defaultdict(list)
        
        for item in data:
            for comment in item.get('comments', []):
                tag = comment.get('tag', 'neutral')
                sentiment = comment.get('sentiment', 'neutral')
                comment_tags.append(tag)
                tag_sentiment_map[tag].append(sentiment)
        
        tag_counts = Counter(comment_tags)
        total_comments = len(comment_tags)
        
        # Analyze sentiment distribution within each tag
        tag_sentiment_analysis = {}
        for tag, sentiments in tag_sentiment_map.items():
            sentiment_dist = Counter(sentiments)
            tag_sentiment_analysis[tag] = {
                "count": len(sentiments),
                "sentiment_distribution": dict(sentiment_dist),
                "dominant_sentiment": sentiment_dist.most_common(1)[0][0] if sentiment_dist else "neutral"
            }
        
        return {
            "comment_type_distribution": dict(tag_counts),
            "comment_type_percentages": {
                k: round((v/total_comments)*100, 2) for k, v in tag_counts.items()
            },
            "tag_sentiment_analysis": tag_sentiment_analysis,
            "most_common_tags": dict(tag_counts.most_common(5)),
            "total_comments": total_comments
        }
    
    def _analyze_toxicity_trends(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze toxicity patterns and safety metrics"""
        toxicity_levels = []
        hateful_comments = 0
        spam_comments = 0
        safe_comments = 0
        
        for item in data:
            for comment in item.get('comments', []):
                tag = comment.get('tag', 'neutral')
                
                if tag == 'hateful':
                    hateful_comments += 1
                    toxicity_levels.append('high')
                elif tag == 'spam':
                    spam_comments += 1
                    toxicity_levels.append('moderate')
                else:
                    safe_comments += 1
                    toxicity_levels.append('safe')
        
        total_comments = len(toxicity_levels)
        toxicity_counts = Counter(toxicity_levels)
        
        safety_score = (safe_comments / total_comments * 100) if total_comments > 0 else 100
        
        return {
            "toxicity_distribution": dict(toxicity_counts),
            "hateful_comments": hateful_comments,
            "spam_comments": spam_comments,
            "safe_comments": safe_comments,
            "safety_score": round(safety_score, 2),
            "safety_level": "high" if safety_score > 80 else "moderate" if safety_score > 60 else "low",
            "total_comments_assessed": total_comments
        }
    
    def _analyze_temporal_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns by time of day, day of week"""
        hourly_activity = defaultdict(int)
        daily_activity = defaultdict(int)
        hourly_sentiment = defaultdict(list)
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for item in data:
            hour = item.get('hour', 0)
            day = item.get('day_of_week', 0)
            sentiment = item.get('video_sentiment', 'neutral')
            
            hourly_activity[hour] += 1
            daily_activity[day_names[day]] += 1
            hourly_sentiment[hour].append(sentiment)
        
        # Find peak activity times
        peak_hour = max(hourly_activity, key=hourly_activity.get) if hourly_activity else 0
        peak_day = max(daily_activity, key=daily_activity.get) if daily_activity else "Unknown"
        
        # Analyze sentiment by hour
        hourly_sentiment_analysis = {}
        for hour, sentiments in hourly_sentiment.items():
            sentiment_counts = Counter(sentiments)
            dominant = sentiment_counts.most_common(1)[0][0] if sentiment_counts else "neutral"
            hourly_sentiment_analysis[hour] = {
                "dominant_sentiment": dominant,
                "activity_count": len(sentiments)
            }
        
        return {
            "hourly_activity": dict(hourly_activity),
            "daily_activity": dict(daily_activity),
            "peak_hour": peak_hour,
            "peak_day": peak_day,
            "hourly_sentiment_patterns": hourly_sentiment_analysis,
            "most_active_hours": sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _analyze_language_usage(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze language patterns and code-switching"""
        # Simplified language detection based on common patterns
        english_indicators = ['the', 'and', 'you', 'this', 'that', 'with', 'for']
        swahili_indicators = ['na', 'wa', 'ya', 'poa', 'sawa', 'karibu', 'asante']
        
        language_stats = {
            'english_dominant': 0,
            'swahili_dominant': 0,
            'mixed_language': 0,
            'unclear': 0
        }
        
        for item in data:
            for comment in item.get('comments', []):
                text = comment.get('text', '').lower()
                
                english_count = sum(1 for word in english_indicators if word in text)
                swahili_count = sum(1 for word in swahili_indicators if word in text)
                
                if english_count > swahili_count and english_count > 0:
                    language_stats['english_dominant'] += 1
                elif swahili_count > english_count and swahili_count > 0:
                    language_stats['swahili_dominant'] += 1
                elif english_count > 0 and swahili_count > 0:
                    language_stats['mixed_language'] += 1
                else:
                    language_stats['unclear'] += 1
        
        total = sum(language_stats.values())
        language_percentages = {
            k: round((v/total)*100, 2) if total > 0 else 0 
            for k, v in language_stats.items()
        }
        
        return {
            "language_distribution": language_stats,
            "language_percentages": language_percentages,
            "code_switching_rate": language_percentages['mixed_language'],
            "total_comments_analyzed": total
        }
    
    def _calculate_engagement_metrics(self, data: List[Dict]) -> Dict[str, Any]:
        """Calculate engagement and interaction metrics"""
        total_videos = len(data)
        total_comments = sum(len(item.get('comments', [])) for item in data)
        
        # Calculate average comments per video
        avg_comments = total_comments / total_videos if total_videos > 0 else 0
        
        # Calculate engagement score based on sentiment and emotion diversity
        engagement_scores = []
        for item in data:
            comments = item.get('comments', [])
            if not comments:
                engagement_scores.append(0)
                continue
                
            # Higher engagement for more diverse emotions and active sentiment
            emotions = set()
            sentiments = []
            for comment in comments:
                emotions.update(comment.get('emotion', []))
                sentiments.append(comment.get('sentiment', 'neutral'))
            
            emotion_diversity = len(emotions)
            sentiment_activity = len([s for s in sentiments if s != 'neutral'])
            
            engagement_score = (emotion_diversity * 2 + sentiment_activity) / len(comments)
            engagement_scores.append(engagement_score)
        
        avg_engagement = statistics.mean(engagement_scores) if engagement_scores else 0
        
        return {
            "total_videos_analyzed": total_videos,
            "total_comments": total_comments,
            "average_comments_per_video": round(avg_comments, 2),
            "average_engagement_score": round(avg_engagement, 3),
            "engagement_level": "high" if avg_engagement > 2 else "moderate" if avg_engagement > 1 else "low",
            "most_engaging_videos": len([score for score in engagement_scores if score > avg_engagement])
        }
    
    def _detect_anomalies(self, data: List[Dict]) -> Dict[str, Any]:
        """Detect unusual patterns or anomalies"""
        anomalies = []
        
        # Check for unusual sentiment patterns
        video_sentiments = [item.get('video_sentiment', 'neutral') for item in data]
        negative_ratio = video_sentiments.count('negative') / len(video_sentiments) if video_sentiments else 0
        
        if negative_ratio > 0.7:
            anomalies.append({
                "type": "high_negativity",
                "description": f"Unusually high negative sentiment rate: {negative_ratio:.2%}",
                "severity": "high"
            })
        
        # Check for spam spikes
        spam_comments = 0
        total_comments = 0
        for item in data:
            for comment in item.get('comments', []):
                total_comments += 1
                if comment.get('tag') == 'spam':
                    spam_comments += 1
        
        spam_ratio = spam_comments / total_comments if total_comments > 0 else 0
        if spam_ratio > 0.3:
            anomalies.append({
                "type": "spam_spike",
                "description": f"High spam detection rate: {spam_ratio:.2%}",
                "severity": "moderate"
            })
        
        # Check for emotion anomalies
        all_emotions = []
        for item in data:
            all_emotions.extend(item.get('video_emotion', []))
            for comment in item.get('comments', []):
                all_emotions.extend(comment.get('emotion', []))
        
        anger_ratio = all_emotions.count('anger') / len(all_emotions) if all_emotions else 0
        if anger_ratio > 0.4:
            anomalies.append({
                "type": "high_anger",
                "description": f"Elevated anger levels detected: {anger_ratio:.2%}",
                "severity": "moderate"
            })
        
        return {
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "overall_health": "healthy" if len(anomalies) == 0 else "concerning" if len(anomalies) > 2 else "attention_needed"
        }
    
    def _generate_recommendations(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Analyze overall patterns
        video_sentiments = [item.get('video_sentiment', 'neutral') for item in data]
        positive_ratio = video_sentiments.count('positive') / len(video_sentiments) if video_sentiments else 0
        
        if positive_ratio < 0.3:
            recommendations.append({
                "category": "content_strategy",
                "suggestion": "Consider creating more positive, uplifting content to improve audience sentiment",
                "priority": "high"
            })
        
        # Check comment engagement
        total_comments = sum(len(item.get('comments', [])) for item in data)
        avg_comments = total_comments / len(data) if data else 0
        
        if avg_comments < 2:
            recommendations.append({
                "category": "engagement",
                "suggestion": "Low comment engagement detected. Consider asking questions or encouraging discussion",
                "priority": "medium"
            })
        
        # Check for toxicity issues
        hateful_count = 0
        spam_count = 0
        for item in data:
            for comment in item.get('comments', []):
                if comment.get('tag') == 'hateful':
                    hateful_count += 1
                elif comment.get('tag') == 'spam':
                    spam_count += 1
        
        if hateful_count > 0:
            recommendations.append({
                "category": "moderation",
                "suggestion": "Implement stronger comment moderation to reduce toxic content",
                "priority": "high"
            })
        
        if spam_count > total_comments * 0.1:
            recommendations.append({
                "category": "security",
                "suggestion": "Enable spam filtering and consider verification requirements for comments",
                "priority": "medium"
            })
        
        return {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "action_required": any(rec["priority"] == "high" for rec in recommendations)
        }
    
    def export_report_json(self, report: Dict[str, Any], filename: str = None) -> str:
        """Export report as JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_trend_summary(self, metric: str = 'sentiment') -> Dict[str, Any]:
        """Get trend summary for a specific metric"""
        if len(self.analysis_history) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        recent_data = self.analysis_history[-10:]  # Last 10 analyses
        
        if metric == 'sentiment':
            scores = []
            for item in recent_data:
                sentiment = item.get('video_sentiment', 'neutral')
                if sentiment == 'positive':
                    scores.append(1)
                elif sentiment == 'negative':
                    scores.append(-1)
                elif sentiment == 'mixed':
                    scores.append(0.5)
                else:
                    scores.append(0)
            
            if len(scores) >= 2:
                trend = "improving" if scores[-1] > scores[0] else "declining" if scores[-1] < scores[0] else "stable"
                avg_score = statistics.mean(scores)
                
                return {
                    "metric": metric,
                    "trend": trend,
                    "current_average": round(avg_score, 3),
                    "data_points": len(scores),
                    "latest_score": scores[-1]
                }
        
        return {"error": f"Trend analysis not available for metric: {metric}"}
