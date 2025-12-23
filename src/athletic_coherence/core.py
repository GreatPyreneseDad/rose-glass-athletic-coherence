"""
Core Athletic Coherence Assessment Components
==============================================

Main classes for organizational physical coherence assessment.
Detects systemic patterns, not individual issues.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics


class FlagSeverity(Enum):
    """Severity levels for coherence flags"""
    INFO = "info"           # Pattern noted, no concern
    WATCH = "watch"         # Monitor trend
    ELEVATED = "elevated"   # Above normal, needs attention
    CRITICAL = "critical"   # Systemic issue, requires intervention


class PatternType(Enum):
    """Types of detected patterns"""
    INDIVIDUAL = "individual"   # Single player issue
    POSITIONAL = "positional"   # Position group pattern
    SYSTEMIC = "systemic"       # Organization-wide pattern
    PROTOCOL = "protocol"       # Training/recovery protocol issue


@dataclass
class InjuryRecord:
    """Single injury record"""
    player_id: str
    position: str
    position_group: str
    injury_type: str          # "soft_tissue", "structural", "chronic", "acute"
    body_part: str
    severity: str             # "minor", "moderate", "severe", "season_ending"
    date: datetime
    days_missed: int
    is_recurrence: bool = False
    previous_injury_id: Optional[str] = None


@dataclass
class TrainingLoad:
    """Training load data point"""
    player_id: str
    date: datetime
    load_score: float         # 0-10 scale
    intensity: float          # 0-1 scale
    duration_minutes: int
    session_type: str         # "practice", "conditioning", "recovery", "game"


@dataclass
class RecoveryMetric:
    """Recovery data point"""
    player_id: str
    date: datetime
    reported_readiness: float    # Player self-report 0-10
    objective_readiness: float   # Biometric/performance data 0-10
    sleep_quality: float         # 0-10
    soreness_level: float        # 0-10 (10 = severe)
    hrv: Optional[float] = None  # Heart rate variability


@dataclass
class SystemicFlag:
    """
    A flagged systemic pattern requiring organizational attention.
    
    Systemic flags indicate protocol-level or organization-level issues,
    not individual player problems.
    """
    id: str
    pattern_type: PatternType
    severity: FlagSeverity
    
    # Pattern details
    description: str
    affected_positions: List[str]
    affected_players_count: int
    seasons_observed: List[str]
    
    # Evidence
    data_points: int
    confidence: float
    
    # Analysis
    hypothesis: str           # Root cause hypothesis
    correlation_strength: float
    
    # Recommendations
    investigation_areas: List[str]
    
    # Timestamps
    first_detected: datetime
    last_updated: datetime
    
    def get_summary(self) -> str:
        """Executive summary of the flag"""
        return f"""
⚠️ SYSTEMIC FLAG: {self.id}
{'=' * 50}
Type: {self.pattern_type.value.upper()}
Severity: {self.severity.value.upper()}

PATTERN:
{self.description}

AFFECTED:
  Positions: {', '.join(self.affected_positions)}
  Players: {self.affected_players_count}
  Seasons: {', '.join(self.seasons_observed)}

ANALYSIS:
  Confidence: {self.confidence:.0%}
  Correlation: {self.correlation_strength:.2f}
  
HYPOTHESIS:
{self.hypothesis}

