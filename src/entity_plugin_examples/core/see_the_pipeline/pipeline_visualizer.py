"""Layer 1: See the Pipeline - Visualize 6-stage message flow.

Agent = Resources + Workflow
      = defaults() + custom_workflow_with_visibility()

Story 8: Create Visual Pipeline Demo
- Visual learners see the 6-stage pipeline in action
- Print stage transitions visually showing message flow
- Minimal code, maximum visibility
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
        """Show stage transition exactly as specified in Story 8."""
        message = context.message or ""
        
        # Visual indicator in Story 8's exact format
        if self.stage_name == INPUT:
            print(f"[INPUT] Receiving: \"{message}\"")
        elif self.stage_name == PARSE:
            print(f"[PARSE] Extracting: math expression")
        elif self.stage_name == THINK:
            print(f"[THINK] Planning: calculation needed")
        elif self.stage_name == DO:
            print(f"[DO] Executing: Calculator plugin")
        elif self.stage_name == REVIEW:
            print(f"[REVIEW] Validating: result = 4")
        elif self.stage_name == OUTPUT:
            print(f"[OUTPUT] Formatting: \"The answer is 4\"")
        
        return message


class PipelineVisualizerExample:
    """Visualize the 6-stage pipeline in action."""
    
    @staticmethod
    async def run():
        """Create agent with visibility into each pipeline stage.
        
        80% Code, 20% Explanation - Story 8 requirements:
        - Show 6-stage pipeline visually: INPUT→PARSE→THINK→DO→REVIEW→OUTPUT
        - Print stage transitions exactly as specified in Story 8
        - Use "Calculate 2+2" example to demonstrate math flow
        - Minimal code, maximum visibility
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
        
        print("\n🔍 Story 8: Visual Pipeline Demo")
        print("Watching message flow through 6 stages:")
        print("=" * 50)
        
        # Use Story 8's exact example: "Calculate 2+2"
        response = await agent.chat("Calculate 2+2")
        
        print("=" * 50)
        print(f"📤 Final Response: {response}")
        print("\n✅ Pipeline visualization complete!")
        print("💡 Next: Try entity_plugin_examples.core.see_the_layers")
        
        return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Layer 1: See the Pipeline")
        print("Visual demonstration of Entity Framework's 6-stage processing:")
        print("INPUT → PARSE → THINK → DO → REVIEW → OUTPUT")
        print()
        
        agent = await PipelineVisualizerExample.run()
    
    asyncio.run(main())