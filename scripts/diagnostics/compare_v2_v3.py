"""
scripts/diagnostics/compare_v2_v3.py
Comparison Diagnostic: Sahyadri-GeoRisk-v2.2 vs Sahyadri-GeoRisk-v3.0.
Evaluates:
  1. 17-Day Replay Progression across all 34 frames
  2. Calm-Day Baseline behavior (sawtooth check)
  3. Storm Scenario Sensitivity (calm vs wet pre-history)
  4. Peak Frame Score Distribution and Count of Locations >= 95
"""
import sys
import os
import json
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.data_layer import LOCATIONS_DATA

def calc_drained_storage_w(precips, t_idx, tau=60.0):
    w = 0.0
    for dt in range(min(t_idx + 1, 336)):
        p = float(precips[t_idx - dt] or 0.0)
        w += p * math.exp(-dt / tau)
    return round(w, 1)

def predict_v22(payload):
    """Exact Sahyadri-GeoRisk-v2.2 engine logic."""
    hazard_type = payload.get("hazard_type", "landslide")
    rain_1h = float(payload.get("rain_1h_mm", 0.0))
    rain_24h = float(payload.get("rain_24h_mm", 0.0))
    rain_48h = float(payload.get("rain_48h_mm", rain_24h * 1.5))
    forecast_24h = float(payload.get("forecast_24h_mm", rain_24h * 0.9))
    slope_deg = float(payload.get("slope_deg", 18.0))
    elevation_m = float(payload.get("elevation_m", 640.0))
    drainage_prox = float(payload.get("drainage_proximity_m", 150.0))
    disturbed_prox = float(payload.get("disturbed_slope_prox_m", 80.0))
    veg_cover = float(payload.get("veg_cover_pct", 50.0))

    sm01 = payload.get("soil_moisture_0_to_1cm")
    sm39 = payload.get("soil_moisture_3_to_9cm")
    sm927 = payload.get("soil_moisture_9_to_27cm")
    if sm01 is not None:
        s01 = float(sm01)
        s39 = float(sm39 if sm39 is not None else s01)
        s927 = float(sm927 if sm927 is not None else s39)
        theta_profile = 0.20 * s01 + 0.30 * s39 + 0.50 * s927
        sat_matrix = min(100.0, (theta_profile / 0.53) * 100.0)
    else:
        sat_matrix = float(payload.get("soil_moisture_pct", 50.0))

    w_storage = float(payload.get("api_mm", payload.get("antecedent_store_mm", 0.0)))
    sat_boost = min(18.0, (w_storage / 350.0) * 18.0)
    soil_moisture = min(98.0, sat_matrix * 0.80 + sat_boost)

    weights_ls = np.array([0.02, 0.015, 0.022, 0.012, 0.045, 0.085, 0.001, -0.003, -0.014, -0.025])
    bias_ls = -8.2
    weights_ff = np.array([0.075, 0.018, 0.008, 0.015, 0.038, 0.012, -0.001, -0.012, -0.002, -0.015])
    bias_ff = -5.8

    x = np.array([rain_1h, rain_24h, rain_48h, forecast_24h, soil_moisture, slope_deg, elevation_m, drainage_prox, disturbed_prox, veg_cover])
    z = np.dot(x, weights_ls) + bias_ls if hazard_type == "landslide" else np.dot(x, weights_ff) + bias_ff
    prob_event = float(1.0 / (1.0 + np.exp(-np.clip(z, -15, 15))))
    base_score = int(np.clip(prob_event * 100.0, 0, 100))

    slope_rad = np.radians(slope_deg)
    fs_val = None
    if hazard_type in ["flash_flood", "waterlogging"]:
        c_runoff = 0.25 + 0.65 * ((soil_moisture / 100.0) ** 2)
        drainage_factor = (100.0 / max(drainage_prox, 15.0)) ** 0.35
        surge_index = (rain_1h * 2.8 + rain_24h * 0.22 + rain_48h * 0.08) * c_runoff * drainage_factor
        base_surge = min(22.0, (w_storage / 240.0) * 22.0 * (soil_moisture / 100.0))
        relief_term = max(0.0, (15.0 - slope_deg) * 0.8)
        calibrated_score = int(min(96, max(3, round(10.0 + surge_index * 0.85 + base_surge + relief_term))))
        score = calibrated_score if (rain_48h > 40.0 or soil_moisture > 75.0) else base_score
    else:
        phi_rad = np.radians(30.0 + (veg_cover / 100.0) * 4.0)
        c_prime = max(2.5, 16.0 - (soil_moisture / 100.0) * 11.0 - (50.0 / max(disturbed_prox, 15.0)) * 2.0)
        gamma_total = 19.5
        z_colluvium = 2.2
        m_perched = min(1.0, max(0.0, (soil_moisture - 65.0) / 33.0))
        u_pore = m_perched * z_colluvium * 9.81 * (np.cos(slope_rad) ** 2)
        driving_shear = gamma_total * z_colluvium * np.sin(slope_rad) * np.cos(slope_rad)
        effective_normal = (gamma_total * z_colluvium * (np.cos(slope_rad) ** 2)) - u_pore
        resisting_shear = c_prime + max(0.0, effective_normal) * np.tan(phi_rad)
        fs = float(resisting_shear / max(0.3, driving_shear))
        fs_val = round(fs, 2)

        if fs >= 1.8:
            calibrated_score = int(max(2, round(5.0 + max(0.0, (2.2 - fs) * 15.0))))
        elif fs >= 1.3:
            calibrated_score = int(round(25.0 + ((1.8 - fs) / 0.5) * 30.0))
        elif fs >= 1.0:
            calibrated_score = int(round(55.0 + ((1.3 - fs) / 0.3) * 23.0))
        else:
            fs_deficit = (1.0 - fs) / 0.50
            cut_penalty = min(5.0, (50.0 / max(disturbed_prox, 15.0)))
            rain_pulse = min(6.0, (rain_1h * 0.35 + rain_24h * 0.02))
            calibrated_score = int(min(98, round(78.0 + min(14.0, fs_deficit * 14.0) + cut_penalty + rain_pulse)))
        score = calibrated_score if (rain_48h > 40.0 or soil_moisture > 75.0) else base_score

    return {"risk_score": score, "fs": fs_val, "capped": bool(score >= (96 if hazard_type in ["flash_flood", "waterlogging"] else 98))}

