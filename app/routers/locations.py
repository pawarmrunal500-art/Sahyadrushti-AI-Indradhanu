"""
app/routers/locations.py - Geographic locations, map risk layers, corridors, and shelters.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session
import datetime

from backend.schemas import LocationItem, ShelterItem, CorridorItem
from backend.data_layer import SHELTERS_DATA, CORRIDORS_DATA
from app.db import get_session
from app.repositories import get_locations, get_location_by_id

router = APIRouter(tags=["Locations & Geospatial"])

@router.get("/api/locations", response_model=List[LocationItem])
def get_all_locations(
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Returns directory of verified monitored points (tourist spots, corridors, settlements)."""
    return get_locations(session, category=category)

@router.get("/api/locations/{location_id}", response_model=LocationItem)
def get_location_detail(
    location_id: str,
    session: Session = Depends(get_session)
):
    """Returns detailed hazard intelligence, upstream catchment info, and precautions for a location."""
    loc = get_location_by_id(session, location_id)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Location with id '{location_id}' not found.")
    return loc

@router.get("/api/map/risk", tags=["Geospatial"])
def get_risk_map_layers(session: Session = Depends(get_session)):
    """Returns complete geospatial risk features: monitored points, corridors, and terrain metadata."""
    locations = get_locations(session)
    features = []
    for loc in locations:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [loc["coordinates"][1], loc["coordinates"][0]] # GeoJSON is [lon, lat]
            },
            "properties": {
                "id": loc["id"],
                "name": loc["name"],
                "name_mr": loc["name_mr"],
                "category": loc["category"],
                "risk_level": loc["status"],
                "risk_score": loc["risk_score"],
                "hazard_type": loc["current_hazard"],
                "elevation_m": loc["elevation_m"],
                "slope_deg": loc["slope_deg"],
                "guidance": loc["guidance"],
                "telemetry_status": loc["telemetry_status"],
                "upstream_info": loc.get("upstream_info")
            }
        })

    corridors_geojson = []
    for c in CORRIDORS_DATA:
        corridors_geojson.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [c["coordinates_start"][1], c["coordinates_start"][0]],
                    [c["center_coords"][1], c["center_coords"][0]],
                    [c["coordinates_end"][1], c["coordinates_end"][0]]
                ]
            },
            "properties": {
                "id": c["id"],
                "name": c["corridor_name"],
                "segment": c["segment_name"],
                "status": c["current_status"],
                "hazard_type": c["hazard_type"],
                "slope_susceptibility": c["slope_susceptibility"],
                "traffic_notes": c["traffic_notes"]
            }
        })

    return {
        "type": "FeatureCollection",
        "region": "Lonavala-Khandala Pilot Zone",
        "features": features,
        "corridors": corridors_geojson,
        "layer_metadata": {
            "terrain_source": "Copernicus DEM 30m / SRTM 1-Arc-Second",
            "rainfall_source": "Open-Meteo & Regional Precipitation Data",
            "soil_source": "Derived Soil Moisture Index (Antecedent Model)",
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    }

@router.get("/api/shelters", response_model=List[ShelterItem], tags=["Safety"])
def get_shelters():
    """Returns verified disaster shelters with coordinates, capacity, and official contacts."""
    return SHELTERS_DATA

@router.get("/api/corridors", response_model=List[CorridorItem], tags=["Monitoring"])
def get_corridors():
    """Returns highway and railway corridor monitoring segments."""
    return CORRIDORS_DATA
