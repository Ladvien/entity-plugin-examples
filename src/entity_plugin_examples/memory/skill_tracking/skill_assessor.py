"""Assess user skill levels from conversation patterns."""

from __future__ import annotations
import re
from typing import Dict, Any, List
from collections import defaultdict

from entity.plugins.base import Plugin
from entity.workflow.stages import REVIEW


class SkillAssessorPlugin(Plugin):
    """
    Assess user skill levels based on questions asked and problems solved.
    
    Tracks skill demonstrations and learning indicators over time.
    """
    
    supported_stages = [REVIEW]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Skill demonstration patterns
        self.skill_indicators = {
            "demonstrates": [
                r"i (built|created|developed|implemented|designed) (.+)",
                r"i (solved|fixed|debugged|optimized) (.+)", 
                r"i (know how to|can|am able to) (.+)",
                r"in my (project|work|experience), i (.+)",
            ],
            "learning": [
                r"i'm (learning|studying|trying to understand) (.+)",
                r"i want to (learn|master|understand) (.+)",
                r"how do i (.+)",
                r"can you (teach|show|explain) (.+)",
            ],
            "struggling": [
                r"i (can't|cannot|don't know how to) (.+)",
                r"i'm (stuck|confused|having trouble) (.+)",
                r"i don't understand (.+)",
                r"why (doesn't|isn't|won't) (.+)",
            ]
        }
    
    async def _execute_impl(self, context) -> str:
        """Assess skill level from user interaction."""
        message = (context.message or "").lower().strip()
        
        if not message:
            return context.message or ""
        
        # Get existing skill assessments
        skills = await context.recall("skill_assessments", {
            "demonstrated_skills": defaultdict(list),  # skill -> [evidence]
            "learning_goals": defaultdict(int),        # skill -> frequency
            "struggle_areas": defaultdict(list),       # skill -> [issues]
            "skill_levels": defaultdict(str),          # skill -> level
            "assessment_history": []                   # timestamped assessments
        })
        
        # Extract skills from message
        for category, patterns in self.skill_indicators.items():
            for pattern in patterns:
                matches = re.findall(pattern, message)
                
                for match in matches:
                    # Extract the skill/topic being referenced
                    skill_text = match[-1] if isinstance(match, tuple) else match
                    skill_text = skill_text.strip()
                    
                    # Clean up skill text
                    skill_text = re.sub(r'^(to|the|a|an|how|why)\\s+', '', skill_text)
                    skill_text = re.sub(r'\\s+(it|this|that)$', '', skill_text)
                    
                    if len(skill_text) > 3:  # Valid skill reference
                        skill_category = self._categorize_skill(skill_text)
                        
                        if category == "demonstrates":
                            skills["demonstrated_skills"][skill_category].append(skill_text)
                            # Update skill level based on demonstration
                            current_level = skills["skill_levels"].get(skill_category, "novice")
                            if current_level in ["novice", "learning"]:
                                skills["skill_levels"][skill_category] = "intermediate"
                            
                        elif category == "learning":
                            skills["learning_goals"][skill_category] += 1
                            if skills["skill_levels"].get(skill_category, "novice") == "novice":
                                skills["skill_levels"][skill_category] = "learning"
                            
                        elif category == "struggling":
                            skills["struggle_areas"][skill_category].append(skill_text)
                            # Don't downgrade if they've demonstrated competence
                            if skill_category not in skills["demonstrated_skills"]:
                                skills["skill_levels"][skill_category] = "novice"
        
        # Calculate overall competency score
        competency_score = 0
        total_skills = len(skills["skill_levels"])
        
        if total_skills > 0:
            level_weights = {"novice": 1, "learning": 2, "intermediate": 3, "advanced": 4}
            total_weighted = sum(level_weights.get(level, 1) for level in skills["skill_levels"].values())
            competency_score = round((total_weighted / (total_skills * 4)) * 100, 1)
        
        # Add assessment to history
        import time
        assessment = {
            "timestamp": time.time(),
            "skills_tracked": total_skills,
            "competency_score": competency_score,
            "top_skills": self._get_top_skills(skills["skill_levels"], 3)
        }
        skills["assessment_history"].append(assessment)
        
        # Keep only last 50 assessments
        if len(skills["assessment_history"]) > 50:
            skills["assessment_history"] = skills["assessment_history"][-50:]
        
        # Convert defaultdicts for storage
        skills_storage = {
            "demonstrated_skills": {k: list(set(v)) for k, v in skills["demonstrated_skills"].items()},
            "learning_goals": dict(skills["learning_goals"]),
            "struggle_areas": {k: list(set(v)) for k, v in skills["struggle_areas"].items()},
            "skill_levels": dict(skills["skill_levels"]),
            "assessment_history": skills["assessment_history"]
        }
        
        await context.remember("skill_assessments", skills_storage)
        await context.remember("current_competency_score", competency_score)
        
        return context.message or ""
    
    def _categorize_skill(self, skill_text: str) -> str:
        """Categorize skill into broad domains."""
        skill_lower = skill_text.lower()
        
        # Programming-related
        if any(word in skill_lower for word in ["code", "program", "python", "javascript", "api", "function", "debug"]):
            return "programming"
        # Data-related  
        elif any(word in skill_lower for word in ["data", "analysis", "statistics", "model", "dataset"]):
            return "data_science"
        # Design-related
        elif any(word in skill_lower for word in ["design", "ui", "ux", "interface", "visual"]):
            return "design"
        # Business-related
        elif any(word in skill_lower for word in ["business", "strategy", "marketing", "sales", "management"]):
            return "business"
        # Technical infrastructure
        elif any(word in skill_lower for word in ["server", "database", "cloud", "network", "security"]):
            return "infrastructure"
        else:
            return "general"
    
    def _get_top_skills(self, skill_levels: Dict[str, str], limit: int) -> List[str]:
        """Get top skills by level."""
        level_priority = {"advanced": 4, "intermediate": 3, "learning": 2, "novice": 1}
        sorted_skills = sorted(skill_levels.items(), 
                             key=lambda x: level_priority.get(x[1], 0), reverse=True)
        return [skill for skill, _ in sorted_skills[:limit]]


# Example: User says "I built a REST API in Python"
# Plugin records: programming -> demonstrated, level -> intermediate