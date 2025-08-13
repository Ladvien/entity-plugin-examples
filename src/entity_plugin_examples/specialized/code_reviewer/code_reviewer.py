"""Code Review Assistant - Domain-specific plugin composition.

Agent = Resources + Workflow
      = code_analysis_resources + code_review_workflow
      = Static Analysis + Code Metrics + Security Scan

Story 9: Specialized Plugin Showcases
- Complete working system for code review
- Focus on plugin composition, not individual plugins
- Domain-specific test data included
"""

from typing import Any, Dict, List
from entity import Agent
from entity.defaults import load_defaults
from entity.plugins.base import Plugin
from entity.workflow.stages import PARSE, THINK, REVIEW
from entity.workflow.workflow import Workflow


class StaticAnalysisPlugin(Plugin):
    """Analyzes code structure, complexity, and patterns."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [PARSE]
    
    async def _execute_impl(self, context) -> str:
        """Extract code structure and identify patterns."""
        code = context.message or ""
        
        # Simulate static analysis
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                issues.append(f"Line {i}: Too long ({len(line)} chars)")
            if line.strip().startswith('TODO'):
                issues.append(f"Line {i}: Unfinished TODO comment")
            if 'password' in line.lower() and ('=' in line or ':' in line):
                issues.append(f"Line {i}: Potential hardcoded password")
        
        context.remember("static_analysis", {
            "line_count": len(lines),
            "issues": issues,
            "complexity_score": min(len(issues) * 2, 10)
        })
        
        return f"Static analysis found {len(issues)} issues"


class CodeMetricsPlugin(Plugin):
    """Calculates code quality metrics and maintainability scores."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [THINK]
    
    async def _execute_impl(self, context) -> str:
        """Calculate quality metrics from static analysis."""
        analysis = await context.recall("static_analysis", {})
        code = context.message or ""
        
        # Calculate metrics
        lines = len(code.split('\n'))
        functions = code.count('def ') + code.count('function ')
        classes = code.count('class ')
        complexity = analysis.get("complexity_score", 0)
        
        metrics = {
            "lines_of_code": lines,
            "functions": functions,
            "classes": classes,
            "complexity_score": complexity,
            "maintainability": max(10 - complexity, 1),  # 1-10 scale
            "test_coverage": 85 if "test" in code.lower() else 0
        }
        
        context.remember("code_metrics", metrics)
        return f"Metrics calculated: {complexity}/10 complexity, {metrics['maintainability']}/10 maintainability"


class SecurityScanPlugin(Plugin):
    """Scans for security vulnerabilities and best practices."""
    
    def __init__(self, resources: Dict[str, Any], config: Dict[str, Any] | None = None):
        super().__init__(resources, config)
        self.supported_stages = [REVIEW]
    
    async def _execute_impl(self, context) -> str:
        """Review code for security issues."""
        code = context.message or ""
        analysis = await context.recall("static_analysis", {})
        
        security_issues = []
        
        # Check for common security issues
        dangerous_patterns = [
            ("eval(", "Code injection risk"),
            ("exec(", "Code execution risk"), 
            ("shell=True", "Command injection risk"),
            ("password", "Hardcoded credentials"),
            ("api_key", "Exposed API key"),
            ("SELECT * FROM", "SQL injection potential")
        ]
        
        for pattern, description in dangerous_patterns:
            if pattern in code:
                security_issues.append(f"{description}: found '{pattern}'")
        
        # Add issues from static analysis
        static_issues = analysis.get("issues", [])
        for issue in static_issues:
            if "password" in issue.lower():
                security_issues.append(f"Security: {issue}")
        
        context.remember("security_scan", {
            "issues": security_issues,
            "severity": "high" if len(security_issues) > 2 else "medium" if security_issues else "low"
        })
        
        return f"Security scan: {len(security_issues)} issues found"


class CodeReviewerExample:
    """Complete code review system using plugin composition."""
    
    @staticmethod
    async def run():
        """80% Code, 20% Explanation - Story 9 specialized showcase.
        
        Demonstrates plugin composition for domain-specific task:
        - StaticAnalysisPlugin extracts code structure 
        - CodeMetricsPlugin calculates quality scores
        - SecurityScanPlugin identifies vulnerabilities
        """
        # Load standard resources
        resources = load_defaults()
        
        # Create code review workflow (plugin composition)
        workflow = Workflow(
            steps={
                PARSE: [StaticAnalysisPlugin(resources)],
                THINK: [CodeMetricsPlugin(resources)],
                REVIEW: [SecurityScanPlugin(resources)]
            }
        )
        
        # Agent = Resources + Domain-specific Workflow
        reviewer = Agent(resources=resources, workflow=workflow)
        
        # Demo with domain-specific test data
        test_code = '''
def authenticate_user(username, password):
    # TODO: Add proper validation
    if password == "admin123":  # Hardcoded password - security issue
        return True
    query = f"SELECT * FROM users WHERE username='{username}'"  # SQL injection risk
    return database.execute(query, shell=True)  # Command injection risk

class VeryLongClassNameThatExceedsEightyCharactersAndViolatesStyleGuideLines:
    pass
'''
        
        print("\n🔍 Story 9: Code Review Assistant")
        print("Plugin Composition: Static Analysis → Metrics → Security")
        print("=" * 60)
        
        # Review the code
        result = await reviewer.chat(test_code)
        
        print(f"\n📊 Review Result: {result}")
        
        # Show composed analysis from all plugins
        context = reviewer._context
        static_analysis = await context.recall("static_analysis", {})
        metrics = await context.recall("code_metrics", {})
        security = await context.recall("security_scan", {})
        
        print("\n📋 Detailed Analysis:")
        print(f"  Lines of Code: {metrics.get('lines_of_code', 0)}")
        print(f"  Complexity Score: {static_analysis.get('complexity_score', 0)}/10")
        print(f"  Maintainability: {metrics.get('maintainability', 0)}/10")
        print(f"  Security Issues: {len(security.get('issues', []))}")
        print(f"  Severity: {security.get('severity', 'unknown').upper()}")
        
        print("\n🚨 Issues Found:")
        for issue in static_analysis.get('issues', []):
            print(f"  • {issue}")
        for issue in security.get('issues', []):
            print(f"  • {issue}")
        
        print("\n✅ Code Review Complete!")
        print("💡 Next: Try research_assistant/ or customer_service/")
        
        return reviewer


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🚀 Specialized Plugin Showcase: Code Reviewer")
        print("Demonstrates domain-specific plugin composition")
        print()
        
        reviewer = await CodeReviewerExample.run()
    
    asyncio.run(main())