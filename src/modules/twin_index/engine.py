from decimal import Decimal
from src.modules.twin_index.schemas import RoughTwinAssessmentPayload


def calculate_predictive_lookalike_twin(
    payload: RoughTwinAssessmentPayload, taxonomy_map: dict
) -> dict:
    """
    Executes first-cut engineering logic to render a predictive model of a site's
    invisible power leaks based entirely on un-metered inventory assets.
    """
    total_connected_kw = Decimal("0.00")
    total_weekly_kwh = Decimal("0.00")
    weighted_power_factor = Decimal("0.00")
    cumulative_harmonic_risk_score = 0
    estimated_thermal_stress_multiplier = Decimal("1.00")

    asset_breakdown = []

    for asset in payload.assets:
        # Look up matching static electrical profiles from the pre-seeded taxonomy database
        tax_meta = taxonomy_map.get(str(asset.asset_type_id))
        if not tax_meta:
            continue

        qty = Decimal(str(asset.quantity))
        kw = Decimal(str(asset.average_kw_rating))
        hours = Decimal(str(asset.duty_cycle_hours_per_week))

        cos_phi = Decimal(str(tax_meta["default_cos_phi"]))
        thd_i = Decimal(str(tax_meta["default_thd_i"]))
        thermal_factor = Decimal(str(tax_meta["thermal_loss_factor"]))

        # Calculate base active load parameters
        connected_kw = qty * kw
        weekly_kwh = connected_kw * hours

        total_connected_kw += connected_kw
        total_weekly_kwh += weekly_kwh

        # Aggregate variables for systemic metrics
        weighted_power_factor += cos_phi * weekly_kwh

        # Process discrete power quality indicators mapped out in the taxonomy definitions
        if (
            tax_meta["triplen_harmonic_risk"]
            or tax_meta["voltage_flicker_risk"]
            or tax_meta["phase_imbalance_risk"]
        ):
            cumulative_harmonic_risk_score += int(qty)

        if thd_i > 15.0:
            # Multiplier compounds based on scale of non-linear offenders on-site
            estimated_thermal_stress_multiplier += (
                thermal_factor - Decimal("1.00")
            ) * (connected_kw / Decimal("100.00"))

        asset_breakdown.append(
            {
                "asset_class": tax_meta["asset_class"],
                "connected_load_kw": float(connected_kw),
                "weekly_consumption_kwh": float(weekly_kwh),
                "harmonic_distortion_baseline_pct": float(thd_i),
                "displacement_power_factor": float(cos_phi),
            }
        )

    # Avoid division by zero on empty or inactive facilities
    final_cos_phi = (
        float(weighted_power_factor / total_weekly_kwh) if total_weekly_kwh > 0 else 1.0
    )

    return {
        "summary": {
            "total_connected_load_kw": float(total_connected_kw),
            "estimated_weekly_consumption_kwh": float(total_weekly_kwh),
            "predicted_site_displacement_power_factor": round(final_cos_phi, 2),
            "systemic_harmonic_vulnerability_index": cumulative_harmonic_risk_score,
            "calculated_transformer_thermal_stress_factor": round(
                float(estimated_thermal_stress_multiplier), 2
            ),
        },
        "asset_analytics_breakdown": asset_breakdown,
    }
