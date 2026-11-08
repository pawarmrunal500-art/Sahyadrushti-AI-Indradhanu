"""
app/services/risk.py - Risk scoring and geotechnical calculation service.
Wraps ml_engine logic and provides helper routines for prediction and simulation.
"""
import sys
import os
from typing import Dict, Any, List

# Ensure backend can be imported for existing ml_engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from backend.ml_engine import ml_service, SahyadriHazardEngine
except ImportError:
    from ml_engine import ml_service, SahyadriHazardEngine

class RiskService:
    def __init__(self):
        self.engine = ml_service

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.engine.predict_hazard(payload)

    def get_metrics(self) -> Dict[str, Any]:
        metrics = dict(self.engine.metrics)
        # Amendment 7: Additive field labeling evaluation basis as synthetic
        metrics["evaluation_basis"] = "synthetic_holdout"
        return metrics

    def get_info(self) -> Dict[str, Any]:
        return {
            "model_name": "Sahyadri-GeoRisk Ensemble",
            "version": self.engine.model_version,
            "architecture": "Random Forest (Landslide) & Gradient Boosting (Flash-Flood)",
            "intended_use": "Decision-support early warning for Western Ghats escarpment terrain. Aligned with SDG 13.1.",
            "prohibited_use": "Not a substitute for official district evacuation mandates or legal structural engineering surveys.",
            "evaluation_basis": "physics-informed model calibrated on synthetic scenarios",
            "input_features": [
                {"name": "rain_1h_mm", "description": "1-hour precipitation intensity (mm/h)", "source": "Radar/Rain Gauge"},
                {"name": "rain_24h_mm", "description": "24-hour rainfall accumulation (mm)", "source": "AWS Network"},
                {"name": "rain_48h_mm", "description": "48-hour antecedent rainfall (mm)", "source": "AWS Network"},
                {"name": "forecast_24h_mm", "description": "24-hour predictive accumulation (mm)", "source": "Open-Meteo Numerical Forecast"},
                {"name": "soil_moisture_pct", "description": "Volumetric water content saturation (%)", "source": "FDR Sensor / Antecedent Index"},
                {"name": "slope_deg", "description": "Terrain slope angle (degrees)", "source": "Copernicus DEM 30m"},
                {"name": "elevation_m", "description": "Orthometric elevation (meters MSL)", "source": "DEM"},
                {"name": "drainage_proximity_m", "description": "Distance to mapped stream/gorge line (m)", "source": "Hydrological Flow Accumulation"},
                {"name": "disturbed_slope_prox_m", "description": "Proximity to engineered road/rail cutting (m)", "source": "OpenStreetMap Infrastructure"},
                {"name": "veg_cover_pct", "description": "Canopy and root cohesion density (%)", "source": "Sentinel-2 NDVI"}
            ],
            "training_dataset_summary": "Derived from Western Ghats Basalt Jointing Geotechnical Surveys, Caine (1980) rainfall-trigger thresholds, and synthetic monsoon stress-testing in Maval taluka.",
            "evaluation_metrics": self.get_metrics(),
            "known_limitations": [
                "Coarse 30m DEM may miss micro-terraces under 10m height.",
                "Soil moisture telemetry is sparse in high-altitude ridges; platform falls back to Antecedent Precipitation Index (API).",
                "Model flags potential physical instability, but cannot predict sudden tree-fall or vehicular accidents."
            ]
        }

risk_service = RiskService()

