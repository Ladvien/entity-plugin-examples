"""Memory pattern library - Comprehensive patterns for memory-based plugins."""

# Legacy plugins
from .keyword_extractor import KeywordExtractor as KeywordExtractorPlugin
from .reason_generator import ReasonGenerator as ReasonGeneratorPlugin

# Conversation history patterns
from .conversation_history.conversation_tracker import ConversationTrackerPlugin
from .conversation_history.context_summarizer import ContextSummarizerPlugin
from .conversation_history.turn_counter import TurnCounterPlugin

# User preferences patterns
from .user_preferences.preference_learner import PreferenceLearnerPlugin
from .user_preferences.style_adapter import StyleAdapterPlugin
from .user_preferences.topic_tracker import TopicTrackerPlugin

# Skill tracking patterns
from .skill_tracking.skill_assessor import SkillAssessorPlugin
from .skill_tracking.progress_tracker import ProgressTrackerPlugin
from .skill_tracking.competency_mapper import CompetencyMapperPlugin

# Relationship building patterns
from .relationship_building.rapport_builder import RapportBuilderPlugin
from .relationship_building.personality_adapter import PersonalityAdapterPlugin
from .relationship_building.relationship_tracker import RelationshipTrackerPlugin

__all__ = [
    # Legacy plugins
    "KeywordExtractorPlugin", 
    "ReasonGeneratorPlugin",
    
    # Conversation history
    "ConversationTrackerPlugin",
    "ContextSummarizerPlugin", 
    "TurnCounterPlugin",
    
    # User preferences
    "PreferenceLearnerPlugin",
    "StyleAdapterPlugin",
    "TopicTrackerPlugin",
    
    # Skill tracking
    "SkillAssessorPlugin",
    "ProgressTrackerPlugin",
    "CompetencyMapperPlugin",
    
    # Relationship building
    "RapportBuilderPlugin",
    "PersonalityAdapterPlugin",
    "RelationshipTrackerPlugin",
]