"""Specialized examples for domain-specific use cases."""

from .code_reviewer import CodeReviewerExample, StaticAnalysisPlugin, CodeMetricsPlugin, SecurityScanPlugin
from .research_assistant import ResearchAssistantExample, SourceGathererPlugin, FactCheckerPlugin, SynthesizerPlugin
from .customer_service import CustomerServiceExample, IntentClassifierPlugin, KnowledgeBasePlugin, ResponseGeneratorPlugin

__all__ = [
    # Code Reviewer
    "CodeReviewerExample", "StaticAnalysisPlugin", "CodeMetricsPlugin", "SecurityScanPlugin",
    # Research Assistant  
    "ResearchAssistantExample", "SourceGathererPlugin", "FactCheckerPlugin", "SynthesizerPlugin",
    # Customer Service
    "CustomerServiceExample", "IntentClassifierPlugin", "KnowledgeBasePlugin", "ResponseGeneratorPlugin"
]