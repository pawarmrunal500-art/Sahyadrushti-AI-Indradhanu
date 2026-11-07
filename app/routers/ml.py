"""
app/routers/ml.py - AI/ML inference, parametric simulation, and research transparency.
"""
from fastapi import APIRouter, HTTPException
import datetime
from backend.schemas import PredictionRequest, PredictionResponse, SimulationScenarioRequest
from backend.data_layer import LOCATIONS_DATA, REPLAY_TIMELINE_DATA, DEMO_SCENARIO_DATA
from app.services.risk import risk_service

router = APIRouter(tags=["AI / ML Inference & Transparency"])

@router.post("/api/predict", response_model=PredictionResponse)
def predict_hazard_risk(payload: PredictionRequest):
    """
    Executes physics-informed model inference on given terrain and rainfall payload.
    Returns calibrated probability, relative risk score (0-100), trigger index, and SHAP-proxy factors.
    """
    try:
        data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
        return risk_service.predict(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")

@router.post("/api/simulate")
def run_scenario_simulation(payload: SimulationScenarioRequest):
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

@router.get("/api/replay", tags=["Signature Feature"])
def get_storm_replay():
    """
    Returns time-step progression for the July 2026 Severe Ghat Storm Event.
    Demonstrates dynamic evolution of rainfall, soil saturation, and location hazard levels.
    """
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

