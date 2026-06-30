import os
import sys
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

    if "Primary Intake Switchboard (Centralised Bay)" in selected_mitigations:
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

        if thd > 15.0:
            node_style = f'label="⚠️ {tag}\\n{classification}\\n{rating:,.0f} kW | THD: {thd:.1f}%", fillcolor="#FCE8E6", color="#D9272E", penwidth=1.8'
        elif "Transformer" in classification:
            node_style = f'label="🔌 {tag}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#FFF3CD", color="#FFC107"'
        else:
            node_style = f'label="⚙️ {tag}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#F8F9FA", color="#6C757D"'

        asset_tuple = (clean_id, node_style)
        if (
            "Furnace" in classification
            or "Large Induction" in classification
            or rating >= 1000
        ):
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

    dot_nodes.append("  subgraph cluster_heavy {")
    dot_nodes.append('    label="⚡ Heavy Industrial Process Board";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#FFFDF6"; color="#D1A113"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_HEAVY [label="⚡ Furnace Sub-Distribution\\nBusbar Node B1", fillcolor="#FFF3CD", style="filled,bold"];'
    )

    if "Heavy Industrial Process Board (Panel B1)" in selected_mitigations:
        dot_nodes.append(
            '    SUB_STEM_HEAVY [label="🛡️ LOCAL STEM FILTER B1\\nActive Furnace Compensation", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    SUB_STEM_HEAVY -> BUS_HEAVY [color="#28A745", penwidth=2.0, arrowhead=normal, label=" Active Injection", weight=0];'
        )

    last_id = "BUS_HEAVY"
    for cid, style in heavy_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_HEAVY -> {cid} [weight=10];")
        if last_id != "BUS_HEAVY":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    dot_nodes.append("  subgraph cluster_drives {")
    dot_nodes.append('    label="⚙️ Motor Control Centre (MCC)";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#F4F9FF"; color="#2B72C4"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_DRIVES [label="⚙️ Automated Drive Panel\\nBusbar Node B2", fillcolor="#E2F0FE", style="filled,bold"];'
    )

    if "Motor Control Centre (MCC Panel B2)" in selected_mitigations:
        dot_nodes.append(
            '    SUB_STEM_DRIVES [label="🛡️ LOCAL STEM FILTER B2\\nActive VSD Drive Cancellation", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    SUB_STEM_DRIVES -> BUS_DRIVES [color="#28A745", penwidth=2.0, arrowhead=normal, label=" Active Injection", weight=0];'
        )

    if (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in selected_mitigations
    ):
        dot_nodes.append(
            '    SUB_STEM_BESS [label="🔋 LOCAL BESS & HYBRID UPS\\nAsset Protection & 20ms Sag Backup", fillcolor="#E6FFFA", color="#00A389", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    SUB_STEM_BESS -> BUS_DRIVES [color="#00A389", penwidth=2.0, arrowhead=normal, label=" Dual-Duty Shunt/UPS", weight=0];'
        )

    last_id = "BUS_DRIVES"
    for cid, style in drive_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_DRIVES -> {cid} [weight=10];")
        if last_id != "BUS_DRIVES":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    dot_nodes.append("  subgraph cluster_aux {")
    dot_nodes.append('    label="🏢 Auxiliary & Building Services";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#F8F9FA"; color="#6C757D"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_AUX [label="🏢 Commercial Infrastructure\\nBusbar Node B3", fillcolor="#E9ECEF", style="filled,bold"];'
    )

    if "Auxiliary & Building Services (Panel B3)" in selected_mitigations:
        dot_nodes.append(
            '    SUB_STEM_AUX [label="🛡️ LOCAL STEM FILTER B3\\nAuxiliary Clean Power Bank", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    SUB_STEM_AUX -> BUS_AUX [color="#28A745", penwidth=2.0, arrowhead=normal, label=" Active Injection", weight=0];'
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
    if "sandbox_assets" not in st.session_state:
        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    if "selected_nodes" not in st.session_state:
        st.session_state.selected_nodes = ["Motor Control Centre (MCC Panel B2)"]

    if "prod_val" not in st.session_state:
        st.session_state.prod_val = 150000

    if "restart_hrs" not in st.session_state:
        st.session_state.restart_hrs = 4.0

    if "annual_events" not in st.session_state:
        st.session_state.annual_events = 3

    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = [
            {
                "role": "assistant",
                "text": "👋 Welcome to the upgraded STEM Executive Portal. I am synced with your plant parameters, macro opportunity-cost models, and insurance premium risk curves. Let's optimise the network's financial engineering.",
            }
        ]

    with st.sidebar.expander("💼 Macro Facility Variables", expanded=True):
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

    single_event_loss = st.session_state.prod_val * st.session_state.restart_hrs
    total_unmitigated_opportunity_cost = (
        single_event_loss * st.session_state.annual_events
    )

    has_mcc_filter = (
        "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes
    )
    has_bess_ups = (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    )

    insulation_depreciation_exposure = 23800.0 if not has_mcc_filter else 0.0
    copper_loss_energy_exposure = 26400.0 if not has_mcc_filter else 0.0
    active_technical_bleed = (
        insulation_depreciation_exposure + copper_loss_energy_exposure
    )

    insulation_savings_captured = 23800.0 if has_mcc_filter else 0.0
    copper_savings_captured = 26400.0 if has_mcc_filter else 0.0
    opportunity_savings_captured = (
        total_unmitigated_opportunity_cost if has_bess_ups else 0.0
    )
    operational_annual_savings = insulation_savings_captured + copper_savings_captured

    current_opportunity_exposure = (
        0.0 if has_bess_ups else total_unmitigated_opportunity_cost
    )
    total_residual_leak = current_opportunity_exposure + active_technical_bleed

    insurance_credit = (
        "£12,400 / yr"
        if len(st.session_state.selected_nodes) >= 2
        else "£0 (High Risk Profile)"
    )

    if total_residual_leak > 0:
        ticker_html = f"""
        <div style="background-color: #FCE8E6; padding: 12px; border-radius: 6px; border-left: 6px solid #D9272E; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="5" style="color: #A81C1C; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🚨 STEM LIVE THREAT INVENTORY // TOTAL RESIDUAL FACILITY BLEED: £{total_residual_leak:,.0f}/YR ••• DETAILED UNMITIGATED LEAKS ➔ [DOWNTIME OPPORTUNITY RISK: £{current_opportunity_exposure:,.0f}/YR] ••• [EXCESS INSULATION WEAR PENALTY: £{insulation_depreciation_exposure:,.0f}/YR] ••• [WASTED COPPER LOSS ENERGY: £{copper_loss_energy_exposure:,.0f}/YR]
            </marquee>
        </div>
        """
    else:
        ticker_html = f"""
        <div style="background-color: #E6FFFA; padding: 12px; border-radius: 6px; border-left: 6px solid #00A389; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="4" style="color: #006654; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🟢 STEM ACTIVE BLOCKADES // TOTAL RECLAIMED CASH SAVINGS: £{(operational_annual_savings + opportunity_savings_captured):,.0f}/YR ••• [ENERGY BILL REDUCTIONS: £{copper_savings_captured:,.0f}/YR] ••• [DEPRECIATION RECOVERY: £{insulation_savings_captured:,.0f}/YR] ••• RISK INSULATED TO £0
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
            help="Calculated live as Hourly Production Value x Process Reset Loop Duration.",
        )
    with metric_col3:
        st.metric(
            label="🛡️ Underwriter Premium Credit",
            value=insurance_credit,
            delta=(
                "Premium Credit Approved"
                if len(st.session_state.selected_nodes) >= 2
                else "G5/5 Penalty Risk Flag"
            ),
        )

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
            st.multiselect(
                label="🏛️ Select Steering Committee Target Deployment Nodes:",
                options=[
                    "Primary Intake Switchboard (Centralised Bay)",
                    "Heavy Industrial Process Board (Panel B1)",
                    "Motor Control Centre (MCC Panel B2)",
                    "Auxiliary & Building Services (Panel B3)",
                    "Local BESS & Hybrid UPS Array (Robotics Asset Protection)",
                ],
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
            st.markdown("### 📋 STEM Unified Investment & Risk Mitigation Brief")
            st.caption(
                "This brief updates natively as you adjust valuation variables on your sidebar or check switchgear nodes."
            )
            st.markdown("---")

            st.markdown(f"""
            #### 1. Financial Exposure & Opportunity Cost Assessment
            Ammanford Alloys currently carries an active annualised operational risk posture of **£{total_residual_leak:,.0f}/year** consisting of parallel downtime vulnerabilities, unmitigated energy friction, and accelerated hardware degradation. Based on an active line valuation of **£{st.session_state.prod_val:,.0f}/hour** and an average process calibration restart curve of **{st.session_state.restart_hrs:.1f} hours**, a single sub-cycle voltage sag event results in an immediate opportunity cost bottleneck loss of **£{single_event_loss:,.0f}**.
            
            #### 2. Technical Single Line Architecture Interventions
            To insulate the factory floor from macro grid volatility, the steering committee outlines the following physical network infrastructure modification:
            """)

            if st.session_state.selected_nodes:
                for node in st.session_state.selected_nodes:
                    st.markdown(f"* 🟢 Deployed Parallel Asset: **{node}**")
            else:
                st.markdown(
                    "* ⚠️ **CRITICAL WARNING:** No mitigation assets active. The plant is fully exposed to incoming harmonic degradation and line trips."
                )

            st.markdown(f"""
            #### 3. Actuarial Risk Profile & Underwriting Adjustments
            By demonstrating compliance with EREC G5/5 and implementing sub-20ms ride-through asset protection on sensitive electronics, the plant's structural risk posture decreases. 
            * **Current Underwriter Credit Yield:** **{insurance_credit}**
            * **Macro Benchmark Perspective:** This protective model successfully implements the systems-thinking framework validated by regional high-value facilities like the Aston Martin super-hangar in St Athan, converting volatile power quality anomalies into a predictable asset lifecycle.
            """)
            st.button("📥 Export Audit-Ready Proposal (.md)")

        with tab_upload:
            st.markdown("### 📋 Excel-Style Batch Asset Clipboard & File Ingestion")
            st.markdown(
                "You can manually adjust machine specs inside the live grid editor below, copy-paste cell blocks "
                "directly from Microsoft Excel, or directly drop a structured Asset Register CSV table or an official "
                "**PDF/JPEG Single Line Diagram (SLD) Schematic drawing**."
            )

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
                            st.error(
                                f"❌ Ingestion Aborted: Missing column components. Expected explicit schema keys: {required_cols}"
                            )
                    else:
                        mime_mapping = {
                            "pdf": "application/pdf",
                            "jpg": "image/jpeg",
                            "jpeg": "image/jpeg",
                            "png": "image/png",
                        }
                        ext = filename.split(".")[-1]
                        active_mime = mime_mapping.get(ext, "image/jpeg")

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
                        else:
                            st.error(
                                "⚠️ Ingestion Warning: Blueprint analysed successfully but no distinct load groups were identified."
                            )

                except Exception as e:
                    st.error(
                        f"❌ Ingestion Crash: Error processing asset file stream array. Details: `{str(e)}`"
                    )

            st.markdown("---")
            st.markdown("#### 💾 Project State Management")
            p_col1, p_col2 = st.columns([3, 1])
            with p_col1:
                st.caption(
                    "Commit the current transient memory grid configuration down to the secure Neon SQL database "
                    "to prevent loss of project updates on session resets."
                )
            with p_col2:
                if st.button("💾 Save Project State", use_container_width=True):
                    target_site_uid = "00000000-0000-0000-0000-000000000002"
                    repo_writer = ProjectPersistenceRepository(db_engine=engine)
                    save_report = repo_writer.save_site_inventory_state(
                        target_site_uid, st.session_state.sandbox_assets
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
            st.markdown(
                "Upload an interval log file stream to cross-reference your surveyor checklist totals "
                "against actual peak utility demands."
            )

            with st.expander("📝 View Required CSV Header Schema Spec", expanded=False):
                st.markdown("""
                The ingestion data pipeline expects a CSV file containing three continuous headers:
                * **`timestamp`**: Scheduled date-time strings (`YYYY-MM-DD HH:MM:SS`)
                * **`active_kwh`**: Total active energy registered in the 30-min settlement block
                * **`reactive_kvarh`**: Total reactive energy registered in the 30-min settlement block
                """)
                dummy_df = pd.DataFrame(
                    {
                        "timestamp": [
                            "2026-06-22 06:00:00",
                            "2026-06-22 06:30:00",
                            "2026-06-22 07:00:00",
                        ],
                        "active_kwh": [40.0, 42.0, 95.0],
                        "reactive_kvarh": [20.0, 21.0, 45.0],
                    }
                )
                st.dataframe(dummy_df, hide_index=True)

            uploaded_amr = st.file_uploader(
                "Ingest Smart Meter Profile Logs (.csv)",
                type=["csv"],
                key="active_amr_uploader",
            )

            ratings_clean = (
                st.session_state.sandbox_assets["Rating (kW)"]
                .astype(str)
                .str.replace(",", "")
                .astype(float)
            )
            total_survey_kw = float(ratings_clean.sum())

            if uploaded_amr is not None:
                try:
                    df_uploaded = pd.read_csv(uploaded_amr)
                    df_uploaded.columns = [
                        str(c).strip().lower() for c in df_uploaded.columns
                    ]

                    target_columns = {"timestamp", "active_kwh", "reactive_kvarh"}
                    if not target_columns.issubset(df_uploaded.columns):
                        st.error(
                            f"❌ Ingestion Blocked: Uploaded file is missing required components. Target: {list(target_columns)}"
                        )
                    else:
                        current_tenant = st.session_state.get("role", "swalek")
                        reconciler = AMRDataReconciler(tenant_id=current_tenant)

                        processed_intervals = []
                        for _, row in df_uploaded.iterrows():
                            read_node = {
                                "timestamp": str(row["timestamp"]),
                                "active_kwh": float(row["active_kwh"]),
                                "reactive_kvarh": float(row["reactive_kvarh"]),
                            }
                            processed_intervals.append(
                                reconciler.parse_half_hourly_reading(read_node)
                            )

                        df_processed = pd.DataFrame(processed_intervals)
                        df_processed.set_index("timestamp", inplace=True)

                        st.success(
                            f"📊 Pipeline Engaged: Successfully reconciled {len(df_processed)} half-hourly records."
                        )
                        st.line_chart(df_processed[["demand_kw", "apparent_kva"]])

                        st.markdown("#### 🔍 Transient Inrush Anomaly Diagnostics")
                        jumps = reconciler.detect_sudden_consumption_jumps(
                            processed_intervals, jump_threshold_kw=50.0
                        )
                        if jumps:
                            for jump in jumps:
                                st.warning(
                                    f"⚠️ **Heavy Start Event Caught:** Sharp step-change registered at `{jump['timestamp']}`! "
                                    f"Magnitude: `+{jump['magnitude_step_kw']} kW` (Profile transitioned from `{jump['pre_jump_kw']} kW` up to `{jump['post_jump_kw']} kW`)."
                                )
                        else:
                            st.info(
                                "🟢 Zero sudden load jumps caught across the current utility billing horizon."
                            )

                        st.markdown("#### 📑 Auditor Capacity Allocation Report")
                        recon_summary = reconciler.reconcile_desktop_survey(
                            total_survey_kw, processed_intervals
                        )

                        r_col1, r_col2, r_col3 = st.columns(3)
                        with r_col1:
                            st.metric(
                                "Empirical Peak Grid Demand",
                                f"{recon_summary['measured_peak_demand_kw']:,} kW",
                            )
                        with r_col2:
                            st.metric(
                                "Surveyor Estimated Checklist",
                                f"{recon_summary['surveyor_estimated_load_kw']:,} kW",
                            )
                        with r_col3:
                            st.metric(
                                "Relational Capacity Variance",
                                f"{recon_summary['variance_gap_kw']:,} kW",
                                delta=f"{recon_summary['variance_divergence_pct']}% Divergence",
                                delta_color=(
                                    "inverse"
                                    if recon_summary["variance_divergence_pct"] > 25.0
                                    else "normal"
                                ),
                            )

                        if (
                            recon_summary["action_required"]
                            == "RE_CALIBRATE_DUTY_CYCLES"
                        ):
                            st.error(
                                f"🚨 **Auditor Action Required:** Static survey inventory calculations overshoot actual maximum observed "
                                f"demands by **{recon_summary['variance_divergence_pct']}%**. The asset register contains exaggerated duty cycles "
                                f"or missing diversity factors. Re-calibrate names and schedules before submitting CapEx requests."
                            )
                        else:
                            st.success(
                                "🎯 **Checklist Integrity Approved:** Surveyor checklist load matrices align perfectly within the "
                                "acceptable engineering diversity limits of actual site operations."
                            )
                except Exception as err:
                    st.error(
                        f"❌ Execution Fault: Failed to process interval stream array. Details: `{str(err)}`"
                    )
            else:
                st.info(
                    "💡 Sandbox Staging View: No file uploaded yet. Parsing validation profile records below:"
                )

                reconciler = AMRDataReconciler(tenant_id="swalek")
                simulated_meter_logs = [
                    {
                        "timestamp": "2026-06-22 06:00:00",
                        "active_kwh": 40.0,
                        "reactive_kvarh": 20.0,
                    },
                    {
                        "timestamp": "2026-06-22 06:30:00",
                        "active_kwh": 42.0,
                        "reactive_kvarh": 21.0,
                    },
                    {
                        "timestamp": "2026-06-22 07:00:00",
                        "active_kwh": 95.0,
                        "reactive_kvarh": 45.0,
                    },
                    {
                        "timestamp": "2026-06-22 07:30:00",
                        "active_kwh": 93.0,
                        "reactive_kvarh": 44.0,
                    },
                ]
                processed_stream = [
                    reconciler.parse_half_hourly_reading(log)
                    for log in simulated_meter_logs
                ]
                df_sim = pd.DataFrame(processed_stream).set_index("timestamp")

                st.line_chart(df_sim[["demand_kw", "apparent_kva"]])

                jumps = reconciler.detect_sudden_consumption_jumps(
                    processed_stream, jump_threshold_kw=50.0
                )
                for jump in jumps:
                    st.warning(
                        f"⚠️ **Heavy Start Event Caught:** Registered load jump at `{jump['timestamp']}`! Step: `+{jump['magnitude_step_kw']} kW`."
                    )

                recon_summary = reconciler.reconcile_desktop_survey(
                    total_survey_kw, processed_stream
                )
                st.write(
                    f"**Verification Report Index:** `{recon_summary['action_required']}` | Measured Divergence: `{recon_summary['variance_divergence_pct']}%`."
                )

    with col_copilot:
        st.markdown("### 🧠 STEM AI Co-Pilot Console")
        st.caption("Two-Way Conversational Topology Optimisation Gateway")
        st.markdown("---")

        chat_container = st.container(height=450)
        with chat_container:
            for message in st.session_state.copilot_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["text"])

        st.markdown("##### 📎 Attach Drawing to Active Conversation")
        chat_attachment = st.file_uploader(
            "Upload schematic blueprint for real-time Co-Pilot inspection:",
            type=["pdf", "jpg", "jpeg", "png"],
            key="copilot_direct_drawing_uploader",
            label_visibility="collapsed",
        )

        if user_prompt := st.chat_input(
            "Ask about capital costs, opportunity costs, drawing metrics..."
        ):
            st.session_state.copilot_history.append(
                {"role": "user", "text": user_prompt}
            )
            with chat_container:
                st.chat_message("user").markdown(user_prompt)

            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                # 🛠️ FIXED: Manual string building pattern to completely bypass third-party library dependencies like 'tabulate'
                if not st.session_state.sandbox_assets.empty:
                    df_inv = st.session_state.sandbox_assets
                    headers = list(df_inv.columns)
                    markdown_lines = [
                        "| " + " | ".join(headers) + " |",
                        "| " + " | ".join(["---"] * len(headers)) + " |",
                    ]
                    for _, row in df_inv.iterrows():
                        markdown_lines.append(
                            "| " + " | ".join(str(row[h]) for h in headers) + " |"
                        )
                    serialized_sld_matrix = "\n".join(markdown_lines)

                    thd_clean_series = (
                        st.session_state.sandbox_assets["Distortion (THD_i)"]
                        .astype(str)
                        .str.replace("%", "")
                        .astype(float)
                    )
                    peak_row = st.session_state.sandbox_assets.iloc[
                        thd_clean_series.idxmax()
                    ]
                    peak_anomaly_context = f"{peak_row['Asset Tag']} ({peak_row['Classification']}) exhibiting {peak_row['Distortion (THD_i)']}% THD_i"
                else:
                    serialized_sld_matrix = "No equipment nodes currently registered."
                    peak_anomaly_context = "None"

                system_context = f"""
                You are the master STEM Power Quality AI Agent. You blend technical electrical physics with corporate financial risk modelling.
                
                LIVE FACILITY DATA OVERVIEW:
                - Deployed Active Shunt Nodes: {st.session_state.selected_nodes}
                - Hourly Plant Production Value: £{st.session_state.prod_val:,.0f} / hr
                - Process Reset Loop Downtime: {st.session_state.restart_hrs} hours
                - Single Interruption Interruption Cost: £{single_event_loss:,.0f}
                - Annualised Risk Exposure: £{total_residual_leak:,.0f} / yr
                - Expected Annual Insurance Premium Reduction: {insurance_credit}
                
                🏆 CRITICAL LIVE SLD NETWORK ASSET INVENTORY:
                {serialized_sld_matrix}
                
                ⚠️ DETECTED NETWORK ANOMALY TARGET:
                The peak wave-shape distortion emitter currently active on the busbar network is: {peak_anomaly_context}.
                
                💰 BUDGETARY CAPITAL COST ESTIMATION HEURISTICS:
                1. Primary Intake Switchboard (Centralised Bay): £85,000
                2. Heavy Industrial Process Board (Panel B1): £42,000
                3. Motor Control Centre (MCC Panel B2): £35,000
                4. Auxiliary & Building Services (Panel B3): £18,000
                5. Local BESS & Hybrid UPS Array (Robotics Asset Protection): £65,000. Provides the sub-20ms ride-through to insulate sensitive equipment from sags, bringing Opportunity Cost exposure to £0.
                """

                contents_payload = [system_context]

                if chat_attachment is not None:
                    att_filename = chat_attachment.name.lower()
                    att_bytes = chat_attachment.read()
                    mime_map = {
                        "pdf": "application/pdf",
                        "jpg": "image/jpeg",
                        "jpeg": "image/jpeg",
                        "png": "image/png",
                    }
                    att_mime = mime_map.get(att_filename.split(".")[-1], "image/jpeg")

                    contents_payload.append(
                        types.Part.from_bytes(data=att_bytes, mime_type=att_mime)
                    )
                    contents_payload.append(
                        "Analyse this attached drawing file directly as part of the conversation context. "
                        "Cross-reference its contents with the user's natural prompt query below."
                    )

                contents_payload.append(user_prompt)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_payload,
                    config=types.GenerateContentConfig(
                        tools=[update_electrical_mitigation_nodes],
                        temperature=0.15,
                        system_instruction="You are a brilliant cost consultant and systems-thinking power engineer. Speak with professional, boardroom-ready authority. Address specific asset tags dynamically. Never give canned robotic disclaimers.",
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
                                    "text": f"🤖 **AI Optimisation Action Executed:**\n`{execution_result}`\n\nI have rewritten the network topology tree and updated the active business risk metrics on your executive ribbon.",
                                }
                            )
                else:
                    reply = (
                        response.text
                        if response.text
                        else "Telemetry data parsed. System state stabilised."
                    )
                    st.session_state.copilot_history.append(
                        {"role": "assistant", "text": reply}
                    )

            except Exception as e:
                st.session_state.copilot_history.append(
                    {
                        "role": "assistant",
                        "text": f"❌ **Co-Pilot Communication Error:** Details: `{str(e)}`",
                    }
                )

            st.rerun()
