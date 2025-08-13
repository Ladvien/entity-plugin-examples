"""First Plugin - Minimal plugin creation example.

Agent = Resources + Workflow
      = defaults() + Workflow([YourPlugin])
"""

from typing import Any, Dict

from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import THINK
from entity.workflow.workflow import Workflow


class MyFirstPlugin(Plugin):
    """Your first custom plugin - minimal but complete.
    
    Every plugin needs:
    1. Inherit from Plugin
    2. Define supported_stages
    3. Implement _execute_impl()
    """
    
    # Step 1: Declare which stages this plugin supports
    supported_stages = [THINK]
    
    # Step 2: Implement the execution logic
    async def _execute_impl(self, context) -> str:
        """Process the message and return a result.
        
        Args:
            context: Contains message, resources, and state methods
            
        Returns:
            The processed message to pass to next stage
        """
        # Get the incoming message
        message = context.message or ""
        
        # Access resources if needed
        llm = context.get_resource("llm")
        
        # Use memory to store/recall state
        counter = await context.recall("visit_count", 0)
        await context.remember("visit_count", counter + 1)
        
        # Process the message (your custom logic here)
        result = f"[Visit #{counter + 1}] Processed: {message}"
        
        # Return the result for next stage
        return result


class FirstPluginExample:
    """Learn to create and use your first plugin."""
    
    @staticmethod
    async def run():
        """Create an agent with your custom plugin.
        
        80% Code showing plugin creation:
        - Minimal plugin structure
        - How to add it to a workflow
        - How to create an agent with it
        """
        # Get default resources
        resources = load_defaults()
        
        # Create workflow with your plugin
        workflow = Workflow(
            steps={
                THINK: [MyFirstPlugin(resources)],
            }
        )
        
        # Agent = Resources + Workflow(YourPlugin)
        agent = Agent(resources=resources, workflow=workflow)
        
        print("🎉 Using your first custom plugin:")
        print("=" * 50)
        
        # Test the plugin
        response = await agent.chat("Hello from my plugin!")
        print(f"Response: {response}")
        
        # Plugin remembers state
        response = await agent.chat("Testing memory!")
        print(f"Response: {response}")
        
        print("=" * 50)
        print("\n🚀 Congratulations! You created your first plugin!")
        
        return agent


# Minimal plugin template for copy-paste
PLUGIN_TEMPLATE = '''
from entity.plugins.base import Plugin
from entity.workflow.stages import DO  # or INPUT, PARSE, THINK, REVIEW, OUTPUT

class YourPlugin(Plugin):
    """Your plugin description."""
    
    supported_stages = [DO]  # Choose your stage(s)
    
    async def _execute_impl(self, context) -> str:
        message = context.message or ""
        
        # Your logic here
        result = f"Processed: {message}"
        
        return result
'''


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 First Plugin Example")
        print("=" * 40)
        agent = await FirstPluginExample.run()
        
        print("\n📝 Plugin Template:")
        print("-" * 40)
        print(PLUGIN_TEMPLATE)
    
    asyncio.run(main())