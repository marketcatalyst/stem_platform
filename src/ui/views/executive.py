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
    and Actuarial Appraisal Dashboard. Features an all-inclusive scrolling ticker tape
    integrating opportunity costs, asset depreciation, and energy consumption losses.
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

    # 🏛️ SYSTEM PARAMETER FORMULAS & HEURISTICS
    single_event_loss = prod_val * restart_hrs
    total_unmitigated_opportunity_cost = single_event_loss * annual_events

    # Financial Engineering Heuristics per Node Block
    cost_mapping = {
        "Primary Intake Switchboard (Centralised Bay)": 85000,
        "Heavy Industrial Process Board (Panel B1)": 42000,
        "Motor Control Centre (MCC Panel B2)": 35000,
        "Auxiliary & Building Services (Panel B3)": 18000,
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)": 65000,
    }

    # ⚡ Electricity Consumption Reduction Savings Model (Wasted Heat Reclaimed)
    energy_loss_mapping = {
        "Primary Intake Switchboard (Centralised Bay)": 8500,
        "Heavy Industrial Process Board (Panel B1)": 14200,
        "Motor Control Centre (MCC Panel B2)": 6800,
        "Auxiliary & Building Services (Panel B3)": 1500,
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)": 2200,
    }

    # 📉 Accelerated Asset Depreciation Cost Model (Thermal Insulation Strain Avoided)
    depreciation_loss_mapping = {
        "Primary Intake Switchboard (Centralised Bay)": 12000,
        "Heavy Industrial Process Board (Panel B1)": 9500,
        "Motor Control Centre (MCC Panel B2)": 7200,
        "Auxiliary & Building Services (Panel B3)": 800,
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)": 1500,
    }

    # Calculate Totals based on current active state selections
    total_capex = sum(
        cost_mapping.get(node, 0) for node in st.session_state.selected_nodes
    )
    active_energy_savings = sum(
        energy_loss_mapping.get(node, 0) for node in st.session_state.selected_nodes
    )
    active_depreciation_saved = sum(
        depreciation_loss_mapping.get(node, 0)
        for node in st.session_state.selected_nodes
    )

    # Max baseline exposures when no interventions are selected
    max_energy_waste = sum(energy_loss_mapping.values())
    max_depreciation_penalty = sum(depreciation_loss_mapping.values())

    # Calculate ongoing operational bleeding
    current_wasted_energy = max_energy_waste - active_energy_savings
    current_excess_depreciation = max_depreciation_penalty - active_depreciation_saved

    has_ups_protection = (
        "Local BESS & Hybrid UPS Array (Robotics Asset Protection)"
        in st.session_state.selected_nodes
    )
    current_opportunity_exposure = (
        0.0 if has_ups_protection else total_unmitigated_opportunity_cost
    )

    insurance_credit_val = 12400 if len(st.session_state.selected_nodes) >= 2 else 0
    insurance_credit = (
        f"£{insurance_credit_val:,}/yr"
        if insurance_credit_val > 0
        else "£0 (High Risk Profile)"
    )

    # Final C-Suite Valuation Calculations
    total_annual_benefit = (
        active_energy_savings
        + active_depreciation_saved
        + (total_unmitigated_opportunity_cost if has_ups_protection else 0)
        + insurance_credit_val
    )
    payback_months = (
        (total_capex / total_annual_benefit * 12) if total_annual_benefit > 0 else 0.0
    )

    # --------------------------------------------------------------------------
    # 🚨 THE UNIFIED TRIPARTITE DYNAMIC SCROLLING TICKER TAPE
    # --------------------------------------------------------------------------
    if has_ups_protection and len(st.session_state.selected_nodes) >= 3:
        ticker_html = f"""
        <div style="background-color: #E6FFFA; padding: 12px; border-radius: 6px; border-left: 6px solid #00A389; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="4" style="color: #006654; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🟢 STEM OPTIMISED SUSTAINABLE GRID ACTIVE ••• NET OPPORTUNITY COST EXPOSURE INSULATED TO: £0/YR ••• RECLAIMED DIRECT ELECTRICITY CONSUMPTION SAVINGS: £{active_energy_savings:,.0f}/YR ••• FOREGONE ACCELERATED ASSET DEPRECIATION SAVINGS: £{active_depreciation_saved:,.0f}/YR ••• ACTUARIAL COMPLIANCE PREMIUM CREDIT: {insurance_credit} ••• TOTAL ANNUAL RECOVERED BALANCE SHEET VALUE: £{total_annual_benefit:,.0f}/YR
            </marquee>
        </div>
        """
    else:
        ticker_html = f"""
        <div style="background-color: #FCE8E6; padding: 12px; border-radius: 6px; border-left: 6px solid #D9272E; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <marquee scrollamount="5" style="color: #A81C1C; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;">
                🚨 STEM LIVE THREAT INVENTORY // UNMITIGATED CONCURRENT EXPOSURES RUNNING ••• DOWNTIME OPPORTUNITY COST EXPOSURE: £{current_opportunity_exposure:,.0f}/YR ••• HARMONIC ACCELERATED ASSET DEPRECIATION PENALTY: £{current_excess_depreciation:,.0f}/YR ••• WASTED ELECTRICITY EFFICIENCY DIRECT CONSUMPTION LOSS: £{current_wasted_energy:,.0f}/YR ••• TOTAL UNMITIGATED CASH BLEED RATE: £{(current_opportunity_exposure + current_excess_depreciation + current_wasted_energy):,.0f}/YR // ACTION REQUIRED
            </marquee>
        </div>
        """
    st.markdown(ticker_html, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 📈 THE C-SUITE FINANCIAL RISK SCORECARD RIBBON
    # --------------------------------------------------------------------------
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(
            label="📉 Annualised Operational & Opportunity Exposure",
            value=f"£{(current_opportunity_exposure + current_excess_depreciation + current_wasted_energy):,.0f} / yr",
            delta=(
                f"£{total_annual_benefit:,.0f}/yr Saved"
                if total_annual_benefit > 0
                else "Unmitigated Bleed"
            ),
            delta_color="normal" if total_annual_benefit > 0 else "inverse",
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
            label="🛡 extinction Underwriter Premium Credit",
            value=insurance_credit,
            delta=(
                "Risk Profile Approved"
                if insurance_credit_val > 0
                else "G5/5 Compliance Risk"
            ),
        )

    st.markdown("---")

    # --------------------------------------------------------------------------
    # 📊 DUAL COLUMN EXECUTIVE ANALYTICS DECK
    # --------------------------------------------------------------------------
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 📝 Integrated Value Chain & Loss Justification Narrative")
        st.markdown(
            f"A comprehensive systems-thinking financial audit demands that electrical infrastructure be treated as an "
            f"integrated value driver rather than an engineering cost center. Unmitigated network distortion across your "
            f"circuits results in a combined annual cash drag consisting of three parallel layers:\n\n"
            f"1. **Opportunity Cost of Interruption:** **£{current_opportunity_exposure:,.0f}/yr** at risk from utility grid sags.\n"
            f"2. **Accelerated Asset Degradation:** **£{current_excess_depreciation:,.0f}/yr** in baseline equipment lifespan truncation caused by high harmonic thermal stress.\n"
            f"3. **Direct Energy Inefficiency:** **£{current_wasted_energy:,.0f}/yr** in pure copper losses and harmonic reactive penalties."
        )

        if has_ups_protection:
            st.success(
                f"🎯 **Capital Protection Verified:** Active interventions have successfully captured **£{active_energy_savings:,.0f}/yr** "
                f"in direct electrical consumption reductions and preserved **£{active_depreciation_saved:,.0f}/yr** in hardware asset lifetime extensions, "
                f"completely insulating the facility from sudden downtime bottlenecks."
            )
        else:
            st.warning(
                f"🚨 **System Exposure Notice:** Core operations are currently bleeding unnecessary capital. Activating distributed "
                f"shunt filtering or BESS protection on your staging data tab will instantly arrest these parallel cash drains."
            )

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
            f"* Dynamic Opportunity Risk: **£{calculated_sim_loss:,.0f}/yr**"
        )

        st.markdown("### 📦 Active Infrastructure Allocations")
        if not st.session_state.selected_nodes:
            st.caption("No active optimization hardware assets currently deployed.")
        else:
            for node in st.session_state.selected_nodes:
                capex_val = cost_mapping.get(node, 0)
                st.markdown(f" * 🛡️ **{node}** (`£{capex_val:,}` CapEx)")

        st.markdown("### 📊 Capital Allocation Breakdown")
        summary_data = {
            "Financial Vector": [
                "Unmitigated Opportunity Exposure",
                "Accelerated Asset Wear Bleed",
                "Wasted Consumption Cost",
                "Mitigation Investment CapEx",
                "Net Total Annual Benefit",
                "Project Payback Horizon",
            ],
            "Value": [
                f"£{current_opportunity_exposure:,.0f}/yr",
                f"£{current_excess_depreciation:,.0f}/yr",
                f"£{current_wasted_energy:,.0f}/yr",
                f"£{total_capex:,.0f}",
                f"£{total_annual_benefit:,.0f}/yr",
                f"{payback_months:.1f} Months" if payback_months > 0 else "N/A",
            ],
        }
        st.table(pd.DataFrame(summary_data))
