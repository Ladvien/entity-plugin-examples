"""Simple turn counter for conversation flow control."""

from __future__ import annotations

from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE


class TurnCounterPlugin(Plugin):
    """
    Count conversation turns and track engagement metrics.
    
    Useful for conversation flow control and engagement analysis.
    """
    
    supported_stages = [PARSE]
    
    async def _execute_impl(self, context) -> str:
        """Count and track conversation turns."""
        message = context.message or ""
        
        # Increment total turn counter
        total_turns = await context.recall("total_turns", 0)
        total_turns += 1
        await context.remember("total_turns", total_turns)
        
        # Track consecutive short responses (engagement indicator)
        message_length = len(message.strip())
        short_responses = await context.recall("consecutive_short_responses", 0)
        
        if message_length < 10:  # Short response
            short_responses += 1
        else:
            short_responses = 0  # Reset counter on longer response
            
        await context.remember("consecutive_short_responses", short_responses)
        
        # Calculate engagement score (simple heuristic)
        if total_turns > 0:
            history = await context.recall("conversation_history", [])
            avg_message_length = sum(len(h.get("message", "")) for h in history) / max(1, len(history))
            
            engagement_score = min(100, max(0, 
                (avg_message_length / 50) * 50 +  # Length factor
                (total_turns / 10) * 25 +          # Participation factor  
                (max(0, 5 - short_responses) / 5) * 25  # Engagement factor
            ))
            
            await context.remember("engagement_score", round(engagement_score, 1))
        
        # Store turn metadata
        await context.remember("current_turn", total_turns)
        await context.remember("turn_message_length", message_length)
        
        return message


# Example: Tracks turns and calculates engagement metrics
# turn_counter.execute() -> Updates counters, returns original message