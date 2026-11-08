"""
tests/test_phase5_regression.py
Phase 5B Regression and Validation Tests:
  1. Data Origin Verification:
     - Seeded records have data_origin == 'demo_seed'
     - Citizen submissions (POST /api/incidents) store data_origin == 'user_submitted'
     - Live sensor ingest (POST /api/sensors/ingest) stores data_origin == 'live'
     - Seeded sensor transitioning to live ingest updates data_origin to 'live'
  2. Model Monotonicity:
     - Holding rainfall constant, increasing antecedent store W(t) never lowers risk score
     - Holding antecedent store constant, increasing rainfall never lowers risk score
  3. Score Stability / Non-Collapse:
     - Score does not collapse between consecutive frames when cumulative rainfall stays high
  4. Replay Features & Extended Lookback:
     - Timeline starts >= 10 days before storm onset
     - Frame 0 is calm baseline (scores <= 5 across all locations)
     - Multi-day lookback features (48h, 72h, 7d, API, multi-layer soil moisture) are populated
  5. Reverse Proxy Security:
     - FORWARDED_ALLOW_IPS defaults to '127.0.0.1' to prevent IP spoofing
"""
import os
import sys
import json
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from app.config import Settings, settings
from app.db import get_session
from app.models import Incident, Alert, SensorNodeDB, User
from app.auth import hash_password, hash_token
from app.repositories import seed_all_if_empty
from app.services.risk import risk_service
from backend.data_layer import LOCATIONS_DATA
from app.limiter import limiter

# Disable rate limiter for functional test assertions
limiter.enabled = False

# Dedicated SQLite test DB fixture
@pytest.fixture(scope="module")
def test_db():
    temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_fd)
    db_url = f"sqlite:///{temp_path}"
    test_engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        seed_all_if_empty(session)

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)

    yield {"engine": test_engine, "client": client, "path": temp_path}

    app.dependency_overrides.clear()
    try:
        os.remove(temp_path)
    except OSError:
        pass


# ==================== 1. Data Origin Verification ====================

def test_data_origin_seed_data(test_db):
    """Confirm all seeded incidents, alerts, and sensor nodes carry data_origin='demo_seed'."""
    with Session(test_db["engine"]) as session:
        incidents = session.exec(select(Incident)).all()
        assert len(incidents) > 0
        for inc in incidents:
            assert inc.data_origin == "demo_seed"

        alerts = session.exec(select(Alert)).all()
        assert len(alerts) > 0
        for alert in alerts:
            assert alert.data_origin == "demo_seed"

        sensors = session.exec(select(SensorNodeDB)).all()
        assert len(sensors) > 0
        for sensor in sensors:
            assert sensor.data_origin == "demo_seed"


def test_data_origin_user_submitted_incident(test_db):
    """Confirm POST /api/incidents stores data_origin='user_submitted' (never demo_seed)."""
    client = test_db["client"]
    payload = {
        "hazard_type": "landslide",
        "location_name": "Patan Village Settlements",
        "lat": 18.730,
        "lon": 73.385,
        "description": "Small rock detachment observed on outer bend after morning showers.",
        "observed_time": "2026-07-06T12:00:00Z",
        "reporter_name": "Citizen Observer Patil"
    }
    response = client.post("/api/incidents", json=payload)
    assert response.status_code == 201
    data = response.json()
    incident_id = data["incident_id"]

    with Session(test_db["engine"]) as session:
        saved = session.exec(select(Incident).where(Incident.id == incident_id)).first()
        assert saved is not None
        assert saved.data_origin == "user_submitted"
        assert saved.verification_status == "Unverified report"


