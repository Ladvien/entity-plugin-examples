"""Test the progressive core examples."""

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock


def test_progressive_examples_imports():
    """Test that all progressive examples can be imported."""
    from entity_plugin_examples.core import (
        InstantAgentExample,
        PipelineVisualizerExample,
        LayerExplorerExample,
        WorkflowTemplatesExample,
        FirstPluginExample,
        MyFirstPlugin,
    )
    
    # Verify all example classes exist
    assert InstantAgentExample is not None
    assert PipelineVisualizerExample is not None
    assert LayerExplorerExample is not None
    assert WorkflowTemplatesExample is not None
    assert FirstPluginExample is not None
    assert MyFirstPlugin is not None


def test_instant_agent_structure():
    """Test Layer 0: InstantAgent has correct structure."""
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    
    # Should have a run method
    assert hasattr(InstantAgentExample, 'run')
    assert callable(InstantAgentExample.run)


def test_story_7_requirements():
    """Test Story 7: Simplify Getting Started Experience requirements."""
    import inspect
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    
    # Check that run method exists (3-line example)
    assert hasattr(InstantAgentExample, 'run')
    assert callable(InstantAgentExample.run)
    
    # Check method signature for async
    run_method = getattr(InstantAgentExample, 'run')
    assert inspect.iscoroutinefunction(run_method)
    
    # Check docstring mentions Story 7 requirements
    docstring = InstantAgentExample.run.__doc__ or ""
    assert "3-line" in docstring.lower() or "3 lines" in docstring.lower()
    
    # Check that demo method provides next steps
    assert hasattr(InstantAgentExample, 'demo')
    demo_docstring = InstantAgentExample.demo.__doc__ or ""
    assert "demo" in demo_docstring.lower() or "extended" in demo_docstring.lower()


def test_story_7_inline_comments():
    """Test that Story 7 shows output inline as comments."""
    import inspect
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    
    # Get source code of the run method
    source = inspect.getsource(InstantAgentExample.run)
    
    # Should contain inline comments showing expected output
    assert "# \"Hi! How can I help?\"" in source or "# This appears immediately" in source
    
    # Should show the 3-line pattern clearly
    assert "agent = Agent()" in source
    assert "await agent.chat(" in source


def test_story_7_zero_configuration():
    """Test that Story 7 requires no configuration files."""
    import inspect
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    
    # Get source code
    source = inspect.getsource(InstantAgentExample.run)
    
    # Should use Agent() without parameters (zero configuration)
    assert "Agent()" in source
    
    # Should not reference config files, settings, etc.
    forbidden_terms = ["config", "settings", "yaml", "json", "toml", ".env"]
    for term in forbidden_terms:
        assert term not in source.lower()


def test_story_7_next_steps_guidance():
    """Test that Story 7 provides clear next steps."""
    from entity_plugin_examples.core.instant_agent import InstantAgentExample
    import inspect
    
    # Check if there's guidance to next example
    source = inspect.getsource(InstantAgentExample)
    docstring = InstantAgentExample.__doc__ or ""
    
    # Should mention next steps or reference see_the_pipeline
    next_step_indicators = ["next", "see_the_pipeline", "pipeline", "step"]
    has_next_steps = any(indicator in source.lower() or indicator in docstring.lower() 
                        for indicator in next_step_indicators)
    
    assert has_next_steps, "Story 7 should provide clear next steps to second example"


def test_pipeline_visualizer_structure():
    """Test Layer 1: PipelineVisualizer has correct structure."""
    from entity_plugin_examples.core.see_the_pipeline import (
        PipelineVisualizerExample,
        VisibilityPlugin
    )
    
    # Should have example and plugin
    assert hasattr(PipelineVisualizerExample, 'run')
    assert hasattr(VisibilityPlugin, 'supported_stages')
    assert hasattr(VisibilityPlugin, '_execute_impl')


def test_layer_explorer_structure():
    """Test Layer 2: LayerExplorer has correct structure."""
    from entity_plugin_examples.core.see_the_layers import (
        LayerExplorerExample,
        ResourceExplorerPlugin
    )
    
    # Should have example and plugin
    assert hasattr(LayerExplorerExample, 'run')
    assert hasattr(ResourceExplorerPlugin, 'supported_stages')
    assert ResourceExplorerPlugin.supported_stages == ['think']


def test_workflow_templates_structure():
    """Test WorkflowTemplates has correct structure."""
    from entity_plugin_examples.core.workflow_templates import (
        WorkflowTemplatesExample,
        create_chat_workflow,
        create_tool_workflow,
        create_analysis_workflow,
    )
    
    # Should have example and workflow creators
    assert hasattr(WorkflowTemplatesExample, 'run')
    assert callable(create_chat_workflow)
    assert callable(create_tool_workflow)
    assert callable(create_analysis_workflow)


