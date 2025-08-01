import streamlit as st

def display_inputs_with_tab():
    """
    Draws all UI input sections using tabs instead of sidebar.
    Returns:
        tuple(dict, UploadedFile): user configuration dictionary, load profile file
    """
    st.header("📁 Load Profile Upload")
    load_file = st.file_uploader(
        "Upload CSV with 15-min/hourly 'timestamp' and 'load_kW' or 'energy_kWh'",
        type="csv"
    )

    st.markdown("---")
    st.subheader("⚙️ Simulation Settings")

    tab1, tab2, tab3 = st.tabs(["☀️ PV Configuration", "🔋 Battery Storage", "🚗 EV Charging"])

    with tab1:
        pv_kwp = st.number_input("Preferred PV size (kWp)", min_value=10, max_value=2000, value=100, step=10)
        shading = st.slider("Shading factor", 0.0, 1.0, 1.0, step=0.05)

    with tab2:
        bess_kwh = st.number_input("Battery capacity (kWh)", min_value=0, max_value=5000, value=500, step=50)
        bess_kw = st.number_input("Battery power (kW)", min_value=0, max_value=1000, value=250, step=10)

    with tab3:
        fleet_size = st.number_input("Number of EVs", min_value=0, max_value=500, value=10, step=1)
        ev_batt = st.number_input("Battery size per EV (kWh)", min_value=10, max_value=200, value=50, step=5)
        ev_window = st.slider("Charging hours (start–end)", 0, 24, (9, 17))

    user_input = {
        "pv": {"kwp_pref": pv_kwp, "shading_factor": shading},
        "bess": {"capacity_kwh": bess_kwh, "power_kw": bess_kw},
        "ev": {
            "fleet_size": fleet_size,
            "battery_capacity_kwh": ev_batt,
            "charging_window": list(ev_window)
        }
    }
    return user_input, load_file