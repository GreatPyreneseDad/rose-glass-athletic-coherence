"""
Coherence Graph Service

Graph-based storage and analysis of user coherence profiles and influence patterns.
Integrates with Rose Looking Glass translation framework.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import statistics

from ..core import RoseLookingGlass, PatternVisibility


@dataclass
class UserCoherenceProfile:
    """
    Aggregated coherence profile for a user across all their communications.

    Built from Rose Looking Glass translations of user's text.
    """
    user_id: str
    total_messages: int

    # Average GCT variables
    avg_psi: float          # Average internal consistency
    avg_rho: float          # Average wisdom depth
    avg_q: float            # Average emotional activation
    avg_f: float            # Average social belonging

    # Volatility metrics (standard deviation)
    psi_volatility: float
    rho_volatility: float
    q_volatility: float
    f_volatility: float

    # Derived metrics
    avg_coherence: float    # Average overall coherence
    influence_score: float  # How much this user influences others (0-1)

    # Temporal
    first_seen: datetime
    last_seen: datetime


@dataclass
class CoherenceCascade:
    """
    A detected coherence cascade in the network.

    Represents rapid propagation of a coherence pattern (especially high-q)
    through influence connections.
    """
    id: str
    pattern_signature: Dict[str, float]  # The pattern that's cascading
    source_user: str
    affected_users: List[str]
    cascade_strength: float
    detected_at: datetime
    status: str  # "active", "stabilized", "dissipated"


class CoherenceGraphService:
    """
    Manages coherence patterns in a social network graph.

    Uses Rose Looking Glass to translate user communications into coherence
    patterns, then analyzes how these patterns influence and propagate
    through the network.

    Backend-agnostic interface - can be implemented with Neo4j, NetworkX,
    or any graph database.
    """

    def __init__(self, rose_glass: Optional[RoseLookingGlass] = None):
        """
        Initialize graph service.

        Args:
            rose_glass: RoseLookingGlass instance for translation
        """
        self.rose_glass = rose_glass or RoseLookingGlass()

        # In-memory storage (replace with graph DB in production)
        self.user_profiles: Dict[str, UserCoherenceProfile] = {}
        self.user_messages: Dict[str, List[PatternVisibility]] = {}
        self.influence_edges: List[Tuple[str, str, float]] = []  # (from, to, resonance)
        self.cascades: List[CoherenceCascade] = []

    async def add_user_message(
        self,
        user_id: str,
        text: str,
        timestamp: Optional[datetime] = None
    ) -> PatternVisibility:
        """
        Translate a user message through Rose Looking Glass and update profile.

        Args:
            user_id: User identifier
            text: Message text
            timestamp: When message was sent

        Returns:
            PatternVisibility from translation
        """
        # Translate through Rose Looking Glass
        visibility = self.rose_glass.translate_text(text)

        # Store message
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []
        self.user_messages[user_id].append(visibility)

        # Update user profile
        await self._update_user_profile(user_id, timestamp or datetime.now())

        return visibility

    async def _update_user_profile(self, user_id: str, timestamp: datetime):
        """Recompute user's coherence profile from all messages"""
        messages = self.user_messages.get(user_id, [])
        if not messages:
            return

        # Compute averages
        avg_psi = statistics.mean(m.psi for m in messages)
        avg_rho = statistics.mean(m.rho for m in messages)
        avg_q = statistics.mean(m.q for m in messages)
        avg_f = statistics.mean(m.f for m in messages)
        avg_coherence = statistics.mean(m.coherence for m in messages)

        # Compute volatility (stdev)
        psi_volatility = statistics.stdev([m.psi for m in messages]) if len(messages) > 1 else 0.0
        rho_volatility = statistics.stdev([m.rho for m in messages]) if len(messages) > 1 else 0.0
        q_volatility = statistics.stdev([m.q for m in messages]) if len(messages) > 1 else 0.0
        f_volatility = statistics.stdev([m.f for m in messages]) if len(messages) > 1 else 0.0

        # Compute influence score (placeholder - would use graph topology in production)
        influence_score = min(1.0, len(messages) / 100.0)  # Simple: more messages = more influence

        # Get or create profile
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            profile.total_messages = len(messages)
            profile.avg_psi = avg_psi
            profile.avg_rho = avg_rho
            profile.avg_q = avg_q
            profile.avg_f = avg_f
            profile.psi_volatility = psi_volatility
            profile.rho_volatility = rho_volatility
            profile.q_volatility = q_volatility
            profile.f_volatility = f_volatility
            profile.avg_coherence = avg_coherence
            profile.influence_score = influence_score
            profile.last_seen = timestamp
        else:
            profile = UserCoherenceProfile(
                user_id=user_id,
                total_messages=len(messages),
                avg_psi=avg_psi,
                avg_rho=avg_rho,
                avg_q=avg_q,
                avg_f=avg_f,
                psi_volatility=psi_volatility,
                rho_volatility=rho_volatility,
                q_volatility=q_volatility,
                f_volatility=f_volatility,
                avg_coherence=avg_coherence,
                influence_score=influence_score,
                first_seen=timestamp,
                last_seen=timestamp
            )
            self.user_profiles[user_id] = profile

    async def add_influence_edge(
        self,
        from_user: str,
        to_user: str,
        resonance: float
    ):
        """
        Record that from_user influences to_user with given resonance.

        Resonance = pattern similarity between users (0-1)
        High resonance = to_user's patterns match from_user's patterns
        """
        self.influence_edges.append((from_user, to_user, resonance))

    async def get_user_coherence_profile(
        self,
        user_id: str
    ) -> Optional[UserCoherenceProfile]:
        """Get aggregated coherence profile for a user"""
        return self.user_profiles.get(user_id)

    async def get_influence_topology(
        self,
        user_id: str,
        depth: int = 1
    ) -> Dict:
        """
        Get influence topology around a user.

        Returns:
            Dict with:
            - influencers: Users who influence this user
            - influenced: Users influenced by this user
            - resonance scores for each connection
        """
        # Who influences this user
        influencers = [
            {"user_id": from_user, "resonance": res}
            for from_user, to_user, res in self.influence_edges
            if to_user == user_id
        ]

        # Who this user influences
        influenced = [
            {"user_id": to_user, "resonance": res}
            for from_user, to_user, res in self.influence_edges
            if from_user == user_id
        ]

        return {
            "user_id": user_id,
            "influencers": influencers,
            "influenced": influenced
        }

    async def detect_coherence_cascades(
        self,
        min_affected: int = 5,
        min_strength: float = 0.6
    ) -> List[CoherenceCascade]:
        """
        Detect active coherence cascades in the network.

        A cascade is rapid propagation of a coherence pattern
        (especially high-q activation) through influence connections.

        Args:
            min_affected: Minimum users affected to qualify as cascade
            min_strength: Minimum cascade strength (0-1)

        Returns:
            List of detected cascades
        """
        # Simplified detection: find users with high q that influence others
        active_cascades = []

        for user_id, profile in self.user_profiles.items():
            if profile.avg_q > 0.7:  # High activation source
                # Find influenced users
                influenced = [
                    to_user for from_user, to_user, _ in self.influence_edges
                    if from_user == user_id
                ]

                if len(influenced) >= min_affected:
                    # Check if influenced users also have high q
                    influenced_profiles = [
                        self.user_profiles.get(u) for u in influenced
                        if u in self.user_profiles
                    ]

                    if influenced_profiles:
                        avg_influenced_q = statistics.mean(p.avg_q for p in influenced_profiles)
                        cascade_strength = min(1.0, avg_influenced_q)

                        if cascade_strength >= min_strength:
                            cascade = CoherenceCascade(
                                id=f"cascade_{user_id}_{int(datetime.now().timestamp())}",
                                pattern_signature={
                                    "psi": profile.avg_psi,
                                    "rho": profile.avg_rho,
                                    "q": profile.avg_q,
                                    "f": profile.avg_f
                                },
                                source_user=user_id,
                                affected_users=influenced,
                                cascade_strength=cascade_strength,
                                detected_at=datetime.now(),
                                status="active"
                            )
                            active_cascades.append(cascade)

        return active_cascades

    def calculate_pattern_resonance(
        self,
        profile1: UserCoherenceProfile,
        profile2: UserCoherenceProfile
    ) -> float:
        """
        Calculate resonance between two user profiles.

        Resonance = how similar their coherence patterns are.
        Uses Euclidean distance in 4D GCT space.

        Returns:
            Resonance score (0-1), where 1 = perfect match
        """
        # Euclidean distance in GCT space
        distance = (
            (profile1.avg_psi - profile2.avg_psi) ** 2 +
            (profile1.avg_rho - profile2.avg_rho) ** 2 +
            (profile1.avg_q - profile2.avg_q) ** 2 +
            (profile1.avg_f - profile2.avg_f) ** 2
        ) ** 0.5

        # Convert distance to resonance (0-1, where 1 = identical patterns)
        # Max possible distance in unit hypercube = 2.0
        max_distance = 2.0
        resonance = 1.0 - (distance / max_distance)

        return max(0.0, min(1.0, resonance))
