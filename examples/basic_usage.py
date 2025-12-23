"""
Rose Looking Glass - Basic Usage Examples
==========================================

Demonstrates core functionality of the translation framework.
"""

from src.core import RoseLookingGlass


def example_1_translate_academic_text():
    """Example 1: Translating academic-style text"""
    print("\n" + "="*60)
    print("Example 1: Academic Text Translation")
    print("="*60)

    glass = RoseLookingGlass(default_lens='modern_academic')

    text = """
    Therefore, based on extensive empirical research conducted over
    five years, I conclude that this methodological approach yields
    significantly more reliable results compared to previous methods.
    The data demonstrates a clear correlation between variables.
    """

    result = glass.translate_text(text)
    print(result.get_narrative())


def example_2_digital_native_communication():
    """Example 2: Digital native communication style"""
    print("\n" + "="*60)
    print("Example 2: Digital Native Communication")
    print("="*60)

    glass = RoseLookingGlass(default_lens='digital_native')

    text = """
    omg this is SO COOL!! 🎉 we should totally do this together,
    like everyone in the community would love it. super excited!!
    """

    result = glass.translate_text(text)
    print(result.get_narrative())


def example_3_compare_interpretations():
    """Example 3: Comparing how different lenses interpret the same pattern"""
    print("\n" + "="*60)
    print("Example 3: Lens Comparison")
    print("="*60)

    glass = RoseLookingGlass()

    # Extract variables from activist text
    text = "We must stand together against injustice. Our community deserves better!"
    variables = glass.gct_extractor.extract(text)

    print(f"\nOriginal text: {text}")
    print(f"\nExtracted GCT variables:")
    print(f"  Ψ (consistency): {variables.psi:.2f}")
    print(f"  ρ (wisdom):      {variables.rho:.2f}")
    print(f"  q (emotion):     {variables.q:.2f}")
    print(f"  f (social):      {variables.f:.2f}")

    print("\n--- Coherence Through Different Lenses ---\n")

    comparisons = glass.compare_lenses(
        psi=variables.psi,
        rho=variables.rho,
        q=variables.q,
        f=variables.f
    )

    for lens_name, visibility in comparisons.items():
        print(f"{visibility.lens_name:20s} coherence: {visibility.coherence:.3f}")


def example_4_trauma_informed_detection():
    """Example 4: Trauma-informed lens for crisis detection"""
    print("\n" + "="*60)
    print("Example 4: Trauma-Informed Crisis Detection")
    print("="*60)

    glass = RoseLookingGlass(default_lens='trauma_informed')

    crisis_text = """
    I'm so scared and I don't know what to do. Everything feels
    overwhelming and I'm terrified about what's happening.
    I desperately need help right now.
    """

    result = glass.translate_text(crisis_text)

    print(f"\nText: {crisis_text.strip()}")
    print(f"\nEmotional activation (q): {result.q:.2f}")
    print(f"Overall coherence: {result.coherence:.2f}")
    print(f"Confidence: {result.confidence:.1%}")

    if result.q > 0.7:
        print("\n⚠️  HIGH EMOTIONAL ACTIVATION DETECTED")
        print("→ Response should be trauma-informed")
        print("→ Consider immediate support resources")


def example_5_view_preextracted_variables():
    """Example 5: Using pre-extracted GCT variables"""
    print("\n" + "="*60)
    print("Example 5: Pre-Extracted Variables")
    print("="*60)

    glass = RoseLookingGlass()

    # Suppose you got these from an external source
    psi = 0.45  # Low consistency (paradoxical)
    rho = 0.85  # High wisdom
    q = 0.30    # Low emotion
    f = 0.20    # Low social

    print(f"\nGCT Variables:")
    print(f"  Ψ: {psi:.2f} (Low - paradoxical)")
    print(f"  ρ: {rho:.2f} (High - deep wisdom)")
    print(f"  q: {q:.2f} (Low - calm)")
    print(f"  f: {f:.2f} (Low - individualistic)")

    # Best lens for low consistency + high wisdom?
    result = glass.view_through_lens(
        psi=psi, rho=rho, q=q, f=f,
        lens_name='contemplative'
    )

    print(f"\nThrough contemplative lens:")
    print(f"  Coherence: {result.coherence:.2f}")
    print(f"  Suggested alternatives: {', '.join(result.alternative_lenses)}")


def example_6_biological_optimization():
    """Example 6: Demonstrating biological optimization of q"""
    print("\n" + "="*60)
    print("Example 6: Biological Optimization")
    print("="*60)

    from src.core.biological_optimization import BiologicalOptimizer

    optimizer = BiologicalOptimizer()

    print("\nHow biological optimization dampens extreme emotional activation:\n")

    test_values = [0.0, 0.2, 0.4, 0.6, 0.8, 0.95]

    for q_raw in test_values:
        q_opt = optimizer.optimize_q(q_raw)
        explanation = optimizer.explain_optimization(q_raw)
        print(f"  q_raw: {q_raw:.2f} → q_opt: {q_opt:.2f}  ({explanation})")


def example_7_adding_custom_lens():
    """Example 7: Adding a custom cultural lens"""
    print("\n" + "="*60)
    print("Example 7: Custom Cultural Lens")
    print("="*60)

    from src.core import CulturalLens

    glass = RoseLookingGlass()

    # Create a custom lens for poetic expression
    poetic_lens = CulturalLens(
        name='poetic',
        display_name='Poetic Expression',
        description='Metaphorical and artistic communication',
        weight_psi=0.15,  # Lower (metaphor can seem inconsistent)
        weight_rho=0.45,  # Higher (depth of meaning)
        weight_q=0.30,    # Moderate emotion
        weight_f=0.10,    # Lower social
        typical_patterns='Metaphor, imagery, emotional resonance',
        use_cases=['Poetry', 'Literature', 'Artistic expression']
    )

    glass.add_lens(poetic_lens)

    text = "The moon weeps silver tears upon the darkened sea, and in its sorrow I find my own reflection."

    result = glass.translate_text(text, lens_name='poetic')

    print(f"\nPoetic text coherence: {result.coherence:.2f}")
    print(f"Lens: {result.lens_name}")


def main():
    """Run all examples"""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  Rose Looking Glass v2.1 - Usage Examples                 ║")
    print("╚════════════════════════════════════════════════════════════╝")

    example_1_translate_academic_text()
    example_2_digital_native_communication()
    example_3_compare_interpretations()
    example_4_trauma_informed_detection()
    example_5_view_preextracted_variables()
    example_6_biological_optimization()
    example_7_adding_custom_lens()

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
