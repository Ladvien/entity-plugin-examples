"""Learn user preferences from conversation patterns."""

from __future__ import annotations
import re
from typing import Dict, Any, List

from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE


class PreferenceLearnerPlugin(Plugin):
    """
    Learn user preferences from explicit statements and usage patterns.
    
    Detects preference indicators: "I prefer", "I like", "I don't like", etc.
    """
    
    supported_stages = [PARSE]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Preference detection patterns
        self.preference_patterns = [
            (r"i (prefer|like|love|enjoy) (.+)", "positive"),
            (r"i (don't like|hate|dislike|avoid) (.+)", "negative"), 
            (r"i (always|usually|often) (.+)", "behavioral"),
            (r"i (never|rarely|seldom) (.+)", "avoidance"),
            (r"my favorite (.+) is (.+)", "favorite"),
            (r"i'm (interested in|into) (.+)", "interest"),
        ]
    
    async def _execute_impl(self, context) -> str:
        """Extract and store user preferences."""
        message = (context.message or "").lower().strip()
        
        if not message:
            return context.message or ""
        
        # Get existing preferences
        preferences = await context.recall("user_preferences", {
            "positive": [],     # Things user likes
            "negative": [],     # Things user dislikes  
            "behavioral": [],   # User behavior patterns
            "avoidance": [],    # Things user avoids
            "favorites": {},    # User's favorite things
            "interests": [],    # Areas of interest
        })
        
        # Extract preferences from message
        for pattern, pref_type in self.preference_patterns:
            matches = re.findall(pattern, message)
            
            for match in matches:
                if pref_type == "favorite":
                    category, item = match
                    if "favorites" not in preferences:
                        preferences["favorites"] = {}
                    preferences["favorites"][category.strip()] = item.strip()
                else:
                    # Extract the preference item
                    if isinstance(match, tuple):
                        item = match[1].strip() if len(match) > 1 else match[0].strip()
                    else:
                        item = match.strip()
                    
                    # Clean up the item (remove common stop words)
                    item = re.sub(r'^(to|the|a|an|that|when|where|how)\\s+', '', item)
                    
                    if item and len(item) > 2:  # Valid preference
                        if pref_type not in preferences:
                            preferences[pref_type] = []
                        
                        # Avoid duplicates
                        if item not in preferences[pref_type]:
                            preferences[pref_type].append(item)
                            
                            # Limit list sizes to prevent memory bloat
                            if len(preferences[pref_type]) > 20:
                                preferences[pref_type] = preferences[pref_type][-20:]
        
        # Store updated preferences
        await context.remember("user_preferences", preferences)
        
        # Store preference count for analytics
        total_prefs = sum(len(v) if isinstance(v, list) else len(v) if isinstance(v, dict) else 0 
                         for v in preferences.values())
        await context.remember("total_learned_preferences", total_prefs)
        
        return context.message or ""


# Example usage:
# User: "I prefer short explanations and I don't like verbose responses"
# Plugin learns: positive=["short explanations"], negative=["verbose responses"]