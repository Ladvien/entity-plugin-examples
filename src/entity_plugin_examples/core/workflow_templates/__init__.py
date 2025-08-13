"""Workflow Templates - Pre-built workflows for common patterns.

Shows how to create and use named workflow templates:
- ChatWorkflow: Conversational agent
- ToolWorkflow: Task execution agent
- AnalysisWorkflow: Data analysis agent
"""

from .workflow_templates import (
    WorkflowTemplatesExample,
    ChatPlugin,
    ToolPlugin,
    AnalysisPlugin,
    create_chat_workflow,
    create_tool_workflow,
    create_analysis_workflow
)

__all__ = [
    "WorkflowTemplatesExample",
    "ChatPlugin",
    "ToolPlugin", 
    "AnalysisPlugin",
    "create_chat_workflow",
    "create_tool_workflow",
    "create_analysis_workflow"
]