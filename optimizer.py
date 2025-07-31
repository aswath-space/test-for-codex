# ----------------------
# optimizer.py
# ----------------------

from pv_model import simulate_pv_generation
from ev_model import simulate_ev_charging
from bess_model import simulate_bess_dispatch

import pandas as pd

def run_optimization(load_series: pd.Series, config: dict) -> dict:
    """
    Combine PV, BESS, and EV models to simulate total system behavior.

    Args:
        load_series (pd.Series): site load in kW
        config (dict): full configuration dict from user input

    Returns:
        dict: { 'pv': pd.Series, 'ev': pd.Series, 'bess': dict, 'net_grid_kW': pd.Series }
    """
    timestamps = load_series.index

    # Simulate PV generation
    pv_series = simulate_pv_generation(config, timestamps)

    # Simulate EV charging
    ev_series = simulate_ev_charging(config, timestamps)

    # Compute gross load = site load + EVs
    gross_demand = load_series + ev_series

    # Simulate BESS
    bess_results = simulate_bess_dispatch(gross_demand, pv_series, config)
    bess_dispatch = bess_results["bess_dispatch_kW"]

    # Net grid import = load + ev - pv - battery
    net_grid = gross_demand - pv_series - bess_dispatch

    return {
        "pv": pv_series,
        "ev": ev_series,
        "bess": bess_results,
        "net_grid_kW": net_grid
    }