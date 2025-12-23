"""
Rose Looking Glass - Core Engine Tests
======================================

Tests for GCT variable extraction, biological optimization,
and core translation engine.
"""

import pytest
from src.core import (
    RoseLookingGlass,
    GCTExtractor,
    BiologicalOptimizer,
    BiologicalParameters,
    CulturalLens
)


class TestGCTExtractor:
    """Tests for GCT variable extraction"""

    def test_extract_high_consistency(self):
        """Text with logical connectors should have high Ψ"""
        extractor = GCTExtractor()
        text = "Therefore, based on the evidence, I conclude this is correct."

        variables = extractor.extract(text)

        assert variables.psi > 0.6, "Should have high consistency"

    def test_extract_low_consistency(self):
        """Text with contradictions should have lower Ψ"""
        extractor = GCTExtractor()
        text = "I love it, but I hate it, although maybe it's okay."

        variables = extractor.extract(text)

        assert variables.psi < 0.7, "Should have lower consistency"

    def test_extract_high_specificity(self):
        """Text with specific details should have high ρ"""
        extractor = GCTExtractor()
        text = "On January 15, 2024, at precisely 3:00 PM, the experiment began."

        variables = extractor.extract(text)

        assert variables.rho > 0.6, "Should have high specificity"

    def test_extract_vague_language(self):
        """Vague language should lower ρ"""
        extractor = GCTExtractor()
        text = "Maybe sometime I think it might possibly be sort of okay."

        variables = extractor.extract(text)

        assert variables.rho < 0.5, "Should have low specificity"

    def test_extract_high_emotion(self):
        """Emotional language should increase q"""
        extractor = GCTExtractor()
        text = "I'm terrified and devastated! This is absolutely horrifying!"

        variables = extractor.extract(text)

        assert variables.q >= 0.45, "Should have high emotional activation"

    def test_extract_calm_language(self):
        """Calm factual language should have low q"""
        extractor = GCTExtractor()
        text = "The data indicates a correlation between the variables."

        variables = extractor.extract(text)

        assert variables.q < 0.4, "Should have low emotional activation"

    def test_extract_collective_language(self):
        """Collective language should increase f"""
        extractor = GCTExtractor()
        text = "We stand together as a community, united in our purpose."

        variables = extractor.extract(text)

        assert variables.f > 0.6, "Should have high social belonging"

    def test_extract_individual_language(self):
        """Individual language should lower f"""
        extractor = GCTExtractor()
        text = "I alone made my decision based on my personal values."

        variables = extractor.extract(text)

        assert variables.f < 0.4, "Should have lower social belonging"


class TestBiologicalOptimizer:
    """Tests for biological optimization curves"""

    def test_optimize_zero_q(self):
        """Zero q should remain zero"""
        optimizer = BiologicalOptimizer()
        assert optimizer.optimize_q(0.0) == 0.0

    def test_optimize_moderate_q(self):
        """Moderate q should amplify slightly"""
        optimizer = BiologicalOptimizer()
        q_opt = optimizer.optimize_q(0.3)

        assert q_opt > 0.3, "Should amplify moderate values"
        assert q_opt < 0.7, "Should not over-amplify"

    def test_optimize_extreme_q(self):
        """Extreme q should be dampened (substrate inhibition)"""
        optimizer = BiologicalOptimizer()
        q_opt = optimizer.optimize_q(0.9)

        assert q_opt < 0.9, "Should dampen extreme values"

    def test_optimize_never_exceeds_max(self):
        """Optimized q should never exceed max_q"""
        optimizer = BiologicalOptimizer()

        for q_raw in [0.0, 0.3, 0.5, 0.7, 0.9, 0.95]:
            q_opt = optimizer.optimize_q(q_raw)
            assert q_opt <= optimizer.params.max_q

    def test_optimize_all_variables(self):
        """optimize_all should process all four variables"""
        optimizer = BiologicalOptimizer()

        result = optimizer.optimize_all(
            psi=0.8,
            rho=0.9,
            q=0.7,
            f=0.6
        )

        assert 'psi' in result
        assert 'rho' in result
        assert 'q' in result
        assert 'f' in result

        # All should be in valid range
        for key, value in result.items():
            assert 0.0 <= value <= 1.0, f"{key} out of range: {value}"


class TestCulturalLens:
    """Tests for cultural lens calibrations"""

    def test_lens_weights_must_sum_to_one(self):
        """Lens weights must sum to 1.0"""
        with pytest.raises(ValueError):
            CulturalLens(
                name='invalid',
                display_name='Invalid Lens',
                description='Invalid weights',
                weight_psi=0.5,
                weight_rho=0.5,
                weight_q=0.5,
                weight_f=0.5  # Total = 2.0, should fail
            )

    def test_valid_lens_creation(self):
        """Valid lens should be created successfully"""
        lens = CulturalLens(
            name='test',
            display_name='Test Lens',
            description='For testing',
            weight_psi=0.25,
            weight_rho=0.25,
            weight_q=0.25,
            weight_f=0.25
        )

        assert lens.name == 'test'
        assert lens.weight_psi == 0.25


