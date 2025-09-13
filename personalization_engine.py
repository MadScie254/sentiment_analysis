"""
🤖 PERSONALIZATION ENGINE
AI-powered user profiles, preferences, customizable dashboards, and intelligent recommendations
"""

import json
import time
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class UserProfile:
    """User profile data structure"""
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: datetime = None
    preferences: Dict = None
    analysis_history: List = None
    favorite_apis: List = None
    dashboard_layout: Dict = None
    achievements: List = None
    level: int = 1
    total_points: int = 0
    theme_preference: str = 'auto'  # auto, light, dark, custom
    notification_settings: Dict = None
    privacy_settings: Dict = None
    ai_insights_enabled: bool = True
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.preferences is None:
            self.preferences = self._default_preferences()
        if self.analysis_history is None:
            self.analysis_history = []
        if self.favorite_apis is None:
            self.favorite_apis = []
        if self.dashboard_layout is None:
            self.dashboard_layout = self._default_layout()
        if self.achievements is None:
            self.achievements = []
        if self.notification_settings is None:
            self.notification_settings = self._default_notifications()
        if self.privacy_settings is None:
            self.privacy_settings = self._default_privacy()
    
    def _default_preferences(self) -> Dict:
        return {
            'default_analysis_method': 'auto',
            'show_confidence_scores': True,
            'auto_save_analyses': True,
            'preferred_chart_type': 'bar',
            'language': 'en',
            'timezone': 'UTC',
            'data_refresh_interval': 30,
            'show_live_activity': True,
            'enable_sound_notifications': False,
            'compact_view': False
        }
    
    def _default_layout(self) -> Dict:
        return {
            'main_dashboard': {
                'widgets': [
                    {'id': 'sentiment_analyzer', 'position': {'x': 0, 'y': 0, 'w': 6, 'h': 4}},
                    {'id': 'live_stats', 'position': {'x': 6, 'y': 0, 'w': 3, 'h': 2}},
                    {'id': 'recent_analyses', 'position': {'x': 6, 'y': 2, 'w': 3, 'h': 2}},
                    {'id': 'news_feed', 'position': {'x': 0, 'y': 4, 'w': 4, 'h': 3}},
                    {'id': 'api_explorer', 'position': {'x': 4, 'y': 4, 'w': 5, 'h': 3}}
                ]
            },
            'sidebar_panels': ['gamification', 'live_activity', 'achievements']
        }
    
    def _default_notifications(self) -> Dict:
        return {
            'achievements': True,
            'level_ups': True,
            'daily_challenges': True,
            'breaking_news': False,
            'analysis_complete': True,
            'system_updates': True,
            'email_digest': 'weekly'  # never, daily, weekly, monthly
        }
    
    def _default_privacy(self) -> Dict:
        return {
            'share_usage_data': True,
            'public_profile': False,
            'show_in_leaderboards': True,
            'allow_friend_requests': True,
            'data_retention_days': 365
        }

