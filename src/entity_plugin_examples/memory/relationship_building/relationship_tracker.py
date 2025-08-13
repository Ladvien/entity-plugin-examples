"""Track relationship dynamics and interaction quality over time."""

from __future__ import annotations
import time
import re
from typing import Dict, Any, List
from collections import defaultdict

from entity.plugins.base import Plugin
from entity.workflow.stages import REVIEW


class RelationshipTrackerPlugin(Plugin):
    """
    Track the evolution of user-agent relationship dynamics.
    
    Monitors trust, engagement, satisfaction, and interaction patterns.
    """
    
    supported_stages = [REVIEW]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Relationship quality indicators
        self.quality_indicators = {
            "positive_engagement": [
                r"thank you", r"thanks", r"appreciate", r"helpful", r"useful",
                r"great", r"awesome", r"perfect", r"exactly", r"love this"
            ],
            "negative_engagement": [
                r"not helpful", r"doesn't work", r"wrong", r"frustrated",
                r"confused", r"disappointed", r"not what i wanted"
            ],
            "trust_building": [
                r"i trust", r"reliable", r"consistent", r"dependable",
                r"you understand", r"you get it", r"you know me"
            ],
            "trust_erosion": [
                r"don't trust", r"unreliable", r"inconsistent", r"let me down",
                r"you don't understand", r"not helpful", r"waste of time"
            ],
            "personal_sharing": [
                r"personally", r"for me", r"in my case", r"my situation",
                r"i feel", r"i believe", r"my experience", r"to be honest"
            ],
            "dependency_signals": [
                r"always ask you", r"rely on you", r"depend on", r"my go-to",
                r"first thing i do", r"can't do without", r"need your help"
            ]
        }
        
        # Conversation flow patterns
        self.flow_patterns = {
            "smooth": [r"yes", r"exactly", r"right", r"correct", r"perfect"],
            "clarification": [r"what do you mean", r"can you explain", r"i don't understand"],
            "correction": [r"no", r"that's wrong", r"not right", r"incorrect"],
            "continuation": [r"also", r"and", r"furthermore", r"in addition", r"next"]
        }
    
    async def _execute_impl(self, context) -> str:
        """Track relationship dynamics from current interaction."""
        message = (context.message or "").lower().strip()
        
        if not message:
            return context.message or ""
        
        # Get current relationship metrics
        relationship_data = await context.recall("relationship_tracking", {
            "interaction_history": [],           # timestamped interactions with quality scores
            "relationship_metrics": {            # current relationship health metrics
                "trust_level": 50,               # 0-100 scale
                "engagement_quality": 50,        # 0-100 scale  
                "personal_connection": 0,        # 0-100 scale
                "dependency_level": 0,           # 0-100 scale
                "satisfaction_trend": []         # last 10 interaction scores
            },
            "communication_patterns": {          # how user typically interacts
                "avg_message_length": 0,
                "formality_level": 50,
                "question_frequency": 0,
                "sharing_frequency": 0
            },
            "relationship_milestones": []       # significant relationship events
        })
        
        current_time = time.time()
        
        # Analyze current interaction quality
        interaction_scores = self._analyze_interaction(message)
        
        # Update relationship metrics based on this interaction
        metrics = relationship_data["relationship_metrics"]
        
        # Trust level adjustments
        trust_change = interaction_scores.get("trust_building", 0) - interaction_scores.get("trust_erosion", 0)
        metrics["trust_level"] = max(0, min(100, metrics["trust_level"] + trust_change * 5))
        
        # Engagement quality adjustments  
        engagement_change = interaction_scores.get("positive_engagement", 0) - interaction_scores.get("negative_engagement", 0)
        metrics["engagement_quality"] = max(0, min(100, metrics["engagement_quality"] + engagement_change * 3))
        
        # Personal connection growth
        personal_signals = interaction_scores.get("personal_sharing", 0)
        if personal_signals > 0:
            metrics["personal_connection"] = min(100, metrics["personal_connection"] + personal_signals * 2)
        
        # Dependency level tracking
        dependency_signals = interaction_scores.get("dependency_signals", 0)
        if dependency_signals > 0:
            metrics["dependency_level"] = min(100, metrics["dependency_level"] + dependency_signals * 3)
        
        # Track satisfaction trend
        overall_interaction_score = sum(interaction_scores.values()) / max(len(interaction_scores), 1)
        satisfaction_score = max(0, min(100, 50 + (overall_interaction_score * 10)))
        
        metrics["satisfaction_trend"].append(satisfaction_score)
        if len(metrics["satisfaction_trend"]) > 10:
            metrics["satisfaction_trend"] = metrics["satisfaction_trend"][-10:]
        
        # Update communication patterns
        patterns = relationship_data["communication_patterns"]
        patterns["avg_message_length"] = self._update_average(
            patterns["avg_message_length"], len(context.message or ""), 0.1
        )
        
        # Check for relationship milestones
        milestones = self._check_milestones(relationship_data["relationship_metrics"], 
                                          relationship_data["relationship_milestones"])
        relationship_data["relationship_milestones"].extend(milestones)
        
        # Record this interaction
        interaction_record = {
            "timestamp": current_time,
            "message_length": len(context.message or ""),
            "quality_scores": interaction_scores,
            "satisfaction_score": satisfaction_score,
            "relationship_state": {
                "trust": metrics["trust_level"],
                "engagement": metrics["engagement_quality"],
                "connection": metrics["personal_connection"]
            }
        }
        relationship_data["interaction_history"].append(interaction_record)
        
        # Keep only last 100 interactions
        if len(relationship_data["interaction_history"]) > 100:
            relationship_data["interaction_history"] = relationship_data["interaction_history"][-100:]
        
        # Store updated relationship data
        await context.remember("relationship_tracking", relationship_data)
        
        # Store current relationship health score
        health_score = (metrics["trust_level"] + metrics["engagement_quality"] + 
                       metrics["personal_connection"]) / 3
        await context.remember("relationship_health_score", round(health_score, 1))
        
        return context.message or ""
    
    def _analyze_interaction(self, message: str) -> Dict[str, int]:
        """Analyze message for relationship quality indicators."""
        scores = defaultdict(int)
        
        # Check for quality indicators
        for category, patterns in self.quality_indicators.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, message))
                scores[category] += matches
        
        # Analyze conversation flow
        for flow_type, patterns in self.flow_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    scores[f"flow_{flow_type}"] += 1
        
        return dict(scores)
    
    def _update_average(self, current_avg: float, new_value: float, weight: float) -> float:
        """Update running average with exponential smoothing."""
        if current_avg == 0:
            return new_value
        return current_avg * (1 - weight) + new_value * weight
    
    def _check_milestones(self, metrics: Dict[str, Any], existing_milestones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for relationship milestones."""
        milestones = []
        current_time = time.time()
        
        # Check for milestone thresholds
        milestone_thresholds = {
            "first_trust": (metrics["trust_level"], 70, "High trust established"),
            "deep_connection": (metrics["personal_connection"], 60, "Personal connection formed"),
            "high_engagement": (metrics["engagement_quality"], 80, "Highly engaged relationship"),
            "strong_dependency": (metrics["dependency_level"], 70, "Strong dependency developed")
        }
        
        for milestone_type, (current_value, threshold, description) in milestone_thresholds.items():
            # Check if this milestone hasn't been reached before
            if current_value >= threshold:
                if not any(m.get("type") == milestone_type for m in existing_milestones):
                    milestones.append({
                        "type": milestone_type,
                        "timestamp": current_time,
                        "description": description,
                        "metric_value": current_value
                    })
        
        # Check for satisfaction trends
        satisfaction_trend = metrics.get("satisfaction_trend", [])
        if len(satisfaction_trend) >= 5:
            recent_avg = sum(satisfaction_trend[-5:]) / 5
            if recent_avg > 85 and not any(m.get("type") == "consistent_satisfaction" for m in existing_milestones):
                milestones.append({
                    "type": "consistent_satisfaction",
                    "timestamp": current_time,
                    "description": "Consistently high satisfaction",
                    "metric_value": recent_avg
                })
        
        return milestones


# Example: Tracks when user says "I really trust your advice" -> increases trust_level
# Detects "Thank you, that was exactly what I needed" -> positive engagement
# Monitors overall relationship health over time