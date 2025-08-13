"""Chart generator plugin for creating text-based visualizations."""

from __future__ import annotations
import json
from typing import Dict, Any, Optional, List

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class ChartGeneratorPlugin(ToolPlugin):
    """
    Chart generator for creating simple text-based visualizations.
    
    Features: bar charts, histograms, simple line plots (ASCII art)
    """
    
    supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        """Generate text-based charts."""
        message = (context.message or "").strip()
        
        if not message:
            return "Error: No chart command provided"
        
        try:
            # Parse: chart_type:data or chart_type:labels:data
            parts = message.split(":", 2)
            if len(parts) < 2:
                return "Format: chart_type:data or chart_type:labels:data"
            
            chart_type = parts[0].lower()
            
            if len(parts) == 2:
                # chart_type:data
                data = json.loads(parts[1])
                labels = [str(i) for i in range(len(data))]
            else:
                # chart_type:labels:data
                labels = json.loads(parts[1])
                data = json.loads(parts[2])
            
            if len(labels) != len(data):
                return "Error: Labels and data must have the same length"
            
            if chart_type == "bar":
                return self._create_bar_chart(labels, data)
            elif chart_type == "histogram":
                return self._create_histogram(data)
            elif chart_type == "line":
                return self._create_line_plot(labels, data)
            else:
                return f"Unknown chart type: {chart_type}. Available: bar, histogram, line"
                
        except json.JSONDecodeError:
            return "Error: Invalid JSON in data or labels"
        except Exception as e:
            return f"Chart Generation Error: {str(e)}"
    
    def _create_bar_chart(self, labels: List[str], data: List[float]) -> str:
        """Create ASCII bar chart."""
        if not data:
            return "Error: No data provided"
        
        # Normalize data for display
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        max_bar_width = 40
        
        output = ["📊 **Bar Chart:**\n"]
        
        for label, value in zip(labels, data):
            # Calculate bar length
            normalized = (value - min_val) / range_val
            bar_length = int(normalized * max_bar_width)
            
            # Create bar
            bar = "█" * bar_length
            
            # Format label (truncate if too long)
            formatted_label = label[:10].ljust(10)
            
            output.append(f"{formatted_label} │{bar} {value:.2f}")
        
        output.append(f"{'':>10} └{'─' * max_bar_width}")
        output.append(f"{'':>12}{min_val:.1f}{'':<{max_bar_width-8}}{max_val:.1f}")
        
        return "\n".join(output)
    
    def _create_histogram(self, data: List[float]) -> str:
        """Create histogram of data distribution."""
        if not data:
            return "Error: No data provided"
        
        # Create bins
        min_val = min(data)
        max_val = max(data)
        num_bins = min(10, len(set(data)))  # Up to 10 bins
        
        if num_bins == 1:
            return f"📊 **Histogram:** All values are {min_val}"
        
        bin_width = (max_val - min_val) / num_bins
        bins = [0] * num_bins
        
        # Count values in each bin
        for value in data:
            bin_index = int((value - min_val) / bin_width)
            if bin_index >= num_bins:
                bin_index = num_bins - 1
            bins[bin_index] += 1
        
        # Create histogram
        max_count = max(bins)
        max_bar_height = 20
        
        output = ["📊 **Histogram:**\n"]
        
        # Draw bars from top to bottom
        for level in range(max_bar_height, 0, -1):
            line = "  "
            for count in bins:
                normalized_height = (count / max_count) * max_bar_height
                if normalized_height >= level:
                    line += "█"
                else:
                    line += " "
            output.append(line)
        
        # Add x-axis
        output.append("  " + "─" * num_bins)
        
        # Add bin labels
        bin_labels = []
        for i in range(num_bins):
            bin_start = min_val + i * bin_width
            bin_labels.append(f"{bin_start:.1f}")
        
        output.append("  " + "".join(label[0] for label in bin_labels))
        
        return "\n".join(output)
    
    def _create_line_plot(self, labels: List[str], data: List[float]) -> str:
        """Create simple ASCII line plot."""
        if not data:
            return "Error: No data provided"
        
        if len(data) < 2:
            return "Error: Need at least 2 data points for line plot"
        
        # Normalize data
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        height = 15  # Plot height
        width = min(len(data), 50)  # Plot width
        
        output = ["📈 **Line Plot:**\n"]
        
        # Create plot grid
        plot_grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Plot data points
        for i, value in enumerate(data[:width]):
            x = i
            y = height - 1 - int(((value - min_val) / range_val) * (height - 1))
            y = max(0, min(height - 1, y))
            
            plot_grid[y][x] = '●'
            
            # Connect points with lines (simple approximation)
            if i > 0 and i < len(data):
                prev_value = data[i-1]
                prev_y = height - 1 - int(((prev_value - min_val) / range_val) * (height - 1))
                prev_y = max(0, min(height - 1, prev_y))
                
                # Draw line between points
                if abs(y - prev_y) > 1:
                    steps = abs(y - prev_y)
                    for step in range(1, steps):
                        interp_y = prev_y + int((y - prev_y) * step / steps)
                        interp_y = max(0, min(height - 1, interp_y))
                        if plot_grid[interp_y][x] == ' ':
                            plot_grid[interp_y][x] = '│'
        
        # Add y-axis labels and render plot
        for i, row in enumerate(plot_grid):
            y_val = max_val - (i / (height - 1)) * range_val
            y_label = f"{y_val:.1f}".rjust(6)
            output.append(f"{y_label} │{''.join(row)}")
        
        # Add x-axis
        output.append("       └" + "─" * width)
        
        # Add some x-axis labels
        x_labels = "        "
        for i in range(0, min(width, len(labels)), max(1, width // 10)):
            label = labels[i][:3]
            x_labels += label + " " * (max(1, width // 10) - len(label))
        
        output.append(x_labels[:width + 8])
        
        return "\n".join(output)


# Example: await plugin._execute_impl(Mock(message='bar:["A","B","C"]:[10, 25, 15]'))
# Returns ASCII bar chart