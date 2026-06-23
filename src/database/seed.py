import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.connection import engine
from src.database.models import Base
from src.modules.data_ingestion.amr_parser import AMRDataReconciler


def execute_system_seeding():
    """
    Orchestrates full relational migrations on the Neon PostgreSQL cluster.
    Creates required multi-tenant schemas, provisions core asset tables,
    commits transactional seed data, and executes AMR reconciliation pipelines.
    """
    print("[INFO] Initiating database taxonomy verification loop...")

    # 1. Establish Secure Multi-Tenant Schema Boundaries Natively
    with engine.connect() as connection:
        print("[INFO] Provisioning isolated tenant schema containers...")
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS jv_swalek;"))
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS tenant_partnerbroker;"))
        connection.commit()

    # 2. Compile Declarative Table Structures across the Data Plane
    print("[INFO] Binding declarative tables to active target schemas...")
    Base.metadata.create_all(bind=engine)

    # 3. Open Direct Transactional Session to Seed Core Technical Taxonomy
    with Session(engine) as session:
        try:
            print("[INFO] Executing transactional DML injections for asset fleet...")

            # Using raw text blocks to guarantee execution safety regardless of model variation
            session.execute(text("""
                    CREATE TABLE IF NOT EXISTS jv_swalek.asset_registry (
                        id SERIAL PRIMARY KEY,
                        asset_class VARCHAR(100) UNIQUE,
                        nominal_kw DOUBLE PRECISION,
                        weekly_runtime_hours DOUBLE PRECISION,
                        base_thd_i DOUBLE PRECISION
                    );
                """))

            # Seed the absolute operational baseline categories
            core_assets = [
                ("Variable Speed Drive (VSD)", 75.0, 120.0, 38.0),
                ("Large Direct-on-Line Induction Motor", 110.0, 80.0, 5.0),
                ("LED Lighting & Server Clusters", 15.0, 168.0, 12.0),
                ("Arc Furnace & Heavy Welding Plant", 250.0, 35.0, 15.0),
            ]

            for asset_class, kw, runtime, thd in core_assets:
                session.execute(
                    text("""
                        INSERT INTO jv_swalek.asset_registry (asset_class, nominal_kw, weekly_runtime_hours, base_thd_i)
                        VALUES (:asset_class, :kw, :runtime, :thd)
                        ON CONFLICT (asset_class) DO UPDATE 
                        SET nominal_kw = EXCLUDED.nominal_kw,
                            weekly_runtime_hours = EXCLUDED.weekly_runtime_hours,
                            base_thd_i = EXCLUDED.base_thd_i;
                    """),
                    {
                        "asset_class": asset_class,
                        "kw": kw,
                        "runtime": runtime,
                        "thd": thd,
                    },
                )

            session.commit()
            print("[SUCCESS] Prepared seed record for: Variable Speed Drive (VSD)")
            print(
                "[SUCCESS] Prepared seed record for: Large Direct-on-Line Induction Motor"
            )
            print("[SUCCESS] Prepared seed record for: LED Lighting & Server Clusters")
            print(
                "[SUCCESS] Prepared seed record for: Arc Furnace & Heavy Welding Plant"
            )
            print(
                "[INFO] Database seeding complete. Asset taxonomy successfully active.\n"
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

    # Reconcile against an un-metered desktop survey estimation profile totaling 260 kW
    reconciliation_summary = reconciler.reconcile_desktop_survey(
        total_survey_kw=260.0, empirical_intervals=processed_stream
    )
    print(
        f"[REPORT] Survey Load Reconciliation: {reconciliation_summary['action_required']} "
        f"({reconciliation_summary['variance_divergence_pct']}% Divergence found)"
    )


if __name__ == "__main__":
    execute_system_seeding()
