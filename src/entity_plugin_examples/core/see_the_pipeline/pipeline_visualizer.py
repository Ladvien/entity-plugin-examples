"""Layer 1: See the Pipeline - Visualize 6-stage message flow.

Agent = Resources + Workflow
      = defaults() + custom_workflow_with_visibility()
"""

from typing import Any, Dict

from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import DO, INPUT, OUTPUT, PARSE, REVIEW, THINK
from entity.workflow.workflow import Workflow


class VisibilityPlugin(Plugin):
    """Plugin that shows what happens at each stage."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.stage_name = config.get("stage") if config else "UNKNOWN"
        self.supported_stages = [self.stage_name]
    
    async def _execute_impl(self, context) -> str:
        """Show stage transition and pass message through."""
        message = context.message or ""
        
        # Visual indicator of stage processing
        print(f"[{self.stage_name:^8}] Processing: '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        # Stage-specific behavior (minimal, just for demonstration)
        if self.stage_name == INPUT:
            print(f"           → Receiving user input")
        elif self.stage_name == PARSE:
            print(f"           → Extracting intent and entities")
        elif self.stage_name == THINK:
            print(f"           → Planning response strategy")
        elif self.stage_name == DO:
            print(f"           → Executing actions")
        elif self.stage_name == REVIEW:
            print(f"           → Validating response")
        elif self.stage_name == OUTPUT:
            print(f"           → Formatting final output")
            context.say(f"Processed: {message}")
        
        return message


class PipelineVisualizerExample:
    """Visualize the 6-stage pipeline in action."""
    
    @staticmethod
    async def run():
        """Create agent with visibility into each pipeline stage.
        
        80% Code showing the pipeline:
        - Each stage gets a visibility plugin
        - See message flow through INPUT→PARSE→THINK→DO→REVIEW→OUTPUT
        """
        # Load default resources
        resources = load_defaults()
        
        # Create workflow with visibility at each stage
        workflow = Workflow(
            steps={
                INPUT: [VisibilityPlugin(resources, {"stage": INPUT})],
                PARSE: [VisibilityPlugin(resources, {"stage": PARSE})],
                THINK: [VisibilityPlugin(resources, {"stage": THINK})],
                DO: [VisibilityPlugin(resources, {"stage": DO})],
                REVIEW: [VisibilityPlugin(resources, {"stage": REVIEW})],
                OUTPUT: [VisibilityPlugin(resources, {"stage": OUTPUT})],
            }
        )
        
        # Agent = Resources + Workflow (with visibility)
        agent = Agent(resources=resources, workflow=workflow)
        
        print("\n🔍 Watching message flow through 6 stages:")
        print("=" * 50)
        
        # Process a message and see it flow through stages
        response = await agent.chat("Calculate 2 + 2")
        
        print("=" * 50)
        print(f"\n📤 Final Response: {response}")
        
        return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Layer 1: See the Pipeline")
        print("=" * 40)
        agent = await PipelineVisualizerExample.run()
        print("\n✅ Pipeline visualization complete!")
    
    asyncio.run(main())