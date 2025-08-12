"""Entity Plugin Examples - Example plugins for the Entity Framework.

This package contains example plugins demonstrating various Entity Framework features.
"""

# Import all plugins from their modules
from .calculator import Calculator as CalculatorPlugin
from .input_reader import InputReader as InputReaderPlugin
from .keyword_extractor import KeywordExtractor as KeywordExtractorPlugin
from .output_formatter import OutputFormatter as OutputFormatterPlugin
from .reason_generator import ReasonGenerator as ReasonGeneratorPlugin
from .static_reviewer import StaticReviewer as StaticReviewerPlugin
from .typed_example_plugin import TypedExamplePlugin

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
