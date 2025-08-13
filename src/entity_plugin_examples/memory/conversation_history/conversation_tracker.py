"""Track conversation turns with timestamped history."""

from __future__ import annotations
import time
from typing import Dict, Any, List

from entity.plugins.base import Plugin
from entity.workflow.stages import INPUT, OUTPUT


class ConversationTrackerPlugin(Plugin):
    """
    Tracks conversation history with timestamps.
    
    Stores each user input and agent response in memory for context.
    """
    
    supported_stages = [INPUT, OUTPUT]
    
    async def _execute_impl(self, context) -> str:
        """Track conversation turns in memory."""
        message = context.message or ""
        
        # Get current conversation history
        history = await context.recall("conversation_history", [])
        
        if context.current_stage_name == "INPUT":
            # Record user input
            turn = {
                "timestamp": time.time(),
                "speaker": "user", 
                "message": message,
                "turn_number": len([h for h in history if h.get("speaker") == "user"]) + 1
            }
            history.append(turn)
            await context.remember("conversation_history", history)
            await context.remember("last_user_input", message)
            
        elif context.current_stage_name == "OUTPUT":
            # Record agent response
            turn = {
                "timestamp": time.time(), 
                "speaker": "agent",
                "message": message,
                "turn_number": len([h for h in history if h.get("speaker") == "agent"]) + 1
            }
            history.append(turn)
            await context.remember("conversation_history", history)
            
            # Keep only last 20 turns to prevent memory bloat
            if len(history) > 20:
                history = history[-20:]
                await context.remember("conversation_history", history)
        
        return message


# Example usage:
# await plugin._execute_impl(Mock(message="Hello!", current_stage_name="INPUT"))
# Returns: "Hello!" and stores timestamped conversation turn