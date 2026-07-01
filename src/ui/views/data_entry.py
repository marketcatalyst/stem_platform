import os
import sys
import uuid
import streamlit as st
import pandas as pd
import numpy as np
from google import genai
from google.genai import types

# ==========================================================================
# 🛡️ PATH INSURANCE POLICY (CRITICAL FOR LINUX CLOUD DEPLOYMENTS)
# ==========================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.ui.views.operations import load_ammanford_alloys_dataset
from src.modules.data_ingestion.amr_parser import AMRDataReconciler
from src.modules.data_ingestion.sld_parser import MultimodalSLDParser
from src.database.connection import engine
from src.database.repository import ProjectPersistenceRepository


def update_electrical_mitigation_nodes(nodes: list[str]) -> str:
    """Executes a structural mutation of the SLD network architecture memory."""
    st.session_state.selected_nodes = nodes
    return f"Consensus updated. Native active nodes deployed: {nodes}"


def generate_dynamic_sld_graph(df: pd.DataFrame, selected_mitigations: list) -> str:
    """
    Programmatically constructs an adaptive, 3-column vertical SLD tree schema.
    Dynamically injects multiple parallel STEM mitigation blocks into any combination
    of circuits selected by the steering committee or conversational co-pilot.
    """
    dot_nodes = [
        "digraph G {",
        '  graph [rankdir=TB, bgcolor="transparent", fontname="Helvetica", nodesep=0.4, ranksep=0.4, compound=true];',
        '  node [fontname="Helvetica", shape=box, style="filled", fillcolor="#F8F9FA", color="#CED4DA", penwidth=1.5];',
        '  edge [fontname="Helvetica", color="#495057", penwidth=1.2];',
        "",
        "  // ⚡ Core Infrastructure Incoming Grid Foundations",
        '  GRID [label="🔋 National Grid\\n11kV Incoming Boundary", shape=cloud, fillcolor="#E8F4FD", color="#1D82DC"];',
        '  BUS_MAIN [label="🎛️ Primary Intake Switchboard\\nMain Busbar Distribution Panel", fillcolor="#E9ECEF", style="filled,bold", penwidth=2];',
        '  GRID -> BUS_MAIN [label=" Main Intake"];',
        "",
    ]

    if any("Primary Intake" in str(node) for node in selected_mitigations):
        dot_nodes.append(
            '  SUB_STEM_CENTRAL [label="🛡️ STEM OPTIMISATION BAY\\nCentralised Filtering Matrix", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.5];'
        )
        dot_nodes.append(
            '  SUB_STEM_CENTRAL -> BUS_MAIN [color="#28A745", penwidth=2.0, arrowhead=normal, label=" Active Injection", weight=0];'
        )

    heavy_assets = []
    drive_assets = []
    aux_assets = []

    for _, row in df.iterrows():
        if pd.isna(row.get("Asset Tag")) or str(row.get("Asset Tag")).strip() == "":
            continue

        tag = str(row.get("Asset Tag")).strip()
        classification = str(row.get("Classification", "General Load")).strip()
        loc = str(row.get("Plant Location", "Main Busbar")).strip()

        try:
            rating_val = (
                str(row.get("Rating (kW)", "0"))
                .replace("kW", "")
                .replace(",", "")
                .strip()
            )
            rating = float(rating_val) if rating_val else 0.0
        except ValueError:
            rating = 0.0

        try:
            thd_val = str(row.get("Distortion (THD_i)", "0")).replace("%", "").strip()
            thd = float(thd_val) if thd_val else 0.0
        except ValueError:
            thd = 0.0

        clean_id = "".join(c if c.isalnum() or c == "_" else "_" for c in tag)
        if not clean_id or clean_id == "____":
            continue

        is_mitigated = loc in selected_mitigations
        mit_label = " [MITIGATED]" if is_mitigated else ""

        if thd > 15.0 and not is_mitigated:
            node_style = f'label="⚠️ {tag}{mit_label}\\n{classification}\\n{rating:,.0f} kW | THD: {thd:.1f}%", fillcolor="#FCE8E6", color="#D9272E", penwidth=1.8'
        elif "Transformer" in classification:
            node_style = f'label="🔌 {tag}{mit_label}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#FFF3CD", color="#FFC107"'
        else:
            node_style = f'label="⚙️ {tag}{mit_label}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#F8F9FA", color="#6C757D"'

        asset_tuple = (clean_id, node_style)
        if "Furnace" in classification or "Melt" in classification or rating >= 1000:
            heavy_assets.append(asset_tuple)
        elif (
            "Drive" in classification
            or "VSD" in classification
            or "Pump" in classification
            or "Motor" in classification
        ):
            drive_assets.append(asset_tuple)
        else:
            aux_assets.append(asset_tuple)

    # 1. Heavy Process Board Subgraph
    dot_nodes.append("  subgraph cluster_heavy {")
    dot_nodes.append('    label="⚡ Heavy Industrial Process Board";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#FFFDF6"; color="#D1A113"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_HEAVY [label="⚡ Furnace Sub-Distribution\\nBusbar Node B1", fillcolor="#FFF3CD", style="filled,bold"];'
    )

    last_id = "BUS_HEAVY"
    for cid, style in heavy_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_HEAVY -> {cid} [weight=10];")
        if last_id != "BUS_HEAVY":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    # 2. Automated Drives MCC Subgraph
    dot_nodes.append("  subgraph cluster_drives {")
    dot_nodes.append('    label="⚙️ Motor Control Centre (MCC)";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#F4F9FF"; color="#2B72C4"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_DRIVES [label="⚙️ Automated Drive Panel\\nBusbar Node B2", fillcolor="#E2F0FE", style="filled,bold"];'
    )

    if any("BESS" in str(node) or "UPS" in str(node) for node in selected_mitigations):
        dot_nodes.append(
            '    SUB_STEM_BESS [label="🔋 LOCAL BESS & HYBRID UPS\\nProcess Protection Grid Shield", fillcolor="#E6FFFA", color="#00A389", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    SUB_STEM_BESS -> BUS_DRIVES [color="#00A389", penwidth=2.0, arrowhead=normal, label=" Dual-Duty Ride-Through", weight=0];'
        )

    last_id = "BUS_DRIVES"
    for cid, style in drive_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_DRIVES -> {cid} [weight=10];")
        if last_id != "BUS_DRIVES":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    # 3. Auxiliary Infrastructure Subgraph
    dot_nodes.append("  subgraph cluster_aux {")
    dot_nodes.append('    label="🏢 Auxiliary & Building Services";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#F8F9FA"; color="#6C757D"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_AUX [label="🏢 Commercial Infrastructure\\nBusbar Node B3", fillcolor="#E9ECEF", style="filled,bold"];'
    )

    last_id = "BUS_AUX"
    for cid, style in aux_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_AUX -> {cid} [weight=10];")
        if last_id != "BUS_AUX":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    dot_nodes.append("")
    dot_nodes.append(
        '  BUS_MAIN -> BUS_HEAVY [color="#D1A113", penwidth=2.0, weight=5];'
    )
    dot_nodes.append(
        '  BUS_MAIN -> BUS_DRIVES [color="#2B72C4", penwidth=2.0, weight=5];'
    )
    dot_nodes.append('  BUS_MAIN -> BUS_AUX [color="#6C757D", penwidth=2.0, weight=5];')

    dot_nodes.append("}")
    return "\n".join(dot_nodes)


