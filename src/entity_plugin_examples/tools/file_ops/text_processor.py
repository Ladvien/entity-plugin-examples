"""Text processor plugin for text manipulation operations."""

from __future__ import annotations
import re
from typing import Dict, Any, Optional

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class TextProcessorPlugin(ToolPlugin):
    """
    Text processor for common text manipulation tasks.
    
    Features: word count, find/replace, case conversion, line operations
    """
    
    supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        """Execute text processing operations."""
        message = (context.message or "").strip()
        
        if not message:
            return "Error: No text processing command provided"
        
        try:
            # Parse command: operation:text or operation:pattern:replacement:text
            parts = message.split(":", 1)
            if len(parts) != 2:
                return "Format: operation:text (e.g., 'wordcount:Hello world')"
            
            operation = parts[0].lower()
            text_part = parts[1]
            
            if operation == "wordcount":
                words = len(text_part.split())
                chars = len(text_part)
                lines = len(text_part.split('\n'))
                return f"Words: {words}, Characters: {chars}, Lines: {lines}"
            
            elif operation == "upper":
                return text_part.upper()
            
            elif operation == "lower":
                return text_part.lower()
            
            elif operation == "reverse":
                return text_part[::-1]
            
            elif operation == "replace":
                # Format: replace:pattern:replacement:text
                replace_parts = text_part.split(":", 2)
                if len(replace_parts) != 3:
                    return "Format: replace:pattern:replacement:text"
                pattern, replacement, text = replace_parts
                return text.replace(pattern, replacement)
            
            else:
                return f"Unknown operation: {operation}. Available: wordcount, upper, lower, reverse, replace"
                
        except Exception as e:
            return f"Text Processing Error: {str(e)}"


# Example: await plugin._execute_impl(Mock(message="wordcount:Hello world"))
# Returns: "Words: 2, Characters: 11, Lines: 1"