import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd


class ProjectPersistenceRepository:
    """
    Handles the transactional persistence loop between front-end UI dataframes
    and the production PostgreSQL relational database. Features a defensive
    parent-checking architecture to eliminate foreign key integrity errors.
    """

    def __init__(self, db_engine):
        self.engine = db_engine

    def save_site_inventory_state(
        self, site_uuid_str: str, df_sandbox_assets: pd.DataFrame
    ) -> dict:
        """
        Translates human-readable datagrid fields into snake_case relational tables.
        Executes an atomic transactional block to safely write configuration metrics.
        """
        if df_sandbox_assets.empty:
            return {
                "status": "SKIPPED",
                "message": "Asset register is empty. Save bypassed.",
            }

        site_uuid = uuid.UUID(site_uuid_str)

        with Session(self.engine) as session:
            try:
                # 1. Establish an atomic transaction boundary
                session.begin()

                # 2. DEFENSIVE GUARD: Ensure parent context row exists to block FK IntegrityErrors
                session.execute(
                    text("""
                        INSERT INTO sites (site_id, site_name, client_id)
                        VALUES (:site_id, 'Messington HV Feasibility Scheme', NULL)
                        ON CONFLICT (site_id) DO NOTHING;
                    """),
                    {"site_id": site_uuid},
                )

                # 3. Clear out any legacy transient data configurations for this site node
                session.execute(
                    text("DELETE FROM site_inventories WHERE site_id = :site_id;"),
                    {"site_id": site_uuid},
                )

                # 4. Iterate and safely insert individual fleet asset structures
                inserted_count = 0
                for _, row in df_sandbox_assets.iterrows():
                    tag = str(row.get("Asset Tag", "")).strip()
                    if not tag:
                        continue

                    location = str(
                        row.get("Plant Location", "Main Distribution Busbar")
                    ).strip()
                    asset_class = str(row.get("Classification", "General Load")).strip()

                    try:
                        rating = float(
                            str(row.get("Rating (kW)", "0")).replace(",", "")
                        )
                        hours = float(row.get("Weekly Hrs", 40.0))
                    except ValueError:
                        rating = 45.0
                        hours = 40.0

                    # Lookup corresponding classification map asset_type_id
                    taxonomy_res = session.execute(
                        text(
                            "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = :ac LIMIT 1;"
                        ),
                        {"ac": asset_class},
                    ).fetchone()

                    if taxonomy_res:
                        type_id = taxonomy_res[0]
                    else:
                        # Defensive fallback category allocation
                        fallback_res = session.execute(
                            text(
                                "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = 'General Load' LIMIT 1;"
                            )
                        ).fetchone()
                        type_id = fallback_res[0] if fallback_res else uuid.uuid4()

                    # 5. Inject full relational parameters safely
                    session.execute(
                        text("""
                            INSERT INTO site_inventories (
                                inventory_id, site_id, asset_type_id, quantity, 
                                average_kw_rating, duty_cycle_hours_per_week
                            )
                            VALUES (:inventory_id, :site_id, :asset_type_id, 1, :rating, :hours);
                        """),
                        {
                            "inventory_id": uuid.uuid4(),
                            "site_id": site_uuid,
                            "asset_type_id": type_id,
                            "rating": rating,
                            "hours": hours,
                        },
                    )
                    inserted_count += 1

                # Commit all relational updates atomically
                session.commit()
                return {
                    "status": "SUCCESS",
                    "message": f"Relational sync complete! Saved {inserted_count} assets down to persistent database storage lines.",
                }

            except Exception as err:
                session.rollback()
                return {
                    "status": "CRASHED",
                    "message": f"Database Operation Fault: Core constraint transaction rollback executed. Detail: `{str(err)}`",
                }
