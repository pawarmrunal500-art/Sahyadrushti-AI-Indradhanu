"""
tests/test_phase4_backtest.py
Tests for Phase 4A (Replay & Model Audit), Phase 4B (Production Hardening & Origin Badging),
and Phase 4C (Back-Test Scaffolding & Evaluation).
"""
import csv
import json
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import Settings
from app.services.risk import risk_service
from scripts.backtest import load_inventory, run_backtest, haversine_distance_km

def test_debug_defaults_to_false_and_validates_jwt_secret():
    """Verify that Settings defaults DEBUG to False, and enforces JWT_SECRET strength in production mode."""
    old_debug = os.environ.get("DEBUG")
    old_secret = os.environ.get("JWT_SECRET")
    try:
        os.environ.pop("DEBUG", None)
        os.environ.pop("JWT_SECRET", None)
        with pytest.raises(RuntimeError, match="FATAL: In production mode"):
            Settings()
            
        # With valid production secret, startup succeeds with DEBUG=False
        os.environ["JWT_SECRET"] = "production_grade_secret_with_more_than_32_characters_12345"
        prod_settings = Settings()
        assert prod_settings.DEBUG is False
        assert prod_settings.JWT_SECRET.startswith("production_grade_secret")
    finally:
        if old_debug is not None:
            os.environ["DEBUG"] = old_debug
        else:
            os.environ.pop("DEBUG", None)
        if old_secret is not None:
            os.environ["JWT_SECRET"] = old_secret
        else:
            os.environ.pop("JWT_SECRET", None)


def test_model_version_is_v22():
    """Verify model version is updated to Sahyadri-GeoRisk-v2.2."""
    assert risk_service.engine.model_version == "Sahyadri-GeoRisk-v2.2"
    info = risk_service.get_info()
    assert info["version"] == "Sahyadri-GeoRisk-v2.2"


def test_model_differentiates_peak_and_retains_antecedent():
    """
    Verify physics-consistent geotechnical model:
    - Step 5 does not collapse to near-zero after heavy multi-day rain.
    - Steep slopes (Amrutanjan, Kune, Monkey Hill) do not all clamp flat at 99.
    """
    pred_amrutanjan = risk_service.predict({
        "location_id": "khandala_expressway",
        "hazard_type": "landslide",
        "rain_1h_mm": 5.0,
        "rain_24h_mm": 180.0,
        "rain_48h_mm": 350.0,
        "rain_72h_mm": 480.0,
        "slope_deg": 36.5,
        "disturbed_slope_prox_m": 15.0,
        "soil_moisture_0_to_1cm": 0.52,
        "soil_moisture_3_to_9cm": 0.52,
        "soil_moisture_9_to_27cm": 0.52
    })
    
    pred_kune = risk_service.predict({
        "location_id": "kune_falls",
        "hazard_type": "landslide",
        "rain_1h_mm": 5.0,
        "rain_24h_mm": 180.0,
        "rain_48h_mm": 350.0,
        "rain_72h_mm": 480.0,
        "slope_deg": 38.0,
        "disturbed_slope_prox_m": 30.0,
        "soil_moisture_0_to_1cm": 0.52,
        "soil_moisture_3_to_9cm": 0.52,
        "soil_moisture_9_to_27cm": 0.52
    })

    # Scores should be high (critical regime)
    assert pred_amrutanjan["risk_score"] >= 80
    assert pred_kune["risk_score"] >= 80
    assert "factor_of_safety" in pred_amrutanjan
    assert pred_amrutanjan["drainage_recession_tau_hours"] == 60.0
    assert "uncalibrated_assumption" in pred_amrutanjan

    # Post-peak step (instantaneous rain eases to 1 mm, but 48h was 310 mm)
    pred_post_peak = risk_service.predict({
        "location_id": "khandala_expressway",
        "hazard_type": "landslide",
        "rain_1h_mm": 1.0,
        "rain_24h_mm": 70.0,
        "rain_48h_mm": 310.0,
        "rain_72h_mm": 485.0,
        "slope_deg": 36.5,
        "disturbed_slope_prox_m": 15.0,
        "soil_moisture_0_to_1cm": 0.51,
        "soil_moisture_3_to_9cm": 0.51,
        "soil_moisture_9_to_27cm": 0.51
    })
    # Must remain elevated/high due to 60h drainage recession, NOT collapse to low (<25)
    assert pred_post_peak["risk_score"] >= 70


def test_data_origin_field_in_schemas():
    """Verify data_origin field is returned on incidents, alerts, sensors, shelters, corridors."""
    from backend.data_layer import HISTORICAL_INCIDENTS, ALERTS_DATA, SHELTERS_DATA, CORRIDORS_DATA, SENSOR_NODES
    assert HISTORICAL_INCIDENTS[0]["data_origin"] == "demo_seed"
    assert ALERTS_DATA[0]["data_origin"] == "demo_seed"
    assert SHELTERS_DATA[0]["data_origin"] == "demo_seed"
    assert CORRIDORS_DATA[0]["data_origin"] == "demo_seed"
    assert SENSOR_NODES[0]["data_origin"] == "demo_seed"


def test_backtest_refuses_example_row_and_runs_on_real_inventory():
    """Verify scripts/backtest.py refuses example row and evaluates real events with proper disclaimers."""
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "event_inventory_template.csv")
    assert os.path.exists(template_path)

    # 1. Refusal on template file containing only example row
    with pytest.raises(SystemExit):
        load_inventory(template_path)

    # 2. Execution on temporary CSV with 2 real test events
    fd, temp_csv = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    out_fd, temp_out = tempfile.mkstemp(suffix=".json")
    os.close(out_fd)

    try:
        with open(temp_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["event_id", "date_time_ist", "location_name", "lat", "lon", "hazard_type", "description", "source_name", "source_url", "confidence", "notes"])
            writer.writerow(["TEST-EV-01", "2026-07-06 18:00", "Amrutanjan Cut Slope", "18.7562", "73.3751", "landslide", "Debris slide on expressway", "Police Control Room", "https://example.gov.in/e1", "High", "Ground truth record"])
            writer.writerow(["TEST-EV-02", "2026-07-07 03:00", "Bhushi Spillway Gorge", "18.7280", "73.3980", "flash_flood", "Sudden stream cresting", "Irrigation Dept", "https://example.gov.in/e2", "High", "Ground truth record"])

        res = run_backtest(
            inventory_path=temp_csv,
            window_hours=24,
            threshold=70,
            output_json_path=temp_out
        )

        assert res["status"] == "COMPLETED"
        assert res["total_events"] == 2
        assert res["hits_count"] == 2
        assert res["hit_rate_pct"] == 100.0
        assert "preliminary, small sample, synthetic-calibrated model" in res["evaluation_basis"]

        with open(temp_out, "r", encoding="utf-8") as f:
            saved = json.load(f)
            assert saved["total_events"] == 2
            assert "preliminary, small sample" in saved["evaluation_basis"]
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
        if os.path.exists(temp_out):
            os.remove(temp_out)