RECOMMENDED INVESTIGATION:
{chr(10).join(f'  • {area}' for area in self.investigation_areas)}
"""


@dataclass
class DimensionReading:
    """Single dimension reading with athletic context"""
    dimension: str
    value: float
    confidence: float
    athletic_interpretation: str
    trend: str  # "improving", "stable", "declining"


@dataclass
class CoherenceSnapshot:
    """Point-in-time coherence assessment for an organization"""
    organization_id: str
    timestamp: datetime
    seasons_analyzed: List[str]
    
    # Core dimensions (athletic context)
    psi_load_coherence: DimensionReading       # Training program consistency
    rho_history_integration: DimensionReading  # Learning from past injuries
    q_strain_accumulation: DimensionReading    # Physical stress on tissues
    f_team_protection: DimensionReading        # Disclosure environment safety
    tau_recovery_depth: DimensionReading       # Actual healing vs. RTP performance
    
    # Aggregate score
    physical_coherence_score: float
    confidence_interval: Tuple[float, float]
    
    # Data sources
    data_sources: Dict[str, int]
    
    # Flags
    systemic_flags: List[SystemicFlag]
    
    # Comparisons
    league_average: float
    year_over_year_trend: str
    
    def get_status(self, dimension: str) -> str:
        """Get status label for a dimension"""
        reading = getattr(self, dimension)
        
        if dimension == "q_strain_accumulation":
            # Higher is worse for strain
            if reading.value > 0.8:
                return "CRITICAL"
            elif reading.value > 0.6:
                return "ELEVATED"
            elif reading.value > 0.4:
                return "WATCH"
            return "NOMINAL"
        
        elif dimension == "tau_recovery_depth":
            # Lower is worse for recovery
            if reading.value < 0.3:
                return "CRITICAL"
            elif reading.value < 0.5:
                return "SHALLOW"
            elif reading.value < 0.7:
                return "WATCH"
            return "ADEQUATE"
        
        else:
            # Standard interpretation
            if reading.value < 0.4:
                return "CRITICAL"
            elif reading.value < 0.6:
                return "WATCH"
            elif reading.value > 0.8:
                return "STRONG"
            return "NOMINAL"


@dataclass
class PositionGroupAnalysis:
    """Analysis for a specific position group"""
    position_group: str
    injury_rate: float              # Injuries per player-season
    injury_rate_vs_league: float    # Multiplier vs. league average
    load_recovery_ratio: float      # Training load / recovery capacity
    soft_tissue_rate: float         # Soft tissue injuries specifically
    recurrence_rate: float          # Re-injury rate
    
    flags: List[str]
    recommendations: List[str]


class OrganizationDashboard:
    """
    Front office interface for organizational coherence.
    
    Provides snapshots, trends, systemic flags, and recommendations.
    """
    
    def __init__(self, org_id: str):
        self.org_id = org_id
        self.snapshots: List[CoherenceSnapshot] = []
        self.flags: Dict[str, SystemicFlag] = {}
        self.injury_records: List[InjuryRecord] = []
        self.training_data: List[TrainingLoad] = []
        self.recovery_data: List[RecoveryMetric] = []
    
    def get_snapshot(self) -> CoherenceSnapshot:
        """Get current coherence snapshot"""
        if not self.snapshots:
            return self._create_empty_snapshot()
        return self.snapshots[-1]
    
    def get_systemic_flags(self, min_severity: FlagSeverity = FlagSeverity.WATCH) -> List[SystemicFlag]:
        """Get systemic flags at or above severity level"""
        severity_order = [FlagSeverity.INFO, FlagSeverity.WATCH, 
                         FlagSeverity.ELEVATED, FlagSeverity.CRITICAL]
        min_idx = severity_order.index(min_severity)
        
        return [f for f in self.flags.values() 
                if severity_order.index(f.severity) >= min_idx]
    
    def get_position_group_analysis(self, position_group: str) -> PositionGroupAnalysis:
        """Get detailed analysis for a position group"""
        # Filter data for position group
        group_injuries = [i for i in self.injury_records 
                         if i.position_group == position_group]
        
        if not group_injuries:
            return PositionGroupAnalysis(
                position_group=position_group,
                injury_rate=0.0,
                injury_rate_vs_league=0.0,
                load_recovery_ratio=1.0,
                soft_tissue_rate=0.0,
                recurrence_rate=0.0,
                flags=[],
                recommendations=[]
            )
        
        # Calculate metrics
        total_injuries = len(group_injuries)
        soft_tissue = len([i for i in group_injuries 
                          if i.injury_type == "soft_tissue"])
        recurrences = len([i for i in group_injuries if i.is_recurrence])
        
        injury_rate = total_injuries / 3  # Per season (assuming 3 seasons)
        soft_tissue_rate = soft_tissue / total_injuries if total_injuries else 0
        recurrence_rate = recurrences / total_injuries if total_injuries else 0
        
        # Generate flags
        flags = []
        recommendations = []
        
        if soft_tissue_rate > 0.5:
            flags.append("High soft tissue injury rate")
            recommendations.append("Review training load and nutrition protocols")
        
        if recurrence_rate > 0.3:
            flags.append("High re-injury rate")
            recommendations.append("Extend recovery timelines, review RTP protocols")
        
        return PositionGroupAnalysis(
            position_group=position_group,
            injury_rate=injury_rate,
            injury_rate_vs_league=1.0,  # Would calculate vs. league data
            load_recovery_ratio=1.0,    # Would calculate from training data
            soft_tissue_rate=soft_tissue_rate,
            recurrence_rate=recurrence_rate,
            flags=flags,
            recommendations=recommendations
        )
    
    def executive_summary(self) -> str:
        """Generate executive summary for leadership"""
        snapshot = self.get_snapshot()
        systemic_flags = self.get_systemic_flags(FlagSeverity.ELEVATED)
        
        summary = f"""
