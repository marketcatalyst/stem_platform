from decimal import Decimal


class BESSActiveFilterController:
    """
    Models a dual-benefit Battery Energy Storage System running active power conditioning.
    Simultaneously executes harmonic cancellation and millisecond-level resilience logic.
    """

    def __init__(self, capacity_kwh: float, power_rating_kw: float):
        self.capacity_kwh = Decimal(str(capacity_kwh))
        self.power_rating_kw = Decimal(str(power_rating_kw))
        self.state_of_charge_pct = Decimal(
            "50.0"
        )  # Initialise at standard neutral state

    def process_harmonic_mitigation_loop(self, incoming_thd_i: float) -> dict:
        """
        Simulates dynamic, phase-locked high-frequency opposite waveform injection.
        Protects upstream distribution transformers from distortion stress patterns.
        """
        thd = Decimal(str(incoming_thd_i))

        # Compute targeted compensation scale required to bring THD within statutory targets
        if thd <= Decimal("5.00"):
            attenuation_required_pct = Decimal("0.00")
            pcs_thermal_overhead_pct = Decimal("0.00")
        else:
            # Active filtering overhead strains the PCS inverter components
            attenuation_required_pct = ((thd - Decimal("5.00")) / thd) * Decimal(
                "100.00"
            )
            pcs_thermal_overhead_pct = thd * Decimal("1.8")

        return {
            "harmonic_attenuation_achieved_pct": round(
                float(attenuation_required_pct), 2
            ),
            "remaining_site_thd_i": 5.0 if thd > 5.0 else float(thd),
            "pcs_inverter_thermal_load_pct": min(
                round(float(pcs_thermal_overhead_pct), 2), 100.0
            ),
        }

    def evaluate_resilience_transition(self, grid_voltage_pu: float) -> dict:
        """
        Evaluates millisecond-level transitions to an isolated voltage-source loop
        during regional grid brown-out or sudden voltage sag conditions.
        """
        voltage = Decimal(str(grid_voltage_pu))

        # Trigger isolation state if voltage deviates past standard statutory limits (0.90 pu)
        if voltage < Decimal("0.90"):
            island_mode_active = True
            transition_time_ms = (
                4.2  # Sub-cycle response threshold accomplished via hardware PCS
            )
            discharge_load_kw = float(self.power_rating_kw * Decimal("0.85"))
        else:
            island_mode_active = False
            transition_time_ms = 0.0
            discharge_load_kw = 0.0

        return {
            "island_mode_active": island_mode_active,
            "transition_latency_ms": transition_time_ms,
            "emergency_discharge_delivery_kw": discharge_load_kw,
        }
