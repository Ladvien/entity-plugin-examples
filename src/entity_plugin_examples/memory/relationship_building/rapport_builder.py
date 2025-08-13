"""Build rapport through personal details and shared experiences."""

from __future__ import annotations
import re
import time
from typing import Dict, Any, List

from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE


class RapportBuilderPlugin(Plugin):
    """
    Build rapport by remembering and referencing personal details.
    
    Captures personal information to create more personalized interactions.
    """
    
    supported_stages = [PARSE]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Personal detail extraction patterns
        self.personal_patterns = [
            (r"my name is (\\w+)", "name"),
            (r"i'm (\\w+)", "name_casual"),
            (r"call me (\\w+)", "nickname"),
            (r"i work (at|for|as) (.+)", "work"),
            (r"i'm a (.+)", "role"),
            (r"i live in (.+)", "location"),
            (r"i'm from (.+)", "origin"),
            (r"i have (.+) (kids|children|cats|dogs)", "family"),
            (r"my (\\w+) is (.+)", "relationship"),
            (r"i (love|enjoy|like) (.+)", "interest"),
            (r"i'm working on (.+)", "project"),
            (r"i studied (.+)", "education"),
            (r"i went to (.+) (university|college|school)", "school"),
        ]
    
    async def _execute_impl(self, context) -> str:
        """Extract and remember personal details for rapport building."""
        message = (context.message or "").lower().strip()
        
        if not message:
            return context.message or ""
        
        # Get existing personal profile
        personal_profile = await context.recall("personal_profile", {
            "basic_info": {},           # name, location, role, etc.
            "relationships": {},        # family, friends, pets
            "interests": [],           # hobbies, likes
            "professional": {},        # work, education, projects
            "personal_history": [],    # timestamped personal shares
            "rapport_level": 0         # calculated rapport score
        })
        
        # Extract personal details
        details_found = []
        
        for pattern, detail_type in self.personal_patterns:
            matches = re.findall(pattern, message)
            
            for match in matches:
                if isinstance(match, tuple):
                    detail_value = match[-1].strip() if len(match) > 1 else match[0].strip()
                else:
                    detail_value = match.strip()
                
                # Store detail in appropriate category
                if detail_type in ["name", "name_casual", "nickname"]:
                    personal_profile["basic_info"]["name"] = detail_value
                    details_found.append(f"name: {detail_value}")
                    
                elif detail_type in ["location", "origin"]:
                    personal_profile["basic_info"][detail_type] = detail_value
                    details_found.append(f"{detail_type}: {detail_value}")
                    
                elif detail_type in ["work", "role"]:
                    personal_profile["professional"][detail_type] = detail_value
                    details_found.append(f"{detail_type}: {detail_value}")
                    
                elif detail_type in ["family", "relationship"]:
                    if "family" not in personal_profile["relationships"]:
                        personal_profile["relationships"]["family"] = []
                    personal_profile["relationships"]["family"].append(detail_value)
                    details_found.append(f"family: {detail_value}")
                    
                elif detail_type == "interest":
                    if detail_value not in personal_profile["interests"]:
                        personal_profile["interests"].append(detail_value)
                    details_found.append(f"interest: {detail_value}")
                    
                elif detail_type in ["project", "education", "school"]:
                    personal_profile["professional"][detail_type] = detail_value
                    details_found.append(f"{detail_type}: {detail_value}")
        
        # Record personal sharing event
        if details_found:
            sharing_event = {
                "timestamp": time.time(),
                "details_shared": details_found,
                "context_message": context.message,
                "rapport_impact": len(details_found)
            }
            personal_profile["personal_history"].append(sharing_event)
            
            # Keep only last 50 sharing events
            if len(personal_profile["personal_history"]) > 50:
                personal_profile["personal_history"] = personal_profile["personal_history"][-50:]
        
        # Calculate rapport level (0-100)
        rapport_factors = {
            "name_known": 15 if personal_profile["basic_info"].get("name") else 0,
            "location_known": 10 if personal_profile["basic_info"].get("location") else 0,
            "work_known": 10 if personal_profile["professional"].get("work") else 0,
            "interests_known": min(20, len(personal_profile["interests"]) * 5),
            "family_known": 10 if personal_profile["relationships"].get("family") else 0,
            "sharing_frequency": min(25, len(personal_profile["personal_history"]) * 2),
            "recent_sharing": 10 if self._has_recent_sharing(personal_profile["personal_history"]) else 0
        }
        
        rapport_level = sum(rapport_factors.values())
        personal_profile["rapport_level"] = min(100, rapport_level)
        
        # Store updated profile
        await context.remember("personal_profile", personal_profile)
        
        # Store rapport metrics
        await context.remember("current_rapport_level", rapport_level)
        await context.remember("total_personal_details", 
            len(personal_profile["basic_info"]) + 
            len(personal_profile["professional"]) + 
            len(personal_profile["interests"]) +
            len(personal_profile["relationships"])
        )
        
        return context.message or ""
    
    def _has_recent_sharing(self, history: List[Dict[str, Any]]) -> bool:
        """Check if user has shared personal details recently."""
        if not history:
            return False
        
        recent_threshold = time.time() - (24 * 3600)  # Last 24 hours
        return any(event.get("timestamp", 0) > recent_threshold for event in history)


# Example: User says "My name is Sarah and I work at Google"
# Plugin extracts: name="Sarah", work="Google", increases rapport level