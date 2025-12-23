"""
Coherence Influence Analyzer

Analyzes how users influence coherence patterns in social networks.
Replaces traditional PageRank sentiment influence with coherence-based
influence topology analysis using Rose Looking Glass translations.

Integration with Rose Looking Glass v2.1
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .coherence_graph import CoherenceGraphService, UserCoherenceProfile, CoherenceCascade


class InfluenceType(Enum):
    """Types of coherence influence in the network"""
    AMPLIFIER = "amplifier"      # Increases emotional activation in network
    STABILIZER = "stabilizer"    # Reduces volatility, increases consistency
    FRAGMENTER = "fragmenter"    # Decreases internal consistency
    RESONATOR = "resonator"      # Creates strong pattern matching
    DAMPENER = "dampener"        # Reduces overall activation
    WISDOM_SOURCE = "wisdom_source"  # High ρ influence, knowledge sharing


@dataclass
class InfluenceAnalysis:
    """
    Analysis of a user's influence on network coherence patterns.

    Based on Rose Looking Glass GCT variables (Ψ, ρ, q, f)
    rather than traditional sentiment metrics.
    """
    user_id: str
    influence_type: InfluenceType
    influence_score: float  # Overall influence magnitude (0-1)
    reach: int              # How many users directly affected
    avg_resonance: float    # Average pattern resonance with influenced users
    pattern_signature: Dict[str, float]  # User's coherence signature (Ψ, ρ, q, f)
    risk_indicators: List[str]  # Potential concerns
    recommendations: List[str]  # Suggested interventions or amplifications


class CoherenceInfluenceAnalyzer:
    """
    Analyzes how users influence coherence patterns in social networks.

    Unlike sentiment-based influence which tracks positive/negative spread,
    this analyzes:
    - Pattern amplification (who makes others more emotionally activated)
    - Pattern stabilization (who calms the network, increases consistency)
    - Coherence resonance (whose patterns others adopt)
    - Fragmentation risk (who decreases internal consistency)
    - Wisdom propagation (who shares knowledge, increases ρ)

    Integrates with Rose Looking Glass translation framework for
    multi-lens cultural interpretation.
    """

    def __init__(self, graph_service: CoherenceGraphService):
        """
        Initialize analyzer.

        Args:
            graph_service: CoherenceGraphService with user profiles and influence edges
        """
        self.graph = graph_service

    async def analyze_user_influence(
        self,
        user_id: str
    ) -> InfluenceAnalysis:
        """
        Analyze a user's influence on network coherence patterns.

        Returns comprehensive analysis including:
        - Influence type (amplifier, stabilizer, etc.)
        - Magnitude and reach
        - Pattern signature (GCT variables)
        - Risk indicators
        - Recommendations

        Args:
            user_id: User to analyze

        Returns:
            InfluenceAnalysis with complete assessment

        Raises:
            ValueError: If user not found
        """
        # Get user's coherence profile
        profile = await self.graph.get_user_coherence_profile(user_id)
        if not profile:
            raise ValueError(f"User not found: {user_id}")

        # Get influence topology
        topology = await self.graph.get_influence_topology(user_id, depth=2)

        # Analyze influenced users' patterns
        influenced_profiles = []
        for inf in topology["influenced"]:
            if inf["user_id"]:
                p = await self.graph.get_user_coherence_profile(inf["user_id"])
                if p:
                    influenced_profiles.append((p, inf["resonance"]))

        # Determine influence type
        influence_type = self._determine_influence_type(profile, influenced_profiles)

        # Calculate metrics
        avg_resonance = (
            sum(r for _, r in influenced_profiles) / len(influenced_profiles)
            if influenced_profiles else 0.0
        )

        # Identify risk indicators
        risk_indicators = self._identify_risks(profile, influenced_profiles)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            profile, influence_type, risk_indicators
        )

        return InfluenceAnalysis(
            user_id=user_id,
            influence_type=influence_type,
            influence_score=profile.influence_score,
            reach=len(influenced_profiles),
            avg_resonance=avg_resonance,
            pattern_signature={
                "psi": profile.avg_psi,
                "rho": profile.avg_rho,
                "q": profile.avg_q,
                "f": profile.avg_f
            },
            risk_indicators=risk_indicators,
            recommendations=recommendations
        )

    def _determine_influence_type(
        self,
        user_profile: UserCoherenceProfile,
        influenced: List[Tuple[UserCoherenceProfile, float]]
    ) -> InfluenceType:
        """
        Determine the type of influence this user has on the network.

        Based on:
        - User's own coherence pattern (Ψ, ρ, q, f)
        - Patterns of influenced users
        - Volatility characteristics

        Args:
            user_profile: The user's coherence profile
            influenced: List of (influenced_profile, resonance) tuples

        Returns:
            InfluenceType classification
        """

        if not influenced:
            return InfluenceType.RESONATOR  # Default for users without influence data

        # Calculate average patterns in influenced users
        avg_influenced_q = sum(p.avg_q for p, _ in influenced) / len(influenced)
        avg_influenced_psi = sum(p.avg_psi for p, _ in influenced) / len(influenced)
        avg_influenced_rho = sum(p.avg_rho for p, _ in influenced) / len(influenced)
        avg_influenced_volatility = sum(p.q_volatility for p, _ in influenced) / len(influenced)

        # High ρ user + influenced users have high ρ = wisdom source
        if user_profile.avg_rho > 0.7 and avg_influenced_rho > 0.6:
            return InfluenceType.WISDOM_SOURCE

        # High q user + high q influenced = amplifier
        if user_profile.avg_q > 0.6 and avg_influenced_q > 0.5:
            return InfluenceType.AMPLIFIER

        # Low volatility user + influenced users have low volatility = stabilizer
        if user_profile.q_volatility < 0.2 and avg_influenced_volatility < 0.3:
            return InfluenceType.STABILIZER

        # Low psi user + influenced have low psi = fragmenter
        if user_profile.avg_psi < 0.4 and avg_influenced_psi < 0.5:
            return InfluenceType.FRAGMENTER

        # Low q user + influenced have low q = dampener
        if user_profile.avg_q < 0.4 and avg_influenced_q < 0.4:
            return InfluenceType.DAMPENER

        # Default: resonator (neutral influence, pattern matching)
        return InfluenceType.RESONATOR

    def _identify_risks(
        self,
        user_profile: UserCoherenceProfile,
        influenced: List[Tuple[UserCoherenceProfile, float]]
    ) -> List[str]:
        """
        Identify risk indicators for this user's influence.

        Risks include:
        - High activation amplification (emotional contagion)
        - Volatility propagation
        - Fragmentation (decreased coherence)
        - Cascade potential (rapid spread)

        Args:
            user_profile: User's coherence profile
            influenced: Influenced users and resonance

        Returns:
            List of risk indicator strings
        """
        risks = []

        # High activation source (potential emotional contagion)
        if user_profile.avg_q > 0.7:
            risks.append("high_activation_source")

        # High volatility (unpredictable patterns)
        if user_profile.q_volatility > 0.4:
            risks.append("volatile_patterns")

        # Low consistency fragmenter with reach
        if user_profile.avg_psi < 0.3 and len(influenced) > 10:
            risks.append("fragmentation_risk")

        # Creates cascade potential (many high-resonance connections)
        high_resonance_influenced = [p for p, r in influenced if r > 0.7]
        if len(high_resonance_influenced) > 5:
            risks.append("cascade_potential")

        # Extreme social isolation or collectivism
        if user_profile.avg_f < 0.2:
            risks.append("isolated_pattern_source")
        elif user_profile.avg_f > 0.9:
            risks.append("groupthink_risk")

        return risks

    def _generate_recommendations(
        self,
        user_profile: UserCoherenceProfile,
        influence_type: InfluenceType,
        risks: List[str]
    ) -> List[str]:
        """
        Generate intervention or amplification recommendations.

        Args:
            user_profile: User's coherence profile
            influence_type: Classified influence type
            risks: Identified risk indicators

        Returns:
            List of actionable recommendations
        """
        recommendations = []

        # Amplifier recommendations
        if influence_type == InfluenceType.AMPLIFIER:
            if "cascade_potential" in risks:
                recommendations.append("Monitor for emotional contagion cascades")
            recommendations.append("Consider pairing with stabilizers to balance activation")

        # Stabilizer recommendations (positive influence)
        elif influence_type == InfluenceType.STABILIZER:
            recommendations.append("Amplify reach - valuable stabilizing influence")
            recommendations.append("Deploy during cascade events to calm network")

        # Fragmenter recommendations
        elif influence_type == InfluenceType.FRAGMENTER:
            recommendations.append("Monitor consistency impact on network")
            if len(risks) > 2:
                recommendations.append("Consider intervention to reduce fragmentation")

        # Wisdom source recommendations (positive influence)
        elif influence_type == InfluenceType.WISDOM_SOURCE:
            recommendations.append("Amplify reach - valuable knowledge sharing")
            recommendations.append("Encourage continued high-ρ contributions")

        # General risk-based recommendations
        if "high_activation_source" in risks:
            recommendations.append("Provide trauma-informed response options")

        if "volatile_patterns" in risks:
            recommendations.append("Offer consistency-building tools or prompts")

        return recommendations

    async def find_top_influencers(
        self,
        influence_type: Optional[InfluenceType] = None,
        limit: int = 10
    ) -> List[InfluenceAnalysis]:
        """
        Find top influencers in the network.

        Can filter by influence type to find:
        - Top amplifiers (who escalates emotional activation)
        - Top stabilizers (who calms things down)
        - Top fragmenters (who decreases coherence)
        - Top wisdom sources (who shares knowledge)

        Args:
            influence_type: Optional filter by type
            limit: Maximum results to return

        Returns:
            List of InfluenceAnalysis sorted by influence_score
        """
        all_analyses = []

        # Analyze all users
        for user_id in self.graph.user_profiles.keys():
            try:
                analysis = await self.analyze_user_influence(user_id)
                all_analyses.append(analysis)
            except ValueError:
                continue

        # Filter by type if specified
        if influence_type:
            all_analyses = [a for a in all_analyses if a.influence_type == influence_type]

        # Sort by influence score
        all_analyses.sort(key=lambda x: x.influence_score, reverse=True)

        return all_analyses[:limit]

    async def recommend_interventions(
        self,
        cascade_id: str
    ) -> List[Dict]:
        """
        Recommend interventions for an active coherence cascade.

        Finds users who could stabilize the cascade based on:
        - Their influence type (stabilizers)
        - Their resonance with affected users
        - Their reach in the affected network

        Args:
            cascade_id: ID of cascade to address

        Returns:
            List of intervention recommendations with user details
        """
        # Get cascade details
        cascades = await self.graph.detect_coherence_cascades()
        cascade = next((c for c in cascades if c.id == cascade_id), None)

        if not cascade:
            return []

        recommendations = []

        # Find stabilizers connected to affected users
        for affected_user in cascade.affected_users[:10]:  # Check top 10 affected
            topology = await self.graph.get_influence_topology(affected_user)

            for influencer in topology["influencers"]:
                if not influencer["user_id"]:
                    continue

                # Get influencer's profile
                profile = await self.graph.get_user_coherence_profile(
                    influencer["user_id"]
                )

                # Look for stabilizer characteristics
                if profile and profile.q_volatility < 0.2 and profile.avg_psi > 0.6:
                    recommendations.append({
                        "user_id": influencer["user_id"],
                        "influence_type": "stabilizer",
                        "avg_psi": profile.avg_psi,
                        "avg_q": profile.avg_q,
                        "resonance_with_cascade": influencer["resonance"],
                        "recommendation": "Engage to provide stabilizing counter-pattern",
                        "suggested_action": "Encourage high-Ψ, low-q communication"
                    })

        # Remove duplicates and sort by resonance
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec["user_id"] not in seen:
                seen.add(rec["user_id"])
                unique_recommendations.append(rec)

        unique_recommendations.sort(
            key=lambda x: x["resonance_with_cascade"],
            reverse=True
        )

        return unique_recommendations[:5]  # Return top 5

    async def get_network_health_metrics(self) -> Dict:
        """
        Compute overall network health metrics.

        Returns:
            Dict with network-level coherence statistics
        """
        all_profiles = list(self.graph.user_profiles.values())

        if not all_profiles:
            return {
                "total_users": 0,
                "network_avg_coherence": 0.0,
                "network_avg_q": 0.0,
                "network_q_volatility": 0.0,
                "active_cascades": 0,
                "influence_distribution": {}
            }

        # Compute network averages
        import statistics

        network_avg_coherence = statistics.mean(p.avg_coherence for p in all_profiles)
        network_avg_q = statistics.mean(p.avg_q for p in all_profiles)
        network_avg_psi = statistics.mean(p.avg_psi for p in all_profiles)
        network_avg_rho = statistics.mean(p.avg_rho for p in all_profiles)

        # Network volatility
        network_q_volatility = statistics.mean(p.q_volatility for p in all_profiles)

        # Count active cascades
        cascades = await self.graph.detect_coherence_cascades()
        active_cascades = len([c for c in cascades if c.status == "active"])

        # Influence type distribution
        influence_counts = {t.value: 0 for t in InfluenceType}
        for user_id in self.graph.user_profiles.keys():
            try:
                analysis = await self.analyze_user_influence(user_id)
                influence_counts[analysis.influence_type.value] += 1
            except ValueError:
                continue

        return {
            "total_users": len(all_profiles),
            "network_avg_coherence": round(network_avg_coherence, 3),
            "network_avg_psi": round(network_avg_psi, 3),
            "network_avg_rho": round(network_avg_rho, 3),
            "network_avg_q": round(network_avg_q, 3),
            "network_q_volatility": round(network_q_volatility, 3),
            "active_cascades": active_cascades,
            "influence_distribution": influence_counts
        }
