"""
scripts/audit_phase5a.py
Comprehensive diagnostic engine for Phase 5A audit.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DEBUG"] = "true"

from backend.data_layer import LOCATIONS_DATA
from app.services.risk import risk_service

cache_file = os.path.join(os.path.dirname(__file__), "extended_archive_cache.json")
with open(cache_file, "r", encoding="utf-8") as f:
    archive_results = json.load(f)

times = archive_results[0]["hourly"]["time"]
idx_start = times.index("2026-06-22T00:00")
idx_event_peak = times.index("2026-07-06T18:00")
idx_end = times.index("2026-07-08T23:00")

def calc_w_storage(precips, t_idx, tau=60.0):
    w = 0.0
    for dt in range(min(t_idx + 1, 336)):
        p = float(precips[t_idx - dt] or 0.0)
        w += p * math.exp(-dt / tau)
    return round(w, 1)

def eval_loc_raw(loc, r_1h, r_24h, r_48h, r_72h, w_storage, sm01, sm39, sm927):
    return risk_service.predict({
        "location_id": loc["id"],
        "hazard_type": loc["current_hazard"],
        "rain_1h_mm": r_1h,
        "rain_24h_mm": r_24h,
        "rain_48h_mm": r_48h,
        "rain_72h_mm": r_72h,
        "api_mm": w_storage,
        "soil_moisture_0_to_1cm": sm01,
        "soil_moisture_3_to_9cm": sm39,
        "soil_moisture_9_to_27cm": sm927,
        "slope_deg": loc["slope_deg"],
        "elevation_m": loc["elevation_m"],
        "drainage_proximity_m": loc["drainage_proximity_m"],
        "disturbed_slope_prox_m": loc.get("disturbed_slope_prox_m", 80.0),
        "veg_cover_pct": loc.get("veg_cover_pct", 50.0)
    })

def eval_loc_time(loc, loc_hourly, t_idx):
    p = loc_hourly["precipitation"]
    sm01_series = loc_hourly.get("soil_moisture_0_to_1cm", [])
    sm39_series = loc_hourly.get("soil_moisture_3_to_9cm", [])
    sm927_series = loc_hourly.get("soil_moisture_9_to_27cm", [])
    
    r_1h = float(p[t_idx] or 0.0)
    r_24h = sum(float(x or 0.0) for x in p[max(0, t_idx - 23):t_idx + 1])
    r_48h = sum(float(x or 0.0) for x in p[max(0, t_idx - 47):t_idx + 1])
    r_72h = sum(float(x or 0.0) for x in p[max(0, t_idx - 71):t_idx + 1])
    w_storage = calc_w_storage(p, t_idx, tau=60.0)
    
    s01 = float(sm01_series[t_idx] or 0.45) if t_idx < len(sm01_series) else 0.45
    s39 = float(sm39_series[t_idx] or 0.45) if t_idx < len(sm39_series) else 0.45
    s927 = float(sm927_series[t_idx] or 0.45) if t_idx < len(sm927_series) else 0.45

    return eval_loc_raw(loc, r_1h, r_24h, r_48h, r_72h, w_storage, s01, s39, s927)

print("=" * 140)
print("PHASE 5A.1: EXTENDED 14-DAY REPLAY (12-Hourly Frames from 2026-06-22 to 2026-07-08)")
print("=" * 140)

twelve_hourly = list(range(idx_start, idx_end + 1, 12))
header_labels = [times[t][5:16].replace("T", " ") for t in twelve_hourly]

# Compute hours >= 70 prior to 2026-07-06 18:00
hours_above_70 = {loc["id"]: 0 for loc in LOCATIONS_DATA}
for t in range(idx_start, idx_event_peak + 1):
    for loc_idx, loc in enumerate(LOCATIONS_DATA):
        loc_hourly = archive_results[loc_idx]["hourly"]
        pred = eval_loc_time(loc, loc_hourly, t)
        if pred["risk_score"] >= 70:
            hours_above_70[loc["id"]] += 1

total_window_hours = idx_event_peak - idx_start

# Compute 12-hourly score matrix
matrix = {}
for loc_idx, loc in enumerate(LOCATIONS_DATA):
    loc_hourly = archive_results[loc_idx]["hourly"]
    scores = []
    for t in twelve_hourly:
        pred = eval_loc_time(loc, loc_hourly, t)
        scores.append(pred["risk_score"])
    matrix[loc["id"]] = scores

# Print compact summary of extended replay: sample every 24h for visual table plus key storm steps
print(f"{'Location ID':<22} " + " ".join(f"{times[t][5:10]:>5}" for t in range(idx_start, idx_end + 1, 24)))
for loc in LOCATIONS_DATA:
    row = [f"{loc['id']:<22}"]
    loc_hourly = archive_results[LOCATIONS_DATA.index(loc)]["hourly"]
    for t in range(idx_start, idx_end + 1, 24):
        pred = eval_loc_time(loc, loc_hourly, t)
        row.append(f"{pred['risk_score']:>5}")
    print(" ".join(row))

print("\n--- HOURS ABOVE 70 BEFORE 2026-07-06 18:00 IST (Total window: %d hours) ---" % total_window_hours)
for loc in LOCATIONS_DATA:
    hrs = hours_above_70[loc["id"]]
    pct = (hrs / total_window_hours) * 100.0
    print(f"  {loc['id']:<24}: {hrs:>3} hours ({pct:>5.1f}% of pre-storm window)")


# =========================================================================
# PHASE 5A.2: SENSITIVITY TESTS PER LOCATION
# =========================================================================
print("\n" + "=" * 140)
print("PHASE 5A.2 (a): SENSITIVITY TO 24-HOUR RAINFALL (Under Dry, Moderate, Saturated Antecedent Conditions)")
print("=" * 140)

rain_levels = [0.0, 25.0, 50.0, 100.0, 150.0, 200.0, 300.0]

for regime_name, w_val, sm_val in [
    ("Dry (W=10mm, SM=30%)", 10.0, 0.16),
    ("Moderate (W=120mm, SM=60%)", 120.0, 0.32),
    ("Saturated (W=350mm, SM=90%)", 350.0, 0.50)
]:
    print(f"\n--- Regime: {regime_name} ---")
    print(f"{'Location ID':<22} " + " ".join(f"{r:>6.0f}mm" for r in rain_levels))
    for loc in LOCATIONS_DATA:
        row = [f"{loc['id']:<22}"]
        for r24 in rain_levels:
            r1 = min(r24, r24 / 10.0)
            r48 = r24 * 1.3
            r72 = r24 * 1.5
            pred = eval_loc_raw(loc, r1, r24, r48, r72, w_val, sm_val, sm_val, sm_val)
            row.append(f"{pred['risk_score']:>8}")
        print(" ".join(row))

print("\n" + "=" * 140)
print("PHASE 5A.2 (b): SENSITIVITY TO ANTECEDENT WETNESS W(t) (With 24h Rainfall Fixed at 100 mm)")
print("=" * 140)

w_levels = [0.0, 50.0, 100.0, 200.0, 300.0, 450.0, 600.0]
print(f"{'Location ID':<22} " + " ".join(f"{w:>6.0f}mm" for w in w_levels))
for loc in LOCATIONS_DATA:
    row = [f"{loc['id']:<22}"]
    for w in w_levels:
        # Scale baseline volumetric moisture with antecedent store:
        sm_v = min(0.53, 0.18 + (w / 600.0) * 0.34)
        pred = eval_loc_raw(loc, 10.0, 100.0, 130.0, 150.0, w, sm_v, sm_v, sm_v)
        row.append(f"{pred['risk_score']:>8}")
    print(" ".join(row))


# =========================================================================
# PHASE 5A.3: FACTOR OF SAFETY AUDIT (Dry, Moderate, Saturated)
# =========================================================================
print("\n" + "=" * 140)
print("PHASE 5A.3: GEOTECHNICAL FACTOR OF SAFETY AUDIT")
print("=" * 140)
print(f"{'Location ID':<22} {'Hazard':<12} {'Slope':<7} {'CutProx(m)':<11} {'Veg(%)':<8} {'FS Dry':<9} {'FS Mod':<9} {'FS Sat':<9} {'Dry Inconsistency?':<20}")
print("-" * 140)

for loc in LOCATIONS_DATA:
    slope = loc["slope_deg"]
    cut_prox = loc.get("disturbed_slope_prox_m", 80.0)
    veg = loc.get("veg_cover_pct", 50.0)
    hazard = loc["current_hazard"]

    p_dry = eval_loc_raw(loc, 0.0, 0.0, 0.0, 0.0, 5.0, 0.15, 0.15, 0.15)
    p_mod = eval_loc_raw(loc, 5.0, 50.0, 70.0, 80.0, 100.0, 0.35, 0.35, 0.35)
    p_sat = eval_loc_raw(loc, 15.0, 200.0, 300.0, 450.0, 400.0, 0.52, 0.52, 0.52)

    fs_dry = p_dry.get("factor_of_safety")
    fs_mod = p_mod.get("factor_of_safety")
    fs_sat = p_sat.get("factor_of_safety")

    fs_d_str = f"{fs_dry:.2f}" if fs_dry is not None else "N/A (Hydro)"
    fs_m_str = f"{fs_mod:.2f}" if fs_mod is not None else "N/A (Hydro)"
    fs_s_str = f"{fs_sat:.2f}" if fs_sat is not None else "N/A (Hydro)"

    flag = "YES (FS < 1.0) !!" if (fs_dry is not None and fs_dry < 1.0) else "NO (Stable)"
    print(f"{loc['id']:<22} {hazard:<12} {slope:<7.1f} {cut_prox:<11.1f} {veg:<8.1f} {fs_d_str:<9} {fs_m_str:<9} {fs_s_str:<9} {flag:<20}")


# =========================================================================
# PHASE 5A.4: SCORE DISTRIBUTION AT PEAK FRAME
# =========================================================================
print("\n" + "=" * 140)
print("PHASE 5A.4: SCORE DISTRIBUTION AT PEAK FRAME (2026-07-06 18:00 IST)")
print("=" * 140)

peak_scores = {}
loc_hourly_0 = archive_results[0]["hourly"]
for loc_idx, loc in enumerate(LOCATIONS_DATA):
    lh = archive_results[loc_idx]["hourly"]
    pred = eval_loc_time(loc, lh, idx_event_peak)
    peak_scores[loc["id"]] = pred["risk_score"]

for lid, sc in sorted(peak_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"  {lid:<24}: {sc:>3}/100")

ge_95 = [lid for lid, sc in peak_scores.items() if sc >= 95]
print(f"\nLocations at or above 95: {len(ge_95)}/12 ({', '.join(ge_95)})")


# =========================================================================
# PHASE 5A.6: PATAN VILLAGE AUDIT
# =========================================================================
print("\n" + "=" * 140)
print("PHASE 5A.6: PATAN VILLAGE DIAGNOSTIC AUDIT")
print("=" * 140)
patan_loc = next(l for l in LOCATIONS_DATA if l["id"] == "patan_village")
print(f"Patan Village Terrain Parameters:")
print(f"  Elevation:              {patan_loc['elevation_m']} m")
print(f"  Slope:                  {patan_loc['slope_deg']} degrees")
print(f"  Catchment:              {patan_loc.get('upstream_catchment_km2')} km2")
print(f"  Drainage Proximity:     {patan_loc['drainage_proximity_m']} m")
print(f"  Disturbed Prox (Cut):   {patan_loc.get('disturbed_slope_prox_m')} m")
print(f"  Vegetation Cover:       {patan_loc.get('veg_cover_pct')}%")
print(f"  Designated Hazard:      {patan_loc['current_hazard']}")

p_patan_dry = eval_loc_raw(patan_loc, 0.0, 0.0, 0.0, 0.0, 10.0, 0.15, 0.15, 0.15)
p_patan_sat = eval_loc_raw(patan_loc, 15.0, 200.0, 350.0, 500.0, 450.0, 0.52, 0.52, 0.52)
p_patan_event = eval_loc_time(patan_loc, archive_results[LOCATIONS_DATA.index(patan_loc)]["hourly"], idx_event_peak)

print(f"\nPatan Geotechnical Factor of Safety:")
print(f"  FS (Dry Conditions):         {p_patan_dry.get('factor_of_safety')} (Score: {p_patan_dry['risk_score']})")
print(f"  FS (Saturated Conditions):   {p_patan_sat.get('factor_of_safety')} (Score: {p_patan_sat['risk_score']})")
print(f"  FS at Event Peak (July 6):   {p_patan_event.get('factor_of_safety')} (Score: {p_patan_event['risk_score']})")
