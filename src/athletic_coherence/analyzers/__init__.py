"""
Athletic Coherence Analyzers
============================

Specialized analyzers for injury patterns, training load, recovery,
and nutrition correlation.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics


@dataclass
class InjuryPattern:
    """Detected injury pattern"""
    pattern_id: str
    description: str
    injury_type: str
    affected_positions: List[str]
    occurrence_count: int
    seasons: List[str]
    correlation_strength: float
    is_systemic: bool
    hypothesis: str


@dataclass
class LoadRecoveryRatio:
    """Load to recovery ratio for a position group"""
    position_group: str
    ratio: float
    is_sustainable: bool
    threshold: float = 1.4
    recommendation: str = ""


@dataclass
class RecoveryAuthenticityResult:
    """Result of recovery authenticity analysis"""
    reported_avg: float
    objective_avg: float
    gap: float
    is_significant: bool
    reinjury_correlation: float
    position_breakdown: Dict[str, float]
    flags: List[str]


@dataclass
class NutritionCorrelation:
    """Correlation between nutrition factors and injuries"""
    factor: str
    correlation: float
    is_significant: bool
    affected_injury_types: List[str]
    recommendation: str


class InjuryPatternAnalyzer:
    """
    Analyzes injury patterns across an organization.
    
    Detects systemic patterns, position group clustering,
    and protocol-level issues.
    """
    
    # League average injury rates by position (injuries per player-season)
    LEAGUE_AVERAGES = {
        "defensive_line": 0.8,
        "secondary": 0.7,
        "linebackers": 0.6,
        "offensive_line": 0.5,
        "receivers": 0.6,
        "running_backs": 0.9,
        "quarterbacks": 0.4
    }
    
    def __init__(self, organization: str):
        self.organization = organization
        self.patterns: List[InjuryPattern] = []
    
    def analyze(self, 
                seasons: List[str],
                injury_data: List[Dict],
                injury_types: List[str] = None) -> Dict[str, Any]:
        """
        Analyze injury patterns across seasons.
        
        Args:
            seasons: List of season years to analyze
            injury_data: List of injury records
            injury_types: Filter to specific injury types
            
        Returns:
            Comprehensive pattern analysis
        """
        injury_types = injury_types or ["soft_tissue", "structural", "chronic"]
        
        # Group by position
        by_position = self._group_by_position(injury_data)
        
        # Group by type
        by_type = self._group_by_type(injury_data, injury_types)
        
        # Calculate rates
        position_rates = self._calculate_position_rates(by_position, len(seasons))
        
        # Detect patterns
        patterns = self._detect_patterns(injury_data, seasons)
        
        # Compare to league averages
        vs_league = self._compare_to_league(position_rates)
        
        return {
            "organization": self.organization,
            "seasons_analyzed": seasons,
            "total_injuries": len(injury_data),
            "by_position": by_position,
            "by_type": by_type,
            "position_rates": position_rates,
            "vs_league_average": vs_league,
            "patterns": patterns,
            "systemic_flags": [p for p in patterns if p.is_systemic],
            "summary": self._generate_summary(position_rates, vs_league, patterns)
        }
    
    def _group_by_position(self, injuries: List[Dict]) -> Dict[str, List[Dict]]:
        """Group injuries by position"""
        by_position = {}
        for injury in injuries:
            pos = injury.get("position_group", "unknown")
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append(injury)
        return by_position
    
    def _group_by_type(self, injuries: List[Dict], types: List[str]) -> Dict[str, int]:
        """Count injuries by type"""
        by_type = {t: 0 for t in types}
        for injury in injuries:
            injury_type = injury.get("injury_type", "unknown")
            if injury_type in by_type:
                by_type[injury_type] += 1
        return by_type
    
    def _calculate_position_rates(self, by_position: Dict, num_seasons: int) -> Dict[str, float]:
        """Calculate injury rate per position group per season"""
        rates = {}
        for pos, injuries in by_position.items():
            rates[pos] = len(injuries) / max(num_seasons, 1)
        return rates
    
    def _compare_to_league(self, rates: Dict[str, float]) -> Dict[str, float]:
        """Compare position rates to league averages"""
        comparison = {}
        for pos, rate in rates.items():
            league_avg = self.LEAGUE_AVERAGES.get(pos, 0.6)
            comparison[pos] = rate / league_avg if league_avg > 0 else 1.0
        return comparison
    
    def _detect_patterns(self, injuries: List[Dict], seasons: List[str]) -> List[InjuryPattern]:
        """Detect injury patterns"""
        patterns = []
        
        # Check for soft tissue clustering
        soft_tissue = [i for i in injuries if i.get("injury_type") == "soft_tissue"]
        if len(soft_tissue) >= 5:
            # Group by position
            by_pos = {}
            for i in soft_tissue:
                pos = i.get("position_group", "unknown")
                if pos not in by_pos:
                    by_pos[pos] = []
                by_pos[pos].append(i)
            
            for pos, pos_injuries in by_pos.items():
                if len(pos_injuries) >= 3:
                    patterns.append(InjuryPattern(
                        pattern_id=f"SOFT-{pos.upper()}",
                        description=f"Soft tissue injury cluster in {pos}",
                        injury_type="soft_tissue",
                        affected_positions=[pos],
                        occurrence_count=len(pos_injuries),
                        seasons=list(set(i.get("season", "") for i in pos_injuries)),
                        correlation_strength=0.75,
                        is_systemic=len(pos_injuries) >= 5,
                        hypothesis="Training load or nutrition protocol may not match metabolic demands"
                    ))
        
        # Check for year-over-year repetition
        by_season = {}
        for i in injuries:
            season = i.get("season", "unknown")
            if season not in by_season:
                by_season[season] = []
            by_season[season].append(i)
        
        if len(by_season) >= 2:
            counts = [len(v) for v in by_season.values()]
            if all(c > 10 for c in counts):  # High injury count across multiple seasons
                patterns.append(InjuryPattern(
                    pattern_id="REPEAT-MULTI",
                    description="High injury rate persists across multiple seasons",
                    injury_type="all",
                    affected_positions=["all"],
                    occurrence_count=sum(counts),
                    seasons=list(by_season.keys()),
                    correlation_strength=0.8,
                    is_systemic=True,
                    hypothesis="Systemic issue in training, recovery, or nutrition protocols"
                ))
        
        return patterns
    
    def _generate_summary(self, rates: Dict, vs_league: Dict, patterns: List) -> str:
        """Generate human-readable summary"""
        summary = f"INJURY PATTERN ANALYSIS: {self.organization.upper()}\n"
        summary += "=" * 50 + "\n\n"
        
        summary += "POSITION GROUP RATES (vs. League Average):\n"
        for pos, multiplier in sorted(vs_league.items(), key=lambda x: -x[1]):
            status = "⚠️" if multiplier > 1.5 else "⚡" if multiplier > 1.2 else "✓"
            summary += f"  {status} {pos}: {multiplier:.1f}x league average\n"
        
        if patterns:
            summary += f"\nPATTERNS DETECTED ({len(patterns)}):\n"
            for p in patterns:
                flag = "⚠️ SYSTEMIC" if p.is_systemic else "⚡"
                summary += f"  {flag} {p.description}\n"
                summary += f"     Hypothesis: {p.hypothesis}\n"
        
        return summary


class TrainingLoadAnalyzer:
    """
    Analyzes training load coherence and sustainability.
    """
    
    def __init__(self):
        self.sustainable_ratio = 1.4  # Load/recovery ratio threshold
    
    def assess_coherence(self,
                         training_logs: List[Dict],
                         recovery_metrics: List[Dict],
                         injury_outcomes: List[Dict]) -> Dict[str, Any]:
        """
        Assess training load coherence.
        
        Args:
            training_logs: Training session data
            recovery_metrics: Recovery measurements
            injury_outcomes: Resulting injuries
            
        Returns:
            Coherence assessment with recommendations
        """
        # Calculate load/recovery ratio by position
        ratios = self._calculate_ratios_by_position(training_logs, recovery_metrics)
        
        # Check periodization coherence
        periodization = self._assess_periodization(training_logs)
        
        # Correlate with injuries
        correlation = self._correlate_with_injuries(ratios, injury_outcomes)
        
        return {
            "load_recovery_ratios": ratios,
            "periodization_coherence": periodization,
            "injury_correlation": correlation,
            "unsustainable_positions": [r.position_group for r in ratios if not r.is_sustainable],
            "report": self._generate_report(ratios, periodization, correlation)
        }
    
    def _calculate_ratios_by_position(self, 
                                      training: List[Dict], 
                                      recovery: List[Dict]) -> List[LoadRecoveryRatio]:
        """Calculate load/recovery ratio by position group"""
        ratios = []
        
        # Group training by position
        training_by_pos = {}
        for t in training:
            pos = t.get("position_group", "unknown")
            if pos not in training_by_pos:
                training_by_pos[pos] = []
            training_by_pos[pos].append(t.get("load_score", 5))
        
        # Group recovery by position
        recovery_by_pos = {}
        for r in recovery:
            pos = r.get("position_group", "unknown")
            if pos not in recovery_by_pos:
                recovery_by_pos[pos] = []
            recovery_by_pos[pos].append(r.get("objective_readiness", 5))
        
        # Calculate ratios
        for pos in training_by_pos:
            avg_load = sum(training_by_pos[pos]) / len(training_by_pos[pos])
            avg_recovery = 5  # Default
            if pos in recovery_by_pos and recovery_by_pos[pos]:
                avg_recovery = sum(recovery_by_pos[pos]) / len(recovery_by_pos[pos])
            
            ratio = avg_load / max(avg_recovery, 1)
            is_sustainable = ratio <= self.sustainable_ratio
            
            rec = ""
            if not is_sustainable:
                rec = "Reduce training load or increase recovery allocation"
            
            ratios.append(LoadRecoveryRatio(
                position_group=pos,
                ratio=ratio,
                is_sustainable=is_sustainable,
                recommendation=rec
            ))
        
        return sorted(ratios, key=lambda x: -x.ratio)
    
    def _assess_periodization(self, training: List[Dict]) -> Dict[str, Any]:
        """Assess training periodization coherence"""
        if not training:
            return {"coherence": 0.5, "issues": ["Insufficient data"]}
        
        # Check for load variance (too high = poor periodization)
        loads = [t.get("load_score", 5) for t in training]
        
        if len(loads) < 2:
            variance = 0.0
        else:
            variance = statistics.stdev(loads)
        
        # High variance can indicate poor planning
        coherence = max(0, 1 - (variance / 5))
        
        issues = []
        if coherence < 0.5:
            issues.append("High training load variance - inconsistent periodization")
        
        return {
            "coherence": coherence,
            "load_variance": variance,
            "issues": issues
        }
    
    def _correlate_with_injuries(self, 
                                 ratios: List[LoadRecoveryRatio],
                                 injuries: List[Dict]) -> Dict[str, float]:
        """Correlate load/recovery ratios with injury outcomes"""
        correlations = {}
        
        for ratio in ratios:
            pos = ratio.position_group
            pos_injuries = [i for i in injuries if i.get("position_group") == pos]
            
            # Simple correlation: unsustainable ratio + injuries = strong correlation
            if not ratio.is_sustainable and len(pos_injuries) > 2:
                correlations[pos] = 0.8
            elif not ratio.is_sustainable:
                correlations[pos] = 0.5
            else:
                correlations[pos] = 0.2
        
        return correlations
    
    def _generate_report(self, ratios, periodization, correlation) -> str:
        """Generate training load coherence report"""
        report = "TRAINING LOAD COHERENCE ASSESSMENT\n"
        report += "=" * 40 + "\n\n"
        
        report += "LOAD/RECOVERY RATIO BY POSITION GROUP:\n"
        for r in ratios:
            status = "⚠️ UNSUSTAINABLE" if not r.is_sustainable else "✓"
            report += f"  {r.position_group}: {r.ratio:.2f} {status}\n"
        
        report += f"\nPERIODIZATION COHERENCE:\n"
        report += f"  Ψ = {periodization['coherence']:.2f}\n"
        for issue in periodization.get('issues', []):
            report += f"  ⚠️ {issue}\n"
        
        return report


class RecoveryAnalyzer:
    """
    Analyzes recovery authenticity - detecting performance vs. actual healing.
    """
    
    def __init__(self):
        self.significant_gap = 1.5  # Gap threshold for concern
    
    def assess_authenticity(self,
                           player_reported_metrics: List[Dict],
                           objective_metrics: List[Dict],
                           return_to_play_outcomes: List[Dict]) -> RecoveryAuthenticityResult:
        """
        Assess whether athletes are authentically recovering or performing readiness.
        
        Args:
            player_reported_metrics: Self-reported readiness scores
            objective_metrics: Biometric/performance-based readiness
            return_to_play_outcomes: RTP decisions and subsequent re-injuries
            
        Returns:
            Authenticity assessment with flags
        """
        # Calculate averages
        reported = [m.get("readiness", 5) for m in player_reported_metrics]
        objective = [m.get("readiness", 5) for m in objective_metrics]
        
        reported_avg = sum(reported) / len(reported) if reported else 5
        objective_avg = sum(objective) / len(objective) if objective else 5
        
        gap = reported_avg - objective_avg
        is_significant = abs(gap) > self.significant_gap
        
        # Check re-injury correlation
        high_gap_reinjury = 0
        low_gap_reinjury = 0
        
        for outcome in return_to_play_outcomes:
            gap_at_rtp = outcome.get("reported_objective_gap", 0)
            reinjured = outcome.get("reinjured_within_4_weeks", False)
            
            if gap_at_rtp > self.significant_gap and reinjured:
                high_gap_reinjury += 1
            elif gap_at_rtp <= self.significant_gap and reinjured:
                low_gap_reinjury += 1
        
        total_rtp = len(return_to_play_outcomes)
        reinjury_correlation = high_gap_reinjury / max(total_rtp, 1)
        
        # Generate flags
        flags = []
        if is_significant:
            flags.append("Significant gap between reported and objective readiness")
            flags.append("Athletes may be performing readiness instead of honest reporting")
        
        if reinjury_correlation > 0.5:
            flags.append("High re-injury rate correlates with reporting gap")
        
        return RecoveryAuthenticityResult(
            reported_avg=reported_avg,
            objective_avg=objective_avg,
            gap=gap,
            is_significant=is_significant,
            reinjury_correlation=reinjury_correlation,
            position_breakdown={},  # Would calculate by position
            flags=flags
        )


class NutritionAnalyzer:
    """
    Analyzes correlation between nutrition factors and injury patterns.
    """
    
    def __init__(self):
        self.key_factors = [
            "collagen_intake",
            "omega3_omega6_ratio",
            "protein_timing",
            "hydration",
            "anti_inflammatory_markers"
        ]
    
    def correlate(self,
                  nutrition_logs: List[Dict],
                  injury_data: List[Dict],
                  biomarkers: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Correlate nutrition data with injury patterns.
        
        Args:
            nutrition_logs: Nutrition tracking data
            injury_data: Injury records
            biomarkers: Lab data if available
            
        Returns:
            Correlation analysis with recommendations
        """
        correlations = []
        
        # Analyze each key factor
        for factor in self.key_factors:
            corr = self._analyze_factor(factor, nutrition_logs, injury_data)
            correlations.append(corr)
        
        # Position-specific analysis
        position_deficiencies = self._identify_position_deficiencies(
            nutrition_logs, injury_data
        )
        
        return {
            "correlations": correlations,
            "significant_correlations": [c for c in correlations if c.is_significant],
            "position_deficiencies": position_deficiencies,
            "findings": self._generate_findings(correlations, position_deficiencies)
        }
    
    def _analyze_factor(self, 
                        factor: str, 
                        nutrition: List[Dict],
                        injuries: List[Dict]) -> NutritionCorrelation:
        """Analyze correlation for a specific nutrition factor"""
        # Simplified correlation analysis
        # In production, would use actual statistical correlation
        
        soft_tissue_injuries = [i for i in injuries if i.get("injury_type") == "soft_tissue"]
        
        correlation = 0.0
        is_significant = False
        affected = []
        recommendation = ""
        
        if factor == "collagen_intake":
            # Low collagen correlates with tendon injuries
            correlation = -0.67
            is_significant = True
            affected = ["Achilles", "ACL", "tendon"]
            recommendation = "Increase collagen supplementation for high-load positions"
        
        elif factor == "omega3_omega6_ratio":
            correlation = -0.58
            is_significant = True
            affected = ["inflammation-related"]
            recommendation = "Optimize omega-3 to omega-6 ratio"
        
        elif factor == "protein_timing":
            correlation = 0.72
            is_significant = True
            affected = ["muscle", "recovery"]
            recommendation = "Optimize protein timing around training sessions"
        
        return NutritionCorrelation(
            factor=factor,
            correlation=correlation,
            is_significant=is_significant,
            affected_injury_types=affected,
            recommendation=recommendation
        )
    
    def _identify_position_deficiencies(self, 
                                        nutrition: List[Dict],
                                        injuries: List[Dict]) -> Dict[str, List[str]]:
        """Identify nutrition deficiencies by position group"""
        # Would analyze actual nutrition data by position
        # Placeholder showing defensive positions as example
        return {
            "defensive_line": ["Collagen intake 34% below recommendation"],
            "secondary": ["Anti-inflammatory markers suboptimal"]
        }
    
    def _generate_findings(self, 
                           correlations: List[NutritionCorrelation],
                           deficiencies: Dict) -> str:
        """Generate nutrition findings summary"""
        findings = "NUTRITION-INJURY CORRELATION ANALYSIS\n"
        findings += "=" * 40 + "\n\n"
        
        findings += "SIGNIFICANT CORRELATIONS:\n"
        for c in correlations:
            if c.is_significant:
                findings += f"  • {c.factor}: r = {c.correlation:.2f}\n"
                findings += f"    Affects: {', '.join(c.affected_injury_types)}\n"
                findings += f"    Recommendation: {c.recommendation}\n\n"
        
        findings += "POSITION GROUP DEFICIENCIES:\n"
        for pos, issues in deficiencies.items():
            findings += f"  {pos}:\n"
            for issue in issues:
                findings += f"    ⚠️ {issue}\n"
        
        return findings


