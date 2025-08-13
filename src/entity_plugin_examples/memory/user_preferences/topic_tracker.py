"""Track user's topic interests and expertise levels."""

from __future__ import annotations
import re
from typing import Dict, Any, List
from collections import defaultdict

from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE


class TopicTrackerPlugin(Plugin):
    """
    Track topics user discusses and their apparent expertise levels.
    
    Identifies topics and gauges user knowledge for better assistance.
    """
    
    supported_stages = [PARSE]
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] = None):
        super().__init__(resources, config)
        
        # Domain keywords for topic classification
        self.topic_domains = {
            "programming": ["code", "programming", "python", "javascript", "api", "function", "bug", "debug", "software"],
            "data_science": ["data", "analysis", "statistics", "machine learning", "ml", "model", "dataset", "visualization"],  
            "business": ["strategy", "marketing", "sales", "revenue", "customer", "market", "business", "growth"],
            "technology": ["tech", "cloud", "server", "database", "security", "network", "infrastructure", "devops"],
            "design": ["ui", "ux", "design", "interface", "user", "visual", "layout", "prototype", "mockup"],
            "academic": ["research", "study", "paper", "theory", "analysis", "methodology", "hypothesis", "literature"]
        }
        
        # Expertise indicators
        self.expertise_indicators = {
            "beginner": ["how do i", "what is", "i don't understand", "i'm new to", "basic question", "help me learn"],
            "intermediate": ["i've tried", "i know about", "i'm working on", "can you explain", "best practices"],
            "advanced": ["i'm optimizing", "i'm implementing", "architecture", "i've been using", "in my experience", "production"]
        }
    
    async def _execute_impl(self, context) -> str:
        """Track topics and expertise levels from user message."""
        message = (context.message or "").lower().strip()
        
        if not message:
            return context.message or ""
        
        # Get existing topic data
        topic_data = await context.recall("user_topics", {
            "interests": defaultdict(int),      # topic -> frequency count
            "expertise": defaultdict(str),      # topic -> expertise level  
            "recent_topics": [],                # last 10 topics discussed
            "topic_progression": defaultdict(list)  # topic -> [timestamps of mentions]
        })
        
        # Ensure defaultdict behavior is preserved
        if not isinstance(topic_data.get("interests"), dict):
            topic_data["interests"] = defaultdict(int)
        if not isinstance(topic_data.get("expertise"), dict):
            topic_data["expertise"] = defaultdict(str)
        if not isinstance(topic_data.get("topic_progression"), dict):
            topic_data["topic_progression"] = defaultdict(list)
        
        # Detect topics in the message
        detected_topics = []
        for domain, keywords in self.topic_domains.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in message)
            if keyword_matches >= 1:  # At least one keyword match
                detected_topics.append(domain)
                topic_data["interests"][domain] = topic_data["interests"].get(domain, 0) + keyword_matches
        
        # Detect expertise level for each topic
        for topic in detected_topics:
            current_expertise = topic_data["expertise"].get(topic, "unknown")
            
            # Check for expertise indicators
            detected_level = "unknown"
            for level, indicators in self.expertise_indicators.items():
                if any(indicator in message for indicator in indicators):
                    detected_level = level
                    break
            
            # Update expertise (progressive: beginner -> intermediate -> advanced)
            if detected_level != "unknown":
                if current_expertise == "unknown" or self._expertise_priority(detected_level) > self._expertise_priority(current_expertise):
                    topic_data["expertise"][topic] = detected_level
        
        # Update recent topics (keep last 10)
        for topic in detected_topics:
            if topic not in topic_data["recent_topics"]:
                topic_data["recent_topics"].append(topic)
        
        topic_data["recent_topics"] = topic_data["recent_topics"][-10:]
        
        # Track topic progression with timestamps
        import time
        current_time = time.time()
        for topic in detected_topics:
            if topic not in topic_data["topic_progression"]:
                topic_data["topic_progression"][topic] = []
            topic_data["topic_progression"][topic].append(current_time)
            
            # Keep only last 20 timestamps per topic
            topic_data["topic_progression"][topic] = topic_data["topic_progression"][topic][-20:]
        
        # Convert defaultdicts to regular dicts for storage
        topic_data_storage = {
            "interests": dict(topic_data["interests"]),
            "expertise": dict(topic_data["expertise"]), 
            "recent_topics": topic_data["recent_topics"],
            "topic_progression": {k: v for k, v in topic_data["topic_progression"].items()}
        }
        
        await context.remember("user_topics", topic_data_storage)
        
        # Store summary stats
        await context.remember("total_topics_tracked", len(topic_data["interests"]))
        await context.remember("primary_interests", 
            sorted(topic_data["interests"].items(), key=lambda x: x[1], reverse=True)[:3])
        
        return context.message or ""
    
    def _expertise_priority(self, level: str) -> int:
        """Return numeric priority for expertise levels."""
        priorities = {"unknown": 0, "beginner": 1, "intermediate": 2, "advanced": 3}
        return priorities.get(level, 0)


# Example: User asks "How do I debug Python code?"
# Plugin detects: topic="programming", expertise="beginner"
# Later: "I'm optimizing my Python algorithms" -> expertise updated to "advanced"