"""
🤝 SOCIAL FEATURES ENGINE
User sharing, collaboration, community features, and social analytics
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import uuid

@dataclass
class SocialProfile:
    """Extended user profile with social features"""
    user_id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    followers: Set[str] = None
    following: Set[str] = None
    public_analyses: List[str] = None
    shared_collections: List[str] = None
    collaboration_invites: List[str] = None
    reputation_score: int = 0
    verified: bool = False
    
    def __post_init__(self):
        if self.followers is None:
            self.followers = set()
        if self.following is None:
            self.following = set()
        if self.public_analyses is None:
            self.public_analyses = []
        if self.shared_collections is None:
            self.shared_collections = []
        if self.collaboration_invites is None:
            self.collaboration_invites = []

@dataclass
class SharedAnalysis:
    """Shareable analysis with social features"""
    id: str
    user_id: str
    username: str
    title: str
    content: str
    analysis_results: Dict
    created_at: datetime
    likes: Set[str] = None
    comments: List[Dict] = None
    shares: int = 0
    visibility: str = 'public'  # public, private, friends
    tags: List[str] = None
    
    def __post_init__(self):
        if self.likes is None:
            self.likes = set()
        if self.comments is None:
            self.comments = []
        if self.tags is None:
            self.tags = []

@dataclass
class CollaborationSpace:
    """Collaborative workspace for team analysis"""
    id: str
    name: str
    description: str
    owner_id: str
    members: Set[str] = None
    analyses: List[str] = None
    created_at: datetime = None
    last_activity: datetime = None
    permissions: Dict = None
    
    def __post_init__(self):
        if self.members is None:
            self.members = set()
        if self.analyses is None:
            self.analyses = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_activity is None:
            self.last_activity = datetime.now()
        if self.permissions is None:
            self.permissions = {'view': True, 'comment': True, 'edit': False}

class SocialEngine:
    """
    Complete social features system for collaborative sentiment analysis
    """
    
    def __init__(self):
        self.social_profiles = {}
        self.shared_analyses = {}
        self.collaboration_spaces = {}
        self.activity_feed = []
        self.trending_tags = defaultdict(int)
        self.leaderboards = {}
        
    def create_social_profile(self, user_id: str, username: str, display_name: str) -> SocialProfile:
        """Create social profile for user"""
        profile = SocialProfile(
            user_id=user_id,
            username=username,
            display_name=display_name
        )
        self.social_profiles[user_id] = profile
        return profile
    
    def follow_user(self, follower_id: str, following_id: str) -> bool:
        """Follow another user"""
        if follower_id == following_id:
            return False
            
        follower = self.social_profiles.get(follower_id)
        following = self.social_profiles.get(following_id)
        
        if follower and following:
            follower.following.add(following_id)
            following.followers.add(follower_id)
            
            self._add_activity({
                'type': 'follow',
                'user_id': follower_id,
                'username': follower.username,
                'target_user_id': following_id,
                'target_username': following.username,
                'timestamp': datetime.now()
            })
            return True
        return False
    
    def unfollow_user(self, follower_id: str, following_id: str) -> bool:
        """Unfollow user"""
        follower = self.social_profiles.get(follower_id)
        following = self.social_profiles.get(following_id)
        
        if follower and following:
            follower.following.discard(following_id)
            following.followers.discard(follower_id)
            return True
        return False
    
    def share_analysis(self, user_id: str, title: str, content: str, 
                      analysis_results: Dict, visibility: str = 'public',
                      tags: List[str] = None) -> SharedAnalysis:
        """Share analysis with community"""
        analysis_id = str(uuid.uuid4())
        user_profile = self.social_profiles.get(user_id)
        
        shared_analysis = SharedAnalysis(
            id=analysis_id,
            user_id=user_id,
            username=user_profile.username if user_profile else 'Unknown',
            title=title,
            content=content,
            analysis_results=analysis_results,
            created_at=datetime.now(),
            visibility=visibility,
            tags=tags or []
        )
        
        self.shared_analyses[analysis_id] = shared_analysis
        
        # Update user's public analyses
        if user_profile:
            user_profile.public_analyses.append(analysis_id)
        
        # Update trending tags
        for tag in shared_analysis.tags:
            self.trending_tags[tag.lower()] += 1
        
        # Add to activity feed
        self._add_activity({
            'type': 'share',
            'user_id': user_id,
            'username': shared_analysis.username,
            'analysis_id': analysis_id,
            'title': title,
            'timestamp': datetime.now()
        })
        
        return shared_analysis
    
    def like_analysis(self, user_id: str, analysis_id: str) -> bool:
        """Like a shared analysis"""
        analysis = self.shared_analyses.get(analysis_id)
        if analysis:
            analysis.likes.add(user_id)
            
            self._add_activity({
                'type': 'like',
                'user_id': user_id,
                'analysis_id': analysis_id,
                'timestamp': datetime.now()
            })
            return True
        return False
    
    def unlike_analysis(self, user_id: str, analysis_id: str) -> bool:
        """Unlike a shared analysis"""
        analysis = self.shared_analyses.get(analysis_id)
        if analysis:
            analysis.likes.discard(user_id)
            return True
        return False
    
    def comment_on_analysis(self, user_id: str, analysis_id: str, comment: str) -> bool:
        """Add comment to shared analysis"""
        analysis = self.shared_analyses.get(analysis_id)
        user_profile = self.social_profiles.get(user_id)
        
        if analysis and user_profile:
            comment_data = {
                'id': str(uuid.uuid4()),
                'user_id': user_id,
                'username': user_profile.username,
                'comment': comment,
                'timestamp': datetime.now().isoformat(),
                'likes': []
            }
            analysis.comments.append(comment_data)
            
            self._add_activity({
                'type': 'comment',
                'user_id': user_id,
                'username': user_profile.username,
                'analysis_id': analysis_id,
                'timestamp': datetime.now()
            })
            return True
        return False
    
    def create_collaboration_space(self, owner_id: str, name: str, description: str) -> CollaborationSpace:
        """Create collaboration space"""
        space_id = str(uuid.uuid4())
        space = CollaborationSpace(
            id=space_id,
            name=name,
            description=description,
            owner_id=owner_id
        )
        space.members.add(owner_id)
        
        self.collaboration_spaces[space_id] = space
        
        # Add to owner's shared collections
        owner_profile = self.social_profiles.get(owner_id)
        if owner_profile:
            owner_profile.shared_collections.append(space_id)
        
        return space
    
    def invite_to_collaboration(self, space_id: str, inviter_id: str, invitee_id: str) -> bool:
        """Invite user to collaboration space"""
        space = self.collaboration_spaces.get(space_id)
        invitee_profile = self.social_profiles.get(invitee_id)
        
        if space and invitee_profile and inviter_id in space.members:
            invite_data = {
                'id': str(uuid.uuid4()),
                'space_id': space_id,
                'space_name': space.name,
                'inviter_id': inviter_id,
                'timestamp': datetime.now().isoformat()
            }
            invitee_profile.collaboration_invites.append(invite_data)
            return True
        return False
    
    def accept_collaboration_invite(self, user_id: str, invite_id: str) -> bool:
        """Accept collaboration invite"""
        user_profile = self.social_profiles.get(user_id)
        if not user_profile:
            return False
        
        # Find and remove invite
        for invite in user_profile.collaboration_invites:
            if invite['id'] == invite_id:
                space_id = invite['space_id']
                space = self.collaboration_spaces.get(space_id)
                if space:
                    space.members.add(user_id)
                    user_profile.shared_collections.append(space_id)
                user_profile.collaboration_invites.remove(invite)
                return True
        return False
    
    def get_activity_feed(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get personalized activity feed"""
        user_profile = self.social_profiles.get(user_id)
        if not user_profile:
            return []
        
        # Get activities from followed users
        relevant_activities = []
        following_ids = user_profile.following.copy()
        following_ids.add(user_id)  # Include own activities
        
        for activity in self.activity_feed:
            if activity['user_id'] in following_ids:
                relevant_activities.append(activity)
        
        # Sort by timestamp and limit
        relevant_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return relevant_activities[:limit]
    
    def get_trending_analyses(self, limit: int = 10) -> List[SharedAnalysis]:
        """Get trending analyses based on engagement"""
        # Calculate engagement score for each analysis
        scored_analyses = []
        for analysis in self.shared_analyses.values():
            if analysis.visibility == 'public':
                engagement_score = (
                    len(analysis.likes) * 2 +
                    len(analysis.comments) * 3 +
                    analysis.shares * 1
                )
                scored_analyses.append((engagement_score, analysis))
        
        # Sort by engagement and return top analyses
        scored_analyses.sort(key=lambda x: x[0], reverse=True)
        return [analysis for _, analysis in scored_analyses[:limit]]
    
    def get_trending_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get trending hashtags"""
        sorted_tags = sorted(self.trending_tags.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags[:limit]
    
    def search_analyses(self, query: str, limit: int = 20) -> List[SharedAnalysis]:
        """Search shared analyses"""
        results = []
        query_lower = query.lower()
        
        for analysis in self.shared_analyses.values():
            if analysis.visibility == 'public':
                # Search in title, content, and tags
                if (query_lower in analysis.title.lower() or
                    query_lower in analysis.content.lower() or
                    any(query_lower in tag.lower() for tag in analysis.tags)):
                    results.append(analysis)
        
        # Sort by relevance (simple text matching score)
        def relevance_score(analysis):
            score = 0
            if query_lower in analysis.title.lower():
                score += 10
            if query_lower in analysis.content.lower():
                score += 5
            for tag in analysis.tags:
                if query_lower in tag.lower():
                    score += 3
            return score
        
        results.sort(key=relevance_score, reverse=True)
        return results[:limit]
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user social statistics"""
        profile = self.social_profiles.get(user_id)
        if not profile:
            return {}
        
        total_likes = 0
        total_comments = 0
        total_shares = 0
        
        for analysis_id in profile.public_analyses:
            analysis = self.shared_analyses.get(analysis_id)
            if analysis:
                total_likes += len(analysis.likes)
                total_comments += len(analysis.comments)
                total_shares += analysis.shares
        
        return {
            'followers_count': len(profile.followers),
            'following_count': len(profile.following),
            'analyses_count': len(profile.public_analyses),
            'total_likes_received': total_likes,
            'total_comments_received': total_comments,
            'total_shares_received': total_shares,
            'reputation_score': profile.reputation_score,
            'collaborations_count': len(profile.shared_collections)
        }
    
    def _add_activity(self, activity: Dict):
        """Add activity to feed"""
        self.activity_feed.append(activity)
        
        # Keep only recent activities (last 1000)
        if len(self.activity_feed) > 1000:
            self.activity_feed = self.activity_feed[-1000:]

