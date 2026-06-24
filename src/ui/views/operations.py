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


def load_ammanford_alloys_dataset() -> pd.DataFrame:
    """
    Constructs and returns the comprehensive, auditable 18-asset operational matrix
    for Ammanford Alloys Ltd.
    """
    raw_data = [
        {
            "Asset Tag": "TX-01-SUB-A",
            "Plant Location": "Substation 1 Main Bay",
            "Classification": "Main Distribution Transformer",
            "Rating (kW)": 1500,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 8.5,
        },
        {
            "Asset Tag": "VSD-04-LINE-3",
            "Plant Location": "Production Line 3 East",
            "Classification": "Variable Speed Drive (VSD)",
            "Rating (kW)": 75,
            "Weekly Hrs": 40,
            "Distortion (THD_i)": 38.0,
        },
        {
            "Asset Tag": "MOT-12-CRUSHER",
            "Plant Location": "Primary Feed Intake",
            "Classification": "Large Induction Motor",
            "Rating (kW)": 250,
            "Weekly Hrs": 65,
            "Distortion (THD_i)": 5.2,
        },
        {
            "Asset Tag": "ARC-01-MELT",
            "Plant Location": "Casting Hall Furnace Node",
            "Classification": "Arc Furnace Plant",
            "Rating (kW)": 3500,
            "Weekly Hrs": 24,
            "Distortion (THD_i)": 22.1,
        },
        {
            "Asset Tag": "TX-02-SUB-B",
            "Plant Location": "Substation 2 Rolling Mill",
            "Classification": "Auxiliary Step-Down Transformer",
            "Rating (kW)": 750,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 4.2,
        },
        {
            "Asset Tag": "VSD-01-PUMP",
            "Plant Location": "Cooling Tower Array",
            "Classification": "Main Feed Pump VSD",
            "Rating (kW)": 110,
            "Weekly Hrs": 120,
            "Distortion (THD_i)": 32.5,
        },
        {
            "Asset Tag": "MOT-02-FAN",
            "Plant Location": "Baghouse Extractor Node",
            "Classification": "Heavy Ventilation Fan",
            "Rating (kW)": 132,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 6.8,
        },
        {
            "Asset Tag": "ARC-02-LADLE",
            "Plant Location": "Refining Station 2",
            "Classification": "Ladle Metallurgy Furnace",
            "Rating (kW)": 1200,
            "Weekly Hrs": 48,
            "Distortion (THD_i)": 16.4,
        },
        {
            "Asset Tag": "CAP-01-BANK",
            "Plant Location": "Main Incoming Switchroom",
            "Classification": "Power Factor Correction Bank",
            "Rating (kW)": 400,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 1.2,
        },
        {
            "Asset Tag": "VSD-02-COMP",
            "Plant Location": "Utility Compressor House",
            "Classification": "Screw Compressor VSD",
            "Rating (kW)": 90,
            "Weekly Hrs": 80,
            "Distortion (THD_i)": 28.0,
        },
        {
            "Asset Tag": "MOT-05-CONV",
            "Plant Location": "Discharge Crane Feed",
            "Classification": "Main Conveyor Drive",
            "Rating (kW)": 45,
            "Weekly Hrs": 110,
            "Distortion (THD_i)": 4.5,
        },
        {
            "Asset Tag": "TX-03-OFFICE",
            "Plant Location": "Administration Block",
            "Classification": "Commercial Step-Down Transformer",
            "Rating (kW)": 200,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 2.1,
        },
        {
            "Asset Tag": "LIGHT-01-LED",
            "Plant Location": "Plant-Wide High-Bay Arena",
            "Classification": "Industrial LED Lighting Network",
            "Rating (kW)": 60,
            "Weekly Hrs": 120,
            "Distortion (THD_i)": 14.0,
        },
        {
            "Asset Tag": "VSD-03-CHILL",
            "Plant Location": "Ancillary Plant Room",
            "Classification": "Process Chiller VSD",
            "Rating (kW)": 160,
            "Weekly Hrs": 90,
            "Distortion (THD_i)": 24.5,
        },
        {
            "Asset Tag": "MOT-08-HYD",
            "Plant Location": "Baling Press Fluid Node",
            "Classification": "Hydraulic Power Pack",
            "Rating (kW)": 75,
            "Weekly Hrs": 60,
            "Distortion (THD_i)": 3.8,
        },
        {
            "Asset Tag": "UPS-01-SERVER",
            "Plant Location": "Central SCADA Control Room",
            "Classification": "Double-Conversion System UPS",
            "Rating (kW)": 30,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 11.5,
        },
        {
            "Asset Tag": "VSD-05-BLOW",
            "Plant Location": "Furnace Pre-Heater Stack",
            "Classification": "Combustion Air Blower VSD",
            "Rating (kW)": 55,
            "Weekly Hrs": 100,
            "Distortion (THD_i)": 34.0,
        },
        {
            "Asset Tag": "MOT-14-PUMP",
            "Plant Location": "Slurry Treatment Pool",
            "Classification": "Effluent Circulation Pump",
            "Rating (kW)": 90,
            "Weekly Hrs": 168,
            "Distortion (THD_i)": 5.0,
        },
    ]
    return pd.DataFrame(raw_data)


