"""
Demo: Team Coherence Assessment
================================

Demonstrates the commander interface for team coherence assessment.
"""

import sys
sys.path.insert(0, 'src')

from team_coherence.core import (
    TeamCoherenceAssessment,
    UnitDashboard,
    Flag,
    FlagSeverity,
    Citation,
    LensAnalysis,
    DimensionReading,
    CoherenceSnapshot
)
from team_coherence.analyzers import CISDAnalyzer
from team_coherence.lenses import LensLibrary, LensDeviationCalculator
from datetime import datetime


def demo_cisd_analysis():
    """Demonstrate CISD report analysis"""
    
    print("=" * 60)
    print("CISD REPORT ANALYSIS DEMO")
    print("=" * 60)
    
    # Sample CISD report excerpts (anonymized)
    sample_reports = [
        # Authentic processing
        """
        The team discussed the incident openly. Several members shared that 
        they struggled with what happened. One participant realized they had 
        been carrying guilt that wasn't theirs. The facilitator noted strong 
        peer support and willingness to be vulnerable. Follow-up sessions 
        were requested by three participants.
        """,
        
        # Performance/masking
        """
        All participants reported they were fine and handling the situation 
        normally. No one expressed need for additional support. The session 
        was brief as most felt they had already moved on. Leadership was 
        present throughout.
        """,
        
        # Mixed signals
        """
        Initial responses were that everyone was fine and managing okay.
        However, later discussion revealed some were struggling but hadn't
        felt comfortable saying so. The mandatory nature of the session
        may have affected openness. Quiet during certain discussions.
        """
    ]
    
    analyzer = CISDAnalyzer()
    
    for i, report in enumerate(sample_reports, 1):
        print(f"\n--- Report {i} ---")
        result = analyzer.analyze(report)
        
        print(f"Processing ratio: {result.processing_ratio:.0%}")
        print(f"Performance ratio: {result.performance_ratio:.0%}")
        
        if result.environmental_concerns:
            print(f"Environmental concerns: {result.environmental_concerns}")
        
        print(f"Pattern: Ψ={result.pattern.psi:.2f}, q={result.pattern.q:.2f}, f={result.pattern.f:.2f}")
    
    # Program assessment
    print("\n" + "=" * 60)
    print("CISD PROGRAM ASSESSMENT (All Reports)")
    print("=" * 60)
    
    assessment = analyzer.assess_cisd_program(sample_reports)
    print(f"\nProcessing rate: {assessment['processing_rate']:.0%}")
    print(f"Performance rate: {assessment['performance_rate']:.0%}")
    print(f"Sample size: {assessment['sample_size']}")
    print(f"\nEnvironmental factors: {assessment['environmental_factors']}")
    print(f"\nRecommendation: {assessment['recommendation']}")


def demo_cultural_lenses():
    """Demonstrate cultural lens interpretation"""
    
    print("\n" + "=" * 60)
    print("CULTURAL LENS COMPARISON")
    print("=" * 60)
    
    # Same pattern, different lens interpretations
    psi, rho, q, f, tau = 0.75, 0.6, 0.35, 0.45, 0.5
    
    print(f"\nPattern: Ψ={psi}, ρ={rho}, q={q}, f={f}, τ={tau}")
    print("-" * 50)
    
    library = LensLibrary()
    calculator = LensDeviationCalculator(library)
    
    deviation, analysis = calculator.calculate_deviation(psi, rho, q, f, tau)
    
    print(f"\nLens deviation (σ): {deviation:.3f}")
    print(f"Lens-invariant: {analysis['is_lens_invariant']}")
    print(f"Coherence range: {analysis['coherence_range'][0]:.2f} - {analysis['coherence_range'][1]:.2f}")
    
    print("\nPer-lens interpretation:")
    for lens_name, interp in analysis['interpretations'].items():
        print(f"\n  {lens_name}:")
        print(f"    Coherence: {interp.coherence:.2f} (confidence: {interp.confidence:.2f})")
        if interp.notes:
            print(f"    Note: {interp.notes[0]}")
        if interp.concerns:
            print(f"    Concern: {interp.concerns[0]}")
    
    # Get translation notes
    print("\n" + "-" * 50)
    print("TRANSLATION NOTES FOR COMMANDER:")
    for note in calculator.get_translation_notes(analysis):
        print(f"  • {note}")


