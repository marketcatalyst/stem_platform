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
from src.ui.components.tickers import render_cost_of_inaction_ticker
from src.modules.gemini_nlp.service import GeminiTranslationService


def load_client_portfolio_matrix(client_name: str) -> pd.DataFrame:
    """
    Data routing node that delivers the distinct validated asset profiles
    for the active Joint Venture pipeline.
    """
    if client_name == "Ammanford Alloys Ltd":
        return load_ammanford_alloys_dataset()

    elif client_name == "Swansea Silica Mining Operations":
        mining_data = [
            {
                "Asset Tag": "TX-M-01-MAIN",
                "Plant Location": "Primary Substation Intake",
                "Classification": "Grid Step-Down Transformer",
                "Rating (kW)": 2500,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": 4.8,
            },
            {
                "Asset Tag": "PMP-SLURRY-01",
                "Plant Location": "Extraction Pool Alpha",
                "Classification": "Heavy Induction Pump",
                "Rating (kW)": 400,
                "Weekly Hrs": 140,
                "Distortion (THD_i)": 18.5,
            },
            {
                "Asset Tag": "PMP-SLURRY-02",
                "Plant Location": "Extraction Pool Beta",
                "Classification": "Heavy Induction Pump",
                "Rating (kW)": 400,
                "Weekly Hrs": 140,
                "Distortion (THD_i)": 19.2,
            },
            {
                "Asset Tag": "VSD-CRUSH-01",
                "Plant Location": "Processing Face Tier 1",
                "Classification": "Variable Speed Drive (VSD)",
                "Rating (kW)": 500,
                "Weekly Hrs": 90,
                "Distortion (THD_i)": 42.0,
            },
            {
                "Asset Tag": "FAN-VENT-01",
                "Plant Location": "Deep Shaft Intake 2",
                "Classification": "Main Ventilation Fan",
                "Rating (kW)": 200,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": 7.5,
            },
            {
                "Asset Tag": "PMP-DEWATER-01",
                "Plant Location": "Lower Sump Network",
                "Classification": "Submersible Dewatering Unit",
                "Rating (kW)": 160,
                "Weekly Hrs": 110,
                "Distortion (THD_i)": 6.2,
            },
            {
                "Asset Tag": "CONV-MAIN-FEED",
                "Plant Location": "Overhead Rail Line",
                "Classification": "Main Conveyor Drive Motor",
                "Rating (kW)": 250,
                "Weekly Hrs": 120,
                "Distortion (THD_i)": 12.4,
            },
        ]
        return pd.DataFrame(mining_data)

    elif client_name == "Killan Farm Solar Array Hub":
        solar_data = [
            {
                "Asset Tag": "INV-SOLAR-01",
                "Plant Location": "Inverter Enclosure A",
                "Classification": "Central Solar Inverter",
                "Rating (kW)": 500,
                "Weekly Hrs": 70,
                "Distortion (THD_i)": 14.5,
            },
            {
                "Asset Tag": "INV-SOLAR-02",
                "Plant Location": "Inverter Enclosure B",
                "Classification": "Central Solar Inverter",
                "Rating (kW)": 500,
                "Weekly Hrs": 70,
                "Distortion (THD_i)": 15.1,
            },
            {
                "Asset Tag": "BESS-BAT-01",
                "Plant Location": "Containerised Storage Yard",
                "Classification": "Bi-Directional Battery Inverter",
                "Rating (kW)": 750,
                "Weekly Hrs": 112,
                "Distortion (THD_i)": 26.4,
            },
            {
                "Asset Tag": "TX-RENEW-01",
                "Plant Location": "Grid Boundary Compound",
                "Classification": "Step-Up Export Transformer",
                "Rating (kW)": 1250,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": 3.1,
            },
            {
                "Asset Tag": "AUX-CHILL-01",
                "Plant Location": "BESS Thermal Shroud",
                "Classification": "HVAC Cooling Network",
                "Rating (kW)": 45,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": 9.0,
            },
        ]
        return pd.DataFrame(solar_data)

    return pd.DataFrame()


