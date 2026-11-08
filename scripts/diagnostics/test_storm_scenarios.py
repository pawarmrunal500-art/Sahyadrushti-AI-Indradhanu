"""
scripts/diagnostics/test_storm_scenarios.py
Coupled Storm Scenario Sensitivity Diagnostic:
Couples 24h storm rainfall to:
  1. Drained antecedent store W(t) [mm] via 24h recession integral
  2. Multi-layer volumetric soil moisture theta via vadose infiltration
Evaluates all 12 pilot locations across calm vs wet pre-history under 50, 100, 200, and 300 mm storms.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.services.risk import risk_service
from backend.data_layer import LOCATIONS_DATA

def format_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    data_lines = [" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) for row in rows]
    return f"{header_line}\n{sep_line}\n" + "\n".join(data_lines)

def evaluate_coupled_scenario(prehistory: str, p24: float):
    """
    Coupled infiltration parameters (explicitly uncalibrated assumptions):
      - Deccan Trap vadose saturation porosity theta_sat = 0.53 (53% vol moisture)
      - Calm pre-history: base W = 10.0 mm, theta_base = 0.25 (25% vol moisture)
      - Wet pre-history: base W = 200.0 mm, theta_base = 0.44 (44% vol moisture)
      - Coupling:
          W(t) = W_base + 0.85 * p24 (recession over 24h with tau=60h)
          theta = min(0.53, theta_base + (p24 / 400.0) * (0.53 - theta_base))
    """
    if prehistory == "calm":
        w_base = 10.0
        sm_base = 0.25
        p48 = p24 + 2.0
    else:  # wet
        w_base = 200.0
        sm_base = 0.44
        p48 = p24 + 40.0

    w_t = w_base + 0.85 * p24
    sm = min(0.53, sm_base + (p24 / 400.0) * (0.53 - sm_base))

    results = {}
    for loc in LOCATIONS_DATA:
        payload = {
            "location_id": loc["id"],
            "hazard_type": loc.get("current_hazard", "landslide"),
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
            "drainage_proximity_m": loc["drainage_proximity_m"],
            "disturbed_slope_prox_m": loc.get("disturbed_slope_prox_m", 80.0),
            "veg_cover_pct": loc.get("veg_cover_pct", 50.0),
            "rain_1h": p24 * 0.12,
            "rain_24h": p24,
            "rain_48h": p48,
            "api_mm": w_t,
            "antecedent_store_mm": w_t,
            "soil_moisture_0_to_1cm": sm,
            "soil_moisture_3_to_9cm": sm,
            "soil_moisture_9_to_27cm": sm
        }
        pred = risk_service.engine.predict_hazard(payload)
        results[loc["id"]] = {
            "score": pred["risk_score"],
            "fs": pred.get("factor_of_safety"),
            "capped": pred.get("score_capped", False)
        }
    return results, w_t, sm

def run_all():
    print("=" * 110)
    print("COUPLED STORM SCENARIO SENSITIVITY TABLE (Sahyadri-GeoRisk-v2.2)")
    print("Coupled Infiltration Model: W(t) = W_base + 0.85*P24, theta = min(0.53, theta_base + (P24/400)*(0.53 - theta_base))")
    print("=" * 110)

    p_values = [50.0, 100.0, 200.0, 300.0]

    for prehistory in ["calm", "wet"]:
        print(f"\n--- PRE-HISTORY: {prehistory.upper()} (Base W = {'10 mm' if prehistory == 'calm' else '200 mm'}, Base SM = {'25%' if prehistory == 'calm' else '44%'}) ---")
        headers = ["Location ID", "Hazard", "Slope (deg)"] + [f"{int(p)}mm (W, SM)" for p in p_values]
        
        # Pre-compute
        scenarios = {p: evaluate_coupled_scenario(prehistory, p) for p in p_values}
        
        rows = []
        for loc in LOCATIONS_DATA:
            lid = loc["id"]
            row = [lid, loc.get("current_hazard"), f"{loc['slope_deg']:.1f}"]
            for p in p_values:
                res, w_t, sm = scenarios[p]
                sc = res[lid]["score"]
                fs = res[lid]["fs"]
                cap = "*" if res[lid]["capped"] else ""
                fs_str = f" (FS={fs:.2f})" if fs is not None else ""
                row.append(f"{sc}{cap}{fs_str}")
            rows.append(row)
        
        print(format_table(headers, rows))
        print("Note: '*' denotes score capped at safety ceiling (96 for flood, 98 for geotechnical).")

if __name__ == "__main__":
    run_all()
