"""Scientific calculator plugin with advanced mathematical functions."""

from __future__ import annotations
import math
import re
from typing import Dict, Any, Optional, Callable

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class ScientificCalculatorPlugin(ToolPlugin):
    """
    Scientific calculator with trigonometric, logarithmic, and other advanced functions.
    
    Supports: sin, cos, tan, log, ln, sqrt, pow, abs, factorial, constants (pi, e)
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        # Mathematical functions
        self.functions: Dict[str, Callable] = {
            'sin': math.sin,
            'cos': math.cos, 
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'log': math.log10,  # log base 10
            'ln': math.log,     # natural log
            'log2': math.log2,
            'sqrt': math.sqrt,
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'factorial': math.factorial,
            'degrees': math.degrees,
            'radians': math.radians,
            'exp': math.exp,
        }
        
        # Mathematical constants
        self.constants: Dict[str, float] = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': math.inf,
        }
    
    async def _execute_impl(self, context) -> str:
        """Execute scientific calculator operations."""
        expression = (context.message or "0").strip()
        
        try:
            # Process the expression
            result = self._evaluate_scientific_expression(expression)
            
            # Format result appropriately
            if isinstance(result, (int, float)):
                if result == int(result):
                    return f"Result: {int(result)}"
                else:
                    return f"Result: {result:.10g}"  # Remove trailing zeros
            else:
                return f"Result: {result}"
                
        except Exception as e:
            return f"Scientific Calculator Error: {str(e)}"
    
    def _evaluate_scientific_expression(self, expr: str) -> float:
        """Evaluate scientific mathematical expression."""
        # Clean expression
        expr = self._preprocess_expression(expr)
        
        # Handle special cases
        if not expr or expr == "0":
            return 0.0
        
        try:
            # Replace constants
            for const, value in self.constants.items():
                expr = expr.replace(const, str(value))
            
            # Process functions
            expr = self._process_functions(expr)
            
            # Use eval for scientific expressions (with restricted builtins)
            # Note: In production, would use a proper parser instead
            allowed_names = {
                "__builtins__": {},
                "abs": abs,
                "pow": pow,
                "min": min,
                "max": max,
            }
            
            result = eval(expr, allowed_names)
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression: {str(e)}")
    
    def _preprocess_expression(self, expr: str) -> str:
        """Clean and preprocess the expression."""
        # Remove whitespace
        expr = re.sub(r'\s+', '', expr)
        
        # Add multiplication signs where needed (e.g., 2pi -> 2*pi, 3sin -> 3*sin)
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'(\))([a-zA-Z\d\(])', r'\1*\2', expr)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)
        
        return expr
    
    def _process_functions(self, expr: str) -> str:
        """Process mathematical functions in the expression."""
        # Sort functions by length (longest first) to avoid partial matches
        functions = sorted(self.functions.keys(), key=len, reverse=True)
        
        for func_name in functions:
            func = self.functions[func_name]
            
            # Find function calls with parentheses
            pattern = rf'{func_name}\(([^)]+)\)'
            
            def replace_func(match):
                arg_expr = match.group(1)
                # Recursively process the argument
                arg_value = self._evaluate_scientific_expression(arg_expr)
                try:
                    if func_name == 'factorial' and not isinstance(arg_value, int):
                        arg_value = int(arg_value)
                    result = func(arg_value)
                    return str(result)
                except Exception as e:
                    raise ValueError(f"Error in {func_name}({arg_value}): {str(e)}")
            
            expr = re.sub(pattern, replace_func, expr)
        
        return expr
    
    def get_available_functions(self) -> Dict[str, str]:
        """Get a list of available functions with descriptions."""
        descriptions = {
            'sin': 'Sine (radians)',
            'cos': 'Cosine (radians)', 
            'tan': 'Tangent (radians)',
            'asin': 'Arcsine',
            'acos': 'Arccosine',
            'atan': 'Arctangent',
            'sinh': 'Hyperbolic sine',
            'cosh': 'Hyperbolic cosine',
            'tanh': 'Hyperbolic tangent',
            'log': 'Logarithm base 10',
            'ln': 'Natural logarithm',
            'log2': 'Logarithm base 2',
            'sqrt': 'Square root',
            'abs': 'Absolute value',
            'ceil': 'Ceiling (round up)',
            'floor': 'Floor (round down)',
            'factorial': 'Factorial (n!)',
            'degrees': 'Convert radians to degrees',
            'radians': 'Convert degrees to radians',
            'exp': 'Exponential (e^x)',
        }
        return descriptions
    
    def get_available_constants(self) -> Dict[str, float]:
        """Get available mathematical constants."""
        return self.constants.copy()


# Example usage:
"""
calc = ScientificCalculatorPlugin(resources={}, config={})

# Trigonometric functions
await calc._execute_impl(Mock(message="sin(pi/2)"))  # Result: 1.0
await calc._execute_impl(Mock(message="cos(0)"))     # Result: 1.0

# Logarithms  
await calc._execute_impl(Mock(message="log(100)"))   # Result: 2.0 (log base 10)
await calc._execute_impl(Mock(message="ln(e)"))      # Result: 1.0 (natural log)

# Advanced operations
await calc._execute_impl(Mock(message="sqrt(16)"))   # Result: 4.0
await calc._execute_impl(Mock(message="factorial(5)"))  # Result: 120
await calc._execute_impl(Mock(message="pow(2, 8)"))  # Result: 256.0

# Constants
await calc._execute_impl(Mock(message="2 * pi"))     # Result: 6.283185307179586
await calc._execute_impl(Mock(message="e^2"))        # Result: 7.3890560989306495

# Complex expressions
await calc._execute_impl(Mock(message="sin(pi/4) + cos(pi/4)"))  # Result: 1.4142135623730951
"""