"""File converter plugin for format conversions."""

from __future__ import annotations
import json
import csv
from io import StringIO
from typing import Dict, Any, Optional

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class FileConverterPlugin(ToolPlugin):
    """
    File converter for format conversions.
    
    Features: JSON to CSV, CSV to JSON, format validation
    """
    
    supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        """Execute file conversion operations."""
        message = (context.message or "").strip()
        
        if not message:
            return "Error: No conversion command provided"
        
        try:
            # Parse: from_format:to_format:data
            parts = message.split(":", 2)
            if len(parts) != 3:
                return "Format: from_format:to_format:data (e.g., 'json:csv:{\"name\":\"John\"}')"
            
            from_format, to_format, data = parts
            
            if from_format.lower() == "json" and to_format.lower() == "csv":
                return self._json_to_csv(data)
            elif from_format.lower() == "csv" and to_format.lower() == "json":
                return self._csv_to_json(data)
            else:
                return f"Conversion {from_format} to {to_format} not supported"
                
        except Exception as e:
            return f"Conversion Error: {str(e)}"
    
    def _json_to_csv(self, json_data: str) -> str:
        """Convert JSON to CSV format."""
        try:
            data = json.loads(json_data)
            if not isinstance(data, list):
                data = [data]
            
            if not data:
                return "CSV:\n(empty)"
            
            # Get headers from first object
            headers = list(data[0].keys())
            
            # Create CSV
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            
            return f"CSV:\n{output.getvalue()}"
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON data"
    
    def _csv_to_json(self, csv_data: str) -> str:
        """Convert CSV to JSON format."""
        try:
            reader = csv.DictReader(StringIO(csv_data))
            data = list(reader)
            return f"JSON:\n{json.dumps(data, indent=2)}"
        except Exception as e:
            return f"Error: Invalid CSV data - {str(e)}"


# Example: await plugin._execute_impl(Mock(message="json:csv:[{\"name\":\"John\",\"age\":30}]"))
# Returns CSV format of the JSON data