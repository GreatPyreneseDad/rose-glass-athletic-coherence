"""
Rose Looking Glass - Network Analysis Example
=============================================

Demonstrates coherence-based social network analysis using
Rose Looking Glass translation framework.
"""

import asyncio
from datetime import datetime
from src.network_analysis import (
    CoherenceGraphService,
    CoherenceInfluenceAnalyzer,
    InfluenceType
)


async def main():
    print("\n" + "="*70)
    print("Rose Looking Glass - Social Network Coherence Analysis")
    print("="*70 + "\n")

    # Initialize graph service
    graph = CoherenceGraphService()
    analyzer = CoherenceInfluenceAnalyzer(graph)

    # === Scenario 1: Building a network from user messages ===
    print("Scenario 1: Building User Coherence Profiles")
    print("-" * 70)

    # User A: High wisdom, low emotion (academic style)
    await graph.add_user_message(
        "user_a",
        "Based on extensive research, I conclude that this approach yields "
        "significantly more reliable results compared to previous methods."
    )
    await graph.add_user_message(
        "user_a",
        "The data demonstrates a clear correlation between the variables, "
        "therefore we can proceed with confidence."
    )

    # User B: High emotion, high social (activist style)
    await graph.add_user_message(
        "user_b",
        "We must stand together! Our community deserves better and we will "
        "fight for justice!"
    )
    await graph.add_user_message(
        "user_b",
        "I'm so angry about this injustice! Together we are stronger!"
    )

    # User C: High volatility (mixed patterns)
    await graph.add_user_message(
        "user_c",
        "I absolutely love this idea! It's amazing!"
    )
    await graph.add_user_message(
        "user_c",
        "Actually, I'm not sure. Maybe it's not so good after all."
    )
    await graph.add_user_message(
        "user_c",
        "Wait, I changed my mind again. This is definitely the way to go!"
    )

    # User D: Crisis/trauma pattern
    await graph.add_user_message(
        "user_d",
        "I'm terrified and don't know what to do. Everything is overwhelming "
        "and I desperately need help right now."
    )

    # User E: Calm, consistent (stabilizer pattern)
    await graph.add_user_message(
        "user_e",
        "Let's take a moment to breathe and think this through calmly."
    )
    await graph.add_user_message(
        "user_e",
        "I understand your concern. Let's approach this methodically and find "
        "a solution together."
    )

    print("\n✓ Added messages from 5 users\n")

    # === Display user profiles ===
    print("User Coherence Profiles:")
    print("-" * 70)

    for user_id in ["user_a", "user_b", "user_c", "user_d", "user_e"]:
        profile = await graph.get_user_coherence_profile(user_id)
        print(f"\n{user_id.upper()}:")
        print(f"  Messages: {profile.total_messages}")
        print(f"  Avg Ψ (consistency): {profile.avg_psi:.2f}")
        print(f"  Avg ρ (wisdom): {profile.avg_rho:.2f}")
        print(f"  Avg q (emotion): {profile.avg_q:.2f}")
        print(f"  Avg f (social): {profile.avg_f:.2f}")
        print(f"  q volatility: {profile.q_volatility:.2f}")
        print(f"  Avg coherence: {profile.avg_coherence:.2f}")

    # === Scenario 2: Add influence edges ===
    print("\n\n" + "="*70)
    print("Scenario 2: Modeling Influence Topology")
    print("-" * 70 + "\n")

    # User B influences User D (activist → crisis person)
    profile_b = await graph.get_user_coherence_profile("user_b")
    profile_d = await graph.get_user_coherence_profile("user_d")
    resonance_bd = graph.calculate_pattern_resonance(profile_b, profile_d)
    await graph.add_influence_edge("user_b", "user_d", resonance_bd)
    print(f"user_b → user_d (resonance: {resonance_bd:.2f})")

    # User E influences User D (stabilizer → crisis person)
    profile_e = await graph.get_user_coherence_profile("user_e")
    resonance_ed = graph.calculate_pattern_resonance(profile_e, profile_d)
    await graph.add_influence_edge("user_e", "user_d", resonance_ed)
    print(f"user_e → user_d (resonance: {resonance_ed:.2f})")

    # User A influences User E (academic → stabilizer)
    profile_a = await graph.get_user_coherence_profile("user_a")
    resonance_ae = graph.calculate_pattern_resonance(profile_a, profile_e)
    await graph.add_influence_edge("user_a", "user_e", resonance_ae)
    print(f"user_a → user_e (resonance: {resonance_ae:.2f})")

    # User C is influenced by both B and E (volatile person)
    profile_c = await graph.get_user_coherence_profile("user_c")
    resonance_bc = graph.calculate_pattern_resonance(profile_b, profile_c)
    resonance_ec = graph.calculate_pattern_resonance(profile_e, profile_c)
    await graph.add_influence_edge("user_b", "user_c", resonance_bc)
    await graph.add_influence_edge("user_e", "user_c", resonance_ec)
    print(f"user_b → user_c (resonance: {resonance_bc:.2f})")
    print(f"user_e → user_c (resonance: {resonance_ec:.2f})")

    # === Scenario 3: Analyze influence types ===
    print("\n\n" + "="*70)
    print("Scenario 3: Influence Type Analysis")
    print("-" * 70 + "\n")

    for user_id in ["user_a", "user_b", "user_c", "user_d", "user_e"]:
        try:
            analysis = await analyzer.analyze_user_influence(user_id)

            print(f"{user_id.upper()}: {analysis.influence_type.value.upper()}")
            print(f"  Influence score: {analysis.influence_score:.2f}")
            print(f"  Reach: {analysis.reach} users")
            if analysis.reach > 0:
                print(f"  Avg resonance: {analysis.avg_resonance:.2f}")
            print(f"  Pattern: Ψ={analysis.pattern_signature['psi']:.2f}, "
                  f"ρ={analysis.pattern_signature['rho']:.2f}, "
                  f"q={analysis.pattern_signature['q']:.2f}, "
                  f"f={analysis.pattern_signature['f']:.2f}")
            if analysis.risk_indicators:
                print(f"  ⚠️  Risks: {', '.join(analysis.risk_indicators)}")
            if analysis.recommendations:
                print(f"  💡 Recommendations:")
                for rec in analysis.recommendations:
                    print(f"     - {rec}")
            print()
        except ValueError as e:
            print(f"{user_id}: Error - {e}\n")

    # === Scenario 4: Detect cascades ===
    print("\n" + "="*70)
    print("Scenario 4: Cascade Detection")
    print("-" * 70 + "\n")

    cascades = await graph.detect_coherence_cascades(min_affected=1, min_strength=0.5)

    if cascades:
        print(f"Detected {len(cascades)} coherence cascade(s):\n")
        for cascade in cascades:
            print(f"Cascade ID: {cascade.id}")
            print(f"  Source: {cascade.source_user}")
            print(f"  Affected users: {len(cascade.affected_users)}")
            print(f"  Strength: {cascade.cascade_strength:.2f}")
            print(f"  Pattern: q={cascade.pattern_signature['q']:.2f}, "
                  f"f={cascade.pattern_signature['f']:.2f}")
            print(f"  Status: {cascade.status}")
            print()

            # Get intervention recommendations
            print("  Recommended interventions:")
            interventions = await analyzer.recommend_interventions(cascade.id)
            if interventions:
                for intervention in interventions:
                    print(f"    → {intervention['user_id']}: "
                          f"{intervention['recommendation']}")
                    print(f"      Resonance: {intervention['resonance_with_cascade']:.2f}")
            else:
                print("    → No stabilizers found in affected network")
            print()
    else:
        print("No cascades detected (network is stable)")

    # === Scenario 5: Network health metrics ===
    print("\n" + "="*70)
    print("Scenario 5: Network Health Metrics")
    print("-" * 70 + "\n")

    health = await analyzer.get_network_health_metrics()

    print(f"Total users: {health['total_users']}")
    print(f"Network coherence: {health['network_avg_coherence']:.2f}")
    print(f"Network Ψ (consistency): {health['network_avg_psi']:.2f}")
    print(f"Network ρ (wisdom): {health['network_avg_rho']:.2f}")
    print(f"Network q (emotion): {health['network_avg_q']:.2f}")
    print(f"Network q volatility: {health['network_q_volatility']:.2f}")
    print(f"Active cascades: {health['active_cascades']}")
    print("\nInfluence distribution:")
    for inf_type, count in health['influence_distribution'].items():
        if count > 0:
            print(f"  {inf_type}: {count}")

    # === Scenario 6: Find top influencers ===
    print("\n\n" + "="*70)
    print("Scenario 6: Top Influencers by Type")
    print("-" * 70 + "\n")

    print("Top Stabilizers:")
    stabilizers = await analyzer.find_top_influencers(
        influence_type=InfluenceType.STABILIZER,
        limit=3
    )
    for analysis in stabilizers:
        print(f"  {analysis.user_id}: score={analysis.influence_score:.2f}, "
              f"reach={analysis.reach}")

    print("\nTop Amplifiers:")
    amplifiers = await analyzer.find_top_influencers(
        influence_type=InfluenceType.AMPLIFIER,
        limit=3
    )
    for analysis in amplifiers:
        print(f"  {analysis.user_id}: score={analysis.influence_score:.2f}, "
              f"reach={analysis.reach}")

    print("\n" + "="*70)
    print("Network Analysis Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