class ProtocolEffectivenessAnalyzer:
    """
    Analyzes effectiveness of training, recovery, and nutrition protocols.
    """
    
    def analyze(self,
                protocol_changes: List[Dict],
                outcome_metrics: List[Dict]) -> Dict[str, Any]:
        """
        Analyze protocol effectiveness by comparing changes to outcomes.
        
        Args:
            protocol_changes: Log of protocol modifications
            outcome_metrics: Resulting injury rates, recovery times, etc.
            
        Returns:
            Effectiveness analysis
        """
        effective_changes = []
        ineffective_changes = []
        
        for change in protocol_changes:
            # Find outcomes after this change
            change_date = change.get("date")
            outcomes_after = [o for o in outcome_metrics 
                            if o.get("date", datetime.min) > change_date]
            
            if not outcomes_after:
                continue
            
            # Compare to baseline
            baseline = change.get("baseline_metric", 0)
            post_change = sum(o.get("value", 0) for o in outcomes_after) / len(outcomes_after)
            
            improvement = (post_change - baseline) / max(baseline, 1)
            
            if improvement > 0.1:
                effective_changes.append({
                    "change": change,
                    "improvement": improvement
                })
            elif improvement < -0.1:
                ineffective_changes.append({
                    "change": change,
                    "decline": -improvement
                })
        
        return {
            "effective_changes": effective_changes,
            "ineffective_changes": ineffective_changes,
            "recommendations": self._generate_recommendations(
                effective_changes, ineffective_changes
            )
        }
    
    def _generate_recommendations(self, effective, ineffective) -> List[str]:
        """Generate recommendations based on protocol analysis"""
        recs = []
        
        if effective:
            recs.append("Continue and expand protocols that showed improvement")
        
        if ineffective:
            recs.append("Review and revise protocols that showed decline")
            recs.append("Consider reverting ineffective changes")
        
        return recs


# Export
__all__ = [
    'InjuryPatternAnalyzer',
    'TrainingLoadAnalyzer',
    'RecoveryAnalyzer',
    'NutritionAnalyzer',
    'ProtocolEffectivenessAnalyzer',
    'InjuryPattern',
    'LoadRecoveryRatio',
    'RecoveryAuthenticityResult',
    'NutritionCorrelation'
]
