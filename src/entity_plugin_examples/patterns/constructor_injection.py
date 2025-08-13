"""Constructor injection pattern example."""

from __future__ import annotations
from typing import Any, Dict, Optional
import logging

from entity.plugins.base import Plugin
from entity.workflow.stages import THINK


class DatabaseService:
    """Example database service to inject."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.logger = logging.getLogger(__name__)
    
    async def query(self, sql: str) -> Dict[str, Any]:
        """Simulate database query."""
        self.logger.info(f"Querying: {sql}")
        return {"result": "mocked_data", "connection": self.connection_string}


class CacheService:
    """Example cache service to inject."""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.cache = {}
    
    async def get(self, key: str) -> Optional[str]:
        """Get cached value."""
        return self.cache.get(key)
    
    async def set(self, key: str, value: str) -> None:
        """Set cached value."""
        self.cache[key] = value


class ConstructorInjectionPlugin(Plugin):
    """
    Example plugin demonstrating constructor injection pattern.
    
    Dependencies are injected via constructor, making the plugin:
    - Testable (can inject mocks)
    - Flexible (can inject different implementations)  
    - Explicit about dependencies
    """
    
    supported_stages = [THINK]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        # Constructor injection - dependencies passed in during initialization
        self.db_service = config.get("database_service") if config else None
        self.cache_service = config.get("cache_service") if config else None
        
        if not self.db_service:
            # Fallback to default if not injected
            self.db_service = DatabaseService("sqlite:///default.db")
        
        if not self.cache_service:
            # Fallback to default if not injected  
            self.cache_service = CacheService("redis://localhost:6379")
    
    async def _execute_impl(self, context) -> str:
        """Process message using injected dependencies."""
        message = context.message or ""
        
        # Use injected cache service
        cached = await self.cache_service.get(f"result:{hash(message)}")
        if cached:
            return f"[CACHED] {cached}"
        
        # Use injected database service
        db_result = await self.db_service.query(f"SELECT * FROM responses WHERE input = '{message}'")
        
        result = f"Processed '{message}' with DB: {db_result['connection']}"
        
        # Cache result
        await self.cache_service.set(f"result:{hash(message)}", result)
        
        return result


# Example usage showing dependency injection:
"""
# Production setup with real services
db = DatabaseService("postgresql://prod-db:5432/myapp")  
cache = CacheService("redis://prod-cache:6379")

plugin = ConstructorInjectionPlugin(
    resources=resources,
    config={
        "database_service": db,
        "cache_service": cache
    }
)

# Test setup with mocked services
mock_db = Mock(spec=DatabaseService)
mock_cache = Mock(spec=CacheService) 

test_plugin = ConstructorInjectionPlugin(
    resources=resources,
    config={
        "database_service": mock_db,
        "cache_service": mock_cache
    }
)
"""