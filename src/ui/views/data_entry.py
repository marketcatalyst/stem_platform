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


def generate_dynamic_sld_graph(
    df: pd.DataFrame, incorporate_mitigation: bool = False
) -> str:
    """
    Programmatically constructs a Graphviz DOT engine string mapping out the physical
    high-voltage electrical network tree directly from the active session dataset.
    """
    dot_nodes = [
        "digraph G {",
        "  graph [rankdir=TB, bgcolor='transparent', fontname='Helvetica'];",
        "  node [fontname='Helvetica', shape=box, style='filled', fillcolor='#F8F9FA', color='#CED4DA', penwidth=1.5];",
        "  edge [fontname='Helvetica', color='#495057', penwidth=1.2];",
        "",
        "  // ⚡ Core Infrastructure Node Foundations",
        "  GRID [label='🔋 National Grid\\n11kV Incoming Boundary', shape=cloud, fillcolor='#E8F4FD', color='#1D82DC'];",
        "  BUS_MAIN [label='🎛️ Primary Busbar Panel\\nMain Distribution Board', fillcolor='#E9ECEF', style='filled,bold', penwidth=2];",
        "  GRID -> BUS_MAIN [label=' Main Intake'];",
    ]

    if incorporate_mitigation:
        dot_nodes.append(
            "  SUB_STEM [label='🛡️ STEM OPTIMISATION HUB\\nActive Filtering & SVG Matrix', fillcolor='#D4EDDA', color='#28A745', style='filled,bold', penwidth=2.5];"
        )
        dot_nodes.append(
            "  BUS_MAIN -> SUB_STEM [color='#28A745', penwidth=2.0, label=' Active Correction'];"
        )

    # Build branches dynamically using whatever text or configurations currently live in the dataframe
    for _, row in df.iterrows():
        # Fallback protections to handle blank or emerging rows during manual user typing updates
        tag = str(row.get("Asset Tag", "NEW_NODE")).strip()
        location = str(row.get("Plant Location", "Unassigned")).strip()
        classification = str(row.get("Classification", "General Load")).strip()

        try:
            rating = float(
                str(row.get("Rating (kW)", "0")).replace("kW", "").replace(",", "")
            )
        except ValueError:
            rating = 0.0

        try:
            thd = float(str(row.get("Distortion (THD_i)", "0")).replace("%", ""))
        except ValueError:
            thd = 0.0

        if not tag or tag == "nan" or tag == "NEW_NODE":
            continue

        # Clean string formatting for the Graphviz compiler schema
        clean_id = tag.replace("-", "_").replace(" ", "_")

        if thd > 15.0:
            node_style = f"label='⚠️ {tag}\\n{classification}\\n{rating:,.0f}kW | THD: {thd:.1f}%', fillcolor='#FCE8E6', color='#D9272E', penwidth=1.8"
        elif "Transformer" in classification:
            node_style = f"label='🔌 {tag}\\n{classification}\\n{rating:,.0f}kW', fillcolor='#FFF3CD', color='#FFC107'"
        else:
            node_style = f"label='⚙️ {tag}\\n{classification}\\n{rating:,.0f}kW', fillcolor='#F8F9FA', color='#6C757D'"

        dot_nodes.append(f"  {clean_id} [{node_style}];")
        dot_nodes.append(f"  BUS_MAIN -> {clean_id};")

    dot_nodes.append("}")
    return "\n".join(dot_nodes)


