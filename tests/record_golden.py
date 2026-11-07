"""
tests/record_golden.py
Record golden JSON fixtures from the live SAHYADRUSHTI AI backend.
Run against the UNTOUCHED prototype code to establish the API contract baseline.

Usage:
    python -m tests.record_golden
    # (from project root, with backend importable)
"""
import json
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

GOLDEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden")
os.makedirs(GOLDEN_DIR, exist_ok=True)

client = TestClient(app)


def save(name: str, response):
    """Save response JSON and status code to golden directory."""
    payload = {
        "status_code": response.status_code,
        "body": response.json()
    }
    path = os.path.join(GOLDEN_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  [OK] {name} -> {path} (HTTP {response.status_code})")


def main():
    print("=" * 60)
    print("SAHYADRUSHTI AI - Recording Golden API Fixtures")
    print("=" * 60)

    # ---- GET endpoints (safe, read-only) ----
    get_endpoints = {
        "health": "/api/health",
        "region": "/api/region",
        "locations": "/api/locations",
        "locations_filter_tourist": "/api/locations?category=tourist_spot",
        "location_detail_bhushi": "/api/locations/bhushi_dam",
        "weather_current": "/api/weather/current",
        "weather_current_bhushi": "/api/weather/current?location_id=bhushi_dam",
        "weather_forecast": "/api/weather/forecast",
        "map_risk": "/api/map/risk",
        "incidents": "/api/incidents",
        "incidents_no_historical": "/api/incidents?include_historical=false",
        "alerts": "/api/alerts",
        "model_info": "/api/model/info",
        "model_metrics": "/api/model/metrics",
        "replay": "/api/replay",
        "sensors_status": "/api/sensors/status",
        "shelters": "/api/shelters",
        "corridors": "/api/corridors",
        "demo_scenario": "/api/demo/scenario",
    }

    print("\n--- GET Endpoints ---")
    for name, path in get_endpoints.items():
        resp = client.get(path)
        save(name, resp)

    # ---- POST endpoints with safe sample payloads ----
    print("\n--- POST Endpoints (sample payloads) ---")

    # POST /api/predict
    predict_payload = {
        "hazard_type": "landslide",
        "rain_1h_mm": 24.5,
        "rain_24h_mm": 138.0,
        "rain_48h_mm": 212.0,
        "forecast_24h_mm": 155.0,
        "soil_moisture_pct": 84.5,
        "slope_deg": 36.5,
        "elevation_m": 680.0,
        "drainage_proximity_m": 45.0,
        "disturbed_slope_prox_m": 25.0,
        "veg_cover_pct": 35.0
    }
    resp = client.post("/api/predict", json=predict_payload)
    save("predict_landslide", resp)

    predict_ff_payload = {
        "hazard_type": "flash_flood",
        "rain_1h_mm": 45.0,
        "rain_24h_mm": 138.0,
        "rain_48h_mm": 212.0,
        "forecast_24h_mm": 155.0,
        "soil_moisture_pct": 84.5,
        "slope_deg": 24.5,
        "elevation_m": 638.0,
        "drainage_proximity_m": 15.0
    }
    resp = client.post("/api/predict", json=predict_ff_payload)
    save("predict_flash_flood", resp)

    # POST /api/simulate
    simulate_payload = {
        "scenario_name": "Golden File Test Scenario",
        "rain_1h_mm": 30.0,
        "rain_24h_mm": 150.0,
        "rain_48h_mm": 220.0,
        "forecast_24h_mm": 160.0,
        "soil_moisture_pct": 85.0,
        "baseline_location_ids": ["bhushi_dam", "khandala_expressway", "lonavala_town"]
    }
    resp = client.post("/api/simulate", json=simulate_payload)
    save("simulate", resp)

    # POST /api/incidents (citizen report)
    incident_payload = {
        "hazard_type": "rockfall",
        "location_name": "Golden Test Location",
        "lat": 18.74,
        "lon": 73.40,
        "description": "Golden file test incident submission",
        "observed_time": "2026-10-24T18:00:00Z",
        "reporter_name": "Golden Test"
    }
    resp = client.post("/api/incidents", json=incident_payload)
    save("submit_incident", resp)

    # POST /api/authority/alerts/draft
    draft_payload = {
        "title": "Golden Test Alert Draft",
        "title_mr": "गोल्डन टेस्ट अलर्ट",
        "message": "This is a test alert for golden file recording.",
        "message_mr": "हा गोल्डन फाइल रेकॉर्डिंगसाठी चाचणी अलर्ट आहे.",
        "severity": "advisory",
        "geographic_coverage": "Lonavala Ghat Region",
        "target_locations": ["bhushi_dam"]
    }
    resp = client.post("/api/authority/alerts/draft", json=draft_payload)
    save("draft_alert", resp)

    # POST /api/sensors/ingest
    sensor_payload = {
        "sensor_id": "GOLDEN-TEST-001",
        "station_name": "Golden Test Station",
        "sensor_type": "Tipping Bucket Rain Gauge",
        "coordinates": [18.755, 73.395],
        "latest_value": 12.5,
        "unit": "mm/h",
        "last_seen": "2026-10-24T18:00:00Z",
        "battery_pct": 92,
        "signal_rssi": -65,
        "health_status": "HEALTHY",
        "quality_flag": "NOMINAL",
        "is_simulated": True
    }
    resp = client.post("/api/sensors/ingest", json=sensor_payload)
    save("sensor_ingest", resp)

    # ---- 404 test ----
    print("\n--- Error cases ---")
    resp = client.get("/api/locations/nonexistent_location_xyz")
    save("location_404", resp)

    print("\n" + "=" * 60)
    print(f"Golden files recorded to: {GOLDEN_DIR}")
    print(f"Total files: {len(os.listdir(GOLDEN_DIR))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