def generate_social_ui() -> str:
    """Generate social features UI components"""
    return """
    <!-- Social Features UI -->
    <div class="social-overlay">
        <!-- Social Navigation -->
        <div class="social-nav glass-card">
            <div class="nav-tabs">
                <button class="nav-tab active" data-tab="feed">
                    <i class="fas fa-home"></i> Feed
                </button>
                <button class="nav-tab" data-tab="discover">
                    <i class="fas fa-compass"></i> Discover
                </button>
                <button class="nav-tab" data-tab="collaborate">
                    <i class="fas fa-users"></i> Collaborate
                </button>
                <button class="nav-tab" data-tab="profile">
                    <i class="fas fa-user"></i> Profile
                </button>
            </div>
        </div>

        <!-- Activity Feed Tab -->
        <div class="social-tab-content active" id="feed-tab">
            <div class="feed-panel glass-card">
                <div class="panel-header">
                    <h3><i class="fas fa-stream"></i> Activity Feed</h3>
                    <button class="refresh-btn" onclick="refreshFeed()">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
                <div class="feed-content" id="activityFeed">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="quick-share glass-card">
                <h4>Quick Share</h4>
                <div class="share-form">
                    <input type="text" id="quickShareTitle" placeholder="Analysis title...">
                    <textarea id="quickShareContent" placeholder="Share your insights..."></textarea>
                    <div class="share-options">
                        <select id="shareVisibility">
                            <option value="public">Public</option>
                            <option value="friends">Friends Only</option>
                            <option value="private">Private</option>
                        </select>
                        <input type="text" id="shareTags" placeholder="Tags (comma-separated)">
                    </div>
                    <button class="share-btn" onclick="quickShare()">
                        <i class="fas fa-share"></i> Share
                    </button>
                </div>
            </div>
        </div>

        <!-- Discover Tab -->
        <div class="social-tab-content" id="discover-tab">
            <div class="discover-panel glass-card">
                <div class="search-bar">
                    <input type="text" id="socialSearch" placeholder="Search analyses, users, tags...">
                    <button onclick="performSocialSearch()">
                        <i class="fas fa-search"></i>
                    </button>
                </div>

                <div class="trending-section">
                    <h4><i class="fas fa-fire"></i> Trending</h4>
                    <div class="trending-tabs">
                        <button class="trending-tab active" data-type="analyses">Analyses</button>
                        <button class="trending-tab" data-type="tags">Tags</button>
                        <button class="trending-tab" data-type="users">Users</button>
                    </div>
                    <div class="trending-content" id="trendingContent">
                        <!-- Populated dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Collaboration Tab -->
        <div class="social-tab-content" id="collaborate-tab">
            <div class="collaboration-panel glass-card">
                <div class="panel-header">
                    <h3><i class="fas fa-users"></i> Collaboration Spaces</h3>
                    <button class="create-space-btn" onclick="openCreateSpaceModal()">
                        <i class="fas fa-plus"></i> Create
                    </button>
                </div>
                <div class="spaces-list" id="collaborationSpaces">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="invites-panel glass-card">
                <h4><i class="fas fa-envelope"></i> Invitations</h4>
                <div class="invites-list" id="collaborationInvites">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>

        <!-- Social Profile Tab -->
        <div class="social-tab-content" id="profile-tab">
            <div class="social-profile-panel glass-card">
                <div class="profile-header">
                    <div class="profile-avatar">
                        <img id="profileAvatar" src="" alt="Avatar">
                    </div>
                    <div class="profile-info">
                        <h3 id="profileDisplayName">Display Name</h3>
                        <p id="profileUsername">@username</p>
                        <p id="profileBio">User bio goes here...</p>
                    </div>
                    <button class="edit-profile-btn" onclick="editProfile()">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>

                <div class="profile-stats">
                    <div class="stat">
                        <span class="stat-value" id="followersCount">0</span>
                        <span class="stat-label">Followers</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value" id="followingCount">0</span>
                        <span class="stat-label">Following</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value" id="analysesCount">0</span>
                        <span class="stat-label">Analyses</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value" id="reputationScore">0</span>
                        <span class="stat-label">Reputation</span>
                    </div>
                </div>

                <div class="profile-tabs">
                    <button class="profile-tab active" data-tab="analyses">My Analyses</button>
                    <button class="profile-tab" data-tab="liked">Liked</button>
                    <button class="profile-tab" data-tab="collections">Collections</button>
                </div>

                <div class="profile-content" id="profileContent">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </div>

    <!-- Shared Analysis Card Template -->
    <template id="analysisCardTemplate">
        <div class="analysis-card glass-card">
            <div class="card-header">
                <div class="user-info">
                    <div class="user-avatar">
                        <span class="avatar-text"></span>
                    </div>
                    <div>
                        <div class="username"></div>
                        <div class="timestamp"></div>
                    </div>
                </div>
                <button class="card-menu">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
            </div>

            <div class="card-content">
                <h4 class="analysis-title"></h4>
                <p class="analysis-excerpt"></p>
                <div class="analysis-results">
                    <div class="sentiment-badge">
                        <span class="sentiment-label"></span>
                        <span class="confidence-score"></span>
                    </div>
                </div>
                <div class="analysis-tags"></div>
            </div>

            <div class="card-actions">
                <button class="action-btn like-btn">
                    <i class="fas fa-heart"></i>
                    <span class="action-count">0</span>
                </button>
                <button class="action-btn comment-btn">
                    <i class="fas fa-comment"></i>
                    <span class="action-count">0</span>
                </button>
                <button class="action-btn share-btn">
                    <i class="fas fa-share"></i>
                    <span class="action-count">0</span>
                </button>
                <button class="action-btn bookmark-btn">
                    <i class="fas fa-bookmark"></i>
                </button>
            </div>

            <div class="comments-section hidden">
                <div class="comments-list"></div>
                <div class="comment-input">
                    <input type="text" placeholder="Add a comment...">
                    <button class="post-comment-btn">Post</button>
                </div>
            </div>
        </div>
    </template>

    <!-- Create Collaboration Space Modal -->
    <div id="createSpaceModal" class="modal hidden">
        <div class="modal-content glass-card">
            <div class="modal-header">
                <h2>Create Collaboration Space</h2>
                <button class="close-btn" onclick="closeCreateSpaceModal()">×</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Space Name</label>
                    <input type="text" id="spaceName" placeholder="Enter space name">
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="spaceDescription" placeholder="Describe your collaboration space"></textarea>
                </div>
                <div class="form-group">
                    <label>Privacy</label>
                    <select id="spacePrivacy">
                        <option value="public">Public - Anyone can join</option>
                        <option value="private">Private - Invite only</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-secondary" onclick="closeCreateSpaceModal()">Cancel</button>
                <button class="btn-primary" onclick="createCollaborationSpace()">Create Space</button>
            </div>
        </div>
    </div>

    <style>
    /* Social Features Styles */
    .social-overlay {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 300px;
        z-index: 960;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: calc(100vh - 40px);
        overflow-y: auto;
    }

    .social-nav {
        padding: 15px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 197, 94, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .nav-tabs {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
    }

    .nav-tab {
        background: none;
        border: none;
        padding: 10px;
        color: var(--text-secondary);
        cursor: pointer;
        border-radius: 6px;
        transition: all 0.3s ease;
        font-size: 0.8rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }

    .nav-tab.active {
        background: var(--primary);
        color: white;
    }

    .nav-tab:hover:not(.active) {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-primary);
    }

    .social-tab-content {
        display: none;
        flex-direction: column;
        gap: 15px;
    }

    .social-tab-content.active {
        display: flex;
    }

    .feed-panel, .discover-panel, .collaboration-panel, .social-profile-panel {
        padding: 20px;
        max-height: 400px;
        overflow-y: auto;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .panel-header h3 {
        margin: 0;
        font-size: 1.1rem;
        color: var(--text-primary);
    }

    .refresh-btn, .create-space-btn {
        background: none;
        border: 1px solid var(--glass-border);
        color: var(--text-secondary);
        padding: 6px 10px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.8rem;
    }

    .refresh-btn:hover, .create-space-btn:hover {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    .quick-share {
        padding: 15px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .quick-share h4 {
        margin: 0 0 10px 0;
        font-size: 1rem;
        color: var(--text-primary);
    }

    .share-form {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .share-form input, .share-form textarea, .share-form select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 6px;
        padding: 8px;
        color: var(--text-primary);
        font-size: 0.8rem;
        resize: vertical;
    }

    .share-form textarea {
        min-height: 60px;
    }

    .share-options {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .share-btn {
        background: var(--primary);
        color: white;
        border: none;
        padding: 10px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .share-btn:hover {
        background: color-mix(in srgb, var(--primary) 80%, white);
        transform: translateY(-1px);
    }

    .search-bar {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .search-bar input {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 10px 15px;
        color: var(--text-primary);
        font-size: 0.8rem;
    }

    .search-bar button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .search-bar button:hover {
        transform: scale(1.1);
    }

    .trending-tabs {
        display: flex;
        gap: 5px;
        margin-bottom: 15px;
    }

    .trending-tab {
        background: none;
        border: 1px solid var(--glass-border);
        color: var(--text-secondary);
        padding: 6px 12px;
        border-radius: 15px;
        cursor: pointer;
        font-size: 0.75rem;
        transition: all 0.3s ease;
    }

    .trending-tab.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    .analysis-card {
        margin-bottom: 15px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
    }

    .analysis-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }

    .user-info {
        display: flex;
        gap: 10px;
        align-items: center;
    }

    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--primary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }

    .username {
        font-weight: 600;
        font-size: 0.85rem;
        color: var(--text-primary);
    }

    .timestamp {
        font-size: 0.7rem;
        color: var(--text-secondary);
    }

    .card-menu {
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: all 0.3s ease;
    }

    .card-menu:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .card-content {
        margin-bottom: 12px;
    }

    .analysis-title {
        margin: 0 0 6px 0;
        font-size: 0.95rem;
        color: var(--text-primary);
        font-weight: 600;
    }

    .analysis-excerpt {
        margin: 0 0 10px 0;
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }

    .analysis-results {
        margin-bottom: 10px;
    }

    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 500;
    }

    .analysis-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
    }

    .tag {
        background: rgba(99, 102, 241, 0.1);
        color: #6366f1;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.65rem;
        font-weight: 500;
    }

    .card-actions {
        display: flex;
        gap: 15px;
        padding-top: 10px;
        border-top: 1px solid var(--glass-border);
    }

    .action-btn {
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        transition: all 0.3s ease;
    }

    .action-btn:hover {
        color: var(--primary);
        background: rgba(255, 255, 255, 0.05);
    }

    .action-btn.liked {
        color: #ef4444;
    }

    .profile-header {
        display: flex;
        gap: 15px;
        align-items: flex-start;
        margin-bottom: 20px;
    }

    .profile-avatar img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
    }

    .profile-info {
        flex: 1;
    }

    .profile-info h3 {
        margin: 0 0 4px 0;
        font-size: 1.1rem;
        color: var(--text-primary);
    }

    .profile-info p {
        margin: 0;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    .profile-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }

    .stat {
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }

    .stat-value {
        display: block;
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary);
    }

    .stat-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
    }

    .profile-tabs {
        display: flex;
        gap: 5px;
        margin-bottom: 15px;
    }

    .profile-tab {
        background: none;
        border: 1px solid var(--glass-border);
        color: var(--text-secondary);
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.75rem;
        transition: all 0.3s ease;
    }

    .profile-tab.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    /* Responsive */
    @media (max-width: 1200px) {
        .social-overlay {
            position: relative;
            width: 100%;
            right: 0;
            margin-bottom: 20px;
        }
    }
    </style>

    <script>
    // Social Features JavaScript
    class SocialFeatures {
        constructor() {
            this.currentTab = 'feed';
            this.currentUser = null;
            this.activityFeed = [];
            this.trendingData = {};
            
            this.initializeSocialFeatures();
        }
        
        initializeSocialFeatures() {
            // Initialize social navigation
            this.setupNavigation();
            
            // Load initial data
            this.loadActivityFeed();
            this.loadTrendingContent();
            this.loadUserProfile();
            
            // Setup event listeners
            this.setupEventListeners();
        }
        
        setupNavigation() {
            const navTabs = document.querySelectorAll('.nav-tab');
            navTabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const tabName = tab.dataset.tab;
                    this.switchTab(tabName);
                });
            });
        }
        
        switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.social-tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Update navigation
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
            
            this.currentTab = tabName;
            
            // Load tab-specific content
            this.loadTabContent(tabName);
        }
        
        loadTabContent(tabName) {
            switch(tabName) {
                case 'feed':
                    this.loadActivityFeed();
                    break;
                case 'discover':
                    this.loadTrendingContent();
                    break;
                case 'collaborate':
                    this.loadCollaborationSpaces();
                    break;
                case 'profile':
                    this.loadUserProfile();
                    break;
            }
        }
        
        loadActivityFeed() {
            // Simulate activity feed data
            const activities = [
                {
                    type: 'share',
                    user: 'Alice Johnson',
                    action: 'shared a positive analysis',
                    title: 'Customer Review Analysis',
                    time: '2 hours ago'
                },
                {
                    type: 'like',
                    user: 'Bob Smith',
                    action: 'liked your analysis',
                    title: 'Social Media Sentiment',
                    time: '4 hours ago'
                },
                {
                    type: 'follow',
                    user: 'Carol Davis',
                    action: 'started following you',
                    time: '1 day ago'
                }
            ];
            
            const feedContainer = document.getElementById('activityFeed');
            feedContainer.innerHTML = activities.map(activity => `
                <div class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-text">
                            <strong>${activity.user}</strong> ${activity.action}
                            ${activity.title ? `"${activity.title}"` : ''}
                        </div>
                        <div class="activity-time">${activity.time}</div>
                    </div>
                </div>
            `).join('');
        }
        
        getActivityIcon(type) {
            const icons = {
                share: 'share',
                like: 'heart',
                comment: 'comment',
                follow: 'user-plus'
            };
            return icons[type] || 'bell';
        }
        
        quickShare() {
            const title = document.getElementById('quickShareTitle').value;
            const content = document.getElementById('quickShareContent').value;
            const visibility = document.getElementById('shareVisibility').value;
            const tags = document.getElementById('shareTags').value;
            
            if (!title || !content) {
                alert('Please fill in both title and content');
                return;
            }
            
            // Simulate sharing
            console.log('Sharing analysis:', { title, content, visibility, tags });
            
            // Clear form
            document.getElementById('quickShareTitle').value = '';
            document.getElementById('quickShareContent').value = '';
            document.getElementById('shareTags').value = '';
            
            // Show success message
            this.showNotification('Analysis shared successfully!', 'success');
            
            // Refresh feed
            this.loadActivityFeed();
        }
        
        loadTrendingContent() {
            // Simulate trending data
            const trendingAnalyses = [
                {
                    title: 'AI Sentiment Analysis Breakthrough',
                    user: 'TechExpert',
                    likes: 42,
                    comments: 12
                },
                {
                    title: 'Customer Feedback Insights 2024',
                    user: 'DataScientist',
                    likes: 38,
                    comments: 8
                }
            ];
            
            const trendingTags = [
                { tag: 'AI', count: 156 },
                { tag: 'CustomerService', count: 98 },
                { tag: 'MachineLearning', count: 87 }
            ];
            
            this.renderTrendingContent('analyses', trendingAnalyses);
        }
        
        renderTrendingContent(type, data) {
            const container = document.getElementById('trendingContent');
            
            if (type === 'analyses') {
                container.innerHTML = data.map(analysis => `
                    <div class="trending-item">
                        <div class="trending-title">${analysis.title}</div>
                        <div class="trending-meta">
                            by @${analysis.user} • ${analysis.likes} likes • ${analysis.comments} comments
                        </div>
                    </div>
                `).join('');
            } else if (type === 'tags') {
                container.innerHTML = data.map(item => `
                    <div class="trending-tag">
                        <span class="tag-name">#${item.tag}</span>
                        <span class="tag-count">${item.count} uses</span>
                    </div>
                `).join('');
            }
        }
        
        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 350px;
                background: var(--glass-bg);
                border: 1px solid var(--glass-border);
                padding: 12px 16px;
                border-radius: 8px;
                color: var(--text-primary);
                z-index: 1000;
                animation: slideIn 0.3s ease;
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        setupEventListeners() {
            // Trending tabs
            document.querySelectorAll('.trending-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    const type = tab.dataset.type;
                    document.querySelectorAll('.trending-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    this.loadTrendingContentByType(type);
                });
            });
        }
        
        loadTrendingContentByType(type) {
            // Load different trending content based on type
            console.log('Loading trending content for:', type);
        }
    }
    
    // Initialize social features
    const socialFeatures = new SocialFeatures();
    
    // Global functions for HTML onclick handlers
    window.refreshFeed = () => socialFeatures.loadActivityFeed();
    window.quickShare = () => socialFeatures.quickShare();
    window.performSocialSearch = () => {
        const query = document.getElementById('socialSearch').value;
        console.log('Searching for:', query);
    };
    
    // Collaboration space functions
    window.openCreateSpaceModal = () => {
        document.getElementById('createSpaceModal').classList.remove('hidden');
    };
    
    window.closeCreateSpaceModal = () => {
        document.getElementById('createSpaceModal').classList.add('hidden');
    };
    
    window.createCollaborationSpace = () => {
        const name = document.getElementById('spaceName').value;
        const description = document.getElementById('spaceDescription').value;
        const privacy = document.getElementById('spacePrivacy').value;
        
        if (!name) {
            alert('Please enter a space name');
            return;
        }
        
        console.log('Creating collaboration space:', { name, description, privacy });
        closeCreateSpaceModal();
        socialFeatures.showNotification('Collaboration space created!', 'success');
    };
    </script>
    """

if __name__ == "__main__":
    print("🤝 Social Features Engine Initialized!")
    print("Features: Activity feeds, collaboration, sharing, social analytics")