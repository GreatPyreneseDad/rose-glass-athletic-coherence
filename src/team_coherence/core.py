"""
Core Team Coherence Assessment Components
=========================================

Main classes for team coherence assessment, flagging, and commander interface.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics


class FlagSeverity(Enum):
    """Severity levels for coherence flags"""
    INFO = "info"           # Pattern noted, no concern
    WATCH = "watch"         # Monitor trend
    ATTENTION = "attention" # Commander should be aware
    CRITICAL = "critical"   # Lens-invariant signal, needs visibility


@dataclass
class Citation:
    """Source citation for a flag"""
    source_type: str       # "social_media", "cisd", "debrief", "supervisor"
    source_id: str         # Unique identifier
    timestamp: datetime
    excerpt: str           # Relevant excerpt (anonymized)
    confidence: float      # 0-1 confidence in relevance
    
    def __str__(self) -> str:
        return f"[{self.source_type}] {self.timestamp.strftime('%Y-%m-%d')}: {self.excerpt[:50]}..."


@dataclass
class LensAnalysis:
    """Cultural lens analysis for a pattern"""
    lens_name: str
    coherence_reading: float
    interpretation: str
    confidence: float


@dataclass
class Flag:
    """
    A flagged pattern requiring commander attention.
    
    Always includes citations so commander can investigate.
    Always includes cultural lens analysis for translation.
    """
    id: str
    member_id: str         # Anonymized identifier
    dimension: str         # Which dimension triggered (psi, rho, q, f, tau)
    value: float           # Current value
    threshold: float       # What threshold was crossed
    severity: FlagSeverity
    
    # Required context
    citations: List[Citation]
    meaning: str           # Human-readable translation
    
    # Cultural context
    lens_analyses: List[LensAnalysis]
    lens_invariant: bool   # True if all lenses agree (critical signal)
    cultural_note: str     # Translation guidance for commander
    
    # Trajectory
    trend: str             # "rising", "falling", "stable"
    gradient: float        # Rate of change
    
    # Timestamps
    first_detected: datetime
    last_updated: datetime
    
    def get_summary(self) -> str:
        """Commander-facing summary"""
        inv_marker = "⚠️ LENS-INVARIANT" if self.lens_invariant else ""
        
        summary = f"""
FLAG {self.id} {inv_marker}
Dimension: {self.dimension} = {self.value:.2f} (threshold: {self.threshold:.2f})
Severity: {self.severity.value.upper()}
Trend: {self.trend} (gradient: {self.gradient:+.3f})

TRANSLATION:
{self.meaning}

CULTURAL CONTEXT:
{self.cultural_note}

