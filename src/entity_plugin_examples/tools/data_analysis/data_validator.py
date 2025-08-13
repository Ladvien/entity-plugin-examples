"""Data validator plugin for data quality checks."""

from __future__ import annotations
import json
import re
from typing import Dict, Any, Optional, List

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class DataValidatorPlugin(ToolPlugin):
    """
    Data validator for data quality and format validation.
    
    Features: email validation, phone validation, data completeness
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        # Validation patterns
        self.patterns = {
            "email": re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            "phone": re.compile(r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'),
            "url": re.compile(r'^https?://[^\s/$.?#].[^\s]*$'),
            "ssn": re.compile(r'^\d{3}-\d{2}-\d{4}$')
        }
    
    async def _execute_impl(self, context) -> str:
        """Execute data validation."""
        message = (context.message or "").strip()
        
        if not message:
            return "Error: No validation command provided"
        
        try:
            # Parse: validation_type:data or validate:json_data
            if message.startswith("validate:"):
                # Validate JSON data structure
                json_data = message[9:]  # Remove "validate:" prefix
                return self._validate_json_data(json_data)
            else:
                # Single field validation
                parts = message.split(":", 1)
                if len(parts) != 2:
                    return "Format: validation_type:data or validate:json_data"
                
                validation_type, data = parts
                return self._validate_single_field(validation_type.lower(), data)
                
        except Exception as e:
            return f"Validation Error: {str(e)}"
    
    def _validate_single_field(self, validation_type: str, data: str) -> str:
        """Validate a single field."""
        if validation_type not in self.patterns:
            available = ", ".join(self.patterns.keys())
            return f"Unknown validation type: {validation_type}. Available: {available}"
        
        pattern = self.patterns[validation_type]
        is_valid = bool(pattern.match(data.strip()))
        
        return f"✅ Valid {validation_type}" if is_valid else f"❌ Invalid {validation_type}: {data}"
    
    def _validate_json_data(self, json_data: str) -> str:
        """Validate JSON data structure."""
        try:
            data = json.loads(json_data)
            
            if not isinstance(data, (list, dict)):
                return "Error: Data must be JSON object or array"
            
            # If it's a single object, convert to list
            if isinstance(data, dict):
                data = [data]
            
            # Validation results
            results = {
                "total_records": len(data),
                "valid_records": 0,
                "invalid_records": 0,
                "field_analysis": {},
                "errors": []
            }
            
            for i, record in enumerate(data):
                if not isinstance(record, dict):
                    results["errors"].append(f"Record {i}: Not a valid object")
                    continue
                
                record_valid = True
                
                for field, value in record.items():
                    if field not in results["field_analysis"]:
                        results["field_analysis"][field] = {
                            "total": 0,
                            "empty": 0,
                            "valid": 0,
                            "type_counts": {}
                        }
                    
                    field_stats = results["field_analysis"][field]
                    field_stats["total"] += 1
                    
                    # Track value type
                    value_type = type(value).__name__
                    field_stats["type_counts"][value_type] = field_stats["type_counts"].get(value_type, 0) + 1
                    
                    # Check for empty values
                    if value in [None, "", [], {}]:
                        field_stats["empty"] += 1
                    else:
                        field_stats["valid"] += 1
                        
                        # Validate specific field types
                        if "email" in field.lower() and isinstance(value, str):
                            if not self.patterns["email"].match(value):
                                results["errors"].append(f"Record {i}: Invalid email in field '{field}': {value}")
                                record_valid = False
                        
                        elif "phone" in field.lower() and isinstance(value, str):
                            if not self.patterns["phone"].match(value):
                                results["errors"].append(f"Record {i}: Invalid phone in field '{field}': {value}")
                                record_valid = False
                
                if record_valid:
                    results["valid_records"] += 1
                else:
                    results["invalid_records"] += 1
            
            # Format output
            output = ["📋 **Data Validation Results:**\n"]
            output.append(f"**Total Records:** {results['total_records']}")
            output.append(f"**Valid Records:** {results['valid_records']}")
            output.append(f"**Invalid Records:** {results['invalid_records']}")
            
            if results["field_analysis"]:
                output.append("\n**Field Analysis:**")
                for field, stats in results["field_analysis"].items():
                    completeness = (stats["valid"] / stats["total"] * 100) if stats["total"] > 0 else 0
                    output.append(f"• **{field}:** {completeness:.1f}% complete ({stats['valid']}/{stats['total']})")
            
            if results["errors"]:
                output.append(f"\n**Validation Errors ({len(results['errors'])}):**")
                for error in results["errors"][:5]:  # Show first 5 errors
                    output.append(f"• {error}")
                if len(results["errors"]) > 5:
                    output.append(f"• ... and {len(results['errors']) - 5} more errors")
            
            return "\n".join(output)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"


# Example: await plugin._execute_impl(Mock(message="email:test@example.com"))
# Returns: "✅ Valid email"