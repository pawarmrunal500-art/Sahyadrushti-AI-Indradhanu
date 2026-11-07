"""
tests/test_contract.py
Contract tests for SAHYADRUSHTI AI backend API.

Compares live responses against golden files recorded from the prototype baseline.
Rules:
  - New keys in a response are ALLOWED (additive changes are safe).
  - Missing keys (present in golden but absent in live) FAIL.
  - Renamed keys FAIL.
  - Changed value types FAIL (e.g. int->str).
  - Status codes must match.
  - Value equality is NOT checked (timestamps, UUIDs etc. change per run).

Usage:
    pytest tests/test_contract.py -v
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from backend.main import app
from app.db import get_session
from app.repositories import seed_all_if_empty
from app.models import User
from app.auth import get_current_user, verify_sensor_device_key
from app.config import settings

# Disable rate limiting for contract suite
settings.RATELIMIT_ENABLED = False

# Isolated temporary test database
temp_db_fd, temp_db_path = tempfile.mkstemp(suffix=".db")
os.close(temp_db_fd)
test_db_url = f"sqlite:///{temp_db_path}"
test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)
with Session(test_engine) as seed_session:
    seed_all_if_empty(seed_session)

def get_test_session():
    with Session(test_engine) as session:
        yield session

mock_operator = User(
    id=1,
    username="contract_operator",
    role="operator",
    is_active=True,
    password_hash="mock_hash"
)

@pytest.fixture(autouse=True)
def setup_contract_env():
    settings.RATELIMIT_ENABLED = False
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[get_current_user] = lambda: mock_operator
    app.dependency_overrides[verify_sensor_device_key] = lambda: True
    yield

app.dependency_overrides[get_session] = get_test_session
app.dependency_overrides[get_current_user] = lambda: mock_operator
app.dependency_overrides[verify_sensor_device_key] = lambda: True

GOLDEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden")
client = TestClient(app)


def load_golden(name: str) -> dict:
    path = os.path.join(GOLDEN_DIR, f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_keys_and_types(golden, live, path="root"):
    """
    Recursively verify that every key present in `golden` also exists in `live`
    with a compatible type. New keys in `live` are allowed.
    """
    errors = []
    if isinstance(golden, dict) and isinstance(live, dict):
        for key in golden:
            if key not in live:
                errors.append(f"MISSING key '{key}' at {path}")
            else:
                errors.extend(
                    check_keys_and_types(golden[key], live[key], f"{path}.{key}")
                )
    elif isinstance(golden, list) and isinstance(live, list):
        # Check structure of first element if both are non-empty
        if len(golden) > 0 and len(live) > 0:
            errors.extend(
                check_keys_and_types(golden[0], live[0], f"{path}[0]")
            )
    elif golden is not None and live is not None:
        golden_type = type(golden).__name__
        live_type = type(live).__name__
        # Allow int <-> float coercion (JSON has only 'number')
        numeric = {"int", "float"}
        if golden_type != live_type and not (
            {golden_type, live_type} <= numeric
        ):
            errors.append(
                f"TYPE MISMATCH at {path}: golden={golden_type}, live={live_type}"
            )
    return errors


# ========================= GET endpoint tests =========================

GET_TESTS = {
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


@pytest.mark.parametrize("name,path", list(GET_TESTS.items()))
def test_get_contract(name, path):
    golden = load_golden(name)
    resp = client.get(path)

    # Status code must match
    assert resp.status_code == golden["status_code"], (
        f"Status code mismatch for {name}: expected {golden['status_code']}, got {resp.status_code}"
    )

    # Check structural contract
    errors = check_keys_and_types(golden["body"], resp.json())
    assert errors == [], (
        f"Contract violations for GET {path}:\n" + "\n".join(f"  - {e}" for e in errors)
    )


# ========================= POST endpoint tests =========================

POST_TESTS = [
    (
        "predict_landslide",
        "/api/predict",
        {
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
            "veg_cover_pct": 35.0,
        },
    ),
    (
        "predict_flash_flood",
        "/api/predict",
        {
            "hazard_type": "flash_flood",
            "rain_1h_mm": 45.0,
            "rain_24h_mm": 138.0,
            "rain_48h_mm": 212.0,
            "forecast_24h_mm": 155.0,
            "soil_moisture_pct": 84.5,
            "slope_deg": 24.5,
            "elevation_m": 638.0,
            "drainage_proximity_m": 15.0,
        },
    ),
    (
        "simulate",
        "/api/simulate",
        {
            "scenario_name": "Contract Test Scenario",
            "rain_1h_mm": 30.0,
            "rain_24h_mm": 150.0,
            "rain_48h_mm": 220.0,
            "forecast_24h_mm": 160.0,
            "soil_moisture_pct": 85.0,
            "baseline_location_ids": ["bhushi_dam", "khandala_expressway", "lonavala_town"],
        },
    ),
    (
        "submit_incident",
        "/api/incidents",
        {
            "hazard_type": "rockfall",
            "location_name": "Contract Test Location",
            "lat": 18.74,
            "lon": 73.40,
            "description": "Contract test incident",
            "observed_time": "2026-10-24T18:00:00Z",
            "reporter_name": "Contract Test",
        },
    ),
    (
        "draft_alert",
        "/api/authority/alerts/draft",
        {
            "title": "Contract Test Alert",
            "title_mr": "करार चाचणी अलर्ट",
            "message": "Contract test alert message.",
            "message_mr": "करार चाचणी अलर्ट संदेश.",
            "severity": "advisory",
            "geographic_coverage": "Lonavala Ghat Region",
            "target_locations": ["bhushi_dam"],
        },
    ),
    (
        "sensor_ingest",
        "/api/sensors/ingest",
        {
            "sensor_id": "CONTRACT-TEST-001",
            "station_name": "Contract Test Station",
            "sensor_type": "Tipping Bucket Rain Gauge",
            "coordinates": [18.755, 73.395],
            "latest_value": 10.0,
            "unit": "mm/h",
            "last_seen": "2026-10-24T18:00:00Z",
            "battery_pct": 90,
            "signal_rssi": -70,
            "health_status": "HEALTHY",
            "quality_flag": "NOMINAL",
            "is_simulated": True,
        },
    ),
]


@pytest.mark.parametrize("name,path,payload", POST_TESTS)
def test_post_contract(name, path, payload):
    golden = load_golden(name)
    resp = client.post(path, json=payload)

    assert resp.status_code == golden["status_code"], (
        f"Status code mismatch for {name}: expected {golden['status_code']}, got {resp.status_code}"
    )

    errors = check_keys_and_types(golden["body"], resp.json())
    assert errors == [], (
        f"Contract violations for POST {path}:\n" + "\n".join(f"  - {e}" for e in errors)
    )


# ========================= Error case tests =========================

def test_location_404():
    golden = load_golden("location_404")
    resp = client.get("/api/locations/nonexistent_location_xyz")
    assert resp.status_code == 404
    assert resp.status_code == golden["status_code"]
    errors = check_keys_and_types(golden["body"], resp.json())
    assert errors == [], (
        f"Contract violations for 404 response:\n" + "\n".join(f"  - {e}" for e in errors)
    )