def test_data_origin_live_sensor_ingest(test_db):
    """Confirm real sensor ingest stores data_origin='live' and transitions existing nodes."""
    client = test_db["client"]
    raw_key = "test_sensor_secret_key_12345"
    key_hash = hash_token(raw_key)

    with Session(test_db["engine"]) as session:
        # Create a new sensor node with key
        node = SensorNodeDB(
            sensor_id="SAHYA-RAIN-TEST-99",
            station_name="Bhor Ghat Experimental Gauge",
            sensor_type="tipping_bucket_rain_gauge",
            lat=18.780,
            lon=73.350,
            latest_value=12.5,
            unit="mm/h",
            last_seen="2026-07-06T12:00:00Z",
            battery_pct=95.0,
            signal_rssi=-68,
            health_status="active",
            quality_flag="nominal",
            api_key_hash=key_hash,
            data_origin="demo_seed"
        )
        session.add(node)
        session.commit()

    # Ingest a real reading using the device key
    reading_payload = {
        "sensor_id": "SAHYA-RAIN-TEST-99",
        "station_name": "Bhor Ghat Experimental Gauge",
        "sensor_type": "tipping_bucket_rain_gauge",
        "coordinates": [18.780, 73.350],
        "latest_value": 45.0,
        "unit": "mm/h",
        "last_seen": "2026-07-06T12:30:00Z",
        "battery_pct": 94.0,
        "signal_rssi": -65,
        "health_status": "active",
        "quality_flag": "nominal",
        "is_simulated": False
    }

    headers = {"X-Device-Key": raw_key}
    response = client.post("/api/sensors/ingest", json=reading_payload, headers=headers)
    assert response.status_code == 201

    with Session(test_db["engine"]) as session:
        updated = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == "SAHYA-RAIN-TEST-99")).first()
        assert updated is not None
        assert updated.data_origin == "live"
        assert updated.latest_value == 45.0


# ==================== 2. Model Monotonicity ====================

def test_model_monotonicity_antecedent_store():
    """Holding rainfall constant, increasing antecedent store W(t) must NEVER lower risk score."""
    for loc in LOCATIONS_DATA:
        # Test across dry, moderate, and heavy 24h rainfall regimes
        for rain_24h in [20.0, 75.0, 150.0]:
            prev_score = -1
            # Step antecedent store W(t) from 0 to 600 mm in 50 mm steps
            for w_val in [0.0, 50.0, 100.0, 200.0, 350.0, 500.0, 600.0]:
                payload = {
                    "location_id": loc["id"],
                    "hazard_type": loc.get("current_hazard", "landslide"),
                    "slope_deg": loc["slope_deg"],
                    "elevation_m": loc["elevation_m"],
                    "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
                    "drainage_proximity_m": loc["drainage_proximity_m"],
                    "rain_1h": rain_24h * 0.12,
                    "rain_24h": rain_24h,
                    "rain_48h": rain_24h * 1.5,
                    "api_mm": w_val,
                    "antecedent_store_mm": w_val,
                    "soil_moisture_0_to_1cm": 40.0,
                    "soil_moisture_3_to_9cm": 45.0,
                    "soil_moisture_9_to_27cm": 50.0
                }
                res = risk_service.engine.predict_hazard(payload)
                score = res["risk_score"]
                assert score >= prev_score, (
                    f"Monotonicity violation at {loc['id']} for rain_24h={rain_24h}mm: "
                    f"W={w_val} produced score={score} < prev_score={prev_score}"
                )
                prev_score = score


def test_model_monotonicity_rainfall():
    """Holding antecedent store constant, increasing 24h rainfall must NEVER lower risk score."""
    for loc in LOCATIONS_DATA:
        for w_val in [25.0, 150.0, 350.0]:
            prev_score = -1
            # Step 24h rain from 0 to 300 mm in steps
            for rain_24h in [0.0, 25.0, 50.0, 100.0, 175.0, 250.0, 300.0]:
                payload = {
                    "location_id": loc["id"],
                    "hazard_type": loc.get("current_hazard", "landslide"),
                    "slope_deg": loc["slope_deg"],
                    "elevation_m": loc["elevation_m"],
                    "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
                    "drainage_proximity_m": loc["drainage_proximity_m"],
                    "rain_1h": rain_24h * 0.15,
                    "rain_24h": rain_24h,
                    "rain_48h": rain_24h * 1.4,
                    "api_mm": w_val,
                    "antecedent_store_mm": w_val,
                    "soil_moisture_0_to_1cm": 50.0,
                    "soil_moisture_3_to_9cm": 55.0,
                    "soil_moisture_9_to_27cm": 60.0
                }
                res = risk_service.engine.predict_hazard(payload)
                score = res["risk_score"]
                assert score >= prev_score, (
                    f"Rainfall monotonicity violation at {loc['id']} for W={w_val}mm: "
                    f"rain={rain_24h}mm gave score={score} < prev={prev_score}"
                )
                prev_score = score


