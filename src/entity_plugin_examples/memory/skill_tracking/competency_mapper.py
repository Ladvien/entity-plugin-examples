"""Map user competencies and suggest learning paths."""

from __future__ import annotations
import time
from typing import Dict, Any, List, Tuple

from entity.plugins.base import Plugin
from entity.workflow.stages import OUTPUT


class CompetencyMapperPlugin(Plugin):
    """
    Map user competencies and suggest personalized learning paths.
    
    Analyzes skill gaps and recommends next learning steps.
    """
    
    supported_stages = [OUTPUT]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Define skill progression paths
        self.skill_paths = {
            "programming": {
                "novice": ["basic syntax", "variables and data types", "simple functions"],
                "learning": ["control structures", "data structures", "error handling"],
                "intermediate": ["object-oriented programming", "APIs", "testing"],
                "advanced": ["design patterns", "performance optimization", "architecture"]
            },
            "data_science": {
                "novice": ["data types", "basic statistics", "data visualization"],
                "learning": ["data cleaning", "exploratory analysis", "basic modeling"],
                "intermediate": ["machine learning algorithms", "feature engineering", "model evaluation"],
                "advanced": ["deep learning", "MLOps", "advanced statistics"]
            },
            "design": {
                "novice": ["design principles", "color theory", "typography"],
                "learning": ["user research", "wireframing", "prototyping"],
                "intermediate": ["interaction design", "design systems", "usability testing"],
                "advanced": ["design leadership", "strategic design", "design ops"]
            }
        }
    
    async def _execute_impl(self, context) -> str:
        """Generate competency map and learning suggestions."""
        message = context.message or ""
        
        # Only add competency mapping if user is asking for guidance
        message_lower = message.lower()
        guidance_indicators = [
            "what should i learn", "next steps", "how to improve", "learning path",
            "where to go from here", "what's next", "how to get better"
        ]
        
        if not any(indicator in message_lower for indicator in guidance_indicators):
            return message  # Don't add unsolicited advice
        
        # Get user's current skills and progress
        skill_data = await context.recall("skill_assessments", {})
        progress_data = await context.recall("progress_tracking", {})
        
        current_skills = skill_data.get("skill_levels", {})
        struggle_areas = skill_data.get("struggle_areas", {})
        
        if not current_skills:
            return message  # No skill data to work with
        
        # Generate competency map
        competency_map = self._generate_competency_map(current_skills, struggle_areas)
        learning_suggestions = self._generate_learning_suggestions(
            current_skills, struggle_areas, progress_data
        )
        
        # Create enhanced response with competency insights
        if competency_map or learning_suggestions:
            enhanced_response = message + "\\n\\n" + self._format_competency_response(
                competency_map, learning_suggestions
            )
            
            # Store competency analysis
            await context.remember("last_competency_analysis", {
                "timestamp": time.time(),
                "skills_analyzed": len(current_skills),
                "suggestions_provided": len(learning_suggestions)
            })
            
            return enhanced_response
        
        return message
    
    def _generate_competency_map(self, current_skills: Dict[str, str], 
                                struggle_areas: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate a visual competency map."""
        competency_map = {}
        
        for skill_area, level in current_skills.items():
            if skill_area in self.skill_paths:
                competency_map[skill_area] = {
                    "current_level": level,
                    "strengths": self._identify_strengths(skill_area, level),
                    "gaps": self._identify_gaps(skill_area, level, struggle_areas.get(skill_area, [])),
                    "next_level": self._get_next_level(level)
                }
        
        return competency_map
    
    def _generate_learning_suggestions(self, current_skills: Dict[str, str],
                                     struggle_areas: Dict[str, List[str]],
                                     progress_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate personalized learning suggestions."""
        suggestions = []
        
        # Prioritize struggle areas
        for skill_area, struggles in struggle_areas.items():
            if struggles and skill_area in self.skill_paths:
                current_level = current_skills.get(skill_area, "novice")
                suggestions.append({
                    "type": "gap_filling",
                    "skill_area": skill_area,
                    "priority": "high",
                    "suggestion": f"Focus on resolving challenges with: {', '.join(struggles[:2])}",
                    "resources": self._get_level_resources(skill_area, current_level)
                })
        
        # Suggest next-level advancement
        for skill_area, current_level in current_skills.items():
            if skill_area in self.skill_paths:
                next_level = self._get_next_level(current_level)
                if next_level:
                    next_topics = self.skill_paths[skill_area].get(next_level, [])
                    if next_topics:
                        suggestions.append({
                            "type": "advancement",
                            "skill_area": skill_area,
                            "priority": "medium",
                            "suggestion": f"Ready to advance to {next_level}: {', '.join(next_topics[:2])}",
                            "resources": self._get_level_resources(skill_area, next_level)
                        })
        
        # Sort by priority and limit
        priority_order = {"high": 3, "medium": 2, "low": 1}
        suggestions.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)
        
        return suggestions[:3]  # Top 3 suggestions
    
    def _identify_strengths(self, skill_area: str, level: str) -> List[str]:
        """Identify strengths based on current level."""
        if skill_area not in self.skill_paths:
            return []
        
        level_order = ["novice", "learning", "intermediate", "advanced"]
        try:
            level_idx = level_order.index(level)
            strengths = []
            for i in range(level_idx + 1):
                if level_order[i] in self.skill_paths[skill_area]:
                    strengths.extend(self.skill_paths[skill_area][level_order[i]])
            return strengths
        except ValueError:
            return []
    
    def _identify_gaps(self, skill_area: str, level: str, 
                      struggles: List[str]) -> List[str]:
        """Identify skill gaps based on struggles and level."""
        if skill_area not in self.skill_paths:
            return struggles
        
        # Combine struggles with missing skills from current level
        gaps = list(struggles)
        
        if level in self.skill_paths[skill_area]:
            expected_skills = self.skill_paths[skill_area][level]
            # Add expected skills that might be missing (simplified heuristic)
            gaps.extend([skill for skill in expected_skills if not any(
                word in ' '.join(struggles).lower() for word in skill.lower().split()
            )])
        
        return list(set(gaps))  # Remove duplicates
    
    def _get_next_level(self, current_level: str) -> str:
        """Get the next skill level."""
        level_progression = {
            "novice": "learning",
            "learning": "intermediate", 
            "intermediate": "advanced",
            "advanced": None
        }
        return level_progression.get(current_level)
    
    def _get_level_resources(self, skill_area: str, level: str) -> List[str]:
        """Get learning resources for skill area and level."""
        # Simplified resource suggestions
        resource_map = {
            "programming": ["practice coding", "build projects", "read documentation"],
            "data_science": ["work with datasets", "take online courses", "join communities"],
            "design": ["create portfolios", "study examples", "get feedback"]
        }
        return resource_map.get(skill_area, ["practice regularly", "seek mentorship", "join communities"])
    
    def _format_competency_response(self, competency_map: Dict[str, Any], 
                                   suggestions: List[Dict[str, str]]) -> str:
        """Format competency analysis into readable text."""
        response_parts = []
        
        if competency_map:
            response_parts.append("📊 **Your Current Competency Map:**")
            for skill_area, data in competency_map.items():
                response_parts.append(f"• **{skill_area.title()}**: {data['current_level'].title()} level")
        
        if suggestions:
            response_parts.append("\\n🎯 **Personalized Learning Suggestions:**")
            for i, suggestion in enumerate(suggestions, 1):
                priority_emoji = {"high": "🔥", "medium": "⭐", "low": "💡"}
                emoji = priority_emoji.get(suggestion["priority"], "•")
                response_parts.append(f"{emoji} {suggestion['suggestion']}")
        
        return "\\n".join(response_parts)


# Example: User asks "What should I learn next?"
# Plugin analyzes skills and suggests personalized learning path