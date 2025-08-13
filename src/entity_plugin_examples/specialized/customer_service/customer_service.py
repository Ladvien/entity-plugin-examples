"""Customer Service Assistant - Domain-specific plugin composition.

Agent = Resources + Workflow
      = customer_support_resources + service_workflow
      = Intent Classification + Knowledge Base + Response Generation

Story 9: Specialized Plugin Showcases
- Complete working system for customer service
- Focus on plugin composition, not individual plugins
- Domain-specific test data included
"""

from typing import Any, Dict, List
from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE, THINK, OUTPUT
from entity.workflow.workflow import Workflow


class IntentClassifierPlugin(Plugin):
    """Classifies customer intent and extracts key information."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [PARSE]
    
    async def _execute_impl(self, context) -> str:
        """Classify customer intent and extract entities."""
        message = context.message or ""
        
        # Simulate intent classification
        intent = "general_inquiry"
        confidence = 0.7
        entities = {}
        urgency = "normal"
        
        # Simple keyword-based classification
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["refund", "return", "money back"]):
            intent = "refund_request"
            confidence = 0.9
            urgency = "high"
        elif any(word in message_lower for word in ["billing", "charge", "payment", "invoice"]):
            intent = "billing_inquiry"
            confidence = 0.85
        elif any(word in message_lower for word in ["bug", "error", "broken", "not working"]):
            intent = "technical_support"
            confidence = 0.9
            urgency = "high"
        elif any(word in message_lower for word in ["cancel", "subscription", "account"]):
            intent = "account_management"
            confidence = 0.8
        elif any(word in message_lower for word in ["how", "what", "when", "where", "?"]):
            intent = "general_inquiry"
            confidence = 0.7
        
        # Extract entities
        if "order" in message_lower:
            # Look for order numbers (simple pattern)
            import re
            order_matches = re.findall(r'#?\d{4,8}', message)
            if order_matches:
                entities["order_number"] = order_matches[0].replace("#", "")
        
        if "@" in message:
            # Extract email
            email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
            if email_matches:
                entities["email"] = email_matches[0]
        
        context.remember("intent_classification", {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "urgency": urgency,
            "original_message": message
        })
        
        return f"Classified intent: {intent} (confidence: {confidence})"


class KnowledgeBasePlugin(Plugin):
    """Searches knowledge base for relevant information."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [THINK]
        
        # Simulate knowledge base
        self.knowledge_base = {
            "refund_request": {
                "policy": "Refunds available within 30 days of purchase",
                "process": "Submit refund request with order number and reason",
                "timeline": "5-7 business days to process",
                "requirements": ["Original receipt", "Product in original condition"]
            },
            "billing_inquiry": {
                "payment_methods": ["Credit card", "PayPal", "Bank transfer"],
                "billing_cycle": "Monthly on subscription date",
                "late_fees": "$5 after 10 days past due",
                "contact": "billing@company.com"
            },
            "technical_support": {
                "common_issues": ["Login problems", "Performance issues", "Feature not working"],
                "troubleshooting": ["Clear browser cache", "Update browser", "Check internet connection"],
                "escalation": "Technical team available 24/7",
                "contact": "support@company.com"
            },
            "account_management": {
                "cancellation": "Cancel anytime from account settings",
                "data_export": "Download your data before canceling",
                "reactivation": "Contact support to reactivate within 90 days",
                "contact": "accounts@company.com"
            },
            "general_inquiry": {
                "hours": "Monday-Friday 9am-5pm EST",
                "response_time": "Within 24 hours",
                "channels": ["Email", "Chat", "Phone"],
                "contact": "info@company.com"
            }
        }
    
    async def _execute_impl(self, context) -> str:
        """Search knowledge base based on classified intent."""
        classification = await context.recall("intent_classification", {})
        intent = classification.get("intent", "general_inquiry")
        
        # Get relevant knowledge base entry
        kb_entry = self.knowledge_base.get(intent, self.knowledge_base["general_inquiry"])
        
        # Calculate relevance score based on entities
        entities = classification.get("entities", {})
        relevance_score = 0.8  # Base relevance
        
        if entities:
            relevance_score += 0.1  # Boost if we have specific entities
        
        if classification.get("confidence", 0) > 0.8:
            relevance_score += 0.1  # Boost for high confidence classification
        
        context.remember("knowledge_search", {
            "intent": intent,
            "knowledge_entry": kb_entry,
            "relevance_score": min(relevance_score, 1.0),
            "entities_found": len(entities)
        })
        
        return f"Found knowledge base entry for {intent} (relevance: {relevance_score:.2f})"


