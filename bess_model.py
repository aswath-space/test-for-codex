# ----------------------
# bess_model.py
# ----------------------

import pandas as pd
import numpy as np

def simulate_bess_dispatch(load_kW: pd.Series, pv_kW: pd.Series, config: dict) -> dict:
    """
    Simulate battery charge/discharge to shave peaks and reduce grid import.

    Args:
        load_kW (pd.Series): site demand
        pv_kW (pd.Series): PV output
        config (dict): includes battery capacity, power, efficiency

    Returns:
        dict: {'bess_dispatch_kW': ..., 'soc_kWh': ...}
    """
    batt_capacity = config["bess"].get("capacity_kwh", 0)
    batt_power = config["bess"].get("power_kw", 0)
    eff = config["bess"].get("round_trip_efficiency", 0.9)

    timestep_hr = (load_kW.index[1] - load_kW.index[0]).seconds / 3600
    soc = 0.5 * batt_capacity

    dispatch = []
    soc_series = []

    for l, p in zip(load_kW, pv_kW):
        net = l - p
        if net > 0 and soc > 0:
            discharge = min(batt_power, soc / timestep_hr, net)
            soc -= discharge * timestep_hr
            dispatch.append(-discharge)
        elif net < 0 and soc < batt_capacity:
            charge = min(batt_power, (batt_capacity - soc) / timestep_hr, -net)
            soc += charge * timestep_hr * eff
            dispatch.append(charge)
        else:
            dispatch.append(0)
        soc_series.append(soc)

    return {
        "bess_dispatch_kW": pd.Series(dispatch, index=load_kW.index),
        "soc_kWh": pd.Series(soc_series, index=load_kW.index)
    }