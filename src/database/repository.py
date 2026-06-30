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

        site_uuid = uuid.UUID(site_uuid_str)

        with Session(self.engine) as session:
            try:
                # 1. Establish an atomic transaction boundary
                session.begin()

                # 2. Clear out the legacy staging rows for this specific facility node
                session.execute(
                    text("DELETE FROM site_inventories WHERE site_id = :site_id;"),
                    {"site_id": site_uuid},
                )

                print(
                    f"[INFO] Cleared stale inventory configurations for site {site_uuid_str}"
                )

                # 3. Iterate through rows and resolve taxonomy associations live
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

                    # Lookup corresponding asset_type_id from the look-up table directory
                    taxonomy_res = session.execute(
                        text(
                            "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = :ac LIMIT 1;"
                        ),
                        {"ac": asset_class},
                    ).fetchone()

                    if taxonomy_res:
                        type_id = taxonomy_res[0]
                    else:
                        # Fallback default category allocation if anomalous text is input
                        fallback_res = session.execute(
                            text(
                                "SELECT asset_type_id FROM asset_taxonomy WHERE asset_class = 'General Load' LIMIT 1;"
                            )
                        ).fetchone()
                        type_id = fallback_res[0] if fallback_res else uuid.uuid4()

                    # 4. Inject the unified structural data constraint
                    session.execute(
                        text("""
                            INSERT INTO site_inventories (inventory_id, site_id, asset_type_id, quantity, average_kw_rating, duty_cycle_hours_per_week)
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

                # Commit all relational changes together atomically
                session.commit()
                return {
                    "status": "SUCCESS",
                    "message": f"Successfully synchronised and saved {inserted_count} equipment rows to database persistence tables.",
                }

            except Exception as err:
                session.rollback()
                print(
                    f"[CRITICAL] Project state save failed. Rolled back transaction. Error: {str(err)}"
                )
                raise err