ORGANIZATIONAL COHERENCE SUMMARY: {self.org_id.upper()}
{'=' * 60}
Assessment Date: {snapshot.timestamp.strftime('%Y-%m-%d')}
Seasons Analyzed: {', '.join(snapshot.seasons_analyzed)}
Data Sources: {', '.join(f"{v} {k}" for k, v in snapshot.data_sources.items())}

PHYSICAL COHERENCE SCORE: {snapshot.physical_coherence_score:.2f} / 1.0
{'⚠️ CRITICAL' if snapshot.physical_coherence_score < 0.4 else '⚡ WATCH' if snapshot.physical_coherence_score < 0.6 else '✓ NOMINAL'}

DIMENSION BREAKDOWN:
{'-' * 40}
Ψ (Load Coherence):      {snapshot.psi_load_coherence.value:.2f}  [{snapshot.get_status('psi_load_coherence')}]
   {snapshot.psi_load_coherence.athletic_interpretation}
   
ρ (History Integration): {snapshot.rho_history_integration.value:.2f}  [{snapshot.get_status('rho_history_integration')}]
   {snapshot.rho_history_integration.athletic_interpretation}
   
q (Strain Accumulation): {snapshot.q_strain_accumulation.value:.2f}  [{snapshot.get_status('q_strain_accumulation')}]
   {snapshot.q_strain_accumulation.athletic_interpretation}
   
f (Team Protection):     {snapshot.f_team_protection.value:.2f}  [{snapshot.get_status('f_team_protection')}]
   {snapshot.f_team_protection.athletic_interpretation}
   
τ (Recovery Depth):      {snapshot.tau_recovery_depth.value:.2f}  [{snapshot.get_status('tau_recovery_depth')}]
   {snapshot.tau_recovery_depth.athletic_interpretation}

YEAR-OVER-YEAR TREND: {snapshot.year_over_year_trend}
"""
        
        if systemic_flags:
            summary += f"""
SYSTEMIC FLAGS ({len(systemic_flags)} requiring attention)
{'-' * 40}
"""
            for flag in systemic_flags:
                summary += f"""
⚠️ {flag.description}
   Affected: {', '.join(flag.affected_positions)}
   Confidence: {flag.confidence:.0%}
   Hypothesis: {flag.hypothesis}
"""
        
        summary += """
WHAT THIS ASSESSMENT DOES NOT DETERMINE:
{'-' * 40}
• Individual player medical decisions
• Contract implications  
• Playing time allocation
• Personnel changes

