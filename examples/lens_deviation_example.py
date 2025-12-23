"""
Rose Looking Glass - Lens Deviation & Fibonacci Reset Example
=============================================================

Demonstrates lens-invariant truth detection and Fibonacci reset triggers.

"Low distortion = truth stabilizes across frames = new origin point."
"""

from src.core import RoseLookingGlass


def example_1_lens_invariant_truth():
    """Example 1: Detecting lens-invariant truth (universal coherence)"""
    print("\n" + "="*70)
    print("Example 1: Lens-Invariant Truth Detection")
    print("="*70 + "\n")

    glass = RoseLookingGlass(invariance_threshold=0.1)

    # Statement with universal coherence (high Ψ, high ρ, low q, moderate f)
    # Academic research with clear logic
    text = """
    Therefore, based on extensive empirical research conducted at precisely
    3:00 PM on January 15th, 2024, I conclude that this methodological
    approach yields significantly more reliable results.
    """

    result = glass.translate_text(text)

    print(f"Original text: {text.strip()[:100]}...")
    print(f"\nGCT Variables:")
    print(f"  Ψ (consistency): {result.psi:.3f}")
    print(f"  ρ (wisdom):      {result.rho:.3f}")
    print(f"  q (emotion):     {result.q:.3f}")
    print(f"  f (social):      {result.f:.3f}")

    # Calculate lens deviation
    lens_deviation = glass.calculate_lens_deviation(
        result.psi, result.rho, result.q, result.f
    )

    print(f"\n**Lens Deviation (σ_lens): {lens_deviation:.3f}**")

    # Check if should reset Fibonacci
    should_reset, deviation = glass.should_reset_fibonacci(
        result.psi, result.rho, result.q, result.f
    )

    print(f"\nFibonacci Reset? {should_reset}")
    print(f"Reason: {'All lenses agree - lens-invariant truth!' if should_reset else 'Context-dependent - lenses disagree'}")

    # Show coherence across all lenses
    print(f"\n--- Coherence Across All Lenses ---")
    comparisons = glass.compare_lenses(result.psi, result.rho, result.q, result.f)
    for lens_name, visibility in comparisons.items():
        print(f"  {visibility.lens_name:25s} coherence: {visibility.coherence:.3f}")

    print(f"\nInterpretation:")
    if lens_deviation < 0.1:
        print(f"  σ_lens < 0.1 → UNIVERSAL TRUTH")
        print(f"  All cultural contexts agree on coherence.")
        print(f"  This is a Jade structure - translation-invariant.")
        print(f"  **RESET FIBONACCI SEQUENCE** (new origin point)")
    else:
        print(f"  σ_lens ≥ 0.1 → CONTEXT-DEPENDENT")
        print(f"  Different cultures interpret differently.")
        print(f"  Continue exploration.")


def example_2_context_dependent_pattern():
    """Example 2: Context-dependent pattern (lenses disagree)"""
    print("\n\n" + "="*70)
    print("Example 2: Context-Dependent Pattern")
    print("="*70 + "\n")

    glass = RoseLookingGlass(invariance_threshold=0.1)

    # Statement with high emotional activation but high social belonging
    # Activist language - interpreted very differently across lenses
    text = """
    We must stand together against this terrible injustice!
    Our community deserves better and we will fight for our rights!
    """

    result = glass.translate_text(text)

    print(f"Original text: {text.strip()}")
    print(f"\nGCT Variables:")
    print(f"  Ψ (consistency): {result.psi:.3f}")
    print(f"  ρ (wisdom):      {result.rho:.3f}")
    print(f"  q (emotion):     {result.q:.3f}")
    print(f"  f (social):      {result.f:.3f}")

    # Calculate lens deviation
    lens_deviation = glass.calculate_lens_deviation(
        result.psi, result.rho, result.q, result.f
    )

    print(f"\n**Lens Deviation (σ_lens): {lens_deviation:.3f}**")

    # Check if should reset Fibonacci
    should_reset, deviation = glass.should_reset_fibonacci(
        result.psi, result.rho, result.q, result.f
    )

    print(f"\nFibonacci Reset? {should_reset}")
    print(f"Reason: {'All lenses agree' if should_reset else 'Lenses disagree - cultural interpretation varies'}")

    # Show coherence across all lenses
    print(f"\n--- Coherence Across All Lenses ---")
    comparisons = glass.compare_lenses(result.psi, result.rho, result.q, result.f)
    for lens_name, visibility in comparisons.items():
        print(f"  {visibility.lens_name:25s} coherence: {visibility.coherence:.3f}")

    print(f"\nInterpretation:")
    if lens_deviation >= 0.1:
        print(f"  σ_lens ≥ 0.1 → CONTEXT-DEPENDENT")
        print(f"  Different lenses see this differently:")
        print(f"    - Activist lens: High coherence (q+f weighted)")
        print(f"    - Academic lens: Lower coherence (Ψ+ρ weighted)")
        print(f"    - Trauma-informed: Medium coherence (q heavy)")
        print(f"  **CONTINUE EXPLORATION** (not universal truth)")


