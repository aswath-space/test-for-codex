# ----------------------
# ev_model.py
# ----------------------

import pandas as pd
import numpy as np

def simulate_ev_charging(config: dict, timestamps: pd.DatetimeIndex) -> pd.Series:
    """
    Estimate EV fleet charging demand during specified hours.

    Args:
        config (dict): includes EV fleet size, battery size, charging window
        timestamps (pd.DatetimeIndex): simulation range

    Returns:
        pd.Series: EV charging power in kW at each timestamp
    """
    fleet_size = config["ev"].get("fleet_size", 10)
    batt_kwh = config["ev"].get("battery_capacity_kwh", 50)
    charge_start, charge_end = config["ev"].get("charging_window", [9, 17])

    total_energy_kwh = fleet_size * batt_kwh
    charge_hours = charge_end - charge_start
    charge_power = total_energy_kwh / charge_hours  # Total charging power spread evenly

    power_series = []
    for t in timestamps:
        hour = t.hour + t.minute / 60
        if charge_start <= hour < charge_end:
            power_series.append(charge_power)
        else:
            power_series.append(0)

    return pd.Series(power_series, index=timestamps, name="ev_charging_kW")
