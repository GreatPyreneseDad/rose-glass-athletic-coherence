"""
Rose Looking Glass - Network Analysis Module
============================================

Social network coherence analysis using Rose Looking Glass translation framework.

Analyzes how coherence patterns propagate through networks and identifies
influence topologies based on GCT variables rather than traditional sentiment.
"""

from .coherence_graph import (
    CoherenceGraphService,
    UserCoherenceProfile,
    CoherenceCascade
)
from .coherence_influence_analyzer import (
    CoherenceInfluenceAnalyzer,
    InfluenceType,
    InfluenceAnalysis
)

__all__ = [
    'CoherenceGraphService',
    'UserCoherenceProfile',
    'CoherenceCascade',
    'CoherenceInfluenceAnalyzer',
    'InfluenceType',
    'InfluenceAnalysis',
]
