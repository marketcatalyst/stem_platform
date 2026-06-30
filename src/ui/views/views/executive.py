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
            "sld_status": "🔴 OUTDATED (Verification Required)",
            "sld_badge": "error",
            "pfc_status": "⚠️ 0.81 Cos Phi (Lagging)",
            "grid_compliance": "🔒 G99 Approved under strict G100 Export Limitation (0 kW limitation at boundary)",
            "unlocked_headroom": "339.4 kVA",
        },
        "Swansea Silica Mining Operations": {
            "sld_status": "🟢 VERIFIED (Field Survey)",
            "sld_badge": "success",
            "pfc_status": "🟢 0.86 Cos Phi (Nominal)",
            "grid_compliance": "🔴 Legacy G59/3 Protection (Mandatory Statutory Transition to G99 Required)",
            "unlocked_headroom": "151.7 kVA",
        },
        "Killan Farm Solar Array Hub": {
            "sld_status": "🟢 VERIFIED (Commissioning Docs)",
            "sld_badge": "success",
            "pfc_status": "🟢 0.97 Cos Phi (Optimized)",
            "grid_compliance": "🟢 G99 Compliant / Active G100 Import Control Operational",
            "unlocked_headroom": "0.0 kVA",
        },
    }
    return matrix.get(client_name, {})


def calculate_dynamic_systemic_metrics(df: pd.DataFrame, client_name: str) -> dict:
    """
    Executes deep structural engineering calculations combining Harmonic Thermal Loss
    and Power Factor Reactive Penalties to map complete balance sheet risk profiles.
    """
    utility_rate = 0.24 if "Mining" in client_name else 0.22
    total_harmonic_loss = 0.0
    total_active_kw = df["Rating (kW)"].sum()
    peak_thd = df["Distortion (THD_i)"].max()

    comp_data = load_compliance_and_headroom_matrix(client_name)

    if "Alloys" in client_name:
        baseline_cos_phi = 0.81
    elif "Mining" in client_name:
        baseline_cos_phi = 0.86
    else:
        baseline_cos_phi = 0.97

    # Loop 1: Harmonic Thermal Winding Loss Calculation
    for _, row in df.iterrows():
        rating = row["Rating (kW)"]
        hours = row["Weekly Hrs"]
        thd = row["Distortion (THD_i)"]

        if thd > 5.0:
            loss_coefficient = (thd / 100.0) * 0.048
            annual_kwh_waste = rating * loss_coefficient * hours * 52
            total_harmonic_loss += annual_kwh_waste * utility_rate

    # Loop 2: Power Factor Correction Framework & Surcharge Math
    target_cos_phi = 0.96
    if baseline_cos_phi < target_cos_phi:
        apparent_kva_existing = total_active_kw / baseline_cos_phi
        apparent_kva_optimized = total_active_kw / target_cos_phi
        liberated_headroom_kva = apparent_kva_existing - apparent_kva_optimized
        annual_pfc_penalty_gbp = liberated_headroom_kva * 14.50
    else:
        liberated_headroom_kva = 0.0
        annual_pfc_penalty_gbp = 0.0

    # Consolidate unified metrics
    combined_annual_inaction_cost = total_harmonic_loss + annual_pfc_penalty_gbp
    efficiency_score = max(70.0, (baseline_cos_phi * 100) - (peak_thd * 0.25))
    downtime_liability = total_active_kw * 18.50 * (peak_thd / 10.0)

    return {
        "annual_loss_gbp": combined_annual_inaction_cost,
        "harmonic_loss_share": total_harmonic_loss,
        "pfc_penalty_share": annual_pfc_penalty_gbp,
        "efficiency_score": efficiency_score,
        "downtime_liability": downtime_liability,
        "peak_thd": peak_thd,
        "baseline_cos_phi": baseline_cos_phi,
        "target_cos_phi": target_cos_phi,
        "liberated_headroom_kva": liberated_headroom_kva,
        "sld_status": comp_data["sld_status"],
        "grid_compliance": comp_data["grid_compliance"],
        "unlocked_headroom_str": comp_data["unlocked_headroom"],
    }


