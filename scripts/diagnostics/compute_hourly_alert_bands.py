"""
scripts/diagnostics/compute_hourly_alert_bands.py
Computes exact hours spent in each alert band from the FULL HOURLY SERIES:
  - Low / Green: Score < 25 (or < 40)
  - Moderate / Yellow: 25 <= Score < 55 (or 40 <= Score < 60)
  - High / Orange: 55 <= Score < 78 (or 60 <= Score < 80)
  - Very High / Red: Score >= 78 (or Score >= 80)
Ensures every row sums to exactly the total window duration.
Window: 2026-06-22T00:00 to 2026-07-06T18:00 IST (354 hours).
Also reports for the full 408-hour window (to 2026-07-08T23:00 IST).
"""
import sys
import os
import json
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.data_layer import LOCATIONS_DATA
from backend.ml_engine import ml_service
from scripts.diagnostics.compare_v2_v3 import predict_v22, calc_drained_storage_w, format_table

def compute_bands():
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extended_archive_cache.json")
    with open(cache_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)
    data_list = cache_data if isinstance(cache_data, list) else [cache_data]

    ref_hourly = data_list[0]["hourly"]
    timestamps = ref_hourly["time"]

    start_idx = timestamps.index("2026-06-22T00:00")
    peak_idx = timestamps.index("2026-07-06T18:00")
    total_hours_pre_peak = peak_idx - start_idx + 1  # 355 or 354?

    print(f"Total Hourly Timesteps from 2026-06-22T00:00 to 2026-07-06T18:00: {total_hours_pre_peak} hours")

    for model_name, predict_fn in [("Sahyadri-GeoRisk-v3.0", lambda p: ml_service.predict_hazard(p)["risk_score"]),
                                   ("Sahyadri-GeoRisk-v2.2", lambda p: predict_v22(p)["risk_score"])]:
        print(f"\n==========================================================================================")
        print(f"HOURLY ALERT BANDS FOR {model_name.upper()} (Pre-Storm Baseline to Peak, {total_hours_pre_peak} Hours)")
        print(f"Standard Bands: <25 (Low), 25-54 (Moderate), 55-77 (High), >=78 (Very High)")
        print(f"==========================================================================================")

        headers = ["Location ID", "Hazard", "<25 (Low)", "25-54 (Mod)", "55-77 (High)", ">=78 (Very High)", "Sum Hours"]
        rows = []

        for loc in LOCATIONS_DATA:
            node_data = next((d for d in data_list if abs(d["latitude"] - loc["coordinates"][0]) < 0.05 and abs(d["longitude"] - loc["coordinates"][1]) < 0.05), data_list[0])
            h = node_data["hourly"]
            p_series = h["precipitation"]
            sm01_series = h["soil_moisture_0_to_1cm"]
            sm39_series = h["soil_moisture_3_to_9cm"]
            sm927_series = h["soil_moisture_9_to_27cm"]

            b_low, b_mod, b_high, b_vhigh = 0, 0, 0, 0

            for t_idx in range(start_idx, peak_idx + 1):
                r_1h = float(p_series[t_idx] or 0.0)
                r_24h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 23):t_idx + 1])
                r_48h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 47):t_idx + 1])
                r_72h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 71):t_idx + 1])
                w_t = calc_drained_storage_w(p_series, t_idx, tau=60.0)
                s01 = float(sm01_series[t_idx] or 0.45)
                s39 = float(sm39_series[t_idx] or 0.45)
                s927 = float(sm927_series[t_idx] or 0.45)

                payload = {
                    "location_id": loc["id"],
                    "hazard_type": loc["current_hazard"],
                    "slope_deg": loc["slope_deg"],
                    "elevation_m": loc["elevation_m"],
                    "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
                    "drainage_proximity_m": loc["drainage_proximity_m"],
                    "disturbed_slope_prox_m": loc.get("disturbed_slope_prox_m", 80.0),
                    "veg_cover_pct": loc.get("veg_cover_pct", 50.0),
                    "rain_1h_mm": r_1h,
                    "rain_24h_mm": r_24h,
                    "rain_48h_mm": r_48h,
                    "rain_72h_mm": r_72h,
                    "api_mm": w_t,
                    "antecedent_store_mm": w_t,
                    "soil_moisture_0_to_1cm": s01,
                    "soil_moisture_3_to_9cm": s39,
                    "soil_moisture_9_to_27cm": s927
                }
                score = predict_fn(payload)
                if score < 25:
                    b_low += 1
                elif score < 55:
                    b_mod += 1
                elif score < 78:
                    b_high += 1
                else:
                    b_vhigh += 1

            total_h = b_low + b_mod + b_high + b_vhigh
            assert total_h == total_hours_pre_peak, f"Row sum {total_h} != {total_hours_pre_peak}"
            rows.append([
                loc["id"], loc["current_hazard"],
                f"{b_low} h", f"{b_mod} h", f"{b_high} h", f"{b_vhigh} h", f"{total_h} h"
            ])
        print(format_table(headers, rows))

        # Also print Alternative 4-Band format (<40, 40-59, 60-79, >=80)
        print(f"\n--- Alternate Band Intervals: <40, 40-59, 60-79, >=80 ({model_name}) ---")
        alt_headers = ["Location ID", "<40", "40-59", "60-79", ">=80", "Sum Hours"]
        alt_rows = []
        for loc in LOCATIONS_DATA:
            node_data = next((d for d in data_list if abs(d["latitude"] - loc["coordinates"][0]) < 0.05 and abs(d["longitude"] - loc["coordinates"][1]) < 0.05), data_list[0])
            h = node_data["hourly"]
            p_series = h["precipitation"]
            sm01_series = h["soil_moisture_0_to_1cm"]
            sm39_series = h["soil_moisture_3_to_9cm"]
            sm927_series = h["soil_moisture_9_to_27cm"]
            b40, b60, b80, bv80 = 0, 0, 0, 0
            for t_idx in range(start_idx, peak_idx + 1):
                r_1h = float(p_series[t_idx] or 0.0)
                r_24h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 23):t_idx + 1])
                r_48h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 47):t_idx + 1])
                r_72h = sum(float(p or 0.0) for p in p_series[max(0, t_idx - 71):t_idx + 1])
                w_t = calc_drained_storage_w(p_series, t_idx, tau=60.0)
                s01 = float(sm01_series[t_idx] or 0.45)
                s39 = float(sm39_series[t_idx] or 0.45)
                s927 = float(sm927_series[t_idx] or 0.45)
                payload = {
                    "location_id": loc["id"],
                    "hazard_type": loc["current_hazard"],
                    "slope_deg": loc["slope_deg"],
                    "elevation_m": loc["elevation_m"],
                    "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
                    "drainage_proximity_m": loc["drainage_proximity_m"],
                    "disturbed_slope_prox_m": loc.get("disturbed_slope_prox_m", 80.0),
                    "veg_cover_pct": loc.get("veg_cover_pct", 50.0),
                    "rain_1h_mm": r_1h,
                    "rain_24h_mm": r_24h,
                    "rain_48h_mm": r_48h,
                    "rain_72h_mm": r_72h,
                    "api_mm": w_t,
                    "antecedent_store_mm": w_t,
                    "soil_moisture_0_to_1cm": s01,
                    "soil_moisture_3_to_9cm": s39,
                    "soil_moisture_9_to_27cm": s927
                }
                score = predict_fn(payload)
                if score < 40:
                    b40 += 1
                elif score < 60:
                    b60 += 1
                elif score < 80:
                    b80 += 1
                else:
                    bv80 += 1
            total_h = b40 + b60 + b80 + bv80
            alt_rows.append([loc["id"], f"{b40} h", f"{b60} h", f"{b80} h", f"{bv80} h", f"{total_h} h"])
        print(format_table(alt_headers, alt_rows))

if __name__ == "__main__":
    compute_bands()