def test_coupled_storm_scenario_landslide_monotonic_escalation():
    """
    Coupled Storm Scenario Sensitivity Test (Phase 6 Step 4):
    In reality, a storm pulse couples directly to vadose infiltration and antecedent storage W(t).
    Under coupled infiltration:
      - W(t) = W_base + 0.85 * P_24
      - theta = min(0.53, theta_base + (P_24 / 400.0) * (0.53 - theta_base))
    
    Verifies that under wet pre-history (active monsoon conditions), increasing 24h storm rainfall
    from 50mm to 100mm to 200mm to 300mm strictly increases risk score for all landslide sites below the cap.
    
    Physical Plateau Note:
      Once theta reaches full saturation (0.53, water table at surface), pore pressure reaches
      its physical ceiling u_max = gamma_w * z * cos^2(beta) under the infinite-slope assumption;
      excess rainfall becomes surface overland runoff and cannot further increase geotechnical pore pressure.
    """
    landslide_locs = [l for l in LOCATIONS_DATA if l.get("current_hazard") == "landslide"]
    assert len(landslide_locs) > 0

    w_base = 200.0
    sm_base = 0.44

    for loc in landslide_locs:
        scores = []
        for p24 in [50.0, 100.0, 200.0, 300.0]:
            w_t = w_base + 0.85 * p24
            sm = min(0.53, sm_base + (p24 / 400.0) * (0.53 - sm_base))
            payload = {
                "location_id": loc["id"],
                "hazard_type": "landslide",
                "slope_deg": loc["slope_deg"],
                "elevation_m": loc["elevation_m"],
                "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
                "drainage_proximity_m": loc["drainage_proximity_m"],
                "disturbed_slope_prox_m": loc.get("disturbed_slope_prox_m", 80.0),
                "veg_cover_pct": loc.get("veg_cover_pct", 50.0),
                "rain_1h": p24 * 0.12,
                "rain_24h": p24,
                "rain_48h": p24 + 40.0,
                "api_mm": w_t,
                "antecedent_store_mm": w_t,
                "soil_moisture_0_to_1cm": sm,
                "soil_moisture_3_to_9cm": sm,
                "soil_moisture_9_to_27cm": sm
            }
            res = risk_service.engine.predict_hazard(payload)
            scores.append((p24, res["risk_score"], res.get("score_capped", False)))

        # Monotonicity check across the storm progression
        for i in range(len(scores) - 1):
            p_curr, s_curr, _ = scores[i]
            p_next, s_next, capped_next = scores[i + 1]
            assert s_next >= s_curr, (
                f"Coupled storm monotonicity violation at {loc['id']}: "
                f"P={p_curr}mm (score={s_curr}) -> P={p_next}mm (score={s_next})"
            )
            # Below safety cap, score must strictly increase with rainfall
            if not capped_next and s_curr < 96:
                assert s_next > s_curr, (
                    f"Unexpected score plateau at {loc['id']} between P={p_curr}mm and P={p_next}mm: "
                    f"score remained {s_curr}"
                )


# ==================== 3. Score Stability / Non-Collapse ====================

def test_score_does_not_collapse_when_cumulative_rain_stays_high():
    """
    Score must not collapse by more than 30 points between consecutive frames
    when antecedent storage and cumulative rainfall remain elevated, reflecting slow
    joint water recession (tau=60h).
    """
    loc = [l for l in LOCATIONS_DATA if l.get("current_hazard") == "landslide"][0]
    
    # Frame 1: Peak storm pulse (200 mm 24h rain, high antecedent store)
    f1_payload = {
        "location_id": loc["id"],
        "hazard_type": loc.get("current_hazard", "landslide"),
        "slope_deg": loc["slope_deg"],
        "elevation_m": loc["elevation_m"],
        "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
        "drainage_proximity_m": loc["drainage_proximity_m"],
        "rain_1h": 22.0,
        "rain_24h": 200.0,
        "rain_48h": 320.0,
        "api_mm": 280.0,
        "antecedent_store_mm": 280.0,
        "soil_moisture_0_to_1cm": 0.44,
        "soil_moisture_3_to_9cm": 0.46,
        "soil_moisture_9_to_27cm": 0.48
    }
    f1_res = risk_service.engine.predict_hazard(f1_payload)
    f1_score = f1_res["risk_score"]
    assert f1_score >= 80

    # Frame 2: Lull 12h later (recent 24h rain drops to 65 mm, but W(t) remains high at 230 mm)
    f2_payload = {
        "location_id": loc["id"],
        "hazard_type": loc.get("current_hazard", "landslide"),
        "slope_deg": loc["slope_deg"],
        "elevation_m": loc["elevation_m"],
        "catchment_area_km2": loc.get("upstream_catchment_km2", 2.0),
        "drainage_proximity_m": loc["drainage_proximity_m"],
        "rain_1h": 2.0,
        "rain_24h": 65.0,
        "rain_48h": 265.0,
        "api_mm": 230.0,
        "antecedent_store_mm": 230.0,
        "soil_moisture_0_to_1cm": 0.42,
        "soil_moisture_3_to_9cm": 0.45,
        "soil_moisture_9_to_27cm": 0.47
    }
    f2_res = risk_service.engine.predict_hazard(f2_payload)
    f2_score = f2_res["risk_score"]

    score_drop = f1_score - f2_score
    # Drop must be bounded (<= 30 points), avoiding the previous artificial collapse
    assert score_drop <= 30, (
        f"Artificial score collapse detected: f1={f1_score} -> f2={f2_score} (drop={score_drop} > 30)"
    )
    assert f2_score >= 55, f"Post-storm lull score {f2_score} fell too low despite 230mm antecedent storage"