def render_data_entry_view():
    """
    Renders the unified split workspace combining streaming financial tickers,
    executive ribbons, and a fully parameter-aware conversational Gemini co-pilot engine.
    """
    repo_engine = ProjectPersistenceRepository(db_engine=engine)

    # ==========================================================================
    # 🛡️ APEX STATE HYDRATION MATRIX (ELIMINATES STREAMLIT RACE CONDITIONS)
    # ==========================================================================
    if "copilot_history" not in st.session_state:
        st.session_state["copilot_history"] = [
            {
                "role": "assistant",
                "text": "👋 Welcome to the upgraded STEM Executive Portal. I am synced with your plant parameters, macro opportunity-cost models, and insurance premium risk curves. Let's optimise the network's financial engineering.",
            }
        ]

    if "selected_nodes" not in st.session_state:
        st.session_state.selected_nodes = []

    if "prod_val" not in st.session_state:
        st.session_state.prod_val = 150000

    if "restart_hrs" not in st.session_state:
        st.session_state.restart_hrs = 4.0

    if "annual_events" not in st.session_state:
        st.session_state.annual_events = 3

    # ==========================================================================
    # 📁 PROJECT WORKSPACE MANAGER CONTROLLER
    # ==========================================================================
    active_user_handle = (
        st.sidebar.text_input(
            "User Identity Initials / Handle:",
            value="MD",
            help="Type your unique initials or corporate role string to partition your project profiles.",
        )
        .strip()
        .lower()
    )

    existing_records = repo_engine.fetch_all_registered_workspaces()
    workspace_names = [record["site_name"] for record in existing_records]

    menu_choices = ["➕ Create New Project Workspace..."] + workspace_names
    selected_menu_item = st.sidebar.selectbox(
        "Select Active Project Workspace:", options=menu_choices
    )

    if selected_menu_item == "➕ Create New Project Workspace...":
        target_project_name = st.sidebar.text_input(
            "Enter New Project Identity Name:", value="Ammanford Alloys Phase 1"
        )
    else:
        target_project_name = selected_menu_item

    derived_namespace_salt = (
        f"{active_user_handle}_{target_project_name.strip().lower()}"
    )
    active_site_uid_str = str(uuid.uuid5(uuid.NAMESPACE_DNS, derived_namespace_salt))
    st.sidebar.caption(f"**Deterministic Workspace UUID:**\n`{active_site_uid_str}`")

    if (
        "current_loaded_project" not in st.session_state
        or st.session_state.current_loaded_project != target_project_name
    ):
        st.session_state.current_loaded_project = target_project_name
        df_hydrated_session = repo_engine.load_site_inventory_state(active_site_uid_str)

        if not df_hydrated_session.empty:
            st.session_state.sandbox_assets = df_hydrated_session
        else:
            st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    if "sandbox_assets" not in st.session_state:
        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    with st.sidebar.expander("💼 Macro Facility Variables", expanded=False):
        st.number_input(
            "Hourly Production Value (£)",
            min_value=100,
            max_value=500000,
            step=5000,
            key="prod_val",
        )
        st.number_input(
            "Process Reset Loop Duration (Hrs)",
            min_value=1.0,
            max_value=24.0,
            step=0.5,
            key="restart_hrs",
        )
        st.number_input(
            "Typical Utility Grid Sags / Year",
            min_value=1,
            max_value=50,
            step=1,
            key="annual_events",
        )

    # ==========================================================================
    # 🧮 DEEP-DIVE SYSTEMIC INEFFICIENCY EVALUATION LOOPS
    # ==========================================================================
    unmitigated_technical_bleed = 0.0
    mitigated_technical_bleed = 0.0

    total_copper_savings_captured = 0.0
    total_insulation_savings_captured = 0.0
    total_transformer_savings_captured = 0.0
    total_counter_torque_savings_captured = 0.0
    total_hvac_savings_captured = 0.0
    total_reactive_penalty_savings_captured = 0.0

    utility_rate = 0.22
    kva_penalty_factor = 14.50

    for _, row in st.session_state.sandbox_assets.iterrows():
        try:
            kw = float(str(row["Rating (kW)"]).replace(",", ""))
            hours = float(row["Weekly Hrs"])
            thd_base = float(str(row["Distortion (THD_i)"]).replace("%", ""))
            loc = str(row["Plant Location"])
            classification = str(row["Classification"])
        except (ValueError, KeyError):
            continue

        if thd_base > 5.0:
            base_copper_waste_kwh = kw * ((thd_base / 100.0) * 0.048) * hours * 52
            base_insulation_penalty = kw * (thd_base / 100.0) * 12.50
            base_trans_waste_kwh = kw * ((thd_base / 100.0) ** 2 * 0.015) * hours * 52

            if any(m in classification for m in ["Motor", "VSD", "Drive", "Pump"]):
                base_torque_waste_kwh = kw * (thd_base / 100.0) * 0.035 * hours * 52
            else:
                base_torque_waste_kwh = 0.0

            base_thermal_load_kwh = (
                base_copper_waste_kwh
                + base_trans_waste_kwh
                + (base_torque_waste_kwh * 0.4)
            )
            base_hvac_waste_kwh = base_thermal_load_kwh * 0.35
            base_reactive_penalty = (
                kw * (thd_base / 100.0) * 0.12
            ) * kva_penalty_factor
        else:
            base_copper_waste_kwh = 0.0
            base_insulation_penalty = 0.0
            base_trans_waste_kwh = 0.0
            base_torque_waste_kwh = 0.0
            base_hvac_waste_kwh = 0.0
            base_reactive_penalty = 0.0

        row_base_total_bleed = (
            (
                base_copper_waste_kwh
                + base_trans_waste_kwh
                + base_torque_waste_kwh
                + base_hvac_waste_kwh
            )
            * utility_rate
            + base_insulation_penalty
            + base_reactive_penalty
        )
        unmitigated_technical_bleed += row_base_total_bleed

        if loc in st.session_state.selected_nodes:
            thd_mitigated = 3.0

            mit_copper_waste_kwh = (
                kw * ((thd_mitigated / 100.0) * 0.048) * hours * 52
                if thd_mitigated > 5.0
                else 0.0
            )
            mit_insulation_penalty = 0.0
            mit_trans_waste_kwh = (
                kw * ((thd_mitigated / 100.0) ** 2 * 0.015) * hours * 52
                if thd_mitigated > 5.0
                else 0.0
            )
            mit_torque_waste_kwh = 0.0
            mit_hvac_waste_kwh = (mit_copper_waste_kwh + mit_trans_waste_kwh) * 0.35
            mit_reactive_penalty = 0.0

            row_mit_total_bleed = (
                (
                    mit_copper_waste_kwh
                    + mit_trans_waste_kwh
                    + mit_torque_waste_kwh
                    + mit_hvac_waste_kwh
                )
                * utility_rate
                + mit_insulation_penalty
                + mit_reactive_penalty
            )

            total_copper_savings_captured += (
                base_copper_waste_kwh - mit_copper_waste_kwh
            ) * utility_rate
            total_insulation_savings_captured += base_insulation_penalty
            total_transformer_savings_captured += (
                base_trans_waste_kwh - mit_trans_waste_kwh
            ) * utility_rate
            total_counter_torque_savings_captured += (
                base_torque_waste_kwh * utility_rate
            )
            total_hvac_savings_captured += (
                base_hvac_waste_kwh - mit_hvac_waste_kwh
            ) * utility_rate
            total_reactive_penalty_savings_captured += base_reactive_penalty

            mitigated_technical_bleed += row_mit_total_bleed
        else:
            mitigated_technical_bleed += row_base_total_bleed

    single_event_loss = st.session_state.prod_val * st.session_state.restart_hrs
    total_unmitigated_opportunity_cost = (
        single_event_loss * st.session_state.annual_events
    )

    has_bess_shield = (
        "★ Centralised BESS & Hybrid UPS Array (Process Ride-Through Shield)"
        in st.session_state.selected_nodes
    )
    current_opportunity_exposure = (
        0.0 if has_bess_shield else total_unmitigated_opportunity_cost
    )
    opportunity_savings_captured = (
        total_unmitigated_opportunity_cost if has_bess_shield else 0.0
    )

    operational_annual_savings = (
        total_copper_savings_captured
        + total_insulation_savings_captured
        + total_transformer_savings_captured
        + total_counter_torque_savings_captured
        + total_hvac_savings_captured
        + total_reactive_penalty_savings_captured
    )
    total_residual_leak = current_opportunity_exposure + mitigated_technical_bleed

    insurance_credit = (
        "£12,400 / yr"
        if len(st.session_state.selected_nodes) >= 2
        else "£0 (High Risk Profile)"
    )

    if total_residual_leak > 0:
        ticker_html = f"""
        <div style="background-color: #FCE8E6; padding: 12px; border-radius: 6px; border-left: 6px solid #D9272E; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="5" style="color: #A81C1C; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🚨 STEM LIVE THREAT INVENTORY // ACTIVE WORKSPACE: [{target_project_name.upper()}] // USER DELEGATE: [{active_user_handle.upper()}] // TOTAL RESIDUAL FACILITY BLEED: £{total_residual_leak:,.0f}/YR ••• [CORE INEFFICIENCIES: £{(total_copper_savings_captured + total_transformer_savings_captured + total_hvac_savings_captured):,.0f}/YR] ••• [MECHANICAL TORQUE DRAG & PENALTIES: £{(total_insulation_savings_captured + total_counter_torque_savings_captured + total_reactive_penalty_savings_captured):,.0f}/YR]
            </marquee>
        </div>
        """
    else:
        ticker_html = f"""
        <div style="background-color: #E6FFFA; padding: 12px; border-radius: 6px; border-left: 6px solid #00A389; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="4" style="color: #006654; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🟢 STEM ACTIVE BLOCKADES // WORKSPACE '{target_project_name}' SECURED BY USER '{active_user_handle.upper()}' // TOTAL RECLAIMED DEEP CASH SAVINGS: £{(operational_annual_savings + opportunity_savings_captured):,.0f}/YR ••• RISK INSULATED TO £0
            </marquee>
        </div>
        """
    st.markdown(ticker_html, unsafe_allow_html=True)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(
            label="📉 Residual Cash Bleed (Remaining Exposure)",
            value=f"£{total_residual_leak:,.0f} / yr",
            delta=(
                f"£{operational_annual_savings:,.0f}/yr Captured"
                if operational_annual_savings > 0
                else "Full Bleed Active"
            ),
            delta_color="normal" if operational_annual_savings > 0 else "inverse",
        )
    with metric_col2:
        st.metric(
            label="⏱️ Single Event Bottleneck Interruption Loss",
            value=f"£{single_event_loss:,.0f}",
        )
    with metric_col3:
        st.metric(label="🛡️ Underwriter Premium Credit", value=insurance_credit)

    st.markdown("---")

    col_workspace, col_copilot = st.columns([2, 1])

    with col_workspace:
        tab_sld_sandbox, tab_brief, tab_upload, tab_amr = st.tabs(
            [
                "🗺️ Dynamic Single Line Diagram (SLD) Digital Twin",
                "📜 Live Automated Strategic Brief",
                "🗃️ Excel Clipboard & Asset Register Ingestion",
                "⚡ AMR Half-Hourly Ingestion Engine",
            ]
        )

        with tab_sld_sandbox:
            if not st.session_state.sandbox_assets.empty:
                discovered_branches = sorted(
                    st.session_state.sandbox_assets["Plant Location"].unique().tolist()
                )
            else:
                discovered_branches = []

            available_remedial_targets = discovered_branches + [
                "★ Centralised BESS & Hybrid UPS Array (Process Ride-Through Shield)"
            ]

            st.multiselect(
                label="🏛️ Select Steering Committee Target Deployment Nodes:",
                options=available_remedial_targets,
                key="selected_nodes",
            )

            st.markdown("---")

            if st.session_state.sandbox_assets.shape[0] == 0:
                st.info(
                    "No active assets registered. Please append rows inside the staging clipboard."
                )
            else:
                dot_string = generate_dynamic_sld_graph(
                    st.session_state.sandbox_assets, st.session_state.selected_nodes
                )
                st.graphviz_chart(dot_string, use_container_width=True)

        with tab_brief:
            st.markdown(
                f"### 📋 STEM Unified Investment Brief // Workspace: {target_project_name}"
            )
            st.markdown(f"""
            #### 1. Financial Exposure & Opportunity Cost Assessment
            The active asset framework inside project workspace **{target_project_name}** currently carries an active annualised operational risk posture of **£{total_residual_leak:,.0f}/year**. Based on an active line valuation of **£{st.session_state.prod_val:,.0f}/hour** and an average process calibration restart curve of **{st.session_state.restart_hrs:.1f} hours**, a single sub-cycle voltage sag event results in an immediate opportunity cost bottleneck loss of **£{single_event_loss:,.0f}**.
            """)
            st.button("📥 Export Audit-Ready Proposal (.md)")

        with tab_upload:
            st.markdown("### 📋 Excel-Style Batch Asset Clipboard & File Ingestion")
            uploaded_register = st.file_uploader(
                "Bulk Ingest Fleet Asset Register spreadsheet or Blueprints (.csv, .pdf, .jpg, .jpeg, .png)",
                type=["csv", "pdf", "jpg", "jpeg", "png"],
                key="asset_register_sheet_uploader",
            )

            if uploaded_register is not None:
                try:
                    filename = uploaded_register.name.lower()
                    file_bytes = uploaded_register.read()

                    if filename.endswith(".csv"):
                        import io

                        df_uploaded_reg = pd.read_csv(io.BytesIO(file_bytes))
                        df_uploaded_reg.columns = [
                            str(c).strip() for c in df_uploaded_reg.columns
                        ]
                        required_cols = [
                            "Asset Tag",
                            "Plant Location",
                            "Classification",
                            "Rating (kW)",
                            "Weekly Hrs",
                            "Distortion (THD_i)",
                        ]

                        if all(c in df_uploaded_reg.columns for c in required_cols):
                            st.session_state.sandbox_assets = df_uploaded_reg[
                                required_cols
                            ]
                            st.success(
                                "🎯 Asset register spreadsheet parsed and synchronised into memory successfully!"
                            )
                    else:
                        mime_mapping = {
                            "pdf": "application/pdf",
                            "jpg": "image/jpeg",
                            "jpeg": "image/jpeg",
                            "png": "image/png",
                        }
                        active_mime = mime_mapping.get(
                            filename.split(".")[-1], "image/jpeg"
                        )

                        st.info(
                            "🧠 STEM Vision AI Module engaged. Executing programmatic drawing parsing..."
                        )
                        parser_engine = MultimodalSLDParser(
                            api_key=st.secrets["GEMINI_API_KEY"]
                        )
                        raw_extracted_json = (
                            parser_engine.extract_structured_json_from_drawing(
                                file_bytes, active_mime
                            )
                        )
                        df_extracted_twin = (
                            parser_engine.convert_extracted_payload_to_registry(
                                raw_extracted_json
                            )
                        )

                        if not df_extracted_twin.empty:
                            st.session_state.sandbox_assets = df_extracted_twin
                            st.success(
                                f"⚡ Vision Audit Complete! Reverse-engineered {len(df_extracted_twin)} equipment nodes straight from blueprint schematics."
                            )

                except Exception as e:
                    st.error(f"❌ Ingestion Crash: Details: `{str(e)}`")

            st.markdown("---")
            st.markdown(
                f"#### 💾 Project Workspace Persistence Manager // Active Profile: `{target_project_name}`"
            )
            p_col1, p_col2 = st.columns([3, 1])
            with p_col1:
                st.caption(
                    f"Commit the current transient memory grid configuration down to the secure Neon SQL database under your user account "
                    f"profile. This project configuration state remains partitioned cleanly under UUID namespace structures."
                )
            with p_col2:
                if st.button("💾 Save Project State", use_container_width=True):
                    save_report = repo_engine.save_site_inventory_state(
                        active_site_uid_str,
                        target_project_name,
                        st.session_state.sandbox_assets,
                    )
                    if save_report["status"] == "SUCCESS":
                        st.toast(save_report["message"], icon="✅")
                    else:
                        st.error(save_report["message"])

            st.markdown("---")
            edited_df = st.data_editor(
                data=st.session_state.sandbox_assets,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=True,
                column_config={
                    "Asset Tag": st.column_config.TextColumn(
                        "Asset Tag", required=True
                    ),
                    "Plant Location": st.column_config.TextColumn(
                        "Plant Location", required=True
                    ),
                    "Classification": st.column_config.SelectboxColumn(
                        "Classification",
                        options=[
                            "Main Distribution Transformer",
                            "Auxiliary Step-Down Transformer",
                            "Variable Speed Drive (VSD)",
                            "Large Induction Motor",
                            "Arc Furnace Plant",
                            "Ladle Metallurgy Furnace",
                            "Power Factor Correction Bank",
                            "Industrial LED Lighting Network",
                            "General Load",
                        ],
                        required=True,
                    ),
                    "Rating (kW)": st.column_config.NumberColumn(
                        "Rating (kW)",
                        min_value=1,
                        max_value=10000,
                        step=5,
                        required=True,
                    ),
                    "Weekly Hrs": st.column_config.NumberColumn(
                        "Weekly Hrs", min_value=1, max_value=168, step=1, required=True
                    ),
                    "Distortion (THD_i)": st.column_config.NumberColumn(
                        "Distortion (THD_i)",
                        min_value=0.0,
                        max_value=100.0,
                        step=0.1,
                        format="%.1f%%",
                        required=True,
                    ),
                },
            )
            st.session_state.sandbox_assets = edited_df

        with tab_amr:
            st.markdown("### ⚡ Half-Hourly AMR Utility Log Ingestion Engine")
            uploaded_amr = st.file_uploader(
                "Ingest Smart Meter Profile Logs (.csv)",
                type=["csv"],
                key="active_amr_uploader",
            )

            if uploaded_amr is not None:
                try:
                    df_uploaded = pd.read_csv(uploaded_amr)
                    df_uploaded.columns = [
                        str(c).strip().lower() for c in df_uploaded.columns
                    ]
                    reconciler = AMRDataReconciler(tenant_id="swalek")
                    processed_intervals = [
                        reconciler.parse_half_hourly_reading(
                            {
                                "timestamp": str(r["timestamp"]),
                                "active_kwh": float(r["active_kwh"]),
                                "reactive_kvarh": float(r["reactive_kvarh"]),
                            }
                        )
                        for _, r in df_uploaded.iterrows()
                    ]
                    df_processed = pd.DataFrame(processed_intervals).set_index(
                        "timestamp"
                    )
                    st.success(f"📊 Reconciled {len(df_processed)} records.")
                    st.line_chart(df_processed[["demand_kw", "apparent_kva"]])
                except Exception as err:
                    st.error(f"❌ Execution Fault: `{str(err)}`")

    with col_copilot:
        st.markdown("### 🧠 STEM AI Co-Pilot Console")
        chat_container = st.container(height=450)
        with chat_container:
            active_chat_stream = st.session_state.get("copilot_history", [])
            for message in active_chat_stream:
                with st.chat_message(message["role"]):
                    st.markdown(message["text"])

        if user_prompt := st.chat_input(
            "Ask about capital costs, metrics, calculations..."
        ):
            st.session_state.copilot_history.append(
                {"role": "user", "text": user_prompt}
            )
            with chat_container:
                st.chat_message("user").markdown(user_prompt)

            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                if not st.session_state.sandbox_assets.empty:
                    df_m = st.session_state.sandbox_assets
                    markdown_lines = [
                        "| " + " | ".join(df_m.columns) + " |",
                        "| " + " | ".join(["---"] * len(df_m.columns)) + " |",
                    ]
                    for _, row in df_m.iterrows():
                        markdown_lines.append(
                            "| " + " | ".join(str(row[h]) for h in df_m.columns) + " |"
                        )
                    serialized_sld_matrix = "\n".join(markdown_lines)
                else:
                    serialized_sld_matrix = "No nodes."

                system_context = f"""
                You are the master STEM Power Quality AI Agent. Active project workspace name context: '{target_project_name}' assigned to user handle: '{active_user_handle}'.
                - Deployed Active Shunt Nodes: {st.session_state.selected_nodes}
                - Total Active Workspace Risk Leak: £{total_residual_leak:,.0f} / yr
                
                🏆 CRITICAL LIVE SLD NETWORK ASSET INVENTORY:
                {serialized_sld_matrix}
                """

                engineering_instruction_layer = """
                You are a senior power systems auditing engineer and cost consultant. Speak with professional authority. Use proper UK English spelling standards exclusively.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[system_context, user_prompt],
                    config=types.GenerateContentConfig(
                        tools=[update_electrical_mitigation_nodes],
                        temperature=0.15,
                        system_instruction=engineering_instruction_layer,
                    ),
                )

                if response.function_calls:
                    for call in response.function_calls:
                        if call.name == "update_electrical_mitigation_nodes":
                            tool_args = call.args
                            execution_result = update_electrical_mitigation_nodes(
                                **tool_args
                            )
                            st.session_state.copilot_history.append(
                                {
                                    "role": "assistant",
                                    "text": f"🤖 **AI Action Executed:**\n``{execution_result}``",
                                }
                            )
                else:
                    reply = (
                        response.text
                        if response.text
                        else "Telemetry context synchronised."
                    )
                    st.session_state.copilot_history.append(
                        {"role": "assistant", "text": reply}
                    )

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    st.session_state.copilot_history.append(
                        {
                            "role": "assistant",
                            "text": "⚠️ **Gemini API Free Tier Quota Exhausted (Error 429):**\n\nThe local session has exceeded the standard free request volume allowed for the `gemini-2.5-flash` endpoint. Please retry in 16 seconds.",
                        }
                    )
                else:
                    st.session_state.copilot_history.append(
                        {
                            "role": "assistant",
                            "text": f"❌ **Co-Pilot Error:** `{str(e)}`",
                        }
                    )

            st.sidebar.caption("State updated.")
            st.rerun()
