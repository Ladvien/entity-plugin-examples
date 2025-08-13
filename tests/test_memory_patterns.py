"""Basic tests for memory pattern library plugins."""

import pytest


def test_memory_patterns_import():
    """Test that all memory pattern plugins can be imported."""
    from entity_plugin_examples.memory import (
        ConversationTrackerPlugin,
        ContextSummarizerPlugin,
        TurnCounterPlugin,
        PreferenceLearnerPlugin,
        StyleAdapterPlugin,
        TopicTrackerPlugin,
        SkillAssessorPlugin,
        ProgressTrackerPlugin,
        CompetencyMapperPlugin,
        RapportBuilderPlugin,
        PersonalityAdapterPlugin,
        RelationshipTrackerPlugin,
    )
    
    # Verify all plugins exist
    assert ConversationTrackerPlugin is not None
    assert ContextSummarizerPlugin is not None
    assert TurnCounterPlugin is not None
    assert PreferenceLearnerPlugin is not None
    assert StyleAdapterPlugin is not None
    assert TopicTrackerPlugin is not None
    assert SkillAssessorPlugin is not None
    assert ProgressTrackerPlugin is not None
    assert CompetencyMapperPlugin is not None
    assert RapportBuilderPlugin is not None
    assert PersonalityAdapterPlugin is not None
    assert RelationshipTrackerPlugin is not None


def test_conversation_patterns_structure():
    """Test conversation history patterns have correct structure."""
    from unittest.mock import AsyncMock
    from entity_plugin_examples.memory import (
        ConversationTrackerPlugin,
        ContextSummarizerPlugin,
        TurnCounterPlugin,
    )
    
    # Mock resources for plugins that need them
    mock_llm = AsyncMock()
    resources_with_llm = {"llm": mock_llm}
    
    # Test ConversationTrackerPlugin
    plugin = ConversationTrackerPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test ContextSummarizerPlugin (needs LLM)
    plugin = ContextSummarizerPlugin(resources_with_llm)
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test TurnCounterPlugin
    plugin = TurnCounterPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')


def test_user_preferences_patterns_structure():
    """Test user preferences patterns have correct structure."""
    from unittest.mock import AsyncMock
    from entity_plugin_examples.memory import (
        PreferenceLearnerPlugin,
        StyleAdapterPlugin,
        TopicTrackerPlugin,
    )
    
    # Mock resources for plugins that need them
    mock_llm = AsyncMock()
    resources_with_llm = {"llm": mock_llm}
    
    # Test PreferenceLearnerPlugin
    plugin = PreferenceLearnerPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test StyleAdapterPlugin (needs LLM)
    plugin = StyleAdapterPlugin(resources_with_llm)
    assert hasattr(plugin, 'supported_stages') 
    assert hasattr(plugin, '_execute_impl')
    
    # Test TopicTrackerPlugin
    plugin = TopicTrackerPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')


def test_skill_tracking_patterns_structure():
    """Test skill tracking patterns have correct structure."""
    from entity_plugin_examples.memory import (
        SkillAssessorPlugin,
        ProgressTrackerPlugin,
        CompetencyMapperPlugin,
    )
    
    # Test SkillAssessorPlugin
    plugin = SkillAssessorPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test ProgressTrackerPlugin
    plugin = ProgressTrackerPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test CompetencyMapperPlugin
    plugin = CompetencyMapperPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')


def test_relationship_building_patterns_structure():
    """Test relationship building patterns have correct structure."""
    from entity_plugin_examples.memory import (
        RapportBuilderPlugin,
        PersonalityAdapterPlugin,
        RelationshipTrackerPlugin,
    )
    
    # Test RapportBuilderPlugin
    plugin = RapportBuilderPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test PersonalityAdapterPlugin
    plugin = PersonalityAdapterPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')
    
    # Test RelationshipTrackerPlugin
    plugin = RelationshipTrackerPlugin({})
    assert hasattr(plugin, 'supported_stages')
    assert hasattr(plugin, '_execute_impl')


def test_plugin_stage_assignments():
    """Test that plugins are assigned to appropriate workflow stages."""
    from unittest.mock import AsyncMock
    from entity_plugin_examples.memory import (
        ConversationTrackerPlugin,
        ContextSummarizerPlugin,
        TurnCounterPlugin,
        PreferenceLearnerPlugin,
        StyleAdapterPlugin,
        TopicTrackerPlugin,
        SkillAssessorPlugin,
        ProgressTrackerPlugin,
        CompetencyMapperPlugin,
        RapportBuilderPlugin,
        PersonalityAdapterPlugin,
        RelationshipTrackerPlugin,
    )
    from entity.workflow.stages import INPUT, PARSE, THINK, DO, REVIEW, OUTPUT
    
    # Test stage assignments are valid
    all_stages = [INPUT, PARSE, THINK, DO, REVIEW, OUTPUT]
    
    # Mock resources for plugins that need them
    mock_llm = AsyncMock()
    resources_with_llm = {"llm": mock_llm}
    
    plugins = [
        ConversationTrackerPlugin({}),
        ContextSummarizerPlugin(resources_with_llm),  # needs LLM
        TurnCounterPlugin({}),
        PreferenceLearnerPlugin({}),
        StyleAdapterPlugin(resources_with_llm),  # needs LLM
        TopicTrackerPlugin({}),
        SkillAssessorPlugin({}),
        ProgressTrackerPlugin({}),
        CompetencyMapperPlugin({}),
        RapportBuilderPlugin({}),
        PersonalityAdapterPlugin({}),
        RelationshipTrackerPlugin({}),
    ]
    
    for plugin in plugins:
        assert hasattr(plugin, 'supported_stages')
        assert isinstance(plugin.supported_stages, list)
        assert len(plugin.supported_stages) > 0
        
        # Each supported stage should be a valid stage
        for stage in plugin.supported_stages:
            assert stage in all_stages


if __name__ == "__main__":
    pytest.main([__file__, "-v"])