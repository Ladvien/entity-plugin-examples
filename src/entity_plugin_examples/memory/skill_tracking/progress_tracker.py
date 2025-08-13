"""Track learning progress and skill development over time."""

from __future__ import annotations
import time
from typing import Dict, Any, List

from entity.plugins.base import Plugin
from entity.workflow.stages import THINK


class ProgressTrackerPlugin(Plugin):
    """
    Track user's learning progress and skill development journey.
    
    Monitors progression through different skill levels over time.
    """
    
    supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        """Track progress indicators and learning milestones.""" 
        message = context.message or ""
        
        # Get current skill assessments
        skill_data = await context.recall("skill_assessments", {})
        progress_data = await context.recall("progress_tracking", {
            "skill_progressions": {},      # skill -> [{"level": str, "timestamp": float}]
            "learning_milestones": [],     # [{"milestone": str, "skill": str, "timestamp": float}]
            "session_progress": {},        # session tracking
            "progress_metrics": {}         # calculated metrics
        })
        
        current_time = time.time()
        current_skills = skill_data.get("skill_levels", {})
        
        # Track skill level progressions
        for skill, current_level in current_skills.items():
            if skill not in progress_data["skill_progressions"]:
                progress_data["skill_progressions"][skill] = []
            
            # Check if level has changed
            progression_history = progress_data["skill_progressions"][skill]
            last_level = progression_history[-1]["level"] if progression_history else None
            
            if current_level != last_level:
                # Record progression
                progress_entry = {
                    "level": current_level,
                    "timestamp": current_time,
                    "previous_level": last_level
                }
                progress_data["skill_progressions"][skill].append(progress_entry)
                
                # Record milestone if it's an advancement
                if self._is_advancement(last_level, current_level):
                    milestone = {
                        "milestone": f"Advanced from {last_level or 'unknown'} to {current_level}",
                        "skill": skill,
                        "timestamp": current_time,
                        "type": "skill_advancement"
                    }
                    progress_data["learning_milestones"].append(milestone)
        
        # Track session-level progress
        session_key = f"session_{int(current_time // 3600)}"  # Hour-based sessions
        if session_key not in progress_data["session_progress"]:
            progress_data["session_progress"][session_key] = {
                "start_time": current_time,
                "skills_discussed": set(),
                "questions_asked": 0,
                "problems_solved": 0,
                "topics_explored": set()
            }
        
        session = progress_data["session_progress"][session_key]
        session["skills_discussed"].update(current_skills.keys())
        
        # Detect questions and problem-solving in current message
        message_lower = (message or "").lower()
        if any(indicator in message_lower for indicator in ["how", "what", "why", "can you", "?"]):
            session["questions_asked"] += 1
            
        if any(indicator in message_lower for indicator in ["solved", "fixed", "figured out", "got it working"]):
            session["problems_solved"] += 1
        
        # Calculate progress metrics
        progress_data["progress_metrics"] = self._calculate_progress_metrics(
            progress_data, current_skills, current_time
        )
        
        # Clean up old session data (keep last 7 days)
        week_ago = current_time - (7 * 24 * 3600)
        progress_data["session_progress"] = {
            k: v for k, v in progress_data["session_progress"].items()
            if v.get("start_time", 0) > week_ago
        }
        
        # Convert sets to lists for storage
        for session_data in progress_data["session_progress"].values():
            if isinstance(session_data.get("skills_discussed"), set):
                session_data["skills_discussed"] = list(session_data["skills_discussed"])
            if isinstance(session_data.get("topics_explored"), set):
                session_data["topics_explored"] = list(session_data["topics_explored"])
        
        await context.remember("progress_tracking", progress_data)
        
        return message
    
    def _is_advancement(self, old_level: str, new_level: str) -> bool:
        """Check if the level change represents advancement."""
        level_order = ["novice", "learning", "intermediate", "advanced"]
        
        if not old_level or not new_level:
            return False
            
        try:
            old_idx = level_order.index(old_level)
            new_idx = level_order.index(new_level)
            return new_idx > old_idx
        except ValueError:
            return False
    
    def _calculate_progress_metrics(self, progress_data: Dict[str, Any], 
                                   current_skills: Dict[str, str], 
                                   current_time: float) -> Dict[str, Any]:
        """Calculate various progress metrics."""
        metrics = {}
        
        # Skills growth rate (new skills per week)
        week_ago = current_time - (7 * 24 * 3600)
        recent_progressions = []
        
        for skill, progressions in progress_data.get("skill_progressions", {}).items():
            recent = [p for p in progressions if p["timestamp"] > week_ago]
            recent_progressions.extend(recent)
        
        metrics["weekly_skill_growth"] = len(recent_progressions)
        
        # Learning velocity (questions to problem-solving ratio)
        total_questions = sum(
            session.get("questions_asked", 0) 
            for session in progress_data.get("session_progress", {}).values()
        )
        total_solutions = sum(
            session.get("problems_solved", 0)
            for session in progress_data.get("session_progress", {}).values() 
        )
        
        if total_questions > 0:
            metrics["solution_rate"] = round(total_solutions / total_questions, 2)
        else:
            metrics["solution_rate"] = 0.0
        
        # Skill distribution
        level_counts = {}
        for level in current_skills.values():
            level_counts[level] = level_counts.get(level, 0) + 1
        
        metrics["skill_distribution"] = level_counts
        
        # Progress momentum (recent advancement frequency)
        recent_milestones = [
            m for m in progress_data.get("learning_milestones", [])
            if m.get("timestamp", 0) > week_ago
        ]
        metrics["recent_milestones"] = len(recent_milestones)
        
        return metrics


# Example: Tracks when user progresses from "novice" -> "learning" -> "intermediate"
# Records milestones and calculates learning velocity metrics