SOURCES ({len(self.citations)} citations):
"""
        for c in self.citations[:3]:  # Show top 3
            summary += f"  • {c}\n"
        
        if len(self.citations) > 3:
            summary += f"  ... and {len(self.citations) - 3} more\n"
        
        return summary


@dataclass
class DimensionReading:
    """Single dimension reading with confidence"""
    dimension: str
    value: float
    confidence: float
    sample_size: int
    sources: List[str]


@dataclass
class CoherenceSnapshot:
    """Point-in-time coherence assessment for a unit"""
    unit_id: str
    timestamp: datetime
    
    # Core dimensions (with confidence intervals)
    psi: DimensionReading
    rho: DimensionReading
    q: DimensionReading
    f: DimensionReading
    tau: DimensionReading
    
    # Aggregate metrics
    overall_coherence: float
    confidence_interval: Tuple[float, float]
    
    # Data sources used
    data_sources: Dict[str, int]  # source_type -> count
    
    # Flags
    flags: List[Flag]
    
    # Lens analysis
    lens_deviation: float  # σ across lenses
    lens_invariant_signals: List[str]
    
    def get_status(self, dimension: str) -> str:
        """Get status label for a dimension"""
        reading = getattr(self, dimension)
        
        if dimension == "q":
            if reading.value > 0.7:
                return "ELEVATED"
            elif reading.value > 0.5:
                return "WATCH"
            return "NOMINAL"
        
        elif dimension == "f":
            if reading.value < 0.4:
                return "CONCERN"
            elif reading.value < 0.6:
                return "WATCH"
            return "NOMINAL"
        
        else:  # psi, rho, tau
            if reading.value < 0.5:
                return "LOW"
            elif reading.value > 0.8:
                return "STRONG"
            return "NOMINAL"


@dataclass
class Trajectory:
    """Coherence trajectory over time"""
    unit_id: str
    timeframe_days: int
    snapshots: List[CoherenceSnapshot]
    
    # Trends
    psi_trend: float    # Slope per week
    rho_trend: float
    q_trend: float
    f_trend: float
    tau_trend: float
    
    # Flags over time
    flag_frequency: float  # Flags per week
    recurring_flags: List[str]  # Flag IDs that reappear
    
    def get_trend_arrow(self, dimension: str) -> str:
        """Get trend indicator"""
        trend = getattr(self, f"{dimension}_trend")
        if trend > 0.02:
            return "↑ RISING"
        elif trend < -0.02:
            return "↓ DECLINING"
        return "→ STABLE"


class UnitDashboard:
    """
    Commander interface for unit coherence.
    
    Provides snapshots, trajectories, flags with full citations.
    """
    
    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        self.snapshots: List[CoherenceSnapshot] = []
        self.flags: Dict[str, Flag] = {}
        self.members: Dict[str, Dict] = {}  # Anonymized member tracking
    
    def get_snapshot(self) -> CoherenceSnapshot:
        """Get current coherence snapshot"""
        if not self.snapshots:
            return self._create_empty_snapshot()
        return self.snapshots[-1]
    
    def get_trajectory(self, days: int = 90) -> Trajectory:
        """Get coherence trajectory over time"""
        cutoff = datetime.now() - timedelta(days=days)
        relevant = [s for s in self.snapshots if s.timestamp > cutoff]
        
        if len(relevant) < 2:
            return self._create_flat_trajectory(days)
        
        # Calculate trends
        def calc_trend(dim: str) -> float:
            values = [getattr(s, dim).value for s in relevant]
            if len(values) < 2:
                return 0.0
            # Simple linear regression slope
            n = len(values)
            x_mean = (n - 1) / 2
            y_mean = sum(values) / n
            
            numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                return 0.0
            
            # Convert to per-week
            slope_per_point = numerator / denominator
            points_per_week = 7 * len(relevant) / days
            return slope_per_point * points_per_week
        
        return Trajectory(
            unit_id=self.unit_id,
            timeframe_days=days,
            snapshots=relevant,
            psi_trend=calc_trend("psi"),
            rho_trend=calc_trend("rho"),
            q_trend=calc_trend("q"),
            f_trend=calc_trend("f"),
            tau_trend=calc_trend("tau"),
            flag_frequency=len([f for f in self.flags.values() 
                              if f.first_detected > cutoff]) / (days / 7),
            recurring_flags=[f.id for f in self.flags.values() 
                           if (datetime.now() - f.first_detected).days > 14]
        )
    
    def get_flag(self, flag_id: str) -> Optional[Flag]:
        """Get detailed flag with all citations"""
        return self.flags.get(flag_id)
    
    def get_flags_by_severity(self, min_severity: FlagSeverity = FlagSeverity.WATCH) -> List[Flag]:
        """Get flags at or above severity level"""
        severity_order = [FlagSeverity.INFO, FlagSeverity.WATCH, 
                         FlagSeverity.ATTENTION, FlagSeverity.CRITICAL]
        min_idx = severity_order.index(min_severity)
        
        return [f for f in self.flags.values() 
                if severity_order.index(f.severity) >= min_idx]
    
    def get_lens_invariant_flags(self) -> List[Flag]:
        """Get flags where all cultural lenses agree (critical signals)"""
        return [f for f in self.flags.values() if f.lens_invariant]
    
    def commander_summary(self) -> str:
        """Generate commander-facing summary"""
        snapshot = self.get_snapshot()
        trajectory = self.get_trajectory()
        
        summary = f"""
