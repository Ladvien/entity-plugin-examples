"""Layer 0: Instant Agent - Zero configuration example.

Agent = Resources + Workflow
      = defaults() + default_workflow()
      = Ready to use!
"""

from entity import Agent
from entity.defaults import load_defaults


class InstantAgentExample:
    """The simplest possible agent - zero configuration required."""
    
    @staticmethod
    async def run():
        """Create and run an agent with zero configuration.
        
        80% Code, 20% Explanation:
        - Agent() creates a fully functional agent
        - Uses default resources (memory, LLM, storage)
        - Uses default workflow (6-stage pipeline)
        """
        # Agent = Resources + Workflow (all defaults)
        agent = Agent()
        
        # That's it! Agent is ready to use
        response = await agent.chat("Hello, Entity!")
        print(f"Agent: {response}")
        
        # Example interactions
        response = await agent.chat("What is 2 + 2?")
        print(f"Agent: {response}")
        
        response = await agent.chat("Remember my name is Alice")
        print(f"Agent: {response}")
        
        response = await agent.chat("What's my name?")
        print(f"Agent: {response}")
        
        return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Layer 0: Instant Agent")
        print("=" * 40)
        agent = await InstantAgentExample.run()
        print("\n✅ Agent created with zero configuration!")
    
    asyncio.run(main())