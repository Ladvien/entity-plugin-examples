"""Multi-stage plugin support pattern example."""

from __future__ import annotations
from typing import Any, Dict, Optional
import json
import logging

from entity.plugins.base import Plugin
from entity.workflow.stages import INPUT, PARSE, THINK, DO, REVIEW, OUTPUT


class MultiStageAnalyticsPlugin(Plugin):
    """
    Example plugin demonstrating multi-stage support pattern.
    
    This plugin participates in multiple workflow stages:
    - PARSE: Extract analytics requirements
    - THINK: Plan analysis approach  
    - DO: Execute data analysis
    - REVIEW: Validate results
    - OUTPUT: Format final report
    
    Each stage has different responsibilities and can pass data via context metadata.
    """
    
    # Plugin supports multiple stages
    supported_stages = [PARSE, THINK, DO, REVIEW, OUTPUT]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        self.logger = logging.getLogger(__name__)
    
    async def _execute_impl(self, context) -> str:
        """Route execution to appropriate stage handler."""
        stage = getattr(context, 'current_stage', None)
        
        if stage == PARSE:
            return await self._handle_parse_stage(context)
        elif stage == THINK:
            return await self._handle_think_stage(context)
        elif stage == DO:
            return await self._handle_do_stage(context)
        elif stage == REVIEW:
            return await self._handle_review_stage(context)
        elif stage == OUTPUT:
            return await self._handle_output_stage(context)
        else:
            # Fallback if stage not detected
            return await self._handle_do_stage(context)
    
    async def _handle_parse_stage(self, context) -> str:
        """PARSE stage: Extract analytics requirements from input."""
        message = context.message or ""
        
        # Parse analytics request
        requirements = {
            "data_type": self._detect_data_type(message),
            "analysis_type": self._detect_analysis_type(message),
            "metrics": self._extract_metrics(message),
            "filters": self._extract_filters(message)
        }
        
        # Store in context metadata for other stages
        if not hasattr(context, 'metadata'):
            context.metadata = {}
        context.metadata['analytics_requirements'] = requirements
        
        self.logger.info(f"PARSE: Extracted requirements: {requirements}")
        return f"[PARSE] Analytics requirements extracted: {requirements['analysis_type']} on {requirements['data_type']}"
    
    async def _handle_think_stage(self, context) -> str:
        """THINK stage: Plan analysis approach based on requirements."""
        requirements = getattr(context, 'metadata', {}).get('analytics_requirements', {})
        
        # Create analysis plan
        plan = {
            "steps": self._plan_analysis_steps(requirements),
            "estimated_time": self._estimate_processing_time(requirements),
            "required_resources": self._identify_required_resources(requirements),
            "potential_issues": self._identify_potential_issues(requirements)
        }
        
        # Store plan in metadata
        context.metadata['analysis_plan'] = plan
        
        self.logger.info(f"THINK: Created analysis plan with {len(plan['steps'])} steps")
        return f"[THINK] Analysis plan created: {len(plan['steps'])} steps, ~{plan['estimated_time']}s"
    
    async def _handle_do_stage(self, context) -> str:
        """DO stage: Execute the planned analysis."""
        plan = getattr(context, 'metadata', {}).get('analysis_plan', {})
        requirements = getattr(context, 'metadata', {}).get('analytics_requirements', {})
        
        # Execute analysis (simulated)
        results = {
            "status": "completed",
            "data_points_analyzed": 1000,
            "findings": self._generate_findings(requirements),
            "execution_time": 2.5,
            "confidence_score": 0.87
        }
        
        # Store results in metadata
        context.metadata['analysis_results'] = results
        
        self.logger.info(f"DO: Analysis completed with confidence {results['confidence_score']}")
        return f"[DO] Analysis executed: {results['data_points_analyzed']} points, {len(results['findings'])} findings"
    
    async def _handle_review_stage(self, context) -> str:
        """REVIEW stage: Validate analysis results for quality and accuracy."""
        results = getattr(context, 'metadata', {}).get('analysis_results', {})
        
        # Perform quality checks
        quality_checks = {
            "data_completeness": self._check_data_completeness(results),
            "statistical_validity": self._check_statistical_validity(results),
            "outlier_detection": self._check_for_outliers(results),
            "bias_assessment": self._assess_potential_bias(results)
        }
        
        # Determine overall quality score
        quality_score = sum(quality_checks.values()) / len(quality_checks)
        
        # Store quality assessment
        context.metadata['quality_assessment'] = {
            "checks": quality_checks,
            "overall_score": quality_score,
            "approved": quality_score >= 0.75
        }
        
        status = "APPROVED" if quality_score >= 0.75 else "NEEDS_REVISION"
        self.logger.info(f"REVIEW: Quality score {quality_score:.2f} - {status}")
        return f"[REVIEW] Quality assessment: {quality_score:.2f} - {status}"
    
    async def _handle_output_stage(self, context) -> str:
        """OUTPUT stage: Format and present final results."""
        results = getattr(context, 'metadata', {}).get('analysis_results', {})
        quality = getattr(context, 'metadata', {}).get('quality_assessment', {})
        
        # Generate formatted report
        report = {
            "executive_summary": self._generate_executive_summary(results),
            "detailed_findings": results.get('findings', []),
            "methodology": "Multi-stage analytics pipeline",
            "quality_score": quality.get('overall_score', 0.0),
            "confidence": results.get('confidence_score', 0.0),
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        # Format as readable output
        formatted_output = self._format_final_report(report)
        
        self.logger.info(f"OUTPUT: Final report generated ({len(formatted_output)} chars)")
        return formatted_output
    
    # Helper methods for each stage
    
    def _detect_data_type(self, message: str) -> str:
        """Detect type of data to analyze."""
        message_lower = message.lower()
        if any(word in message_lower for word in ["sales", "revenue", "profit"]):
            return "financial"
        elif any(word in message_lower for word in ["user", "visitor", "session"]):
            return "behavioral"
        elif any(word in message_lower for word in ["performance", "speed", "latency"]):
            return "performance"
        else:
            return "general"
    
    def _detect_analysis_type(self, message: str) -> str:
        """Detect type of analysis requested."""
        message_lower = message.lower()
        if "trend" in message_lower:
            return "trend_analysis"
        elif "compare" in message_lower:
            return "comparative_analysis"
        elif "predict" in message_lower:
            return "predictive_analysis"
        else:
            return "descriptive_analysis"
    
    def _extract_metrics(self, message: str) -> list[str]:
        """Extract metrics to analyze from message."""
        # Simplified metric extraction
        metrics = []
        common_metrics = ["conversion", "retention", "engagement", "revenue", "traffic"]
        for metric in common_metrics:
            if metric in message.lower():
                metrics.append(metric)
        return metrics or ["general_performance"]
    
    def _extract_filters(self, message: str) -> Dict[str, Any]:
        """Extract any filters or constraints."""
        return {
            "time_range": "last_30_days",
            "segment": "all_users"
        }
    
    def _plan_analysis_steps(self, requirements: Dict[str, Any]) -> list[str]:
        """Plan the analysis steps based on requirements."""
        base_steps = ["data_validation", "data_cleaning", "analysis_execution"]
        if requirements.get("analysis_type") == "predictive_analysis":
            base_steps.extend(["model_training", "model_validation"])
        return base_steps
    
    def _estimate_processing_time(self, requirements: Dict[str, Any]) -> float:
        """Estimate processing time."""
        base_time = 2.0
        if requirements.get("analysis_type") == "predictive_analysis":
            base_time *= 3
        return base_time
    
    def _identify_required_resources(self, requirements: Dict[str, Any]) -> list[str]:
        """Identify required computational resources."""
        return ["cpu", "memory", "storage"]
    
    def _identify_potential_issues(self, requirements: Dict[str, Any]) -> list[str]:
        """Identify potential issues that could arise."""
        return ["data_quality", "sample_size", "statistical_power"]
    
    def _generate_findings(self, requirements: Dict[str, Any]) -> list[str]:
        """Generate analysis findings (simulated)."""
        return [
            f"Key insight for {requirements.get('data_type', 'general')} analysis",
            "Identified significant correlation in data",
            "Detected anomaly in recent time period"
        ]
    
    def _check_data_completeness(self, results: Dict[str, Any]) -> float:
        """Check data completeness (simulated)."""
        return 0.95
    
    def _check_statistical_validity(self, results: Dict[str, Any]) -> float:
        """Check statistical validity (simulated)."""
        return 0.88
    
    def _check_for_outliers(self, results: Dict[str, Any]) -> float:
        """Check for outliers (simulated)."""
        return 0.82
    
    def _assess_potential_bias(self, results: Dict[str, Any]) -> float:
        """Assess potential bias (simulated)."""
        return 0.79
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate executive summary."""
        return f"Analysis completed successfully with {results.get('confidence_score', 0)*100:.1f}% confidence."
    
    def _format_final_report(self, report: Dict[str, Any]) -> str:
        """Format the final report for output."""
        return f"""[OUTPUT] Analytics Report Generated

Executive Summary: {report['executive_summary']}

Key Findings:
{chr(10).join(f"• {finding}" for finding in report['detailed_findings'])}

Quality Score: {report['quality_score']:.2f}/1.00
Confidence: {report['confidence']:.2f}/1.00
Methodology: {report['methodology']}
Generated: {report['timestamp']}

This multi-stage plugin processed your request through:
PARSE → THINK → DO → REVIEW → OUTPUT
"""


# Example usage showing multi-stage processing:
"""
# The plugin will be called at each stage with different context.current_stage values:

# Stage 1 - PARSE
context.current_stage = PARSE
context.message = "Analyze user engagement trends for last month"
result = await plugin.execute(context)  
# Returns: "[PARSE] Analytics requirements extracted: trend_analysis on behavioral"

# Stage 2 - THINK  
context.current_stage = THINK
result = await plugin.execute(context)
# Returns: "[THINK] Analysis plan created: 3 steps, ~2.0s"

# Stage 3 - DO
context.current_stage = DO
result = await plugin.execute(context)
# Returns: "[DO] Analysis executed: 1000 points, 3 findings"

# Stage 4 - REVIEW
context.current_stage = REVIEW  
result = await plugin.execute(context)
# Returns: "[REVIEW] Quality assessment: 0.86 - APPROVED"

# Stage 5 - OUTPUT
context.current_stage = OUTPUT
result = await plugin.execute(context)
# Returns: Full formatted analytics report
"""