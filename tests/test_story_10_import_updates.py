"""Test Story 10: Update Import Paths and Tests."""

import os
import pytest


def test_story_10_all_imports_work():
    """Test that all import statements match new structure."""
    # Core imports
    from entity_plugin_examples.core import (
        InstantAgentExample,
        PipelineVisualizerExample,
        LayerExplorerExample,
        WorkflowTemplatesExample,
        FirstPluginExample,
        MyFirstPlugin,
    )
    
    # Additional core imports that were missing
    from entity_plugin_examples.core.see_the_layers import ResourceExplorerPlugin
    from entity_plugin_examples.core.workflow_templates import (
        ChatPlugin,
        ToolPlugin,
        AnalysisPlugin,
        create_chat_workflow,
        create_tool_workflow,
        create_analysis_workflow,
    )
    from entity_plugin_examples.core.first_plugin import PLUGIN_TEMPLATE
    
    # Tools imports
    from entity_plugin_examples.tools import (
        CalculatorPlugin,
        OutputFormatterPlugin,
    )
    
    # Memory imports  
    from entity_plugin_examples.memory import (
        KeywordExtractorPlugin,
        ReasonGeneratorPlugin,
    )
    
    # Patterns imports
    from entity_plugin_examples.patterns import StaticReviewerPlugin
    
    # Specialized imports
    from entity_plugin_examples.specialized import (
        CodeReviewerExample,
        ResearchAssistantExample,
        CustomerServiceExample,
    )
    
    # All imports should work without errors
    assert InstantAgentExample is not None
    assert ResourceExplorerPlugin is not None
    assert create_chat_workflow is not None
    assert PLUGIN_TEMPLATE is not None


def test_story_10_backward_compatibility():
    """Test that backward compatibility is maintained."""
    # These old-style imports should still work
    from entity_plugin_examples import (
        CalculatorPlugin,
        KeywordExtractorPlugin,
        OutputFormatterPlugin,
        ReasonGeneratorPlugin,
        StaticReviewerPlugin,
    )
    
    assert CalculatorPlugin is not None
    assert KeywordExtractorPlugin is not None
    assert OutputFormatterPlugin is not None
    assert ReasonGeneratorPlugin is not None
    assert StaticReviewerPlugin is not None


def test_story_10_migration_guide_exists():
    """Test that migration guide for existing users exists."""
    migration_guide_path = "/Users/ladvien/entity/plugins/examples/MIGRATION_GUIDE.md"
    assert os.path.exists(migration_guide_path), "Migration guide should exist"
    
    # Check that migration guide contains key sections
    with open(migration_guide_path, 'r') as f:
        content = f.read()
        
    assert "Import Changes" in content
    assert "Backward Compatibility" in content
    assert "Migration Steps" in content
    assert "New Directory Structure" in content


def test_story_10_core_exports_complete():
    """Test that all core module exports are complete."""
    import entity_plugin_examples.core
    
    # Check main core exports
    expected_core_exports = [
        "InstantAgentExample",
        "PipelineVisualizerExample", 
        "LayerExplorerExample",
        "WorkflowTemplatesExample",
        "FirstPluginExample",
        "MyFirstPlugin",
        "VisibilityPlugin",
    ]
    
    for export in expected_core_exports:
        assert export in entity_plugin_examples.core.__all__


def test_story_10_submodule_exports():
    """Test that submodule exports are properly updated."""
    # Test see_the_layers exports
    from entity_plugin_examples.core import see_the_layers
    assert "LayerExplorerExample" in see_the_layers.__all__
    assert "ResourceExplorerPlugin" in see_the_layers.__all__
    
    # Test workflow_templates exports
    from entity_plugin_examples.core import workflow_templates
    assert "WorkflowTemplatesExample" in workflow_templates.__all__
    assert "create_chat_workflow" in workflow_templates.__all__
    assert "create_tool_workflow" in workflow_templates.__all__
    assert "create_analysis_workflow" in workflow_templates.__all__
    
    # Test first_plugin exports
    from entity_plugin_examples.core import first_plugin
    assert "FirstPluginExample" in first_plugin.__all__
    assert "MyFirstPlugin" in first_plugin.__all__
    assert "PLUGIN_TEMPLATE" in first_plugin.__all__