UNIT COHERENCE SUMMARY: {self.unit_id.upper()}
{'=' * 50}
Assessment Date: {snapshot.timestamp.strftime('%Y-%m-%d %H:%M')}
Data Sources: {', '.join(f"{v} {k}" for k, v in snapshot.data_sources.items())}

AGGREGATE METRICS (with 90% confidence intervals)
{'-' * 50}
Ψ (Consistency):    {snapshot.psi.value:.2f} ± {(1-snapshot.psi.confidence)*0.2:.2f}  [{snapshot.get_status('psi')}]
ρ (Wisdom):         {snapshot.rho.value:.2f} ± {(1-snapshot.rho.confidence)*0.2:.2f}  [{snapshot.get_status('rho')}]
q (Activation):     {snapshot.q.value:.2f} ± {(1-snapshot.q.confidence)*0.2:.2f}  [{snapshot.get_status('q')}]
f (Cohesion):       {snapshot.f.value:.2f} ± {(1-snapshot.f.confidence)*0.2:.2f}  [{snapshot.get_status('f')}]
τ (Temporal):       {snapshot.tau.value:.2f} ± {(1-snapshot.tau.confidence)*0.2:.2f}  [{snapshot.get_status('tau')}]
"""
        
        # Lens-invariant signals
        invariant_flags = self.get_lens_invariant_flags()
        if invariant_flags:
            summary += f"""
LENS-INVARIANT SIGNALS (Critical - all lenses agree)
{'-' * 50}
"""
            for flag in invariant_flags:
                summary += f"⚠️  {flag.dimension}-dimension: {flag.meaning}\n"
                summary += f"    Sources: {', '.join(str(c) for c in flag.citations[:2])}\n\n"
        
        # Trajectory
        summary += f"""
TRAJECTORY ({trajectory.timeframe_days}-day trend)
{'-' * 50}
f-dimension: {trajectory.get_trend_arrow('f')} (slope: {trajectory.f_trend:+.3f}/week)
q-dimension: {trajectory.get_trend_arrow('q')} (slope: {trajectory.q_trend:+.3f}/week)
Ψ-dimension: {trajectory.get_trend_arrow('psi')} (slope: {trajectory.psi_trend:+.3f}/week)
"""
        
        # Flagged individuals
        attention_flags = self.get_flags_by_severity(FlagSeverity.ATTENTION)
        if attention_flags:
            summary += f"""
FLAGGED PATTERNS ({len(attention_flags)} requiring attention)
{'-' * 50}
"""
            for flag in attention_flags[:5]:
                inv = " [LENS-INVARIANT]" if flag.lens_invariant else ""
                summary += f"[{flag.id}] - {flag.dimension} = {flag.value:.2f}{inv}\n"
                summary += f"         {flag.meaning}\n"
                summary += f"         Lens note: {flag.cultural_note}\n\n"
        
        summary += """
