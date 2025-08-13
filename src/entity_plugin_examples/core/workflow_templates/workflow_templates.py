"""Workflow Templates - Named workflows for different agent types.

Agent = Resources + Workflow
      = defaults() + [ChatWorkflow | ToolWorkflow | AnalysisWorkflow]
"""

from typing import Any, Dict

from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import DO, INPUT, OUTPUT, PARSE, REVIEW, THINK
from entity.workflow.workflow import Workflow


class ChatPlugin(Plugin):
    """Plugin optimized for conversational interactions."""
    supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        message = context.message or ""
        # Remember conversation context
        history = await context.recall("chat_history", [])
        history.append({"user": message})
        await context.remember("chat_history", history)
        return f"Chat response to: {message}"


class ToolPlugin(Plugin):
    """Plugin optimized for tool execution."""
    supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        message = context.message or ""
        # Execute tool-like operations
        if "calculate" in message.lower():
            return "Calculation performed"
        elif "search" in message.lower():
            return "Search completed"
        return f"Tool executed for: {message}"


class AnalysisPlugin(Plugin):
    """Plugin optimized for data analysis."""
    supported_stages = [PARSE, THINK]
    
    async def _execute_impl(self, context) -> str:
        message = context.message or ""
        
        if context.current_stage == PARSE:
            # Extract data points
            await context.remember("data_points", message.split())
            return message
        
        elif context.current_stage == THINK:
            # Analyze extracted data
            data = await context.recall("data_points", [])
            return f"Analysis of {len(data)} data points complete"
        
        return message


def create_chat_workflow(resources: Dict[str, Any]) -> Workflow:
    """Create workflow optimized for conversations.
    
    Emphasizes THINK stage for context-aware responses.
    """
    return Workflow(
        steps={
            THINK: [ChatPlugin(resources)],
        }
    )


def create_tool_workflow(resources: Dict[str, Any]) -> Workflow:
    """Create workflow optimized for tool execution.
    
    Emphasizes DO stage for action execution.
    """
    return Workflow(
        steps={
            DO: [ToolPlugin(resources)],
        }
    )


def create_analysis_workflow(resources: Dict[str, Any]) -> Workflow:
    """Create workflow optimized for data analysis.
    
    Uses PARSE for extraction and THINK for analysis.
    """
    plugin = AnalysisPlugin(resources)
    return Workflow(
        steps={
            PARSE: [plugin],
            THINK: [plugin],
        }
    )


class WorkflowTemplatesExample:
    """Demonstrate using named workflow templates."""
    
    @staticmethod
    async def run():
        """Create agents with different workflow templates.
        
        80% Code showing workflow templates:
        - Chat agent for conversations
        - Tool agent for task execution
        - Analysis agent for data processing
        """
        resources = load_defaults()
        
        print("🎭 Creating agents with different workflows:")
        print("=" * 50)
        
        # Chat Agent = Resources + ChatWorkflow
        chat_agent = Agent(
            resources=resources,
            workflow=create_chat_workflow(resources)
        )
        response = await chat_agent.chat("Hello! How are you?")
        print(f"Chat Agent: {response}")
        
        # Tool Agent = Resources + ToolWorkflow
        tool_agent = Agent(
            resources=resources,
            workflow=create_tool_workflow(resources)
        )
        response = await tool_agent.chat("Calculate the sum")
        print(f"Tool Agent: {response}")
        
        # Analysis Agent = Resources + AnalysisWorkflow
        analysis_agent = Agent(
            resources=resources,
            workflow=create_analysis_workflow(resources)
        )
        response = await analysis_agent.chat("data1 data2 data3")
        print(f"Analysis Agent: {response}")
        
        print("=" * 50)
        print("\n✨ Three different agents, three different workflows!")
        
        return {
            "chat": chat_agent,
            "tool": tool_agent,
            "analysis": analysis_agent
        }


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Workflow Templates")
        print("=" * 40)
        agents = await WorkflowTemplatesExample.run()
        print(f"\n✅ Created {len(agents)} specialized agents!")
    
    asyncio.run(main())