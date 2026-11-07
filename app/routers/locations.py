"""
app/routers/locations.py - Geographic locations, map risk layers, corridors, and shelters.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import datetime
from backend.schemas import LocationItem, ShelterItem, CorridorItem
from backend.data_layer import LOCATIONS_DATA, SHELTERS_DATA, CORRIDORS_DATA

router = APIRouter(tags=["Locations & Geospatial"])

@router.get("/api/locations", response_model=List[LocationItem])
def get_all_locations(category: Optional[str] = None):
    """Returns directory of verified monitored points (tourist spots, corridors, settlements)."""
    if category:
        return [loc for loc in LOCATIONS_DATA if loc.get("category") == category]
    return LOCATIONS_DATA

@router.get("/api/locations/{location_id}", response_model=LocationItem)
def get_location_detail(location_id: str):
    """Returns detailed hazard intelligence, upstream catchment info, and precautions for a location."""
    for loc in LOCATIONS_DATA:
        if loc["id"] == location_id:
            return loc
    raise HTTPException(status_code=404, detail=f"Location with id '{location_id}' not found.")

@router.get("/api/map/risk", tags=["Geospatial"])
def get_risk_map_layers():
    """Returns complete geospatial risk features: monitored points, corridors, and terrain metadata."""
    features = []
    for loc in LOCATIONS_DATA:
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
            "rainfall_source": "IMD Regional Weather Network",
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
