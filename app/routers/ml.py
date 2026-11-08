"""
app/routers/ml.py - AI/ML inference, parametric simulation, and research transparency.
"""
from fastapi import APIRouter, HTTPException, Request, Query
import datetime
from backend.schemas import PredictionRequest, PredictionResponse, SimulationScenarioRequest
from backend.data_layer import LOCATIONS_DATA, REPLAY_TIMELINE_DATA, DEMO_SCENARIO_DATA
from app.services.risk import risk_service
from app.limiter import limiter
from app.config import settings

router = APIRouter(tags=["AI / ML Inference & Transparency"])

@router.post("/api/predict", response_model=PredictionResponse)
@limiter.limit(settings.RATE_LIMIT_PREDICT)
def predict_hazard_risk(request: Request, payload: PredictionRequest):
    """
    Executes physics-informed model inference on given terrain and rainfall payload.
    Returns estimated probability proxy, relative risk score (0-100), trigger index, and SHAP-proxy factors.
    """
    try:
        data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
        return risk_service.predict(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")

@router.post("/api/simulate")
@limiter.limit(settings.RATE_LIMIT_SIMULATE)
def run_scenario_simulation(request: Request, payload: SimulationScenarioRequest):
    """
    Interactive 'What-If Storm Intensifies?' simulation tool.
    Runs the model across baseline locations with user-adjusted rainfall/saturation.
    """
    results = []
    for loc_id in payload.baseline_location_ids:
        loc = next((l for l in LOCATIONS_DATA if l["id"] == loc_id), None)
        if not loc:
            continue
        
        sim_input = {
            "location_id": loc["id"],
            "hazard_type": loc["current_hazard"] if loc["current_hazard"] in ["landslide", "flash_flood"] else "landslide",
            "rain_1h_mm": payload.rain_1h_mm,
            "rain_24h_mm": payload.rain_24h_mm,
            "rain_48h_mm": payload.rain_48h_mm,
            "forecast_24h_mm": payload.forecast_24h_mm,
            "soil_moisture_pct": payload.soil_moisture_pct,
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "drainage_proximity_m": loc["drainage_proximity_m"]
        }
        prediction = risk_service.predict(sim_input)
        
        score_delta = prediction["risk_score"] - loc["risk_score"]
        results.append({
            "location_id": loc["id"],
            "location_name": loc["name"],
            "baseline_score": loc["risk_score"],
            "baseline_level": loc["status"],
            "simulated_score": prediction["risk_score"],
            "simulated_level": prediction["risk_level"],
            "delta_score": score_delta,
            "slope_deg": loc["slope_deg"],
            "factors": prediction["contributing_factors"],
            "precautions": prediction["precautions"]
        })
    
    inputs_dict = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    return {
        "scenario_name": payload.scenario_name,
        "inputs": inputs_dict,
        "simulated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model_version": risk_service.engine.model_version,
        "results": results
    }

@router.get("/api/model/info")
def get_model_info():
    """Returns model card, feature definitions, training regimen, and limitations."""
    return risk_service.get_info()

@router.get("/api/model/metrics")
def get_model_metrics():
    """
    Returns evaluation metrics.
    Explicitly labeled with evaluation_basis: 'synthetic_holdout'.
    """
    return risk_service.get_metrics()

import os
import json

BACKFILLED_REPLAY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "backend",
    "backfilled_replay.json"
)

@router.get("/api/replay", tags=["Signature Feature"])
def get_storm_replay():
    """
    Returns time-step progression for the Severe Ghat Storm Event.
    Serves the backfilled archive sequence if available, or falls back to calibrated timeline.
    """
    if os.path.exists(BACKFILLED_REPLAY_PATH):
        try:
            with open(BACKFILLED_REPLAY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "event_title": "July 2026 Severe Monsoon Squall Event Replay",
        "event_date": "2026-07-24 to 2026-07-25",
        "description": "Historical-calibrated replay demonstrating how high antecedent precipitation saturated Khandala cut-slopes and triggered sudden flash surges at Bhushi cascades.",
        "total_frames": len(REPLAY_TIMELINE_DATA),
        "timeline": REPLAY_TIMELINE_DATA
    }

@router.get("/api/demo/scenario", tags=["Hackathon Demo"])
def get_demo_scenario():
    """Returns deterministic 3-minute comparison scenario comparing Locations A, B, and C."""
    return DEMO_SCENARIO_DATA


# ==============================================================================
# Additive Decision-Support & Spatial Comparison Endpoints (Phase P1h)
# ==============================================================================

