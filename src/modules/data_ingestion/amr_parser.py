from decimal import Decimal
import datetime


class AMRDataReconciler:
    """
    Ingests and processes half-hourly AMR data streams (Active and Reactive energy metrics).
    Analyses step-changes and characterises baseload anomalies to validate desktop survey baselines.
    """

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id.lower()

    def parse_half_hourly_reading(self, raw_reading: dict) -> dict:
        """
        Translates raw half-hourly consumption intervals into uniform load values.
        Converts active energy (kWh) and reactive energy (kVArh) to continuous demand indices.
        """
        active_kwh = Decimal(str(raw_reading.get("active_kwh", 0.0)))
        reactive_kvarh = Decimal(str(raw_reading.get("reactive_kvarh", 0.0)))

        # Energy consumed over 30 minutes translates to twice that value in average hourly demand (kW)
        avg_demand_kw = active_kwh * Decimal("2.0")
        avg_demand_kvar = reactive_kvarh * Decimal("2.0")

        # Compute apparent power: S = sqrt(P^2 + Q^2)
        apparent_kva = float(((avg_demand_kw**2) + (avg_demand_kvar**2)).sqrt())

        # Determine displacement power factor: Cos Phi = P / S
        cos_phi = float(avg_demand_kw) / apparent_kva if apparent_kva > 0 else 1.0

        return {
            "timestamp": raw_reading.get("timestamp"),
            "demand_kw": round(float(avg_demand_kw), 2),
            "demand_kvar": round(float(avg_demand_kvar), 2),
            "apparent_kva": round(apparent_kva, 2),
            "calculated_cos_phi": round(cos_phi, 2),
        }

    def detect_sudden_consumption_jumps(
        self, processed_intervals: list, jump_threshold_kw: float = 50.0
    ) -> list:
        """
        Scans chronological intervals to flag sharp step-changes in real-world energy demand.
        Sudden jumps suggest heavy asset start-events (e.g., induction motors cycling online).
        """
        detected_jumps = []
        if len(processed_intervals) < 2:
            return detected_jumps

        for i in range(1, len(processed_intervals)):
            prev = processed_intervals[i - 1]
            curr = processed_intervals[i]

            delta_kw = curr["demand_kw"] - prev["demand_kw"]

            # Identify significant upward step changes
            if delta_kw >= jump_threshold_kw:
                detected_jumps.append(
                    {
                        "timestamp": curr["timestamp"],
                        "pre_jump_kw": prev["demand_kw"],
                        "post_jump_kw": curr["demand_kw"],
                        "magnitude_step_kw": round(delta_kw, 2),
                    }
                )

        return detected_jumps

    def reconcile_desktop_survey(
        self, total_survey_kw: float, empirical_intervals: list
    ) -> dict:
        """
        Cross-references static surveyor checklist totals against actual peak utility demands.
        Identifies structural discrepancies between reported load capacity and real operations.
        """
        if not empirical_intervals:
            return {"status": "NO_EMPIRICAL_DATA", "variance_kw": 0.0}

        # Extract maximum peak demand observed inside the half-hourly profile records
        measured_peak_kw = max(item["demand_kw"] for item in empirical_intervals)
        survey_limit = float(Decimal(str(total_survey_kw)))

        # Calculate divergence
        variance_kw = survey_limit - measured_peak_kw
        variance_pct = (
            (variance_kw / measured_peak_kw) * 100 if measured_peak_kw > 0 else 0.0
        )

        # If survey estimation exceeds peak demand by over 25%, flag asset duty-cycle inflation
        is_over_estimated = variance_pct > 25.0

        return {
            "measured_peak_demand_kw": round(measured_peak_kw, 2),
            "surveyor_estimated_load_kw": round(survey_limit, 2),
            "variance_gap_kw": round(variance_kw, 2),
            "variance_divergence_pct": round(variance_pct, 1),
            "action_required": (
                "RE_CALIBRATE_DUTY_CYCLES"
                if is_over_estimated
                else "INTEGRITY_VERIFIED"
            ),
        }
