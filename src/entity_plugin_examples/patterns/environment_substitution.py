"""Environment variable substitution pattern example."""

from __future__ import annotations
from typing import Any, Dict, Optional
import os
import re
import logging
from pathlib import Path

from entity.plugins.base import Plugin
from entity.workflow.stages import INPUT, PARSE


class EnvironmentSubstitutionPlugin(Plugin):
    """
    Example plugin demonstrating environment variable substitution pattern.
    
    Features:
    - Substitutes ${VAR_NAME} patterns with environment variables
    - Supports default values: ${VAR_NAME:default_value}
    - Handles nested substitution
    - Can read from .env files
    - Validates required variables
    - Provides clear error messages for missing variables
    """
    
    supported_stages = [INPUT, PARSE]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        self.logger = logging.getLogger(__name__)
        
        # Configuration options
        config = config or {}
        self.env_file_path = config.get("env_file_path", ".env")
        self.required_vars = config.get("required_variables", [])
        self.allow_missing_vars = config.get("allow_missing_variables", False)
        self.substitution_prefix = config.get("substitution_prefix", "${")
        self.substitution_suffix = config.get("substitution_suffix", "}")
        
        # Load additional environment variables from .env file if specified
        if self.env_file_path and Path(self.env_file_path).exists():
            self._load_env_file(self.env_file_path)
        
        # Validate required variables are present
        self._validate_required_variables()
    
    async def _execute_impl(self, context) -> str:
        """Perform environment variable substitution on the message."""
        message = context.message or ""
        
        try:
            # Perform substitution
            substituted_message = self._substitute_environment_variables(message)
            
            # Log substitution details
            if substituted_message != message:
                self.logger.info(f"Environment substitution applied: {len(message)} -> {len(substituted_message)} chars")
            
            return substituted_message
            
        except Exception as e:
            error_msg = f"Environment substitution failed: {str(e)}"
            self.logger.error(error_msg)
            if self.allow_missing_vars:
                return message  # Return original message if substitution fails
            else:
                return f"ERROR: {error_msg}"
    
    def _substitute_environment_variables(self, text: str) -> str:
        """
        Substitute environment variables in text.
        
        Supports patterns:
        - ${VAR_NAME} - substitutes with env var value
        - ${VAR_NAME:default} - substitutes with env var or default value
        - ${VAR_NAME:-default} - substitutes with env var or default if var is empty/unset
        """
        # Pattern to match ${VAR_NAME} or ${VAR_NAME:default} or ${VAR_NAME:-default}
        pattern = re.compile(
            rf'{re.escape(self.substitution_prefix)}'
            r'([A-Za-z_][A-Za-z0-9_]*)'
            r'(?:(:-?)(.*?))?'
            rf'{re.escape(self.substitution_suffix)}'
        )
        
        def replace_match(match):
            var_name = match.group(1)
            separator = match.group(2)  # ':' or ':-'
            default_value = match.group(3) if match.group(3) is not None else ""
            
            # Get environment variable value
            env_value = os.environ.get(var_name)
            
            if env_value is not None:
                # Check for ':-' which means use default if value is empty
                if separator == ":-" and not env_value.strip():
                    return default_value
                return env_value
            elif separator:  # Has default value
                return default_value
            elif self.allow_missing_vars:
                # Return original placeholder if missing vars are allowed
                return match.group(0)
            else:
                raise ValueError(f"Environment variable '{var_name}' is not set and no default provided")
        
        # Perform substitution (may need multiple passes for nested variables)
        max_iterations = 5
        for _ in range(max_iterations):
            new_text = pattern.sub(replace_match, text)
            if new_text == text:
                break  # No more substitutions found
            text = new_text
        
        return text
    
    def _load_env_file(self, env_file_path: str) -> None:
        """Load environment variables from .env file."""
        try:
            with open(env_file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse KEY=VALUE format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Only set if not already in environment (environment takes precedence)
                        if key not in os.environ:
                            os.environ[key] = value
                            
            self.logger.info(f"Loaded environment variables from {env_file_path}")
            
        except Exception as e:
            self.logger.warning(f"Failed to load .env file {env_file_path}: {str(e)}")
    
    def _validate_required_variables(self) -> None:
        """Validate that all required environment variables are present."""
        missing_vars = []
        
        for var_name in self.required_vars:
            if var_name not in os.environ:
                missing_vars.append(var_name)
        
        if missing_vars:
            error_msg = f"Required environment variables missing: {', '.join(missing_vars)}"
            self.logger.error(error_msg)
            if not self.allow_missing_vars:
                raise ValueError(error_msg)
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get information about current environment configuration."""
        return {
            "env_file_loaded": Path(self.env_file_path).exists() if self.env_file_path else False,
            "required_variables": self.required_vars,
            "required_vars_present": [var for var in self.required_vars if var in os.environ],
            "required_vars_missing": [var for var in self.required_vars if var not in os.environ],
            "substitution_pattern": f"{self.substitution_prefix}VAR_NAME{self.substitution_suffix}",
            "allow_missing_vars": self.allow_missing_vars,
            "total_env_vars": len(os.environ)
        }


# Example usage and configuration:
"""
# .env file example:
# APP_NAME=MyEntityApp
# DATABASE_URL=postgresql://localhost:5432/myapp
# API_KEY=sk-1234567890abcdef
# DEBUG_MODE=true
# MAX_WORKERS=4

# Plugin configuration:
plugin = EnvironmentSubstitutionPlugin(
    resources=resources,
    config={
        "env_file_path": ".env",
        "required_variables": ["APP_NAME", "DATABASE_URL"],
        "allow_missing_variables": False,
        "substitution_prefix": "${",
        "substitution_suffix": "}"
    }
)

# Example messages with substitution:
await plugin.execute(context_with_message("Hello from ${APP_NAME}!"))
# Returns: "Hello from MyEntityApp!"

await plugin.execute(context_with_message("Connecting to ${DATABASE_URL}"))
# Returns: "Connecting to postgresql://localhost:5432/myapp"

await plugin.execute(context_with_message("API endpoint: ${API_ENDPOINT:https://api.default.com}"))
# Returns: "API endpoint: https://api.default.com" (uses default since API_ENDPOINT not set)

await plugin.execute(context_with_message("Debug: ${DEBUG_MODE} | Workers: ${MAX_WORKERS}"))
# Returns: "Debug: true | Workers: 4"

# Nested substitution example:
os.environ["BASE_URL"] = "https://${APP_NAME}.com"
await plugin.execute(context_with_message("Visit ${BASE_URL} for more info"))
# Returns: "Visit https://MyEntityApp.com for more info"
"""