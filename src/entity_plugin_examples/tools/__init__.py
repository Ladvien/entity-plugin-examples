"""Tool examples for DO stage plugins."""

# Import the original calculator from the .py file, not the directory
import importlib.util
import os
calculator_path = os.path.join(os.path.dirname(__file__), "calculator.py")
spec = importlib.util.spec_from_file_location("calculator", calculator_path)
calculator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calculator_module)
Calculator = calculator_module.Calculator

from .output_formatter import OutputFormatter as OutputFormatterPlugin

# Calculator tools
from .calculator.basic_calculator import BasicCalculatorPlugin
from .calculator.scientific_calculator import ScientificCalculatorPlugin  
from .calculator.expression_evaluator import ExpressionEvaluatorPlugin

# Web search tools
from .web_search.search_engine_plugin import SearchEnginePlugin
from .web_search.url_extractor import URLExtractorPlugin
from .web_search.web_scraper import WebScraperPlugin

# File operation tools
from .file_ops.file_manager import FileManagerPlugin
from .file_ops.text_processor import TextProcessorPlugin
from .file_ops.file_converter import FileConverterPlugin

# Data analysis tools
from .data_analysis.statistics_calculator import StatisticsCalculatorPlugin
from .data_analysis.data_validator import DataValidatorPlugin
from .data_analysis.chart_generator import ChartGeneratorPlugin

# Assign as CalculatorPlugin for backward compatibility
CalculatorPlugin = Calculator

__all__ = [
    "CalculatorPlugin",
    "OutputFormatterPlugin",
    # Calculator tools
    "BasicCalculatorPlugin",
    "ScientificCalculatorPlugin",
    "ExpressionEvaluatorPlugin",
    # Web search tools
    "SearchEnginePlugin", 
    "URLExtractorPlugin",
    "WebScraperPlugin",
    # File operation tools
    "FileManagerPlugin",
    "TextProcessorPlugin", 
    "FileConverterPlugin",
    # Data analysis tools
    "StatisticsCalculatorPlugin",
    "DataValidatorPlugin",
    "ChartGeneratorPlugin",
]