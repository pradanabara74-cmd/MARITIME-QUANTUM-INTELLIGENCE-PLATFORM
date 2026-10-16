import streamlit as st

st.set_page_config(
    page_title="Maritime Quantum Intelligence Platform",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚓ MARITIME QUANTUM INTELLIGENCE PLATFORM")
st.caption(
    "Unified Maritime ERP • Marine Operations • Fuel Efficiency "
    "• QHSSE • AIS Intelligence • AI • Automation"
)

st.info(
    "Master platform initialized. Existing projects remain separate "
    "until their modules are integrated and tested."
)

st.sidebar.title("Navigation")

module = st.sidebar.radio(
    "Select Module",
    [
        "Executive Dashboard",
        "MQEIP & ERP",
        "Marine Operations",
        "Fuel Efficiency & BBM",
        "QHSSE & Risk",
        "AIS Vessel Tracking",
        "AI Intelligence Center",
        "N8N Workflow Automation",
        "Data Analytics",
        "Document Intelligence",
        "Client Management",
    ],
)

st.subheader(module)

st.write(
    "This module is being prepared for integration. "
    "No existing production system has been modified."
)
