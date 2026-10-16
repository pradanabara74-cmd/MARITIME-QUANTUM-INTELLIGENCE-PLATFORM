import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Maritime Quantum Intelligence Platform",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚓ MARITIME QUANTUM INTELLIGENCE PLATFORM")
st.caption(
    "Unified Maritime ERP | Marine Operations | Fuel Efficiency | "
    "QHSSE | AIS | AI | Automation | Analytics"
)

st.sidebar.title("PLATFORM NAVIGATION")

modules = [
    "Executive Dashboard",
    "MQEIP & ERP",
    "Marine Operations",
    "Fuel Efficiency & BBM",
    "QHSSE & Risk",
    "AIS Vessel Tracking",
    "DPR Master Database",
    "Bunker Intelligence",
    "Cargo Intelligence",
    "Crew & Certificates",
    "Maintenance & Defects",
    "Document Intelligence",
    "Data Analytics",
    "AI Intelligence Center",
    "N8N Workflow Automation",
    "Client Management",
]

module = st.sidebar.radio("Select Module", modules)

st.sidebar.divider()
st.sidebar.caption("MASTER PLATFORM | DEVELOPMENT")

if "vessels" not in st.session_state:
    st.session_state.vessels = []

if module == "Executive Dashboard":
    st.subheader("Executive Dashboard")
    a, b, c = st.columns(3)
    a.metric("Registered Vessels", len(st.session_state.vessels))
    b.metric("Platform Modules", len(modules))
    c.metric("Live AIS", "Not connected")
    st.info(
        "This is the new master platform. "
        "Legacy systems remain separate until integration is tested."
    )

elif module == "Marine Operations":
    st.subheader("Marine Operations")
    with st.form("vessel_form", clear_on_submit=True):
        vessel_name = st.text_input("Vessel Name")
        vessel_type = st.selectbox(
            "Vessel Type",
            ["Tugboat", "Ocean Tug", "AHT", "AHTS", "Tanker", "Cargo Vessel"],
        )
        submitted = st.form_submit_button("Add Vessel")
    if submitted:
        if vessel_name.strip():
            st.session_state.vessels.append(
                {"Vessel Name": vessel_name.strip(), "Vessel Type": vessel_type}
            )
            st.success("Vessel added to this session.")
        else:
            st.warning("Enter a vessel name.")
    if st.session_state.vessels:
        st.dataframe(pd.DataFrame(st.session_state.vessels), use_container_width=True)
    else:
        st.info("No vessel records added in this session.")

elif module == "Data Analytics":
    st.subheader("Data Analytics")
    uploaded = st.file_uploader("Upload CSV for analysis", type=["csv"])
    if uploaded:
        try:
            data = pd.read_csv(uploaded)
            st.write("Rows:", len(data), "| Columns:", len(data.columns))
            st.dataframe(data, use_container_width=True)
            st.download_button(
                "Download CSV",
                data.to_csv(index=False).encode("utf-8"),
                "cleaned_data.csv",
                "text/csv",
            )
        except Exception as exc:
            st.error(f"Unable to read CSV: {exc}")

else:
    st.subheader(module)
    st.info(
        "Module registered. Its legacy project, backend, database, "
        "and credentials must be integrated and tested before production use."
    )
