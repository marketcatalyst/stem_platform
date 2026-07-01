import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd


class ProjectPersistenceRepository:
    """
    Handles the transactional persistence loop between front-end UI dataframes
    and the production PostgreSQL relational database. Features runtime schema
    introspection to automatically adapt to variant target column fields.
    """

    def __init__(self, db_engine):
        self.engine = db_engine

    def _discover_site_name_column(self, session: Session) -> str:
        """
        Programmatically inspects the relational schema catalog parameters
        to discover the exact column token tracking site titles.
        """
        try:
            res = session.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'client_sites';
                """)).fetchall()

            columns = [str(r[0]).lower() for r in res]

            # Iteratively evaluate column candidates matching your production design
            for candidate in [
                "name",
                "site_name",
                "title",
                "site_title",
                "project_name",
                "label",
                "description",
            ]:
                if candidate in columns:
                    return candidate

            # Fallback to the first text column that isn't an identifier flag
            for col in columns:
                if col not in [
                    "site_id",
                    "client_id",
                    "id",
                    "created_at",
                    "updated_at",
                ]:
                    return col
            return "name"  # Absolute base default fallback
        except Exception:
            return "name"

    def fetch_all_registered_workspaces(self) -> list[dict]:
        """
        Queries the persistent database rows to discover all active project
        workspaces currently saved across the system architecture.
        """
        with Session(self.engine) as session:
            try:
                name_col = self._discover_site_name_column(session)

                # Programmatically construct an adaptive lookup script string
                query_str = f"SELECT site_id, {name_col} FROM client_sites ORDER BY {name_col} ASC;"
                result = session.execute(text(query_str)).fetchall()

                # Standardise the dictionary keys so your UI view layer remains completely clean
                return [
                    {"site_id": str(res[0]), "site_name": str(res[1])} for res in result
                ]
            except Exception as err:
                print(f"[WARNING] Could not fetch workspace directories: {str(err)}")
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

                # 🚀 Dynamic column lookup discovery pass executed live
                name_col = self._discover_site_name_column(session)

                # Compile an absolute auto-adaptive transaction command string
                adaptive_upsert_query = f"""
                    INSERT INTO client_sites (site_id, {name_col}, client_id)
                    VALUES (:site_id, :site_name, NULL)
                    ON CONFLICT (site_id) DO UPDATE SET {name_col} = :site_name;
                """

                session.execute(
                    text(adaptive_upsert_query),
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