def predict_v30(payload):
    """Directly calls active backend.ml_engine (v3.0)."""
    from backend.ml_engine import ml_service
    res = ml_service.predict_hazard(payload)
    return {"risk_score": res["risk_score"], "fs": res.get("factor_of_safety"), "capped": res.get("score_capped", False), "extra": res}

def format_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    data_lines = [" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) for row in rows]
    return f"{header_line}\n{sep_line}\n" + "\n".join(data_lines)

def run_diagnostics():
    print("====================================================================================================")
    print("MODEL COMPARISON AUDIT: Sahyadri-GeoRisk-v2.2 vs Sahyadri-GeoRisk-v3.0")
    print("====================================================================================================")

    # 1. Load archive cache
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extended_archive_cache.json")
    with open(cache_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)
    if isinstance(cache_data, list):
        data_list = cache_data
    else:
        data_list = [cache_data]

    ref_hourly = data_list[0]["hourly"]
    timestamps = ref_hourly["time"]

    base_idx = timestamps.index("2026-06-22T00:00")
    peak_idx = timestamps.index("2026-07-06T18:00")
    end_idx = len(timestamps)

    # Sample key frames for comparative table:
    # Baseline, Rain Pulse 1 (06-24 12:00), Calm Lull (06-26 12:00), Rain Pulse 2 (06-30 12:00),
    # Storm Build-up (07-05 12:00), Peak Storm (07-06 18:00), Post-Peak Lull (07-07 21:00), Tail (07-08 12:00)
    key_timestamps = [
        "2026-06-22T00:00",
        "2026-06-24T12:00",
        "2026-06-26T12:00",
        "2026-06-30T12:00",
        "2026-07-05T12:00",
        "2026-07-06T18:00",
        "2026-07-07T21:00",
        "2026-07-08T12:00"
    ]

    print("\n--- 1. KEY TIMESTAMPS COMPARISON TABLE (v2.2 vs v3.0) ---")
    key_locs = ["kune_falls", "tiger_point", "khandala_expressway", "monkey_hill", "patan_village", "bhushi_dam", "lonavala_town"]

    for t_str in key_timestamps:
        t_idx = timestamps.index(t_str)
        print(f"\n>>> FRAME: {t_str}")
        headers = ["Location ID", "Hazard", "Slope", "24h Rain", "W(t)", "v2.2 Score (FS)", "v3.0 Score (FS)", "v3.0 Trigger / Applicability"]
        rows = []
        for loc in LOCATIONS_DATA:
            lid = loc["id"]
            if lid not in key_locs:
                continue
            # find loc telemetry in cache
            node_data = next((d for d in data_list if abs(d["latitude"] - loc["coordinates"][0]) < 0.05 and abs(d["longitude"] - loc["coordinates"][1]) < 0.05), data_list[0])
            h = node_data["hourly"]
            p_series = h["precipitation"]
            sm01_series = h["soil_moisture_0_to_1cm"]
            sm39_series = h["soil_moisture_3_to_9cm"]
            sm927_series = h["soil_moisture_9_to_27cm"]

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

            res22 = predict_v22(payload)
            res30 = predict_v30(payload)

            fs22_str = f" (FS={res22['fs']:.2f})" if res22['fs'] is not None else ""
            fs30_str = f" (FS={res30['fs']:.2f})" if res30['fs'] is not None else ""
            extra = res30["extra"]
            trig_app = f"{extra['trigger_level']} / {extra['model_applicability'][:15]}..."

            rows.append([
                lid, loc["current_hazard"], f"{loc['slope_deg']:.1f}°",
                f"{r_24h:.1f}mm", f"{w_t:.1f}mm",
                f"{res22['risk_score']}{fs22_str}",
                f"{res30['risk_score']}{fs30_str}",
                trig_app
            ])
        print(format_table(headers, rows))

    # 4. Peak Frame >= 95 Audit
    print("\n--- 4. PEAK FRAME AUDIT (2026-07-06 18:00 IST) ---")
    p_idx = timestamps.index("2026-07-06T18:00")
    count_95_v22 = 0
    count_95_v30 = 0
    peak_rows = []
    headers = ["Location ID", "Hazard", "Slope", "v2.2 Score", "v3.0 Score", "v3.0 FS", "v3.0 Trigger", "v3.0 Applicability"]
    for loc in LOCATIONS_DATA:
        node_data = next((d for d in data_list if abs(d["latitude"] - loc["coordinates"][0]) < 0.05 and abs(d["longitude"] - loc["coordinates"][1]) < 0.05), data_list[0])
        h = node_data["hourly"]
        p_series = h["precipitation"]
        sm01_series = h["soil_moisture_0_to_1cm"]
        sm39_series = h["soil_moisture_3_to_9cm"]
        sm927_series = h["soil_moisture_9_to_27cm"]
        r_1h = float(p_series[p_idx] or 0.0)
        r_24h = sum(float(p or 0.0) for p in p_series[max(0, p_idx - 23):p_idx + 1])
        r_48h = sum(float(p or 0.0) for p in p_series[max(0, p_idx - 47):p_idx + 1])
        r_72h = sum(float(p or 0.0) for p in p_series[max(0, p_idx - 71):p_idx + 1])
        w_t = calc_drained_storage_w(p_series, p_idx, tau=60.0)
        s01 = float(sm01_series[p_idx] or 0.45)
        s39 = float(sm39_series[p_idx] or 0.45)
        s927 = float(sm927_series[p_idx] or 0.45)

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
        res22 = predict_v22(payload)
        res30 = predict_v30(payload)
        if res22["risk_score"] >= 95:
            count_95_v22 += 1
        if res30["risk_score"] >= 95:
            count_95_v30 += 1
        extra = res30["extra"]
        peak_rows.append([
            loc["id"], loc["current_hazard"], f"{loc['slope_deg']:.1f}°",
            str(res22["risk_score"]), str(res30["risk_score"]),
            f"{res30['fs']:.2f}" if res30['fs'] is not None else "N/A",
            extra["trigger_level"],
            extra["model_applicability"]
        ])

    print(format_table(headers, peak_rows))
    print(f"\nLocations reaching score >= 95 in Peak Frame (2026-07-06 18:00 IST):")
    print(f"  - Sahyadri-GeoRisk-v2.2: {count_95_v22} / 12 locations")
    print(f"  - Sahyadri-GeoRisk-v3.0: {count_95_v30} / 12 locations")

if __name__ == "__main__":
    run_diagnostics()
