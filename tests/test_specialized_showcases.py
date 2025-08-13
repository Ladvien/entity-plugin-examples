"""Test the specialized domain-specific plugin showcases."""

import pytest
from unittest.mock import Mock, AsyncMock


def test_specialized_imports():
    """Test that all specialized examples can be imported."""
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, StaticAnalysisPlugin, CodeMetricsPlugin, SecurityScanPlugin,
        ResearchAssistantExample, SourceGathererPlugin, FactCheckerPlugin, SynthesizerPlugin,
        CustomerServiceExample, IntentClassifierPlugin, KnowledgeBasePlugin, ResponseGeneratorPlugin
    )
    
    # Code Reviewer
    assert CodeReviewerExample is not None
    assert StaticAnalysisPlugin is not None
    assert CodeMetricsPlugin is not None
    assert SecurityScanPlugin is not None
    
    # Research Assistant
    assert ResearchAssistantExample is not None
    assert SourceGathererPlugin is not None
    assert FactCheckerPlugin is not None
    assert SynthesizerPlugin is not None
    
    # Customer Service
    assert CustomerServiceExample is not None
    assert IntentClassifierPlugin is not None
    assert KnowledgeBasePlugin is not None
    assert ResponseGeneratorPlugin is not None


def test_story_9_directory_structure():
    """Test Story 9: Directory structure matches requirements."""
    import os
    
    base_path = "/Users/ladvien/entity/plugins/examples/src/entity_plugin_examples/specialized"
    
    # Check required subdirectories exist
    assert os.path.exists(os.path.join(base_path, "code_reviewer"))
    assert os.path.exists(os.path.join(base_path, "research_assistant"))
    assert os.path.exists(os.path.join(base_path, "customer_service"))
    
    # Check each has __init__.py
    assert os.path.exists(os.path.join(base_path, "code_reviewer", "__init__.py"))
    assert os.path.exists(os.path.join(base_path, "research_assistant", "__init__.py"))
    assert os.path.exists(os.path.join(base_path, "customer_service", "__init__.py"))
    
    # Check each has main implementation file
    assert os.path.exists(os.path.join(base_path, "code_reviewer", "code_reviewer.py"))
    assert os.path.exists(os.path.join(base_path, "research_assistant", "research_assistant.py"))
    assert os.path.exists(os.path.join(base_path, "customer_service", "customer_service.py"))


def test_story_9_complete_working_systems():
    """Test Story 9: Each showcase is a complete working system."""
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    # Each should have async run method
    assert hasattr(CodeReviewerExample, 'run')
    assert callable(CodeReviewerExample.run)
    
    assert hasattr(ResearchAssistantExample, 'run')
    assert callable(ResearchAssistantExample.run)
    
    assert hasattr(CustomerServiceExample, 'run')
    assert callable(CustomerServiceExample.run)
    
    # Check they're coroutine functions (async)
    import inspect
    assert inspect.iscoroutinefunction(CodeReviewerExample.run)
    assert inspect.iscoroutinefunction(ResearchAssistantExample.run)
    assert inspect.iscoroutinefunction(CustomerServiceExample.run)


def test_story_9_plugin_composition_focus():
    """Test Story 9: Focus on plugin composition, not individual plugins."""
    import inspect
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    # Check docstrings mention plugin composition
    examples = [CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample]
    
    for example in examples:
        docstring = example.run.__doc__ or ""
        assert "composition" in docstring.lower() or "plugin" in docstring.lower()
        assert "story 9" in docstring.lower()
        
        # Check for Agent = Resources + Workflow pattern
        source = inspect.getsource(example.run)
        assert "Agent(" in source
        assert "workflow" in source.lower()


def test_story_9_domain_specific_test_data():
    """Test Story 9: Include domain-specific test data."""
    import inspect
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    # Check for domain-specific test data in source code
    examples = {
        CodeReviewerExample: ["test_code", "def ", "password", "admin123"],
        ResearchAssistantExample: ["research_queries", "artificial intelligence", "Climate change"],
        CustomerServiceExample: ["customer_messages", "refund", "billing", "order #"]
    }
    
    for example, expected_data in examples.items():
        source = inspect.getsource(example.run)
        for data_item in expected_data:
            assert data_item in source, f"{example.__name__} missing domain-specific data: {data_item}"


def test_code_reviewer_plugins():
    """Test Code Reviewer plugin composition."""
    from entity_plugin_examples.specialized.code_reviewer import (
        StaticAnalysisPlugin, CodeMetricsPlugin, SecurityScanPlugin
    )
    
    # Test plugin stages
    static_plugin = StaticAnalysisPlugin({})
    assert "parse" in [stage.lower() for stage in static_plugin.supported_stages]
    
    metrics_plugin = CodeMetricsPlugin({})
    assert "think" in [stage.lower() for stage in metrics_plugin.supported_stages]
    
    security_plugin = SecurityScanPlugin({})
    assert "review" in [stage.lower() for stage in security_plugin.supported_stages]


def test_research_assistant_plugins():
    """Test Research Assistant plugin composition."""
    from entity_plugin_examples.specialized.research_assistant import (
        SourceGathererPlugin, FactCheckerPlugin, SynthesizerPlugin
    )
    
    # Test plugin stages
    sources_plugin = SourceGathererPlugin({})
    assert "parse" in [stage.lower() for stage in sources_plugin.supported_stages]
    
    fact_plugin = FactCheckerPlugin({})
    assert "think" in [stage.lower() for stage in fact_plugin.supported_stages]
    
    synthesis_plugin = SynthesizerPlugin({})
    assert "do" in [stage.lower() for stage in synthesis_plugin.supported_stages]


