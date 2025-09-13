"""
🎯 HABIT FORMATION ENGINE (Minimal viable)
- Daily goals checklist
- Streak tracking per goal
- Lightweight persistence via analytics_cache (EnhancedDatabaseManager)
- UI generator for overlay panel
"""

from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import List, Dict, Optional

DEFAULT_GOALS = [
    { 'id': 'read_news', 'title': 'Read 5 news items', 'target': 5, 'icon': 'fa-newspaper' },
    { 'id': 'analyze_text', 'title': 'Analyze 3 texts', 'target': 3, 'icon': 'fa-brain' },
    { 'id': 'share_insight', 'title': 'Share 1 insight', 'target': 1, 'icon': 'fa-share-alt' },
]


def _today_str() -> str:
    return date.today().isoformat()


class HabitEngine:
    """Logic layer for habit goals and streaks (stateless; callers persist state)"""

    def get_default_goals(self) -> List[Dict]:
        return DEFAULT_GOALS

    def ensure_state(self, state: Optional[Dict]) -> Dict:
        # Structure:
        # {
        #   'goals': { goal_id: { 'progress': int, 'completed_dates': [yyyy-mm-dd], 'streak': int, 'last_completed': yyyy-mm-dd|null } },
        #   'last_reset': yyyy-mm-dd
        # }
        if not state:
            state = { 'goals': {}, 'last_reset': _today_str() }
        # Initialize missing goals
        for g in DEFAULT_GOALS:
            gid = g['id']
            if gid not in state['goals']:
                state['goals'][gid] = { 'progress': 0, 'completed_dates': [], 'streak': 0, 'last_completed': None }
        return state

    def reset_daily_if_needed(self, state: Dict) -> Dict:
        today = _today_str()
        if state.get('last_reset') != today:
            # New day; reset daily progress but keep streaks
            for gid in state.get('goals', {}):
                state['goals'][gid]['progress'] = 0
            state['last_reset'] = today
        return state

    def update_progress(self, state: Dict, goal_id: str, delta: int, target: int) -> Dict:
        state = self.ensure_state(state)
        state = self.reset_daily_if_needed(state)
        goal = state['goals'].get(goal_id)
        if not goal:
            state['goals'][goal_id] = { 'progress': 0, 'completed_dates': [], 'streak': 0, 'last_completed': None }
            goal = state['goals'][goal_id]
        goal['progress'] = max(0, min(target, goal['progress'] + delta))
        return state

    def complete_goal_today(self, state: Dict, goal_id: str) -> Dict:
        state = self.ensure_state(state)
        state = self.reset_daily_if_needed(state)
        goal = state['goals'][goal_id]
        today = _today_str()
        if today not in goal['completed_dates']:
            goal['completed_dates'].append(today)
        # Update streak if completed today and yesterday was completed
        prev_date = (date.today().fromordinal(date.today().toordinal() - 1)).isoformat()
        if goal['last_completed'] == prev_date:
            goal['streak'] = goal.get('streak', 0) + 1
        elif goal['last_completed'] != today:
            # If last completed long ago (or never), start streak at 1
            goal['streak'] = 1
        goal['last_completed'] = today
        return state

    def get_summary(self, state: Dict) -> Dict:
        state = self.ensure_state(state)
        state = self.reset_daily_if_needed(state)
        # Build summary metrics
        totals = { 'daily_completed': 0, 'daily_total': len(DEFAULT_GOALS), 'longest_streak': 0 }
        for g in DEFAULT_GOALS:
            sd = state['goals'].get(g['id'], {})
            if sd.get('last_completed') == _today_str():
                totals['daily_completed'] += 1
            totals['longest_streak'] = max(totals['longest_streak'], sd.get('streak', 0))
        return {
            'goals': DEFAULT_GOALS,
            'state': state.get('goals', {}),
            'summary': totals,
            'last_reset': state.get('last_reset')
        }


