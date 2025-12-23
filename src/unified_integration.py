"""
Rose Looking Glass - Unified Integration Module
================================================

This module integrates the unified components into the rose-looking-glass repository.

NEW FEATURES ADDED:
- τ (temporal depth): Full temporal analysis integration
- λ (lens interference): Enhanced lens deviation with full interference analysis
- Veritas function: Truth valuation with frame analysis
- Mirror/Architect wings: Reflexive validation for API responses

ENHANCED FEATURES:
- Fibonacci learning now uses lens deviation as primary reset trigger
- PatternVisibility extended with tau and lambda
- RoseLookingGlass.translate_text() now returns 6 variables

Author: Christopher MacGregor bin Joseph
Date: December 2025
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import unified shared modules
from ..shared.temporal_dimension import (
    TemporalAnalyzer,
    TemporalSignature,
    TemporalScale,
    extract_tau
)

from ..shared.lens_interference import (
    LensInterferenceAnalyzer,
    InterferenceAnalysis,
    InterferenceType,
    LensReading,
    extract_lambda
)

from ..shared.fibonacci_learning import (
    FibonacciLearningAlgorithm,
    TruthDiscovery,
    TruthType,
    ResetTrigger,
    FibonacciState,
    create_fibonacci_learner
)

from ..shared.veritas_reflexive import (
    VeritasFunction,
    VeritasResult,
    EvaluationFrame,
    ArchitectWing,
    MirrorWing,
    ReflexiveValidationSystem,
    InsightFragment,
    IntegratedInsight,
    ReflectionResult
)

# Import existing core components
from .rose_looking_glass import RoseLookingGlass, PatternVisibility, CulturalLens
from .gct_variables import GCTExtractor


@dataclass
class EnhancedPatternVisibility(PatternVisibility):
    """Extended PatternVisibility with tau and lambda"""
    
    # New dimensions
    tau: float = 0.0          # Temporal depth
    tau_scale: str = "CONTEMPORARY"
    lambda_coef: float = 0.0  # Lens interference
    interference_type: str = "neutral"
    
    # Veritas integration
    veritas_score: float = 0.0
    is_universal: bool = False
    
    # Fibonacci state
    fibonacci_angle: float = 0.0
    truth_discovered: bool = False
    truth_type: Optional[str] = None
    
    def get_full_narrative(self) -> str:
        """Generate extended narrative with all 6 variables"""
        base_narrative = self.get_narrative()
        
        extended = f"""
Extended Dimensions:
--------------------
• τ (Temporal Depth): {self.tau:.2f} ({self.tau_scale})
• λ (Lens Interference): {self.lambda_coef:.2f} ({self.interference_type})

Veritas Score: {self.veritas_score:.3f}
Universal Truth: {'Yes' if self.is_universal else 'No'}