def example_3_fibonacci_reset_sequence():
    """Example 3: Simulating Fibonacci reset sequence across multiple statements"""
    print("\n\n" + "="*70)
    print("Example 3: Fibonacci Reset Sequence Simulation")
    print("="*70 + "\n")

    glass = RoseLookingGlass(invariance_threshold=0.12)

    statements = [
        ("Activist", "We stand together for justice!"),
        ("Academic", "Based on research, I conclude this is optimal."),
        ("Emotional", "I'm terrified and don't know what to do!"),
        ("Wisdom", "On January 15th at 3:00 PM, precisely measured at 2.5 sigma confidence."),
        ("Neutral", "The data shows a clear correlation."),
    ]

    fibonacci_position = 1
    resets = []

    print("Tracking Fibonacci position as lens deviation changes:\n")

    for label, text in statements:
        result = glass.translate_text(text)
        should_reset, deviation = glass.should_reset_fibonacci(
            result.psi, result.rho, result.q, result.f
        )

        status = "🔄 RESET" if should_reset else "➡️  CONTINUE"

        print(f"[{label:12s}] σ_lens={deviation:.3f} | Fib={fibonacci_position:2d} | {status}")
        print(f"  Text: {text[:60]}...")

        if should_reset:
            fibonacci_position = 1  # Reset to beginning
            resets.append((label, deviation))
        else:
            # Advance Fibonacci (simplified: just increment)
            fibonacci_position += 1

        print()

    print(f"\n--- Summary ---")
    print(f"Total resets: {len(resets)}")
    if resets:
        print(f"Reset events:")
        for label, dev in resets:
            print(f"  - {label}: σ_lens={dev:.3f} (lens-invariant truth)")


def example_4_distortion_index():
    """Example 4: Veritas distortion index D(P) in action"""
    print("\n\n" + "="*70)
    print("Example 4: Veritas Distortion Index D(P)")
    print("="*70 + "\n")

    glass = RoseLookingGlass()

    print("Testing different patterns and their distortion indices:\n")

    test_cases = [
        ("High Logic", 0.9, 0.9, 0.1, 0.3, "Academic truth"),
        ("High Emotion", 0.5, 0.4, 0.8, 0.8, "Activist expression"),
        ("Paradox", 0.3, 0.9, 0.3, 0.2, "Contemplative wisdom"),
        ("Crisis", 0.4, 0.6, 0.9, 0.2, "Trauma state"),
        ("Balanced", 0.6, 0.6, 0.5, 0.5, "Neutral communication"),
    ]

    for label, psi, rho, q, f, description in test_cases:
        deviation = glass.calculate_lens_deviation(psi, rho, q, f)
        veritas = 1 / (1 + deviation)  # Veritas = 1 / (1 + D(P))

        print(f"{label:15s} | D(P)={deviation:.3f} | Veritas={veritas:.3f}")
        print(f"  Variables: Ψ={psi:.1f}, ρ={rho:.1f}, q={q:.1f}, f={f:.1f}")
        print(f"  Type: {description}")
        print()

    print("Interpretation:")
    print("  - Low D(P) → High Veritas → Universal truth")
    print("  - High D(P) → Low Veritas → Context-dependent")
    print("  - D(P) = lens deviation = σ_lens")


def main():
    """Run all examples"""
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║  Rose Looking Glass - Lens Deviation & Fibonacci Reset Examples  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    example_1_lens_invariant_truth()
    example_2_context_dependent_pattern()
    example_3_fibonacci_reset_sequence()
    example_4_distortion_index()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
    print("\nKey Insight:")
    print("  Lens deviation (σ_lens) = Veritas distortion index D(P)")
    print("  Low σ_lens → Universal truth → Reset Fibonacci")
    print("  High σ_lens → Context-dependent → Continue exploration")
    print("\n  'The Fibonacci spiral follows epistemological confidence.'")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
