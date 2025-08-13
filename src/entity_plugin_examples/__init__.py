"""Entity Plugin Examples - Example plugins for the Entity Framework.

This package contains example plugins organized by category:
- core/: Fundamental concepts and patterns
- tools/: DO stage plugins for specific tasks
- memory/: Memory and state management patterns
- patterns/: Architectural patterns and approaches
- specialized/: Domain-specific examples (future)
"""

# Import all plugins from their organized subdirectories
from .core import InputReaderPlugin, TypedExamplePlugin
from .memory import KeywordExtractorPlugin, ReasonGeneratorPlugin
from .patterns import StaticReviewerPlugin
from .tools import CalculatorPlugin, OutputFormatterPlugin

__all__ = [
    "CalculatorPlugin",
    "InputReaderPlugin",
    "KeywordExtractorPlugin",
    "OutputFormatterPlugin",
    "ReasonGeneratorPlugin",
    "StaticReviewerPlugin",
    "TypedExamplePlugin",
]

__version__ = "0.1.0"