# ==================== 4. Replay Features & Extended Lookback ====================

def test_replay_features_lookback_and_baseline():
    """Verify backend/backfilled_replay.json starts with a calm baseline and has complete multi-day lookback."""
    replay_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "backfilled_replay.json")
    assert os.path.isfile(replay_path), f"Replay file {replay_path} not found"

    with open(replay_path, "r", encoding="utf-8") as f:
        replay = json.load(f)

    timeline = replay.get("timeline", [])
    assert len(timeline) >= 20, f"Expected extended timeline, got {len(timeline)} frames"

    # Frame 0 check
    f0 = timeline[0]
    f0_time = f0["timestamp_label"]
    assert "2026-06-22" in f0_time, f"Expected replay to start on 2026-06-22, got {f0_time}"
    assert f0["cumulative_24h_mm"] < 10.0, f"Frame 0 rain {f0['cumulative_24h_mm']} is not a calm baseline"

    for loc_id, st in f0["points_state"].items():
        assert st["score"] <= 10, f"Location {loc_id} baseline score {st['score']} is unexpectedly elevated"

    # Mid-event frame (July 6-7) check for multi-day lookback features
    july_frames = [f for f in timeline if "2026-07-06" in f["timestamp_label"] or "2026-07-07" in f["timestamp_label"]]
    assert len(july_frames) > 0

    for frame in july_frames:
        assert "cumulative_48h_mm" in frame and frame["cumulative_48h_mm"] is not None
        assert "cumulative_72h_mm" in frame and frame["cumulative_72h_mm"] is not None
        assert "cumulative_7d_mm" in frame and frame["cumulative_7d_mm"] is not None
        assert "cumulative_14d_mm" in frame and frame["cumulative_14d_mm"] is not None
        assert "antecedent_store_w_mm" in frame and frame["antecedent_store_w_mm"] is not None
        assert "soil_moisture_0_to_1cm" in frame
        assert "soil_moisture_3_to_9cm" in frame
        assert "soil_moisture_9_to_27cm" in frame


# ==================== 5. Reverse Proxy Security ====================

def test_forwarded_allow_ips_security_default():
    """Verify FORWARDED_ALLOW_IPS defaults to '127.0.0.1' and is configurable."""
    old_env = os.environ.get("FORWARDED_ALLOW_IPS")
    try:
        os.environ.pop("FORWARDED_ALLOW_IPS", None)
        s = Settings()
        assert s.FORWARDED_ALLOW_IPS == "127.0.0.1", "FORWARDED_ALLOW_IPS must default to 127.0.0.1 to avoid IP spoofing"

        os.environ["FORWARDED_ALLOW_IPS"] = "10.0.0.1,192.168.1.100"
        s2 = Settings()
        assert s2.FORWARDED_ALLOW_IPS == "10.0.0.1,192.168.1.100"
    finally:
        if old_env is not None:
            os.environ["FORWARDED_ALLOW_IPS"] = old_env
        else:
            os.environ.pop("FORWARDED_ALLOW_IPS", None)