Fibonacci State:
• Current Angle: {self.fibonacci_angle:.1f}°
• Truth Discovered: {'Yes' if self.truth_discovered else 'No'}
{f'• Truth Type: {self.truth_type}' if self.truth_type else ''}
"""
        return base_narrative + extended


class EnhancedRoseLookingGlass(RoseLookingGlass):
    """
    Enhanced Rose Looking Glass with 6-variable GCT and learning.
    
    Extends base RoseLookingGlass with:
    - Temporal depth (τ) analysis
    - Full lens interference (λ) analysis  
    - Fibonacci learning with lens deviation reset
    - Veritas truth valuation
    - Mirror/Architect reflexive validation
    """
    
    def __init__(
        self,
        invariance_threshold: float = 0.10,
        stability_threshold: float = 0.6,
        **kwargs
    ):
        """
        Initialize enhanced Rose Looking Glass.
        
        Args:
            invariance_threshold: σ_lens threshold for Fibonacci reset
            stability_threshold: Minimum Veritas for stable truth
            **kwargs: Passed to base RoseLookingGlass
        """
        super().__init__(**kwargs)
        
        # Store thresholds
        self.invariance_threshold = invariance_threshold
        self.stability_threshold = stability_threshold
        
        # New analyzers
        self.temporal_analyzer = TemporalAnalyzer()
        self.interference_analyzer = LensInterferenceAnalyzer()
        
        # Learning system
        self.fibonacci = FibonacciLearningAlgorithm(
            invariance_threshold=invariance_threshold
        )
        
        # Validation system
        self.validation = ReflexiveValidationSystem()
        self.validation.veritas.stability_threshold = stability_threshold
        
    def translate_text_enhanced(
        self,
        text: str,
        lens_name: Optional[str] = None
    ) -> EnhancedPatternVisibility:
        """
        Full 6-variable translation with learning.
        
        Args:
            text: Text to translate
            lens_name: Optional lens override
            
        Returns:
            EnhancedPatternVisibility with all 6 variables
        """
        # Get base translation (psi, rho, q, f)
        base_visibility = self.translate_text(text, lens_name)
        
        # Extract tau
        temporal_sig = self.temporal_analyzer.analyze(text)
        
        # Calculate lambda
        interference = self.interference_analyzer.analyze_interference(
            base_visibility.psi,
            base_visibility.rho,
            base_visibility.q,
            base_visibility.f
        )
        
        # Run Fibonacci learning
        learning_result = self.fibonacci.rotate(
            base_visibility.psi,
            base_visibility.rho,
            base_visibility.q,
            base_visibility.f,
            text
        )
        
        # Calculate Veritas
        veritas = self.validation.veritas.quick_veritas(
            distortion_index=interference.lambda_coefficient,
            composite_score=base_visibility.coherence
        )
        
        # Build enhanced visibility
        enhanced = EnhancedPatternVisibility(
            # Base fields
            psi=base_visibility.psi,
            rho=base_visibility.rho,
            q=base_visibility.q,
            f=base_visibility.f,
            coherence=base_visibility.coherence,
            lens_name=base_visibility.lens_name,
            timestamp=base_visibility.timestamp,
            original_text_hash=base_visibility.original_text_hash,
            confidence=base_visibility.confidence,
            alternative_lenses=base_visibility.alternative_lenses,
            uncertainty_notes=base_visibility.uncertainty_notes,
            
            # New dimensions
            tau=temporal_sig.tau,
            tau_scale=temporal_sig.scale.name,
            lambda_coef=interference.lambda_coefficient,
            interference_type=interference.interference_type.value,
            
            # Veritas
            veritas_score=veritas,
            is_universal=interference.lambda_coefficient < self.invariance_threshold,
            
            # Fibonacci
            fibonacci_angle=learning_result['current_angle'],
            truth_discovered=learning_result['truth_discovered'],
            truth_type=learning_result['truth_type']
        )
        
        return enhanced
    
    def calculate_lens_deviation(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> float:
        """
        Calculate lens deviation for Fibonacci reset trigger.
        
        This is the Veritas distortion index D(P).
        
        Args:
            psi, rho, q, f: GCT variables
            
        Returns:
            Standard deviation across lenses (0-1)
        """
        return self.interference_analyzer.calculate_lens_deviation(psi, rho, q, f)
    
    def should_reset_fibonacci(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> tuple:
        """
        Check if Fibonacci should reset (lens-invariant truth found).
        
        Args:
            psi, rho, q, f: GCT variables
            
        Returns:
            (should_reset: bool, deviation: float)
        """
        deviation = self.calculate_lens_deviation(psi, rho, q, f)
        return deviation < self.invariance_threshold, deviation
    
    def validate_translation(
        self,
        text: str,
        visibility: EnhancedPatternVisibility
    ) -> Dict[str, Any]:
        """
        Validate a translation through Mirror/Architect/Veritas.
        
        Args:
            text: Original text
            visibility: Translation result
            
        Returns:
            Validation results
        """
        return self.validation.validate_insight(
            insight=text,
            distortion_index=visibility.lambda_coef
        )
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get Fibonacci learning summary"""
        return self.fibonacci.get_discovery_summary()
    
    def get_interference_analysis(
        self,
        psi: float,
        rho: float,
        q: float,
        f: float
    ) -> InterferenceAnalysis:
        """Get full lens interference analysis"""
        return self.interference_analyzer.analyze_interference(psi, rho, q, f)
    
    def get_temporal_signature(self, text: str) -> TemporalSignature:
        """Get temporal depth signature for text"""
        return self.temporal_analyzer.analyze(text)


