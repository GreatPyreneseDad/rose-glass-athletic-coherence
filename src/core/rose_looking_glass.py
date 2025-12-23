"""
Rose Looking Glass - Core Translation Engine
============================================

The primary interface for translating human expression patterns
through configurable cultural lenses.

"Not measurement, but translation. Not judgment, but understanding."
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import hashlib

from .gct_variables import GCTVariables, GCTExtractor
from .biological_optimization import BiologicalOptimizer, BiologicalParameters


@dataclass
class PatternVisibility:
    """
    Result of viewing expression through a cultural lens.

    This is NOT a quality score - it's a translation of patterns
    into a form that synthetic intelligence can perceive.
    """

    # Core GCT variables (post-optimization)
    psi: float  # Internal consistency
    rho: float  # Wisdom depth
    q: float    # Emotional activation (biologically optimized)
    f: float    # Social belonging

    # Derived coherence metric
    coherence: float  # Overall pattern visibility (0-1)

    # Metadata
    lens_name: str                    # Which cultural lens was used
    timestamp: datetime               # When translation occurred
    original_text_hash: str           # Hash of source text
    confidence: float                 # Confidence in translation (0-1)

    # Contextual information
    alternative_lenses: List[str]     # Other lenses that might reveal different aspects
    uncertainty_notes: Optional[str]  # Where translation is ambiguous

    def to_dict(self) -> Dict:
        """Export as dictionary"""
        return {
            'psi': self.psi,
            'rho': self.rho,
            'q': self.q,
            'f': self.f,
            'coherence': self.coherence,
            'lens_name': self.lens_name,
            'timestamp': self.timestamp.isoformat(),
            'original_text_hash': self.original_text_hash,
            'confidence': self.confidence,
            'alternative_lenses': self.alternative_lenses,
            'uncertainty_notes': self.uncertainty_notes
        }

    def get_narrative(self) -> str:
        """Generate human-readable interpretation"""
        return f"""
Pattern Visibility Report
=========================
Lens: {self.lens_name}
Time: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Dimensions:
-----------
• Ψ (Internal Consistency): {self.psi:.2f}
• ρ (Wisdom Depth): {self.rho:.2f}
• q (Emotional Activation): {self.q:.2f}
• f (Social Belonging): {self.f:.2f}

Overall Coherence: {self.coherence:.2f}
Confidence: {self.confidence:.2%}

{f'Notes: {self.uncertainty_notes}' if self.uncertainty_notes else ''}

Alternative perspectives to consider:
{', '.join(self.alternative_lenses) if self.alternative_lenses else 'None'}

