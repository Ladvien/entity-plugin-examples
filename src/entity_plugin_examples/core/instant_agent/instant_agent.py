"""Layer 0: Instant Agent - Zero configuration example.

Agent = Resources + Workflow
      = defaults() + default_workflow()
      = Ready to use!

Story 7: Simplify Getting Started Experience
- First-time users run their first agent in under 30 seconds
- 3-line example with immediate value demonstration
- Output shown inline as comments
- Clear next steps provided
"""

from entity import Agent


class InstantAgentExample:
    """The simplest possible agent - zero configuration required.
    
    Perfect for first-time users who want immediate results.
    """
    
    @staticmethod
    async def run():
        """The 3-line example that gets users started in under 30 seconds.
        
        80% Code, 20% Explanation - Story 7 requirements:
        - 3 lines of code
        - Output shown inline as comments
        - Immediate value demonstration
        """
        agent = Agent()                                # Line 1: Create agent
        response = await agent.chat("Hello")          # Line 2: Chat with agent
        # "Hi! How can I help?" <- This appears immediately
        
        return response
    
    @staticmethod
    async def demo():
        """Extended demo showing more capabilities."""
        print("🚀 Layer 0: Instant Agent - Zero Configuration")
        print("=" * 50)
        print()
        
        print("Step 1: Create an agent (no configuration needed)")
        agent = Agent()
        print("✅ Agent created!")
        print()
        
        print("Step 2: Start chatting")
        response = await agent.chat("Hello")
        print(f'You: "Hello"')
        print(f'Agent: "{response}"')
        print()
        
        print("Step 3: Ask questions")
        response = await agent.chat("What is 2 + 2?")
        print(f'You: "What is 2 + 2?"')
        print(f'Agent: "{response}"')
        print()
        
        print("✨ That's it! You've created your first Entity agent.")
        print()
        print("🎯 NEXT STEPS:")
        print("- Try: entity_plugin_examples.core.see_the_pipeline")
        print("- See the 6-stage pipeline in action")
        print("- Learn how agents process your messages")
        
        return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # The Story 7 requirement: 3-line example
        print("📝 Story 7: 3-line example")
        print("-" * 30)
        
        agent = Agent()                                # Line 1
        response = await agent.chat("Hello")          # Line 2  
        print(f"Response: {response}")                 # Line 3 (demonstration)
        # "Hi! How can I help?" <- This appears immediately
        
        print()
        print("🎯 Next: See core/see_the_pipeline/ for stage visualization")
        
        # Extended demo for those who want more
        print("\n" + "="*60)
        await InstantAgentExample.demo()
    
    asyncio.run(main())