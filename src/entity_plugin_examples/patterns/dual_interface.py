"""Dual interface pattern example - anthropomorphic vs direct."""

from __future__ import annotations
from typing import Any, Dict, Optional
import json

from entity.plugins.base import Plugin
from entity.workflow.stages import DO


class DualInterfacePlugin(Plugin):
    """
    Example plugin demonstrating dual interface pattern.
    
    Supports both:
    1. Anthropomorphic interface - natural language interactions
    2. Direct interface - structured data/API calls
    
    The plugin detects which interface to use based on input format.
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        self.calculator_functions = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero"
        }
    
    async def _execute_impl(self, context) -> str:
        """Route to appropriate interface based on input format."""
        message = context.message or ""
        
        # Try direct interface first (structured data)
        if self._is_structured_input(message):
            return await self._handle_direct_interface(message)
        else:
            return await self._handle_anthropomorphic_interface(message)
    
    def _is_structured_input(self, message: str) -> bool:
        """Check if input is structured JSON."""
        try:
            data = json.loads(message)
            return isinstance(data, dict) and "action" in data
        except (json.JSONDecodeError, TypeError):
            return False
    
    async def _handle_direct_interface(self, message: str) -> str:
        """
        Direct interface - structured commands.
        
        Expected format:
        {
            "action": "calculate", 
            "operation": "add",
            "operands": [5, 3]
        }
        """
        try:
            data = json.loads(message)
            
            if data["action"] == "calculate":
                operation = data["operation"]
                operands = data["operands"]
                
                if operation in self.calculator_functions:
                    result = self.calculator_functions[operation](*operands)
                    return json.dumps({
                        "interface": "direct",
                        "result": result,
                        "operation": f"{operation}({', '.join(map(str, operands))})"
                    })
                else:
                    return json.dumps({
                        "interface": "direct",
                        "error": f"Unknown operation: {operation}",
                        "available_operations": list(self.calculator_functions.keys())
                    })
            
            return json.dumps({
                "interface": "direct", 
                "error": f"Unknown action: {data['action']}"
            })
            
        except Exception as e:
            return json.dumps({
                "interface": "direct",
                "error": f"Invalid JSON structure: {str(e)}"
            })
    
    async def _handle_anthropomorphic_interface(self, message: str) -> str:
        """
        Anthropomorphic interface - natural language.
        
        Examples:
        - "What's 5 plus 3?"
        - "Calculate 10 divided by 2"
        - "Add 15 and 25"
        """
        message_lower = message.lower()
        
        # Simple natural language parsing
        if any(word in message_lower for word in ["add", "plus", "+"]):
            numbers = self._extract_numbers(message)
            if len(numbers) >= 2:
                result = self.calculator_functions["add"](numbers[0], numbers[1])
                return f"🤖 I calculated {numbers[0]} + {numbers[1]} = {result}"
        
        elif any(word in message_lower for word in ["subtract", "minus", "-"]):
            numbers = self._extract_numbers(message)
            if len(numbers) >= 2:
                result = self.calculator_functions["subtract"](numbers[0], numbers[1])
                return f"🤖 I calculated {numbers[0]} - {numbers[1]} = {result}"
        
        elif any(word in message_lower for word in ["multiply", "times", "*"]):
            numbers = self._extract_numbers(message)
            if len(numbers) >= 2:
                result = self.calculator_functions["multiply"](numbers[0], numbers[1])
                return f"🤖 I calculated {numbers[0]} × {numbers[1]} = {result}"
        
        elif any(word in message_lower for word in ["divide", "divided", "/"]):
            numbers = self._extract_numbers(message)
            if len(numbers) >= 2:
                result = self.calculator_functions["divide"](numbers[0], numbers[1])
                return f"🤖 I calculated {numbers[0]} ÷ {numbers[1]} = {result}"
        
        # Fallback for unrecognized natural language
        return (f"🤖 I understand you want me to do something with: '{message}'\n"
                f"I can help with math! Try:\n"
                f"• 'What's 5 plus 3?'\n"  
                f"• 'Calculate 10 divided by 2'\n"
                f"Or use direct JSON: {{'action': 'calculate', 'operation': 'add', 'operands': [5, 3]}}")
    
    def _extract_numbers(self, text: str) -> list[float]:
        """Extract numbers from text."""
        import re
        numbers = []
        for match in re.finditer(r'-?\d+(?:\.\d+)?', text):
            numbers.append(float(match.group()))
        return numbers


# Example usage showing both interfaces:
"""
# Anthropomorphic interface examples:
await plugin.execute(context_with_message("What's 5 plus 3?"))
# Returns: "🤖 I calculated 5.0 + 3.0 = 8.0"

await plugin.execute(context_with_message("Calculate 10 divided by 2"))  
# Returns: "🤖 I calculated 10.0 ÷ 2.0 = 5.0"

# Direct interface examples:
await plugin.execute(context_with_message('{"action": "calculate", "operation": "add", "operands": [5, 3]}'))
# Returns: {"interface": "direct", "result": 8, "operation": "add(5, 3)"}

await plugin.execute(context_with_message('{"action": "calculate", "operation": "multiply", "operands": [7, 6]}'))
# Returns: {"interface": "direct", "result": 42, "operation": "multiply(7, 6)"}
"""