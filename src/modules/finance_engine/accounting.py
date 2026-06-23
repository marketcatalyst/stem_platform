from decimal import Decimal


def calculate_balance_sheet_optimisation(
    asset_purchase_value: float,
    base_useful_life_years: float,
    acceleration_factor: float,
) -> dict:
    """
    Translates technical degradation variables into balance-sheet depreciation models.
    Provides the client's board with an unassailable capital preservation case.
    """
    val = Decimal(str(asset_purchase_value))
    base_life = Decimal(str(base_useful_life_years))
    accel = Decimal(str(acceleration_factor))

    # Compute the degraded economic lifespan caused by unmitigated grid stress
    degraded_useful_life = base_life / accel if accel > 0 else base_life

    # Compute annual asset depreciation under unmitigated, degraded conditions
    annual_depreciation_degraded = val / degraded_useful_life

    # Compute normal depreciation once STEM interventions restore operations to base life
    annual_depreciation_optimised = val / base_life

    # Net annual cash preservation value
    annual_savings = annual_depreciation_degraded - annual_depreciation_optimised

    return {
        "degraded_useful_life_years": round(float(degraded_useful_life), 1),
        "optimised_useful_life_years": float(base_life),
        "annual_depreciation_degraded_gbp": round(
            float(annual_depreciation_degraded), 2
        ),
        "annual_depreciation_optimised_gbp": round(
            float(annual_depreciation_optimised), 2
        ),
        "annual_balance_sheet_savings_gbp": round(float(annual_savings), 2),
    }
