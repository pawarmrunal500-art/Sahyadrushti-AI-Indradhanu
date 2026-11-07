"""
app/routers/system.py - System metadata and health endpoints.
"""
from fastapi import APIRouter
import datetime
from app.services.risk import risk_service

router = APIRouter(tags=["System"])

@router.get("/api/health")
def get_health():
    """Returns backend service health, ML pipeline status, active region, and extended telemetry."""
    return {
        "status": "HEALTHY",
        "service": "SAHYADRUSHTI AI Platform",
        "marathi_name": "सह्यादृष्टी एआय",
        "tagline": "पावसाआधी नव्हे, धोक्याआधी सावध!",
        "version": "2.1.0",
        "pilot_region": "Lonavala - Khandala - Maval (Western Ghats, Maharashtra)",
        "coordinates_bbox": {
            "north": 18.840,
            "south": 18.700,
            "west": 73.320,
            "east": 73.450
        },
        "model_version": risk_service.engine.model_version,
        "sdg_target": "UN SDG 13.1 - Strengthen resilience and adaptive capacity to climate hazards",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        # Amendment 6: Additive health fields
        "db_status": "in_memory_prototype",
        "last_weather_fetch": None,
        "scheduler_status": "standby"
    }

@router.get("/api/region", tags=["Geospatial"])
def get_region_metadata():
    """Returns pilot region geographical bounds, terrain characteristics, and baseline statistics."""
    from backend.data_layer import LOCATIONS_DATA, SHELTERS_DATA, CORRIDORS_DATA, HISTORICAL_INCIDENTS
    return {
        "region_id": "lonavala_khandala_maval",
        "display_name": "Lonavala - Khandala Pilot Zone (Maval, Maharashtra)",
        "marathi_display_name": "लोणावळा - खंडाळा - मावळ प्रायोगिक क्षेत्र",
        "center": [18.755, 73.395],
        "default_zoom": 13,
        "geology": "Deccan Trap Basalt with weathered lateritic overburden",
        "monsoon_context": "Orographic precipitation with extreme localized gradients (2,500mm - 4,500mm annual)",
        "primary_hazards": [
            "Rainfall-triggered rotational/debris landslides",
            "Flash floods & rapid stream convergence surges",
            "Transport corridor disruption (Expressway & Central Railway Ghat)",
            "Tourist waterfall & reservoir access drownings"
        ],
        "monitored_nodes_count": len(LOCATIONS_DATA),
        "shelters_count": len(SHELTERS_DATA),
        "corridors_count": len(CORRIDORS_DATA),
        "historical_incidents_count": len(HISTORICAL_INCIDENTS)
    }
