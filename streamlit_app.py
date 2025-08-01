# ----------------------
# main.py (Entry point with streamlined logic)
# ----------------------

import streamlit as st
import pandas as pd

from ui import display_sidebar_inputs
from parse_inputs import get_config_from_user_input
from load_profile import load_demand_profile
from optimizer import run_optimization
from kpi_module import calculate_kpis

st.set_page_config(page_title="GridEdge Optimizer", layout="wide")
st.title("🔋 GridEdge Optimizer – PV + BESS + EV Sizing Tool")

# Step 1: Get user input from sidebar
user_input, load_file = display_sidebar_inputs()

# Step 2: Validate input & run simulation
st.markdown("---")
st.subheader("📊 Simulation Output")

if load_file is not None:
    try:
        load_df = load_demand_profile(load_file)
        config = get_config_from_user_input(user_input)
        results = run_optimization(load_df["power_kW"], config)
        kpis = calculate_kpis(results)

        # Step 3: Show KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Grid Import (kWh)", f"{kpis['total_grid_import_kWh']:.2f}")
        col2.metric("Solar Generation (kWh)", f"{kpis['total_solar_generation_kWh']:.2f}")
        col3.metric("Self-Consumption (%)", f"{kpis['solar_self_consumption_%']:.2f}%")
        col4.metric("Peak Demand (kW)", f"{kpis['peak_demand_kW']:.2f}")

        # Step 4: Time series chart
        st.markdown("### 📈 Time Series Overview")
        plot_df = pd.DataFrame({
            "Load": results["net_grid_kW"] + results["pv"] + results["bess"]["bess_dispatch_kW"] - results["ev"],
            "PV": results["pv"],
            "EV": results["ev"],
            "BESS Dispatch": results["bess"]["bess_dispatch_kW"],
            "Net Grid": results["net_grid_kW"]
        })
        st.line_chart(plot_df)

        with st.expander("View Raw Results Table"):
            st.dataframe(plot_df)

    except Exception as e:
        st.error(f"❌ Error processing file or simulation: {e}")
else:
    st.info("👈 Upload a valid load profile CSV using the sidebar to begin.")