"""
Rose Glass Team Coherence Assessment Tool
=========================================

Decision support for commanders managing human systems.
Surfaces patterns, provides translation, cites sources.
The commander makes the choices.

Author: Christopher MacGregor bin Joseph
"""

from .core import (
    TeamCoherenceAssessment,
    UnitDashboard,
    CoherenceSnapshot,
    Flag,
    FlagSeverity
)

from .collectors import (
    SocialMediaCollector,
    CISDCollector,
    DebriefCollector,
    MediaMonitor
)

from .analyzers import (
    CISDAnalyzer,
    DebriefAnalyzer,
    SocialPatternAnalyzer,
    TrajectoryAnalyzer
)

from .lenses import (
    CulturalLens,
    LensLibrary,
    LensDeviationCalculator
)

__version__ = "1.0.0"
__author__ = "Christopher MacGregor bin Joseph"

__all__ = [
    # Core
    "TeamCoherenceAssessment",
    "UnitDashboard", 
    "CoherenceSnapshot",
    "Flag",
    "FlagSeverity",
    
    # Collectors
    "SocialMediaCollector",
    "CISDCollector",
    "DebriefCollector",
    "MediaMonitor",
    
    # Analyzers
    "CISDAnalyzer",
    "DebriefAnalyzer",
    "SocialPatternAnalyzer",
    "TrajectoryAnalyzer",
    
    # Lenses
    "CulturalLens",
    "LensLibrary",
    "LensDeviationCalculator"
]