class PersonalizationEngine:
    """
    Advanced personalization system with AI-powered recommendations
    """
    
    def __init__(self):
        self.users = {}  # In production, this would be a database
        self.recommendation_engine = RecommendationEngine()
        self.usage_tracker = UsageTracker()
        self.ai_insights = AIInsights()
        
    def create_user_profile(self, user_id: str, username: str, email: str = None) -> UserProfile:
        """Create a new user profile"""
        profile = UserProfile(
            user_id=user_id,
            username=username,
            email=email
        )
        self.users[user_id] = profile
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        return self.users.get(user_id)
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        profile = self.get_user_profile(user_id)
        if profile:
            profile.preferences.update(preferences)
            return True
        return False
    
    def track_user_activity(self, user_id: str, activity: Dict):
        """Track user activity for personalization"""
        profile = self.get_user_profile(user_id)
        if profile:
            activity['timestamp'] = datetime.now().isoformat()
            profile.analysis_history.append(activity)
            
            # Keep only recent history (last 1000 activities)
            if len(profile.analysis_history) > 1000:
                profile.analysis_history = profile.analysis_history[-1000:]
            
            # Update usage tracker
            self.usage_tracker.track_activity(user_id, activity)
    
    def get_personalized_dashboard(self, user_id: str) -> Dict:
        """Get personalized dashboard configuration"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return self._default_dashboard()
        
        # Get AI recommendations
        recommendations = self.recommendation_engine.get_recommendations(profile)
        
        return {
            'layout': profile.dashboard_layout,
            'theme': self._get_theme_config(profile.theme_preference),
            'recommendations': recommendations,
            'favorite_apis': profile.favorite_apis,
            'quick_actions': self._get_quick_actions(profile),
            'insights': self.ai_insights.generate_insights(profile)
        }
    
    def customize_dashboard_layout(self, user_id: str, layout: Dict) -> bool:
        """Save custom dashboard layout"""
        profile = self.get_user_profile(user_id)
        if profile:
            profile.dashboard_layout = layout
            return True
        return False
    
    def _default_dashboard(self) -> Dict:
        """Default dashboard for new users"""
        return {
            'layout': UserProfile('temp', 'temp').dashboard_layout,
            'theme': self._get_theme_config('auto'),
            'recommendations': [],
            'favorite_apis': [],
            'quick_actions': [],
            'insights': []
        }
    
    def _get_theme_config(self, theme_preference: str) -> Dict:
        """Get theme configuration"""
        themes = {
            'light': {
                'primary_color': '#3b82f6',
                'secondary_color': '#10b981',
                'background': '#ffffff',
                'surface': '#f8fafc',
                'text_primary': '#1e293b',
                'text_secondary': '#64748b'
            },
            'dark': {
                'primary_color': '#6366f1',
                'secondary_color': '#10b981',
                'background': '#0f172a',
                'surface': '#1e293b',
                'text_primary': '#f1f5f9',
                'text_secondary': '#94a3b8'
            },
            'auto': {
                'primary_color': '#3b82f6',
                'secondary_color': '#10b981',
                'background': 'var(--bg-primary)',
                'surface': 'var(--bg-secondary)',
                'text_primary': 'var(--text-primary)',
                'text_secondary': 'var(--text-secondary)'
            }
        }
        return themes.get(theme_preference, themes['auto'])
    
    def _get_quick_actions(self, profile: UserProfile) -> List[Dict]:
        """Get personalized quick actions"""
        actions = []
        
        # Based on usage patterns
        if profile.analysis_history:
            recent_methods = [a.get('method') for a in profile.analysis_history[-10:]]
            most_used_method = max(set(recent_methods), key=recent_methods.count) if recent_methods else 'auto'
            
            actions.append({
                'id': 'quick_analyze',
                'title': f'Quick Analysis ({most_used_method})',
                'icon': '⚡',
                'action': f'analyze_with_{most_used_method}'
            })
        
        # Favorite APIs
        for api in profile.favorite_apis[:3]:
            actions.append({
                'id': f'api_{api}',
                'title': f'{api.title()} API',
                'icon': '🔗',
                'action': f'open_api_{api}'
            })
        
        return actions

class RecommendationEngine:
    """AI-powered recommendation system"""
    
    def __init__(self):
        self.recommendation_cache = {}
        
    def get_recommendations(self, profile: UserProfile) -> List[Dict]:
        """Get personalized recommendations"""
        recommendations = []
        
        # API recommendations based on usage
        api_recs = self._recommend_apis(profile)
        recommendations.extend(api_recs)
        
        # Feature recommendations
        feature_recs = self._recommend_features(profile)
        recommendations.extend(feature_recs)
        
        # Challenge recommendations
        challenge_recs = self._recommend_challenges(profile)
        recommendations.extend(challenge_recs)
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def _recommend_apis(self, profile: UserProfile) -> List[Dict]:
        """Recommend APIs based on usage patterns"""
        recommendations = []
        
        # Analyze usage patterns
        if profile.analysis_history:
            sentiments = [a.get('sentiment') for a in profile.analysis_history[-50:]]
            positive_count = sentiments.count('positive')
            negative_count = sentiments.count('negative')
            
            # Recommend mood-boosting APIs if user has many negative analyses
            if negative_count > positive_count * 1.5:
                recommendations.append({
                    'type': 'api',
                    'title': 'Try Inspirational Quotes',
                    'description': 'Brighten your day with motivational content',
                    'icon': '✨',
                    'action': 'open_quotes_api',
                    'relevance_score': 0.8
                })
        
        # Time-based recommendations
        hour = datetime.now().hour
        if 22 <= hour or hour <= 6:  # Night time
            recommendations.append({
                'type': 'api',
                'title': 'Space Explorer',
                'description': 'Explore the cosmos during quiet hours',
                'icon': '🌌',
                'action': 'open_space_api',
                'relevance_score': 0.7
            })
        
        return recommendations
    
    def _recommend_features(self, profile: UserProfile) -> List[Dict]:
        """Recommend features user hasn't tried"""
        recommendations = []
        
        # Check if user hasn't used visualizations much
        viz_usage = len([a for a in profile.analysis_history if a.get('feature') == 'visualization'])
        if viz_usage < 5:
            recommendations.append({
                'type': 'feature',
                'title': 'Try Data Visualizations',
                'description': 'Create beautiful charts from your analyses',
                'icon': '📊',
                'action': 'open_visualizations',
                'relevance_score': 0.6
            })
        
        return recommendations
    
    def _recommend_challenges(self, profile: UserProfile) -> List[Dict]:
        """Recommend personalized challenges"""
        recommendations = []
        
        analyses_count = len(profile.analysis_history)
        if analyses_count > 10 and analyses_count < 50:
            recommendations.append({
                'type': 'challenge',
                'title': 'Analysis Explorer Challenge',
                'description': 'Analyze 20 more texts to unlock rewards',
                'icon': '🏆',
                'action': 'start_challenge',
                'relevance_score': 0.9
            })
        
        return recommendations

