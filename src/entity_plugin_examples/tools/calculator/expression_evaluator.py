"""Advanced expression evaluator plugin with variables and custom functions."""

from __future__ import annotations
import ast
import operator
from typing import Dict, Any, Optional, Union, List

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class ExpressionEvaluatorPlugin(ToolPlugin):
    """
    Advanced expression evaluator with support for:
    - Variables and assignments
    - Custom functions
    - Safe evaluation (no arbitrary code execution)
    - Memory of previous calculations
    """
    
    supported_stages = [DO]
    
    # Safe operators for AST evaluation
    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Not: operator.not_,
        ast.Invert: operator.invert,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.In: lambda x, y: x in y,
        ast.NotIn: lambda x, y: x not in y,
    }
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        # Variable storage
        self.variables: Dict[str, float] = {}
        
        # Built-in functions
        self.functions = {
            'abs': abs,
            'max': max,
            'min': min,
            'sum': sum,
            'len': len,
            'pow': pow,
            'round': round,
        }
        
        # Calculation history
        self.history: List[Dict[str, str]] = []
    
    async def _execute_impl(self, context) -> str:
        """Execute expression evaluation with variables and functions."""
        expression = (context.message or "").strip()
        
        if not expression:
            return "Error: Empty expression"
        
        try:
            # Handle special commands
            if expression.startswith('?'):
                return self._handle_help_command(expression)
            
            # Handle variable assignment (x = 5)
            if '=' in expression and not any(op in expression for op in ['==', '!=', '>=', '<=']):
                return self._handle_assignment(expression)
            
            # Handle function definition (def name(params): body)
            if expression.startswith('def '):
                return self._handle_function_definition(expression)
            
            # Evaluate expression
            result = self._safe_eval(expression)
            
            # Store in history
            self._add_to_history(expression, str(result))
            
            return f"Result: {result}"
            
        except Exception as e:
            error_msg = f"Evaluation Error: {str(e)}"
            self._add_to_history(expression, error_msg)
            return error_msg
    
    def _handle_help_command(self, command: str) -> str:
        """Handle help and info commands."""
        cmd = command[1:].lower()
        
        if cmd == 'vars' or cmd == 'variables':
            if not self.variables:
                return "No variables defined"
            vars_str = ', '.join(f"{k}={v}" for k, v in self.variables.items())
            return f"Variables: {vars_str}"
        
        elif cmd == 'funcs' or cmd == 'functions':
            funcs_str = ', '.join(self.functions.keys())
            return f"Available functions: {funcs_str}"
        
        elif cmd == 'history':
            if not self.history:
                return "No calculation history"
            history_str = '\n'.join([
                f"{i+1}. {h['expr']} = {h['result']}" 
                for i, h in enumerate(self.history[-5:])  # Last 5
            ])
            return f"Recent calculations:\n{history_str}"
        
        elif cmd == 'clear':
            self.variables.clear()
            self.history.clear()
            return "Cleared variables and history"
        
        else:
            return ("Help commands:\n"
                   "?vars - Show variables\n"
                   "?funcs - Show functions\n" 
                   "?history - Show recent calculations\n"
                   "?clear - Clear variables and history")
    
    def _handle_assignment(self, expression: str) -> str:
        """Handle variable assignment (x = expression)."""
        try:
            var_name, value_expr = expression.split('=', 1)
            var_name = var_name.strip()
            value_expr = value_expr.strip()
            
            # Validate variable name
            if not var_name.isidentifier():
                return f"Error: Invalid variable name '{var_name}'"
            
            # Evaluate the right side
            value = self._safe_eval(value_expr)
            
            # Store variable
            self.variables[var_name] = float(value)
            
            self._add_to_history(expression, f"{var_name} = {value}")
            return f"Set {var_name} = {value}"
            
        except Exception as e:
            return f"Assignment Error: {str(e)}"
    
    def _handle_function_definition(self, expression: str) -> str:
        """Handle simple function definitions."""
        # This is a simplified implementation for demo purposes
        # In practice, you'd want a more robust parser
        return "Error: Custom function definitions not yet implemented. Use built-in functions."
    
    def _safe_eval(self, expression: str) -> Union[float, int, bool, List]:
        """Safely evaluate an expression using AST."""
        try:
            # Parse the expression
            node = ast.parse(expression, mode='eval')
            
            # Evaluate the AST node
            return self._eval_node(node.body)
            
        except Exception as e:
            raise ValueError(f"Cannot parse expression: {str(e)}")
    
    def _eval_node(self, node) -> Any:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        
        elif isinstance(node, ast.Str):  # Python < 3.8
            return node.s
        
        elif isinstance(node, ast.Name):
            # Variable lookup
            if node.id in self.variables:
                return self.variables[node.id]
            elif node.id in self.functions:
                return self.functions[node.id]
            else:
                raise NameError(f"Name '{node.id}' is not defined")
        
        elif isinstance(node, ast.BinOp):
            # Binary operations (+ - * / etc.)
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        
        elif isinstance(node, ast.UnaryOp):
            # Unary operations (- + not)
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        
        elif isinstance(node, ast.Compare):
            # Comparison operations
            left = self._eval_node(node.left)
            
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval_node(comparator)
                op_type = type(op)
                
                if op_type in self.SAFE_OPERATORS:
                    if not self.SAFE_OPERATORS[op_type](left, right):
                        return False
                    left = right  # For chained comparisons
                else:
                    raise ValueError(f"Unsupported comparison operator: {op_type.__name__}")
            
            return True
        
        elif isinstance(node, ast.Call):
            # Function calls
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in self.functions:
                    func = self.functions[func_name]
                    args = [self._eval_node(arg) for arg in node.args]
                    kwargs = {kw.arg: self._eval_node(kw.value) for kw in node.keywords}
                    return func(*args, **kwargs)
                else:
                    raise NameError(f"Function '{func_name}' is not defined")
            else:
                raise ValueError("Complex function calls not supported")
        
        elif isinstance(node, ast.List):
            # Lists
            return [self._eval_node(item) for item in node.elts]
        
        elif isinstance(node, ast.Tuple):
            # Tuples
            return tuple(self._eval_node(item) for item in node.elts)
        
        else:
            raise ValueError(f"Unsupported AST node type: {type(node).__name__}")
    
    def _add_to_history(self, expression: str, result: str) -> None:
        """Add calculation to history."""
        self.history.append({
            'expr': expression,
            'result': result
        })
        
        # Keep only last 50 calculations
        if len(self.history) > 50:
            self.history = self.history[-50:]
    
    def get_state(self) -> Dict[str, Any]:
        """Get current calculator state."""
        return {
            'variables': self.variables.copy(),
            'history_count': len(self.history),
            'available_functions': list(self.functions.keys())
        }


# Example usage:
"""
calc = ExpressionEvaluatorPlugin(resources={}, config={})

# Basic calculations
await calc._execute_impl(Mock(message="2 + 3 * 4"))  # Result: 14

# Variables
await calc._execute_impl(Mock(message="x = 5"))      # Set x = 5.0
await calc._execute_impl(Mock(message="y = x * 2"))  # Set y = 10.0
await calc._execute_impl(Mock(message="x + y"))      # Result: 15.0

# Functions
await calc._execute_impl(Mock(message="max(1, 2, 3)"))     # Result: 3
await calc._execute_impl(Mock(message="sum([1,2,3,4])"))   # Result: 10

# Help commands
await calc._execute_impl(Mock(message="?vars"))      # Variables: x=5.0, y=10.0
await calc._execute_impl(Mock(message="?history"))   # Recent calculations: ...

# Lists and comparisons
await calc._execute_impl(Mock(message="[1,2,3,4]"))  # Result: [1, 2, 3, 4]
await calc._execute_impl(Mock(message="5 > 3"))      # Result: True
"""