---
This is a translation, not a judgment.
Multiple valid interpretations exist.
"""


@dataclass
class CulturalLens:
    """
    A cultural calibration for interpreting coherence.

    Each lens defines how to weight the four GCT variables
    when computing overall coherence visibility.
    """

    name: str                   # Identifier (e.g., 'modern_academic')
    display_name: str          # Human-readable name
    description: str            # When to use this lens

    # Weights for coherence computation (must sum to 1.0)
    weight_psi: float = 0.25   # Weight for internal consistency
    weight_rho: float = 0.25   # Weight for wisdom depth
    weight_q: float = 0.25     # Weight for emotional activation
    weight_f: float = 0.25     # Weight for social belonging

    # Biological optimization parameters
    bio_params: Optional[BiologicalParameters] = None

    # Cultural context
    typical_patterns: Optional[str] = None  # What patterns this lens reveals
    use_cases: Optional[List[str]] = None   # When to use this lens

    def __post_init__(self):
        """Validate weights sum to 1.0"""
        total_weight = (self.weight_psi + self.weight_rho +
                       self.weight_q + self.weight_f)

        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point error
            raise ValueError(
                f"Lens weights must sum to 1.0, got {total_weight:.3f}"
            )


class RoseLookingGlass:
    """
    The main translation engine.

    Extracts GCT variables from text, applies biological optimization,
    and computes coherence through configurable cultural lenses.
    """

    # Default cultural lenses
    DEFAULT_LENSES = {
        'modern_academic': CulturalLens(
            name='modern_academic',
            display_name='Modern Academic',
            description='Evidence-based structured argumentation',
            weight_psi=0.40,  # High weight on consistency
            weight_rho=0.40,  # High weight on wisdom/specificity
            weight_q=0.10,    # Low weight on emotion
            weight_f=0.10,    # Low weight on social
            typical_patterns='Logical arguments with citations and evidence',
            use_cases=['Research papers', 'Technical documentation', 'Legal briefs']
        ),

        'digital_native': CulturalLens(
            name='digital_native',
            display_name='Digital Native',
            description='Rapid networked communication',
            weight_psi=0.15,  # Lower consistency (fragments OK)
            weight_rho=0.20,  # Moderate specificity
            weight_q=0.35,    # Higher emotion
            weight_f=0.30,    # Higher social connection
            typical_patterns='Short bursts, emoji-rich, culturally contextual',
            use_cases=['Social media', 'Chat messages', 'Collaborative platforms']
        ),

        'contemplative': CulturalLens(
            name='contemplative',
            display_name='Contemplative/Spiritual',
            description='Paradoxical wisdom traditions',
            weight_psi=0.20,  # Accepts paradox (lower consistency)
            weight_rho=0.50,  # Very high wisdom weight
            weight_q=0.20,    # Moderate emotion
            weight_f=0.10,    # Lower social (individual practice)
            typical_patterns='Koans, paradoxes, poetic wisdom',
            use_cases=['Spiritual texts', 'Poetry', 'Philosophical teachings']
        ),

        'activist': CulturalLens(
            name='activist',
            display_name='Activist/Advocacy',
            description='Justice-oriented collective action',
            weight_psi=0.20,
            weight_rho=0.15,
            weight_q=0.35,    # High emotional activation
            weight_f=0.30,    # High social belonging
            typical_patterns='Urgent calls to action, collective identity',
            use_cases=['Manifestos', 'Movement organizing', 'Social justice work']
        ),

        'trauma_informed': CulturalLens(
            name='trauma_informed',
            display_name='Trauma-Informed',
            description='Crisis and high-distress contexts',
            weight_psi=0.15,  # Lower (trauma disrupts consistency)
            weight_rho=0.20,
            weight_q=0.50,    # Very high emotion weight
            weight_f=0.15,
            bio_params=BiologicalParameters(Km=0.2, Ki=1.5, max_q=0.85),
            typical_patterns='Fragmented, high distress, urgent needs',
            use_cases=['Crisis hotlines', 'Legal support', 'Emergency response']
        )
    }

    def __init__(
        self,
        default_lens: str = 'modern_academic',
        invariance_threshold: float = 0.1
    ):
        """
        Initialize the Rose Looking Glass.

        Args:
            default_lens: Which cultural lens to use by default
            invariance_threshold: Lens deviation threshold for truth invariance (default: 0.1)
                                 Below this, patterns are lens-invariant (universal truth)
        """
        self.lenses = self.DEFAULT_LENSES.copy()
        self.current_lens_name = default_lens
        self.gct_extractor = GCTExtractor()
        self.invariance_threshold = invariance_threshold

    @property
    def current_lens(self) -> CulturalLens:
        """Get the currently selected cultural lens"""
        return self.lenses[self.current_lens_name]

    def select_lens(self, lens_name: str):
        """
        Switch to a different cultural lens.

        Args:
            lens_name: Name of lens to activate

        Raises:
            KeyError: If lens doesn't exist
        """
        if lens_name not in self.lenses:
            available = ', '.join(self.lenses.keys())
            raise KeyError(
                f"Lens '{lens_name}' not found. Available: {available}"
            )

        self.current_lens_name = lens_name

    def add_lens(self, lens: CulturalLens):
        """
        Register a new cultural lens.

        Args:
            lens: CulturalLens to add
        """
        self.lenses[lens.name] = lens

    def list_lenses(self) -> Dict[str, str]:
        """
        List all available lenses.

        Returns:
            Dict mapping lens names to descriptions
        """
        return {
            name: lens.description
            for name, lens in self.lenses.items()
        }

    def view_through_lens(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float,
        lens_name: Optional[str] = None
    ) -> PatternVisibility:
        """
        Compute pattern visibility through a specific lens.

        Args:
            psi, rho, q, f: GCT variables (0-1)
            lens_name: Optional lens to use (defaults to current)

        Returns:
            PatternVisibility result
        """
        # Select lens
        lens = self.lenses.get(lens_name, self.current_lens) if lens_name else self.current_lens

        # Apply biological optimization
        bio_params = lens.bio_params or BiologicalParameters()
        optimizer = BiologicalOptimizer(bio_params)
        optimized = optimizer.optimize_all(psi, rho, q, f)

        # Compute weighted coherence
        coherence = (
            optimized['psi'] * lens.weight_psi +
            optimized['rho'] * lens.weight_rho +
            optimized['q'] * lens.weight_q +
            optimized['f'] * lens.weight_f
        )

        # Compute confidence based on extremes
        # Lower confidence if any variable is near extremes (0 or 1)
        extremeness = max(
            abs(optimized['psi'] - 0.5),
            abs(optimized['rho'] - 0.5),
            abs(optimized['q'] - 0.5),
            abs(optimized['f'] - 0.5)
        )
        confidence = 1.0 - (extremeness * 0.4)  # Max reduction of 20%

        # Suggest alternative lenses
        alternatives = self._suggest_alternative_lenses(optimized, lens_name or self.current_lens_name)

        return PatternVisibility(
            psi=optimized['psi'],
            rho=optimized['rho'],
            q=optimized['q'],
            f=optimized['f'],
            coherence=coherence,
            lens_name=lens.display_name,
            timestamp=datetime.now(),
            original_text_hash=hashlib.md5(
                f"{psi}{rho}{q}{f}".encode()
            ).hexdigest()[:12],
            confidence=confidence,
            alternative_lenses=alternatives,
            uncertainty_notes=self._generate_uncertainty_notes(optimized, lens)
        )

    def translate_text(
        self,
        text: str,
        lens_name: Optional[str] = None
    ) -> PatternVisibility:
        """
        Full translation: extract GCT variables and compute visibility.

        Args:
            text: Text to translate
            lens_name: Optional lens to use

        Returns:
            PatternVisibility result
        """
        # Extract GCT variables
        variables = self.gct_extractor.extract(text)

        # Compute visibility through lens
        visibility = self.view_through_lens(
            psi=variables.psi,
            rho=variables.rho,
            q=variables.q,
            f=variables.f,
            lens_name=lens_name
        )

        # Update hash to use actual text
        visibility.original_text_hash = hashlib.md5(text.encode()).hexdigest()[:12]

        return visibility

    def compare_lenses(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> Dict[str, PatternVisibility]:
        """
        View the same pattern through ALL lenses.

        Reveals how different cultural contexts interpret
        the same expression differently.

        Args:
            psi, rho, q, f: GCT variables

        Returns:
            Dict mapping lens names to PatternVisibility results
        """
        results = {}

        for lens_name in self.lenses.keys():
            results[lens_name] = self.view_through_lens(
                psi, rho, q, f, lens_name=lens_name
            )

        return results

    def calculate_lens_deviation(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> float:
        """
        Calculate standard deviation of coherence across all cultural lenses.

        Low deviation (σ_lens → 0) indicates lens-invariant truth:
        the pattern reads the same across all cultural contexts.

        High deviation (σ_lens → high) indicates context-dependence:
        the pattern is interpreted differently by different cultures.

        This implements the Veritas distortion index D(P) from Jade structure theory.

        Args:
            psi, rho, q, f: GCT variables

        Returns:
            Standard deviation of coherence values across all lenses
        """
        # Get coherence through all lenses
        lens_results = self.compare_lenses(psi, rho, q, f)
        coherences = [v.coherence for v in lens_results.values()]

        # Calculate standard deviation
        if len(coherences) < 2:
            return 0.0

        mean_coherence = sum(coherences) / len(coherences)
        variance = sum((c - mean_coherence) ** 2 for c in coherences) / len(coherences)
        std_dev = variance ** 0.5

        return std_dev

    def should_reset_fibonacci(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> Tuple[bool, float]:
        """
        Determine if Fibonacci sequence should reset based on lens-invariant truth detection.

        Resets when lens deviation collapses to near-zero, indicating that
        all cultural lenses agree on the coherence interpretation.
        This signals translation-invariant truth - a Jade structure.

        The Fibonacci spiral follows epistemological confidence, not just pattern detection.
        Low distortion = truth stabilizes across frames = new origin point.

        Args:
            psi, rho, q, f: GCT variables

        Returns:
            Tuple of (should_reset: bool, lens_deviation: float)
        """
        lens_deviation = self.calculate_lens_deviation(psi, rho, q, f)

        # If deviation below threshold, all lenses agree -> universal truth -> RESET
        should_reset = lens_deviation < self.invariance_threshold

        return should_reset, lens_deviation

    def _suggest_alternative_lenses(
        self,
        optimized: Dict[str, float],
        current_lens: str
    ) -> List[str]:
        """
        Suggest other lenses that might reveal different aspects.

        High q + high f → Try activist lens
        High rho + low q → Try academic lens
        Low psi + high rho → Try contemplative lens
        """
        suggestions = []

        q = optimized['q']
        f = optimized['f']
        psi = optimized['psi']
        rho = optimized['rho']

        # High emotion + high social → activist
        if q > 0.6 and f > 0.6 and current_lens != 'activist':
            suggestions.append('activist')

        # High wisdom + low emotion → academic
        if rho > 0.7 and q < 0.4 and current_lens != 'modern_academic':
            suggestions.append('modern_academic')

        # Low consistency + high wisdom → contemplative
        if psi < 0.5 and rho > 0.6 and current_lens != 'contemplative':
            suggestions.append('contemplative')

        # High emotion → trauma_informed
        if q > 0.7 and current_lens != 'trauma_informed':
            suggestions.append('trauma_informed')

        # Moderate everything → digital_native
        if all(0.3 < v < 0.7 for v in [psi, rho, q, f]) and current_lens != 'digital_native':
            suggestions.append('digital_native')

        return suggestions

    def _generate_uncertainty_notes(
        self,
        optimized: Dict[str, float],
        lens: CulturalLens
    ) -> Optional[str]:
        """Generate notes about where translation is uncertain"""
        notes = []

        # Check for extremes
        if optimized['q'] > 0.8:
            notes.append("Very high emotional activation detected - substrate inhibition may be dampening perception")

        if optimized['psi'] < 0.3:
            notes.append("Low internal consistency - pattern may be paradoxical or fragmented")

        if optimized['rho'] < 0.3:
            notes.append("Low specificity detected - interpretation may be uncertain")

        return "; ".join(notes) if notes else None
