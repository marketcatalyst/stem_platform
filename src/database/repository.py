import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd


class ProjectPersistenceRepository:
    """
    Handles the transactional persistence loop between front-end UI dataframes
    and the production PostgreSQL relational database.
    """

    def __init__(self, db_engine):
        self.engine = db_engine

    def fetch_all_registered_workspaces(self) -> list:
        """
        Queries the database catalog for all existing project profiles.
        """
        query = "SELECT client_name FROM client_sites ORDER BY client_name;"
        with Session(self.engine) as session:
            try:
                res = session.execute(text(query)).fetchall()
                return [str(row[0]) for row in res]
            except Exception as err:
                print(f"[ERROR] Failed to fetch registered workspaces: {str(err)}")
                return ["Ammanford Alloys Ltd"]

    def get_all_saved_projects(self, tenant_id_str: str) -> list:
        """
        Retrieves a complete checklist profile directory of all custom named
        projects active for the authenticated corporate tenant.
        """
        # Hardened: Strict ANSI CAST ensures parameter compatibility
        query = "SELECT client_name FROM client_sites WHERE tenant_id = CAST(:tid AS UUID) ORDER BY client_name;"
        with Session(self.engine) as session:
            try:
                res = session.execute(
                    text(query), {"tid": str(tenant_id_str)}
                ).fetchall()
                return [str(row[0]) for row in res]
            except Exception as err:
                print(
                    f"[ERROR] Failed to index corporate projects portfolio: {str(err)}"
                )
                return ["Ammanford Alloys Ltd"]

    def get_or_create_site_by_name(
        self, tenant_id_str: str, client_name_str: str
    ) -> str:
        """
        Resolves a project string name to its underlying unique relational database site key.
        If no profile exists matching the text, a new site row is dynamically provisioned.
        """
        clean_name = client_name_str.strip()
        with Session(self.engine) as session:
            try:
                # 🛡️ Hardened: Strict ANSI CAST avoids colon operator collisions and type binding errors
                res = session.execute(
                    text(
                        "SELECT site_id FROM client_sites WHERE tenant_id = CAST(:tid AS UUID) AND client_name = :name LIMIT 1;"
                    ),
                    {"tid": str(tenant_id_str), "name": clean_name},
                ).fetchone()

                if res:
                    return str(res[0])

                new_site_id = uuid.uuid4()
                session.execute(
                    text("""
                        INSERT INTO client_sites (site_id, tenant_id, client_name, site_location, estimated_annual_spend, main_transformer_kva)
                        VALUES (CAST(:site_id AS UUID), CAST(:tenant_id AS UUID), :client_name, 'Staged Engineering Zone', 0.00, 1000);
                    """),
                    {
                        "site_id": str(new_site_id),
                        "tenant_id": str(tenant_id_str),
                        "client_name": clean_name,
                    },
                )
                session.commit()
                return str(new_site_id)
            except Exception as err:
                session.rollback()
                print(
                    f"[ERROR] Failed to map named project context boundary: {str(err)}"
                )
                raise err

    def load_site_inventory_state(self, site_uuid_str: str) -> pd.DataFrame:
        """
        Queries the persistent SQL database tables for saved inventory records
        belonging to a specific site facility node.
        """
        query = """
            SELECT 
                si.quantity,
                si.average_kw_rating as "Rating (kW)",
                si.duty_cycle_hours_per_week as "Weekly Hrs",
                t.asset_class as "Classification",
                t.default_thd_i as "Distortion (THD_i)"
            FROM site_inventories si
            JOIN asset_taxonomy t ON si.asset_type_id = t.asset_type_id
            WHERE si.site_id = CAST(:site_id AS UUID);
        """

        with Session(self.engine) as session:
            try:
                result = session.execute(
                    text(query), {"site_id": str(site_uuid_str)}
                ).fetchall()
                if not result:
                    return pd.DataFrame()

                records = []
                for idx, row in enumerate(result):
                    prefix = (
                        "EXT"
                        if row[3] == "General Load"
                        else (
                            "VSD"
                            if "VSD" in row[3]
                            else "MOT" if "Motor" in row[3] else "ARC"
                        )
                    )
                    records.append(
                        {
                            "Asset Tag": f"{prefix}-PARSED-{idx+1:02d}",
                            "Plant Location": "Extracted Low Voltage Panel Branch",
                            "Classification": row[3],
                            "Rating (kW)": float(row[1]),
                            "Weekly Hrs": float(row[2]),
                            "Distortion (THD_i)": float(row[4]),
                        }
                    )
                return pd.DataFrame(records)
            except Exception as err:
                print(f"[ERROR] Failed to fetch persistent project state: {str(err)}")
                return pd.DataFrame()

    def save_site_inventory_state(
        self, site_uuid_str: str, df_sandbox_assets: pd.DataFrame
    ) -> dict:
        """
        Translates human-readable datagrid fields into snake_case relational tables.
        Executes an atomic transactional block to wipe and overwrite the site checklist.
        """
        if df_sandbox_assets.empty:
            return {
                "status": "SKIPPED",
                "message": "Asset register is empty. Save bypassed.",
            }

        with Session(self.engine) as session:
            try:
                session.begin()

                session.execute(
                    text(
                        "DELETE FROM site_inventories WHERE site_id = CAST(:site_id AS UUID);"
                    ),
                    {"site_id": str(site_uuid_str)},
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
                            INSERT INTO site_inventories (inventory_id, site_id, asset_type_id, quantity, average_kw_rating, duty_cycle_hours_per_week)
                            VALUES (CAST(:inventory_id AS UUID), CAST(:site_id AS UUID), CAST(:asset_type_id AS UUID), 1, :rating, :hours);
                        """),
                        {
                            "inventory_id": str(uuid.uuid4()),
                            "site_id": str(site_uuid_str),
                            "asset_type_id": str(type_id),
                            "rating": rating,
                            "hours": hours,
                        },
                    )
                    inserted_count += 1

                session.commit()
                return {
                    "status": "SUCCESS",
                    "message": f"Successfully saved {inserted_count} rows down to Neon SQL database persistence tables.",
                }
            except Exception as e:
                session.rollback()
                raise e
