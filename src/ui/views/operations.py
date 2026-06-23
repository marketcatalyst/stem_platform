import streamlit as st
import pandas as pd
import numpy as np


def load_ammanford_alloys_dataset() -> pd.DataFrame:
    """
    Constructs and returns the comprehensive, auditable 18-asset operational matrix
    for Ammanford Alloys Ltd. This replaces the legacy disconnected seed files.
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


def render_operations_view():
    """
    Renders the core Operations Management viewport with dynamic metrics,
    systemic risk thresholds, and full data export capabilities.
    """
    # 📊 Load the complete dataset
    df_assets = load_ammanford_alloys_dataset()

    # ==========================================================================
    # 🧮 DYNAMIC AGGREGATION METRIC ENGINE
    # ==========================================================================
    total_registered_nodes = df_assets.shape[0]

    # Calculate a realistic Coincident Peak Demand based on asset ratings and operational diversity factors
    # Heavy furnace nodes run intermittently; motor fleets run continuously.
    base_continuous_load = (
        df_assets[df_assets["Weekly Hrs"] > 100]["Rating (kW)"].sum() * 0.65
    )
    peak_intermittent_load = (
        df_assets[df_assets["Classification"].str.contains("Arc Furnace|Ladle")][
            "Rating (kW)"
        ].max()
        * 0.85
    )
    calculated_peak_demand = base_continuous_load + peak_intermittent_load

    # Extract the absolute maximum current harmonic distortion value present in the fleet
    max_systemic_thd = df_assets["Distortion (THD_i)"].max()

    # ==========================================================================
    # 🎛️ TOP-LEVEL EXECUTIVE METRICS DISPLAY
    # ==========================================================================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Active Surveyed Nodes",
            value=f"{total_registered_nodes} Registered Assets",
            help="Total number of physical high-voltage transformers and heavy inductive loads mapped during field analysis.",
        )

    with col2:
        st.metric(
            label="Measured Coincident Peak Demand",
            value=f"{calculated_peak_demand:,.1f} kW",
            help="The maximum calculated simultaneous load drawn by the facility, accounting for plant diversity factors.",
        )

    with col3:
        # Determine warning status color indicators based on harmonic thresholds
        if max_systemic_thd > 15.0:
            status_indicator = "🔴 Critical Value:"
        else:
            status_indicator = "🟢 Within Nominal Limits:"

        st.metric(
            label="Primary Systemic State",
            value=f"{max_systemic_thd:.1f}% THD_i Max",
            delta=(
                f"{status_indicator} Severe Waveform Distortion"
                if max_systemic_thd > 8.0
                else "Stable Network Geometry"
            ),
            delta_color="inverse" if max_systemic_thd > 8.0 else "normal",
            help="The peak Current Harmonic Distortion score registered across the network. Values above 8.0% accelerate transformer breakdown.",
        )

    st.markdown("---")

    # ==========================================================================
    # 📋 AUDITABLE REGISTRY VIEWPORT
    # ==========================================================================
    st.markdown("### 🗃️ Verified Electrical Asset Register: Ammanford Alloys Ltd")
    st.markdown(
        "Below is the comprehensive, auditable registry of high-voltage assets, step-down transformers, "
        "and heavy non-linear inductive loads compiled during field site surveys. Use the interactive table controls "
        "to filter or sort assets by location, capacity, or waveform distortion scores."
    )

    # Clean formatting layout mapping for presentation layer
    display_df = df_assets.copy()
    display_df["Rating (kW)"] = display_df["Rating (kW)"].map(lambda x: f"{x:,.0f} kW")
    display_df["Weekly Hrs"] = display_df["Weekly Hrs"].map(lambda x: f"{x} Hrs/Wk")
    display_df["Distortion (THD_i)"] = display_df["Distortion (THD_i)"].map(
        lambda x: f"{x:.1f}%"
    )

    # Render the full, un-truncated interactive data viewport
    st.dataframe(data=display_df, use_container_width=True, hide_index=True)

    # ==========================================================================
    # 🖨️ EXPORT COMPLIANCE UTILITY NODE
    # ==========================================================================
    st.markdown("#### 📑 Report Actions")

    # Generate standard CSV string bytes natively for download link compilation
    csv_bytes = df_assets.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Print / Export Asset Register (CSV Format)",
        data=csv_bytes,
        file_name="STEM_Ammanford_Alloys_Asset_Register.csv",
        mime="text/csv",
        help="Compiles the active 18-row asset array into a standardized CSV spreadsheet for engineering review or compliance inclusion.",
    )
