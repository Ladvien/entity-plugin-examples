"""Layer 1: See the Pipeline - Visualize the 6-stage message flow.

Shows how messages flow through the Entity pipeline:
INPUT → PARSE → THINK → DO → REVIEW → OUTPUT
"""

from .pipeline_visualizer import PipelineVisualizerExample

__all__ = ["PipelineVisualizerExample"]