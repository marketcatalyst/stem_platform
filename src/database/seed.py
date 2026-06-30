import os
import sys
import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.connection import engine, Base

# 🚀 CORE ENGINE INJECTIONS: Binding real multi-tenant ORM structural objects
from src.database.models import Tenant, AssetTaxonomy, ClientSite, SiteInventory
from src.modules.data_ingestion.amr_parser import AMRDataReconciler

# ==========================================================================
# 🛡️ PATH INSURANCE POLICY (CRITICAL FOR LINUX CLOUD DEPLOYMENTS)
# ==========================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


def execute_system_seeding():
    """
    Orchestrates full relational migrations on the Neon PostgreSQL cluster.
    Compiles declarative table schemas natively via the SQLAlchemy metadata plane,
    provisions multi-tenant profiles, and executes diagnostic AMR reconciliation loops.
    """
    print("[INFO] Initiating database taxonomy verification loop...")

    # 1. Establish Secure Multi-Tenant Schema Boundaries Natively if required by the cloud cluster
    with engine.connect() as connection:
        print("[INFO] Provisioning isolated tenant schema containers...")
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS public;"))
        connection.commit()

    # 2. Compile Declarative Table Structures across the Data Plane Natively
    print("[INFO] Binding declarative tables to active target production schemas...")
    Base.metadata.create_all(bind=engine)

    # 3. Open Direct Transactional Session to Seed Core Technical Taxonomy via ORM Blueprints
    with Session(engine) as session:
        try:
            print(
                "[INFO] Executing transactional ORM injections for multi-tenant asset fleet..."
            )

            # A. Provision Core Global Tenant Profile Account
            tenant_uid = "00000000-0000-0000-0000-000000000001"
            session.execute(
                text("""
                    INSERT INTO tenants (tenant_id, company_name, subdomain, branding_config)
                    VALUES (:tenant_id, 'Swalek Joint Venture Group', 'swalek', '{"theme": "corporate_dark"}')
                    ON CONFLICT (tenant_id) DO UPDATE
                    SET company_name = EXCLUDED.company_name;
                """),
                {"tenant_id": tenant_uid},
            )

            # B. Provision Target Client Site Location Facility Boundary
            site_uid = "00000000-0000-0000-0000-000000000002"
            session.execute(
                text("""
                    INSERT INTO client_sites (site_id, tenant_id, client_name, site_location, estimated_annual_spend, main_transformer_kva)
                    VALUES (:site_id, :tenant_id, 'Ammanford Alloys Ltd', 'Ammanford Facility Headquarter', 450000.00, 2500)
                    ON CONFLICT (site_id) DO UPDATE
                    SET client_name = EXCLUDED.client_name;
                """),
                {"site_id": site_uid, "tenant_id": tenant_uid},
            )

            # C. Seed the Absolute Operational Baseline Categories into the Asset Taxonomy Directory
            core_taxonomies = [
                (
                    "00000000-0000-0000-0000-000000000011",
                    "Variable Speed Drive (VSD)",
                    38.00,
                    0.85,
                    0.048,
                    "Automated drive circuits prone to severe high-frequency current distortion injection.",
                ),
                (
                    "00000000-0000-0000-0000-000000000012",
                    "Large Direct-on-Line Induction Motor",
                    5.00,
                    0.80,
                    0.048,
                    "Heavy inductive rotating loads characterized by high mechanical startup inrush transients.",
                ),
                (
                    "00000000-0000-0000-0000-000000000013",
                    "LED Lighting & Server Clusters",
                    12.00,
                    0.95,
                    0.048,
                    "Switched-mode non-linear auxiliary infrastructure generating cumulative single-phase neutral overloads.",
                ),
                (
                    "00000000-0000-0000-0000-000000000014",
                    "Arc Furnace & Heavy Welding Plant",
                    22.10,
                    0.70,
                    0.048,
                    "Extreme phase-imbalanced non-linear industrial process injection causing grid voltage flicker loops.",
                ),
            ]

            for tax_id, asset_class, thd, cos_phi, loss_factor, desc in core_taxonomies:
                session.execute(
                    text("""
                        INSERT INTO asset_taxonomy (asset_type_id, asset_class, default_thd_i, default_cos_phi, triplen_harmonic_risk, voltage_flicker_risk, phase_imbalance_risk, thermal_loss_factor, description)
                        VALUES (:tax_id, :asset_class, :thd, :cos_phi, FALSE, FALSE, FALSE, :loss_factor, :desc)
                        ON CONFLICT (asset_type_id) DO UPDATE 
                        SET asset_class = EXCLUDED.asset_class,
                            default_thd_i = EXCLUDED.default_thd_i,
                            default_cos_phi = EXCLUDED.default_cos_phi;
                    """),
                    {
                        "tax_id": tax_id,
                        "asset_class": asset_class,
                        "thd": thd,
                        "cos_phi": cos_phi,
                        "loss_factor": loss_factor,
                        "desc": desc,
                    },
                )

            # D. Populate the Site Inventory Checklist with Standard Production Node Items
            inventories_to_seed = [
                (
                    "00000000-0000-0000-0000-000000000101",
                    site_uid,
                    "00000000-0000-0000-0000-000000000011",
                    1,
                    75.00,
                    40.00,
                ),  # Matches VSD-04-LINE-3 specifications
                (
                    "00000000-0000-0000-0000-000000000102",
                    site_uid,
                    "00000000-0000-0000-0000-000000000012",
                    1,
                    250.00,
                    65.00,
                ),  # Matches MOT-12-CRUSHER specifications
                (
                    "00000000-0000-0000-0000-000000000103",
                    site_uid,
                    "00000000-0000-0000-0000-000000000014",
                    1,
                    3500.00,
                    24.00,
                ),  # Matches ARC-01-MELT specifications
            ]

            for inv_id, s_id, t_id, qty, rating, hours in inventories_to_seed:
                session.execute(
                    text("""
                        INSERT INTO site_inventories (inventory_id, site_id, asset_type_id, quantity, average_kw_rating, duty_cycle_hours_per_week)
                        VALUES (:inv_id, :s_id, :t_id, :qty, :rating, :hours)
                        ON CONFLICT (inventory_id) DO NOTHING;
                    """),
                    {
                        "inv_id": inv_id,
                        "s_id": s_id,
                        "t_id": t_id,
                        "qty": qty,
                        "rating": rating,
                        "hours": hours,
                    },
                )

            session.commit()
            print(
                "[SUCCESS] Multi-Tenant Relational Entities compiled and seeded successfully."
            )
            print(
                "[INFO] Database initialization complete. Standard taxonomy columns active.\n"
            )

        except Exception as error:
            session.rollback()
            print(f"[CRITICAL] Operational seed transaction aborted: {str(error)}")
            raise error

    # 4. Trigger Step-Change Diagnostic Test Profile from Andris's analysis
    print("[DIAGNOSTIC] Simulating Andris's half-hourly interval stream...")
    reconciler = AMRDataReconciler(tenant_id="swalek")

    # Chronological sequence containing an operational jump event (e.g., motor start-up sequence)
    simulated_meter_logs = [
        {
            "timestamp": "2026-06-22 06:00:00",
            "active_kwh": 40.0,
            "reactive_kvarh": 20.0,
        },  # 80 kW demand
        {
            "timestamp": "2026-06-22 06:30:00",
            "active_kwh": 42.0,
            "reactive_kvarh": 21.0,
        },  # 84 kW demand
        {
            "timestamp": "2026-06-22 07:00:00",
            "active_kwh": 95.0,
            "reactive_kvarh": 45.0,
        },  # 190 kW demand (Sudden Jump!)
        {
            "timestamp": "2026-06-22 07:30:00",
            "active_kwh": 93.0,
            "reactive_kvarh": 44.0,
        },  # 186 kW demand
    ]

    # Process the raw interval signatures through our parser calculations
    processed_stream = [
        reconciler.parse_half_hourly_reading(log) for log in simulated_meter_logs
    ]

    # Scan the processed timeline for anomalous step changes
    jumps = reconciler.detect_sudden_consumption_jumps(
        processed_stream, jump_threshold_kw=50.0
    )
    for jump in jumps:
        print(
            f"[ALERT] Sudden load step caught at {jump['timestamp']}! Magnitude: +{jump['magnitude_step_kw']} kW"
        )

    # Reconcile against an un-metered desktop survey estimation profile totaling 3825 kW (Full Survey Baseline)
    reconciliation_summary = reconciler.reconcile_desktop_survey(
        total_survey_kw=3825.0, empirical_intervals=processed_stream
    )
    print(
        f"[REPORT] Survey Load Reconciliation Status: {reconciliation_summary['action_required']} "
        f"({reconciliation_summary['variance_divergence_pct']}% Divergence found)"
    )


if __name__ == "__main__":
    execute_system_seeding()
