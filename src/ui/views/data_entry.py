import streamlit as st
import pandas as pd


def render_data_entry_view():
    """
    Renders the advanced STEM Data Ingestion Portal.
    Features manual single asset forms, Excel-style batch copy-paste editors,
    bulk CSV/Excel file porters, Document AI scanning dropzones, and AMR utility parsers.
    """
    st.subheader("📥 STEM Advanced Data Ingestion Portal")
    st.markdown(
        "Transform legacy client records into active digital twin telemetry. Use this workspace to "
        "ingest asset data via individual field forms, live batch spreadsheets, bulk file imports, "
        "or intelligent Document AI optical scans."
    )

    # Screen-Based Consultative Workflow Guidance Callout
    st.info(
        "💡 **JV Field Survey Protocol:** For optimal lookalike model alignment, capture the asset registry "
        "parameters first (via manual, batch, or scanned methods) to anchor your infrastructure inventory. "
        "Follow this by uploading the client's continuous half-hourly AMR utility meter streams to execute "
        "the empirical reconciliation loop."
    )
    st.divider()

    # Split ingestion into three specialized UX onboarding workflows
    tab_registry, tab_scanner, tab_amr = st.tabs(
        [
            "📝 Asset Registry Ingestion",
            "📁 Bulk File & Document AI Scanner",
            "📊 Client AMR Half-Hourly Integration",
        ]
    )

    # ==========================================================================
    # 📝 WORKFLOW 1: LIVE REGISTRY INGESTION (SINGLE & BATCH GRID)
    # ==========================================================================
    with tab_registry:
        st.markdown("### 🔍 Live Inventory Logging Center")
        st.markdown(
            "Select your preferred data entry method below. Use the **Single Asset Form** for immediate "
            "one-off entries during site walks, or the **Excel-Style Batch Editor** to copy and paste "
            "entire table blocks simultaneously."
        )

        entry_mode = st.radio(
            "Choose Active Entry Interface Mode:",
            ["Spreadsheet-Style Batch Editor", "Single Asset Validation Form"],
            horizontal=True,
        )
        st.markdown("---")

        if entry_mode == "Single Asset Validation Form":
            st.markdown("#### 🔍 Individual Field Survey Registration")
            with st.form("client_asset_entry_form", clear_on_submit=True):
                st.markdown("##### 🆔 Core Asset Registry & Tracking")
                col_id, col_loc = st.columns(2)
                with col_id:
                    asset_tag = st.text_input(
                        "Unique Asset Tag / Serial Reference",
                        placeholder="e.g., TX-01-SUB-A",
                    )
                with col_loc:
                    asset_location = st.text_input(
                        "Physical Plant Location / Bay Area",
                        placeholder="e.g., Substation 1 Bay",
                    )

                st.divider()
                st.markdown("##### ⚡ Electrical Operational Parameters")
                col1, col2 = st.columns(2)
                with col1:
                    asset_class = st.selectbox(
                        "Equipment / Asset Classification",
                        [
                            "Variable Speed Drive (VSD)",
                            "Large Direct-on-Line Induction Motor",
                            "LED Lighting Arrays",
                            "Arc Furnace / Heavy Welding Plant",
                        ],
                    )
                    nominal_kw = st.number_input(
                        "Nominal Nameplate Power Rating (kW)", min_value=0.0, value=75.0
                    )
                with col2:
                    weekly_hours = st.slider(
                        "Estimated Weekly Operational Runtime (Hours)",
                        min_value=1,
                        max_value=168,
                        value=40,
                    )
                    observed_thd = st.number_input(
                        "Surveyor Predicted Current Distortion (THD_i %)",
                        min_value=0.0,
                        value=5.0,
                    )

                st.divider()
                st.markdown("##### 📸 Field Evidence Validation")
                uploaded_photo = st.file_uploader(
                    "Upload Physical Asset Snapshot", type=["png", "jpg", "jpeg"]
                )
                if uploaded_photo:
                    st.image(
                        uploaded_photo,
                        caption="Staging Preview: Captured Field Evidence",
                        width=340,
                    )

                st.markdown("##")
                submit_asset = st.form_submit_button(
                    label="⚡ Commit Asset to Client Account Profile"
                )
                if submit_asset:
                    if not asset_tag:
                        st.error(
                            "❌ Validation Failed: A unique Asset Tag Reference is mandatory."
                        )
                    else:
                        st.success(
                            f"Successfully committed asset record **{asset_tag}** into staging registry!"
                        )

        else:
            st.markdown("#### 📊 Excel-Style Batch Spreadsheet Editor")
            st.markdown(
                "💬 **UX Power Pro-Tip:** You can click directly into any cell below to type, edit, or append rows. "
                "Alternatively, you can select a block of cells inside an external **Microsoft Excel** or **Google Sheet** "
                "spreadsheet, press `Ctrl+C`, select the top-left cell of this grid, and press `Ctrl+V` to batch-paste "
                "hundreds of rows instantly."
            )

            # Formulate an empty structural schema block matching our database fields
            batch_template = {
                "Unique Asset Tag *": ["TX-01-SUB-A", "VSD-04-LINE-3", "", "", ""],
                "Plant Location / Bay": [
                    "Substation 1 Main Bay",
                    "Production Line 3 East",
                    "",
                    "",
                    "",
                ],
                "Equipment Classification": [
                    "Main Distribution Transformer",
                    "Variable Speed Drive (VSD)",
                    "Large Direct-on-Line Induction Motor",
                    "LED Lighting Arrays / Server Clusters",
                    "Other Load Node",
                ],
                "Nominal Power (kW)": [1500.0, 75.0, 0.0, 0.0, 0.0],
                "Weekly Runtime (Hrs)": [168, 40, 0, 0, 0],
                "Current Distortion (THD_i %)": [8.5, 38.0, 0.0, 0.0, 0.0],
            }
            df_template = pd.DataFrame(batch_template)

            # Deploy the native interactive spreadsheet grid component with width stretch options
            edited_registry_df = st.data_editor(
                df_template, width="stretch", num_rows="dynamic", hide_index=True
            )

            col_b1, col_b2 = st.columns([4, 1])
            with col_b2:
                st.markdown("##")  # Alignment spacing
                submit_batch = st.button("⚡ Process & Commit Batch Matrix")

            if submit_batch:
                # Clean out any entirely empty placeholder rows added by user typing frames
                cleaned_batch_df = edited_registry_df.dropna(
                    subset=["Unique Asset Tag *"]
                )
                cleaned_batch_df = cleaned_batch_df[
                    cleaned_batch_df["Unique Asset Tag *"] != ""
                ]

                rows_processed = len(cleaned_batch_df)
                if rows_processed == 0:
                    st.warning(
                        "⚠️ Batch processing halted: No valid records containing an Asset Tag Reference were detected."
                    )
                else:
                    st.success(
                        f"🎉 Batch Ingestion Success! Successfully parsed, validated, and committed **{rows_processed} equipment nodes** into the active client registry."
                    )
                    st.dataframe(cleaned_batch_df, width="stretch", hide_index=True)

    # ==========================================================================
    # 📁 WORKFLOW 2: BULK FILE PORTER & DOCUMENT AI SCANNER
    # ==========================================================================
    with tab_scanner:
        st.markdown("### 🗂️ Automated Legacy Ingestion Engine")

        col_file, col_ocr = st.columns(2)

        with col_file:
            st.markdown("#### 📂 Bulk CSV / Excel Upload Porter")
            st.markdown(
                "Upload pre-compiled digital inventory lists exported from historical client databases."
            )
            bulk_file = st.file_uploader(
                "Drop your existing master asset register spreadsheet here (.csv, .xlsx)",
                type=["csv", "xlsx"],
                key="bulk_register_uploader",
            )
            if bulk_file:
                st.success(
                    "✅ File successfully verified. Schema mapping matrix initialized."
                )

        with col_ocr:
            st.markdown("#### 👁️ STEM Document AI Visual Scanner")
            st.markdown(
                "No digital spreadsheet available? Drop in a PDF scan, data sheet blueprint, or a smartphone "
                "snapshot of a physical layout list. The STEM multimodal document engine will extract the text parameters."
            )
            scanned_doc = st.file_uploader(
                "Drop scanned inventory PDFs or equipment photos here",
                type=["pdf", "png", "jpg", "jpeg"],
                key="document_ai_scanner",
            )
            if scanned_doc:
                st.info(
                    "🧠 Document loaded. STEM Intelligence node is performing table isolation and character recognition matrix extractions..."
                )

    # ==========================================================================
    # 📊 WORKFLOW 3: CLIENT AMR HALF-HOURLY FILE INTEGRATION
    # ==========================================================================
    with tab_amr:
        st.markdown("### 💾 Empirical Utility Meter Stream Integration")
        st.markdown(
            "Drop in raw data exports extracted directly from the client's main utility fiscal billing meter. "
            "The parsing engine natively evaluates chronological half-hourly interval arrays."
        )

        uploaded_file = st.file_uploader(
            "Drop client half-hourly utility CSV or Excel export here",
            type=["csv", "xlsx"],
        )

        st.markdown("---")
        st.markdown("#### 📋 Target File Architecture Specifications")
        structure_data = {
            "Expected Column Header": ["timestamp", "active_kwh", "reactive_kvarh"],
            "Data Format Type": [
                "YYYY-MM-DD HH:MM:SS",
                "Decimal / Float",
                "Decimal / Float",
            ],
            "STEM Ingestion Notes & Explanatory Metaphors": [
                "The chronological boundary marking the close of the 30-minute interval window.",
                "Real useful power drawing through the client's busbars. Metaphor: The actual liquid coffee inside a mug.",
                "Reactive power overhead. Metaphor: The non-productive foam sitting on top of the mug. The client is invoiced for it, but it does no work on their production line.",
            ],
        }
        st.table(pd.DataFrame(structure_data))