def load_client_operational_matrix(client_name: str) -> pd.DataFrame:
    """
    Data routing engine aligning the operations grid with the globally selected portfolio client.
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


def render_operations_view():
    """
    Renders the expanded, interactive Operations Management viewport.
    Features dynamic client dataset routing, asset filters, and line-item loss analysis.
    """
    st.markdown("## ⚙️ Operations Management: Digital Twin Telemetry")
    st.markdown(
        "##### Real-Time Asset Load Profiling, Waveform Anomalies, and Line Item Thermal Loss Audits"
    )
    st.markdown("---")

    # ==========================================================================
    # 🗺️ SYNCHRONIZED CLIENT SELECTION ROUTER
    # ==========================================================================
    st.markdown("### 📋 Portfolio Engineering Target")
    active_client = st.selectbox(
        label="Select Site Location Framework for Operational Review:",
        options=[
            "Ammanford Alloys Ltd",
            "Swansea Silica Mining Operations",
            "Killan Farm Solar Array Hub",
        ],
        key="ops_client_selector",
    )

    # Load data dynamically based on selection state
    df_raw = load_client_operational_matrix(active_client)
    utility_rate = 0.24 if "Mining" in active_client else 0.22

    # ==========================================================================
    # 🧮 LINE-BY-LINE ASSET LOSS ANALYTICS INJECTION
    # ==========================================================================
    # We enrich the dataframe with real-time calculated engineering parameters
    df_enriched = df_raw.copy()

    # Calculate annual kWh wasted per individual asset node
    df_enriched["Annual Waste (kWh)"] = df_enriched.apply(
        lambda r: (
            r["Rating (kW)"]
            * ((r["Distortion (THD_i)"] / 100.0) * 0.048)
            * r["Weekly Hrs"]
            * 52
            if r["Distortion (THD_i)"] > 5.0
            else 0.0
        ),
        axis=1,
    )
    # Calculate financial leakage per asset
    df_enriched["Financial Leakage"] = df_enriched["Annual Waste (kWh)"] * utility_rate

    # Calculate remaining insulation asset lifespan factor based on harmonic core heating models
    df_enriched["Insulation Life Expectancy"] = df_enriched["Distortion (THD_i)"].apply(
        lambda x: max(30, round(100.0 - (x * 1.8))) if x > 5.0 else 100
    )

    # ==========================================================================
    # 🎛️ DYNAMIC SUMMARY METRIC CARDS
    # ==========================================================================
    total_registered_nodes = df_enriched.shape[0]
    calculated_peak_demand = (
        df_enriched[df_enriched["Weekly Hrs"] > 100]["Rating (kW)"].sum() * 0.65
    ) + (
        df_enriched[
            df_enriched["Classification"].str.contains(
                "Arc Furnace|Ladle|Battery|Central"
            )
        ]["Rating (kW)"].max()
        * 0.85
        if not df_enriched[
            df_enriched["Classification"].str.contains(
                "Arc Furnace|Ladle|Battery|Central"
            )
        ].empty
        else 200.0
    )
    max_systemic_thd = df_enriched["Distortion (THD_i)"].max()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Active Surveyed Nodes",
            value=f"{total_registered_nodes} Registered Assets",
            help="The total population of physical assets actively mapped inside the site's digital twin. Establishes the foundational structural integrity needed to track and isolate rogue harmonic emitters.",
        )

    with col2:
        st.metric(
            label="Measured Coincident Peak Demand",
            value=f"{calculated_peak_demand:,.1f} kW",
            help="The true maximum simultaneous electrical load drawn across the network boundary. By analyzing engineering diversity factors rather than basic nameplate summation, the model prevents the massive capital expense of over-specifying new transformer gear.",
        )

    with col3:
        status_indicator = (
            "🔴 Critical Value:" if max_systemic_thd > 15.0 else " 🟢 Within Limits:"
        )
        st.metric(
            label="Primary Systemic State",
            value=f"{max_systemic_thd:.1f}% THD_i Max",
            delta=(
                f"{status_indicator} Waveform Distortion"
                if max_systemic_thd > 8.0
                else "Stable Network Geometry"
            ),
            delta_color="inverse" if max_systemic_thd > 8.0 else "normal",
            help="The peak Current Harmonic Distortion score registered across the fleet. Unmitigated values above the IEEE 519 5% boundary inject parasitic heat into asset windings, accelerating insulation aging and causing erratic circuit breaker operations.",
        )

    st.markdown("---")

    # ==========================================================================
    # 🔍 INTERACTIVE FLEET FILTRATION SYSTEM
    # ==========================================================================
    st.markdown("##### 🔍 Real-Time Asset Registry Filters")
    f_col1, f_col2 = st.columns(2)

    with f_col1:
        unique_classes = sorted(df_enriched["Classification"].unique().tolist())
        selected_classes = st.multiselect(
            label="Filter Assets by Equipment Classification:",
            options=unique_classes,
            default=unique_classes,
            help="Filters rows out of the visual datagrid below to isolate specific equipment networks.",
        )

    with f_col2:
        risk_filter = st.selectbox(
            label="Isolate Asset Risk Classification:",
            options=[
                "Show All Monitored Nodes",
                "Critical Distortion Levels (>15% THD)",
                "Nominal Bound Levels (<5% THD)",
            ],
        )

    # Apply interactive filters to the layout state
    df_filtered = df_enriched[df_enriched["Classification"].isin(selected_classes)]

    if risk_filter == "Critical Distortion Levels (>15% THD)":
        df_filtered = df_filtered[df_filtered["Distortion (THD_i)"] > 15.0]
    elif risk_filter == "Nominal Bound Levels (<5% THD)":
        df_filtered = df_filtered[df_filtered["Distortion (THD_i)"] <= 5.0]

    # ==========================================================================
    # 📋 HIGH-FIDELITY DATAGRID WITH ADVANCED RENDERING CONFIGURATIONS
    # ==========================================================================
    st.markdown(f"### 🗃️ Verified Operational Asset Register: {active_client}")
    st.markdown(
        "Review the line-item engineering matrix below. Advanced data configurations inject real-time "
        "calculated thermal losses and physical insulation breakdown estimates directly alongside each hardware row."
    )

    # Apply Streamlit's elite column styling engine to embed indicators and clean units
    st.dataframe(
        data=df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Asset Tag": st.column_config.TextColumn("Asset Tag"),
            "Plant Location": st.column_config.TextColumn("Plant Location"),
            "Classification": st.column_config.TextColumn("Classification"),
            "Rating (kW)": st.column_config.NumberColumn("Rating (kW)", format="%d kW"),
            "Weekly Hrs": st.column_config.NumberColumn(
                "Weekly Hrs", format="%d Hrs/Wk"
            ),
            "Distortion (THD_i)": st.column_config.NumberColumn(
                "Distortion (THD_i)", format="%.1f%%"
            ),
            "Annual Waste (kWh)": st.column_config.NumberColumn(
                "Annual Waste (kWh)", format="%,.0f kWh"
            ),
            "Financial Leakage": st.column_config.NumberColumn(
                "Financial Loss (Annual)", format="£%,.2f"
            ),
            "Insulation Life Expectancy": st.column_config.ProgressColumn(
                "Winding Insulation Integrity",
                help="Estimated current life expectancy index of the solid insulation barrier. Heat accumulation from harmonic frequencies causes geometric acceleration of chemical wear.",
                min_value=0,
                max_value=100,
                format="%d%%",
            ),
        },
    )

    # ==========================================================================
    # 🖨️ EXPORT COMPLIANCE NODE
    # ==========================================================================
    st.markdown("#### 📑 Engineering Documentation Actions")
    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=f"📥 Print / Export Enriched Asset Register ({active_client.replace(' ', '_')}.csv)",
        data=csv_bytes,
        file_name=f"STEM_{active_client.replace(' ', '_')}_Enriched_Operational_Register.csv",
        mime="text/csv",
        help="Compiles the active filtered asset array along with calculated thermal losses and insulation integrity coefficients into an un-truncated CSV format ready for audit records or contractual inclusions.",
    )
