# ----------------------
# ui.py (UI input module)
# ----------------------

import streamlit as st

def display_sidebar_inputs():
    """
    Draws all sidebar input elements and returns a user input dictionary + load profile file.

    Returns:
        tuple(dict, UploadedFile): user configuration dictionary, load profile file
    """
    with st.sidebar:
        st.header("📁 Load Profile")
        load_file = st.file_uploader(
            "Upload CSV with 15-min/hourly 'timestamp' and 'load_kW' or 'energy_kWh'",
            type="csv"
        )

        st.header("⚙️ Simulation Settings")

        st.subheader("☀️ PV Configuration")
        pv_kwp = st.number_input("Preferred PV size (kWp)", min_value=10, max_value=2000, value=100, step=10)
        shading = st.slider("Shading factor", 0.0, 1.0, 1.0, step=0.05)

        st.subheader("🔋 Battery Storage")
        bess_kwh = st.number_input("Battery capacity (kWh)", min_value=0, max_value=5000, value=500, step=50)
        bess_kw = st.number_input("Battery power (kW)", min_value=0, max_value=1000, value=250, step=10)

        st.subheader("🚗 EV Charging")
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