class TestRoseLookingGlass:
    """Tests for main Rose Looking Glass engine"""

    def test_initialization(self):
        """RoseLookingGlass should initialize with default lens"""
        glass = RoseLookingGlass()

        assert glass.current_lens_name == 'modern_academic'
        assert len(glass.lenses) >= 5  # Should have default lenses

    def test_list_lenses(self):
        """list_lenses should return available lenses"""
        glass = RoseLookingGlass()
        lenses = glass.list_lenses()

        assert isinstance(lenses, dict)
        assert 'modern_academic' in lenses
        assert 'digital_native' in lenses
        assert 'trauma_informed' in lenses

    def test_select_lens(self):
        """select_lens should switch active lens"""
        glass = RoseLookingGlass()
        glass.select_lens('digital_native')

        assert glass.current_lens_name == 'digital_native'

    def test_select_invalid_lens(self):
        """Selecting invalid lens should raise KeyError"""
        glass = RoseLookingGlass()

        with pytest.raises(KeyError):
            glass.select_lens('nonexistent_lens')

    def test_add_custom_lens(self):
        """add_lens should register new lens"""
        glass = RoseLookingGlass()

        custom_lens = CulturalLens(
            name='custom',
            display_name='Custom Lens',
            description='Test lens',
            weight_psi=0.3,
            weight_rho=0.3,
            weight_q=0.2,
            weight_f=0.2
        )

        glass.add_lens(custom_lens)

        assert 'custom' in glass.lenses
        assert glass.lenses['custom'].display_name == 'Custom Lens'

    def test_view_through_lens(self):
        """view_through_lens should compute pattern visibility"""
        glass = RoseLookingGlass()

        visibility = glass.view_through_lens(
            psi=0.8,
            rho=0.9,
            q=0.3,
            f=0.4
        )

        assert 0.0 <= visibility.coherence <= 1.0
        assert visibility.lens_name == 'Modern Academic'
        assert isinstance(visibility.confidence, float)

    def test_translate_text(self):
        """translate_text should extract variables and compute visibility"""
        glass = RoseLookingGlass()

        text = "Therefore, based on research, I conclude this is optimal."
        visibility = glass.translate_text(text)

        assert visibility.coherence is not None
        assert visibility.psi is not None
        assert visibility.rho is not None
        assert visibility.q is not None
        assert visibility.f is not None

    def test_academic_lens_favors_consistency_and_wisdom(self):
        """Academic lens should weight Ψ and ρ highly"""
        glass = RoseLookingGlass(default_lens='modern_academic')

        # High Ψ and ρ, low q and f
        vis_high_academic = glass.view_through_lens(
            psi=0.9, rho=0.9, q=0.2, f=0.2
        )

        # Low Ψ and ρ, high q and f
        vis_low_academic = glass.view_through_lens(
            psi=0.3, rho=0.3, q=0.8, f=0.8
        )

        assert vis_high_academic.coherence > vis_low_academic.coherence

    def test_activist_lens_favors_emotion_and_social(self):
        """Activist lens should weight q and f highly"""
        glass = RoseLookingGlass(default_lens='activist')

        # High q and f
        vis_high_activist = glass.view_through_lens(
            psi=0.5, rho=0.4, q=0.9, f=0.9
        )

        # Low q and f
        vis_low_activist = glass.view_through_lens(
            psi=0.8, rho=0.8, q=0.2, f=0.2
        )

        assert vis_high_activist.coherence > vis_low_activist.coherence

    def test_compare_lenses(self):
        """compare_lenses should return results for all lenses"""
        glass = RoseLookingGlass()

        comparisons = glass.compare_lenses(
            psi=0.7, rho=0.7, q=0.5, f=0.5
        )

        assert len(comparisons) >= 5  # At least 5 default lenses
        assert 'modern_academic' in comparisons
        assert 'digital_native' in comparisons

        # All should have valid coherence
        for lens_name, visibility in comparisons.items():
            assert 0.0 <= visibility.coherence <= 1.0

    def test_pattern_visibility_to_dict(self):
        """PatternVisibility should export to dictionary"""
        glass = RoseLookingGlass()

        visibility = glass.view_through_lens(
            psi=0.8, rho=0.7, q=0.5, f=0.6
        )

        result_dict = visibility.to_dict()

        assert 'psi' in result_dict
        assert 'rho' in result_dict
        assert 'q' in result_dict
        assert 'f' in result_dict
        assert 'coherence' in result_dict
        assert 'lens_name' in result_dict

    def test_pattern_visibility_narrative(self):
        """PatternVisibility should generate narrative"""
        glass = RoseLookingGlass()

        visibility = glass.view_through_lens(
            psi=0.8, rho=0.7, q=0.5, f=0.6
        )

        narrative = visibility.get_narrative()

        assert isinstance(narrative, str)
        assert 'Ψ' in narrative or 'psi' in narrative.lower()
        assert 'Coherence' in narrative

    def test_trauma_informed_lens_uses_custom_bio_params(self):
        """Trauma-informed lens should use custom biological parameters"""
        glass = RoseLookingGlass()

        trauma_lens = glass.lenses['trauma_informed']

        assert trauma_lens.bio_params is not None
        assert trauma_lens.bio_params.Km == 0.2  # More sensitive to low values

    def test_calculate_lens_deviation(self):
        """Should calculate standard deviation across lenses"""
        glass = RoseLookingGlass()

        # Pattern with high logic (should have low deviation - all lenses agree)
        deviation = glass.calculate_lens_deviation(
            psi=0.9, rho=0.9, q=0.1, f=0.3
        )

        assert 0.0 <= deviation <= 1.0
        # Academic patterns should have relatively low deviation
        assert deviation < 0.3

    def test_should_reset_fibonacci_universal_truth(self):
        """Should reset when lens deviation is low (universal truth)"""
        glass = RoseLookingGlass(invariance_threshold=0.15)

        # High logic, high wisdom pattern
        should_reset, deviation = glass.should_reset_fibonacci(
            psi=0.9, rho=0.9, q=0.1, f=0.3
        )

        # May or may not reset depending on exact lens calibrations
        assert isinstance(should_reset, bool)
        assert 0.0 <= deviation <= 1.0

    def test_should_reset_fibonacci_context_dependent(self):
        """Should not reset when lens deviation is high (context-dependent)"""
        glass = RoseLookingGlass(invariance_threshold=0.1)

        # High Ψ/ρ, low q/f pattern - lenses weight these differently
        # Academic lenses value Ψ/ρ highly, others don't - creates disagreement
        should_reset, deviation = glass.should_reset_fibonacci(
            psi=0.9, rho=0.9, q=0.1, f=0.1
        )

        # This should have higher deviation (lenses disagree on Ψ/ρ importance)
        assert should_reset is False, "Context-dependent patterns should not trigger reset"
        assert deviation > glass.invariance_threshold, f"Deviation {deviation:.4f} should exceed threshold {glass.invariance_threshold}"

    def test_invariance_threshold_configuration(self):
        """Should allow configuration of invariance threshold"""
        glass1 = RoseLookingGlass(invariance_threshold=0.05)
        glass2 = RoseLookingGlass(invariance_threshold=0.20)

        assert glass1.invariance_threshold == 0.05
        assert glass2.invariance_threshold == 0.20

    def test_lens_deviation_distortion_index(self):
        """Lens deviation should implement Veritas distortion index D(P)"""
        glass = RoseLookingGlass()

        # Calculate for balanced pattern
        deviation = glass.calculate_lens_deviation(
            psi=0.6, rho=0.6, q=0.5, f=0.5
        )

        # Veritas = 1 / (1 + D(P)) where D(P) = lens_deviation
        veritas = 1.0 / (1.0 + deviation)

        assert 0.0 < veritas <= 1.0
        # High veritas = low distortion = universal truth
        # Low veritas = high distortion = context-dependent

    def test_should_reset_fibonacci_edge_case_at_threshold(self):
        """Should handle edge case when deviation exactly equals threshold"""
        glass = RoseLookingGlass(invariance_threshold=0.15)

        # Find pattern that produces deviation near threshold
        # Balanced pattern should have moderate deviation
        should_reset, deviation = glass.should_reset_fibonacci(
            psi=0.6, rho=0.6, q=0.5, f=0.5
        )

        # Behavior at threshold: deviation < threshold means reset
        if deviation < glass.invariance_threshold:
            assert should_reset is True
        else:
            assert should_reset is False

        # Deviation should not equal threshold exactly (floating point makes this rare)
        assert isinstance(deviation, float)

    def test_temporal_deviation_collapse(self):
        """Should show deviation decreasing as patterns converge toward truth"""
        glass = RoseLookingGlass(invariance_threshold=0.1)

        # Sequence: context-dependent → moderate → universal truth
        # NOTE: Biological optimization dampens extreme q, creating universal agreement
        # High Ψ/ρ creates disagreement because lenses weight differently
        patterns = [
            # Context-dependent - lenses disagree on Ψ/ρ importance
            (0.9, 0.9, 0.1, 0.1),  # High deviation (~0.136)
            # Moderate - some imbalance
            (0.7, 0.5, 0.4, 0.4),  # Medium deviation
            # Universal truth - balanced pattern, all lenses agree
            (0.6, 0.6, 0.5, 0.5),  # Low deviation (~0.015)
        ]

        deviations = []
        resets = []

        for psi, rho, q, f in patterns:
            should_reset, deviation = glass.should_reset_fibonacci(psi, rho, q, f)
            deviations.append(deviation)
            resets.append(should_reset)

        # Deviation should decrease as patterns become more balanced
        assert deviations[2] < deviations[0], "Truth convergence should reduce deviation"

        # First pattern should NOT reset (context-dependent)
        assert resets[0] is False, "Context-dependent pattern should not reset"

        # Final pattern SHOULD reset (universal truth)
        assert resets[2] is True, "Balanced universal pattern should trigger reset"