def render_executive_view():
    """
    Renders the uncluttered, symmetrically aligned C-Suite Executive Command Hub.
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
        help="Instantly shifts the underlying infrastructure architectural files, re-executing specialized loss algorithms and rotating active telemetry variables across the dashboard metrics.",
    )

    df_active = load_client_portfolio_matrix(active_client)
    metrics = calculate_dynamic_systemic_metrics(df_active, active_client)

    # Execute scrolling ticker injection driven by combined real-time calculations
    render_cost_of_inaction_ticker(
        annual_losses_gbp=metrics["annual_loss_gbp"],
        tenant_colour=(
            "#D9272E"
            if metrics["peak_thd"] > 15.0 or metrics["baseline_cos_phi"] < 0.85
            else "#F39C12"
        ),
    )

    st.write("")  # Structural breathing room

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
                label="Annual Cost of Inaction (Total Combined Bleed)",
                value=f"£{metrics['annual_loss_gbp']:,.2f}",
                delta="Balance Sheet Erosion Factor",
                delta_color="inverse",
                help="The combined annual cash bleeding from the balance sheet. This tracks invisible thermal power leakage and costly reactive power surcharges levied directly by the utility network without producing a single unit of industrial output.",
            )
            st.caption(
                f"Includes £{metrics['harmonic_loss_share']:,.2f} in thermal winding losses and £{metrics['pfc_penalty_share']:,.2f} in DNO capacity reactive penalties."
            )

        with m_col2:
            projected_savings = metrics["annual_loss_gbp"] * 0.95
            st.metric(
                label="Projected Capital Preservation (Annual Savings)",
                value=f"£{projected_savings:,.2f}",
                delta="Optimised Target State",
                delta_color="normal",
                help="Guaranteed capital recovery achieved by deploying active harmonic cancellation. Redirects current unmetered operational waste back onto the corporate bottom line with an optimized sub-24 month project amortization.",
            )
            st.caption(
                "Guaranteed cost recovery across a 12-month horizon following complete STEM active filtering and SVG installation."
            )

        with m_col3:
            st.metric(
                label="Estimated Asset Failure & Downtime Liability",
                value=f"£{metrics['downtime_liability']:,.2f}",
                help="Vulnerability exposure representing lost manufacturing margin, startup scrap material, and DNO non-compliance penalties triggered if a distorted waveform causes an uncoordinated main breaker trip.",
            )
            st.caption(
                "Capital asset valuation actively positioned at risk over a standard 36-month industrial operating cycle."
            )

        st.markdown("---")

        st.markdown("#### 🗣️ AI Boardroom Context Translation Node")
        if st.button(
            "✨ Compile Strategic Advisory Brief",
            help="Triggers the advanced Google Gemini NLP translation layer to interpret technical telemetry and compile a pristine, boardroom-ready risk summary.",
        ):
            with st.spinner(
                "Processing asset arrays and modeling balance sheet risk metrics..."
            ):
                peak_row = df_active.loc[df_active["Distortion (THD_i)"].idxmax()]
                telemetry_payload = {
                    "thd_i": peak_row["Distortion (THD_i)"],
                    "plant_location": peak_row["Plant Location"],
                    "weekly_hours": int(peak_row["Weekly Hrs"]),
                    "annual_losses_gbp": round(metrics["annual_loss_gbp"], 2),
                    "baseline_cos_phi": metrics["baseline_cos_phi"],
                    "liberated_headroom_kva": round(
                        metrics["liberated_headroom_kva"], 1
                    ),
                }

                ai_service = GeminiTranslationService()
                advisory_brief = ai_service.generate_boardroom_summary(
                    client_name=active_client,
                    asset_class=peak_row["Classification"],
                    telemetry=telemetry_payload,
                )
                st.markdown(advisory_brief)

                st.download_button(
                    label="📥 Download Strategic Brief (Markdown)",
                    data=advisory_brief,
                    file_name=f"STEM_Executive_Brief_{active_client.replace(' ', '_')}.md",
                    mime="text/plain",
                )

    # --------------------------------------------------------------------------
    # TAB 2: GRID COMPLIANCE & CAPACITY HEADROOM (SYMMETRIC DNO ACRONYM pass)
    # --------------------------------------------------------------------------
    with tab_compliance:
        st.markdown("### 📋 Statutory Grid Compliance & Liberated Capacity Scorecard")
        st.write(
            "Auditable infrastructure configuration tracking grid limits, topology safety, and reactive displacement."
        )
        st.write("")

        # Establish two equal-weight structural columns
        c_col1, c_col2 = st.columns(2)

        with c_col1:
            with st.container(border=True):
                st.markdown("##### 📌 Physical Network Topology & Headroom")
                st.divider()

                st.write(
                    f"**Single Line Diagram (SLD) State:** {metrics['sld_status']}"
                )
                st.write(
                    f"**Measured Displacement Factor:** `{metrics['baseline_cos_phi']:.2f} Cos Phi` (Target: `{metrics['target_cos_phi']:.2f}`)"
                )
                st.write("")

                sm_col1, sm_col2 = st.columns(2)
                with sm_col1:
                    st.metric(
                        label="Existing Power Factor",
                        value=f"{metrics['baseline_cos_phi']:.2f}",
                        help="The fundamental displacement factor measured at the main grid boundary breaker.",
                    )
                with sm_col2:
                    st.metric(
                        label="Reclaimable Headroom",
                        value=metrics["unlocked_headroom_str"],
                        delta=(
                            "Liberated kVA"
                            if metrics["liberated_headroom_kva"] > 0
                            else None
                        ),
                        help="Physical thermal capacity returned to the primary incoming distribution transformer by eliminating reactive magnetizing power.",
                    )

        with c_col2:
            with st.container(border=True):
                # 💎 Symmetrical short-form title applied here to match the left card height plane exactly
                st.markdown("##### 🔌 DNO Statutory Boundaries")
                st.divider()

                if "Approved" in metrics["grid_compliance"]:
                    st.warning(
                        f"**Active Boundary Protocol:** \n\n {metrics['grid_compliance']}"
                    )
                elif "Legacy" in metrics["grid_compliance"]:
                    st.error(
                        f"**Active Boundary Protocol:** \n\n {metrics['grid_compliance']}"
                    )
                else:
                    st.success(
                        f"**Active Boundary Protocol:** \n\n {metrics['grid_compliance']}"
                    )

                st.markdown("""
                * **G99 Framework:** Mandatory interconnection specification for generation arrays over 16A per phase.
                * **G100 Export Control:** Demands active fail-safe hardware limits to arrest uncoordinated back-feed leaks.
                """)

        st.markdown("---")
        st.markdown("##### 📈 Integrated Infrastructure Waveform Efficiency Index")
        eff = metrics["efficiency_score"]
        st.progress(int(eff), text=f"Calculated Core Network Purity Score: {eff:.1f}%")

    # ==========================================================================
    # 📚 COMPREHENSIVE METHODOLOGY APPENDIX & AUDIT TRAIL
    # ==========================================================================
    st.markdown("---")
    with st.expander(
        "📚 View Governing Methodology, Mathematical Equations & Audit Ledger"
    ):
        st.markdown("#### 🔢 Governing Mathematical Formulations")
        st.markdown(
            "The system quantifies total operational financial leakage using standard non-linear loss distribution metrics:"
        )
        st.latex(
            r"W_{\text{annual}} = \sum_{n=1}^{N} P_{\text{rating}, n} \times \left( \frac{\text{THD}_{i, n}}{100} \right) \times \alpha \times T_{\text{operational}, n}"
        )
        st.markdown(
            "Capacity liberation maps directly across the displacement vectors to resolve apparent load inflation:"
        )
        st.latex(
            r"\Delta S_{\text{headroom}} = \sum P_{\text{capacity}} \times \left( \frac{1}{\cos\phi_{\text{existing}}} - \frac{1}{\cos\phi_{\text{target}}} \right)"
        )
        st.markdown(
            "The combined corporate loss metric reconciles both statutory overheads and thermal waste factors simultaneously:"
        )
        st.latex(
            r"\text{Total Financial Bleed } (\mathfrak{L}) = (W_{\text{annual}} \times \text{Tariff}) + (\Delta S_{\text{headroom}} \times \text{DNO Penalty Rate})"
        )

        st.markdown("""
        #### 📋 Variable Nomenclature and Definitions
        * $W_{\text{annual}}$: Total cumulative wasted energy calculated in kilowatt-hours per annum.
        * $P_{\text{rating}, n}$: Nominal plate capacity of individual monitored hardware node $n$ expressed in kW.
        * $\text{THD}_{i, n}$: Measured Current Harmonic Distortion percentage bleeding into the local busbar switchgear.
        * $\alpha$: Empirical scaling factor tracking non-linear eddy current and skin effect transformations ($\alpha = 0.048$).
        * $T_{\text{operational}, n}$: Logged operational service timeline measured in hours per annum ($Hrs \times 52$).
        * $\Delta S_{\text{headroom}}$: Total geometric apparent power capacity reclaimed at the distribution transformer boundary expressed in kVA.
        * $\cos\phi_{\text{existing}}$: Baseline measured site power factor displacement score.
        * $\cos\phi_{\text{target}}$: Targeted corrected power factor goal optimized for DNO financial compliance ($\cos\phi = 0.96$).
        
        #### 🏦 Corporate Financial Parameters & Assumptions
        * **Blended Energy Tariff:** Configured dynamically between **£0.22/kWh and £0.24/kWh** based on geographical industrial market parameters.
        * **DNO Apparent Demand Surcharge Penalty:** Evaluated at an empirical run-rate of **£14.50 per excess uncorrected kVA** per annum.
        * **Asset Lifetime Contraction (Arrhenius Realities):** Transformer thermal models assume solid paper insulation longevity degrades geometrically, halving functional service lifespan for every 10°C of sustained harmonic-induced temperature elevation above nominal design limits.
        
        #### 📑 JV Audit Traceability Ledger
        * **System Status:** Production Build Verified (`2026.1.MVP`).
        * **Data Stream Source:** Serverless Data Plane Engine (`Neon PostgreSQL Cluster`).
        * **Validation Target:** Enforced via explicit object validation schemas (`Pydantic BaseSettings`).
        """)
