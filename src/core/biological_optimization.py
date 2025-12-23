"""
Rose Looking Glass - Biological Optimization
============================================

Implements biological saturation curves for GCT variables,
particularly the moral/emotional activation energy (q).

Prevents extreme interpretations and maintains balanced perception,
mirroring natural regulatory systems.
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class BiologicalParameters:
    """Parameters for biological optimization curve"""
    Km: float = 0.3  # Half-saturation constant
    Ki: float = 2.0  # Inhibition constant
    max_q: float = 0.95  # Maximum allowed q value


class BiologicalOptimizer:
    """
    Applies biological saturation curves to prevent extreme values.

    Based on Michaelis-Menten enzyme kinetics with substrate inhibition:

    q_opt = q / (Km + q + q²/Ki)

    This creates a curve that:
    - Allows linear growth at low values
    - Saturates at moderate values (prevents runaway activation)
    - Decreases at very high values (substrate inhibition)

    Just as biological systems protect against overstimulation,
    this prevents the lens from seeing extreme emotional states
    that would distort interpretation.
    """

    def __init__(self, params: Optional[BiologicalParameters] = None):
        """
        Initialize optimizer with parameters.

        Args:
            params: BiologicalParameters or None for defaults
        """
        self.params = params or BiologicalParameters()

    def optimize_q(self, q: float) -> float:
        """
        Apply biological optimization to emotional activation (q).

        The curve shape:
        - 0.0 → 0.0 (no activation remains none)
        - 0.3 → ~0.5 (moderate activation)
        - 0.6 → ~0.6 (approaching saturation)
        - 0.9 → ~0.5 (substrate inhibition kicks in)

        This mirrors how biological systems regulate to prevent damage
        from excessive stimulation.

        Args:
            q: Raw emotional activation (0-1)

        Returns:
            Optimized q value (0-max_q)
        """
        if q <= 0:
            return 0.0

        Km = self.params.Km
        Ki = self.params.Ki

        # Michaelis-Menten with substrate inhibition
        denominator = Km + q + (q ** 2) / Ki

        if denominator == 0:
            return 0.0

        q_optimized = q / denominator

        # Clamp to maximum
        return min(q_optimized, self.params.max_q)

    def optimize_all(self, psi: float, rho: float, q: float, f: float) -> dict:
        """
        Apply optimization to all variables.

        Currently only q uses the biological curve.
        Other variables use simple clamping.

        Returns:
            Dict with optimized values
        """
        return {
            'psi': max(0.0, min(1.0, psi)),  # Simple clamp
            'rho': max(0.0, min(1.0, rho)),  # Simple clamp
            'q': self.optimize_q(q),          # Biological curve
            'f': max(0.0, min(1.0, f))       # Simple clamp
        }

    def get_saturation_curve(self, num_points: int = 100) -> list:
        """
        Generate the saturation curve for visualization.

        Returns:
            List of (q_raw, q_optimized) tuples
        """
        points = []
        for i in range(num_points + 1):
            q_raw = i / num_points
            q_opt = self.optimize_q(q_raw)
            points.append((q_raw, q_opt))
        return points

    def explain_optimization(self, q_raw: float) -> str:
        """
        Explain what happened during optimization.

        Args:
            q_raw: The raw q value before optimization

        Returns:
            Human-readable explanation
        """
        q_opt = self.optimize_q(q_raw)
        delta = q_opt - q_raw

        if abs(delta) < 0.05:
            return f"No significant change (q: {q_raw:.2f} → {q_opt:.2f})"

        elif delta > 0:
            return (f"Amplified moderate activation "
                   f"(q: {q_raw:.2f} → {q_opt:.2f}, +{delta:.2f})")

        else:
            return (f"Dampened extreme activation to prevent distortion "
                   f"(q: {q_raw:.2f} → {q_opt:.2f}, {delta:.2f})")


# Alternative biological models for future exploration

class LogisticOptimizer:
    """
    Alternative: Logistic growth curve.

    S-shaped curve that saturates smoothly without inhibition.
    May be more appropriate for certain cultural lenses.
    """

    def __init__(self, L: float = 1.0, k: float = 5.0, x0: float = 0.5):
        """
        Args:
            L: Maximum value (carrying capacity)
            k: Steepness of curve
            x0: Midpoint of sigmoid
        """
        self.L = L
        self.k = k
        self.x0 = x0

    def optimize_q(self, q: float) -> float:
        """Apply logistic growth curve"""
        return self.L / (1 + math.exp(-self.k * (q - self.x0)))


class HillOptimizer:
    """
    Alternative: Hill equation (cooperative binding).

    Used in biochemistry for cooperative processes.
    Creates sharper transitions than logistic.
    """

    def __init__(self, Kd: float = 0.5, n: float = 2.0, max_val: float = 1.0):
        """
        Args:
            Kd: Dissociation constant (midpoint)
            n: Hill coefficient (cooperativity)
            max_val: Maximum value
        """
        self.Kd = Kd
        self.n = n
        self.max_val = max_val

    def optimize_q(self, q: float) -> float:
        """Apply Hill equation"""
        if q <= 0:
            return 0.0

        numerator = self.max_val * (q ** self.n)
        denominator = (self.Kd ** self.n) + (q ** self.n)

        return numerator / denominator


# Factory for creating optimizers
def create_optimizer(model: str = 'michaelis_menten',
                     **kwargs) -> BiologicalOptimizer:
    """
    Factory function for creating biological optimizers.

    Args:
        model: 'michaelis_menten', 'logistic', or 'hill'
        **kwargs: Parameters for the chosen model

    Returns:
        Optimizer instance
    """
    if model == 'michaelis_menten':
        params = BiologicalParameters(**kwargs) if kwargs else None
        return BiologicalOptimizer(params)

    elif model == 'logistic':
        return LogisticOptimizer(**kwargs)

    elif model == 'hill':
        return HillOptimizer(**kwargs)

    else:
        raise ValueError(f"Unknown optimizer model: {model}")
