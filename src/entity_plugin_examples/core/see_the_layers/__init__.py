"""Layer 2: See the Layers - Understand the 4-layer resource architecture.

Shows the resource layers:
1. Infrastructure (DuckDB, Ollama, Storage)
2. Resources (Database, LLM, FileStorage)
3. Tools (Memory, LLM generation, File operations)
4. Plugins (Use tools to implement behavior)
"""

from .layer_explorer import LayerExplorerExample

__all__ = ["LayerExplorerExample"]