def generate_habits_ui() -> str:
    """Return HTML+CSS+JS overlay for Habit Formation panel"""
    return """
    <!-- Habit Formation UI -->
    <div class="habit-overlay" id="habitOverlay">
      <div class="habit-panel glass-card">
        <div class="habit-header">
          <h4><i class="fas fa-fire" style="color:#ef4444"></i> Daily Habits</h4>
          <div class="habit-stats">
            <span id="habitProgress">0/3</span>
            <span id="habitLongestStreak" title="Longest streak">🔥 0</span>
            <button class="habit-refresh" onclick="window.habitsEngine && window.habitsEngine.loadHabits()">
              <i class="fas fa-sync-alt"></i>
            </button>
          </div>
        </div>
        <div class="habit-goals" id="habitGoals"></div>
      </div>
    </div>

    <style>
      .habit-overlay{ position:fixed; bottom:340px; right:20px; z-index:935; width:320px; }
      .habit-panel{ background:linear-gradient(135deg, rgba(239,68,68,0.08), rgba(234,88,12,0.08)); border:1px solid rgba(239,68,68,0.25); padding:14px; border-radius:12px; }
      .habit-header{ display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
      .habit-header h4{ margin:0; font-size:1rem; display:flex; align-items:center; gap:8px; color:var(--text-primary); }
      .habit-stats{ display:flex; align-items:center; gap:10px; color:var(--text-secondary); font-size:0.85rem; }
      .habit-refresh{ background:none; border:1px solid var(--glass-border); color:var(--text-secondary); padding:4px 8px; border-radius:6px; cursor:pointer; }
      .habit-goals{ display:flex; flex-direction:column; gap:8px; max-height:200px; overflow-y:auto; }
      .habit-goal{ background:rgba(255,255,255,0.04); border:1px solid var(--glass-border); border-radius:8px; padding:10px; display:flex; align-items:center; justify-content:space-between; }
      .habit-left{ display:flex; align-items:center; gap:10px; }
      .habit-title{ font-size:0.9rem; color:var(--text-primary); }
      .habit-actions button{ background:linear-gradient(45deg, var(--primary), var(--secondary)); color:#fff; border:none; padding:6px 10px; border-radius:6px; cursor:pointer; font-size:0.8rem; }
      .habit-progress{ font-size:0.8rem; color:var(--text-secondary); }
    </style>

    <script>
      class HabitsEngine {
        constructor(){ this.endpointBase = '/api/habits'; this.loadHabits(); }
        async loadHabits(){
          try{
            const res = await fetch(`${this.endpointBase}/list`);
            const payload = await res.json();
            if(!payload || payload.error){ return; }
            this.render(payload);
          }catch(e){ console.error('Load habits failed', e); }
        }
        render(data){
          const goalsWrap = document.getElementById('habitGoals');
          if(!goalsWrap) return;
          const goals = data.goals || [];
          const state = data.state || {};
          goalsWrap.innerHTML = goals.map(g=>{
            const s = state[g.id] || { progress:0, streak:0, last_completed:null };
            const completedToday = s.last_completed && s.last_completed.startsWith(new Date().toISOString().slice(0,10));
            return `
              <div class="habit-goal">
                <div class="habit-left">
                  <i class="fas ${g.icon}" style="color:#f59e0b"></i>
                  <div>
                    <div class="habit-title">${g.title}</div>
                    <div class="habit-progress">${s.progress || 0} / ${g.target} • 🔥 ${s.streak || 0}</div>
                  </div>
                </div>
                <div class="habit-actions">
                  ${completedToday ? '<span style="color:#10b981;font-weight:600">Done</span>' : `<button onclick="window.habitsEngine && window.habitsEngine.complete('${g.id}')">Complete</button>`}
                </div>
              </div>
            `;
          }).join('');
          // Header stats
          const prog = document.getElementById('habitProgress');
          const longest = document.getElementById('habitLongestStreak');
          const dailyCompleted = (data.summary && data.summary.daily_completed) || 0;
          const dailyTotal = (data.summary && data.summary.daily_total) || goals.length;
          const longestStreak = (data.summary && data.summary.longest_streak) || 0;
          if(prog) prog.textContent = `${dailyCompleted}/${dailyTotal}`;
          if(longest) longest.textContent = `🔥 ${longestStreak}`;
        }
        async complete(goalId){
          try{
            const res = await fetch(`${this.endpointBase}/complete`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ goal_id: goalId }) });
            const payload = await res.json();
            if(!payload || payload.error){ return; }
            this.render(payload);
          }catch(e){ console.error('Complete habit failed', e); }
        }
      }
      window.habitsEngine = new HabitsEngine();
    </script>
    """

if __name__ == '__main__':
    print('🎯 Habit Formation Engine ready')
