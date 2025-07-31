# ----------------------
# main.py (Streamlit MVP Launcher - Clean UI Layout)
# ----------------------

import streamlit as st
import pandas as pd

from parse_inputs import get_config_from_user_input
from load_profile import load_demand_profile
from optimizer import run_optimization
from kpi_module import calculate_kpis

st.set_page_config(page_title="GridEdge Optimizer", layout="wide")
st.title("🔋 GridEdge Optimizer – PV + BESS + EV Sizing Tool")

# Sidebar configuration pane
with st.sidebar:
    st.header("📁 Load Profile")
    load_file = st.file_uploader("Upload CSV with 15-min/hourly 'timestamp' and 'load_kW' or 'energy_kWh'", type="csv")

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

# Main content area
st.markdown("---")
st.subheader("📊 Simulation Output")

if load_file is not None:
    try:
        load_df = load_demand_profile(load_file)
        timestamps = load_df.index

        # Create config from sidebar input
        user_input = {
            "pv": {"kwp_pref": pv_kwp, "shading_factor": shading},
            "bess": {"capacity_kwh": bess_kwh, "power_kw": bess_kw},
            "ev": {
                "fleet_size": fleet_size,
                "battery_capacity_kwh": ev_batt,
                "charging_window": list(ev_window)
            }
        }
        config = get_config_from_user_input(user_input)

        # Run core simulation
        results = run_optimization(load_df["power_kW"], config)
        kpis = calculate_kpis(results)

        # Output KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Grid Import (kWh)", f"{kpis['total_grid_import_kWh']:.2f}")
        col2.metric("Solar Generation (kWh)", f"{kpis['total_solar_generation_kWh']:.2f}")
        col3.metric("Self-Consumption (%)", f"{kpis['solar_self_consumption_%']:.2f}%")
        col4.metric("Peak Demand (kW)", f"{kpis['peak_demand_kW']:.2f}")

        # Time series output
        st.markdown("### 📈 Time Series Overview")
        plot_df = pd.DataFrame({
            "Load": results["net_grid_kW"] + results["pv"] + results["bess"]["bess_dispatch_kW"] - results["ev"],
            "PV": results["pv"],
            "EV": results["ev"],
            "BESS Dispatch": results["bess"]["bess_dispatch_kW"],
            "Net Grid": results["net_grid_kW"]
        })
        st.line_chart(plot_df)

        # Optional: Add tabs for export or more KPIs later
        with st.expander("View Raw Results Table"):
            st.dataframe(plot_df)

    except Exception as e:
        st.error(f"❌ Error processing file or simulation: {e}")
else:
    st.info("👈 Upload a valid load profile CSV using the sidebar to begin.")