# ----------------------
# parse_inputs.py
# ----------------------

def get_config_from_user_input(user_input: dict) -> dict:
    """
    Normalize and validate user inputs into a structured config dictionary
    used throughout the simulation engine.

    Expected keys in user_input:
    - pv: {kwp_pref, shading_factor}
    - bess: {capacity_kwh, power_kw}
    - ev: {fleet_size, battery_capacity_kwh, charging_window}

    Returns:
        config (dict): structured and validated configuration dictionary
    """

    # PV configuration
    pv_config = {
        "kwp_pref": user_input.get("pv", {}).get("kwp_pref", 100),
        "shading_factor": user_input.get("pv", {}).get("shading_factor", 1.0),
        "orientation": user_input.get("pv", {}).get("orientation", "south"),  # Placeholder
        "tilt": user_input.get("pv", {}).get("tilt", 30),                     # Placeholder
    }

    # Battery configuration
    bess_config = {
        "capacity_kwh": user_input.get("bess", {}).get("capacity_kwh", 0),
        "power_kw": user_input.get("bess", {}).get("power_kw", 0),
        "round_trip_efficiency": 0.9,  # Default assumption
    }

    # EV charging configuration
    ev_config = {
        "fleet_size": user_input.get("ev", {}).get("fleet_size", 0),
        "battery_capacity_kwh": user_input.get("ev", {}).get("battery_capacity_kwh", 50),
        "charging_window": user_input.get("ev", {}).get("charging_window", [9, 17]),
    }

    # Combine into top-level config
    config = {
        "pv": pv_config,
        "bess": bess_config,
        "ev": ev_config,
        "site": user_input.get("site", {}),
        "priorities": user_input.get("priorities", []),
        "costs": user_input.get("costs", {}),
        "constraints": user_input.get("constraints", {}),
    }

    return config