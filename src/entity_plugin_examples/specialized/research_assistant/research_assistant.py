"""Research Assistant - Domain-specific plugin composition.

Agent = Resources + Workflow
      = research_resources + research_workflow
      = Source Gathering + Fact Checking + Synthesis

Story 9: Specialized Plugin Showcases
- Complete working system for research tasks
- Focus on plugin composition, not individual plugins
- Domain-specific test data included
"""

from typing import Any, Dict, List
from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE, THINK, DO
from entity.workflow.workflow import Workflow


class SourceGathererPlugin(Plugin):
    """Identifies and categorizes research sources."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [PARSE]
    
    async def _execute_impl(self, context) -> str:
        """Extract research query and identify potential sources."""
        query = context.message or ""
        
        # Simulate source identification
        sources = []
        
        # Academic sources
        if any(term in query.lower() for term in ["study", "research", "paper", "academic"]):
            sources.extend([
                {"type": "academic", "name": "PubMed", "relevance": 0.9},
                {"type": "academic", "name": "arXiv", "relevance": 0.8},
                {"type": "academic", "name": "Google Scholar", "relevance": 0.85}
            ])
        
        # News sources
        if any(term in query.lower() for term in ["news", "current", "recent", "latest"]):
            sources.extend([
                {"type": "news", "name": "Reuters", "relevance": 0.9},
                {"type": "news", "name": "Associated Press", "relevance": 0.9},
                {"type": "news", "name": "BBC News", "relevance": 0.85}
            ])
        
        # Technical sources
        if any(term in query.lower() for term in ["technology", "software", "programming", "ai"]):
            sources.extend([
                {"type": "technical", "name": "Stack Overflow", "relevance": 0.8},
                {"type": "technical", "name": "GitHub", "relevance": 0.75},
                {"type": "technical", "name": "Documentation", "relevance": 0.9}
            ])
        
        context.remember("research_sources", {
            "query": query,
            "sources": sources,
            "source_count": len(sources)
        })
        
        return f"Identified {len(sources)} relevant sources for research"


class FactCheckerPlugin(Plugin):
    """Validates information credibility and cross-references facts."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        """Analyze source credibility and fact-check information."""
        sources = await context.recall("research_sources", {})
        query = sources.get("query", "")
        source_list = sources.get("sources", [])
        
        # Simulate fact-checking process
        credibility_scores = []
        fact_checks = []
        
        for source in source_list:
            # Calculate credibility based on source type
            credibility = source.get("relevance", 0.5)
            if source["type"] == "academic":
                credibility += 0.2  # Academic sources get bonus
            elif source["type"] == "news":
                credibility += 0.1  # News sources slightly more credible
            
            credibility_scores.append(min(credibility, 1.0))
        
        # Generate fact-check results
        if "climate change" in query.lower():
            fact_checks = [
                {"claim": "Global temperatures rising", "status": "verified", "confidence": 0.95},
                {"claim": "Human activity is primary cause", "status": "verified", "confidence": 0.97}
            ]
        elif "ai" in query.lower() or "artificial intelligence" in query.lower():
            fact_checks = [
                {"claim": "AI improving rapidly", "status": "verified", "confidence": 0.9},
                {"claim": "Job displacement concerns", "status": "mixed", "confidence": 0.7}
            ]
        else:
            fact_checks = [
                {"claim": "Generic research claim", "status": "needs_verification", "confidence": 0.6}
            ]
        
        context.remember("fact_check", {
            "credibility_scores": credibility_scores,
            "average_credibility": sum(credibility_scores) / len(credibility_scores) if credibility_scores else 0,
            "fact_checks": fact_checks,
            "verified_facts": len([f for f in fact_checks if f["status"] == "verified"])
        })
        
        return f"Fact-checked {len(fact_checks)} claims with {len(credibility_scores)} sources"


class SynthesizerPlugin(Plugin):
    """Synthesizes research findings into coherent insights."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [DO]
    
    async def _execute_impl(self, context) -> str:
        """Combine sources and fact-checks into final research summary."""
        sources = await context.recall("research_sources", {})
        fact_check = await context.recall("fact_check", {})
        
        query = sources.get("query", "")
        source_count = sources.get("source_count", 0)
        avg_credibility = fact_check.get("average_credibility", 0)
        verified_facts = fact_check.get("verified_facts", 0)
        fact_checks = fact_check.get("fact_checks", [])
        
        # Generate synthesis
        synthesis = {
            "research_query": query,
            "sources_analyzed": source_count,
            "credibility_score": round(avg_credibility, 2),
            "verified_claims": verified_facts,
            "key_findings": [],
            "confidence_level": "high" if avg_credibility > 0.8 else "medium" if avg_credibility > 0.6 else "low"
        }
        
        # Extract key findings from fact-checks
        for fact in fact_checks:
            if fact["status"] == "verified" and fact["confidence"] > 0.8:
                synthesis["key_findings"].append(fact["claim"])
        
        context.remember("research_synthesis", synthesis)
        
        return f"Synthesized research: {verified_facts} verified facts from {source_count} sources"