class UsageTracker:
    """Track user usage patterns for insights"""
    
    def __init__(self):
        self.usage_data = defaultdict(list)
        
    def track_activity(self, user_id: str, activity: Dict):
        """Track user activity"""
        self.usage_data[user_id].append({
            'activity': activity,
            'timestamp': datetime.now(),
            'hour': datetime.now().hour,
            'day_of_week': datetime.now().weekday()
        })
    
    def get_usage_patterns(self, user_id: str) -> Dict:
        """Analyze usage patterns"""
        activities = self.usage_data.get(user_id, [])
        if not activities:
            return {}
        
        # Time patterns
        hours = [a['hour'] for a in activities]
        most_active_hour = max(set(hours), key=hours.count) if hours else None
        
        # Day patterns
        days = [a['day_of_week'] for a in activities]
        most_active_day = max(set(days), key=days.count) if days else None
        
        # Feature usage
        features = [a['activity'].get('feature') for a in activities]
        favorite_feature = max(set(features), key=features.count) if features else None
        
        return {
            'total_activities': len(activities),
            'most_active_hour': most_active_hour,
            'most_active_day': most_active_day,
            'favorite_feature': favorite_feature,
            'active_days': len(set(a['timestamp'].date() for a in activities))
        }

class AIInsights:
    """Generate AI-powered insights for users"""
    
    def generate_insights(self, profile: UserProfile) -> List[Dict]:
        """Generate personalized insights"""
        insights = []
        
        if len(profile.analysis_history) < 5:
            insights.append({
                'type': 'tip',
                'title': 'Getting Started',
                'message': 'Try analyzing different types of text to see how sentiment varies!',
                'icon': '💡'
            })
            return insights
        
        # Sentiment pattern insights
        recent_analyses = profile.analysis_history[-20:]
        sentiments = [a.get('sentiment') for a in recent_analyses]
        
        positive_ratio = sentiments.count('positive') / len(sentiments)
        if positive_ratio > 0.7:
            insights.append({
                'type': 'pattern',
                'title': 'Optimistic Analyzer!',
                'message': f'{int(positive_ratio * 100)}% of your recent analyses were positive. You tend to work with uplifting content!',
                'icon': '😊'
            })
        elif positive_ratio < 0.3:
            insights.append({
                'type': 'pattern',
                'title': 'Critical Thinker',
                'message': 'You often analyze challenging content. Consider balancing with positive examples!',
                'icon': '🤔'
            })
        
        # Usage time insights
        if profile.analysis_history:
            hours = [datetime.fromisoformat(a['timestamp']).hour for a in profile.analysis_history[-50:] if 'timestamp' in a]
            if hours:
                most_active = max(set(hours), key=hours.count)
                if most_active < 6:
                    insights.append({
                        'type': 'habit',
                        'title': 'Night Owl Detected!',
                        'message': 'You\'re most active in the early morning hours. 🦉',
                        'icon': '🌙'
                    })
                elif 9 <= most_active <= 17:
                    insights.append({
                        'type': 'habit',
                        'title': 'Business Hours Focus',
                        'message': 'You prefer analyzing during work hours. Very professional!',
                        'icon': '💼'
                    })
        
        # Achievement progress
        if profile.total_points > 0:
            insights.append({
                'type': 'progress',
                'title': 'Level Progress',
                'message': f'You\'re at level {profile.level} with {profile.total_points} total points. Keep it up!',
                'icon': '📈'
            })
        
        return insights

