"""
Rose Glass Athletic Coherence
=============================

Decision support for professional sports organizations managing human systems.
Detects patterns before bodies break. Surfaces systemic issues, not individual blame.

Author: Christopher MacGregor bin Joseph
"""

from .core import (
    AthleticCoherenceAssessment,
    OrganizationDashboard,
    PhysicalCoherenceScore,
    CoherenceSnapshot,
    SystemicFlag,
    FlagSeverity
)

from .analyzers import (
    InjuryPatternAnalyzer,
    TrainingLoadAnalyzer,
    RecoveryAnalyzer,
    NutritionAnalyzer,
    ProtocolEffectivenessAnalyzer
)

__version__ = "1.0.0"
__author__ = "Christopher MacGregor bin Joseph"

__all__ = [
    # Core
    "AthleticCoherenceAssessment",
    "OrganizationDashboard",
    "PhysicalCoherenceScore",
    "CoherenceSnapshot",
    "SystemicFlag",
    "FlagSeverity",
    
    # Analyzers
    "InjuryPatternAnalyzer",
    "TrainingLoadAnalyzer",
    "RecoveryAnalyzer",
    "NutritionAnalyzer",
    "ProtocolEffectivenessAnalyzer"
]