class ResearchAssistantExample:
    """Complete research system using plugin composition."""
    
    @staticmethod
    async def run():
        """80% Code, 20% Explanation - Story 9 specialized showcase.
        
        Demonstrates plugin composition for research workflow:
        - SourceGathererPlugin identifies relevant sources
        - FactCheckerPlugin validates information credibility
        - SynthesizerPlugin combines findings into insights
        """
        # Load standard resources
        resources = load_defaults()
        
        # Create research workflow (plugin composition)
        workflow = Workflow(
            steps={
                PARSE: [SourceGathererPlugin(resources)],
                THINK: [FactCheckerPlugin(resources)],
                DO: [SynthesizerPlugin(resources)]
            }
        )
        
        # Agent = Resources + Domain-specific Workflow
        researcher = Agent(resources=resources, workflow=workflow)
        
        # Demo with domain-specific test data
        research_queries = [
            "Latest research on artificial intelligence safety measures",
            "Climate change impact on global food security studies",
            "Recent developments in quantum computing applications"
        ]
        
        print("\n🔬 Story 9: Research Assistant")
        print("Plugin Composition: Source Gathering → Fact Checking → Synthesis")
        print("=" * 70)
        
        for i, query in enumerate(research_queries, 1):
            print(f"\n📝 Research Query {i}: {query}")
            print("-" * 50)
            
            # Process the research query
            result = await researcher.chat(query)
            print(f"✅ Result: {result}")
            
            # Show composed analysis from all plugins
            context = researcher._context
            sources = await context.recall("research_sources", {})
            fact_check = await context.recall("fact_check", {})
            synthesis = await context.recall("research_synthesis", {})
            
            print(f"📊 Sources Found: {sources.get('source_count', 0)}")
            print(f"🎯 Credibility: {synthesis.get('credibility_score', 0)}/1.0")
            print(f"✓ Verified Facts: {synthesis.get('verified_claims', 0)}")
            print(f"🔍 Confidence: {synthesis.get('confidence_level', 'unknown').upper()}")
            
            if synthesis.get('key_findings'):
                print("📋 Key Findings:")
                for finding in synthesis['key_findings']:
                    print(f"  • {finding}")
            
            # Reset context for next query
            await context.remember("research_sources", {})
            await context.remember("fact_check", {})
            await context.remember("research_synthesis", {})
        
        print("\n✅ Research Analysis Complete!")
        print("💡 Next: Try code_reviewer/ or customer_service/")
        
        return researcher


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Specialized Plugin Showcase: Research Assistant")
        print("Demonstrates domain-specific plugin composition")
        print()
        
        researcher = await ResearchAssistantExample.run()
    
    asyncio.run(main())