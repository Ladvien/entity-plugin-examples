"""Statistics calculator plugin for basic statistical analysis."""

from __future__ import annotations
import json
import statistics
from typing import Dict, Any, Optional, List, Union

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class StatisticsCalculatorPlugin(ToolPlugin):
    """
    Statistics calculator for basic statistical analysis.
    
    Features: mean, median, mode, std dev, min/max, percentiles
    """
    
    supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        """Execute statistical calculations."""
        message = (context.message or "").strip()
        
        if not message:
            return "Error: No data provided for analysis"
        
        try:
            # Parse input - expect JSON array of numbers
            data = json.loads(message)
            
            if not isinstance(data, list):
                return "Error: Data must be a JSON array of numbers"
            
            # Convert to numbers
            numbers = []
            for item in data:
                if isinstance(item, (int, float)):
                    numbers.append(float(item))
                else:
                    return f"Error: Non-numeric value found: {item}"
            
            if not numbers:
                return "Error: No valid numbers found"
            
            # Calculate statistics
            stats = {
                "count": len(numbers),
                "sum": sum(numbers),
                "mean": statistics.mean(numbers),
                "median": statistics.median(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "range": max(numbers) - min(numbers)
            }
            
            # Standard deviation (if more than 1 value)
            if len(numbers) > 1:
                stats["std_dev"] = statistics.stdev(numbers)
                stats["variance"] = statistics.variance(numbers)
            
            # Mode (if it exists)
            try:
                stats["mode"] = statistics.mode(numbers)
            except statistics.StatisticsError:
                stats["mode"] = "No unique mode"
            
            # Format output
            output = ["📊 **Statistical Analysis Results:**\n"]
            output.append(f"**Count:** {stats['count']}")
            output.append(f"**Sum:** {stats['sum']:.3f}")
            output.append(f"**Mean:** {stats['mean']:.3f}")
            output.append(f"**Median:** {stats['median']:.3f}")
            output.append(f"**Mode:** {stats['mode']}")
            output.append(f"**Min:** {stats['min']:.3f}")
            output.append(f"**Max:** {stats['max']:.3f}")
            output.append(f"**Range:** {stats['range']:.3f}")
            
            if "std_dev" in stats:
                output.append(f"**Std Deviation:** {stats['std_dev']:.3f}")
                output.append(f"**Variance:** {stats['variance']:.3f}")
            
            return "\n".join(output)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format. Expected array of numbers like [1, 2, 3, 4, 5]"
        except Exception as e:
            return f"Statistics Error: {str(e)}"


# Example: await plugin._execute_impl(Mock(message="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"))
# Returns comprehensive statistical analysis