def test_first_plugin_structure():
    """Test FirstPlugin example has correct structure."""
    from entity_plugin_examples.core.first_plugin import (
        FirstPluginExample,
        MyFirstPlugin,
        PLUGIN_TEMPLATE
    )
    
    # Should have example, plugin, and template
    assert hasattr(FirstPluginExample, 'run')
    assert hasattr(MyFirstPlugin, 'supported_stages')
    assert MyFirstPlugin.supported_stages == ['think']
    assert hasattr(MyFirstPlugin, '_execute_impl')
    assert PLUGIN_TEMPLATE is not None
    assert "Plugin" in PLUGIN_TEMPLATE


def test_my_first_plugin_instantiation():
    """Test that MyFirstPlugin can be instantiated."""
    from entity_plugin_examples.core.first_plugin import MyFirstPlugin
    
    # Create mock resources
    resources = {
        "llm": Mock(),
        "memory": Mock(),
    }
    
    # Should instantiate without errors
    plugin = MyFirstPlugin(resources)
    assert plugin is not None
    assert plugin.supported_stages == ['think']


@pytest.mark.asyncio
async def test_my_first_plugin_execution():
    """Test that MyFirstPlugin executes correctly."""
    from entity_plugin_examples.core.first_plugin import MyFirstPlugin
    
    # Create mock context
    context = Mock()
    context.message = "Test message"
    context.get_resource = Mock(return_value=None)
    context.recall = AsyncMock(return_value=0)
    context.remember = AsyncMock()
    
    # Create and execute plugin
    plugin = MyFirstPlugin({})
    result = await plugin._execute_impl(context)
    
    # Should process message and track visit count
    assert "[Visit #1]" in result
    assert "Test message" in result
    context.recall.assert_called_once_with("visit_count", 0)
    context.remember.assert_called_once_with("visit_count", 1)


def test_visibility_plugin_stages():
    """Test VisibilityPlugin supports correct stages."""
    from entity_plugin_examples.core.see_the_pipeline import VisibilityPlugin
    
    # Test with different stage configs
    for stage in ["input", "parse", "think", "do", "review", "output"]:
        plugin = VisibilityPlugin({}, {"stage": stage})
        assert plugin.supported_stages == [stage]
        assert plugin.stage_name == stage


def test_resource_explorer_plugin():
    """Test ResourceExplorerPlugin structure."""
    from entity_plugin_examples.core.see_the_layers import ResourceExplorerPlugin
    
    plugin = ResourceExplorerPlugin({})
    assert plugin.supported_stages == ['think']
    assert hasattr(plugin, '_execute_impl')


def test_workflow_plugins():
    """Test workflow template plugins."""
    from entity_plugin_examples.core.workflow_templates import (
        ChatPlugin,
        ToolPlugin,
        AnalysisPlugin,
    )
    
    # Test ChatPlugin
    chat = ChatPlugin({})
    assert chat.supported_stages == ['think']
    
    # Test ToolPlugin
    tool = ToolPlugin({})
    assert tool.supported_stages == ['do']
    
    # Test AnalysisPlugin
    analysis = AnalysisPlugin({})
    assert 'parse' in analysis.supported_stages
    assert 'think' in analysis.supported_stages


def test_progressive_example_ordering():
    """Test that examples follow Layer 0 → 1 → 2 progression."""
    from entity_plugin_examples.core import (
        InstantAgentExample,  # Layer 0
        PipelineVisualizerExample,  # Layer 1
        LayerExplorerExample,  # Layer 2
    )
    
    # Each should exist and represent increasing complexity
    # Layer 0: Zero config
    assert InstantAgentExample.__doc__ and "zero configuration" in InstantAgentExample.__doc__.lower()
    
    # Layer 1: Pipeline visibility
    assert PipelineVisualizerExample.__doc__ and "pipeline" in PipelineVisualizerExample.__doc__.lower()
    
    # Layer 2: Resource layers
    assert LayerExplorerExample.__doc__ and "layer" in LayerExplorerExample.__doc__.lower()


def test_agent_equation_in_examples():
    """Test that each example shows Agent = Resources + Workflow."""
    import entity_plugin_examples.core.instant_agent.instant_agent as instant
    import entity_plugin_examples.core.see_the_pipeline.pipeline_visualizer as pipeline
    import entity_plugin_examples.core.see_the_layers.layer_explorer as layers
    import entity_plugin_examples.core.workflow_templates.workflow_templates as templates
    import entity_plugin_examples.core.first_plugin.first_plugin as first
    
    # Each module should document the equation
    for module in [instant, pipeline, layers, templates, first]:
        assert module.__doc__ is not None
        assert "Agent = Resources + Workflow" in module.__doc__


def test_code_first_approach():
    """Test that examples follow 80% code, 20% explanation approach."""
    from entity_plugin_examples.core.instant_agent import instant_agent
    from entity_plugin_examples.core.first_plugin import first_plugin
    
    # Check that code examples have minimal but present documentation
    for module in [instant_agent, first_plugin]:
        # Module should have code
        assert hasattr(module, '__file__')
        
        # Should have the 80/20 mention in docstrings
        content = module.__doc__ or ""
        example_class = getattr(module, [c for c in dir(module) if "Example" in c][0])
        if hasattr(example_class, 'run'):
            run_doc = example_class.run.__doc__ or ""
            # Should mention code-first approach
            assert "80%" in run_doc or "Code" in run_doc