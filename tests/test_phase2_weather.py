"""
tests/test_phase2_weather.py - Unit and Integration Tests for Phase 2 Weather Pipeline.

Tests:
  - Antecedent Precipitation Index (API) exact mathematical calculation
  - Modular bias correction function
  - Batched Open-Meteo response parser with mocked HTTP client
  - Complete resilience fallback chain (Live -> Cache -> Database Snapshot -> Static)
  - Timezone formatting verification (IST in response, UTC stored)
  - Opt-in live network test (@pytest.mark.live)
"""
import pytest
import datetime
import json
import httpx
from sqlmodel import Session, create_engine, SQLModel
import tempfile
import os

from app.services.weather import (
    compute_antecedent_precipitation_index,
    apply_bias_correction,
    LiveWeatherService
)
from app.models import WeatherSnapshot

# ======================== 1. Mathematical Tests ========================

def test_api_exact_calculation():
    """
    Verify Antecedent Precipitation Index math:
    API = Σ (k^i * P_i)
    Test with k = 0.9 and daily past rain = [10.0, 20.0, 0.0]
    Expected:
      Day 1: 0.9^1 * 10 = 9.0
      Day 2: 0.9^2 * 20 = 16.2
      Day 3: 0.9^3 * 0 = 0.0
      Total API = 25.20 mm
    """
    daily_precip = [10.0, 20.0, 0.0]
    api_val = compute_antecedent_precipitation_index(daily_precip, decay_k=0.9)
    assert api_val == 25.20

    # Test with all zeros
    assert compute_antecedent_precipitation_index([0.0] * 14, decay_k=0.88) == 0.0

    # Test with negative inputs (clamped to 0.0)
    assert compute_antecedent_precipitation_index([-5.0, 10.0], decay_k=0.9) == 8.10


def test_bias_correction_layer():
    """Verify raw vs corrected separation and linear/modular multiplier."""
    raw = 25.0
    assert apply_bias_correction(raw, multiplier=1.0) == 25.0
    assert apply_bias_correction(raw, multiplier=1.5) == 37.5
    assert apply_bias_correction(-5.0, multiplier=1.0) == 0.0


# ======================== 2. Parser & Fallback Tests ========================

MOCK_OPENMETEO_RESPONSE = [
    {
        "latitude": 18.75,
        "longitude": 73.39,
        "hourly": {
            "time": [f"2026-10-24T{h:02d}:00" for h in range(350)],
            "precipitation": [5.0 if h == 336 else 1.0 for h in range(350)],
            "soil_moisture_0_to_1cm": [0.48 for _ in range(350)],
            "soil_moisture_3_to_9cm": [0.50 for _ in range(350)],
            "soil_moisture_9_to_27cm": [0.52 for _ in range(350)],
            "temperature_2m": [22.5 for _ in range(350)],
            "relative_humidity_2m": [94.0 for _ in range(350)],
            "wind_speed_10m": [26.0 for _ in range(350)]
        }
    }
]

import asyncio

def test_batched_response_parser(monkeypatch):
    """Verify batched parser correctly processes multi-coordinate response without network access."""
    service = LiveWeatherService()

    class MockResponse:
        status_code = 200
        def raise_for_status(self): pass
        def json(self): return MOCK_OPENMETEO_RESPONSE

    class MockAsyncClient:
        async def get(self, url, params=None):
            return MockResponse()
        async def aclose(self): pass

    test_locations = [{"id": "bhushi_dam", "name": "Bhushi Dam", "coordinates": [18.7364, 73.3965]}]
    parsed = asyncio.run(service.fetch_openmeteo_batched(test_locations, client=MockAsyncClient()))

    assert "bhushi_dam" in parsed
    obs = parsed["bhushi_dam"]
    assert obs["location_id"] == "bhushi_dam"
    assert obs["rain_1h_mm"] == 5.0
    assert obs["rain_mm_raw"] == 5.0
    assert obs["rain_mm_corrected"] == 5.0
    assert obs["data_source"] == "Open-Meteo Live API"
    assert obs["is_stale"] is False
    assert "antecedent_precipitation_index_mm" in obs
    assert "grid_cell_resolution_km" in obs


