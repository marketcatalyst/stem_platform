import streamlit as st
import pandas as pd


def render_operations_view():
    """
    Renders the STEM Operations Management interface workspace.
    Displays cross-client portfolio asset metrics, dynamic risk profiling,
    and provides a fully viewable, downloadable, and printable asset register.
    """
    st.subheader("📋 STEM Portfolio Account & Operations Registry")
    st.markdown(
        "This master console tracks active high-voltage infrastructure profiles, logged engineering "
        "asset volumes, and calculated operational risk matrices across your active client accounts."
    )
    st.divider()

    # ==========================================================================
    # 📂 1. PORTFOLIO ACCOUNT FOCUS SELECTOR
    # ==========================================================================
    st.markdown("#### 📂 Select Client Account Registry")
    client_name = st.selectbox(
        "Switch Operational Focus Profile",
        [
            "Ammanford Alloys Ltd",
            "Swansea Silica Mining Operations",
            "Killan Farm Solar Array Hub",
        ],
    )
    st.caption(f"Currently inspecting operational field records for: **{client_name}**")
    st.divider()

    # ==========================================================================
    # 📈 2. DYNAMIC CLIENT OVERVIEW METRICS
    # ==========================================================================
    # Context-switching summary stat vectors matching our master profiles
    client_stats = {
        "Ammanford Alloys Ltd": {
            "assets": 18,
            "peak": "190.0 kW",
            "status": "🔴 38% THD_i Distortion",
            "color": "inverse",
        },
        "Swansea Silica Mining Operations": {
            "assets": 14,
            "peak": "680.0 kW",
            "status": "🟢 Nominal Operations",
            "color": "normal",
        },
        "Killan Farm Solar Array Hub": {
            "assets": 10,
            "peak": "920.0 kW",
            "status": "🟡 Severe Phase Imbalance",
            "color": "off",
        },
    }
    stats = client_stats[client_name]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="⚙️ Active Surveyed Nodes",
            value=f"{stats['assets']} Registered Assets",
            help="Total number of distinct physical equipment entries mapped onto this client's database profile.",
        )
    with col2:
        st.metric(
            label="⚡ Measured Peak Demand",
            value=stats["peak"],
            help="The maximum empirical active power throughput registered on the client's incoming network switch.",
        )
    with col3:
        st.metric(
            label="⚠️ Primary Systemic State",
            value=stats["status"],
            help="The leading operational risk or compliance vector flagged by the STEM analytics engine.",
        )

    st.divider()

    # ==========================================================================
    # 📝 3. THE ELECTRICAL ASSET REGISTER VIEW & EXPORT
    # ==========================================================================
    st.write(f"### 🗃️ Verified Electrical Asset Register: {client_name}")
    st.markdown(
        "Below is the comprehensive, auditable registry of high-voltage assets, transformers, "
        "and heavy non-linear inductive loads compiled during field site surveys. Use the download button "
        "below to export a print-ready spreadsheet file for compliance records."
    )

    # Granular mock registers mapped directly to our lookalike portfolio accounts
    registers = {
        "Ammanford Alloys Ltd": [
            {
                "Asset Tag": "TX-01-SUB-A",
                "Plant Location": "Substation 1 Main Bay",
                "Classification": "Main Distribution Transformer",
                "Rating (kW)": 1500.0,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": "8.5%",
            },
            {
                "Asset Tag": "VSD-04-LINE-3",
                "Plant Location": "Production Line 3 East",
                "Classification": "Variable Speed Drive (VSD)",
                "Rating (kW)": 75.0,
                "Weekly Hrs": 40,
                "Distortion (THD_i)": "38.0%",
            },
            {
                "Asset Tag": "MOT-12-CRUSHER",
                "Plant Location": "Primary Feed Intake",
                "Classification": "Large Induction Motor",
                "Rating (kW)": 250.0,
                "Weekly Hrs": 65,
                "Distortion (THD_i)": "5.2%",
            },
            {
                "Asset Tag": "ARC-01-MELT",
                "Plant Location": "Casting Hall Furnace Node",
                "Classification": "Arc Furnace Plant",
                "Rating (kW)": 3500.0,
                "Weekly Hrs": 24,
                "Distortion (THD_i)": "22.1%",
            },
        ],
        "Swansea Silica Mining Operations": [
            {
                "Asset Tag": "TX-01-MINE",
                "Plant Location": "Surface Intake Substation",
                "Classification": "Main Distribution Transformer",
                "Rating (kW)": 2000.0,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": "3.1%",
            },
            {
                "Asset Tag": "PMP-08-DEWATER",
                "Plant Location": "Lower Shaft Pump Room",
                "Classification": "Large Induction Motor",
                "Rating (kW)": 500.0,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": "4.0%",
            },
            {
                "Asset Tag": "VSD-01-CONVEY",
                "Plant Location": "Main Incline Belt",
                "Classification": "Variable Speed Drive (VSD)",
                "Rating (kW)": 110.0,
                "Weekly Hrs": 80,
                "Distortion (THD_i)": "18.0%",
            },
        ],
        "Killan Farm Solar Array Hub": [
            {
                "Asset Tag": "INV-01-SOLAR",
                "Plant Location": "Inverter Enclosure 1",
                "Classification": "Central Solar Inverter",
                "Rating (kW)": 500.0,
                "Weekly Hrs": 70,
                "Distortion (THD_i)": "12.0%",
            },
            {
                "Asset Tag": "INV-02-SOLAR",
                "Plant Location": "Inverter Enclosure 2",
                "Classification": "Central Solar Inverter",
                "Rating (kW)": 500.0,
                "Weekly Hrs": 70,
                "Distortion (THD_i)": "11.5%",
            },
            {
                "Asset Tag": "BESS-01-BATTERY",
                "Plant Location": "Main DC Storage Vault",
                "Classification": "Custom Inductive Load",
                "Rating (kW)": 1000.0,
                "Weekly Hrs": 168,
                "Distortion (THD_i)": "2.1%",
            },
        ],
    }

    # Extract target account list and parse into an active Pandas Dataframe
    active_registry_data = registers[client_name]
    df_registry = pd.DataFrame(active_registry_data)

    # Compile the Dataframe to a raw CSV string buffer for the download button
    csv_buffer = df_registry.to_csv(index=False).encode("utf-8")

    # Visual layout controls linking data view and data printing actions side-by-side
    col_table, col_print = st.columns([4, 1])

    with col_table:
        # Render the spreadsheet view using 2026 design standard width stretch values
        st.dataframe(df_registry, width="stretch", hide_index=True)

    with col_print:
        st.markdown("#### 🖨️ Document Actions")
        st.caption(
            "Generate an un-truncated Excel/CSV spreadsheet format ready for immediate physical printing or audit inclusion."
        )

        # Native, secure Streamlit download anchor compiling file on demand
        st.download_button(
            label="📥 Print / Export Asset Register",
            data=csv_buffer,
            file_name=f"STEM_Asset_Register_{client_name.replace(' ', '_')}.csv",
            mime="text/csv",
            help="Downloads this specific client register as a standard CSV format file. Opens natively in Microsoft Excel for immediate local printing.",
        )

    st.divider()

    # ==========================================================================
    # 🧠 4. CONSULTATIVE FIELD STRATEGY CALLOUT
    # ==========================================================================
    st.write("### 🧭 Strategic Intervention Framework")
    st.markdown(
        "When an account logs a systemic risk profile anomaly, the STEM platform advises executing the "
        "following joint venture deployment sequence to preserve client capital:"
    )

    with st.expander("🔍 Phase 1: Empirical Validation Loop"):
        st.write(
            "Deploy the client data ingestion module to reconcile historical desktop survey estimates "
            "against raw half-hourly utility AMR logs. This isolates exact maximum demand baselines "
            "and exposes capacity overestimation waste."
        )
    with st.expander("⚡ Phase 2: Hardware Filter Deployment"):
        st.write(
            "Utilise Swalek's technical field resources and engineering assets to design, position, "
            "and commission active-filtering or battery storage systems (BESS) directly at the client's "
            "main incoming busbars to suppress waveform friction."
        )
    with st.expander("📊 Phase 3: Financial Boardroom Reporting"):
        st.write(
            "Generate an AI-driven text transformation brief inside the Executive workspace. Use "
            "the resulting custom financial metaphors to illustrate balance-sheet insulation degradation "
            "and lifetime restoration metrics directly to their non-technical directors."
        )
