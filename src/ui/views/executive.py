import streamlit as st
import pandas as pd
from src.ui.components.gauges import render_efficiency_ghost_dial
from src.ui.components.tickers import render_cost_of_inaction_ticker
from src.modules.finance_engine.arrhenius import calculate_thermal_acceleration_factor
from src.modules.finance_engine.accounting import calculate_balance_sheet_optimisation
from src.modules.gemini_nlp.service import GeminiTranslationService


def render_executive_view():
    """
    Renders the Consultative C-suite Command view layer.
    Enables JV partners to project holistic enterprise risk vectors, straight-line
    asset depreciation, sub-cycle downtime losses, and turnkey implementation CapEx/ROI metrics.
    Includes an interactive, auditable math and assumptions verification ledger for skeptical executives.
    """
    st.subheader("📊 STEM C-Suite Command Hub & Capital Presentation Matrix")
    st.markdown(
        "This strategic cockpit models macro enterprise risk, turnkey implementation capital expenditure, "
        "and multi-year payback matrices across active joint venture corporate accounts."
    )
    st.divider()

    # ==========================================================================
    # 📂 1. ACTIVE PORTFOLIO CLIENT PROFILE CONTEXT MATRIX
    # ==========================================================================
    st.markdown("#### 📂 Active Client Account Workspace")
    client_name = st.selectbox(
        "Select Target Client Portfolio Profile",
        [
            "Ammanford Alloys Ltd",
            "Swansea Silica Mining Operations",
            "Killan Farm Solar Array Hub",
        ],
    )

    # Expanded lookalike profiles including Turnkey CapEx, Annual OpEx, and WACC thresholds
    client_profiles = {
        "Ammanford Alloys Ltd": {
            "asset_class": "Heavy Arc Furnace Substation",
            "asset_value": 150000.00,
            "nominal_life": 10.0,
            "stress_factor": 1.35,
            "current_eff": 72.4,
            "opt_eff": 96.8,
            "annual_events": 4,
            "scrap_per_event": 4500.00,
            "penalty_per_event": 2500.00,
            "reset_hours": 3.5,
            "labor_rate": 2000.00,
            "proposed_solution": "Active Harmonic Filtering Matrix + 250kW BESS-UPS Shield",
            "turnkey_capex": 95000.00,
            "annual_opex": 2500.00,
            "wacc_pct": 8.0,
            "telemetry_pf": {"cos_phi": 0.72, "thd_i": 38.0, "phase_imbalance": True},
        },
        "Swansea Silica Mining Operations": {
            "asset_class": "High-Voltage Induction Processing Plant",
            "asset_value": 280000.00,
            "nominal_life": 15.0,
            "stress_factor": 1.12,
            "current_eff": 84.1,
            "opt_eff": 97.2,
            "annual_events": 2,
            "scrap_per_event": 12000.00,
            "penalty_per_event": 5000.00,
            "reset_hours": 5.0,
            "labor_rate": 1500.00,
            "proposed_solution": "Dynamic Power Factor Correction + Heavy-Duty Substation Re-Earthing",
            "turnkey_capex": 135000.00,
            "annual_opex": 3800.00,
            "wacc_pct": 7.5,
            "telemetry_pf": {"cos_phi": 0.81, "thd_i": 18.0, "phase_imbalance": False},
        },
        "Killan Farm Solar Array Hub": {
            "asset_class": "1MW Solar Array & Battery Storage Matrix",
            "asset_value": 450000.00,
            "nominal_life": 20.0,
            "stress_factor": 1.48,
            "current_eff": 61.5,
            "opt_eff": 98.5,
            "annual_events": 6,
            "scrap_per_event": 1500.00,
            "penalty_per_event": 8000.00,
            "reset_hours": 2.0,
            "labor_rate": 500.00,
            "proposed_solution": "Coordinated 500kW/1MWh BESS Upgrade & Phase Balancing Networks",
            "turnkey_capex": 240000.00,
            "annual_opex": 6000.00,
            "wacc_pct": 8.5,
            "telemetry_pf": {"cos_phi": 0.65, "thd_i": 42.0, "phase_imbalance": True},
        },
    }

    # Extract currently selected corporate profile parameters
    cp = client_profiles[client_name]

    # Calculate operational downtime insurance metrics
    labor_loss_per_event = cp["reset_hours"] * cp["labor_rate"]
    total_single_event_loss = (
        cp["scrap_per_event"] + cp["penalty_per_event"] + labor_loss_per_event
    )
    total_annual_downtime_liability = cp["annual_events"] * total_single_event_loss

    # Calculate long-term physical asset degradation metrics
    accel_factor = calculate_thermal_acceleration_factor(cp["stress_factor"])
    fin_model = calculate_balance_sheet_optimisation(
        cp["asset_value"], cp["nominal_life"], accel_factor
    )
    annual_depreciation_bleed = fin_model["annual_balance_sheet_savings_gbp"]

    # Summate total annual corporate leak for the combined ticker tape display
    total_combined_annual_bleed = (
        total_annual_downtime_liability + annual_depreciation_bleed
    )

    # Trigger rolling financial loss ticker tape showing combined systemic vulnerability
    render_cost_of_inaction_ticker(
        total_combined_annual_bleed, st.session_state.get("primary_colour", "#FF3333")
    )
    st.divider()

    # ==========================================================================
    # 📊 2. VISUALIZATION AND TRI-PRONGED RISK & INVESTMENT GRID
    # ==========================================================================
    col_chart, col_metrics = st.columns([1, 1])

    with col_chart:
        fig_power = render_efficiency_ghost_dial(
            current_efficiency_pct=cp["current_eff"],
            optimized_ceiling_pct=cp["opt_eff"],
            dial_title=f"{client_name} | Total System Efficiency Profile",
            accent_colour=st.session_state.get("primary_colour", "#FF3333"),
        )
        # Fixed: Converted deprecated parameter to width="stretch" to ensure 2026 specification compliance
        st.plotly_chart(fig_power, width="stretch")

    with col_metrics:
        st.markdown("### 🧮 Integrated Financial Impact Analysis")

        # Tri-pronged tab layout mapping out Risk Exposure vs Implementation Costs
        tab_capital, tab_operations, tab_investment = st.tabs(
            [
                "🛡️ Pillar 1: Capital Protection",
                "🤖 Pillar 2: Process Insurance",
                "💰 Pillar 3: Turnkey Investment",
            ]
        )

        with tab_capital:
            st.metric(
                label="🔒 Projected Annual Balance-Sheet Depreciation Savings",
                value=f"£{annual_depreciation_bleed:,.2f} p.a.",
                delta=f"Life Restored: {fin_model['optimised_useful_life_years']} Years",
            )
            st.markdown(
                f"**Asset Degradation Analysis:** Unmitigated current harmonics are elevating internal hot-spot "
                f"winding temperatures within the **{cp['asset_class']}**, compressing the useful economic "
                f"lifespan of this capital asset down to **{fin_model['degraded_useful_life_years']:.1f} years** "
                f"(vs. a nominal {cp['nominal_life']} year design envelope)."
            )

        with tab_operations:
            st.metric(
                label="🚨 Unmitigated Annual Risk Exposure (ARE)",
                value=f"£{total_annual_downtime_liability:,.2f} p.a.",
                delta=f"Cost Per Event: £{total_single_event_loss:,.2f}",
                delta_color="inverse",
            )
            st.markdown(
                f"**Continuous Production Risk Analysis:** Sensitive digital PLC brains and robotic automation layers "
                f"are vulnerable to transient voltage sags. This facility averages **{cp['annual_events']} dropout events per year**. "
                f"Each single trip triggers a **{cp['reset_hours']} hour uncoordinated recovery process**, racking up "
                f"fines, idle shift labor overheads, and immediate scrap materials."
            )

        with tab_investment:
            # Net annual operational savings accounts for solution maintenance OpEx overheads
            net_annual_savings = total_combined_annual_bleed - cp["annual_opex"]
            simple_payback_years = cp["turnkey_capex"] / net_annual_savings

            # Simple lifetime ROI metric project over standard 15-year infrastructure window
            system_lifetime_years = 15
            total_lifetime_net_return = (
                net_annual_savings * system_lifetime_years
            ) - cp["turnkey_capex"]
            roi_percentage = (total_lifetime_net_return / cp["turnkey_capex"]) * 100

            st.metric(
                label="💰 Turnkey Implementation Investment (CapEx)",
                value=f"£{cp['turnkey_capex']:,.2f}",
                delta=f"Simple Payback: {simple_payback_years:.1f} Years",
                delta_color="normal",
            )

            st.markdown(
                f"**Proposed JV Engineering Framework:** `{cp['proposed_solution']}`"
            )

            col_inv1, col_inv2 = st.columns(2)
            with col_inv1:
                st.caption("🔧 Estimated Engineering OpEx")
                st.markdown(f"**£{cp['annual_opex']:,.2f} / annum**")
                st.caption("📈 Projected 15-Yr Net Yield")
                st.markdown(f"**£{total_lifetime_net_return:,.2f}**")
            with col_inv2:
                st.caption("🎯 Projected Solution ROI")
                st.markdown(f"**{roi_percentage:.1f} %**")
                st.caption("🏢 Client Corporate WACC")
                st.markdown(f"**{cp['wacc_pct']}% Cost of Capital**")

    st.divider()

    # ==========================================================================
    # 🧠 3. CONTEXTUAL AI BOARDROOM TRANSLATION LAYER
    # ==========================================================================
    st.write("### 🧠 STEM Platform Boardroom Translation Node")
    st.markdown(
        f"Select a captured engineering vulnerability below to instantly generate an authoritative, "
        f"executive-ready advisory brief customized for the **{client_name}** board of directors."
    )

    anomaly_selection = st.selectbox(
        "Select Active Telemetry Anomaly to Translate",
        [
            "Select an anomaly to translate...",
            f"Severe Voltage Sags & Automated Process Dropout Vulnerability (ARE: £{total_annual_downtime_liability:,.2f})",
            f"Elevated Current Harmonic Waveform Distortion (THD_i = {cp['telemetry_pf']['thd_i']}%)",
            f"Poor Lagging Displacement Power Factor (Cos Phi = {cp['telemetry_pf']['cos_phi']})",
        ],
    )

    if anomaly_selection != "Select an anomaly to translate...":
        if "Voltage Sags" in anomaly_selection:
            selected_asset = "Automated Production Control Line & Robotics Array"
            payload = {
                "annual_events": cp["annual_events"],
                "cost_per_event": total_single_event_loss,
                "proposed_solution": cp["proposed_solution"],
                "turnkey_capex": cp["turnkey_capex"],
                "payback_years": simple_payback_years,
            }
        elif "Harmonic" in anomaly_selection:
            selected_asset = cp["asset_class"]
            payload = {
                "cos_phi": cp["telemetry_pf"]["cos_phi"],
                "thd_i": cp["telemetry_pf"]["thd_i"],
                "turnkey_capex": cp["turnkey_capex"],
            }
        else:
            selected_asset = "Main Incoming Substation Switchgear"
            payload = {
                "cos_phi": cp["telemetry_pf"]["cos_phi"],
                "reactive_penalty": True,
            }

        with st.spinner(
            f"Compiling consultative boardroom brief for {client_name} via Gemini..."
        ):
            ai_service = GeminiTranslationService()
            summary_markdown = ai_service.generate_boardroom_summary(
                client_name=client_name, asset_class=selected_asset, telemetry=payload
            )
            st.info(summary_markdown)

    st.divider()

    # ==========================================================================
    # 📚 4. TRANSPARENT METHODOLOGY & AUDITABLE APPENDIX
    # ==========================================================================
    with st.expander(
        "📚 Appendix: Technical Methodologies, Governing Equations & Financial Assumptions"
    ):
        st.markdown("### 🏛️ STEM Platform Audit Traceability Ledger")
        st.markdown(
            "To ensure absolute corporate accountability and validation, the calculations running "
            "within the STEM framework are governed by standardized international physics constraints "
            "and straight-line capital accounting protocols."
        )

        st.markdown("#### 1. Core Analytical Formulations")

        st.latex(r"I_{RMS} = I_1 \sqrt{1 + \left(\frac{THD_i}{100}\right)^2}")
        st.caption(
            "Equation 1.1: Root-Mean-Square current inflation as a direct vector function of Total Harmonic Distortion."
        )

        st.latex(
            r"F_{AA} = \exp\left( \frac{15000}{110 + 273.15} - \frac{15000}{\Theta_H + 273.15} \right)"
        )
        st.caption(
            "Equation 1.2: IEEE C57.91 Arrhenius chemical kinetics formula mapping insulation degradation vs. thermal winding spikes."
        )

        st.latex(r"\Delta D = (F_{AA} - 1) \cdot \frac{V_A}{L_N}")
        st.caption(
            "Equation 1.3: Annualized balance-sheet depreciation bleed representing accelerated asset capital erosion."
        )

        st.latex(
            r"ARE = N_{events} \cdot \left[ C_{scrap} + C_{penalty} + (T_{reset} \cdot R_{labor}) \right]"
        )
        st.caption(
            "Equation 1.4: Unmitigated Process Insurance Annual Risk Exposure modeling cumulative manufacturing automation dropouts."
        )

        st.markdown("---")

        # SKEPTICAL MD EXPLICIT AUDIT PASS: Dynamic worked validation breakdown
        st.markdown(f"#### 🔍 Ticker Validation Ledger: {client_name}")
        st.markdown(
            f"This auditable verification profile outlines exactly how the live rolling ticker value of "
            f"**£{total_combined_annual_bleed:,.2f} p.a.** was calculated for the **{client_name}** infrastructure portfolio."
        )

        audit_steps = [
            {
                "Audit Step Identification": "Step 1: Calculate Asset Depreciation Bleed (Pillar 1)",
                "Calculated Operational Sub-Vector": f"£{annual_depreciation_bleed:,.2f} p.a.",
                "Underlying Accounting / Physics Derivation": f"Transformer baseline replacement capital footprint (£{cp['asset_value']:,.2f}) compressed by an Arrhenius thermal degradation acceleration factor of {accel_factor:.2f}x.",
            },
            {
                "Audit Step Identification": "Step 2.1: Material Scrap Loss per Trip",
                "Calculated Operational Sub-Vector": f"£{cp['scrap_per_event']:,.2f}",
                "Underlying Accounting / Physics Derivation": "WIP components lost mid-cycle + raw chemical/line feed purge costs incurred during uncoordinated line shutdown.",
            },
            {
                "Audit Step Identification": "Step 2.2: Supply Chain Contractual Fines per Trip",
                "Calculated Operational Sub-Vector": f"£{cp['penalty_per_event']:,.2f}",
                "Underlying Accounting / Physics Derivation": "Just-In-Time delivery non-conformance penalties levied by downstream buyers + expedited emergency transport haulage.",
            },
            {
                "Audit Step Identification": "Step 2.3: Idle Labour Burn-Rate per Trip",
                "Calculated Operational Sub-Vector": f"£{labor_loss_per_event:,.2f}",
                "Underlying Accounting / Physics Derivation": f"Factory floor workforce standing completely idle during a prolonged mechanical recovery/homing window ({cp['reset_hours']} hours @ £{cp['labor_rate']:,.2f}/hr).",
            },
            {
                "Audit Step Identification": "Step 3: Aggregate Single Dropout Financial Impact",
                "Calculated Operational Sub-Vector": f"£{total_single_event_loss:,.2f} / event",
                "Underlying Accounting / Physics Derivation": "Summation of Step 2.1 + Step 2.2 + Step 2.3. The true cost of a single unmitigated voltage sag event.",
            },
            {
                "Audit Step Identification": "Step 4: Annualised Process Insurance Liability (Pillar 2)",
                "Calculated Operational Sub-Vector": f"£{total_annual_downtime_liability:,.2f} p.a.",
                "Underlying Accounting / Physics Derivation": f"Step 3 multiplied by the historical grid frequency threshold ({cp['annual_events']} unmitigated brown-out drops per annum).",
            },
            {
                "Audit Step Identification": "Step 5: Master Active Ticker Value (Cost of Inaction)",
                "Calculated Operational Sub-Vector": f"£{total_combined_annual_bleed:,.2f} p.a.",
                "Underlying Accounting / Physics Derivation": "Step 1 (Capital Asset Preservation Bleed) added directly to Step 4 (Process Insurance Vulnerability). Total active enterprise capital bleed.",
            },
        ]
        st.dataframe(pd.DataFrame(audit_steps), width="stretch", hide_index=True)

        st.markdown("---")
        st.markdown("#### 3. Governing Engineering & Financial Constants")

        structure_data = {
            "Core Parameter Group": [
                "Baseline Transformer Hot-Spot Boundary",
                "Arrhenius Material Activation Constant",
                "Sub-Cycle BESS Intercept Efficiency (η)",
                "Turnkey System Useful Lifespan",
                "Standard Industrial Cost of Capital (WACC)",
            ],
            "Fixed Assumption Baseline": [
                "110 °C",
                "15,000",
                "99.0 %",
                "15 Years",
                "7.5% - 8.5% (Client Synchronized)",
            ],
            "Regulatory Reference / Auditable Justification": [
                "IEEE C57.91 thermal standard boundary for solid polymer winding stabilization.",
                "Empirical molecular kinetic energy constant required for paper insulation decay.",
                "Operational probability threshold of active sub-4ms micro-static transfer switchgear.",
                "Amortization and economic operational cycle limits for utility-grade LFP cell chemistry.",
                "Standard capital hurdle tracking parameters for UK industrial manufacturing networks.",
            ],
        }
        st.table(pd.DataFrame(structure_data))
