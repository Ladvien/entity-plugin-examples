"""Adapt response style based on learned user preferences."""

from __future__ import annotations
import re
from typing import Dict, Any

from entity.plugins.prompt import PromptPlugin
from entity.workflow.stages import OUTPUT


class StyleAdapterPlugin(PromptPlugin):
    """
    Adapt response style based on user preferences.
    
    Modifies agent responses to match user's preferred communication style.
    """
    
    supported_stages = [OUTPUT]
    
    async def _execute_impl(self, context) -> str:
        """Adapt response style to user preferences."""
        message = context.message or ""
        
        # Get learned preferences
        preferences = await context.recall("user_preferences", {})
        
        if not preferences or not message:
            return message
            
        # Build style adaptation prompt
        adaptations = []
        
        # Check for communication style preferences
        positive_prefs = preferences.get("positive", [])
        negative_prefs = preferences.get("negative", [])
        
        style_keywords = [
            "short", "brief", "concise", "detailed", "verbose", "simple", 
            "technical", "casual", "formal", "examples", "explanations"
        ]
        
        for pref in positive_prefs:
            if any(keyword in pref.lower() for keyword in style_keywords):
                adaptations.append(f"User prefers: {pref}")
                
        for pref in negative_prefs:
            if any(keyword in pref.lower() for keyword in style_keywords):
                adaptations.append(f"User dislikes: {pref}")
        
        # If no style preferences learned, return original message
        if not adaptations:
            return message
        
        # Use LLM to adapt the style
        llm = context.get_resource("llm")
        
        if llm:
            style_prompt = f"""Adapt this response to match the user's preferences:

Original response: {message}

User preferences:
{chr(10).join(adaptations)}

Adapted response (keep the same meaning but adjust the style):"""
            
            try:
                adapted_response = await llm.generate(style_prompt)
                
                # Store adaptation metadata
                await context.remember("last_style_adaptation", {
                    "original_length": len(message),
                    "adapted_length": len(adapted_response),
                    "preferences_applied": len(adaptations)
                })
                
                return adapted_response.strip()
                
            except Exception:
                # Fallback to original message if adaptation fails
                return message
        else:
            # Simple text-based adaptation without LLM
            adapted = message
            
            # Apply simple rules based on preferences
            for pref in positive_prefs:
                if "short" in pref.lower() or "brief" in pref.lower():
                    # Attempt to shorten by removing redundant phrases
                    adapted = re.sub(r'\\b(basically|essentially|obviously)\\s+', '', adapted)
                    adapted = re.sub(r'\\s+(and|also)\\s+', ' ', adapted)
                    
                elif "detailed" in pref.lower() or "verbose" in pref.lower():
                    # Add clarifying phrases
                    if not adapted.endswith('.'):
                        adapted += "."
                    adapted += " This should give you a comprehensive understanding."
            
            return adapted


# Example: User prefers "short explanations" -> Plugin shortens responses
# User dislikes "technical jargon" -> Plugin simplifies language