def load_compliance_and_headroom_matrix(client_name: str) -> dict:
    """
    Returns structured statutory compliance and electrical capacity states
    for site infrastructure audits.
    """
    matrix = {
        "Ammanford Alloys Ltd": {
            "sld_status": "🔴 OUTDATED (Audit Required)",
            "sld_color": "error",
            "pfc_status": "⚠️ Lagging (0.82 Cos Phi)",
            "grid_compliance": "🔒 G99 Approved under G100 Export Limitation (0 kW)",
            "unlocked_headroom": "320 kVA (Potential via Active SVG Integration)",
        },
        "Swansea Silica Mining Operations": {
            "sld_status": "🟢 VERIFIED (2025 Field Survey)",
            "sld_color": "success",
            "pfc_status": "🟢 Optimized (0.92 Cos Phi)",
            "grid_compliance": "🔴 Legacy G59/3 (Requires Urgent G99 Transition)",
            "unlocked_headroom": "150 kVA (Available Node Restructuring)",
        },
        "Killan Farm Solar Array Hub": {
            "sld_status": "🟢 VERIFIED (2026 Commissioning)",
            "sld_color": "success",
            "pfc_status": "🟢 Peak Optimized (0.98 Cos Phi)",
            "grid_compliance": "🟢 G99 Compliant / G100 Active Import Control Active",
            "unlocked_headroom": "500 kW (Fully Liberated Injection Capacity)",
        },
    }
    return matrix.get(client_name, {})


def calculate_dynamic_loss_metrics(df: pd.DataFrame, client_name: str) -> dict:
    """
    Executes structural engineering computations mapping thermal dissipation
    and non-linear loss overheads against specialized tariff tiers.
    """
    utility_rate = 0.24 if "Mining" in client_name else 0.22
    total_annual_loss = 0.0
    total_capacity_kw = df["Rating (kW)"].sum()
    peak_thd = df["Distortion (THD_i)"].max()

    for _, row in df.iterrows():
        rating = row["Rating (kW)"]
        hours = row["Weekly Hrs"]
        thd = row["Distortion (THD_i)"]

        if thd > 5.0:
            loss_coefficient = (thd / 100.0) * 0.048
            annual_kwh_waste = rating * loss_coefficient * hours * 52
            total_annual_loss += annual_kwh_waste * utility_rate

    efficiency_score = max(70.0, 99.4 - (peak_thd * 0.45))
    downtime_liability = total_capacity_kw * 18.50 * (peak_thd / 10.0)

    return {
        "annual_loss_gbp": total_annual_loss,
        "efficiency_score": efficiency_score,
        "downtime_liability": downtime_liability,
        "peak_thd": peak_thd,
    }


