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


def update_electrical_mitigation_nodes(nodes: list[str]) -> str:
    """Executes a structural mutation of the SLD network architecture memory."""
    st.session_state.selected_nodes = nodes
    return f"Consensus updated. Native active nodes deployed: {nodes}"


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
                "text": "👋 Welcome to the upgraded STEM Executive Portal. I am synced with your plant parameters, macro opportunity-cost models, and insurance premium risk curves. Let's optimize the network's financial engineering.",
            }
        ]

    with st.sidebar.expander("💼 Macro Facility Valuation Variables", expanded=True):
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

    # 🧮 HARMONIZED TRIPARTITE CALCULATION BLOCK (MATCHES EXECUTIVE VIEW)
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
        else "£0 (High Risk Exposure Portfolio)"
    )

    # --------------------------------------------------------------------------
    # 🚨 DYNAMIC SCROLLING RISK MARQUEE (PERFECT MULTI-TAB ALIGNMENT)
    # --------------------------------------------------------------------------
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

    # 📈 SECONDARY EXECUTIVE RIBBON DATA METRICS
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
        tab_sld_sandbox, tab_brief, tab_upload = st.tabs(
            [
                "🗺️ Dynamic Single Line Diagram (SLD) Digital Twin",
                "📜 Live Automated Strategic Brief",
                "📥 Excel Clipboard & Document Feed",
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
                help="Select one or more circuits to see how the system seamlessly scales and deploys co-located active power elements.",
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
            Ammanford Alloys currently carries an active annualized operational risk posture of **£{total_residual_leak:,.0f}/year** consisting of parallel downtime vulnerabilities, unmitigated energy friction, and accelerated hardware degradation. Based on an active line valuation of **£{st.session_state.prod_val:,.0f}/hour** and an average process calibration restart curve of **{st.session_state.restart_hrs:.1f} hours**, a single sub-cycle voltage sag event results in an immediate opportunity cost bottleneck loss of **£{single_event_loss:,.0f}**.
            
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

    with col_copilot:
        st.markdown("### 🧠 STEM AI Co-Pilot Console")
        st.caption("Two-Way Conversational Topology Optimization Gateway")
        st.markdown("---")

        chat_container = st.container(height=450)
        with chat_container:
            for message in st.session_state.copilot_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["text"])

        if user_prompt := st.chat_input(
            "Ask about capital costs, opportunity costs, or insurance credits..."
        ):
            st.session_state.copilot_history.append(
                {"role": "user", "text": user_prompt}
            )
            with chat_container:
                st.chat_message("user").markdown(user_prompt)

            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                system_context = f"""
                You are the master STEM Power Quality AI Agent. You blend technical electrical physics with corporate financial risk modeling.
                
                LIVE FACILITY DATA OVERVIEW:
                - Deployed Active Shunt Nodes: {st.session_state.selected_nodes}
                - Hourly Plant Production Value: £{st.session_state.prod_val:,.0f} / hr
                - Process Reset Loop Downtime: {st.session_state.restart_hrs} hours
                - Single Interruption Interruption Cost: £{single_event_loss:,.0f}
                - Annualized Risk Exposure: £{total_residual_leak:,.0f} / yr
                - Expected Annual Insurance Premium Reduction: {insurance_credit}
                
                Budgetary Cost Metrics: Switchboard=£85k, Furnace Sub-Board=£42k, MCC B2=£35k, Aux Panel=£18k, UPS/BESS=£65k.
                
                CASE STUDY BENCHMARK (ASTON MARTIN ST ATHAN):
                - Peak capacity of 7,000 cars/yr (~28 cars/day). Normal rate ~4,000-5,000 cars/yr (~16-20 cars/day). At £150k+ per vehicle, a 4-hour reset bottleneck costs £1.2M - £1.5M in lost throughput per single grid anomaly event.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[system_context, user_prompt],
                    config=types.GenerateContentConfig(
                        tools=[update_electrical_mitigation_nodes],
                        temperature=0.15,
                        system_instruction="You are a brilliant cost consultant and systems-thinking power engineer. Speak with professional, boardroom-ready authority. Never give canned robotic disclaimers.",
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
                                    "text": f"🤖 **AI Optimization Action Executed:**\n`{execution_result}`\n\nI have rewritten the network topology tree and updated the active business risk metrics on your executive ribbon.",
                                }
                            )
                else:
                    reply = (
                        response.text
                        if response.text
                        else "Telemetry data parsed. System state stabilized."
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
