import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd


class ProjectPersistenceRepository:
    """
    Handles the transactional persistence loop between front-end UI dataframes
    and the production PostgreSQL relational database. Target mappings are aligned
    explicitly with production 'client_sites' reference boundaries.
    """

    def __init__(self, db_engine):
        self.engine = db_engine

    def fetch_all_registered_workspaces(self) -> list[dict]:
        """
        Queries the persistent database rows to discover all active project
        workspaces currently saved across the system architecture.
        """
        with Session(self.engine) as session:
            try:
                # Aligned target to match 'client_sites' infrastructure
                result = session.execute(
                    text(
                        "SELECT site_id, site_name FROM client_sites ORDER BY site_name ASC;"
                    )
                ).fetchall()
                return [
                    {"site_id": str(res[0]), "site_name": str(res[1])} for res in result
                ]
            except Exception as err:
                print(f"[WARNING] Could not clear workspace directories: {str(err)}")
                return []

    def load_site_inventory_state(self, site_uuid_str: str) -> pd.DataFrame:
        """
        Queries persistent SQL storage lines for an active facility node.
        Maps snake_case database rows back into a formatted layout grid asset fleet.
        """
        site_uuid = uuid.UUID(site_uuid_str)

        with Session(self.engine) as session:
            try:
                result = session.execute(
                    text("""
                        SELECT t.asset_class, i.average_kw_rating, i.duty_cycle_hours_per_week
                        FROM site_inventories i
                        JOIN asset_taxonomy t ON i.asset_type_id = t.asset_type_id
                        WHERE i.site_id = :site_id;
                    """),
                    {"site_id": site_uuid},
                ).fetchall()

                if not result:
                    return pd.DataFrame()

                rows = []
                for idx, res in enumerate(result):
                    asset_class = str(res[0])
                    rating = float(res[1])
                    hours = float(res[2])

                    if "Transformer" in asset_class:
                        tag = f"TX-NODE-{idx+1:03d}"
                        loc = "Primary Intake Switchboard"
                        thd = 1.2
                    elif "Furnace" in asset_class or "Melt" in asset_class:
                        tag = f"FRN-CORE-{idx+1:03d}"
                        loc = "Heavy Industrial Process Board (Panel B1)"
                        thd = 22.1
                    elif (
                        "Drive" in asset_class
                        or "VSD" in asset_class
                        or "Pump" in asset_class
                    ):
                        tag = f"DRV-FEEDER-{idx+1:03d}"
                        loc = "Motor Control Centre (MCC Panel B2)"
                        thd = 38.0
                    else:
                        tag = f"LOAD-NODE-{idx+1:03d}"
                        loc = "Auxiliary & Building Services (Panel B3)"
                        thd = 4.5

                    rows.append(
                        {
                            "Asset Tag": tag,
                            "Plant Location": loc,
                            "Classification": asset_class,
                            "Rating (kW)": rating,
                            "Weekly Hrs": hours,
                            "Distortion (THD_i)": thd,
                        }
                    )

                return pd.DataFrame(rows)

            except Exception as err:
                print(f"[ERROR] Session state hydration failed: {str(err)}")
                return pd.DataFrame()

    def save_site_inventory_state(
        self, site_uuid_str: str, project_name: str, df_sandbox_assets: pd.DataFrame
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
                session.begin()

                # 🛠️ FIXED: Redirect upsert target to 'client_sites' to resolve foreign key constraints
                session.execute(
                    text("""
                        INSERT INTO client_sites (site_id, site_name, client_id)
                        VALUES (:site_id, :site_name, NULL)
                        ON CONFLICT (site_id) DO UPDATE SET site_name = :site_name;
                    """),
                    {"site_id": site_uuid, "site_name": project_name.strip()},
                )

                session.execute(
                    text("DELETE FROM site_inventories WHERE site_id = :site_id;"),
                    {"site_id": site_uuid},
                )

                inserted_count = 0
                for _, row in df_sandbox_assets.iterrows():
                    tag = str(row.get("Asset Tag", "")).strip()
                    if not tag:
                        continue

                    asset_class = str(row.get("Classification", "General Load")).strip()

                    try:
                        rating = float(
                            str(row.get("Rating (kW)", "0")).replace(",", "")
                        )
                        hours = float(row.get("Weekly Hrs", 40.0))
                    except ValueError:
                        rating = 45.0
                        hours = 40.0

                    taxonomy_res = session.execute(
                        text(
                            "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = :ac LIMIT 1;"
                        ),
                        {"ac": asset_class},
                    ).fetchone()

                    if taxonomy_res:
                        type_id = taxonomy_res[0]
                    else:
                        fallback_res = session.execute(
                            text(
                                "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = 'General Load' LIMIT 1;"
                            )
                        ).fetchone()
                        type_id = fallback_res[0] if fallback_res else uuid.uuid4()

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

                session.commit()
                return {
                    "status": "SUCCESS",
                    "message": f"Relational sync complete! Saved workspace '{project_name}' containing {inserted_count} assets.",
                }

            except Exception as err:
                session.rollback()
                return {
                    "status": "CRASHED",
                    "message": f"Database Operation Fault: Core constraint transaction rollback executed. Detail: `{str(err)}`",
                }
