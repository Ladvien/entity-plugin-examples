"""Pattern examples showing architectural approaches."""

from .static_reviewer import StaticReviewer as StaticReviewerPlugin
from .constructor_injection import ConstructorInjectionPlugin
from .dual_interface import DualInterfacePlugin
from .multi_stage_plugin import MultiStageAnalyticsPlugin
from .environment_substitution import EnvironmentSubstitutionPlugin

__all__ = [
    "StaticReviewerPlugin",
    "ConstructorInjectionPlugin", 
    "DualInterfacePlugin",
    "MultiStageAnalyticsPlugin",
    "EnvironmentSubstitutionPlugin",
]