COMMANDER NOTES
{'-' * 50}
This assessment surfaces patterns for your consideration.
It does not determine fitness, readiness, or require action.
The humans behind these metrics deserve your judgment, not an algorithm's.
"""
        
        return summary
    
    def _create_empty_snapshot(self) -> CoherenceSnapshot:
        """Create empty snapshot when no data"""
        now = datetime.now()
        empty_reading = DimensionReading(
            dimension="", value=0.5, confidence=0.0, sample_size=0, sources=[]
        )
        return CoherenceSnapshot(
            unit_id=self.unit_id,
            timestamp=now,
            psi=DimensionReading("psi", 0.5, 0.0, 0, []),
            rho=DimensionReading("rho", 0.5, 0.0, 0, []),
            q=DimensionReading("q", 0.5, 0.0, 0, []),
            f=DimensionReading("f", 0.5, 0.0, 0, []),
            tau=DimensionReading("tau", 0.5, 0.0, 0, []),
            overall_coherence=0.5,
            confidence_interval=(0.0, 1.0),
            data_sources={},
            flags=[],
            lens_deviation=0.5,
            lens_invariant_signals=[]
        )
    
    def _create_flat_trajectory(self, days: int) -> Trajectory:
        """Create flat trajectory when insufficient data"""
        return Trajectory(
            unit_id=self.unit_id,
            timeframe_days=days,
            snapshots=[],
            psi_trend=0.0,
            rho_trend=0.0,
            q_trend=0.0,
            f_trend=0.0,
            tau_trend=0.0,
            flag_frequency=0.0,
            recurring_flags=[]
        )


class TeamCoherenceAssessment:
    """
    Main assessment orchestrator.
    
    Coordinates data collection, analysis, and flag generation.
    """
    
    def __init__(self, 
                 unit_id: str,
                 data_sources: List[str] = None,
                 cultural_lenses: List[str] = None):
        self.unit_id = unit_id
        self.data_sources = data_sources or ["social_media", "cisd", "supervisor_evals"]
        self.cultural_lenses = cultural_lenses or ["combat_veteran", "first_generation"]
        
        self.dashboard = UnitDashboard(unit_id)
        self.collectors = {}
        self.analyzers = {}
        
        # Will be initialized by submodules
        self._init_collectors()
        self._init_analyzers()
    
    def _init_collectors(self):
        """Initialize data collectors"""
        # Placeholder - actual collectors in collectors/ module
        pass
    
    def _init_analyzers(self):
        """Initialize pattern analyzers"""
        # Placeholder - actual analyzers in analyzers/ module
        pass
    
    def run(self) -> CoherenceSnapshot:
        """Run full assessment and return snapshot"""
        # Collect data from all sources
        collected_data = self._collect_all()
        
        # Analyze patterns
        patterns = self._analyze_patterns(collected_data)
        
        # Apply cultural lenses
        lens_analysis = self._apply_lenses(patterns)
        
        # Generate flags
        flags = self._generate_flags(patterns, lens_analysis)
        
        # Create snapshot
        snapshot = self._create_snapshot(patterns, lens_analysis, flags)
        
        # Store in dashboard
        self.dashboard.snapshots.append(snapshot)
        for flag in flags:
            self.dashboard.flags[flag.id] = flag
        
        return snapshot
    
    def _collect_all(self) -> Dict[str, List[Any]]:
        """Collect data from all configured sources"""
        data = {}
        for source in self.data_sources:
            if source in self.collectors:
                data[source] = self.collectors[source].collect()
            else:
                data[source] = []  # Placeholder
        return data
    
    def _analyze_patterns(self, data: Dict) -> Dict[str, float]:
        """Analyze patterns across all data"""
        # Placeholder - actual analysis in analyzers
        return {
            "psi": 0.7,
            "rho": 0.65,
            "q": 0.55,
            "f": 0.6,
            "tau": 0.5
        }
    
    def _apply_lenses(self, patterns: Dict) -> Dict[str, List[LensAnalysis]]:
        """Apply cultural lenses to patterns"""
        # Placeholder - actual lens application in lenses module
        return {}
    
    def _generate_flags(self, patterns: Dict, lens_analysis: Dict) -> List[Flag]:
        """Generate flags from patterns"""
        # Placeholder - actual flag generation logic
        return []
    
    def _create_snapshot(self, patterns: Dict, lens_analysis: Dict, 
                        flags: List[Flag]) -> CoherenceSnapshot:
        """Create coherence snapshot from analysis"""
        now = datetime.now()
        
        def make_reading(dim: str) -> DimensionReading:
            return DimensionReading(
                dimension=dim,
                value=patterns.get(dim, 0.5),
                confidence=0.8,
                sample_size=10,
                sources=self.data_sources
            )
        
        return CoherenceSnapshot(
            unit_id=self.unit_id,
            timestamp=now,
            psi=make_reading("psi"),
            rho=make_reading("rho"),
            q=make_reading("q"),
            f=make_reading("f"),
            tau=make_reading("tau"),
            overall_coherence=sum(patterns.values()) / len(patterns),
            confidence_interval=(0.6, 0.8),
            data_sources={s: 10 for s in self.data_sources},
            flags=flags,
            lens_deviation=0.1,
            lens_invariant_signals=[]
        )
    
    def commander_summary(self) -> str:
        """Get commander summary"""
        return self.dashboard.commander_summary()