def demo_commander_dashboard():
    """Demonstrate commander dashboard output"""
    
    print("\n" + "=" * 60)
    print("COMMANDER DASHBOARD DEMO")
    print("=" * 60)
    
    dashboard = UnitDashboard("ALPHA_COMPANY")
    
    # Create sample snapshot with flags
    now = datetime.now()
    
    # Create a lens-invariant flag (all lenses agree - critical)
    critical_flag = Flag(
        id="F-001",
        member_id="ANON-127",
        dimension="f",
        value=0.23,
        threshold=0.40,
        severity=FlagSeverity.CRITICAL,
        citations=[
            Citation(
                source_type="social_media",
                source_id="post_8821",
                timestamp=now,
                excerpt="Been feeling like nobody gets it. Just me against...",
                confidence=0.85
            ),
            Citation(
                source_type="cisd",
                source_id="cisd_2025_01",
                timestamp=now,
                excerpt="Did not engage with group. Sat apart from team.",
                confidence=0.90
            )
        ],
        meaning="Isolation language increasing. Social connection patterns collapsing.",
        lens_analyses=[
            LensAnalysis("combat_veteran", 0.31, "Low f in unit-oriented member", 0.85),
            LensAnalysis("neurodivergent", 0.35, "Low f significant even for ND", 0.80)
        ],
        lens_invariant=True,
        cultural_note="All lenses agree this pattern indicates concern. Not a translation artifact.",
        trend="declining",
        gradient=-0.04,
        first_detected=now,
        last_updated=now
    )
    
    # Create context-dependent flag (lenses disagree)
    context_flag = Flag(
        id="F-002",
        member_id="ANON-089",
        dimension="q",
        value=0.72,
        threshold=0.65,
        severity=FlagSeverity.ATTENTION,
        citations=[
            Citation(
                source_type="supervisor",
                source_id="eval_2025_q1",
                timestamp=now,
                excerpt="Has been more vocal about frustrations lately",
                confidence=0.70
            )
        ],
        meaning="Emotional activation elevated above baseline",
        lens_analyses=[
            LensAnalysis("combat_veteran", 0.78, "High q unusual for stoic communicator", 0.82),
            LensAnalysis("first_generation", 0.55, "Within normal expression range", 0.75)
        ],
        lens_invariant=False,
        cultural_note="May be first-gen expression style - higher verbal emotional expression is cultural norm. Investigate background before action.",
        trend="rising",
        gradient=0.02,
        first_detected=now,
        last_updated=now
    )
    
    # Add to dashboard
    dashboard.flags["F-001"] = critical_flag
    dashboard.flags["F-002"] = context_flag
    
    # Create snapshot
    snapshot = CoherenceSnapshot(
        unit_id="ALPHA_COMPANY",
        timestamp=now,
        psi=DimensionReading("psi", 0.72, 0.85, 47, ["social", "cisd"]),
        rho=DimensionReading("rho", 0.68, 0.80, 35, ["debrief"]),
        q=DimensionReading("q", 0.61, 0.82, 52, ["social", "supervisor"]),
        f=DimensionReading("f", 0.58, 0.78, 47, ["social", "cisd"]),
        tau=DimensionReading("tau", 0.55, 0.75, 28, ["debrief"]),
        overall_coherence=0.63,
        confidence_interval=(0.58, 0.68),
        data_sources={
            "social_media_posts": 47,
            "cisd_reports": 3,
            "supervisor_evals": 12,
            "debrief_records": 8
        },
        flags=[critical_flag, context_flag],
        lens_deviation=0.08,
        lens_invariant_signals=["f-dimension collapse"]
    )
    
    dashboard.snapshots.append(snapshot)
    
    # Print summary
    print(dashboard.commander_summary())
    
    # Drill down on critical flag
    print("\n" + "=" * 60)
    print("FLAG DETAIL: F-001")
    print("=" * 60)
    print(critical_flag.get_summary())


if __name__ == "__main__":
    demo_cisd_analysis()
    demo_cultural_lenses()
    demo_commander_dashboard()
