from decimal import Decimal


def calculate_thermal_acceleration_factor(
    transformer_thermal_stress_factor: float,
) -> float:
    """
    Applies Arrhenius thermal acceleration principles to compute insulation degradation.
    Determines how background harmonic profiles accelerate winding breakdown.
    """
    stress_factor = Decimal(str(transformer_thermal_stress_factor))

    # If there is no elevated thermal stress, degradation runs at nominal base speed
    if stress_factor <= Decimal("1.00"):
        return 1.0

    # Extrapolate localised temperature delta from system stress overhead
    # Each 0.10 increase past nominal stress maps to a 2°C baseline temperature rise
    delta_t = (stress_factor - Decimal("1.00")) * Decimal("20.00")

    # Enforce the 10°C thermal runaway rule: Acceleration Factor = 2^(ΔT / 10)
    acceleration_factor = Decimal("2") ** (delta_t / Decimal("10.00"))

    return float(acceleration_factor)
