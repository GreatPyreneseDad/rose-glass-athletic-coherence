"""
Rose Looking Glass - GCT Variables Core Implementation
======================================================

Grounded Coherence Theory (GCT) variable extraction and computation.

Variables:
- Ψ (psi): Internal consistency harmonic
- ρ (rho): Accumulated wisdom depth
- q: Moral/emotional activation energy
- f: Social belonging architecture
"""

from dataclasses import dataclass
from typing import Dict, Optional
import re
from collections import Counter


@dataclass
class GCTVariables:
    """Container for the four GCT dimensions"""
    psi: float  # Ψ - Internal consistency (0-1)
    rho: float  # ρ - Wisdom depth (0-1)
    q: float    # q - Emotional activation (0-1)
    f: float    # f - Social belonging (0-1)

    def to_dict(self) -> Dict[str, float]:
        """Export as dictionary"""
        return {
            'psi': self.psi,
            'rho': self.rho,
            'q': self.q,
            'f': self.f
        }


class GCTExtractor:
    """
    Extracts GCT variables from text using pattern matching.

    This is a linguistic pattern detector, not a judgment system.
    It identifies patterns that MAY indicate certain dimensions,
    but these are interpretations through a specific lens.
    """

    # Pattern vocabularies for each dimension
    CONSISTENCY_MARKERS = {
        'positive': ['therefore', 'because', 'since', 'so', 'thus', 'hence',
                    'consequently', 'accordingly', 'as a result'],
        'negative': ['but', 'however', 'although', 'yet', 'nevertheless',
                    'nonetheless', 'except', 'unless', 'despite']
    }

    WISDOM_MARKERS = {
        'specific': ['exactly', 'specifically', 'precisely', 'particularly',
                    'on', 'at', 'during', 'between', 'approximately'],
        'vague': ['maybe', 'perhaps', 'possibly', 'sometimes', 'usually',
                 'i think', 'i guess', 'sort of', 'kind of', 'probably',
                 'might', 'could']
    }

    EMOTIONAL_MARKERS = [
        'feel', 'felt', 'afraid', 'scared', 'angry', 'furious',
        'upset', 'hurt', 'love', 'hate', 'worried', 'anxious',
        'terrified', 'devastated', 'thrilled', 'horrified',
        'desperate', 'hopeful', 'relieved', 'frustrated'
    ]

    SOCIAL_MARKERS = {
        'collective': ['we', 'us', 'our', 'together', 'family', 'community',
                      'team', 'group', 'everyone', 'collective'],
        'individual': ['i', 'me', 'my', 'mine', 'myself', 'alone', 'solo']
    }

    def extract(self, text: str) -> GCTVariables:
        """
        Extract all four GCT variables from text.

        Returns GCTVariables with values 0-1 for each dimension.
        """
        return GCTVariables(
            psi=self._extract_psi(text),
            rho=self._extract_rho(text),
            q=self._extract_q(text),
            f=self._extract_f(text)
        )

    def _extract_psi(self, text: str) -> float:
        """
        Extract Ψ - Internal consistency harmonic.

        Higher when language is self-consistent with logical flow.
        Lower when contradicting markers present.

        Range: 0.1 - 0.95 (clamped to prevent extremes)
        """
        words = text.lower().split()
        if len(words) == 0:
            return 0.5  # Neutral baseline

        # Count consistency markers
        positive = sum(1 for w in words if w in self.CONSISTENCY_MARKERS['positive'])
        negative = sum(1 for w in words if w in self.CONSISTENCY_MARKERS['negative'])

        # Base score + marker adjustment
        # More positive markers = higher consistency
        # More negative markers = lower consistency
        score = 0.7 + (positive - negative) * 0.1

        # Clamp to valid range
        return max(0.1, min(0.95, score))

    def _extract_rho(self, text: str) -> float:
        """
        Extract ρ - Accumulated wisdom depth.

        Higher when specific details present (dates, names, precision).
        Lower when vague language dominates (maybe, probably, I think).

        Range: 0.1 - 0.95
        """
        text_lower = text.lower()

        # Count specificity markers
        specific = sum(1 for m in self.WISDOM_MARKERS['specific'] if m in text_lower)
        vague = sum(1 for m in self.WISDOM_MARKERS['vague'] if m in text_lower)

        # Check for numeric precision (dates, numbers, measurements)
        has_numbers = bool(re.search(r'\d+', text))
        if has_numbers:
            specific += 1

        # Base score + marker adjustment
        score = 0.5 + (specific - vague) * 0.15

        return max(0.1, min(0.95, score))

    def _extract_q(self, text: str) -> float:
        """
        Extract q - Moral/emotional activation energy.

        Higher when emotional language present.
        Represents the "heat" of values and feelings in motion.

        Range: 0.0 - 0.95 (capped by biological optimization)
        """
        text_lower = text.lower()

        # Count emotional markers
        emotional_count = sum(1 for m in self.EMOTIONAL_MARKERS if m in text_lower)

        # Check for exclamation marks (emotional punctuation)
        exclamations = text.count('!')

        # Check for ALL CAPS words (shouting)
        words = text.split()
        caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)

        # Combine indicators
        score = emotional_count * 0.15 + exclamations * 0.1 + caps_words * 0.2

        # Clamp to maximum (biological optimization will further constrain)
        return min(0.95, score)

    def _extract_f(self, text: str) -> float:
        """
        Extract f - Social belonging architecture.

        Higher when collective language used (we, together, family).
        Lower when purely individual focus (I, me, alone).

        Range: 0.0 - 1.0
        """
        words = text.lower().split()

        # Count collective vs individual markers
        collective = sum(1 for w in words if w in self.SOCIAL_MARKERS['collective'])
        individual = sum(1 for w in words if w in self.SOCIAL_MARKERS['individual'])

        total = collective + individual
        if total == 0:
            return 0.5  # Neutral baseline

        # Ratio of collective to total social markers
        return collective / (total + 1)  # +1 to soften extremes


# Convenience function for quick extraction
def extract_gct_variables(text: str) -> GCTVariables:
    """Extract GCT variables from text - convenience wrapper"""
    extractor = GCTExtractor()
    return extractor.extract(text)
