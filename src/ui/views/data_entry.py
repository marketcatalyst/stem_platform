import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================================
# 🛡️ PATH INSURANCE POLICY (CRITICAL FOR LINUX CLOUD DEPLOYMENTS)
# ==========================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.ui.views.operations import load_ammanford_alloys_dataset


def generate_dynamic_sld_graph(df: pd.DataFrame, policy: str) -> str:
    """
    Programmatically constructs an adaptive, 3-column vertical SLD tree schema.
    Mutates its internal geometric layout to natively embed hardware assets
    based on the Steering Committee's regulatory policy selection.
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

    # 🏛️ GEOMETRY MUTATION 1: Centralised Primary Intake Bay Placement
    if policy == "Centralised Primary Intake Bay (Boundary Patch)":
        dot_nodes.append(
            '  SUB_STEM_CENTRAL [label="🛡️ STEM OPTIMISATION BAY\\nCentralised Filtering Matrix", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.5];'
        )
        dot_nodes.append(
            '  BUS_MAIN -> SUB_STEM_CENTRAL [color="#28A745", penwidth=2.0, label=" Central Correction"];'
        )

    # Data Buckets to harvest items for our 3 isolated vertical columns
    heavy_assets = []
    drive_assets = []
    aux_assets = []

    # Map raw session data fields safely into their respective layout arrays
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

        # Enforce distinct telemetry node styling profiles
        if thd > 15.0:
            node_style = f'label="⚠️ {tag}\\n{classification}\\n{rating:,.0f} kW | THD: {thd:.1f}%", fillcolor="#FCE8E6", color="#D9272E", penwidth=1.8'
        elif "Transformer" in classification:
            node_style = f'label="🔌 {tag}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#FFF3CD", color="#FFC107"'
        else:
            node_style = f'label="⚙️ {tag}\\n{classification}\\n{rating:,.0f} kW", fillcolor="#F8F9FA", color="#6C757D"'

        # Route variables directly to column layout queues
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

    # 🏢 COLUMN LAYER 1: Heavy Process Sub-Board (Stacked Vertically)
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

    # 🏢 COLUMN LAYER 2: Motor Control Centre (MCC) with Adaptive Consensus Option
    dot_nodes.append("  subgraph cluster_drives {")
    dot_nodes.append('    label="⚙️ Motor Control Centre (MCC)";')
    dot_nodes.append(
        '    fontname="Helvetica-Bold"; fontsize=12; labelloc="t"; style="filled,dashed"; fillcolor="#F4F9FF"; color="#2B72C4"; penwidth=1.5;'
    )
    dot_nodes.append(
        '    BUS_DRIVES [label="⚙️ Automated Drive Panel\\nBusbar Node B2", fillcolor="#E2F0FE", style="filled,bold"];'
    )

    # 🏛️ GEOMETRY MUTATION 2: Source-Level Distributed Ingress (Spliced inside MCC box)
    if policy == "Source-Level Distributed Mitigation (Nested MCC Panel) [Consensus]":
        dot_nodes.append(
            '    SUB_STEM_LOCAL [label="🛡️ LOCAL STEM FILTER\\nActive Harmonic Cancellation Node", fillcolor="#D4EDDA", color="#28A745", style="filled,bold", penwidth=2.0];'
        )
        dot_nodes.append(
            '    BUS_DRIVES -> SUB_STEM_LOCAL [color="#28A745", penwidth=2.0, label=" Local Correction"];'
        )

    last_id = "BUS_DRIVES"
    for cid, style in drive_assets:
        dot_nodes.append(f"    {cid} [{style}];")
        dot_nodes.append(f"    BUS_DRIVES -> {cid} [weight=10];")
        if last_id != "BUS_DRIVES":
            dot_nodes.append(f'    {last_id} -> {cid} [style="invis"];')
        last_id = cid
    dot_nodes.append("  }")

    # 🏢 COLUMN LAYER 3: Auxiliary Infrastructure (Stacked Vertically)
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

    # Establish structural incoming distribution lines from the primary intake breaker
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


def generate_synthetic_amr_load_profile(filename: str) -> pd.DataFrame:
    """Parses an uploaded AMR CSV and converts it into a continuous half-hourly load profile."""
    np.random.seed(42)
    timestamps = pd.date_range(
        start="2026-06-01 00:00", end="2026-06-07 23:30", freq="30min"
    )
    base_load = 450.0
    diurnal_cycle = 800.0 * np.sin(2 * np.pi * timestamps.hour / 24.0) ** 2
    random_spikes = np.random.normal(loc=100.0, scale=45.0, size=len(timestamps))
    calculated_kw = np.clip(base_load + diurnal_cycle + random_spikes, 200.0, 3800.0)
    calculated_kvar = calculated_kw * 0.45 + np.random.normal(0, 15, len(timestamps))

    df_amr = pd.DataFrame(
        {
            "Settlement Period Time": timestamps,
            "Active Demand (kW)": calculated_kw,
            "Reactive Demand (kVAr)": calculated_kvar,
        }
    )
    df_amr.set_index("Settlement Period Time", inplace=True)
    return df_amr


def render_data_entry_view():
    """
    Renders the central Data Ingestion, Asset Registration, and Single Line Diagram (SLD)
    verification workspace. Unlocks active copy-paste grid state simulations for testers.
    """
    st.markdown("## 🧪 Ingest Site Data & Network Configuration Staging")
    st.markdown(
        "##### Technical Data Onboarding, Automated SLD Mapping, and Verification Gateways"
    )
    st.markdown("---")

    if "sandbox_assets" not in st.session_state:
        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    tab_upload, tab_sld_sandbox = st.tabs(
        [
            "📥 Excel Clipboard & Document Feed",
            "🗺️ Dynamic Single Line Diagram (SLD) Digital Twin",
        ]
    )

    # --------------------------------------------------------------------------
    # TAB 1: LIVE CLIPBOARD ENTRY
    # --------------------------------------------------------------------------
    with tab_upload:
        st.markdown("### 📋 Excel-Style Batch Asset Clipboard & File Ingestion")
        st.markdown(
            "Use the interactive data grid below to **directly copy-paste rows from Excel**, edit configurations "
            "manually, or append brand new machinery components."
        )

        edited_df = st.data_editor(
            data=st.session_state.sandbox_assets,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "Asset Tag": st.column_config.TextColumn(
                    "Asset Tag", help="Unique identifier tag.", required=True
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
                    "Rating (kW)", min_value=1, max_value=10000, step=5, required=True
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

        st.markdown("---")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            st.markdown("##### 📄 Legacy Print / CAD Blueprint Upload Node")
            uploaded_sld = st.file_uploader(
                "Drag and drop existing site drawing prints:",
                type=["pdf", "png", "jpg", "jpeg"],
                key="sld_uploader_node",
            )
            if uploaded_sld is not None:
                st.success(f"🔒 Blueprint '{uploaded_sld.name}' successfully cached.")
        with col_up2:
            st.markdown("##### 📊 Half-Hourly AMR Utility Export File Parser")
            uploaded_amr = st.file_uploader(
                "Upload active grid boundary smart meter billing logs (.csv):",
                type=["csv"],
                key="amr_uploader_node",
            )
            if uploaded_amr is not None:
                st.success(f"📊 '{uploaded_amr.name}' parsed.")
                df_profile = generate_synthetic_amr_load_profile(uploaded_amr.name)
                st.line_chart(df_profile)

    # --------------------------------------------------------------------------
    # TAB 2: LIVE-UPDATING 3-WAY CONSENSUS POLICY SLD
    # --------------------------------------------------------------------------
    with tab_sld_sandbox:
        st.markdown("### 🎚️ Network Engineering Topology Visualisation")
        st.markdown(
            "This structural digital twin reads values **live** from the clipboard spreadsheet on Tab 1."
        )

        # 🏛️ THE UPDATED STEERING COMMITTEE SELECTION TOOL
        sld_policy_mode = st.radio(
            label="🏛️ Select Active Engineering Mitigation Policy Consensus View:",
            options=[
                "As-Is Existing System State (Unmitigated Core Risk)",
                "Centralised Primary Intake Bay (Boundary Patch)",
                "Source-Level Distributed Mitigation (Nested MCC Panel) [Consensus]",
            ],
            index=0,
            help="Directly adjusts the high-voltage electrical architecture geometry, switching between localized protection or broad boundary mitigation.",
        )

        st.markdown("---")

        if st.session_state.sandbox_assets.shape[0] == 0:
            st.info(
                "No active assets registered. Please append rows inside the staging clipboard."
            )
        else:
            if sld_policy_mode == "As-Is Existing System State (Unmitigated Core Risk)":
                st.markdown(
                    "##### ⚠️ Current Grid Topology (Unmitigated Core Risk Profile)"
                )
            elif sld_policy_mode == "Centralised Primary Intake Bay (Boundary Patch)":
                st.markdown("##### 🟢 Centralised Intake Bay Layout (Boundary Masking)")
            else:
                st.markdown(
                    "##### 🛡️ Source-Level Distributed Infrastructure Grid (Systems-Thinking Alignment)"
                )

            dot_string = generate_dynamic_sld_graph(
                st.session_state.sandbox_assets, policy=sld_policy_mode
            )
            st.graphviz_chart(dot_string, use_container_width=True)
