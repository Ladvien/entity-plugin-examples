"""User preferences memory pattern - Learn and adapt to user needs."""

from .preference_learner import PreferenceLearnerPlugin
from .style_adapter import StyleAdapterPlugin
from .topic_tracker import TopicTrackerPlugin

__all__ = [
    "PreferenceLearnerPlugin",
    "StyleAdapterPlugin",
    "TopicTrackerPlugin", 
]