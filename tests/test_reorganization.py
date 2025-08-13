"""Test that the reorganization worked correctly."""

import pytest


def test_main_imports():
    """Test that all plugins can still be imported from main package."""
    from entity_plugin_examples import (
        CalculatorPlugin,
        InputReaderPlugin,
        KeywordExtractorPlugin,
        OutputFormatterPlugin,
        ReasonGeneratorPlugin,
        StaticReviewerPlugin,
        TypedExamplePlugin,
    )
    
    # Verify all expected classes exist
    assert CalculatorPlugin is not None
    assert InputReaderPlugin is not None
    assert KeywordExtractorPlugin is not None
    assert OutputFormatterPlugin is not None
    assert ReasonGeneratorPlugin is not None
    assert StaticReviewerPlugin is not None
    assert TypedExamplePlugin is not None


def test_core_imports():
    """Test that core plugins can be imported from core subdirectory."""
    from entity_plugin_examples.core import InputReaderPlugin, TypedExamplePlugin
    
    assert InputReaderPlugin is not None
    assert TypedExamplePlugin is not None


def test_tools_imports():
    """Test that tool plugins can be imported from tools subdirectory."""
    from entity_plugin_examples.tools import CalculatorPlugin, OutputFormatterPlugin
    
    assert CalculatorPlugin is not None
    assert OutputFormatterPlugin is not None


def test_memory_imports():
    """Test that memory plugins can be imported from memory subdirectory."""
    from entity_plugin_examples.memory import (
        KeywordExtractorPlugin,
        ReasonGeneratorPlugin,
    )
    
    assert KeywordExtractorPlugin is not None
    assert ReasonGeneratorPlugin is not None


def test_patterns_imports():
    """Test that pattern plugins can be imported from patterns subdirectory."""
    from entity_plugin_examples.patterns import StaticReviewerPlugin
    
    assert StaticReviewerPlugin is not None


def test_specialized_imports():
    """Test that specialized module exists even if empty."""
    import entity_plugin_examples.specialized
    
    # Should be importable but empty for now
    assert entity_plugin_examples.specialized.__all__ == []


def test_plugin_functionality():
    """Test that plugins still work after reorganization."""
    from entity_plugin_examples.tools import CalculatorPlugin
    from unittest.mock import Mock
    
    # Create a mock context
    context = Mock()
    context.message = "2 + 3"
    
    # Create plugin and test it works
    plugin = CalculatorPlugin({}, {})
    
    # This should work without errors (basic instantiation test)
    assert plugin.supported_stages is not None
    assert hasattr(plugin, '_execute_impl')


def test_backward_compatibility():
    """Test that old import patterns still work for backward compatibility."""
    # These should all work the same as before reorganization
    from entity_plugin_examples import (
        CalculatorPlugin,
        InputReaderPlugin,
        KeywordExtractorPlugin,
        OutputFormatterPlugin,
        ReasonGeneratorPlugin,
        StaticReviewerPlugin,
        TypedExamplePlugin,
    )
    
    # Verify __all__ is properly defined
    import entity_plugin_examples
    assert len(entity_plugin_examples.__all__) == 7
    assert all(name in entity_plugin_examples.__all__ for name in [
        "CalculatorPlugin",
        "InputReaderPlugin", 
        "KeywordExtractorPlugin",
        "OutputFormatterPlugin",
        "ReasonGeneratorPlugin",
        "StaticReviewerPlugin",
        "TypedExamplePlugin",
    ])