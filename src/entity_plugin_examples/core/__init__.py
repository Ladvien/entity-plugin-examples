"""Core examples demonstrating fundamental Entity Framework concepts.

Progressive examples following Layer 0 → 1 → 2 progression:
- instant_agent/: Layer 0 - Zero config instant agent
- see_the_pipeline/: Layer 1 - Visualize 6-stage pipeline
- see_the_layers/: Layer 2 - Explore 4-layer resources
- workflow_templates/: Named workflows for different use cases
- first_plugin/: Create your first custom plugin
"""

from .first_plugin import FirstPluginExample, MyFirstPlugin
from .input_reader import InputReader as InputReaderPlugin
from .instant_agent import InstantAgentExample
from .see_the_layers import LayerExplorerExample
from .see_the_pipeline import PipelineVisualizerExample
from .typed_example_plugin import TypedExamplePlugin
from .workflow_templates import WorkflowTemplatesExample

__all__ = [
    # Original plugins
    "InputReaderPlugin",
    "TypedExamplePlugin",
    # Progressive examples (Layer 0 → 1 → 2)
    "InstantAgentExample",
    "PipelineVisualizerExample", 
    "LayerExplorerExample",
    "WorkflowTemplatesExample",
    "FirstPluginExample",
    "MyFirstPlugin",
]