def render_executive_view():
    """
    Renders the uncluttered, tabbed C-Suite Executive Command Hub.
    Maintains clean visual hierarchy using horizontal workspace nodes.
    """
    st.markdown("## 🏢 Executive Command Center: Portfolio Governance")
    st.markdown(
        "##### Enterprise Risk Modelling, Financial Loss Mapping, and Asset Longevity Engineering"
    )
    st.markdown("---")

    # ==========================================================================
    # 🗺️ PORTFOLIO CLIENT PROFILE ROUTER SELECTOR
    # ==========================================================================
    st.markdown("### 📋 Active Joint Venture Pipeline Profiles")
    active_client = st.selectbox(
        label="Select Target Enterprise Client Profile for Analysis:",
        options=[
            "Ammanford Alloys Ltd",
            "Swansea Silica Mining Operations",
            "Killan Farm Solar Array Hub",
        ],
    )

    df_active = load_client_portfolio_matrix(active_client)
    metrics = calculate_dynamic_loss_metrics(df_active, active_client)
    compliance = load_compliance_and_headroom_matrix(active_client)

    # Execute scrolling ticker injection
    render_cost_of_inaction_ticker(
        annual_losses_gbp=metrics["annual_loss_gbp"],
        tenant_colour="#D9272E" if metrics["peak_thd"] > 15.0 else "#F39C12",
    )

    st.write("")  # Clean vertical grouping space

    # ==========================================================================
    # 🗂️ DECOUPLED TABS TO PREVENT INTERFACE CLUTTER
    # ==========================================================================
    tab_financial, tab_compliance = st.tabs(
        ["💰 Financial Balance Sheet Matrix", "🔌 Grid Compliance & Network Headroom"]
    )

    # --------------------------------------------------------------------------
    # TAB 1: FINANCIAL RISK ANALYSIS
    # --------------------------------------------------------------------------
    with tab_financial:
        st.markdown("### 📊 Balance Sheet Financial Exposure Matrix")
        m_col1, m_col2, m_col3 = st.columns(3)

        with m_col1:
            st.metric(
                label="Annual Cost of Inaction (Systemic Waste)",
                value=f"£{metrics['annual_loss_gbp']:,.2f}",
                delta="Balance Sheet Erosion Factor",
                delta_color="inverse",
            )
            st.caption(
                "Direct leakage from electrical non-linear degradation and parasitic heat transformation."
            )

        with m_col2:
            projected_savings = metrics["annual_loss_gbp"] * 0.94
            st.metric(
                label="Projected Capital Preservation (Annual Savings)",
                value=f"£{projected_savings:,.2f}",
                delta="Optimised Target State",
                delta_color="normal",
            )
            st.caption(
                "Guaranteed cost recovery following deployment of localized active correction hardware."
            )

        with m_col3:
            st.metric(
                label="Estimated Asset Failure & Downtime Liability",
                value=f"£{metrics['downtime_liability']:,.2f}",
                help="Calculates financial exposure to uncoordinated protection trips and insulation failure.",
            )
            st.caption(
                "Insurance capital asset valuation at risk over a rolling 36-month operational cycle."
            )

        st.markdown("---")

        # AI Orchestration Module
        st.markdown("#### 🗣️ AI Boardroom Context Translation Node")
        if st.button("✨ Compile Strategic Advisory Brief"):
            with st.spinner(
                "Processing asset arrays and modeling balance sheet risk metrics..."
            ):
                peak_row = df_active.loc[df_active["Distortion (THD_i)"].idxmax()]
                telemetry_payload = {
                    "thd_i": peak_row["Distortion (THD_i)"],
                    "plant_location": peak_row["Plant Location"],
                    "weekly_hours": int(peak_row["Weekly Hrs"]),
                    "annual_losses_gbp": round(metrics["annual_loss_gbp"], 2),
                }

                ai_service = GeminiTranslationService()
                advisory_brief = ai_service.generate_boardroom_summary(
                    client_name=active_client,
                    asset_class=peak_row["Classification"],
                    telemetry=telemetry_payload,
                )
                st.markdown(advisory_brief)

    # --------------------------------------------------------------------------
    # TAB 2: GRID COMPLIANCE & CAPACITY HEADROOM
    # --------------------------------------------------------------------------
    with tab_compliance:
        st.markdown("### 📋 Statutory Grid Compliance & Liberated Capacity Scorecard")
        st.write(
            "Tracks Single Line Diagram auditable integrity, power factor capacity overheads, and DNO interconnection limits."
        )

        c_col1, c_col2 = st.columns(2)

        with c_col1:
            st.markdown("##### 📌 Physical Network Topology & Headroom")
            st.write(
                f"**Single Line Diagram (SLD) Status:** {compliance['sld_status']}"
            )
            st.write(
                f"**Power Factor Correction (PFC) Vector:** {compliance['pfc_status']}"
            )
            st.write(
                f"**Reclaimable Capacity Headroom:** `{compliance['unlocked_headroom']}`"
            )

        with c_col2:
            st.markdown(
                "##### 🔌 Distribution Network Operator (DNO) Statutory Boundaries"
            )
            st.info(
                f"**Current Interconnection Protocol:** \n\n {compliance['grid_compliance']}"
            )
            st.markdown("""
            * **G99 Mapping:** Required for all generation topologies over 16A/phase.
            * **G100 Enforcement:** Dictates active export-limitation protection frameworks at the grid boundary constraint node.
            """)

        st.markdown("---")
        st.markdown("##### ⚡ Active Infrastructure Waveform Efficiency Index")
        eff = metrics["efficiency_score"]
        st.progress(int(eff), text=f"Calculated Network Purity Score: {eff:.1f}%")

    # ==========================================================================
    # 📚 COMPREHENSIVE METHODOLOGY APPENDIX
    # ==========================================================================
    st.markdown("---")
    with st.expander(
        "📚 View Governing Methodology, Mathematical Equations & Audit Ledger"
    ):
        st.markdown("#### 🔢 Governing Mathematical Formulations")
        st.latex(
            r"W_{\text{annual}} = \sum_{n=1}^{N} P_{\text{rating}, n} \times \left( \frac{\text{THD}_{i, n}}{100} \right) \times \alpha \times T_{\text{operational}, n}"
        )
        st.latex(
            r"\text{Financial Bleed } (\mathfrak{L}) = W_{\text{annual}} \times \text{Utility Cost } (\text{GBP per kWh})"
        )

        st.markdown("""
        #### 🏦 Corporate Financial Parameters & Assumptions
        * Blended Energy Tariff: Configured dynamically between **£0.22/kWh and £0.24/kWh** based on DNO geographical market parameters.
        * Asset protection assumes Arrhenius lifecycles, where transformer winding insulation life contracts by 50% for every 10°C of unmitigated harmonic heat generation.
        """)