def test_weather_fallback_chain():
    """
    Verify complete resilience fallback chain:
    1. Empty cache -> falls back to DB snapshot if available
    2. No snapshot -> falls back to static seed data (never crashes)
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_fd)
    db_url = f"sqlite:///{temp_path}"
    test_engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)

    service = LiveWeatherService()

    # Step 1: No cache, no DB -> returns static fallback
    with Session(test_engine) as session:
        static_obs = service.get_current_sync("bhushi_dam", session=session)
        assert static_obs is not None
        assert "Static Fallback" in static_obs["data_source"]
        assert static_obs["rain_1h_mm"] > 0

    # Step 2: Insert a historical snapshot into DB -> should return database snapshot
    with Session(test_engine) as session:
        snap_data = {
            "location_id": "bhushi_dam",
            "location_name": "Bhushi Dam & Waterfall Catchment",
            "station_name": "Bhushi Dam Automated Station",
            "observation_time": "2026-10-24T18:00:00+05:30",
            "rain_1h_mm": 19.5,
            "rain_3h_mm": 38.0,
            "rain_24h_mm": 110.0,
            "rain_48h_mm": 175.0,
            "rain_intensity_mm_hr": 19.5,
            "soil_moisture_pct": 82.0,
            "temperature_c": 21.0,
            "humidity_pct": 98.0,
            "wind_speed_kmh": 22.0,
            "data_source": "Open-Meteo Live API",
            "data_status": "verified_observation",
            "staleness_threshold_minutes": 60,
            "is_stale": False
        }
        snapshot = WeatherSnapshot(
            location_id="bhushi_dam",
            fetched_at="2026-10-24T18:00:00Z",
            rain_mm_1h=19.5,
            rain_mm_24h=110.0,
            soil_moisture=82.0,
            source="open-meteo-live",
            raw_json=json.dumps(snap_data)
        )
        session.add(snapshot)
        session.commit()

        # Service with fresh cache should return the DB snapshot (marked stale)
        service._cache.clear()
        db_obs = service.get_current_sync("bhushi_dam", session=session)
        assert db_obs["data_source"] == "database_snapshot"
        assert db_obs["is_stale"] is True
        assert db_obs["stale"] is True
        assert db_obs["rain_1h_mm"] == 19.5

    # Step 3: Populate memory cache -> should return from memory cache immediately
    service._set_cache("bhushi_dam", {"location_id": "bhushi_dam", "rain_1h_mm": 35.0, "data_source": "cached"})
    with Session(test_engine) as session:
        cached_obs = service.get_current_sync("bhushi_dam", session=session)
        assert cached_obs["data_source"] == "cached"
        assert cached_obs["rain_1h_mm"] == 35.0

    try:
        os.remove(temp_path)
    except OSError:
        pass


def test_timezone_consistency():
    """Verify IST timestamp in observation_time and UTC timestamp in fetched_at."""
    service = LiveWeatherService()
    obs = service.get_current_sync("bhushi_dam")
    # IST observation_time contains +05:30
    assert "+05:30" in obs["observation_time"]
    # fetched_at is valid ISO
    assert "T" in obs["fetched_at"]


# ======================== 3. Opt-in Live Network Test ========================

@pytest.mark.live
def test_live_openmeteo_network_call():
    """
    Opt-in test requiring live internet connectivity.
    Run explicitly via: pytest -m live tests/test_phase2_weather.py
    """
    service = LiveWeatherService()
    test_locations = [{"id": "bhushi_dam", "name": "Bhushi Dam", "coordinates": [18.7364, 73.3965]}]
    parsed = asyncio.run(service.fetch_openmeteo_batched(test_locations))
    assert "bhushi_dam" in parsed
    obs = parsed["bhushi_dam"]
    assert obs["rain_1h_mm"] >= 0.0
    assert obs["data_source"] == "Open-Meteo Live API"
