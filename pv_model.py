# ----------------------
# pv_model.py
# ----------------------

import numpy as np
import pandas as pd

def simulate_pv_generation(config: dict, timestamps: pd.DatetimeIndex) -> pd.Series:
    """
    Generate synthetic PV output based on location, size, and daytime hours.
    Placeholder version using sine curve across daily daylight hours.

    Args:
        config (dict): includes PV size and shading factor
        timestamps (pd.DatetimeIndex): index of the simulation range

    Returns:
        pd.Series: PV output in kW at each timestamp
    """
    capacity_kw = config["pv"].get("kwp_pref", 100)
    shading = config["pv"].get("shading_factor", 1.0)

    generation = []
    for t in timestamps:
        hour = t.hour + t.minute / 60
        daily_factor = max(0, np.sin((hour - 6) / 12 * np.pi))  # peak at noon
        generation.append(capacity_kw * daily_factor * shading)

    return pd.Series(generation, index=timestamps, name="pv_generation_kW")