The humans behind these metrics deserve your judgment, not an algorithm's.
"""
        
        return summary
    
    def _create_empty_snapshot(self) -> CoherenceSnapshot:
        """Create empty snapshot when no data"""
        now = datetime.now()
        
        def empty_reading(dim: str, interp: str) -> DimensionReading:
            return DimensionReading(
                dimension=dim,
                value=0.5,
                confidence=0.0,
                athletic_interpretation=interp,
                trend="stable"
            )
        
        return CoherenceSnapshot(
            organization_id=self.org_id,
            timestamp=now,
            seasons_analyzed=[],
            psi_load_coherence=empty_reading("psi", "Insufficient data"),
            rho_history_integration=empty_reading("rho", "Insufficient data"),
            q_strain_accumulation=empty_reading("q", "Insufficient data"),
            f_team_protection=empty_reading("f", "Insufficient data"),
            tau_recovery_depth=empty_reading("tau", "Insufficient data"),
            physical_coherence_score=0.5,
            confidence_interval=(0.0, 1.0),
            data_sources={},
            systemic_flags=[],
            league_average=0.5,
            year_over_year_trend="insufficient data"
        )


class PhysicalCoherenceScore:
    """
    Calculates aggregate physical coherence for an organization.
    """
    
    def __init__(self, organization: str):
        self.organization = organization
        self.weights = {
            'psi': 0.20,  # Load coherence
            'rho': 0.15,  # History integration
            'q': 0.25,    # Strain (inverted - high strain = low coherence)
            'f': 0.15,    # Team protection
            'tau': 0.25   # Recovery depth
        }
    
    def calculate(self, 
                  injury_history: List[InjuryRecord],
                  training_data: List[TrainingLoad],
                  recovery_data: List[RecoveryMetric],
                  nutrition_data: Optional[Dict] = None) -> CoherenceSnapshot:
        """Calculate comprehensive physical coherence score"""
        
        now = datetime.now()
        
        # Calculate each dimension
        psi = self._calculate_load_coherence(training_data)
        rho = self._calculate_history_integration(injury_history)
        q = self._calculate_strain_accumulation(training_data, injury_history)
        f = self._calculate_team_protection(recovery_data)
        tau = self._calculate_recovery_depth(recovery_data)
        
        # Aggregate score (q is inverted)
        score = (
            psi.value * self.weights['psi'] +
            rho.value * self.weights['rho'] +
            (1 - q.value) * self.weights['q'] +  # Invert q
            f.value * self.weights['f'] +
            tau.value * self.weights['tau']
        )
        
        # Detect systemic flags
        flags = self._detect_systemic_flags(injury_history, training_data, recovery_data)
        
        # Determine trend
        trend = self._determine_trend()
        
        return CoherenceSnapshot(
            organization_id=self.organization,
            timestamp=now,
            seasons_analyzed=self._get_seasons(injury_history),
            psi_load_coherence=psi,
            rho_history_integration=rho,
            q_strain_accumulation=q,
            f_team_protection=f,
            tau_recovery_depth=tau,
            physical_coherence_score=score,
            confidence_interval=(score - 0.1, score + 0.1),
            data_sources={
                "injury_records": len(injury_history),
                "training_sessions": len(training_data),
                "recovery_metrics": len(recovery_data)
            },
            systemic_flags=flags,
            league_average=0.55,  # Would calculate from league data
            year_over_year_trend=trend
        )
    
    def _calculate_load_coherence(self, training_data: List[TrainingLoad]) -> DimensionReading:
        """Calculate Ψ - training load coherence"""
        if not training_data:
            return DimensionReading(
                dimension="psi",
                value=0.5,
                confidence=0.0,
                athletic_interpretation="Insufficient training data",
                trend="unknown"
            )
        
        # Check for load consistency
        loads = [t.load_score for t in training_data]
        
        if len(loads) < 2:
            variance = 0.5
        else:
            variance = statistics.stdev(loads) / 10  # Normalize
        
        coherence = 1 - min(variance, 1)  # Lower variance = higher coherence
        
        if coherence < 0.5:
            interp = "Training program shows high variance - inconsistent loading"
        elif coherence < 0.7:
            interp = "Moderate training coherence - some periodization issues"
        else:
            interp = "Training program is coherent and consistent"
        
        return DimensionReading(
            dimension="psi",
            value=coherence,
            confidence=min(len(training_data) / 100, 1.0),
            athletic_interpretation=interp,
            trend="stable"
        )
    
    def _calculate_history_integration(self, injuries: List[InjuryRecord]) -> DimensionReading:
        """Calculate ρ - how well past injuries inform protocols"""
        if not injuries:
            return DimensionReading(
                dimension="rho",
                value=0.5,
                confidence=0.0,
                athletic_interpretation="Insufficient injury history",
                trend="unknown"
            )
        
        # Check recurrence rate
        recurrences = len([i for i in injuries if i.is_recurrence])
        recurrence_rate = recurrences / len(injuries)
        
        # Low recurrence = learning from history
        integration = 1 - recurrence_rate
        
        if integration < 0.5:
            interp = "High re-injury rate suggests protocols not learning from history"
        elif integration < 0.7:
            interp = "Moderate recurrence - some patterns repeating"
        else:
            interp = "Low recurrence rate - good integration of injury history"
        
        return DimensionReading(
            dimension="rho",
            value=integration,
            confidence=min(len(injuries) / 50, 1.0),
            athletic_interpretation=interp,
            trend="stable"
        )
    
    def _calculate_strain_accumulation(self, 
                                       training: List[TrainingLoad],
                                       injuries: List[InjuryRecord]) -> DimensionReading:
        """Calculate q - physical strain accumulation"""
        if not training:
            return DimensionReading(
                dimension="q",
                value=0.5,
                confidence=0.0,
                athletic_interpretation="Insufficient data for strain analysis",
                trend="unknown"
            )
        
        # Average load intensity
        avg_intensity = sum(t.intensity for t in training) / len(training)
        
        # Soft tissue injury rate (indicator of strain)
        soft_tissue = len([i for i in injuries if i.injury_type == "soft_tissue"])
        soft_tissue_rate = soft_tissue / max(len(injuries), 1)
        
        # Combine for strain score
        strain = (avg_intensity + soft_tissue_rate) / 2
        
        if strain > 0.7:
            interp = "Critical strain accumulation - tissues under maximum load"
        elif strain > 0.5:
            interp = "Elevated strain - approaching sustainable limits"
        else:
            interp = "Strain levels within sustainable range"
        
        return DimensionReading(
            dimension="q",
            value=strain,
            confidence=0.7,
            athletic_interpretation=interp,
            trend="stable"
        )
    
    def _calculate_team_protection(self, recovery: List[RecoveryMetric]) -> DimensionReading:
        """Calculate f - disclosure environment safety"""
        if not recovery:
            return DimensionReading(
                dimension="f",
                value=0.5,
                confidence=0.0,
                athletic_interpretation="Insufficient recovery data",
                trend="unknown"
            )
        
        # Gap between reported and objective readiness
        gaps = [abs(r.reported_readiness - r.objective_readiness) for r in recovery]
        avg_gap = sum(gaps) / len(gaps)
        
        # Low gap = athletes reporting honestly
        protection = 1 - (avg_gap / 10)  # Normalize to 0-1
        
        if protection < 0.5:
            interp = "Large gap between reported and objective readiness - disclosure environment may not feel safe"
        elif protection < 0.7:
            interp = "Moderate reporting gap - some performance of readiness"
        else:
            interp = "Athletes reporting honestly - safe disclosure environment"
        
        return DimensionReading(
            dimension="f",
            value=protection,
            confidence=min(len(recovery) / 100, 1.0),
            athletic_interpretation=interp,
            trend="stable"
        )
    
    def _calculate_recovery_depth(self, recovery: List[RecoveryMetric]) -> DimensionReading:
        """Calculate τ - actual recovery vs. quick RTP"""
        if not recovery:
            return DimensionReading(
                dimension="tau",
                value=0.5,
                confidence=0.0,
                athletic_interpretation="Insufficient recovery data",
                trend="unknown"
            )
        
        # Average objective readiness
        avg_readiness = sum(r.objective_readiness for r in recovery) / len(recovery)
        
        # Normalize to 0-1
        depth = avg_readiness / 10
        
        if depth < 0.4:
            interp = "Shallow recovery patterns - quick RTPs without full healing"
        elif depth < 0.6:
            interp = "Moderate recovery depth - some rushing evident"
        else:
            interp = "Adequate recovery depth - allowing time for healing"
        
        return DimensionReading(
            dimension="tau",
            value=depth,
            confidence=min(len(recovery) / 100, 1.0),
            athletic_interpretation=interp,
            trend="stable"
        )
    
    def _detect_systemic_flags(self,
                               injuries: List[InjuryRecord],
                               training: List[TrainingLoad],
                               recovery: List[RecoveryMetric]) -> List[SystemicFlag]:
        """Detect systemic patterns requiring organizational attention"""
        flags = []
        now = datetime.now()
        
        # Check for position group clustering
        position_groups = {}
        for injury in injuries:
            group = injury.position_group
            if group not in position_groups:
                position_groups[group] = []
            position_groups[group].append(injury)
        
        for group, group_injuries in position_groups.items():
            # High soft tissue rate in position group
            soft_tissue = [i for i in group_injuries if i.injury_type == "soft_tissue"]
            if len(soft_tissue) >= 3 and len(soft_tissue) / len(group_injuries) > 0.5:
                flags.append(SystemicFlag(
                    id=f"SYS-SOFT-{group.upper()}",
                    pattern_type=PatternType.POSITIONAL,
                    severity=FlagSeverity.ELEVATED,
                    description=f"High soft tissue injury rate in {group}",
                    affected_positions=[group],
                    affected_players_count=len(set(i.player_id for i in soft_tissue)),
                    seasons_observed=list(set(i.date.strftime("%Y") for i in soft_tissue)),
                    data_points=len(soft_tissue),
                    confidence=0.8,
                    hypothesis="Training load or nutrition protocol may not match metabolic demands for this position group",
                    correlation_strength=0.7,
                    investigation_areas=[
                        "Position-specific training load audit",
                        "Nutrition assessment (collagen, anti-inflammatory)",
                        "Recovery protocol review"
                    ],
                    first_detected=now,
                    last_updated=now
                ))
        
        # Check for recovery authenticity gap
        if recovery:
            gaps = [abs(r.reported_readiness - r.objective_readiness) for r in recovery]
            avg_gap = sum(gaps) / len(gaps)
            
            if avg_gap > 2.0:  # Gap > 2 points on 10-point scale
                flags.append(SystemicFlag(
                    id="SYS-DISCLOSURE",
                    pattern_type=PatternType.SYSTEMIC,
                    severity=FlagSeverity.CRITICAL,
                    description="Athletes performing readiness instead of honest reporting",
                    affected_positions=["All"],
                    affected_players_count=len(set(r.player_id for r in recovery)),
                    seasons_observed=[],
                    data_points=len(recovery),
                    confidence=0.85,
                    hypothesis="Disclosure environment may not feel safe - reporting pain may affect playing time",
                    correlation_strength=0.8,
                    investigation_areas=[
                        "Medical staff independence review",
                        "Playing time correlation with injury reports",
                        "Anonymous athlete survey on disclosure safety"
                    ],
                    first_detected=now,
                    last_updated=now
                ))
        
        return flags
    
    def _get_seasons(self, injuries: List[InjuryRecord]) -> List[str]:
        """Extract unique seasons from injury data"""
        return list(set(i.date.strftime("%Y") for i in injuries))
    
    def _determine_trend(self) -> str:
        """Determine year-over-year trend"""
        # Would calculate from historical data
        return "declining"


class AthleticCoherenceAssessment:
    """
    Main assessment orchestrator for athletic organizations.
    
    Coordinates data collection, analysis, and flag generation.
    """
    
    def __init__(self,
                 organization: str,
                 data_sources: List[str] = None,
                 seasons: List[str] = None):
        self.organization = organization
        self.data_sources = data_sources or ["injuries", "training", "recovery"]
        self.seasons = seasons or []
        
        self.dashboard = OrganizationDashboard(organization)
        self.scorer = PhysicalCoherenceScore(organization)
    
    def run(self) -> CoherenceSnapshot:
        """Run full assessment and return snapshot"""
        
        # In production, these would be loaded from actual data sources
        injuries = self._load_injury_data()
        training = self._load_training_data()
        recovery = self._load_recovery_data()
        
        # Calculate coherence
        snapshot = self.scorer.calculate(injuries, training, recovery)
        
        # Store in dashboard
        self.dashboard.snapshots.append(snapshot)
        self.dashboard.injury_records = injuries
        self.dashboard.training_data = training
        self.dashboard.recovery_data = recovery
        
        for flag in snapshot.systemic_flags:
            self.dashboard.flags[flag.id] = flag
        
        return snapshot
    
    def _load_injury_data(self) -> List[InjuryRecord]:
        """Load injury data from configured sources"""
        # Placeholder - actual implementation would connect to data sources
        return []
    
    def _load_training_data(self) -> List[TrainingLoad]:
        """Load training data from configured sources"""
        return []
    
    def _load_recovery_data(self) -> List[RecoveryMetric]:
        """Load recovery data from configured sources"""
        return []
    
    def executive_summary(self) -> str:
        """Get executive summary"""
        return self.dashboard.executive_summary()
    
    @property
    def systemic_flags(self) -> List[SystemicFlag]:
        """Get all systemic flags"""
        return self.dashboard.get_systemic_flags()
    
    @property
    def recommendations(self) -> List[str]:
        """Get aggregated recommendations from all flags"""
        recs = []
        for flag in self.systemic_flags:
            recs.extend(flag.investigation_areas)
        return list(set(recs))
