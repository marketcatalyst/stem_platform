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


def render_executive_view():
    """
    Renders the comprehensive C-suite Financial Risk, Strategic Investment Briefing,
    and Actuarial Appraisal Dashboard. Synchronises perfectly with live site telemetry
    and shared parameter configurations.
    """
    st.markdown("## 🏛️ Executive Boardroom Command Center")
    st.markdown(
        "##### Macro Financial Risk Modeling, Actuarial Appraisals, and Capital Governance"
    )
    st.markdown("---")

    # Fallback initialization safeguards to keep shared state memory completely stable
    if "sandbox_assets" not in st.session_state:
        st.session_state.sandbox_assets = load_ammanford_alloys_dataset()

    if "selected_nodes" not in st.session_state:
        st.session_state.selected_nodes = ["Motor Control Centre (MCC Panel B2)"]

    # Pull baseline values safely from memory or fall back to standard defaults
    prod_val = st.session_state.get("prod_val", 150000)
    restart_hrs = st.session_state.get("restart_hrs", 4.0)
    annual_events = st.session_state.get("annual_events", 3)

    # Dynamic Calculations based on active policy state
    single_event_loss = prod_val * restart_hrs
    total_unmitigated_exposure = single_event_loss * annual_events

    # Capital Expenditure Cost Profile Mapping Heuristics
    cost_mapping = {
        "Primary Intake Switchboard (Centralised Bay)": 85000,
        "Heavy Industrial Process Board (Panel B1)": 42000,
        "Motor Control Centre (MCC Panel B2)": 35000,
        "Auxiliary & Building Services (Panel B3)": 18000,
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)": 65000,
    }

    total_capex = sum(
        cost_mapping.get(node, 0) for node in st.session_state.selected_nodes
    )

    # Assess if protective measures are deployed
    has_ups_protection = (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    )
    current_exposure = 0.0 if has_ups_protection else total_unmitigated_exposure
    annual_savings = total_unmitigated_exposure if has_ups_protection else 0.0

    insurance_credit_val = 12400 if len(st.session_state.selected_nodes) >= 2 else 0
    insurance_credit = (
        f"£{insurance_credit_val:,} / yr"
        if insurance_credit_val > 0
        else "£0 (High Risk Profile)"
    )

    # Strategic Financial Appraisal Formulas
    total_annual_benefit = annual_savings + insurance_credit_val
    payback_months = (
        (total_capex / total_annual_benefit * 12) if total_annual_benefit > 0 else 0.0
    )

    # --------------------------------------------------------------------------
    # 📈 THE C-SUITE FINANCIAL RISK SCORECARD RIBBON
    # --------------------------------------------------------------------------
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(
            label="📉 Annualised Profit Exposure",
            value=f"£{current_exposure:,.0f} / yr",
            delta=(
                "-100% Insulated" if has_ups_protection else "Critical Operational Risk"
            ),
            delta_color="normal" if has_ups_protection else "inverse",
        )
    with metric_col2:
        st.metric(
            label="💰 Implemented Mitigation CapEx",
            value=f"£{total_capex:,.0f}",
            delta=(
                f"Payback: {payback_months:.1f} Months"
                if payback_months > 0
                else "No Active Investment"
            ),
            delta_color="normal",
        )
    with metric_col3:
        st.metric(
            label="🛡️ Underwriter Premium Credit",
            value=insurance_credit,
            delta=(
                "Risk Profile Approved"
                if insurance_credit_val > 0
                else "G5/5 Penalty Exposure"
            ),
        )

    st.markdown("---")

    # --------------------------------------------------------------------------
    # 📊 DUAL COLUMN EXECUTIVE ANALYTICS DECK
    # --------------------------------------------------------------------------
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 📝 Strategic Capital Justification Narrative")
        st.markdown(
            f"An empirical review of plant-wide electrical infrastructure reveals a severe dependency on utility grid "
            f"transient stability. Unmitigated harmonic distortion combined with typical voltage sags exposes the asset "
            f"base to an annualized opportunity-cost risk of **£{total_unmitigated_exposure:,.0f}**. "
        )

        # Interactive Alert States
        if has_ups_protection:
            st.success(
                f"🎯 **Capital Protection Verified:** Deploying the Local BESS & Hybrid UPS Array (£65,000) isolates "
                f"critical robotics and automation control logic from grid voltage dips. By establishing sub-20ms alternative "
                f"power injection networks, the facility completely avoids the **£{single_event_loss:,.0f}** "
                f"single-event line clearance penalty."
            )
        else:
            st.warning(
                f"🚨 **Critical Exposure Warning:** The facility's automated assembly and drive panels are currently "
                f"vulnerable to cascade trip loops. A single 50ms voltage sag will result in a mandatory **{restart_hrs} hour** "
                f"re-calibration and manual purge cycle, wiping out **£{single_event_loss:,.0f}** in net output value."
            )

        # 🚗 THE ASTON MARTIN BENCHMARK STUDY
        with st.expander(
            "🚗 Regional Case Study Reference: Aston Martin St Athan", expanded=True
        ):
            st.markdown(
                "To ground this capital risk model in regional automotive manufacturing data, look at the **Aston Martin plant in St Athan**:\n\n"
                "* **Throughput Metrics:** Engineered for a peak output of 7,000 vehicles/year, stabilizing at a standard operational baseline of ~4,000 to 5,000 luxury SUVs/year (DBX line).\n"
                "* **Daily Output:** Over a standard 250-day production schedule, this maps directly to **16 to 20 vehicles per day** (~2.0 to 2.5 cars per hour during an *8-hour shift*).\n"
                "* **The Cost of Downtime:** With a premium asset value starting at £150,000+ per vehicle, a single 4-hour robotics line failure doesn't just halt a machine—it causes an irrecoverable bottleneck loss of **8 to 10 vehicles**, hitting the balance sheet with an immediate **£1.2M to £1.5M profit loss** per event.\n\n"
                "**Systems-Thinking Application:** Investing in fast-acting hybrid shunt containment turns power quality from an obscure engineering maintenance expense into an elite corporate insurance mechanism."
            )

    with col_right:
        st.markdown("### 🎚️ Boardroom Loss Sensitivity Simulator")
        st.caption("Adjust parameters to stress-test your investment thresholds live:")

        # Dynamic slider tools for boardroom simulations
        sim_hours = st.slider(
            "Simulated Outage Reset Duration (Hours)",
            1.0,
            12.0,
            float(restart_hrs),
            0.5,
        )
        sim_events = st.slider(
            "Simulated Grid Incidents / Year", 1, 20, int(annual_events)
        )

        calculated_sim_loss = prod_val * sim_hours * sim_events

        st.info(
            f"🔮 **Simulated Financial Exposure:**\n\n"
            f"* Cost per Outage: **£{prod_val * sim_hours:,.0f}**\n"
            f"* Total Annual Risk: **£{calculated_sim_loss:,.0f}**"
        )

        st.markdown("### 📦 Active Infrastructure Allocations")
        if not st.session_state.selected_nodes:
            st.caption("No active optimization hardware assets currently deployed.")
        else:
            for node in st.session_state.selected_nodes:
                capex_val = cost_mapping.get(node, 0)
                st.markdown(f" * 🛡️ **{node}** (`£{capex_val:,}` CapEx)")

        # Financial Summary Reference Data Grid
        st.markdown("### 📊 Capital Allocation Breakdown")
        summary_data = {
            "Financial Metric": [
                "Unmitigated Risk Exposure",
                "Active Mitigation CapEx",
                "Net Annualised Benefit",
                "Project Payback Period",
            ],
            "Value": [
                f"£{total_unmitigated_exposure:,.0f}/yr",
                f"£{total_capex:,.0f}",
                f"£{total_annual_benefit:,.0f}/yr",
                f"{payback_months:.1f} Months" if payback_months > 0 else "N/A",
            ],
        }
        st.table(pd.DataFrame(summary_data))
