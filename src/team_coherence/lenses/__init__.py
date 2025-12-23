"""
Cultural Lens System
====================

Provides cultural calibrations for interpreting coherence patterns.
Different backgrounds express stress, cohesion, and processing differently.
All expressions are valid - the lens provides translation, not judgment.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import statistics


@dataclass
class LensParameters:
    """Calibration parameters for a cultural lens"""
    
    # Dimension weights (how much each dimension matters in this context)
    psi_weight: float = 1.0
    rho_weight: float = 1.0
    q_weight: float = 1.0
    f_weight: float = 1.0
    tau_weight: float = 1.0
    
    # Baseline expectations (what's "normal" for this lens)
    q_baseline: float = 0.5   # Expected emotional activation
    f_baseline: float = 0.5   # Expected social expression
    psi_tolerance: float = 0.3  # How much inconsistency is normal
    
    # Expression modifiers
    verbal_expression: float = 0.5  # 0=action-oriented, 1=verbal-oriented
    direct_communication: float = 0.5  # 0=indirect, 1=direct
    collective_orientation: float = 0.5  # 0=individual, 1=collective
    
    # Biological optimization parameters
    km: float = 0.3
    ki: float = 2.0


@dataclass 
class LensInterpretation:
    """How a specific lens interprets a pattern"""
    lens_name: str
    coherence: float
    confidence: float
    notes: List[str]
    
    # Flags specific to this lens view
    concerns: List[str]
    strengths: List[str]


class CulturalLens:
    """
    A cultural calibration for interpreting coherence patterns.
    
    Each lens represents a valid way of expressing and processing experience.
    No lens is "better" - they provide different translations.
    """
    
    def __init__(self, name: str, params: LensParameters, description: str = ""):
        self.name = name
        self.params = params
        self.description = description
    
    def interpret(self, psi: float, rho: float, q: float, 
                  f: float, tau: float) -> LensInterpretation:
        """
        Interpret pattern through this cultural lens.
        
        Returns coherence reading and contextual notes.
        """
        notes = []
        concerns = []
        strengths = []
        
        # Apply biological optimization to q
        q_opt = self._optimize_q(q)
        
        # Calculate weighted coherence
        weighted_sum = (
            psi * self.params.psi_weight +
            rho * self.params.rho_weight +
            q_opt * self.params.q_weight +
            f * self.params.f_weight +
            tau * self.params.tau_weight
        )
        total_weight = (
            self.params.psi_weight +
            self.params.rho_weight +
            self.params.q_weight +
            self.params.f_weight +
            self.params.tau_weight
        )
        coherence = weighted_sum / total_weight
        
        # Generate lens-specific notes
        
        # q-dimension interpretation
        q_diff = q - self.params.q_baseline
        if abs(q_diff) > 0.2:
            if q_diff > 0 and self.params.verbal_expression < 0.4:
                notes.append(
                    f"High q ({q:.2f}) in action-oriented culture may indicate "
                    "significant distress despite reserved expression style"
                )
                concerns.append("Elevated activation in typically reserved communicator")
            elif q_diff < 0 and self.params.verbal_expression > 0.6:
                notes.append(
                    f"Low q ({q:.2f}) in verbally expressive culture may indicate "
                    "suppression rather than calm"
                )
                concerns.append("Unusual suppression in typically expressive communicator")
            elif q_diff > 0:
                notes.append(f"q-activation elevated ({q:.2f}) - within cultural range")
        
        # f-dimension interpretation
        if f < 0.4:
            if self.params.collective_orientation > 0.6:
                concerns.append("Low social expression in collective-oriented individual")
                notes.append(
                    "This lens expects higher social engagement - "
                    "low f may signal isolation"
                )
            elif self.params.collective_orientation < 0.4:
                notes.append(
                    "Low f is within normal range for individual-oriented lens"
                )
        elif f > 0.7:
            strengths.append("Strong social connection patterns")
        
        # psi-dimension interpretation
        if psi < 0.5:
            if self.params.psi_tolerance > 0.4:
                notes.append(
                    "Narrative inconsistency within acceptable range for this lens"
                )
            else:
                concerns.append("Low consistency in consistency-valuing culture")
        elif psi > 0.8:
            strengths.append("Strong narrative consistency")
        
        # tau-dimension interpretation
        if tau < 0.4:
            notes.append("Present-focused temporal orientation - may be crisis mode")
            concerns.append("Limited temporal integration")
        elif tau > 0.7:
            strengths.append("Good integration of past experience")
        
        # Calculate confidence based on how well pattern fits lens expectations
        fit_score = 1.0 - (
            abs(q - self.params.q_baseline) * 0.3 +
            abs(f - 0.5 - (self.params.collective_orientation - 0.5) * 0.4) * 0.3
        )
        confidence = max(0.5, min(1.0, fit_score))
        
        return LensInterpretation(
            lens_name=self.name,
            coherence=coherence,
            confidence=confidence,
            notes=notes,
            concerns=concerns,
            strengths=strengths
        )
    
    def _optimize_q(self, q_raw: float) -> float:
        """Apply biological optimization to q"""
        if q_raw <= 0:
            return 0
        km = self.params.km
        ki = self.params.ki
        return q_raw / (km + q_raw + (q_raw ** 2 / ki))


class LensLibrary:
    """
    Library of available cultural lenses.
    
    Each lens is developed with input from members of that cultural context.
    """
    
    def __init__(self):
        self.lenses: Dict[str, CulturalLens] = {}
        self._init_default_lenses()
    
    def _init_default_lenses(self):
        """Initialize default cultural lenses"""
        
        # Combat Veteran Lens
        self.lenses["combat_veteran"] = CulturalLens(
            name="combat_veteran",
            description="Calibration for those with combat experience",
            params=LensParameters(
                psi_weight=1.2,      # Consistency matters
                rho_weight=1.0,
                q_weight=0.8,        # Emotional suppression is adaptive
                f_weight=1.3,        # Unit cohesion critical
                tau_weight=1.0,
                q_baseline=0.35,     # Lower emotional baseline
                f_baseline=0.7,      # Higher social expectation (unit)
                psi_tolerance=0.2,   # Tighter consistency expectation
                verbal_expression=0.3,    # Action over words
                direct_communication=0.8,  # Direct communication valued
                collective_orientation=0.8, # Unit identity strong
                km=0.25,
                ki=1.5
            )
        )
        
        # First Generation Lens
        self.lenses["first_generation"] = CulturalLens(
            name="first_generation",
            description="Calibration for first-generation Americans/immigrants",
            params=LensParameters(
                psi_weight=0.9,
                rho_weight=1.2,      # Wisdom from dual cultures
                q_weight=1.1,        # More emotional expression typical
                f_weight=1.0,
                tau_weight=1.1,
                q_baseline=0.55,     # Slightly higher emotional baseline
                f_baseline=0.6,
                psi_tolerance=0.4,   # Code-switching creates apparent inconsistency
                verbal_expression=0.6,
                direct_communication=0.4,  # Often more indirect
                collective_orientation=0.7,  # Family/community orientation
                km=0.3,
                ki=2.0
            )
        )
        
        # Neurodivergent Lens
        self.lenses["neurodivergent"] = CulturalLens(
            name="neurodivergent",
            description="Calibration for neurodivergent communication styles",
            params=LensParameters(
                psi_weight=1.3,      # Logical consistency highly valued
                rho_weight=1.0,
                q_weight=0.7,        # "Flat affect" is not low emotion
                f_weight=0.8,        # Different social patterns
                tau_weight=1.0,
                q_baseline=0.4,
                f_baseline=0.4,      # Lower social expectation
                psi_tolerance=0.1,   # High consistency expectation
                verbal_expression=0.5,
                direct_communication=0.9,  # Very direct
                collective_orientation=0.4,
                km=0.35,
                ki=2.5
            )
        )
        
        # Rural Traditional Lens
        self.lenses["rural_traditional"] = CulturalLens(
            name="rural_traditional",
            description="Calibration for rural/traditional backgrounds",
            params=LensParameters(
                psi_weight=1.0,
                rho_weight=1.2,      # Wisdom valued
                q_weight=0.7,        # Stoic expression
                f_weight=1.0,
                tau_weight=1.1,
                q_baseline=0.35,
                f_baseline=0.5,
                psi_tolerance=0.3,
                verbal_expression=0.3,    # Action-oriented
                direct_communication=0.6,
                collective_orientation=0.6,  # Community matters
                km=0.3,
                ki=2.0
            )
        )
        
        # Urban Contemporary Lens
        self.lenses["urban_contemporary"] = CulturalLens(
            name="urban_contemporary",
            description="Calibration for urban/contemporary expression",
            params=LensParameters(
                psi_weight=0.9,
                rho_weight=0.9,
                q_weight=1.2,        # More emotional expression
                f_weight=1.1,
                tau_weight=0.9,
                q_baseline=0.55,
                f_baseline=0.6,
                psi_tolerance=0.4,
                verbal_expression=0.8,    # Verbal processing
                direct_communication=0.5,
                collective_orientation=0.5,
                km=0.3,
                ki=2.0
            )
        )
        
        # Religious Framework Lens
        self.lenses["religious_framework"] = CulturalLens(
            name="religious_framework",
            description="Calibration for faith-based meaning-making",
            params=LensParameters(
                psi_weight=1.1,
                rho_weight=1.3,      # Wisdom tradition valued
                q_weight=1.0,
                f_weight=1.2,        # Community orientation
                tau_weight=1.2,      # Temporal/eternal perspective
                q_baseline=0.5,
                f_baseline=0.7,
                psi_tolerance=0.3,
                verbal_expression=0.6,
                direct_communication=0.5,
                collective_orientation=0.8,
                km=0.3,
                ki=2.0
            )
        )
        
        # Female Service Member Lens
        self.lenses["female_service"] = CulturalLens(
            name="female_service",
            description="Calibration accounting for female experience in military",
            params=LensParameters(
                psi_weight=1.0,
                rho_weight=1.0,
                q_weight=1.0,        # Don't penalize emotional expression
                f_weight=1.1,
                tau_weight=1.0,
                q_baseline=0.5,      # Neutral baseline
                f_baseline=0.5,
                psi_tolerance=0.3,
                verbal_expression=0.6,
                direct_communication=0.7,
                collective_orientation=0.6,
                km=0.3,
                ki=2.0
            )
        )
    
    def get_lens(self, name: str) -> Optional[CulturalLens]:
        """Get a lens by name"""
        return self.lenses.get(name)
    
    def list_lenses(self) -> List[str]:
        """List available lens names"""
        return list(self.lenses.keys())
    
    def interpret_all(self, psi: float, rho: float, q: float,
                     f: float, tau: float) -> Dict[str, LensInterpretation]:
        """Interpret pattern through all lenses"""
        return {
            name: lens.interpret(psi, rho, q, f, tau)
            for name, lens in self.lenses.items()
        }


class LensDeviationCalculator:
    """
    Calculates deviation across lenses to identify lens-invariant signals.
    
    Low deviation = all lenses agree = critical signal
    High deviation = lenses disagree = context-dependent, provide translation
    """
    
    def __init__(self, library: LensLibrary = None):
        self.library = library or LensLibrary()
    
    def calculate_deviation(self, psi: float, rho: float, q: float,
                           f: float, tau: float,
                           lenses: List[str] = None) -> Tuple[float, Dict]:
        """
        Calculate lens deviation and return analysis.
        
        Args:
            psi, rho, q, f, tau: Pattern dimensions
            lenses: Which lenses to use (default: all)
            
        Returns:
            (deviation, analysis_dict)
        """
        if lenses is None:
            lenses = self.library.list_lenses()
        
        interpretations = {}
        coherences = []
        
        for lens_name in lenses:
            lens = self.library.get_lens(lens_name)
            if lens:
                interp = lens.interpret(psi, rho, q, f, tau)
                interpretations[lens_name] = interp
                coherences.append(interp.coherence)
        
        if len(coherences) < 2:
            deviation = 0.0
        else:
            deviation = statistics.stdev(coherences)
        
        # Determine if lens-invariant
        invariance_threshold = 0.1
        is_invariant = deviation < invariance_threshold
        
        # Find areas of agreement and disagreement
        all_concerns = []
        all_strengths = []
        for interp in interpretations.values():
            all_concerns.extend(interp.concerns)
            all_strengths.extend(interp.strengths)
        
        # Count frequency of concerns/strengths
        concern_counts = {}
        for c in all_concerns:
            concern_counts[c] = concern_counts.get(c, 0) + 1
        
        # Universal concerns (appear in >50% of lenses)
        threshold = len(lenses) / 2
        universal_concerns = [c for c, count in concern_counts.items() 
                            if count > threshold]
        
        analysis = {
            "deviation": deviation,
            "is_lens_invariant": is_invariant,
            "interpretations": interpretations,
            "coherence_range": (min(coherences), max(coherences)),
            "coherence_mean": statistics.mean(coherences),
            "universal_concerns": universal_concerns,
            "translation_needed": not is_invariant
        }
        
        return deviation, analysis
    
    def get_translation_notes(self, analysis: Dict) -> List[str]:
        """Generate translation notes for commander"""
        notes = []
        
        if analysis["is_lens_invariant"]:
            notes.append(
                "⚠️ LENS-INVARIANT SIGNAL: All cultural lenses agree on this pattern. "
                "This is not a translation artifact - the signal is real."
            )
        else:
            range_low, range_high = analysis["coherence_range"]
            notes.append(
                f"Coherence varies by lens ({range_low:.2f} to {range_high:.2f}). "
                "Consider individual's cultural background when interpreting."
            )
        
        if analysis["universal_concerns"]:
            notes.append(
                "Universal concerns (flagged by multiple lenses): " +
                ", ".join(analysis["universal_concerns"])
            )
        
        # Add specific lens notes
        for lens_name, interp in analysis["interpretations"].items():
            if interp.notes:
                notes.append(f"{lens_name}: {interp.notes[0]}")
        
        return notes
