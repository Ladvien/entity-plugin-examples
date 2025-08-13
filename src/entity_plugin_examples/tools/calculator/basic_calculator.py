"""Basic calculator plugin for simple arithmetic operations."""

from __future__ import annotations
import re
from typing import Dict, Any, Optional

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class BasicCalculatorPlugin(ToolPlugin):
    """
    Basic calculator for simple arithmetic operations.
    
    Supports: +, -, *, /, parentheses, decimal numbers
    Safe evaluation without exec/eval for security.
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y, 
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else float('inf')
        }
    
    async def _execute_impl(self, context) -> str:
        """Execute basic calculator operations."""
        expression = (context.message or "0").strip()
        
        try:
            # Clean and validate expression
            expression = self._clean_expression(expression)
            
            # Parse and evaluate
            result = self._evaluate_expression(expression)
            
            return f"Result: {result}"
            
        except Exception as e:
            return f"Calculator Error: {str(e)}"
    
    def _clean_expression(self, expr: str) -> str:
        """Clean and validate mathematical expression."""
        # Remove whitespace
        expr = re.sub(r'\s+', '', expr)
        
        # Validate characters
        allowed = set('0123456789+-*/.()') 
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters in expression")
        
        # Basic validation
        if not expr:
            return "0"
        
        return expr
    
    def _evaluate_expression(self, expr: str) -> float:
        """Safely evaluate mathematical expression using recursive descent parser."""
        self.pos = 0
        self.expr = expr
        result = self._parse_expression()
        
        if self.pos < len(self.expr):
            raise ValueError("Unexpected characters at end of expression")
        
        return result
    
    def _parse_expression(self) -> float:
        """Parse addition and subtraction (lowest precedence)."""
        result = self._parse_term()
        
        while self.pos < len(self.expr) and self.expr[self.pos] in '+-':
            op = self.expr[self.pos]
            self.pos += 1
            right = self._parse_term()
            result = self.operations[op](result, right)
        
        return result
    
    def _parse_term(self) -> float:
        """Parse multiplication and division (higher precedence)."""
        result = self._parse_factor()
        
        while self.pos < len(self.expr) and self.expr[self.pos] in '*/':
            op = self.expr[self.pos]
            self.pos += 1
            right = self._parse_factor()
            result = self.operations[op](result, right)
        
        return result
    
    def _parse_factor(self) -> float:
        """Parse numbers and parentheses (highest precedence)."""
        if self.pos >= len(self.expr):
            raise ValueError("Unexpected end of expression")
        
        # Handle negative numbers
        if self.expr[self.pos] == '-':
            self.pos += 1
            return -self._parse_factor()
        
        # Handle positive sign
        if self.expr[self.pos] == '+':
            self.pos += 1
            return self._parse_factor()
        
        # Handle parentheses
        if self.expr[self.pos] == '(':
            self.pos += 1
            result = self._parse_expression()
            if self.pos >= len(self.expr) or self.expr[self.pos] != ')':
                raise ValueError("Missing closing parenthesis")
            self.pos += 1
            return result
        
        # Handle numbers
        return self._parse_number()
    
    def _parse_number(self) -> float:
        """Parse decimal numbers."""
        start = self.pos
        
        # Parse digits before decimal point
        while (self.pos < len(self.expr) and 
               self.expr[self.pos].isdigit()):
            self.pos += 1
        
        # Parse decimal point and digits after
        if (self.pos < len(self.expr) and 
            self.expr[self.pos] == '.'):
            self.pos += 1
            while (self.pos < len(self.expr) and 
                   self.expr[self.pos].isdigit()):
                self.pos += 1
        
        if start == self.pos:
            raise ValueError("Expected number")
        
        return float(self.expr[start:self.pos])


# Example usage:
"""
calculator = BasicCalculatorPlugin(resources={}, config={})

# Simple arithmetic
await calculator._execute_impl(Mock(message="2 + 3"))  # "Result: 5.0"
await calculator._execute_impl(Mock(message="10 / 2"))  # "Result: 5.0" 
await calculator._execute_impl(Mock(message="(2 + 3) * 4"))  # "Result: 20.0"

# Decimal numbers
await calculator._execute_impl(Mock(message="3.14 * 2"))  # "Result: 6.28"

# Error handling
await calculator._execute_impl(Mock(message="10 / 0"))  # "Result: inf"
await calculator._execute_impl(Mock(message="2 + abc"))  # "Calculator Error: Invalid characters..."
"""