import os
import sys

# ==========================================================================
# 🛡️ PATH INSURANCE POLICY (CRITICAL FOR LINUX CLOUD DEPLOYMENTS)
# ==========================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import streamlit as st

# Configure the master application page envelope
st.set_page_config(
    page_title="STEM Platform | Market Catalyst & Swalek JV",
    page_icon="⚡",
    layout="wide",
)


def check_password():
    """
    Returns True if the user has entered a valid password.
    Differentiates between Master Admin, Sandbox Tester, and Read-Only Reviewer roles.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = "viewer"  # Roles: admin, tester, viewer

    if st.session_state.authenticated:
        return True

    # Render a clean, branded boardroom login gateway
    st.markdown("## ⚡ STEM Platform Strategic Advisory Portal")
    st.markdown(
        "##### Managed Joint Venture Framework | Market Catalyst Ltd & Swalek Ltd"
    )
    st.write(
        "Please enter your corporate authorisation credential to access the active portfolio twin."
    )

    # Securely retrieve credentials from Streamlit's secrets manager
    try:
        admin_password = st.secrets["auth_credentials"]["admin_password"]
        tester_password = st.secrets["auth_credentials"]["tester_password"]
        reviewer_password = st.secrets["auth_credentials"]["reviewer_password"]
    except KeyError:
        # Secure fallbacks for local staging runs
        admin_password = "STEM_Admin_2026"
        tester_password = "STEM_Staging_2026"
        reviewer_password = "STEM_Reviewer_2026"

    with st.form("credential_logging_gateway"):
        user_password = st.text_input("Enterprise Security Access Key", type="password")
        submit_key = st.form_submit_button("Authorise Session")

        if submit_key:
            if user_password == admin_password:
                st.session_state.authenticated = True
                st.session_state.role = "admin"
                st.success(
                    "🔒 Admin Session Authorised. Full Read-Write Privileges Granted."
                )
                st.rerun()
            elif user_password == tester_password:
                st.session_state.authenticated = True
                st.session_state.role = "tester"
                st.warning(
                    "🧪 Sandbox Tester Session Authorised. Data Ingestion Walk-Through Enabled."
                )
                st.rerun()
            elif user_password == reviewer_password:
                st.session_state.authenticated = True
                st.session_state.role = "viewer"
                st.info(
                    "👁️ Reviewer Session Authorised. Read-Only Portfolio Mode Activated."
                )
                st.rerun()
            else:
                st.error(
                    "❌ Invalid Access Key. Security boundary maintained. Please check with the MD."
                )
                return False
    return False


# Execute the security boundary check
if check_password():
    # Lazy-load the dashboard view nodes to optimise runtime speeds
    from src.ui.views.executive import render_executive_view
    from src.ui.views.operations import render_operations_view
    from src.ui.views.data_entry import render_data_entry_view

    # ==========================================================================
    # 🗺️ NAVIGATION SIDEBAR & BRAND WORKSPACE
    # ==========================================================================
    st.sidebar.title("⚡ STEM")
    st.sidebar.markdown("**High-Voltage Joint Venture**")

    # Render localised status configurations based on authorised role
    if st.session_state.role == "admin":
        st.sidebar.caption("🔥 **Session Status:** `MASTER ADMIN (RW)`")
        workspace_options = [
            "Executive Command",
            "Operations Management",
            "Ingest Site Data",
        ]
    elif st.session_state.role == "tester":
        st.sidebar.caption("🧪 **Session Status:** `SANDBOX TESTER`")
        st.sidebar.info(
            "Sandbox Mode: Data entry screens are unlocked for simulation walk-throughs."
        )
        workspace_options = [
            "Executive Command",
            "Operations Management",
            "Ingest Site Data",
        ]
    else:
        st.sidebar.caption("🔒 **Session Status:** `READ-ONLY REVIEWER`")
        workspace_options = ["Executive Command", "Operations Management"]

    workspace_selection = st.sidebar.radio(
        "Select Active Portal Node:", workspace_options
    )

    st.sidebar.divider()
    st.sidebar.caption("Compute Context: `LOCAL_LAPTOP_STREAM`")
    st.sidebar.caption("System Version: `2026.1.MVP`")

    # ==========================================================================
    # 🎛️ CENTRAL VIEW ROUTER NODE
    # ==========================================================================
    if workspace_selection == "Executive Command":
        render_executive_view()
    elif workspace_selection == "Operations Management":
        render_operations_view()
    elif workspace_selection == "Ingest Site Data":
        render_data_entry_view()