class ResponseGeneratorPlugin(Plugin):
    """Generates personalized customer service response."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [OUTPUT]
    
    async def _execute_impl(self, context) -> str:
        """Generate personalized response based on intent and knowledge."""
        classification = await context.recall("intent_classification", {})
        knowledge = await context.recall("knowledge_search", {})
        
        intent = classification.get("intent", "general_inquiry")
        urgency = classification.get("urgency", "normal")
        entities = classification.get("entities", {})
        kb_entry = knowledge.get("knowledge_entry", {})
        
        # Generate response based on intent
        response_parts = []
        
        # Greeting based on urgency
        if urgency == "high":
            response_parts.append("Thank you for contacting us. I understand this is urgent, and I'm here to help immediately.")
        else:
            response_parts.append("Thank you for reaching out! I'm happy to help you today.")
        
        # Intent-specific response
        if intent == "refund_request":
            response_parts.append(f"I can help you with your refund request. Our refund policy allows returns within 30 days.")
            if "order_number" in entities:
                response_parts.append(f"I see you mentioned order #{entities['order_number']}. Let me look that up for you.")
            response_parts.append("To proceed, please provide your order number and the reason for the refund.")
            
        elif intent == "billing_inquiry":
            response_parts.append("I can assist with your billing question.")
            response_parts.append(f"Our billing cycle is {kb_entry.get('billing_cycle', 'monthly')}, and we accept {', '.join(kb_entry.get('payment_methods', []))}.")
            
        elif intent == "technical_support":
            response_parts.append("I'm here to help resolve your technical issue.")
            troubleshooting = kb_entry.get("troubleshooting", [])
            if troubleshooting:
                response_parts.append(f"Here are some quick troubleshooting steps: {', '.join(troubleshooting[:2])}.")
            
        elif intent == "account_management":
            response_parts.append("I can help you manage your account.")
            response_parts.append(f"For account changes, you can {kb_entry.get('cancellation', 'manage your account online')}.")
            
        else:  # general_inquiry
            response_parts.append("I'm here to help with any questions you might have.")
            response_parts.append(f"Our support hours are {kb_entry.get('hours', '24/7')}.")
        
        # Closing
        if urgency == "high":
            response_parts.append("Is there anything else urgent I can help you with right now?")
        else:
            response_parts.append("Is there anything else I can help you with today?")
        
        final_response = " ".join(response_parts)
        
        context.remember("customer_response", {
            "response": final_response,
            "intent_addressed": intent,
            "urgency_level": urgency,
            "personalization_score": 0.8 if entities else 0.6,
            "response_length": len(final_response.split())
        })
        
        return final_response


class CustomerServiceExample:
    """Complete customer service system using plugin composition."""
    
    @staticmethod
    async def run():
        """80% Code, 20% Explanation - Story 9 specialized showcase.
        
        Demonstrates plugin composition for customer service:
        - IntentClassifierPlugin identifies customer needs
        - KnowledgeBasePlugin finds relevant information
        - ResponseGeneratorPlugin creates personalized responses
        """
        # Load standard resources
        resources = load_defaults()
        
        # Create customer service workflow (plugin composition)
        workflow = Workflow(
            steps={
                PARSE: [IntentClassifierPlugin(resources)],
                THINK: [KnowledgeBasePlugin(resources)],
                OUTPUT: [ResponseGeneratorPlugin(resources)]
            }
        )
        
        # Agent = Resources + Domain-specific Workflow
        service_agent = Agent(resources=resources, workflow=workflow)
        
        # Demo with domain-specific test data
        customer_messages = [
            "Hi, I need a refund for order #12345. The product was damaged.",
            "I'm having trouble with my billing. Why was I charged twice this month?",
            "The app keeps crashing when I try to upload files. This is urgent!",
            "How do I cancel my subscription? I can't find the option.",
            "What are your business hours? I have a general question about your service."
        ]
        
        print("\n🎧 Story 9: Customer Service Assistant")
        print("Plugin Composition: Intent Classification → Knowledge Search → Response Generation")
        print("=" * 80)
        
        for i, message in enumerate(customer_messages, 1):
            print(f"\n💬 Customer Message {i}: \"{message}\"")
            print("-" * 60)
            
            # Process the customer message
            response = await service_agent.chat(message)
            print(f"🤖 Agent Response:\n{response}")
            
            # Show composed analysis from all plugins
            context = service_agent._context
            classification = await context.recall("intent_classification", {})
            knowledge = await context.recall("knowledge_search", {})
            response_data = await context.recall("customer_response", {})
            
            print(f"\n📊 Analysis:")
            print(f"  Intent: {classification.get('intent', 'unknown')} (confidence: {classification.get('confidence', 0):.2f})")
            print(f"  Urgency: {classification.get('urgency', 'normal').upper()}")
            print(f"  Entities: {len(classification.get('entities', {}))}")
            print(f"  Knowledge Relevance: {knowledge.get('relevance_score', 0):.2f}")
            print(f"  Response Length: {response_data.get('response_length', 0)} words")
            print(f"  Personalization: {response_data.get('personalization_score', 0):.2f}")
            
            # Reset context for next message
            await context.remember("intent_classification", {})
            await context.remember("knowledge_search", {})
            await context.remember("customer_response", {})
        
        print("\n✅ Customer Service Demo Complete!")
        print("💡 Next: Try code_reviewer/ or research_assistant/")
        
        return service_agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Specialized Plugin Showcase: Customer Service")
        print("Demonstrates domain-specific plugin composition")
        print()
        
        service_agent = await CustomerServiceExample.run()
    
    asyncio.run(main())