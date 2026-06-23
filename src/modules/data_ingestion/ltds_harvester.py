from decimal import Decimal


class LTDSHarvester:
    """
    Ingests and parses public utility network parameters from DNO Long Term Development Statements.
    Utilises public grid parameters to seed local structural fault-level logic.
    """

    def __init__(self, dno_region_id: str):
        self.dno_region_id = dno_region_id.upper()

    def parse_substation_headroom(self, substation_name: str) -> dict:
        """
        Simulates parsing a DNO open data matrix to extract capacity parameters.
        Ensures the engine can cross-reference available capacity before pitching green infrastructure.
        """
        # Mock payload matching structure required for Ofgem Data Best Practice guidelines
        return {
            "substation_name": substation_name.upper(),
            "region": self.dno_region_id,
            "transformer_size_mva": 45.0,
            "firm_capacity_mva": 38.5,
            "current_peak_demand_mva": 29.2,
            "available_headroom_mva": float(Decimal("38.5") - Decimal("29.2")),
            "three_phase_fault_level_ka": 25.4,
        }

    def calculate_source_impedance(
        self, nominal_kv: float, fault_level_mva: float
    ) -> dict:
        """
        Computes base network short-circuit impedances to drive upstream grid models.
        """
        kv = Decimal(str(nominal_kv))
        mva = Decimal(str(fault_level_mva))

        if mva <= 0:
            return {"r_ohms": 0.0, "x_ohms": 0.0}

        # Z_base = (kV^2) / MVA
        z_ohms = (kv**2) / mva

        # Approximate standard UK grid X/R distribution ratio of 10
        x_ohms = z_ohms * Decimal("0.995")
        r_ohms = z_ohms * Decimal("0.099")

        return {"r_ohms": round(float(r_ohms), 5), "x_ohms": round(float(x_ohms), 5)}
