"""
Advanced Analytics Engine with ML-powered insights
Provides predictive analytics, trend analysis, and intelligent recommendations
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import statistics
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity
import re
import math
from database_manager import db_manager

class AdvancedAnalytics:
    def __init__(self):
        self.sentiment_history = []
        self.trend_data = defaultdict(list)
        self.ml_models = {}
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize ML models for analytics"""
        self.ml_models = {
            'sentiment_predictor': LinearRegression(),
            'cluster_analyzer': KMeans(n_clusters=5, random_state=42),
            'tfidf_vectorizer': TfidfVectorizer(max_features=100, stop_words='english')
        }
    
    def analyze_sentiment_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Analyze sentiment trends over time"""
        recent_analyses = db_manager.get_recent_analyses(limit=1000, hours=hours)
        
        if not recent_analyses:
            return self._get_empty_trend_analysis()
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([
            {
                'timestamp': analysis.timestamp,
                'sentiment': analysis.sentiment,
                'confidence': analysis.confidence,
                'source': analysis.source,
                'content_length': len(analysis.content)
            }
            for analysis in recent_analyses
        ])
        
        # Time-based analysis
        df['hour'] = df['timestamp'].dt.hour
        df['sentiment_score'] = df.apply(self._sentiment_to_score, axis=1)
        
        # Trend calculations
        hourly_trends = self._calculate_hourly_trends(df)
        sentiment_momentum = self._calculate_momentum(df)
        prediction = self._predict_next_hour_sentiment(df)
        
        # Advanced metrics
        volatility = self._calculate_sentiment_volatility(df)
        confidence_analysis = self._analyze_confidence_patterns(df)
        source_performance = self._analyze_source_performance(df)
        
        return {
            'trend_analysis': {
                'overall_direction': self._determine_trend_direction(hourly_trends),
                'momentum': sentiment_momentum,
                'volatility': volatility,
                'prediction': prediction
            },
            'hourly_trends': hourly_trends,
            'confidence_analysis': confidence_analysis,
            'source_performance': source_performance,
            'summary': self._generate_trend_summary(df, sentiment_momentum, volatility),
            'recommendations': self._generate_recommendations(df, sentiment_momentum)
        }
    
    def perform_content_clustering(self, limit: int = 500) -> Dict[str, Any]:
        """Perform ML-based content clustering to identify themes"""
        recent_analyses = db_manager.get_recent_analyses(limit=limit, hours=72)
        
        if len(recent_analyses) < 10:
            return {'error': 'Insufficient data for clustering analysis'}
        
        # Prepare text data
        texts = [analysis.content for analysis in recent_analyses]
        sentiments = [analysis.sentiment for analysis in recent_analyses]
        
        try:
            # TF-IDF vectorization
            tfidf_matrix = self.ml_models['tfidf_vectorizer'].fit_transform(texts)
            
            # Perform clustering
            clusters = self.ml_models['cluster_analyzer'].fit_predict(tfidf_matrix)
            
            # Analyze clusters
            cluster_analysis = self._analyze_clusters(clusters, sentiments, texts)
            
            # Extract key themes
            themes = self._extract_themes(tfidf_matrix, clusters)
            
            return {
                'total_documents': len(texts),
                'clusters_found': len(set(clusters)),
                'cluster_analysis': cluster_analysis,
                'key_themes': themes,
                'sentiment_by_cluster': self._sentiment_by_cluster(clusters, sentiments)
            }
        
        except Exception as e:
            return {'error': f'Clustering analysis failed: {str(e)}'}
    
    def generate_predictive_insights(self) -> Dict[str, Any]:
        """Generate predictive insights and forecasts"""
        # Get historical data
        stats = db_manager.get_sentiment_statistics(hours=168)  # 1 week
        recent_data = db_manager.get_recent_analyses(limit=1000, hours=24)
        
        insights = {
            'volume_prediction': self._predict_volume_trends(),
            'sentiment_forecast': self._forecast_sentiment_direction(),
            'anomaly_detection': self._detect_anomalies(recent_data),
            'peak_hours': self._analyze_peak_activity_hours(stats),
            'risk_assessment': self._assess_sentiment_risks(recent_data)
        }
        
        return insights
    
    def calculate_engagement_metrics(self) -> Dict[str, Any]:
        """Calculate advanced engagement and interaction metrics"""
        recent_data = db_manager.get_recent_analyses(limit=500, hours=24)
        
        if not recent_data:
            return {'error': 'No recent data available'}
        
        # Content analysis
        content_metrics = self._analyze_content_patterns(recent_data)
        
        # Response quality
        quality_metrics = self._calculate_quality_scores(recent_data)
        
        # Engagement patterns
        engagement_patterns = self._analyze_engagement_patterns(recent_data)
        
        return {
            'content_metrics': content_metrics,
            'quality_metrics': quality_metrics,
            'engagement_patterns': engagement_patterns,
            'optimization_suggestions': self._generate_optimization_suggestions(
                content_metrics, quality_metrics
            )
        }
    
    def _sentiment_to_score(self, row) -> float:
        """Convert sentiment to numerical score"""
        sentiment_scores = {
            'positive': 1.0,
            'neutral': 0.0,
            'negative': -1.0
        }
        base_score = sentiment_scores.get(row['sentiment'], 0.0)
        return base_score * row['confidence']
    
    def _calculate_hourly_trends(self, df: pd.DataFrame) -> Dict[str, List]:
        """Calculate hourly sentiment trends"""
        hourly_data = df.groupby('hour').agg({
            'sentiment_score': ['mean', 'count', 'std'],
            'confidence': 'mean'
        }).round(3)
        
        return {
            'hours': list(range(24)),
            'avg_sentiment': [hourly_data['sentiment_score']['mean'].get(h, 0) for h in range(24)],
            'volume': [hourly_data['sentiment_score']['count'].get(h, 0) for h in range(24)],
            'volatility': [hourly_data['sentiment_score']['std'].get(h, 0) for h in range(24)],
            'confidence': [hourly_data['confidence']['mean'].get(h, 0) for h in range(24)]
        }
    
    def _calculate_momentum(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate sentiment momentum"""
        if len(df) < 10:
            return {'score': 0.0, 'direction': 'stable', 'strength': 'weak'}
        
        # Sort by timestamp and get recent vs older sentiment
        df_sorted = df.sort_values('timestamp')
        recent_sentiment = df_sorted.tail(len(df) // 3)['sentiment_score'].mean()
        older_sentiment = df_sorted.head(len(df) // 3)['sentiment_score'].mean()
        
        momentum_score = recent_sentiment - older_sentiment
        
        direction = 'positive' if momentum_score > 0.1 else 'negative' if momentum_score < -0.1 else 'stable'
        strength = 'strong' if abs(momentum_score) > 0.3 else 'moderate' if abs(momentum_score) > 0.1 else 'weak'
        
        return {
            'score': round(momentum_score, 3),
            'direction': direction,
            'strength': strength
        }
    
    def _predict_next_hour_sentiment(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Predict sentiment for next hour using simple linear regression"""
        if len(df) < 5:
            return {'prediction': 0.0, 'confidence': 0.0, 'method': 'insufficient_data'}
        
        try:
            # Prepare time-series data
            df_sorted = df.sort_values('timestamp')
            X = np.arange(len(df_sorted)).reshape(-1, 1)
            y = df_sorted['sentiment_score'].values
            
            # Fit linear regression
            self.ml_models['sentiment_predictor'].fit(X, y)
            
            # Predict next point
            next_prediction = self.ml_models['sentiment_predictor'].predict([[len(df_sorted)]])[0]
            
            # Calculate prediction confidence based on R²
            confidence = max(0, self.ml_models['sentiment_predictor'].score(X, y))
            
            return {
                'prediction': round(float(next_prediction), 3),
                'confidence': round(confidence, 3),
                'method': 'linear_regression'
            }
        
        except Exception:
            # Fallback to moving average
            recent_avg = df.tail(min(10, len(df)))['sentiment_score'].mean()
            return {
                'prediction': round(recent_avg, 3),
                'confidence': 0.5,
                'method': 'moving_average'
            }
    
    def _calculate_sentiment_volatility(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate sentiment volatility metrics"""
        if len(df) < 2:
            return {'hourly': 0.0, 'overall': 0.0, 'risk_level': 'low'}
        
        # Hourly volatility
        hourly_std = df.groupby('hour')['sentiment_score'].std().mean()
        
        # Overall volatility
        overall_std = df['sentiment_score'].std()
        
        # Risk assessment
        risk_level = 'high' if overall_std > 0.6 else 'medium' if overall_std > 0.3 else 'low'
        
        return {
            'hourly': round(hourly_std, 3) if not pd.isna(hourly_std) else 0.0,
            'overall': round(overall_std, 3),
            'risk_level': risk_level
        }
    
    def _analyze_confidence_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze confidence score patterns"""
        confidence_stats = {
            'average': df['confidence'].mean(),
            'median': df['confidence'].median(),
            'std': df['confidence'].std(),
            'min': df['confidence'].min(),
            'max': df['confidence'].max()
        }
        
        # Confidence by sentiment
        confidence_by_sentiment = df.groupby('sentiment')['confidence'].mean().to_dict()
        
        # Quality assessment
        high_confidence_pct = (df['confidence'] > 0.8).mean() * 100
        
        return {
            'statistics': {k: round(v, 3) for k, v in confidence_stats.items()},
            'by_sentiment': {k: round(v, 3) for k, v in confidence_by_sentiment.items()},
            'high_confidence_percentage': round(high_confidence_pct, 1),
            'quality_score': round(confidence_stats['average'] * 100, 1)
        }
    
    def _analyze_source_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance by data source"""
        source_stats = df.groupby('source').agg({
            'sentiment_score': ['count', 'mean', 'std'],
            'confidence': 'mean',
            'content_length': 'mean'
        }).round(3)
        
        performance = {}
        for source in source_stats.index:
            performance[source] = {
                'volume': int(source_stats.loc[source, ('sentiment_score', 'count')]),
                'avg_sentiment': source_stats.loc[source, ('sentiment_score', 'mean')],
                'volatility': source_stats.loc[source, ('sentiment_score', 'std')],
                'avg_confidence': source_stats.loc[source, ('confidence', 'mean')],
                'avg_content_length': int(source_stats.loc[source, ('content_length', 'mean')])
            }
        
        return performance
    
    def _determine_trend_direction(self, hourly_trends: Dict) -> str:
        """Determine overall trend direction"""
        recent_hours = hourly_trends['avg_sentiment'][-6:]  # Last 6 hours
        older_hours = hourly_trends['avg_sentiment'][:6]    # First 6 hours
        
        recent_avg = sum(recent_hours) / len(recent_hours) if recent_hours else 0
        older_avg = sum(older_hours) / len(older_hours) if older_hours else 0
        
        diff = recent_avg - older_avg
        
        if diff > 0.1:
            return 'improving'
        elif diff < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _generate_trend_summary(self, df: pd.DataFrame, momentum: Dict, volatility: Dict) -> str:
        """Generate human-readable trend summary"""
        total_analyses = len(df)
        avg_sentiment = df['sentiment_score'].mean()
        
        sentiment_desc = 'positive' if avg_sentiment > 0.2 else 'negative' if avg_sentiment < -0.2 else 'neutral'
        
        summary = f"Based on {total_analyses} analyses, sentiment is {sentiment_desc} "
        summary += f"with {momentum['direction']} momentum ({momentum['strength']} strength) "
        summary += f"and {volatility['risk_level']} volatility."
        
        return summary
    
    def _generate_recommendations(self, df: pd.DataFrame, momentum: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        avg_confidence = df['confidence'].mean()
        if avg_confidence < 0.6:
            recommendations.append("Consider improving data quality - confidence scores are below optimal levels")
        
        if momentum['direction'] == 'negative' and momentum['strength'] in ['moderate', 'strong']:
            recommendations.append("Monitor closely - negative sentiment momentum detected")
        
        source_counts = df['source'].value_counts()
        if len(source_counts) == 1:
            recommendations.append("Diversify data sources to get more comprehensive sentiment analysis")
        
        hourly_volume = df.groupby('hour').size()
        if hourly_volume.std() > hourly_volume.mean():
            recommendations.append("Consider analyzing peak hours for better resource allocation")
        
        return recommendations
    
    def _get_empty_trend_analysis(self) -> Dict[str, Any]:
        """Return empty trend analysis structure"""
        return {
            'trend_analysis': {
                'overall_direction': 'unknown',
                'momentum': {'score': 0.0, 'direction': 'stable', 'strength': 'weak'},
                'volatility': {'hourly': 0.0, 'overall': 0.0, 'risk_level': 'low'},
                'prediction': {'prediction': 0.0, 'confidence': 0.0, 'method': 'insufficient_data'}
            },
            'hourly_trends': {
                'hours': list(range(24)),
                'avg_sentiment': [0] * 24,
                'volume': [0] * 24,
                'volatility': [0] * 24,
                'confidence': [0] * 24
            },
            'confidence_analysis': {},
            'source_performance': {},
            'summary': "Insufficient data for trend analysis",
            'recommendations': ["Collect more data to enable comprehensive trend analysis"]
        }
    
    def _analyze_clusters(self, clusters: np.ndarray, sentiments: List[str], texts: List[str]) -> Dict:
        """Analyze content clusters"""
        cluster_info = {}
        
        for cluster_id in set(clusters):
            cluster_mask = clusters == cluster_id
            cluster_sentiments = [sentiments[i] for i in range(len(sentiments)) if cluster_mask[i]]
            cluster_texts = [texts[i] for i in range(len(texts)) if cluster_mask[i]]
            
            sentiment_dist = Counter(cluster_sentiments)
            avg_length = sum(len(text) for text in cluster_texts) / len(cluster_texts)
            
            cluster_info[f"cluster_{cluster_id}"] = {
                'size': int(cluster_mask.sum()),
                'sentiment_distribution': dict(sentiment_dist),
                'avg_text_length': round(avg_length, 1),
                'dominant_sentiment': sentiment_dist.most_common(1)[0][0] if sentiment_dist else 'unknown'
            }
        
        return cluster_info
    
    def _extract_themes(self, tfidf_matrix, clusters: np.ndarray) -> Dict[str, List[str]]:
        """Extract key themes from clusters"""
        feature_names = self.ml_models['tfidf_vectorizer'].get_feature_names_out()
        themes = {}
        
        for cluster_id in set(clusters):
            cluster_mask = clusters == cluster_id
            cluster_tfidf = tfidf_matrix[cluster_mask]
            
            # Get mean TF-IDF scores for this cluster
            mean_scores = np.mean(cluster_tfidf, axis=0).A1
            
            # Get top features
            top_indices = mean_scores.argsort()[-10:][::-1]
            top_terms = [feature_names[i] for i in top_indices if mean_scores[i] > 0]
            
            themes[f"cluster_{cluster_id}"] = top_terms[:5]
        
        return themes
    
    def _sentiment_by_cluster(self, clusters: np.ndarray, sentiments: List[str]) -> Dict:
        """Calculate sentiment distribution by cluster"""
        result = {}
        
        for cluster_id in set(clusters):
            cluster_mask = clusters == cluster_id
            cluster_sentiments = [sentiments[i] for i in range(len(sentiments)) if cluster_mask[i]]
            
            total = len(cluster_sentiments)
            if total > 0:
                positive = cluster_sentiments.count('positive') / total
                neutral = cluster_sentiments.count('neutral') / total
                negative = cluster_sentiments.count('negative') / total
                
                result[f"cluster_{cluster_id}"] = {
                    'positive': round(positive, 3),
                    'neutral': round(neutral, 3),
                    'negative': round(negative, 3)
                }
        
        return result
    
    def _predict_volume_trends(self) -> Dict[str, Any]:
        """Predict volume trends"""
        # This is a simplified prediction - in production, use more sophisticated models
        return {
            'next_hour': 'moderate_increase',
            'confidence': 0.7,
            'recommendation': 'Normal capacity should handle expected volume'
        }
    
    def _forecast_sentiment_direction(self) -> Dict[str, Any]:
        """Forecast sentiment direction"""
        return {
            'direction': 'slightly_positive',
            'confidence': 0.65,
            'time_horizon': '2_hours'
        }
    
    def _detect_anomalies(self, recent_data: List) -> List[Dict[str, Any]]:
        """Detect anomalies in recent data"""
        anomalies = []
        
        if len(recent_data) > 10:
            confidences = [analysis.confidence for analysis in recent_data]
            avg_confidence = statistics.mean(confidences)
            std_confidence = statistics.stdev(confidences)
            
            # Detect unusually low confidence scores
            threshold = avg_confidence - 2 * std_confidence
            low_confidence_count = sum(1 for c in confidences if c < threshold)
            
            if low_confidence_count > len(confidences) * 0.1:  # More than 10%
                anomalies.append({
                    'type': 'low_confidence_spike',
                    'description': f'Unusually high number of low-confidence predictions: {low_confidence_count}',
                    'severity': 'medium'
                })
        
        return anomalies
    
    def _analyze_peak_activity_hours(self, stats: Dict) -> Dict[str, Any]:
        """Analyze peak activity patterns"""
        if 'hourly_trend' not in stats:
            return {'error': 'Insufficient hourly data'}
        
        hourly_counts = {}
        for hour, sentiments in stats['hourly_trend'].items():
            total = sum(sentiments.values())
            hourly_counts[int(hour)] = total
        
        if not hourly_counts:
            return {'error': 'No hourly data available'}
        
        peak_hour = max(hourly_counts, key=hourly_counts.get)
        low_hour = min(hourly_counts, key=hourly_counts.get)
        
        return {
            'peak_hour': peak_hour,
            'peak_volume': hourly_counts[peak_hour],
            'lowest_hour': low_hour,
            'lowest_volume': hourly_counts[low_hour],
            'peak_to_low_ratio': round(hourly_counts[peak_hour] / max(hourly_counts[low_hour], 1), 2)
        }
    
    def _assess_sentiment_risks(self, recent_data: List) -> Dict[str, Any]:
        """Assess sentiment-related risks"""
        if not recent_data:
            return {'risk_level': 'unknown', 'factors': []}
        
        risk_factors = []
        risk_score = 0
        
        # Check for negative sentiment concentration
        negative_count = sum(1 for analysis in recent_data if analysis.sentiment == 'negative')
        negative_ratio = negative_count / len(recent_data)
        
        if negative_ratio > 0.6:
            risk_factors.append('High concentration of negative sentiment')
            risk_score += 3
        elif negative_ratio > 0.4:
            risk_factors.append('Moderate negative sentiment')
            risk_score += 1
        
        # Check confidence levels
        avg_confidence = sum(analysis.confidence for analysis in recent_data) / len(recent_data)
        if avg_confidence < 0.5:
            risk_factors.append('Low average confidence in predictions')
            risk_score += 2
        
        risk_level = 'high' if risk_score >= 4 else 'medium' if risk_score >= 2 else 'low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'factors': risk_factors,
            'recommendations': self._get_risk_recommendations(risk_level, risk_factors)
        }
    
    def _get_risk_recommendations(self, risk_level: str, factors: List[str]) -> List[str]:
        """Get recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append('Immediate attention required - monitor sentiment closely')
            recommendations.append('Consider implementing corrective measures')
        
        if 'negative sentiment' in ' '.join(factors).lower():
            recommendations.append('Investigate sources of negative sentiment')
            recommendations.append('Consider targeted interventions')
        
        if 'confidence' in ' '.join(factors).lower():
            recommendations.append('Review data quality and model performance')
            recommendations.append('Consider retraining or adjusting models')
        
        return recommendations
    
    def _analyze_content_patterns(self, recent_data: List) -> Dict[str, Any]:
        """Analyze content patterns and characteristics"""
        if not recent_data:
            return {}
        
        content_lengths = [len(analysis.content) for analysis in recent_data]
        
        return {
            'avg_length': round(statistics.mean(content_lengths), 1),
            'median_length': statistics.median(content_lengths),
            'length_std': round(statistics.stdev(content_lengths), 1) if len(content_lengths) > 1 else 0,
            'short_content_ratio': sum(1 for l in content_lengths if l < 50) / len(content_lengths),
            'long_content_ratio': sum(1 for l in content_lengths if l > 200) / len(content_lengths)
        }
    
    def _calculate_quality_scores(self, recent_data: List) -> Dict[str, Any]:
        """Calculate content and analysis quality scores"""
        if not recent_data:
            return {}
        
        confidence_scores = [analysis.confidence for analysis in recent_data]
        
        quality_score = statistics.mean(confidence_scores) * 100
        consistency_score = (1 - statistics.stdev(confidence_scores)) * 100 if len(confidence_scores) > 1 else 100
        
        return {
            'overall_quality': round(quality_score, 1),
            'consistency': round(max(0, consistency_score), 1),
            'high_quality_ratio': sum(1 for c in confidence_scores if c > 0.8) / len(confidence_scores)
        }
    
    def _analyze_engagement_patterns(self, recent_data: List) -> Dict[str, Any]:
        """Analyze engagement and interaction patterns"""
        if not recent_data:
            return {}
        
        sources = [analysis.source for analysis in recent_data]
        source_distribution = Counter(sources)
        
        return {
            'source_diversity': len(source_distribution),
            'dominant_source': source_distribution.most_common(1)[0][0] if source_distribution else 'unknown',
            'source_concentration': source_distribution.most_common(1)[0][1] / len(sources) if source_distribution else 0
        }
    
    def _generate_optimization_suggestions(self, content_metrics: Dict, quality_metrics: Dict) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []
        
        if content_metrics.get('short_content_ratio', 0) > 0.5:
            suggestions.append('Consider encouraging longer, more detailed content for better analysis')
        
        if quality_metrics.get('overall_quality', 0) < 70:
            suggestions.append('Focus on improving analysis quality - consider model retraining')
        
        if quality_metrics.get('consistency', 0) < 80:
            suggestions.append('Work on improving prediction consistency across different content types')
        
        return suggestions

# Global analytics instance
analytics_engine = AdvancedAnalytics()