def generate_personalization_ui() -> str:
    """Generate personalization UI components"""
    return """
    <!-- Personalization UI Components -->
    <div class="personalization-overlay">
        <!-- User Profile Panel -->
        <div class="user-profile-panel glass-card">
            <div class="profile-header">
                <div class="avatar" id="userAvatar">
                    <span id="avatarText">U</span>
                </div>
                <div class="profile-info">
                    <div class="username" id="username">Guest User</div>
                    <div class="user-level">Level <span id="userLevel">1</span></div>
                    <div class="user-points"><span id="userPoints">0</span> points</div>
                </div>
                <button class="settings-btn" onclick="openUserSettings()">
                    <i class="fas fa-cog"></i>
                </button>
            </div>
            
            <div class="quick-stats">
                <div class="stat-chip">
                    <span class="stat-value" id="totalAnalyses">0</span>
                    <span class="stat-label">Analyses</span>
                </div>
                <div class="stat-chip">
                    <span class="stat-value" id="streakDays">0</span>
                    <span class="stat-label">Day Streak</span>
                </div>
                <div class="stat-chip">
                    <span class="stat-value" id="favoriteAPIs">0</span>
                    <span class="stat-label">Fav APIs</span>
                </div>
            </div>
        </div>

        <!-- AI Recommendations Panel -->
        <div class="recommendations-panel glass-card">
            <h3><i class="fas fa-magic"></i> Recommended for You</h3>
            <div class="recommendations-list" id="recommendationsList">
                <!-- Populated dynamically -->
            </div>
        </div>

        <!-- AI Insights Panel -->
        <div class="insights-panel glass-card">
            <h3><i class="fas fa-brain"></i> Your Insights</h3>
            <div class="insights-list" id="insightsList">
                <!-- Populated dynamically -->
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions-panel glass-card">
            <h3><i class="fas fa-bolt"></i> Quick Actions</h3>
            <div class="quick-actions-grid" id="quickActionsGrid">
                <!-- Populated dynamically -->
            </div>
        </div>
    </div>

    <!-- User Settings Modal -->
    <div id="userSettingsModal" class="modal hidden">
        <div class="modal-content glass-card">
            <div class="modal-header">
                <h2>User Settings</h2>
                <button class="close-btn" onclick="closeUserSettings()">×</button>
            </div>
            
            <div class="settings-tabs">
                <button class="tab-btn active" data-tab="profile">Profile</button>
                <button class="tab-btn" data-tab="preferences">Preferences</button>
                <button class="tab-btn" data-tab="dashboard">Dashboard</button>
                <button class="tab-btn" data-tab="privacy">Privacy</button>
            </div>

            <div class="settings-content">
                <!-- Profile Settings -->
                <div class="tab-pane active" id="profile-settings">
                    <div class="setting-group">
                        <label>Username</label>
                        <input type="text" id="settingsUsername" class="setting-input">
                    </div>
                    <div class="setting-group">
                        <label>Email</label>
                        <input type="email" id="settingsEmail" class="setting-input">
                    </div>
                    <div class="setting-group">
                        <label>Theme</label>
                        <select id="themeSelect" class="setting-input">
                            <option value="auto">Auto</option>
                            <option value="light">Light</option>
                            <option value="dark">Dark</option>
                        </select>
                    </div>
                </div>

                <!-- Preferences Settings -->
                <div class="tab-pane" id="preferences-settings">
                    <div class="setting-group">
                        <label>Default Analysis Method</label>
                        <select id="defaultMethod" class="setting-input">
                            <option value="auto">Auto</option>
                            <option value="vader">VADER</option>
                            <option value="textblob">TextBlob</option>
                            <option value="huggingface">HuggingFace</option>
                        </select>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="showConfidence">
                            <span class="checkmark"></span>
                            Show Confidence Scores
                        </label>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="autoSave">
                            <span class="checkmark"></span>
                            Auto-save Analyses
                        </label>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="soundNotifications">
                            <span class="checkmark"></span>
                            Sound Notifications
                        </label>
                    </div>
                </div>

                <!-- Dashboard Settings -->
                <div class="tab-pane" id="dashboard-settings">
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="compactView">
                            <span class="checkmark"></span>
                            Compact View
                        </label>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="showLiveActivity">
                            <span class="checkmark"></span>
                            Show Live Activity
                        </label>
                    </div>
                    <div class="setting-group">
                        <label>Data Refresh Interval</label>
                        <select id="refreshInterval" class="setting-input">
                            <option value="10">10 seconds</option>
                            <option value="30">30 seconds</option>
                            <option value="60">1 minute</option>
                            <option value="300">5 minutes</option>
                        </select>
                    </div>
                    <button class="reset-layout-btn" onclick="resetDashboardLayout()">
                        Reset Dashboard Layout
                    </button>
                </div>

                <!-- Privacy Settings -->
                <div class="tab-pane" id="privacy-settings">
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="shareUsageData">
                            <span class="checkmark"></span>
                            Share Usage Data for Improvements
                        </label>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="publicProfile">
                            <span class="checkmark"></span>
                            Public Profile
                        </label>
                    </div>
                    <div class="setting-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="showInLeaderboards">
                            <span class="checkmark"></span>
                            Show in Leaderboards
                        </label>
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn-secondary" onclick="closeUserSettings()">Cancel</button>
                <button class="btn-primary" onclick="saveUserSettings()">Save Settings</button>
            </div>
        </div>
    </div>

    <style>
    /* Personalization UI Styles */
    .personalization-overlay {
        position: fixed;
        top: 20px;
        right: 340px; /* Next to gamification overlay */
        width: 280px;
        z-index: 950;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: calc(100vh - 40px);
        overflow-y: auto;
    }

    .user-profile-panel {
        padding: 20px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 69, 193, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .profile-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }

    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        color: white;
    }

    .profile-info {
        flex: 1;
    }

    .username {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-primary);
        margin-bottom: 2px;
    }

    .user-level, .user-points {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    .settings-btn {
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    .settings-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-primary);
    }

    .quick-stats {
        display: flex;
        gap: 8px;
    }

    .stat-chip {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-chip:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: scale(1.05);
    }

    .stat-value {
        display: block;
        font-size: 1.1rem;
        font-weight: bold;
        color: var(--primary);
    }

    .stat-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
    }

    .recommendations-panel, .insights-panel, .quick-actions-panel {
        padding: 15px;
    }

    .recommendations-list, .insights-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 12px;
    }

    .recommendation-item, .insight-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        border-left: 3px solid var(--primary);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .recommendation-item:hover, .insight-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }

    .recommendation-title, .insight-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-primary);
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .recommendation-desc, .insight-message {
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.3;
    }

    .quick-actions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 12px;
    }

    .quick-action-btn {
        background: rgba(255, 255, 255, 0.05);
        border: none;
        border-radius: 8px;
        padding: 12px;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
    }

    .quick-action-btn:hover {
        background: var(--primary);
        color: white;
        transform: scale(1.05);
    }

    .action-icon {
        font-size: 1.5rem;
    }

    .action-title {
        font-size: 0.8rem;
        font-weight: 500;
        text-align: center;
    }

    /* Modal Styles */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    }

    .modal.hidden {
        display: none;
    }

    .modal-content {
        width: 90%;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        padding: 0;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 20px 0 20px;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 20px;
    }

    .close-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--text-secondary);
        cursor: pointer;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-primary);
    }

    .settings-tabs {
        display: flex;
        gap: 4px;
        margin: 0 20px;
        border-bottom: 1px solid var(--glass-border);
    }

    .settings-tabs .tab-btn {
        background: none;
        border: none;
        padding: 12px 16px;
        color: var(--text-secondary);
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }

    .settings-tabs .tab-btn.active {
        color: var(--primary);
        border-bottom-color: var(--primary);
    }

    .settings-tabs .tab-btn:hover:not(.active) {
        color: var(--text-primary);
    }

    .settings-content {
        padding: 20px;
    }

    .tab-pane {
        display: none;
    }

    .tab-pane.active {
        display: block;
    }

    .setting-group {
        margin-bottom: 20px;
    }

    .setting-group label:not(.checkbox-label) {
        display: block;
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 6px;
        font-size: 0.9rem;
    }

    .setting-input {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 10px 12px;
        color: var(--text-primary);
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .setting-input:focus {
        outline: none;
        border-color: var(--primary);
        background: rgba(255, 255, 255, 0.1);
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        color: var(--text-primary);
        font-size: 0.9rem;
    }

    .checkbox-label input[type="checkbox"] {
        display: none;
    }

    .checkmark {
        width: 18px;
        height: 18px;
        border: 2px solid var(--glass-border);
        border-radius: 4px;
        position: relative;
        transition: all 0.3s ease;
    }

    .checkbox-label input[type="checkbox"]:checked + .checkmark {
        background: var(--primary);
        border-color: var(--primary);
    }

    .checkbox-label input[type="checkbox"]:checked + .checkmark::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }

    .reset-layout-btn {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444;
        padding: 10px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .reset-layout-btn:hover {
        background: rgba(239, 68, 68, 0.2);
    }

    .modal-footer {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        padding: 20px;
        border-top: 1px solid var(--glass-border);
    }

    .btn-primary, .btn-secondary {
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }

    .btn-primary {
        background: var(--primary);
        color: white;
    }

    .btn-primary:hover {
        background: color-mix(in srgb, var(--primary) 80%, white);
        transform: translateY(-1px);
    }

    .btn-secondary {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-primary);
        border: 1px solid var(--glass-border);
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    /* Responsive */
    @media (max-width: 1400px) {
        .personalization-overlay {
            position: relative;
            width: 100%;
            right: 0;
            margin-bottom: 20px;
        }
    }
    </style>
    """

if __name__ == "__main__":
    print("🤖 Personalization Engine Initialized!")
    print("Features: User profiles, AI recommendations, custom layouts, insights")