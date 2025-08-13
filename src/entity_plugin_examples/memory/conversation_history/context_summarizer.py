"""Summarize conversation context for efficient memory usage."""

from __future__ import annotations
from typing import List, Dict, Any

from entity.plugins.prompt import PromptPlugin  
from entity.workflow.stages import THINK


class ContextSummarizerPlugin(PromptPlugin):
    """
    Create conversation summaries to maintain context efficiently.
    
    When conversation gets long, summarizes key points to save memory.
    """
    
    supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        """Summarize conversation if it's getting long."""
        message = context.message or ""
        
        # Get conversation history
        history = await context.recall("conversation_history", [])
        
        if len(history) >= 15:  # Time to summarize
            # Extract messages for summarization
            recent_turns = history[-10:]  # Last 10 turns
            conversation_text = []
            
            for turn in recent_turns:
                speaker = turn.get("speaker", "unknown")
                msg = turn.get("message", "")
                conversation_text.append(f"{speaker.title()}: {msg}")
            
            # Create summary prompt
            dialogue = "\\n".join(conversation_text)
            llm = context.get_resource("llm")
            
            if llm:
                summary_prompt = f"""Summarize this conversation in 2-3 sentences, focusing on:
- Main topics discussed
- User's apparent goals or needs  
- Key decisions or outcomes

Conversation:
{dialogue}

Summary:"""
                
                summary = await llm.generate(summary_prompt)
                await context.remember("conversation_summary", summary)
                
                # Store summary creation timestamp
                import time
                await context.remember("summary_created_at", time.time())
            else:
                # Fallback summary without LLM
                topics = set()
                for turn in recent_turns:
                    msg = turn.get("message", "").lower()
                    # Simple keyword extraction
                    words = msg.split()
                    topics.update([w for w in words if len(w) > 4])
                
                summary = f"Conversation covered: {', '.join(list(topics)[:5])}"
                await context.remember("conversation_summary", summary)
        
        return message


# Example: Automatically creates summaries when conversation exceeds 15 turns
# Helps maintain context while keeping memory usage manageable