# API extension for FastAPI integration
def create_enhanced_api_routes(app, glass: EnhancedRoseLookingGlass):
    """
    Add enhanced API routes to FastAPI app.
    
    Args:
        app: FastAPI application instance
        glass: EnhancedRoseLookingGlass instance
    """
    from fastapi import HTTPException
    from pydantic import BaseModel
    
    class EnhancedTranslateRequest(BaseModel):
        text: str
        lens_name: Optional[str] = None
    
    class LearningStateResponse(BaseModel):
        current_angle: float
        rotation_factor: int
        learning_resets: int
        exploration_coverage: float
        truths_discovered: int
    
    @app.post("/translate/enhanced")
    async def translate_enhanced(request: EnhancedTranslateRequest):
        """Enhanced translation with 6 variables"""
        try:
            visibility = glass.translate_text_enhanced(
                text=request.text,
                lens_name=request.lens_name
            )
            return {
                'psi': visibility.psi,
                'rho': visibility.rho,
                'q': visibility.q,
                'f': visibility.f,
                'tau': visibility.tau,
                'lambda': visibility.lambda_coef,
                'coherence': visibility.coherence,
                'veritas': visibility.veritas_score,
                'is_universal': visibility.is_universal,
                'truth_discovered': visibility.truth_discovered,
                'fibonacci_angle': visibility.fibonacci_angle,
                'lens_name': visibility.lens_name,
                'narrative': visibility.get_full_narrative()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/learning/state", response_model=LearningStateResponse)
    async def get_learning_state():
        """Get current Fibonacci learning state"""
        state = glass.fibonacci.get_state()
        return LearningStateResponse(
            current_angle=state.current_angle,
            rotation_factor=state.rotation_factor,
            learning_resets=state.learning_resets,
            exploration_coverage=state.exploration_coverage,
            truths_discovered=state.truths_discovered
        )
    
    @app.get("/learning/summary")
    async def get_learning_summary():
        """Get Fibonacci learning summary"""
        return glass.get_learning_summary()
    
    @app.post("/validate")
    async def validate_insight(request: EnhancedTranslateRequest):
        """Validate insight through reflexive system"""
        visibility = glass.translate_text_enhanced(request.text)
        validation = glass.validate_translation(request.text, visibility)
        return {
            'is_validated': validation['is_validated'],
            'veritas_score': validation['veritas_score'],
            'resonance_score': validation['resonance_score']
        }


# Factory function
def create_enhanced_looking_glass(**kwargs) -> EnhancedRoseLookingGlass:
    """Factory for enhanced Rose Looking Glass"""
    return EnhancedRoseLookingGlass(**kwargs)


# Module exports
__all__ = [
    # Enhanced classes
    'EnhancedRoseLookingGlass',
    'EnhancedPatternVisibility',
    'create_enhanced_looking_glass',
    'create_enhanced_api_routes',
    
    # Re-export shared modules
    'TemporalAnalyzer',
    'TemporalSignature',
    'extract_tau',
    'LensInterferenceAnalyzer',
    'InterferenceAnalysis',
    'extract_lambda',
    'FibonacciLearningAlgorithm',
    'TruthDiscovery',
    'TruthType',
    'ResetTrigger',
    'VeritasFunction',
    'VeritasResult',
    'ArchitectWing',
    'MirrorWing',
    'ReflexiveValidationSystem',
]
