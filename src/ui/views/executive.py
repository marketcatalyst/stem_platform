import os
import sys
import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# ==========================================================================
# 🛡️ PATH INSURANCE POLICY (CRITICAL FOR LINUX CLOUD DEPLOYMENTS)
# ==========================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.ui.views.data_entry import generate_dynamic_sld_graph


def render_executive_view():
    """
    Renders the central Executive Command Centre dashboard. Elevates opportunity cost,
    streaming financial tickers, dynamic capital cost overrides, and real-time payback
    calculators to the absolute apex of the platform runtime.
    """
    # 🔄 Synchronized Global Session State Initialisation Checks
    if "sandbox_assets" not in st.session_state:
        from src.ui.views.operations import load_ammanford_alloys_dataset

        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    if "selected_nodes" not in st.session_state:
        st.session_state.selected_nodes = ["Motor Control Centre (MCC Panel B2)"]

    if "prod_val" not in st.session_state:
        st.session_state.prod_val = 150000

    if "restart_hrs" not in st.session_state:
        st.session_state.restart_hrs = 4.0

    if "annual_events" not in st.session_state:
        st.session_state.annual_events = 3

    # Baseline CapEx State Initializers
    if "capex_intake" not in st.session_state:
        st.session_state.capex_intake = 85000
    if "capex_heavy" not in st.session_state:
        st.session_state.capex_heavy = 42000
    if "capex_mcc" not in st.session_state:
        st.session_state.capex_mcc = 35000
    if "capex_aux" not in st.session_state:
        st.session_state.capex_aux = 18000
    if "capex_bess" not in st.session_state:
        st.session_state.capex_bess = 65000

    if "executive_chat_history" not in st.session_state:
        st.session_state.executive_chat_history = [
            {
                "role": "assistant",
                "text": "🏛️ *Welcome to the Executive Command Centre.* I am synced live with your plant's grid topology, dynamic CapEx overrides, and macro opportunity-cost curves.",
            }
        ]

    # --------------------------------------------------------------------------
    # 🗂️ SIDEBAR SCENARIO ENGINE: Sensitivity Inputs & CapEx Overwrites
    # --------------------------------------------------------------------------
    with st.sidebar.expander(
        "📊 Executive Sensitivity & Downtime Modeling", expanded=True
    ):
        st.markdown("### 💼 Operational Valuation Variables")
        st.number_input(
            "Hourly Production Line Value (£)",
            min_value=100,
            max_value=1000000,
            step=5000,
            key="prod_val",
        )
        st.slider(
            "Process Reset & Recalibration (Hours)",
            min_value=0.5,
            max_value=24.0,
            step=0.5,
            key="restart_hrs",
        )
        st.slider(
            "Documented Utility Grid Sags / Year",
            min_value=1,
            max_value=50,
            step=1,
            key="annual_events",
        )

        st.markdown("---")
        st.markdown("### 💰 STEM Asset CapEx Overrides (£)")
        st.caption("Overwrite default engineering estimates with live supplier quotes:")
        st.number_input(
            "Primary Intake Switchboard Bay", min_value=0, step=1000, key="capex_intake"
        )
        st.number_input(
            "Heavy Process Sub-Board (B1)", min_value=0, step=1000, key="capex_heavy"
        )
        st.number_input(
            "Motor Control Centre Filter (B2)", min_value=0, step=1000, key="capex_mcc"
        )
        st.number_input(
            "Auxiliary Infrastructure Panel (B3)",
            min_value=0,
            step=1000,
            key="capex_aux",
        )
        st.number_input(
            "Local BESS / Hybrid UPS Array", min_value=0, step=1000, key="capex_bess"
        )

    # 📈 DYNAMIC FINANCIAL HARDENING ENGINE
    single_event_loss = st.session_state.prod_val * st.session_state.restart_hrs
    total_unmitigated_exposure = single_event_loss * st.session_state.annual_events

    # Track physical mitigation states independently
    has_mcc_filter = (
        "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes
    )
    has_bess_ups = (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    )

    # Compute baseline dynamic engineering tracking variables
    insulation_depreciation_exposure = 23800.0 if not has_mcc_filter else 0.0
    copper_loss_energy_exposure = 26400.0 if not has_mcc_filter else 0.0
    active_technical_bleed = (
        insulation_depreciation_exposure + copper_loss_energy_exposure
    )

    # Realized annualized cash savings values
    insulation_savings_captured = 23800.0 if has_mcc_filter else 0.0
    copper_savings_captured = 26400.0 if has_mcc_filter else 0.0
    opportunity_savings_captured = total_unmitigated_exposure if has_bess_ups else 0.0

    total_combined_annual_savings = (
        insulation_savings_captured
        + copper_savings_captured
        + opportunity_savings_captured
    )

    # Calculate active installation CapEx based on dynamic state inputs
    capex_total = 0.0
    if (
        "Primary Intake Switchboard (Centralised Bay)"
        in st.session_state.selected_nodes
    ):
        capex_total += st.session_state.capex_intake
    if "Heavy Industrial Process Board (Panel B1)" in st.session_state.selected_nodes:
        capex_total += st.session_state.capex_heavy
    if "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes:
        capex_total += st.session_state.capex_mcc
    if "Auxiliary & Building Services (Panel B3)" in st.session_state.selected_nodes:
        capex_total += st.session_state.capex_aux
    if (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    ):
        capex_total += st.session_state.capex_bess

    # Calculate payback natively using the user's specific CapEx values
    if total_combined_annual_savings > 0:
        calculated_payback_months = (capex_total / total_combined_annual_savings) * 12.0
        payback_display_value = f"{calculated_payback_months:.2f} Months"
    else:
        payback_display_value = "0.00 Months"

    current_opportunity_exposure = 0.0 if has_bess_ups else total_unmitigated_exposure
    insurance_credit = (
        "£12,400 / yr"
        if len(st.session_state.selected_nodes) >= 2
        else "£0 (High Risk Exposure Portfolio)"
    )

    # --------------------------------------------------------------------------
    # 🎚️ THE TICKER: STREAMING EXECUTIVE RISK & SYSTEMIC FAILURE MARQUEE
    # --------------------------------------------------------------------------
    if (current_opportunity_exposure + active_technical_bleed) > 0:
        ticker_html = f"""
        <div style="background-color: #FFF0F0; border-left: 5px solid #D9272E; padding: 12px; border-radius: 4px; margin-bottom: 25px; overflow: hidden; white-space: nowrap;">
            <marquee behavior="scroll" direction="left" scrollamount="6" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: bold; color: #D9272E;">
                🚨 COMMAND CENTRE RISK ALERT: Unmitigated localized opportunity cost exposure is currently £{current_opportunity_exposure:,.0f} / year ••• [ACTIVE TECHNICAL BLISTERS: Insulation Depreciation At £{insulation_depreciation_exposure:,.0f}/yr | Copper Loss Grid Energy Wastage At £{copper_loss_energy_exposure:,.0f}/yr] ••• A single utility voltage sag triggers an immediate £{single_event_loss:,.0f} production bottleneck loss.
            </marquee>
        </div>
        """
    else:
        ticker_html = f"""
        <div style="background-color: #EBFBFA; border-left: 5px solid #00A389; padding: 12px; border-radius: 4px; margin-bottom: 25px; overflow: hidden; white-space: nowrap;">
            <marquee behavior="scroll" direction="left" scrollamount="5" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: bold; color: #00A389;">
                🟢 STEM COMMAND ECOSYSTEM STABILIZED: Financial opportunity cost exposure successfully insulated to £0 / year ••• Harmonic degradation mitigated across all distribution layers ••• [INSULATION LIFESPAN RESTORED: £23,800/YR SAVED] ••• [COPPER LOSSES MINIMISED: £26,400/YR RECLAIMED] ••• Actuarial underwriting risk credit status: APPROVED.
            </marquee>
        </div>
        """
    st.markdown(ticker_html, unsafe_allow_html=True)

    # Main Command Title Blocks
    st.markdown("## 🎛️ Executive Command Centre Dashboard")
    st.markdown(
        "##### Macro Portfolio Optimization, Live Single Line Digital Twins, and Financial De-risking Gateways"
    )
    st.markdown("---")

    # 📊 C-SUITE BALANCED CARD INDEX
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric(
            label="📉 Opportunity Cost Exposure",
            value=f"£{current_opportunity_exposure:,.0f} / yr",
            delta="-100% Shielded" if has_bess_ups else "Revenue At Risk",
            delta_color="normal" if has_bess_ups else "inverse",
        )
    with metric_col2:
        st.metric(
            label="⚙️ Technical Cash Bleed",
            value=f"£{active_technical_bleed:,.0f} / yr",
            delta=(
                f"£{insulation_savings_captured + copper_savings_captured:,.0f}/yr Saved"
                if has_mcc_filter
                else "Thermal Waste Loading"
            ),
            delta_color="normal" if has_mcc_filter else "inverse",
        )
    with metric_col3:
        st.metric(
            label="💰 Active Intervention CapEx",
            value=f"£{capex_total:,.0f}",
            delta="Dynamic Project Cost",
            delta_color="off",
        )
    with metric_col4:
        st.metric(
            label="⏱️ Capital Amortization Cycle",
            value=payback_display_value,
            delta="ROI Horizon",
        )

    st.markdown("---")

    # Split Workspace Layout: Technical/Briefing Controls on Left, AI Co-Pilot on Right
    col_workspace, col_ai_agent = st.columns([2, 1])

    with col_workspace:
        tab_digital_twin, tab_investment_brief = st.tabs(
            [
                "🗺️ Coordinated Single Line Diagram (SLD) Twin",
                "📜 Investment Brief & Risk Memorandum",
            ]
        )

        with tab_digital_twin:
            st.multiselect(
                label="🏛️ Core Switchgear Mitigation Asset Allocation Policy:",
                options=[
                    "Primary Intake Switchboard (Centralised Bay)",
                    "Heavy Industrial Process Board (Panel B1)",
                    "Motor Control Centre (MCC Panel B2)",
                    "Auxiliary & Building Services (Panel B3)",
                    "Local BESS & Hybrid UPS Array (Robotics Asset Protection)",
                ],
                key="selected_nodes",
                help="Toggle network infrastructure assets to observe how the active geometric layout and corresponding streaming ticker metrics adapt.",
            )
            st.markdown("---")

            dot_string = generate_dynamic_sld_graph(
                st.session_state.sandbox_assets, st.session_state.selected_nodes
            )
            st.graphviz_chart(dot_string, use_container_width=True)

        with tab_investment_brief:
            st.markdown("### 📋 Executive Business Case & Underwriting Brief")
            st.markdown("---")
            st.markdown(f"""
            #### 1. Financial Position & Revenue Bottlenecks
            The asset portfolio at Ammanford Alloys carries an unmitigated annualized opportunity cost risk posture of **£{current_opportunity_exposure:,.0f}/year** alongside an active physical technical cash bleed of **£{active_technical_bleed:,.0f}/year** from harmonic network degradation. Factoring in an operational run-rate of **£{st.session_state.prod_val:,.0f}/hour** and a calibration reset latency of **{st.session_state.restart_hrs:.1f} hours**, any single utility grid sag event triggers an immediate bottleneck loss of **£{single_event_loss:,.0f}**.
            
            #### 2. Infrastructure Resilience Allocations & Proven Payback
            To completely isolate production margins from utility grid volatility, the steering committee outlines an adjusted implementation investment allocation totaling **£{capex_total:,.0f}** based on user-verified quote profiles. 
            
            When deployed explicitly against the Motor Control Centre switchgear (MCC Panel B2), this allocation reclaims **£23,800/year** in avoided insulation depreciation stress alongside **£26,400/year** in direct copper loss energy waste mitigation. This delivers a verified engineering-level capital recovery cycle of exactly **{payback_display_value}** under current procurement assumptions.
            
            #### 3. Actuarial Risk Profile
            Implementing localized sub-20ms high-speed shunt compensation converts highly unpredictable grid disruptions into an insulated corporate asset lifecycle.
            * **Current Underwriter Financial Yield:** **{insurance_credit}**
            * **Strategic Validation:** This system-thinking framework replicates the exact risk-mitigation models utilized by world-class high-value regional manufacturers, such as the Aston Martin DBX assembly facility in St Athan, ensuring absolute continuity on critical robotics lines.
            """)
            st.button("📥 Export Boardroom Ready Proposal (.md)", key="exec_export_btn")

    # --------------------------------------------------------------------------
    # RIGHT CONTAINER: TWO-WAY AI CONVERSATIONAL COMMAND CONSOLE
    # --------------------------------------------------------------------------
    with col_ai_agent:
        st.markdown("### 🧠 Command Co-Pilot Console")
        st.caption("Strategic Multi-Circuit Natural Language Interface")
        st.markdown("---")

        exec_chat_box = st.container(height=450)
        with exec_chat_box:
            for msg in st.session_state.executive_chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["text"])

        if exec_input := st.chat_input(
            "Command the platform to optimize or recalculate risk profiles..."
        ):
            st.session_state.executive_chat_history.append(
                {"role": "user", "text": exec_input}
            )
            with exec_chat_box:
                st.chat_message("user").markdown(exec_input)

            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                system_context = f"""
                You are the master STEM Power Quality AI Agent running inside the executive command center.
                
                LIVE EXECUTIVE STATE WINDOW:
                - Active Shielding Assets: {st.session_state.selected_nodes}
                - Value / Hour of Production: £{st.session_state.prod_val:,.0f}
                - Process Line Restart Reset Window: {st.session_state.restart_hrs} hours
                - Single Outage Interruption Cost: £{single_event_loss:,.0f}
                - Annualized Opportunity Risk Exposure: £{current_opportunity_exposure:,.0f}
                - Annualized Direct Technical Harmonics Bleed: £{active_technical_bleed:,.0f}
                - Annualized Project Savings (Before Opportunity Cost): £{insulation_savings_captured + copper_savings_captured:,.0f}
                - Active Combined Project Payback Period: {payback_display_value}
                - Insurance Broker Premium Credit: {insurance_credit}
                
                💰 CURRENT RE-INITIALISED USER MODIFIABLE COST MATRIX:
                1. Primary Intake Switchboard Bay: £{st.session_state.capex_intake:,.0f}
                2. Heavy Process Sub-Board (Panel B1): £{st.session_state.capex_heavy:,.0f}
                3. Motor Control Centre (MCC Panel B2): £{st.session_state.capex_mcc:,.0f}
                4. Auxiliary Infrastructure Panel (Panel B3): £{st.session_state.capex_aux:,.0f}
                5. Local BESS & Hybrid UPS Array: £{st.session_state.capex_bess:,.0f}
                
                CASE STUDY BENCHMARK REFERENCE:
                - Aston Martin St Athan Plant: Peak output 28 cars/day, target run-rate 16-20 cars/day (DBX line). At £150k+ per vehicle, a 4-hour robotics line failure cost £1.2M - £1.5M in lost throughput per single event.
                
                Be conversational, strategic, and highly supportive of executive goals. Use your built-in cost overrides natively to frame dynamic financial engineering recommendations. If changes to asset layout selections are requested, call tools instantly.
                """

                from src.ui.views.data_entry import update_electrical_mitigation_nodes

                exec_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[system_context, exec_input],
                    config=types.GenerateContentConfig(
                        tools=[update_electrical_mitigation_nodes],
                        temperature=0.15,
                        system_instruction="You are a trusted strategic C-suite technology advisor. Speak with clear boardroom-ready authority. Natively use user-adjusted cost overrides and data vectors to frame your financial reasoning.",
                    ),
                )

                if exec_response.function_calls:
                    for functional_call in exec_response.function_calls:
                        if functional_call.name == "update_electrical_mitigation_nodes":
                            t_args = functional_call.args
                            res = update_electrical_mitigation_nodes(**t_args)
                            st.session_state.executive_chat_history.append(
                                {
                                    "role": "assistant",
                                    "text": f"🤖 **Command Executed Upstream:**\n`{res}`\n\nI have rewritten the network topology configuration. The interactive single-line digital twin, the strategic brief text, and the financial metrics cards have adjusted live.",
                                }
                            )
                else:
                    reply_msg = (
                        exec_response.text
                        if exec_response.text
                        else "Command analyzed. State constants remain locked."
                    )
                    st.session_state.executive_chat_history.append(
                        {"role": "assistant", "text": reply_msg}
                    )

            except Exception as e:
                st.session_state.executive_chat_history.append(
                    {
                        "role": "assistant",
                        "text": f"❌ **Command Processing Error:** Details: `{str(e)}`",
                    }
                )

            st.rerun()
