"""Adapt communication style based on observed personality traits."""

from __future__ import annotations
import re
from typing import Dict, Any, List
from collections import defaultdict

from entity.plugins.base import Plugin
from entity.workflow.stages import OUTPUT


class PersonalityAdapterPlugin(Plugin):
    """
    Adapt communication style based on learned personality traits.
    
    Observes communication preferences and adjusts response style accordingly.
    """
    
    supported_stages = [OUTPUT]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Personality trait indicators
        self.personality_patterns = {
            "communication_style": {
                "formal": [r"please", r"thank you", r"would you", r"could you", r"i appreciate"],
                "casual": [r"hey", r"yeah", r"cool", r"awesome", r"no worries", r"sure thing"],
                "direct": [r"just", r"simply", r"exactly", r"specifically", r"straight"],
                "detailed": [r"explain", r"elaborate", r"comprehensive", r"thorough", r"complete"]
            },
            "learning_preference": {
                "visual": [r"show me", r"diagram", r"chart", r"image", r"picture", r"visual"],
                "practical": [r"example", r"demo", r"hands-on", r"practice", r"try it"],
                "theoretical": [r"concept", r"theory", r"principle", r"abstract", r"understand why"],
                "step_by_step": [r"step", r"guide", r"walkthrough", r"sequence", r"order"]
            },
            "interaction_style": {
                "collaborative": [r"let's", r"we can", r"together", r"team", r"work with"],
                "independent": [r"i'll", r"myself", r"on my own", r"individually", r"solo"],
                "supportive": [r"help me", r"assist", r"guide", r"support", r"encourage"],
                "challenging": [r"challenge", r"difficult", r"advanced", r"complex", r"push"]
            }
        }
    
    async def _execute_impl(self, context) -> str:
        """Adapt response style based on personality profile."""
        message = context.message or ""
        
        # Get current personality profile
        personality_profile = await context.recall("personality_profile", {
            "communication_traits": defaultdict(int),    # trait -> frequency count
            "learning_preferences": defaultdict(int),    # preference -> frequency
            "interaction_preferences": defaultdict(int), # style -> frequency
            "adaptation_history": [],                    # track adaptations
            "dominant_traits": {}                        # current dominant traits
        })
        
        # Analyze current message for personality indicators
        message_lower = message.lower()
        traits_detected = []
        
        for category, traits in self.personality_patterns.items():
            for trait, patterns in traits.items():
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        personality_profile[f"{category}"][trait] += 1
                        traits_detected.append(f"{category}:{trait}")
        
        # Update dominant traits
        for category in ["communication_traits", "learning_preferences", "interaction_preferences"]:
            if personality_profile[category]:
                dominant_trait = max(personality_profile[category].items(), key=lambda x: x[1])
                personality_profile["dominant_traits"][category.replace("_traits", "").replace("_preferences", "")] = dominant_trait[0]
        
        # Adapt response style based on personality profile
        adapted_message = self._adapt_response_style(message, personality_profile["dominant_traits"])
        
        # Record adaptation if changes were made
        if adapted_message != message:
            import time
            adaptation_record = {
                "timestamp": time.time(),
                "original_length": len(message),
                "adapted_length": len(adapted_message),
                "traits_applied": list(personality_profile["dominant_traits"].values()),
                "detected_indicators": traits_detected
            }
            personality_profile["adaptation_history"].append(adaptation_record)
            
            # Keep only last 20 adaptations
            if len(personality_profile["adaptation_history"]) > 20:
                personality_profile["adaptation_history"] = personality_profile["adaptation_history"][-20:]
        
        # Convert defaultdicts for storage
        profile_storage = {
            "communication_traits": dict(personality_profile["communication_traits"]),
            "learning_preferences": dict(personality_profile["learning_preferences"]),
            "interaction_preferences": dict(personality_profile["interaction_preferences"]),
            "adaptation_history": personality_profile["adaptation_history"],
            "dominant_traits": personality_profile["dominant_traits"]
        }
        
        await context.remember("personality_profile", profile_storage)
        
        return adapted_message
    
    def _adapt_response_style(self, message: str, dominant_traits: Dict[str, str]) -> str:
        """Adapt message style based on dominant personality traits."""
        adapted = message
        
        # Get communication style preference
        communication_style = dominant_traits.get("communication", "casual")
        learning_preference = dominant_traits.get("learning", "practical")
        interaction_style = dominant_traits.get("interaction", "collaborative")
        
        # Apply communication style adaptations
        if communication_style == "formal" and message:
            # Make responses more formal
            adapted = self._formalize_response(adapted)
        elif communication_style == "casual" and message:
            # Make responses more casual/friendly
            adapted = self._casualize_response(adapted)
        elif communication_style == "direct" and message:
            # Make responses more concise and direct
            adapted = self._directify_response(adapted)
        elif communication_style == "detailed" and message:
            # Add more comprehensive explanations
            adapted = self._add_detail_cues(adapted)
        
        # Apply learning preference adaptations
        if learning_preference == "visual" and message:
            adapted = self._add_visual_cues(adapted)
        elif learning_preference == "practical" and message:
            adapted = self._add_practical_examples(adapted)
        elif learning_preference == "step_by_step" and message:
            adapted = self._add_structure_cues(adapted)
        
        # Apply interaction style adaptations
        if interaction_style == "collaborative" and message:
            adapted = self._add_collaborative_language(adapted)
        elif interaction_style == "supportive" and message:
            adapted = self._add_supportive_language(adapted)
        
        return adapted
    
    def _formalize_response(self, message: str) -> str:
        """Make response more formal."""
        # Add formal language patterns
        if message and not message.startswith(("Please", "I would", "Allow me")):
            if "let me" in message.lower():
                message = message.replace("let me", "Allow me to", 1)
            elif message.startswith(("I'll", "I will")):
                message = "I shall " + message[5:] if message.startswith("I'll ") else message
        return message
    
    def _casualize_response(self, message: str) -> str:
        """Make response more casual and friendly."""
        # Add casual language patterns
        casual_starters = ["Sure!", "Great!", "Absolutely!", "No problem!"]
        if message and not any(message.startswith(starter) for starter in casual_starters):
            # Add casual acknowledgment occasionally
            import random
            if random.random() < 0.3:  # 30% chance
                message = random.choice(casual_starters) + " " + message
        return message
    
    def _directify_response(self, message: str) -> str:
        """Make response more direct and concise."""
        # Remove unnecessary qualifiers
        qualifiers = ["perhaps", "maybe", "possibly", "it seems", "I think"]
        for qualifier in qualifiers:
            message = message.replace(qualifier + " ", "")
        return message
    
    def _add_detail_cues(self, message: str) -> str:
        """Add cues for more detailed explanations."""
        if message and len(message) > 50:
            # Add detail invitation
            if not any(phrase in message.lower() for phrase in ["more detail", "explain further", "elaborate"]):
                message += "\n\nWould you like me to elaborate on any specific aspect?"
        return message
    
    def _add_visual_cues(self, message: str) -> str:
        """Add visual learning cues."""
        visual_cues = ["diagram", "chart", "visual representation", "illustration"]
        if message and len(message) > 100:
            # Suggest visual aids for complex topics
            if not any(cue in message.lower() for cue in visual_cues):
                message += "\n\n(A diagram might help visualize this concept.)"
        return message
    
    def _add_practical_examples(self, message: str) -> str:
        """Add practical example cues."""
        if message and "example" not in message.lower() and len(message) > 80:
            message += "\n\nWould a practical example help clarify this?"
        return message
    
    def _add_structure_cues(self, message: str) -> str:
        """Add step-by-step structure cues."""
        if message and len(message) > 100 and not re.search(r'\d+\.|Step \d+', message):
            # Suggest breaking into steps
            message += "\n\nShall I break this down into specific steps?"
        return message
    
    def _add_collaborative_language(self, message: str) -> str:
        """Add collaborative language patterns."""
        collaborative_phrases = ["let's", "we can", "together we", "our approach"]
        if message and not any(phrase in message.lower() for phrase in collaborative_phrases):
            # Replace "you should" with "we could"
            message = message.replace("You should", "We could")
            message = message.replace("you should", "we could")
        return message
    
    def _add_supportive_language(self, message: str) -> str:
        """Add supportive and encouraging language."""
        if message and len(message) > 50:
            supportive_endings = [
                "You're doing great!",
                "Keep up the good work!",
                "This is a great question!",
                "You're on the right track!"
            ]
            import random
            if random.random() < 0.2:  # 20% chance
                message += "\n\n" + random.choice(supportive_endings)
        return message


# Example: User consistently uses formal language -> plugin adapts to formal response style
# User prefers step-by-step -> plugin offers to break down complex topics