"""
app/routers/system.py - System metadata and health endpoints.
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
import datetime

from app.services.risk import risk_service
from app.services.weather import weather_service
from app.scheduler import scheduler
from app.db import get_session
from app.repositories import get_locations

router = APIRouter(tags=["System"])

@router.get("/api/health")
def get_health(session: Session = Depends(get_session)):
    """Returns backend service health, ML pipeline status, active region, and extended telemetry."""
    # Check DB connectivity
    db_status = "connected"
    try:
        session.connection()
    except Exception:
        db_status = "disconnected"

    scheduler_status = "running" if scheduler.running else "standby"

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
        # Additive health fields (Amendment 6)
        "db_status": db_status,
        "last_weather_fetch": weather_service.last_successful_fetch,
        "scheduler_status": scheduler_status
    }

@router.get("/api/region", tags=["Geospatial"])
def get_region_metadata(session: Session = Depends(get_session)):
    """Returns pilot region geographical bounds, terrain characteristics, and baseline statistics."""
    from backend.data_layer import SHELTERS_DATA, CORRIDORS_DATA, HISTORICAL_INCIDENTS
    locations = get_locations(session)
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
        "monitored_nodes_count": len(locations),
        "shelters_count": len(SHELTERS_DATA),
        "corridors_count": len(CORRIDORS_DATA),
        "historical_incidents_count": len(HISTORICAL_INCIDENTS)
    }
