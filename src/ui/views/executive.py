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
    streaming financial tickers, and dynamic real-time payback calculators
    to the absolute apex of the platform runtime.
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

    if "executive_chat_history" not in st.session_state:
        st.session_state.executive_chat_history = [
            {
                "role": "assistant",
                "text": "🏛️ *Welcome to the Executive Command Centre.* I am synced live with your plant's grid topology, verified financial payback arrays, and macro opportunity-cost curves.",
            }
        ]

    # --------------------------------------------------------------------------
    # 🗂️ SIDEBAR SCENARIO ENGINE: Interactive Boardroom Modeling Sliders
    # --------------------------------------------------------------------------
    with st.sidebar.expander(
        "📊 Executive Sensitivity & Downtime Modeling", expanded=True
    ):
        st.markdown("### 💼 Operational Valuation Variables")
        st.caption(
            "Adjust these market and operational parameters to evaluate the business risk of grid-level power anomalies."
        )
        st.markdown("---")
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

    # 📈 DYNAMIC FINANCIAL HARDENING ENGINE
    single_event_loss = st.session_state.prod_val * st.session_state.restart_hrs
    total_unmitigated_exposure = single_event_loss * st.session_state.annual_events

    # Base verified engineering savings metrics
    insulation_depreciation_savings = (
        23800.0
        if "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes
        else 0.0
    )
    copper_loss_energy_savings = (
        26400.0
        if "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes
        else 0.0
    )
    total_annual_engineering_savings = (
        insulation_depreciation_savings + copper_loss_energy_savings
    )

    # Calculate active installation CapEx based on layout array
    capex_total = 0.0
    if (
        "Primary Intake Switchboard (Centralised Bay)"
        in st.session_state.selected_nodes
    ):
        capex_total += 85000
    if "Heavy Industrial Process Board (Panel B1)" in st.session_state.selected_nodes:
        capex_total += 42000
    if "Motor Control Centre (MCC Panel B2)" in st.session_state.selected_nodes:
        capex_total += 35000
    if "Auxiliary & Building Services (Panel B3)" in st.session_state.selected_nodes:
        capex_total += 18000
    if (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    ):
        capex_total += 65000

    # Calculate payback natively using the verified 8.37 month logic matrix
    if total_annual_engineering_savings > 0:
        calculated_payback_months = (
            capex_total / total_annual_engineering_savings
        ) * 12.0
        payback_delta_text = f"↑ Payback: {calculated_payback_months:.2f} Months"
    else:
        payback_delta_text = "No Active Engineering Savings"

    # Assess resilience architecture state for opportunity cost mitigation
    has_bess_ups = (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    )
    current_exposure = 0.0 if has_bess_ups else total_unmitigated_exposure
    insurance_credit = (
        "£12,400 / yr"
        if len(st.session_state.selected_nodes) >= 2
        else "£0 (High Risk Exposure Portfolio)"
    )

    # --------------------------------------------------------------------------
    # 🔥 THE TICKER: STREAMING EXECUTIVE RISK & SYSTEMIC FAILURE MARQUEE
    # --------------------------------------------------------------------------
    if current_exposure > 0:
        ticker_html = f"""
        <div style="background-color: #FFF0F0; border-left: 5px solid #D9272E; padding: 12px; border-radius: 4px; margin-bottom: 25px; overflow: hidden; white-space: nowrap;">
            <marquee behavior="scroll" direction="left" scrollamount="6" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: bold; color: #D9272E;">
                🚨 COMMAND CENTRE RISK ALERT: Unmitigated localized opportunity cost exposure is currently £{current_exposure:,.0f} / year ••• [INSULATION WEAR DEPRECIATION PENALTY: £{insulation_depreciation_savings:,.0f} / YR] ••• [WASTED COPPER LOSS ENERGY COST: £{copper_loss_energy_savings:,.0f} / YR] ••• A single utility voltage sag triggers an immediate £{single_event_loss:,.0f} line interruption reset bottleneck ••• Deploy high-speed shunt hybrid backup assets to insulate plant revenue streams.
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
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(
            label="📉 Residual Cash Bleed (Remaining Exposure)",
            value=f"£{current_exposure:,.0f} / yr",
            delta=(
                "-100% Fully Shielded"
                if has_bess_ups
                else "Unmitigated Revenue Liability"
            ),
            delta_color="normal" if has_bess_ups else "inverse",
        )
    with metric_col2:
        st.metric(
            label="💰 Active Mitigation CapEx",
            value=f"£{capex_total:,.0f}",
            delta=payback_delta_text,
            delta_color="normal",
        )
    with metric_col3:
        st.metric(
            label="🔌 Underwriter Premium Credit",
            value=insurance_credit,
            delta=(
                "Premium Incentive Unlocked"
                if len(st.session_state.selected_nodes) >= 2
                else "High Vulnerability Status"
            ),
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
            The asset portfolio at Ammanford Alloys carries an unmitigated annualized risk posture of **£{current_exposure:,.0f}/year** due to incoming grid power fluctuations. Factoring in an operational valuation run-rate of **£{st.session_state.prod_val:,.0f}/hour** and an average line clearance latency of **{st.session_state.restart_hrs:.1f} hours**, any single sub-cycle voltage sag event triggers an immediate opportunity cost production loss of **£{single_event_loss:,.0f}**.
            
            #### 2. Infrastructure Resilience Allocations & Proven Payback
            To protect production margins from grid volatility, the steering committee outlines a total targeted implementation expenditure of **£{capex_total:,.0f}**. 
            
            When deployed against the Motor Control Centre switchgear, this infrastructure reclaims **£23,800/year** in avoided machine depreciation stress and **£26,400/year** in direct electrical waste mitigation, resulting in an annualized baseline optimization yield of **£{total_annual_engineering_savings:,.0f}**. This delivers a verified capital amortization cycle of exactly **{calculated_payback_months:.2f} months** before modeling macro opportunity cost revenue protections.
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
                - Annualized Risk Exposure: £{current_exposure:,.0f}
                - Annualized Direct Engineering Savings (Depreciation + Energy): £{total_annual_engineering_savings:,.0f}
                - Active Project Payback Period: {calculated_payback_months:.2f} Months
                - Insurance Broker Premium Credit: {insurance_credit}
                
                💰 BUDGETARY CAPITAL COST ENGINEERING ESTIMATES:
                1. Primary Intake Switchboard (Centralised Bay): £85,000
                2. Heavy Industrial Process Board (Panel B1): £42,000
                3. Motor Control Centre (MCC Panel B2): £35,000 (Unlocks £23.8k depreciation savings + £26.4k electricity savings; 8.37 month payback)
                4. Auxiliary & Building Services (Panel B3): £18,000
                5. Local BESS & Hybrid UPS Array (Robotics Asset Protection): £65,000. Eradicates opportunity cost exposure entirely via sub-20ms sub-cycle transfer capability.
                
                CASE STUDY BENCHMARK REFERENCE:
                - Aston Martin St Athan Plant: Peak output 28 cars/day, target run-rate 16-20 cars/day (DBX line). At £150k+ per vehicle, a 4-hour robotics line failure cost £1.2M - £1.5M in lost throughput per single event.
                
                Be conversational, strategic, and highly supportive of executive goals. If the user asks to add, change, remove, or modify active nodes, use your function-calling tools instantly to alter the state.
                """

                from src.ui.views.data_entry import update_electrical_mitigation_nodes

                exec_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[system_context, exec_input],
                    config=types.GenerateContentConfig(
                        tools=[update_electrical_mitigation_nodes],
                        temperature=0.15,
                        system_instruction="You are a trusted strategic C-suite technology advisor. Speak with clear boardroom-ready authority. Natively use built-in financial loss, cost estimation, and the verified 8.37 month payback data to frame business cases.",
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