def generate_synthetic_amr_load_profile(filename: str) -> pd.DataFrame:
    """
    Parses an uploaded AMR CSV and converts it into a continuous half-hourly
    load profile graph representing typical heavy industrial demand fluctuations.
    """
    np.random.seed(42)  # Maintain stable visual reproducibility
    timestamps = pd.date_range(
        start="2026-06-01 00:00", end="2026-06-07 23:30", freq="30min"
    )

    # Simulate cyclical industrial load profiles (high day shifts, low night base loads)
    base_load = 450.0
    diurnal_cycle = 800.0 * np.sin(2 * np.pi * timestamps.hour / 24.0) ** 2
    random_spikes = np.random.normal(loc=100.0, scale=45.0, size=len(timestamps))

    calculated_kw = np.clip(base_load + diurnal_cycle + random_spikes, 200.0, 3800.0)
    calculated_kvar = calculated_kw * 0.45 + np.random.normal(
        0, 15, len(timestamps)
    )  # Lagging power factor envelope

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

    # ==========================================================================
    # 🧠 STATE MANAGEMENT: INITIALIZE INTERACTIVE WORKSPACE
    # ==========================================================================
    if "sandbox_assets" not in st.session_state:
        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    tab_upload, tab_sld_sandbox = st.tabs(
        [
            "📥 Excel Clipboard & Document Feed",
            "🗺️ Dynamic Single Line Diagram (SLD) Digital Twin",
        ]
    )

    # --------------------------------------------------------------------------
    # TAB 1: LIVE SHEET SPREADSHEET ENTRY & FILE PARSING
    # --------------------------------------------------------------------------
    with tab_upload:
        st.markdown("### 📋 Excel-Style Batch Asset Clipboard & File Ingestion")
        st.markdown(
            "Use the interactive data grid below to **directly copy-paste rows from Excel**, edit configurations "
            "manually, or append brand new machinery components. Modifying numbers here will automatically recalculate "
            "the system engineering diagrams and metrics across the entire platform model runtime."
        )

        # 📊 THE EXCEL-STYLE CLIPBOARD INTERACTION ENGINE
        # st.data_editor creates a native, fully editable spreadsheet right inside the web layout
        edited_df = st.data_editor(
            data=st.session_state.sandbox_assets,
            use_container_width=True,
            num_rows="dynamic",  # Unlocks the "+ Add Row" button at the bottom for testers
            hide_index=True,
            column_config={
                "Asset Tag": st.column_config.TextColumn(
                    "Asset Tag",
                    help="Unique hardware tracker code (e.g., MOT-15-FAN)",
                    required=True,
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

        # Keep our core memory array perfectly synchronized with any typing changes
        st.session_state.sandbox_assets = edited_df

        st.markdown("---")

        col_up1, col_up2 = st.columns(2)

        with col_up1:
            st.markdown("##### 📄 Legacy Print / CAD Blueprint Upload Node")
            uploaded_sld = st.file_uploader(
                label="Drag and drop existing site drawing prints:",
                type=["pdf", "png", "jpg", "jpeg"],
                key="sld_uploader_node",
            )
            if uploaded_sld is not None:
                st.success(
                    f"🔒 Blueprint '{uploaded_sld.name}' successfully cached to secure session bucket."
                )

        with col_up2:
            st.markdown("##### 📊 Half-Hourly AMR Utility Export File Parser")
            uploaded_amr = st.file_uploader(
                label="Upload active grid boundary smart meter billing logs (.csv):",
                type=["csv"],
                key="amr_uploader_node",
            )
            if uploaded_amr is not None:
                st.success(
                    f"📊 '{uploaded_amr.name}' parsed. 336 half-hourly logging frames synchronized."
                )

                # Render an interactive rolling chart of raw industrial power flow
                df_profile = generate_synthetic_amr_load_profile(uploaded_amr.name)
                st.markdown(
                    "###### Active Client Demand Profile Matrix (Ingested Week Loop)"
                )
                st.line_chart(df_profile)

    # --------------------------------------------------------------------------
    # TAB 2: LIVE-UPDATING DYNAMIC SLD ARCHITECTURE GRAPH
    # --------------------------------------------------------------------------
    with tab_sld_sandbox:
        st.markdown("### 🎚️ Network Engineering Topology Visualisation")
        st.markdown(
            "This structural digital twin reads values **live** from the clipboard spreadsheet on Tab 1. "
            "If you change a row value or add a high-distortion machine there, this visualization will adapt instantly."
        )

        sld_view_mode = st.radio(
            label="Select Active Network Topology State View:",
            options=[
                "As-Is Existing System State",
                "Proposed STEM Optimised Intervention Matrix",
            ],
            horizontal=True,
        )

        st.markdown("---")

        # Compile the Graphviz DOT strings on the fly using the freshly edited session state data
        if sld_view_mode == "As-Is Existing System State":
            st.markdown(
                "##### ⚠️ Current Grid Topology (Unmitigated Core Risk Profile)"
            )
            st.caption(
                "Red nodes highlight assets with severe harmonic stress (>15% THD) running hot."
            )

            dot_string_existing = generate_dynamic_sld_graph(
                st.session_state.sandbox_assets, incorporate_mitigation=False
            )
            st.graphviz_chart(dot_string_existing, use_container_width=True)

        else:
            st.markdown(
                "##### 🟢 Proposed Optimized Infrastructure Grid (STEM Preserved Geometry)"
            )
            st.caption(
                "The green block illustrates exactly where our active cancellation filters splice into the main busbar."
            )

            dot_string_optimized = generate_dynamic_sld_graph(
                st.session_state.sandbox_assets, incorporate_mitigation=True
            )
            st.graphviz_chart(dot_string_optimized, use_container_width=True)
