# ----------------------
# load_profile.py
# ----------------------

import pandas as pd

def load_demand_profile(file, resolution: str = "15min") -> pd.DataFrame:
    """
    Load a CSV file uploaded via Streamlit with a timestamp column and either
    'load_kW' or 'energy_kWh'. If only energy is provided, convert it to power.

    Args:
        file: File-like object from st.file_uploader
        resolution: '15min' or '60min' (used for conversion if needed)

    Returns:
        pd.DataFrame with timestamp index and power_kW column
    """
    df = pd.read_csv(file, parse_dates=["timestamp"])
    df = df.set_index("timestamp")

    if "power_kW" not in df.columns:
        if "energy_kWh" in df.columns:
            interval_minutes = int(resolution.replace("min", ""))
            df["power_kW"] = df["energy_kWh"] * (60 / interval_minutes)
        else:
            raise ValueError("CSV must have either 'power_kW' or 'energy_kWh' column.")

    df = df[["power_kW"]].sort_index()
    return df