@router.get("/api/risk", tags=["Decision Support"])
def get_risk_at_coordinates(
    lat: float = Query(..., description="Latitude of user query"),
    lon: float = Query(..., description="Longitude of user query")
):
    """
    Finds nearest pilot monitoring location, calculates distance, and returns
    hyperlocal risk evaluation with contributing factors and multilingual action advice.
    """
    import math
    nearest_loc = None
    min_dist_km = float("inf")

    for loc in LOCATIONS_DATA:
        clat, clon = loc["coordinates"]
        dlat = math.radians(clat - lat)
        dlon = math.radians(clon - lon)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(clat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = 6371.0 * c
        if dist_km < min_dist_km:
            min_dist_km = dist_km
            nearest_loc = loc

    if not nearest_loc:
        raise HTTPException(status_code=404, detail="No pilot location found")

    pred = risk_service.predict({
        "location_id": nearest_loc["id"],
        "hazard_type": nearest_loc["current_hazard"],
        "slope_deg": nearest_loc["slope_deg"],
        "elevation_m": nearest_loc["elevation_m"],
        "drainage_proximity_m": nearest_loc["drainage_proximity_m"],
        "upstream_catchment_km2": nearest_loc.get("upstream_catchment_km2", 3.0),
        "rain_1h_mm": 5.0,
        "rain_24h_mm": 60.0
    })

    return {
        "query_coordinates": [lat, lon],
        "nearest_pilot_location": {
            "id": nearest_loc["id"],
            "name": nearest_loc["name"],
            "name_mr": nearest_loc["name_mr"],
            "name_hi": nearest_loc["name_hi"],
            "coordinates": nearest_loc["coordinates"],
            "distance_km": round(min_dist_km, 2)
        },
        "risk_evaluation": pred,
        "action_guidance": {
            "en": nearest_loc.get("guidance", ""),
            "mr": nearest_loc.get("guidance_mr", ""),
            "hi": nearest_loc.get("guidance_hi", "")
        },
        "data_provenance": {
            "data_source": "Copernicus GLO-30 DEM & Open-Meteo API",
            "model_version": risk_service.engine.model_version,
            "disclaimer": "Pilot-stage physics-informed risk index (0-100), not calibrated against field sensors."
        }
    }


@router.get("/api/risk/forecast", tags=["Decision Support"])
def get_risk_forecast(
    location_id: str = Query(..., description="Location ID to retrieve multi-horizon forecast")
):
    """
    Computes forecasted risk scores at +6h, +24h, and +48h horizons for a location.
    """
    loc = next((l for l in LOCATIONS_DATA if l["id"] == location_id), None)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Location '{location_id}' not found")

    horizons = [
        {"horizon": "+6h", "rain_accum_mm": 20.0, "w_storage_mm": 80.0, "soil_moisture_pct": 70.0},
        {"horizon": "+24h", "rain_accum_mm": 95.0, "w_storage_mm": 160.0, "soil_moisture_pct": 82.0},
        {"horizon": "+48h", "rain_accum_mm": 175.0, "w_storage_mm": 240.0, "soil_moisture_pct": 91.0}
    ]

    projections = []
    for h in horizons:
        p = risk_service.predict({
            "location_id": loc["id"],
            "hazard_type": loc["current_hazard"],
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "drainage_proximity_m": loc["drainage_proximity_m"],
            "upstream_catchment_km2": loc.get("upstream_catchment_km2", 3.0),
            "rain_1h_mm": 10.0,
            "rain_24h_mm": h["rain_accum_mm"],
            "antecedent_store_w_mm": h["w_storage_mm"],
            "soil_moisture_pct": h["soil_moisture_pct"]
        })
        projections.append({
            "horizon": h["horizon"],
            "expected_24h_rain_mm": h["rain_accum_mm"],
            "risk_score": p["risk_score"],
            "risk_level": p["risk_level"],
            "factor_of_safety": p.get("factor_of_safety"),
            "trigger_level": p.get("trigger_level")
        })

    return {
        "location_id": loc["id"],
        "name": loc["name"],
        "hazard_type": loc["current_hazard"],
        "projections": projections,
        "model_version": risk_service.engine.model_version
    }


@router.get("/api/locations/{location_id}/history", tags=["Decision Support"])
def get_location_history(location_id: str):
    """
    Returns the complete timestamped historical / replay risk series for a specific location.
    """
    loc = next((l for l in LOCATIONS_DATA if l["id"] == location_id), None)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Location '{location_id}' not found")

    replay_data = get_storm_replay()
    timeline = replay_data.get("timeline", [])

    history_points = []
    for frame in timeline:
        pt_state = frame.get("points_state", {}).get(location_id, {})
        history_points.append({
            "step_index": frame.get("step_index"),
            "timestamp": frame.get("timestamp_label"),
            "rain_24h_mm": frame.get("cumulative_24h_mm"),
            "antecedent_w_mm": frame.get("antecedent_store_w_mm"),
            "soil_saturation_pct": frame.get("soil_saturation_pct"),
            "risk_score": pt_state.get("score", 0),
            "risk_level": pt_state.get("risk_level", "low"),
            "factor_of_safety": pt_state.get("factor_of_safety")
        })

    return {
        "location_id": loc["id"],
        "location_name": loc["name"],
        "hazard_type": loc["current_hazard"],
        "total_points": len(history_points),
        "history": history_points
    }


@router.get("/api/compare", tags=["Decision Support"])
def compare_storm_response(
    rain_24h_mm: float = Query(120.0, description="Hypothetical 24h storm rainfall in mm"),
    antecedent_mm: float = Query(140.0, description="Drained antecedent storage W(t) in mm")
):
    """
    Same Storm, Different Risk: Evaluates all 12 pilot locations under identical hypothetical
    rainfall and antecedent conditions to highlight terrain and catchment differentiation.
    """
    results = []
    for loc in LOCATIONS_DATA:
        p = risk_service.predict({
            "location_id": loc["id"],
            "hazard_type": loc["current_hazard"],
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "drainage_proximity_m": loc["drainage_proximity_m"],
            "upstream_catchment_km2": loc.get("upstream_catchment_km2", 3.0),
            "rain_1h_mm": round(rain_24h_mm / 10.0, 1),
            "rain_24h_mm": rain_24h_mm,
            "antecedent_store_w_mm": antecedent_mm,
            "soil_moisture_pct": min(95.0, 45.0 + (antecedent_mm / 300.0) * 45.0)
        })
        results.append({
            "location_id": loc["id"],
            "name": loc["name"],
            "hazard_type": loc["current_hazard"],
            "slope_deg": loc["slope_deg"],
            "drainage_proximity_m": loc["drainage_proximity_m"],
            "upstream_catchment_km2": loc.get("upstream_catchment_km2", 2.0),
            "risk_score": p["risk_score"],
            "risk_level": p["risk_level"],
            "factor_of_safety": p.get("factor_of_safety"),
            "susceptibility_class": p.get("susceptibility_class")
        })

    # Sort descending by risk score
    results.sort(key=lambda x: x["risk_score"], reverse=True)

    return {
        "storm_scenario": {
            "rain_24h_mm": rain_24h_mm,
            "antecedent_w_mm": antecedent_mm
        },
        "spread": {
            "max_score": results[0]["risk_score"],
            "min_score": results[-1]["risk_score"],
            "score_differential": results[0]["risk_score"] - results[-1]["risk_score"]
        },
        "ranking": results
    }


@router.get("/api/vulnerable-zones", tags=["Decision Support"])
def get_vulnerable_zones():
    """
    Returns ranked vulnerable zones with GeoJSON points for regional map layers.
    """
    features = []
    for loc in LOCATIONS_DATA:
        pred = risk_service.predict({
            "location_id": loc["id"],
            "hazard_type": loc["current_hazard"],
            "slope_deg": loc["slope_deg"],
            "elevation_m": loc["elevation_m"],
            "drainage_proximity_m": loc["drainage_proximity_m"],
            "upstream_catchment_km2": loc.get("upstream_catchment_km2", 3.0),
            "rain_1h_mm": 5.0,
            "rain_24h_mm": 40.0
        })
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [loc["coordinates"][1], loc["coordinates"][0]]  # GeoJSON: [lon, lat]
            },
            "properties": {
                "id": loc["id"],
                "name": loc["name"],
                "hazard_type": loc["current_hazard"],
                "slope_deg": loc["slope_deg"],
                "elevation_m": loc["elevation_m"],
                "risk_score": pred["risk_score"],
                "risk_level": pred["risk_level"],
                "susceptibility_class": pred.get("susceptibility_class", "moderate_hazard_slope")
            }
        })

    features.sort(key=lambda f: f["properties"]["risk_score"], reverse=True)

    return {
        "type": "FeatureCollection",
        "features": features
    }


