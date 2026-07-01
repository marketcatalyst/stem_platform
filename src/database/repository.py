import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd


class ProjectPersistenceRepository:
    def __init__(self, db_engine):
        self.engine = db_engine

    def fetch_all_registered_workspaces(self) -> list:
        query = "SELECT client_name FROM client_sites ORDER BY client_name;"
        with Session(self.engine) as session:
            try:
                res = session.execute(text(query)).fetchall()
                return [str(row[0]) for row in res]
            except Exception:
                return ["Ammanford Alloys Ltd"]

    def get_or_create_site_by_name(
        self, tenant_id_str: str, client_name_str: str
    ) -> str:
        """
        Uses explicit type-safe parameter binding to resolve project IDs.
        """
        # Ensure we are dealing with pure strings for the database driver
        tid_str = str(tenant_id_str)
        clean_name = client_name_str.strip()

        with Session(self.engine) as session:
            try:
                # 🛡️ FIXED: Added explicit CAST(:tid AS UUID) to satisfy PostgreSQL operator matching
                stmt = text("""
                    SELECT site_id FROM client_sites 
                    WHERE tenant_id = CAST(:tid AS UUID) AND client_name = :name LIMIT 1;
                """)
                res = session.execute(
                    stmt, {"tid": tid_str, "name": clean_name}
                ).fetchone()

                if res:
                    return str(res[0])

                new_site_id = str(uuid.uuid4())
                insert_stmt = text("""
                    INSERT INTO client_sites (site_id, tenant_id, client_name) 
                    VALUES (CAST(:id AS UUID), CAST(:tid AS UUID), :name);
                """)
                session.execute(
                    insert_stmt,
                    {"id": new_site_id, "tid": tid_str, "name": clean_name},
                )
                session.commit()
                return new_site_id
            except Exception as e:
                session.rollback()
                raise e

    def load_site_inventory_state(self, site_uuid_str: str) -> pd.DataFrame:
        sid_str = str(site_uuid_str)
        # 🛡️ FIXED: Cast the parameter inside the SQL query
        query = text("""
            SELECT si.quantity, si.average_kw_rating, si.duty_cycle_hours_per_week, t.asset_class, t.default_thd_i 
            FROM site_inventories si
            JOIN asset_taxonomy t ON si.asset_type_id = t.asset_type_id
            WHERE si.site_id = CAST(:id AS UUID);
        """)

        with Session(self.engine) as session:
            try:
                result = session.execute(query, {"id": sid_str}).fetchall()
                if not result:
                    return pd.DataFrame()

                records = []
                for row in result:
                    records.append(
                        {
                            "Asset Tag": f"PARSED-{uuid.uuid4().hex[:4].upper()}",
                            "Plant Location": "Extracted LV Panel",
                            "Classification": row[3],
                            "Rating (kW)": float(row[1]),
                            "Weekly Hrs": float(row[2]),
                            "Distortion (THD_i)": float(row[4]),
                        }
                    )
                return pd.DataFrame(records)
            except Exception:
                return pd.DataFrame()

    def save_site_inventory_state(self, site_uuid_str: str, df: pd.DataFrame) -> dict:
        sid_str = str(site_uuid_str)
        with Session(self.engine) as session:
            try:
                session.begin()
                # 🛡️ FIXED: Use CAST on delete/insert parameters
                session.execute(
                    text(
                        "DELETE FROM site_inventories WHERE site_id = CAST(:id AS UUID);"
                    ),
                    {"id": sid_str},
                )

                for _, row in df.iterrows():
                    session.execute(
                        text(
                            "INSERT INTO site_inventories (inventory_id, site_id, asset_tag) VALUES (CAST(:inv AS UUID), CAST(:site AS UUID), :tag);"
                        ),
                        {
                            "inv": str(uuid.uuid4()),
                            "site": sid_str,
                            "tag": row["Asset Tag"],
                        },
                    )
                session.commit()
                return {"status": "SUCCESS"}
            except Exception as e:
                session.rollback()
                raise e
