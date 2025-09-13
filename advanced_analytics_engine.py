"""
📊 ADVANCED ANALYTICS ENGINE
AI insights, predictive analytics, trend analysis, intelligent reporting, and data-driven recommendations
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics
import math
import re

@dataclass
class AnalyticsInsight:
    """Structure for analytics insights"""
    id: str
    type: str  # trend, anomaly, prediction, pattern, recommendation
    title: str
    description: str
    confidence: float  # 0-1
    impact: str  # low, medium, high
    actionable: bool
    created_at: datetime
    data_points: Dict
    visualization_type: str  # chart, graph, heatmap, etc.

@dataclass
class TrendAnalysis:
    """Trend analysis results"""
    metric: str
    direction: str  # up, down, stable
    strength: float  # 0-1
    duration: int  # days
    prediction: Dict
    seasonality: Optional[Dict] = None
    anomalies: List[Dict] = None

class AdvancedAnalyticsEngine:
    """
    Comprehensive analytics system with AI-powered insights and predictions
    """
    
    def __init__(self):
        self.insights_cache = {}
        self.trend_analyzer = TrendAnalyzer()
        self.pattern_detector = PatternDetector()
        self.anomaly_detector = AnomalyDetector()
        self.prediction_engine = PredictionEngine()
        self.intelligence_engine = IntelligenceEngine()
        
    def analyze_sentiment_trends(self, analysis_history: List[Dict]) -> Dict:
        """Analyze sentiment trends over time"""
        if not analysis_history:
            return {}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(analysis_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp']).sort_values('timestamp')
        
        # Basic sentiment distribution
        sentiment_counts = df['sentiment'].value_counts()
        total_analyses = len(df)
        
        # Time-based trends
        df['date'] = df['timestamp'].dt.date
        daily_sentiment = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        # Calculate trend direction
        recent_period = df[df['timestamp'] >= (datetime.now() - timedelta(days=7))]
        previous_period = df[
            (df['timestamp'] >= (datetime.now() - timedelta(days=14))) &
            (df['timestamp'] < (datetime.now() - timedelta(days=7)))
        ]
        
        trend_analysis = self._calculate_sentiment_trend(recent_period, previous_period)
        
        # Pattern detection
        patterns = self.pattern_detector.detect_sentiment_patterns(df)
        
        # Anomaly detection
        anomalies = self.anomaly_detector.detect_sentiment_anomalies(df)
        
        return {
            'summary': {
                'total_analyses': total_analyses,
                'sentiment_distribution': sentiment_counts.to_dict(),
                'dominant_sentiment': sentiment_counts.index[0] if len(sentiment_counts) > 0 else 'neutral',
                'sentiment_diversity': len(sentiment_counts)
            },
            'trends': trend_analysis,
            'patterns': patterns,
            'anomalies': anomalies,
            'daily_breakdown': daily_sentiment.to_dict('index') if not daily_sentiment.empty else {},
            'insights': self._generate_sentiment_insights(df, trend_analysis, patterns)
        }
    
    def analyze_user_behavior(self, user_activity: List[Dict]) -> Dict:
        """Analyze user behavior patterns"""
        if not user_activity:
            return {}
        
        df = pd.DataFrame(user_activity)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        
        # Usage patterns
        usage_patterns = self._analyze_usage_patterns(df)
        
        # Feature preferences
        feature_usage = self._analyze_feature_usage(df)
        
        # Engagement metrics
        engagement_metrics = self._calculate_engagement_metrics(df)
        
        # Predictive insights
        predictions = self.prediction_engine.predict_user_behavior(df)
        
        return {
            'usage_patterns': usage_patterns,
            'feature_preferences': feature_usage,
            'engagement_metrics': engagement_metrics,
            'predictions': predictions,
            'recommendations': self._generate_behavior_recommendations(df, usage_patterns)
        }
    
    def generate_predictive_insights(self, data: Dict) -> List[AnalyticsInsight]:
        """Generate AI-powered predictive insights"""
        insights = []
        
        # Sentiment trend predictions
        if 'sentiment_trends' in data:
            sentiment_insights = self._predict_sentiment_trends(data['sentiment_trends'])
            insights.extend(sentiment_insights)
        
        # User engagement predictions
        if 'user_behavior' in data:
            engagement_insights = self._predict_user_engagement(data['user_behavior'])
            insights.extend(engagement_insights)
        
        # Performance insights
        performance_insights = self._analyze_system_performance(data)
        insights.extend(performance_insights)
        
        # Sort by impact and confidence
        insights.sort(key=lambda x: (x.impact == 'high', x.confidence), reverse=True)
        
        return insights[:10]  # Return top 10 insights
    
    def create_intelligent_report(self, analysis_data: Dict, user_data: Dict) -> Dict:
        """Create comprehensive intelligent report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'report_id': f"report_{int(datetime.now().timestamp())}",
            'executive_summary': self._generate_executive_summary(analysis_data, user_data),
            'key_metrics': self._extract_key_metrics(analysis_data, user_data),
            'insights': self.generate_predictive_insights({
                'sentiment_trends': analysis_data,
                'user_behavior': user_data
            }),
            'recommendations': self._generate_strategic_recommendations(analysis_data, user_data),
            'visualizations': self._suggest_visualizations(analysis_data, user_data)
        }
        
        return report
    
    def _calculate_sentiment_trend(self, recent_df: pd.DataFrame, previous_df: pd.DataFrame) -> Dict:
        """Calculate sentiment trend between periods"""
        if recent_df.empty or previous_df.empty:
            return {'direction': 'stable', 'strength': 0, 'confidence': 0}
        
        recent_positive = len(recent_df[recent_df['sentiment'] == 'positive']) / len(recent_df)
        previous_positive = len(previous_df[previous_df['sentiment'] == 'positive']) / len(previous_df)
        
        change = recent_positive - previous_positive
        
        if abs(change) < 0.05:
            direction = 'stable'
        elif change > 0:
            direction = 'improving'
        else:
            direction = 'declining'
        
        strength = min(abs(change) * 2, 1.0)  # Normalize to 0-1
        confidence = min(len(recent_df) / 10, 1.0)  # More data = higher confidence
        
        return {
            'direction': direction,
            'strength': strength,
            'confidence': confidence,
            'change_percentage': change * 100,
            'recent_positive_rate': recent_positive,
            'previous_positive_rate': previous_positive
        }
    
    def _analyze_usage_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze user usage patterns"""
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['date'] = df['timestamp'].dt.date
        
        # Peak usage hours
        hourly_usage = df['hour'].value_counts().sort_index()
        peak_hour = hourly_usage.idxmax()
        
        # Weekly patterns
        daily_usage = df['day_of_week'].value_calls().sort_index()
        peak_day = daily_usage.idxmax()
        
        # Session analysis
        dates = df['date'].value_counts()
        avg_daily_sessions = dates.mean()
        most_active_day = dates.idxmax()
        
        # Usage intensity
        recent_usage = len(df[df['timestamp'] >= (datetime.now() - timedelta(days=7))])
        usage_trend = 'increasing' if recent_usage > avg_daily_sessions * 7 * 0.8 else 'stable'
        
        return {
            'peak_hour': int(peak_hour),
            'peak_day': int(peak_day),
            'avg_daily_sessions': round(avg_daily_sessions, 2),
            'most_active_day': most_active_day.isoformat(),
            'usage_trend': usage_trend,
            'hourly_distribution': hourly_usage.to_dict(),
            'daily_distribution': daily_usage.to_dict()
        }
    
    def _analyze_feature_usage(self, df: pd.DataFrame) -> Dict:
        """Analyze feature usage preferences"""
        if 'feature' not in df.columns:
            return {}
        
        feature_counts = df['feature'].value_counts()
        total_usage = len(df)
        
        feature_preferences = {}
        for feature, count in feature_counts.items():
            feature_preferences[feature] = {
                'usage_count': int(count),
                'usage_percentage': round((count / total_usage) * 100, 2),
                'rank': feature_counts.rank(method='dense', ascending=False)[feature]
            }
        
        # Most used feature
        top_feature = feature_counts.index[0] if len(feature_counts) > 0 else None
        
        return {
            'preferences': feature_preferences,
            'top_feature': top_feature,
            'feature_diversity': len(feature_counts),
            'specialization_score': (feature_counts.iloc[0] / total_usage) if len(feature_counts) > 0 else 0
        }
    
    def _calculate_engagement_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate user engagement metrics"""
        if df.empty:
            return {}
        
        # Time-based metrics
        time_span = (df['timestamp'].max() - df['timestamp'].min()).days
        total_sessions = len(df)
        
        # Frequency metrics
        dates_active = df['timestamp'].dt.date.nunique()
        avg_sessions_per_day = total_sessions / max(dates_active, 1)
        
        # Consistency metrics
        daily_counts = df['timestamp'].dt.date.value_counts()
        consistency_score = 1 - (daily_counts.std() / daily_counts.mean()) if daily_counts.mean() > 0 else 0
        consistency_score = max(0, min(1, consistency_score))
        
        # Engagement level classification
        if avg_sessions_per_day >= 5:
            engagement_level = 'high'
        elif avg_sessions_per_day >= 2:
            engagement_level = 'medium'
        else:
            engagement_level = 'low'
        
        return {
            'total_sessions': total_sessions,
            'active_days': dates_active,
            'time_span_days': time_span,
            'avg_sessions_per_day': round(avg_sessions_per_day, 2),
            'consistency_score': round(consistency_score, 2),
            'engagement_level': engagement_level
        }
    
    def _generate_sentiment_insights(self, df: pd.DataFrame, trend_analysis: Dict, patterns: Dict) -> List[str]:
        """Generate textual insights about sentiment data"""
        insights = []
        
        if not df.empty:
            # Sentiment distribution insight
            sentiment_counts = df['sentiment'].value_counts()
            dominant = sentiment_counts.index[0]
            percentage = (sentiment_counts.iloc[0] / len(df)) * 100
            insights.append(f"{dominant.capitalize()} sentiment dominates with {percentage:.1f}% of analyses")
            
            # Trend insight
            if trend_analysis.get('direction') == 'improving':
                insights.append(f"Sentiment is improving with {trend_analysis.get('change_percentage', 0):.1f}% increase in positivity")
            elif trend_analysis.get('direction') == 'declining':
                insights.append(f"Sentiment is declining with {abs(trend_analysis.get('change_percentage', 0)):.1f}% decrease in positivity")
            
            # Volume insight
            if len(df) >= 100:
                insights.append(f"High analysis volume detected with {len(df)} total analyses providing robust data")
            elif len(df) >= 20:
                insights.append(f"Moderate analysis volume with {len(df)} analyses - consider increasing sample size")
            else:
                insights.append(f"Limited analysis volume with only {len(df)} analyses - insights may be preliminary")
        
        return insights
    
    def _generate_behavior_recommendations(self, df: pd.DataFrame, usage_patterns: Dict) -> List[str]:
        """Generate behavior-based recommendations"""
        recommendations = []
        
        # Peak time recommendations
        peak_hour = usage_patterns.get('peak_hour', 12)
        if 9 <= peak_hour <= 17:
            recommendations.append("Consider scheduling important analyses during business hours for optimal engagement")
        elif 18 <= peak_hour <= 22:
            recommendations.append("Evening usage detected - perfect time for reflection and deep analysis")
        elif peak_hour <= 8 or peak_hour >= 23:
            recommendations.append("Early/late usage patterns suggest high dedication - maintain this momentum")
        
        # Engagement recommendations
        engagement = usage_patterns.get('usage_trend', 'stable')
        if engagement == 'increasing':
            recommendations.append("Usage is trending up - consider exploring advanced features")
        else:
            recommendations.append("Try setting daily analysis goals to boost engagement")
        
        return recommendations
    
    def _predict_sentiment_trends(self, sentiment_data: Dict) -> List[AnalyticsInsight]:
        """Predict future sentiment trends"""
        insights = []
        
        current_trend = sentiment_data.get('trends', {})
        direction = current_trend.get('direction', 'stable')
        confidence = current_trend.get('confidence', 0.5)
        
        if direction == 'improving' and confidence > 0.7:
            insight = AnalyticsInsight(
                id=f"pred_sent_{int(datetime.now().timestamp())}",
                type="prediction",
                title="Positive Sentiment Momentum",
                description="Current positive trend is likely to continue based on strong confidence indicators",
                confidence=confidence,
                impact="high",
                actionable=True,
                created_at=datetime.now(),
                data_points=current_trend,
                visualization_type="trend_chart"
            )
            insights.append(insight)
        
        return insights
    
    def _predict_user_engagement(self, behavior_data: Dict) -> List[AnalyticsInsight]:
        """Predict user engagement patterns"""
        insights = []
        
        engagement = behavior_data.get('engagement_metrics', {})
        engagement_level = engagement.get('engagement_level', 'low')
        consistency = engagement.get('consistency_score', 0)
        
        if engagement_level == 'high' and consistency > 0.8:
            insight = AnalyticsInsight(
                id=f"pred_eng_{int(datetime.now().timestamp())}",
                type="prediction",
                title="Sustained High Engagement Predicted",
                description="User shows consistent high engagement patterns likely to continue",
                confidence=0.85,
                impact="high",
                actionable=True,
                created_at=datetime.now(),
                data_points=engagement,
                visualization_type="engagement_graph"
            )
            insights.append(insight)
        
        return insights
    
    def _analyze_system_performance(self, data: Dict) -> List[AnalyticsInsight]:
        """Analyze system performance metrics"""
        insights = []
        
        # This would integrate with actual system metrics
        insight = AnalyticsInsight(
            id=f"perf_{int(datetime.now().timestamp())}",
            type="pattern",
            title="Optimal Performance Window",
            description="System shows peak performance during identified usage patterns",
            confidence=0.75,
            impact="medium",
            actionable=True,
            created_at=datetime.now(),
            data_points={'performance': 'optimal'},
            visualization_type="performance_chart"
        )
        insights.append(insight)
        
        return insights
    
    def _generate_executive_summary(self, analysis_data: Dict, user_data: Dict) -> str:
        """Generate executive summary of findings"""
        summary_parts = []
        
        # Sentiment summary
        if analysis_data and 'summary' in analysis_data:
            total = analysis_data['summary'].get('total_analyses', 0)
            dominant = analysis_data['summary'].get('dominant_sentiment', 'neutral')
            summary_parts.append(f"Analyzed {total} sentiment instances with {dominant} sentiment predominating")
        
        # Engagement summary
        if user_data and 'engagement_metrics' in user_data:
            level = user_data['engagement_metrics'].get('engagement_level', 'unknown')
            summary_parts.append(f"User engagement classified as {level}")
        
        # Trend summary
        if analysis_data and 'trends' in analysis_data:
            direction = analysis_data['trends'].get('direction', 'stable')
            summary_parts.append(f"Overall sentiment trend is {direction}")
        
        return ". ".join(summary_parts) if summary_parts else "Comprehensive analysis completed with actionable insights generated"
    
    def _extract_key_metrics(self, analysis_data: Dict, user_data: Dict) -> Dict:
        """Extract key performance metrics"""
        metrics = {}
        
        if analysis_data:
            metrics.update({
                'total_analyses': analysis_data.get('summary', {}).get('total_analyses', 0),
                'sentiment_accuracy': 0.95,  # Would be calculated from actual validation
                'trend_confidence': analysis_data.get('trends', {}).get('confidence', 0)
            })
        
        if user_data:
            metrics.update({
                'engagement_score': user_data.get('engagement_metrics', {}).get('consistency_score', 0),
                'feature_utilization': len(user_data.get('feature_preferences', {}).get('preferences', {}))
            })
        
        return metrics
    
    def _generate_strategic_recommendations(self, analysis_data: Dict, user_data: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Based on sentiment trends
        if analysis_data and 'trends' in analysis_data:
            direction = analysis_data['trends'].get('direction')
            if direction == 'declining':
                recommendations.append("Focus on positive content sources to improve sentiment balance")
            elif direction == 'improving':
                recommendations.append("Maintain current analysis practices as they're yielding positive results")
        
        # Based on user behavior
        if user_data and 'engagement_metrics' in user_data:
            level = user_data['engagement_metrics'].get('engagement_level')
            if level == 'low':
                recommendations.append("Implement gamification features to boost user engagement")
            elif level == 'high':
                recommendations.append("Introduce advanced analytics features to retain power users")
        
        return recommendations
    
    def _suggest_visualizations(self, analysis_data: Dict, user_data: Dict) -> List[Dict]:
        """Suggest appropriate visualizations"""
        visualizations = []
        
        if analysis_data:
            visualizations.append({
                'type': 'sentiment_trend_chart',
                'title': 'Sentiment Trends Over Time',
                'description': 'Line chart showing sentiment evolution',
                'data_source': 'sentiment_trends',
                'priority': 'high'
            })
            
            visualizations.append({
                'type': 'sentiment_distribution_pie',
                'title': 'Sentiment Distribution',
                'description': 'Pie chart of sentiment categories',
                'data_source': 'sentiment_summary',
                'priority': 'medium'
            })
        
        if user_data:
            visualizations.append({
                'type': 'usage_heatmap',
                'title': 'Usage Pattern Heatmap',
                'description': 'Heatmap showing usage by time and day',
                'data_source': 'usage_patterns',
                'priority': 'medium'
            })
        
        return visualizations

class TrendAnalyzer:
    """Specialized trend analysis component"""
    
    def analyze_trend(self, data_points: List[float], timestamps: List[datetime]) -> TrendAnalysis:
        """Analyze trend in time series data"""
        if len(data_points) < 3:
            return TrendAnalysis(
                metric="insufficient_data",
                direction="stable",
                strength=0.0,
                duration=0,
                prediction={}
            )
        
        # Simple linear regression for trend
        x = np.arange(len(data_points))
        slope, _ = np.polyfit(x, data_points, 1)
        
        # Determine direction
        if abs(slope) < 0.01:
            direction = "stable"
        elif slope > 0:
            direction = "up"
        else:
            direction = "down"
        
        # Calculate strength (normalized)
        strength = min(abs(slope), 1.0)
        
        # Simple prediction (next 3 points)
        prediction = {
            'next_values': [data_points[-1] + slope * i for i in range(1, 4)],
            'confidence': max(0.5, 1 - abs(slope) * 0.1)
        }
        
        return TrendAnalysis(
            metric="general",
            direction=direction,
            strength=strength,
            duration=len(data_points),
            prediction=prediction
        )

class PatternDetector:
    """Pattern detection in user behavior and sentiment data"""
    
    def detect_sentiment_patterns(self, df: pd.DataFrame) -> Dict:
        """Detect patterns in sentiment data"""
        if df.empty:
            return {}
        
        patterns = {}
        
        # Time-based patterns
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            hourly_sentiment = df.groupby(['hour', 'sentiment']).size().unstack(fill_value=0)
            
            # Find peak positive/negative hours
            if 'positive' in hourly_sentiment.columns:
                peak_positive_hour = hourly_sentiment['positive'].idxmax()
                patterns['peak_positive_time'] = f"{peak_positive_hour}:00"
            
            if 'negative' in hourly_sentiment.columns:
                peak_negative_hour = hourly_sentiment['negative'].idxmax()
                patterns['peak_negative_time'] = f"{peak_negative_hour}:00"
        
        # Sequential patterns
        sentiments = df['sentiment'].tolist()
        if len(sentiments) > 5:
            # Look for sentiment switches
            switches = sum(1 for i in range(1, len(sentiments)) if sentiments[i] != sentiments[i-1])
            patterns['sentiment_volatility'] = switches / len(sentiments)
        
        return patterns

class AnomalyDetector:
    """Detect anomalies in data patterns"""
    
    def detect_sentiment_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect anomalies in sentiment data"""
        anomalies = []
        
        if df.empty or len(df) < 10:
            return anomalies
        
        # Daily sentiment counts
        df['date'] = df['timestamp'].dt.date
        daily_counts = df.groupby('date').size()
        
        # Statistical anomaly detection (simple Z-score method)
        mean_count = daily_counts.mean()
        std_count = daily_counts.std()
        
        for date, count in daily_counts.items():
            z_score = abs(count - mean_count) / std_count if std_count > 0 else 0
            
            if z_score > 2:  # Anomaly threshold
                anomalies.append({
                    'date': date.isoformat(),
                    'type': 'volume_anomaly',
                    'value': int(count),
                    'expected': round(mean_count, 1),
                    'severity': 'high' if z_score > 3 else 'medium'
                })
        
        return anomalies

class PredictionEngine:
    """Predictive analytics component"""
    
    def predict_user_behavior(self, df: pd.DataFrame) -> Dict:
        """Predict future user behavior"""
        if df.empty:
            return {}
        
        # Simple predictions based on historical patterns
        recent_days = 7
        recent_data = df[df['timestamp'] >= (datetime.now() - timedelta(days=recent_days))]
        
        if recent_data.empty:
            return {}
        
        # Predict next week's activity level
        recent_activity = len(recent_data) / recent_days
        
        # Trend-based adjustment
        if len(df) >= 14:
            previous_week = df[
                (df['timestamp'] >= (datetime.now() - timedelta(days=14))) &
                (df['timestamp'] < (datetime.now() - timedelta(days=7)))
            ]
            if not previous_week.empty:
                previous_activity = len(previous_week) / 7
                trend_factor = recent_activity / previous_activity if previous_activity > 0 else 1
            else:
                trend_factor = 1
        else:
            trend_factor = 1
        
        predicted_activity = recent_activity * trend_factor
        
        return {
            'next_week_activity': round(predicted_activity * 7, 1),
            'daily_average_prediction': round(predicted_activity, 1),
            'trend_factor': round(trend_factor, 2),
            'confidence': min(len(recent_data) / 20, 0.9)  # Higher confidence with more data
        }

class IntelligenceEngine:
    """AI-powered intelligence and insights"""
    
    def generate_smart_insights(self, data: Dict) -> List[str]:
        """Generate intelligent insights from data"""
        insights = []
        
        # This would integrate with more sophisticated AI models
        # For now, using rule-based intelligence
        
        if 'sentiment_trends' in data:
            trends = data['sentiment_trends'].get('trends', {})
            if trends.get('confidence', 0) > 0.8:
                direction = trends.get('direction', 'stable')
                insights.append(f"High confidence {direction} sentiment trend detected - consider strategic adjustments")
        
        if 'user_behavior' in data:
            engagement = data['user_behavior'].get('engagement_metrics', {})
            if engagement.get('engagement_level') == 'high':
                insights.append("User shows power-user characteristics - introduce advanced features")
        
        return insights

def generate_analytics_ui() -> str:
    """Generate advanced analytics UI components"""
    return """
    <!-- Advanced Analytics UI -->
    <div class="analytics-overlay">
        <!-- Analytics Dashboard -->
        <div class="analytics-dashboard glass-card">
            <div class="dashboard-header">
                <h3><i class="fas fa-chart-line"></i> Analytics Intelligence</h3>
                <div class="dashboard-controls">
                    <select id="analyticsTimeframe">
                        <option value="7d">Last 7 days</option>
                        <option value="30d">Last 30 days</option>
                        <option value="90d">Last 90 days</option>
                        <option value="all">All time</option>
                    </select>
                    <button class="refresh-analytics" onclick="refreshAnalytics()">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
            </div>

            <!-- Key Metrics Cards -->
            <div class="metrics-grid">
                <div class="metric-card" id="totalAnalyses">
                    <div class="metric-icon"><i class="fas fa-chart-bar"></i></div>
                    <div class="metric-content">
                        <div class="metric-value">0</div>
                        <div class="metric-label">Total Analyses</div>
                        <div class="metric-change positive">+12%</div>
                    </div>
                </div>
                
                <div class="metric-card" id="sentimentAccuracy">
                    <div class="metric-icon"><i class="fas fa-bullseye"></i></div>
                    <div class="metric-content">
                        <div class="metric-value">95%</div>
                        <div class="metric-label">Accuracy</div>
                        <div class="metric-change positive">+2%</div>
                    </div>
                </div>
                
                <div class="metric-card" id="engagementScore">
                    <div class="metric-icon"><i class="fas fa-heart"></i></div>
                    <div class="metric-content">
                        <div class="metric-value">8.5</div>
                        <div class="metric-label">Engagement</div>
                        <div class="metric-change positive">+0.3</div>
                    </div>
                </div>
                
                <div class="metric-card" id="trendConfidence">
                    <div class="metric-icon"><i class="fas fa-brain"></i></div>
                    <div class="metric-content">
                        <div class="metric-value">87%</div>
                        <div class="metric-label">AI Confidence</div>
                        <div class="metric-change neutral">~</div>
                    </div>
                </div>
            </div>

            <!-- AI Insights Panel -->
            <div class="insights-panel">
                <h4><i class="fas fa-lightbulb"></i> AI-Powered Insights</h4>
                <div class="insights-list" id="aiInsightsList">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Predictions Panel -->
            <div class="predictions-panel">
                <h4><i class="fas fa-crystal-ball"></i> Predictive Analytics</h4>
                <div class="predictions-grid">
                    <div class="prediction-card">
                        <div class="prediction-header">
                            <span class="prediction-title">Next Week Activity</span>
                            <span class="confidence-badge">85%</span>
                        </div>
                        <div class="prediction-value">42 analyses</div>
                        <div class="prediction-trend">
                            <i class="fas fa-arrow-up"></i> +15% expected growth
                        </div>
                    </div>
                    
                    <div class="prediction-card">
                        <div class="prediction-header">
                            <span class="prediction-title">Sentiment Forecast</span>
                            <span class="confidence-badge">72%</span>
                        </div>
                        <div class="prediction-value">Positive trend</div>
                        <div class="prediction-trend">
                            <i class="fas fa-chart-line"></i> Continued improvement
                        </div>
                    </div>
                </div>
            </div>

            <!-- Advanced Charts -->
            <div class="charts-section">
                <div class="chart-tabs">
                    <button class="chart-tab active" data-chart="trends">Trends</button>
                    <button class="chart-tab" data-chart="patterns">Patterns</button>
                    <button class="chart-tab" data-chart="anomalies">Anomalies</button>
                    <button class="chart-tab" data-chart="heatmap">Heatmap</button>
                </div>
                <div class="chart-container" id="analyticsChart">
                    <canvas id="trendsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Intelligence Reports -->
        <div class="reports-panel glass-card">
            <div class="panel-header">
                <h4><i class="fas fa-file-alt"></i> Intelligent Reports</h4>
                <button class="generate-report-btn" onclick="generateReport()">
                    <i class="fas fa-magic"></i> Generate
                </button>
            </div>
            <div class="reports-list" id="reportsList">
                <!-- Populated dynamically -->
            </div>
        </div>
    </div>

    <style>
    /* Advanced Analytics Styles */
    .analytics-overlay {
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        z-index: 940;
        display: flex;
        gap: 20px;
        max-height: 300px;
    }

    .analytics-dashboard {
        flex: 3;
        padding: 20px;
        background: linear-gradient(135deg, rgba(139, 69, 193, 0.1), rgba(99, 102, 241, 0.1));
        border: 1px solid rgba(139, 69, 193, 0.3);
        overflow-y: auto;
    }

    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .dashboard-header h3 {
        margin: 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .dashboard-controls {
        display: flex;
        gap: 10px;
        align-items: center;
    }

    .dashboard-controls select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
    }

    .refresh-analytics {
        background: none;
        border: 1px solid var(--glass-border);
        color: var(--text-secondary);
        padding: 6px 10px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .refresh-analytics:hover {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        transform: rotate(180deg);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
    }

    .metric-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: var(--primary);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }

    .metric-content {
        flex: 1;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 2px;
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }

    .metric-change {
        font-size: 0.75rem;
        font-weight: 500;
    }

    .metric-change.positive { color: #10b981; }
    .metric-change.negative { color: #ef4444; }
    .metric-change.neutral { color: var(--text-secondary); }

    .insights-panel, .predictions-panel {
        margin-bottom: 20px;
    }

    .insights-panel h4, .predictions-panel h4 {
        margin: 0 0 12px 0;
        color: var(--text-primary);
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .insights-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 120px;
        overflow-y: auto;
    }

    .insight-item {
        background: rgba(16, 185, 129, 0.1);
        border-left: 3px solid #10b981;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        color: var(--text-primary);
    }

    .predictions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .prediction-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 12px;
    }

    .prediction-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .prediction-title {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .confidence-badge {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
    }

    .prediction-value {
        font-size: 1.1rem;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 4px;
    }

    .prediction-trend {
        font-size: 0.75rem;
        color: #10b981;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .charts-section {
        border-top: 1px solid var(--glass-border);
        padding-top: 20px;
    }

    .chart-tabs {
        display: flex;
        gap: 8px;
        margin-bottom: 15px;
    }

    .chart-tab {
        background: none;
        border: 1px solid var(--glass-border);
        color: var(--text-secondary);
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }

    .chart-tab.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    .chart-container {
        height: 200px;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 10px;
    }

    .reports-panel {
        flex: 1;
        padding: 20px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 197, 94, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
        overflow-y: auto;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .panel-header h4 {
        margin: 0;
        color: var(--text-primary);
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .generate-report-btn {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .generate-report-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .reports-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .report-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .report-item:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(4px);
    }

    .report-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 4px;
    }

    .report-date {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }

    /* Responsive */
    @media (max-width: 1400px) {
        .analytics-overlay {
            position: relative;
            flex-direction: column;
            max-height: none;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .predictions-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>

    <script>
    // Advanced Analytics JavaScript
    class AdvancedAnalyticsEngine {
        constructor() {
            this.currentTimeframe = '7d';
            this.currentChart = 'trends';
            this.analyticsData = {};
            
            this.initializeAnalytics();
        }
        
        initializeAnalytics() {
            this.setupEventListeners();
            this.loadAnalyticsData();
            this.renderInitialCharts();
        }
        
        setupEventListeners() {
            // Timeframe selector
            const timeframeSelect = document.getElementById('analyticsTimeframe');
            if (timeframeSelect) {
                timeframeSelect.addEventListener('change', (e) => {
                    this.currentTimeframe = e.target.value;
                    this.refreshAnalytics();
                });
            }
            
            // Chart tabs
            document.querySelectorAll('.chart-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    this.switchChart(tab.dataset.chart);
                });
            });
        }
        
        loadAnalyticsData() {
            // Simulate loading analytics data
            this.analyticsData = {
                metrics: {
                    totalAnalyses: 1247,
                    accuracy: 95.2,
                    engagement: 8.5,
                    confidence: 87.3
                },
                trends: {
                    sentiment: [0.6, 0.7, 0.65, 0.8, 0.75, 0.82, 0.85],
                    volume: [12, 15, 18, 22, 19, 25, 28],
                    engagement: [7.2, 7.8, 8.1, 8.5, 8.3, 8.7, 8.5]
                },
                insights: [
                    "Sentiment analysis accuracy improved by 2% this week",
                    "User engagement shows consistent upward trend",
                    "Peak usage occurs during 2-4 PM daily",
                    "Positive sentiment increased by 15% compared to last month"
                ],
                predictions: {
                    nextWeekActivity: 42,
                    sentimentForecast: 'positive',
                    confidenceLevels: [85, 72, 91]
                }
            };
            
            this.updateMetricsDisplay();
            this.updateInsightsDisplay();
        }
        
        updateMetricsDisplay() {
            const metrics = this.analyticsData.metrics;
            
            // Update metric cards
            const totalAnalysesCard = document.querySelector('#totalAnalyses .metric-value');
            if (totalAnalysesCard) {
                totalAnalysesCard.textContent = metrics.totalAnalyses.toLocaleString();
            }
            
            const accuracyCard = document.querySelector('#sentimentAccuracy .metric-value');
            if (accuracyCard) {
                accuracyCard.textContent = `${metrics.accuracy}%`;
            }
            
            const engagementCard = document.querySelector('#engagementScore .metric-value');
            if (engagementCard) {
                engagementCard.textContent = metrics.engagement.toFixed(1);
            }
            
            const confidenceCard = document.querySelector('#trendConfidence .metric-value');
            if (confidenceCard) {
                confidenceCard.textContent = `${metrics.confidence}%`;
            }
        }
        
        updateInsightsDisplay() {
            const insightsList = document.getElementById('aiInsightsList');
            if (!insightsList) return;
            
            insightsList.innerHTML = this.analyticsData.insights.map(insight => `
                <div class="insight-item">
                    <i class="fas fa-lightbulb" style="margin-right: 8px; color: #f59e0b;"></i>
                    ${insight}
                </div>
            `).join('');
        }
        
        switchChart(chartType) {
            this.currentChart = chartType;
            
            // Update active tab
            document.querySelectorAll('.chart-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelector(`[data-chart="${chartType}"]`).classList.add('active');
            
            // Render appropriate chart
            this.renderChart(chartType);
        }
        
        renderChart(chartType) {
            const canvas = document.getElementById('trendsChart');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Simple chart rendering (in production, use Chart.js or similar)
            switch (chartType) {
                case 'trends':
                    this.renderTrendChart(ctx, canvas);
                    break;
                case 'patterns':
                    this.renderPatternChart(ctx, canvas);
                    break;
                case 'anomalies':
                    this.renderAnomalyChart(ctx, canvas);
                    break;
                case 'heatmap':
                    this.renderHeatmapChart(ctx, canvas);
                    break;
            }
        }
        
        renderTrendChart(ctx, canvas) {
            const data = this.analyticsData.trends.sentiment;
            const width = canvas.width;
            const height = canvas.height;
            
            ctx.strokeStyle = '#3b82f6';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            data.forEach((value, index) => {
                const x = (index / (data.length - 1)) * width;
                const y = height - (value * height);
                
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            
            ctx.stroke();
            
            // Add labels
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Arial';
            ctx.fillText('Sentiment Trend Over Time', 10, 20);
        }
        
        renderPatternChart(ctx, canvas) {
            ctx.fillStyle = '#10b981';
            ctx.fillRect(10, 10, 100, 50);
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Arial';
            ctx.fillText('Usage Patterns', 10, 80);
        }
        
        renderAnomalyChart(ctx, canvas) {
            ctx.fillStyle = '#ef4444';
            ctx.fillRect(10, 10, 80, 40);
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Arial';
            ctx.fillText('Detected Anomalies', 10, 70);
        }
        
        renderHeatmapChart(ctx, canvas) {
            // Simple heatmap representation
            const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 7; j++) {
                    ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
                    ctx.fillRect(j * 20 + 10, i * 20 + 10, 18, 18);
                }
            }
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Arial';
            ctx.fillText('Usage Heatmap', 10, 110);
        }
        
        renderInitialCharts() {
            // Set canvas size
            const canvas = document.getElementById('trendsChart');
            if (canvas) {
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;
                this.renderChart('trends');
            }
        }
        
        refreshAnalytics() {
            // Simulate data refresh
            console.log(`Refreshing analytics for ${this.currentTimeframe}`);
            
            // Add loading animation
            const refreshBtn = document.querySelector('.refresh-analytics');
            if (refreshBtn) {
                refreshBtn.style.transform = 'rotate(360deg)';
                setTimeout(() => {
                    refreshBtn.style.transform = '';
                    this.loadAnalyticsData();
                }, 500);
            }
        }
        
        generateReport() {
            console.log('Generating intelligent report...');
            
            // Simulate report generation
            const reportsList = document.getElementById('reportsList');
            if (reportsList) {
                const newReport = document.createElement('div');
                newReport.className = 'report-item';
                newReport.innerHTML = `
                    <div class="report-title">Automated Intelligence Report</div>
                    <div class="report-date">${new Date().toLocaleString()}</div>
                `;
                reportsList.insertBefore(newReport, reportsList.firstChild);
                
                // Limit to 5 reports
                while (reportsList.children.length > 5) {
                    reportsList.removeChild(reportsList.lastChild);
                }
            }
        }
    }
    
    // Global functions
    window.refreshAnalytics = () => {
        if (window.analyticsEngine) {
            window.analyticsEngine.refreshAnalytics();
        }
    };
    
    window.generateReport = () => {
        if (window.analyticsEngine) {
            window.analyticsEngine.generateReport();
        }
    };
    
    // Initialize analytics engine
    window.analyticsEngine = new AdvancedAnalyticsEngine();
    </script>
    """

if __name__ == "__main__":
    print("📊 Advanced Analytics Engine Initialized!")
    print("Features: AI insights, predictive analytics, trend analysis, intelligent reporting")