def test_customer_service_plugins():
    """Test Customer Service plugin composition."""
    from entity_plugin_examples.specialized.customer_service import (
        IntentClassifierPlugin, KnowledgeBasePlugin, ResponseGeneratorPlugin
    )
    
    # Test plugin stages
    intent_plugin = IntentClassifierPlugin({})
    assert "parse" in [stage.lower() for stage in intent_plugin.supported_stages]
    
    kb_plugin = KnowledgeBasePlugin({})
    assert "think" in [stage.lower() for stage in kb_plugin.supported_stages]
    
    response_plugin = ResponseGeneratorPlugin({})
    assert "output" in [stage.lower() for stage in response_plugin.supported_stages]


@pytest.mark.asyncio
async def test_code_reviewer_execution():
    """Test Code Reviewer plugin execution."""
    from entity_plugin_examples.specialized.code_reviewer import StaticAnalysisPlugin
    
    # Create mock context
    context = Mock()
    context.message = '''
def authenticate_user(username, password):
    if password == "admin123":
        return True
'''
    context.remember = AsyncMock()
    
    plugin = StaticAnalysisPlugin({})
    result = await plugin._execute_impl(context)
    
    assert "analysis" in result.lower()
    context.remember.assert_called_once()


@pytest.mark.asyncio
async def test_research_assistant_execution():
    """Test Research Assistant plugin execution."""
    from entity_plugin_examples.specialized.research_assistant import SourceGathererPlugin
    
    # Create mock context
    context = Mock()
    context.message = "Latest research on artificial intelligence safety"
    context.remember = AsyncMock()
    
    plugin = SourceGathererPlugin({})
    result = await plugin._execute_impl(context)
    
    assert "sources" in result.lower()
    context.remember.assert_called_once()


@pytest.mark.asyncio
async def test_customer_service_execution():
    """Test Customer Service plugin execution."""
    from entity_plugin_examples.specialized.customer_service import IntentClassifierPlugin
    
    # Create mock context
    context = Mock()
    context.message = "I need a refund for order #12345"
    context.remember = AsyncMock()
    
    plugin = IntentClassifierPlugin({})
    result = await plugin._execute_impl(context)
    
    assert "intent" in result.lower()
    context.remember.assert_called_once()


def test_agent_equation_in_specialized():
    """Test that specialized examples show Agent = Resources + Workflow."""
    import entity_plugin_examples.specialized.code_reviewer.code_reviewer as code_rev
    import entity_plugin_examples.specialized.research_assistant.research_assistant as research
    import entity_plugin_examples.specialized.customer_service.customer_service as service
    
    # Each module should document the equation
    for module in [code_rev, research, service]:
        assert module.__doc__ is not None
        assert "Agent = Resources + Workflow" in module.__doc__


def test_80_20_principle_in_specialized():
    """Test that specialized examples follow 80% code, 20% explanation."""
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    examples = [CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample]
    
    for example in examples:
        docstring = example.run.__doc__ or ""
        # Should mention the 80/20 principle
        assert "80%" in docstring and "20%" in docstring


def test_specialized_memory_operations():
    """Test that specialized plugins use memory operations correctly."""
    from entity_plugin_examples.specialized.code_reviewer import StaticAnalysisPlugin
    from entity_plugin_examples.specialized.research_assistant import SourceGathererPlugin
    from entity_plugin_examples.specialized.customer_service import IntentClassifierPlugin
    
    import inspect
    
    plugins = [StaticAnalysisPlugin, SourceGathererPlugin, IntentClassifierPlugin]
    
    for plugin_class in plugins:
        # Check that _execute_impl uses context.remember
        source = inspect.getsource(plugin_class._execute_impl)
        assert "context.remember" in source or "remember(" in source


def test_specialized_showcase_completeness():
    """Test that each specialized showcase demonstrates complete workflow."""
    import inspect
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    examples = [CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample]
    
    for example in examples:
        source = inspect.getsource(example.run)
        
        # Should create workflow with multiple stages
        assert "Workflow(" in source
        assert "steps=" in source
        
        # Should show results from plugin composition
        assert "context" in source or "recall" in source
        
        # Should have demo output
        assert "print(" in source


def test_specialized_examples_next_steps():
    """Test that specialized examples provide next steps guidance."""
    import inspect
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    examples = [CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample]
    
    for example in examples:
        source = inspect.getsource(example.run)
        
        # Should mention other specialized examples
        next_step_indicators = ["next:", "try", "code_reviewer", "research_assistant", "customer_service"]
        has_next_steps = any(indicator in source.lower() for indicator in next_step_indicators)
        
        assert has_next_steps, f"{example.__name__} should provide next steps guidance"


def test_specialized_domain_focus():
    """Test that each specialized example focuses on its domain."""
    from entity_plugin_examples.specialized import (
        CodeReviewerExample, ResearchAssistantExample, CustomerServiceExample
    )
    
    # Test domain-specific focus in docstrings and source
    domain_tests = [
        (CodeReviewerExample, ["code", "review", "analysis", "security", "static"]),
        (ResearchAssistantExample, ["research", "source", "fact", "synthesis", "academic"]),
        (CustomerServiceExample, ["customer", "service", "intent", "knowledge", "support"])
    ]
    
    import inspect
    
    for example, expected_terms in domain_tests:
        docstring = (example.__doc__ or "").lower()
        source = inspect.getsource(example).lower()
        
        # Should contain domain-specific terminology
        for term in expected_terms[:2]:  # Check at least 2 terms
            assert term in docstring or term in source, f"{example.__name__} missing domain term: {term}"