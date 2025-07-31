# ----------------------
# kpi_module.py
# ----------------------

import pandas as pd

def calculate_kpis(results: dict) -> dict:
    """
    Compute performance KPIs from simulation results.

    Args:
        results (dict): output from run_optimization

    Returns:
        dict: KPI values like import, generation, self-consumption, peak
    """
    pv = results["pv"]
    ev = results["ev"]
    bess = results["bess"]
    net_grid = results["net_grid_kW"]

    timestep_hr = (pv.index[1] - pv.index[0]).seconds / 3600

    total_import = net_grid[net_grid > 0].sum() * timestep_hr
    total_generation = pv.sum() * timestep_hr
    self_consumed = (pv - net_grid).clip(lower=0).sum() * timestep_hr

    kpis = {
        "total_grid_import_kWh": total_import,
        "total_solar_generation_kWh": total_generation,
        "solar_self_consumption_%": (self_consumed / total_generation * 100) if total_generation > 0 else 0,
        "peak_demand_kW": net_grid.max()
    }
    return kpis