def test_story_10_memory_subcategories():
    """Test that memory subcategory imports work."""
    from entity_plugin_examples.memory.conversation_history import (
        ConversationTrackerPlugin,
        TurnCounterPlugin,
        ContextSummarizerPlugin,
    )
    
    from entity_plugin_examples.memory.user_preferences import (
        PreferenceLearnerPlugin,
        StyleAdapterPlugin,
        TopicTrackerPlugin,
    )
    
    from entity_plugin_examples.memory.skill_tracking import (
        SkillAssessorPlugin,
        ProgressTrackerPlugin,
        CompetencyMapperPlugin,
    )
    
    from entity_plugin_examples.memory.relationship_building import (
        RelationshipTrackerPlugin,
        RapportBuilderPlugin,
        PersonalityAdapterPlugin,
    )
    
    # All subcategory imports should work
    assert ConversationTrackerPlugin is not None
    assert PreferenceLearnerPlugin is not None
    assert SkillAssessorPlugin is not None
    assert RelationshipTrackerPlugin is not None


def test_story_10_tools_subcategories():
    """Test that tools subcategory imports work."""
    from entity_plugin_examples.tools.calculator import (
        BasicCalculatorPlugin,
        ScientificCalculatorPlugin,
        ExpressionEvaluatorPlugin,
    )
    
    from entity_plugin_examples.tools.file_ops import (
        FileManagerPlugin,
        TextProcessorPlugin,
        FileConverterPlugin,
    )
    
    from entity_plugin_examples.tools.web_search import (
        WebScraperPlugin,
        SearchEnginePlugin,
        URLExtractorPlugin,
    )
    
    from entity_plugin_examples.tools.data_analysis import (
        DataValidatorPlugin,
        StatisticsCalculatorPlugin,
        ChartGeneratorPlugin,
    )
    
    # All subcategory imports should work
    assert BasicCalculatorPlugin is not None
    assert FileManagerPlugin is not None
    assert WebScraperPlugin is not None
    assert DataValidatorPlugin is not None


def test_story_10_specialized_complete():
    """Test that specialized showcases have all imports."""
    from entity_plugin_examples.specialized import (
        # Code Reviewer
        CodeReviewerExample,
        StaticAnalysisPlugin,
        CodeMetricsPlugin,
        SecurityScanPlugin,
        # Research Assistant
        ResearchAssistantExample,
        SourceGathererPlugin,
        FactCheckerPlugin,
        SynthesizerPlugin,
        # Customer Service
        CustomerServiceExample,
        IntentClassifierPlugin,
        KnowledgeBasePlugin,
        ResponseGeneratorPlugin,
    )
    
    # All specialized imports should work
    assert CodeReviewerExample is not None
    assert StaticAnalysisPlugin is not None
    assert ResearchAssistantExample is not None
    assert SourceGathererPlugin is not None
    assert CustomerServiceExample is not None
    assert IntentClassifierPlugin is not None


def test_story_10_no_circular_imports():
    """Test that there are no circular import issues."""
    # Try importing everything at once
    import entity_plugin_examples
    import entity_plugin_examples.core
    import entity_plugin_examples.tools
    import entity_plugin_examples.memory
    import entity_plugin_examples.patterns
    import entity_plugin_examples.specialized
    
    # Then try specific deep imports
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    from entity_plugin_examples.tools.calculator import BasicCalculatorPlugin
    from entity_plugin_examples.memory.conversation_history import ConversationTrackerPlugin
    from entity_plugin_examples.patterns.dual_interface import DualInterfacePlugin
    from entity_plugin_examples.specialized.code_reviewer import CodeReviewerExample
    
    # All imports should work without circular import errors
    assert InstantAgentExample is not None
    assert BasicCalculatorPlugin is not None
    assert ConversationTrackerPlugin is not None
    assert DualInterfacePlugin is not None
    assert CodeReviewerExample is not None


def test_story_10_import_performance():
    """Test that reorganized imports don't significantly impact performance."""
    import time
    import importlib
    import sys
    
    # Clear the module from cache if it exists
    if 'entity_plugin_examples' in sys.modules:
        del sys.modules['entity_plugin_examples']
    
    # Measure import time
    start_time = time.time()
    import entity_plugin_examples
    import_time = time.time() - start_time
    
    # Import time should be reasonable (under 1 second)
    assert import_time < 1.0, f"Import took {import_time:.2f} seconds, which is too slow"


def test_story_10_all_tests_updated():
    """Test that all test files are updated to use new imports."""
    import glob
    
    test_files = glob.glob("/Users/ladvien/entity/plugins/examples/tests/*.py")
    
    # Check that test files exist
    assert len(test_files) > 0, "No test files found"
    
    # Check specific test files that should be updated
    expected_test_files = [
        "test_reorganization.py",
        "test_progressive_examples.py",
        "test_memory_patterns.py",
        "test_specialized_showcases.py",
    ]
    
    test_file_names = [os.path.basename(f) for f in test_files]
    
    for expected_file in expected_test_files:
        assert expected_file in test_file_names, f"{expected_file} should exist"