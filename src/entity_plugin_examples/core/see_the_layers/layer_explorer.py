"""Layer 2: See the Layers - Explore 4-layer resource architecture.

Agent = Resources + Workflow
      = (Infrastructure→Resources→Tools) + Workflow
"""

from typing import Any, Dict

from entity import Agent
from entity.defaults import load_defaults
from entity.infrastructure.duckdb_infra import DuckDBInfrastructure
from entity.infrastructure.local_storage_infra import LocalStorageInfrastructure
from entity.infrastructure.ollama_infra import OllamaInfrastructure
from entity.plugins.base import Plugin
from entity.resources import (
    DatabaseResource,
    FileStorage,
    LLM,
    LLMResource,
    LocalStorageResource,
    Memory,
    VectorStoreResource,
)
from entity.workflow.stages import THINK
from entity.workflow.workflow import Workflow


class ResourceExplorerPlugin(Plugin):
    """Plugin that demonstrates using each resource layer."""
    
    supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        """Explore and use resources from each layer."""
        message = context.message or ""
        
        print("\n🔍 Exploring 4-Layer Architecture:")
        print("=" * 50)
        
        # Layer 4: Plugin (this code)
        print("Layer 4 - PLUGIN: Using tools to implement behavior")
        
        # Layer 3: Tools (Memory, LLM, FileStorage)
        print("Layer 3 - TOOLS:")
        
        # Memory tool
        memory = context.get_resource("memory")
        if memory:
            await context.remember("explored", True)
            print("  ✓ Memory: Stored exploration flag")
        
        # LLM tool
        llm = context.get_resource("llm")
        if llm:
            response = await llm.generate("Say 'Resources working!'")
            print(f"  ✓ LLM: {response[:50]}")
        
        # FileStorage tool
        storage = context.get_resource("file_storage")
        if storage:
            print("  ✓ FileStorage: Available for file operations")
        
        # Layer 2: Resources (abstraction over infrastructure)
        print("Layer 2 - RESOURCES: Abstracting infrastructure")
        print("  • DatabaseResource wraps DuckDB")
        print("  • LLMResource wraps Ollama")
        print("  • LocalStorageResource wraps filesystem")
        
        # Layer 1: Infrastructure (actual implementations)
        print("Layer 1 - INFRASTRUCTURE: Concrete implementations")
        print("  • DuckDBInfrastructure: SQL database")
        print("  • OllamaInfrastructure: Local LLM")
        print("  • LocalStorageInfrastructure: File system")
        
        print("=" * 50)
        
        return f"Explored all 4 layers for: {message}"


class LayerExplorerExample:
    """Demonstrate the 4-layer resource architecture."""
    
    @staticmethod
    async def run():
        """Create agent showing explicit resource layer construction.
        
        80% Code demonstrating layers:
        - Build from infrastructure up through resources to tools
        - Show how Agent = Resources + Workflow
        """
        # Layer 1: Infrastructure (concrete implementations)
        db_infra = DuckDBInfrastructure(":memory:")
        llm_infra = OllamaInfrastructure("http://localhost:11434", "llama3.2:3b")
        storage_infra = LocalStorageInfrastructure("./agent_files")
        
        # Layer 2: Resources (abstraction layer)
        db_resource = DatabaseResource(db_infra)
        vector_resource = VectorStoreResource(db_infra)
        llm_resource = LLMResource(llm_infra)
        storage_resource = LocalStorageResource(storage_infra)
        
        # Layer 3: Tools (high-level interfaces)
        resources = {
            "memory": Memory(db_resource, vector_resource),
            "llm": LLM(llm_resource),
            "file_storage": FileStorage(storage_resource),
        }
        
        # Layer 4: Plugins (use tools to implement behavior)
        workflow = Workflow(
            steps={
                THINK: [ResourceExplorerPlugin(resources)],
            }
        )
        
        # Agent = Resources + Workflow
        agent = Agent(resources=resources, workflow=workflow)
        
        # Explore the layers
        response = await agent.chat("Show me the resource layers")
        print(f"\n📤 Agent Response: {response}")
        
        return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Layer 2: See the Layers")
        print("=" * 40)
        try:
            agent = await LayerExplorerExample.run()
            print("\n✅ Layer exploration complete!")
        except Exception as e:
            print(f"Note: {e}")
            print("(Some infrastructure may not be available in test environment)")
    
    asyncio.run(main())