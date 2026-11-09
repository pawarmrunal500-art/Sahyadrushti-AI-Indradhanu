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

# Regional Gazetteer for Western Ghats / Maval / Pune places
REGIONAL_GAZETTEER = [
    {
        "id": "kamshet_region",
        "name": "Kamshet",
        "name_mr": "कामशेत",
        "name_hi": "कामशेत",
        "region": "Maval Taluka, Pune District",
        "coordinates": [18.7669, 73.5524],
        "elevation_m": 625.0,
        "slope_deg": 6.5,
        "category": "settlement",
        "display_name": "Kamshet, Maval, Pune District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "moderate",
        "status_label": "Riverine Basin Caution",
        "risk_score": 38,
        "upstream_catchment_km2": 18.4,
        "drainage_proximity_m": 80.0,
        "guidance": "Indrayani river basin; check river crossings and railway underpasses during heavy rain.",
        "guidance_mr": "इंद्रायणी नदीचे खोरे; मुसळधार पावसात नदीकाठचे रस्ते आणि रेल्वे भुयारी मार्गांवर सावधगिरी बाळगा.",
        "guidance_hi": "इंद्रािणी नदी बेसिन; भारी बारिश में नदी तट और अंडरपास पर सतर्क रहें।"
    },
    {
        "id": "karla_region",
        "name": "Karla / Ekvira Caves",
        "name_mr": "कार्ला / एकवीरा देवी / कार्ले लेणी",
        "name_hi": "कार्ला / एकवीरा देवी / कार्ले गुफाएं",
        "region": "Maval Taluka, Pune District",
        "coordinates": [18.7820, 73.4700],
        "elevation_m": 650.0,
        "slope_deg": 18.0,
        "category": "tourist_spot",
        "display_name": "Karla, Maval, Pune District, Maharashtra",
        "hazard_type": "landslide",
        "status": "moderate",
        "status_label": "Moderate Slope Caution",
        "risk_score": 45,
        "upstream_catchment_km2": 3.5,
        "drainage_proximity_m": 45.0,
        "guidance": "Hillside approach to ancient rock caves. Watch for loose rocks on temple steps during rain.",
        "guidance_mr": "प्राचीन लेण्यांकडे जाणारा डोंगर मार्ग. पावसाळ्यात पायऱ्यांवर निसरडेपणा व दगड पडण्यापासून सावध राहा.",
        "guidance_hi": "गुफाओं का पहाड़ी मार्ग। बारिश में सीढ़ियों पर सतर्क रहें।"
    },
    {
        "id": "malavli_region",
        "name": "Malavli",
        "name_mr": "मळवली",
        "name_hi": "मलवडी",
        "region": "Maval Taluka, Pune District",
        "coordinates": [18.7490, 73.4680],
        "elevation_m": 615.0,
        "slope_deg": 8.0,
        "category": "settlement",
        "display_name": "Malavli, Maval, Pune District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "low",
        "status_label": "Low Terrain Risk",
        "risk_score": 28,
        "upstream_catchment_km2": 5.2,
        "drainage_proximity_m": 60.0,
        "guidance": "Gateway to Lohagad & Visapur forts. Check stream crossings along fort base roads.",
        "guidance_mr": "लोहगड-विसापूरचे प्रवेशद्वार. किल्ल्याच्या पायथ्याशी नाल्यांच्या प्रवाहात सावधगिरी बाळगा.",
        "guidance_hi": "लोहगढ़ का आधार। नालों के बहाव पर सतर्क रहें।"
    },
    {
        "id": "pawna_lake",
        "name": "Pawna Lake & Dam",
        "name_mr": "पवना धरण व जलाशय",
        "name_hi": "पवना बांध और झील",
        "region": "Maval Taluka, Pune District",
        "coordinates": [18.6730, 73.4970],
        "elevation_m": 640.0,
        "slope_deg": 12.0,
        "category": "water_body",
        "display_name": "Pawna Dam, Maval, Pune District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "moderate",
        "status_label": "Reservoir Perimeter Alert",
        "risk_score": 52,
        "upstream_catchment_km2": 112.0,
        "drainage_proximity_m": 20.0,
        "guidance": "Major catchment dam. Avoid camping near submerged shoreline during spillway discharge.",
        "guidance_mr": "प्रमुख धरण क्षेत्र. सांडव्यातून पाण्याचा विसर्ग सुरू असताना पाणथळ किनारी जाणे टाळा.",
        "guidance_hi": "प्रमुख बांध क्षेत्र। जल निकासी के समय तट के पास न जाएं।"
    },
    {
        "id": "lohagad_fort",
        "name": "Lohagad Fort",
        "name_mr": "लोहगड किल्ला",
        "name_hi": "लोहगढ़ किला",
        "region": "Western Ghats Escarpment",
        "coordinates": [18.7000, 73.4790],
        "elevation_m": 1033.0,
        "slope_deg": 42.0,
        "category": "tourist_spot",
        "display_name": "Lohagad Fort, Maval, Pune District, Maharashtra",
        "hazard_type": "landslide",
        "status": "high",
        "status_label": "High Escarpment Risk",
        "risk_score": 72,
        "upstream_catchment_km2": 1.5,
        "drainage_proximity_m": 150.0,
        "guidance": "Steep escarpment and Vinchu Kata spur. Severe gale winds and slippery steps during monsoon.",
        "guidance_mr": "उंच कडा आणि विंचूकडा. मुसळधार पावसात पायऱ्या निसरड्या होतात आणि वेगाने वाहणाऱ्या वाऱ्यांपासून सावध राहा.",
        "guidance_hi": "खड़ी चट्टान और तेज हवाएं। बारिश में संभलकर चलें।"
    },
    {
        "id": "visapur_fort",
        "name": "Visapur Fort",
        "name_mr": "विसापूर किल्ला",
        "name_hi": "विसापुर किला",
        "region": "Western Ghats Escarpment",
        "coordinates": [18.7240, 73.4900],
        "elevation_m": 1084.0,
        "slope_deg": 44.0,
        "category": "tourist_spot",
        "display_name": "Visapur Fort, Maval, Pune District, Maharashtra",
        "hazard_type": "landslide",
        "status": "high",
        "status_label": "Waterfall Trail Warning",
        "risk_score": 76,
        "upstream_catchment_km2": 1.8,
        "drainage_proximity_m": 10.0,
        "guidance": "Waterfall trek trail up stone stairs. Risk of rapid water cascades and rock rolls.",
        "guidance_mr": "दगडी पायऱ्यांवरून वाहणारा धबधबा मार्ग. अचानक पाण्याचा जोर वाढण्याची व घसरण्याची शक्यता.",
        "guidance_hi": "सीढ़ियों पर तेज बहाव। पत्थरों के गिरने का जोखिम।"
    },
    {
        "id": "khopoli_town",
        "name": "Khopoli",
        "name_mr": "खोपोली",
        "name_hi": "खोपोली",
        "region": "Khalapur Taluka, Raigad District",
        "coordinates": [18.7890, 73.3440],
        "elevation_m": 85.0,
        "slope_deg": 5.0,
        "category": "settlement",
        "display_name": "Khopoli, Khalapur, Raigad District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "moderate",
        "status_label": "Bhor Ghat Base Caution",
        "risk_score": 42,
        "upstream_catchment_km2": 45.0,
        "drainage_proximity_m": 35.0,
        "guidance": "Bhor Ghat base corridor and Patalganga river. Watch for tailrace surges and urban waterlogging.",
        "guidance_mr": "बोरघाटाचा पायथा आणि पाताळगंगा नदी. सखल भागात पाणी साचणे व घाटातून येणाऱ्या पाण्याच्या प्रवाहावर लक्ष ठेवा.",
        "guidance_hi": "बोरघाट की तलहटी। निचले इलाकों में जलभराव पर नजर रखें।"
    },
    {
        "id": "talegaon_dabhade",
        "name": "Talegaon Dabhade",
        "name_mr": "तळेगाव दाभाडे",
        "name_hi": "तलेगांव दाभाड़े",
        "region": "Maval Taluka, Pune District",
        "coordinates": [18.7300, 73.6800],
        "elevation_m": 610.0,
        "slope_deg": 4.0,
        "category": "settlement",
        "display_name": "Talegaon Dabhade, Pune District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "low",
        "status_label": "Low Plateau Risk",
        "risk_score": 22,
        "upstream_catchment_km2": 8.0,
        "drainage_proximity_m": 120.0,
        "guidance": "Plateau plain urban area. Normal monsoon drainage precautions.",
        "guidance_mr": "सपाट पठारी भाग. सामान्य पावसाळी निचरा दक्षता.",
        "guidance_hi": "मैदानी क्षेत्र। सामान्य जल निकासी सावधानियां।"
    },
    {
        "id": "wadgaon_maval",
        "name": "Wadgaon Maval",
        "name_mr": "वडगाव मावळ",
        "name_hi": "वडगांव मावल",
        "region": "Maval Taluka Administrative Center, Pune",
        "coordinates": [18.7420, 73.6450],
        "elevation_m": 615.0,
        "slope_deg": 4.5,
        "category": "settlement",
        "display_name": "Wadgaon Maval, Pune District, Maharashtra",
        "hazard_type": "flash_flood",
        "status": "low",
        "status_label": "Administrative Hub Clear",
        "risk_score": 24,
        "upstream_catchment_km2": 6.5,
        "drainage_proximity_m": 110.0,
        "guidance": "Taluka administrative headquarters. Emergency operations hub for Maval region.",
        "guidance_mr": "मावळ तालुका प्रशासकीय केंद्र व आपत्ती व्यवस्थापन संपर्क केंद्र.",
        "guidance_hi": "मावल तालुका प्रशासनिक केंद्र।"
    }
]

@router.get("/api/geocode", tags=["Geospatial"])
async def geocode_query(q: str, session: Session = Depends(get_session)):
    """
    Geocode search for regional places, settlements, hills, and landmarks.
    Matches monitored pilot locations, regional gazetteer (Kamshet, Karla, Pawna, etc.),
    and falls back to OpenStreetMap Nominatim with Maharashtra/Western Ghats preference.
    """
    clean_q = (q or "").strip()
    if not clean_q:
        return []

    results = []
    q_lower = clean_q.lower()

    # 1. Search pilot monitored locations in DB
    pilot_locs = get_locations(session)
    for loc in pilot_locs:
        name = loc.get("name", "")
        name_mr = loc.get("name_mr", "")
        name_hi = loc.get("name_hi", "")
        loc_id = loc.get("id", "")
        if (q_lower in name.lower() or q_lower in name_mr.lower() or 
            q_lower in name_hi.lower() or q_lower in loc_id.lower()):
            results.append({
                "id": loc["id"],
                "name": loc["name"],
                "name_mr": loc.get("name_mr", loc["name"]),
                "name_hi": loc.get("name_hi", loc["name"]),
                "region": "Pilot Monitored Zone (Western Ghats)",
                "coordinates": loc["coordinates"],
                "lat": loc["coordinates"][0],
                "lon": loc["coordinates"][1],
                "elevation_m": loc.get("elevation_m", 600.0),
                "slope_deg": loc.get("slope_deg", 15.0),
                "category": loc.get("category", "settlement"),
                "display_name": f"{loc['name']}, Lonavala-Khandala Pilot Zone",
                "hazard_type": loc.get("current_hazard", "landslide"),
                "status": loc.get("status", "moderate"),
                "status_label": loc.get("status_label", "Monitored"),
                "risk_score": loc.get("risk_score", 50),
                "guidance": loc.get("guidance", ""),
                "guidance_mr": loc.get("guidance_mr", ""),
                "guidance_hi": loc.get("guidance_hi", ""),
                "is_monitored": True
            })

    # 2. Search Regional Gazetteer
    for item in REGIONAL_GAZETTEER:
        if (q_lower in item["name"].lower() or 
            q_lower in item["name_mr"].lower() or 
            q_lower in item["name_hi"].lower() or
            q_lower in item["id"].lower()):
            # Avoid duplicate if already matched
            if not any(r["id"] == item["id"] for r in results):
                results.append({
                    **item,
                    "lat": item["coordinates"][0],
                    "lon": item["coordinates"][1],
                    "is_monitored": False
                })

    # 3. If no match and query >= 3 chars, query Nominatim with regional bias
    if len(results) == 0 and len(clean_q) >= 3:
        try:
            import urllib.request
            import urllib.parse
            import json
            encoded = urllib.parse.quote(f"{clean_q}, Maharashtra, India")
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={encoded}&viewbox=73.0,19.0,73.8,18.5&bounded=0&limit=3"
            req = urllib.request.Request(url, headers={"User-Agent": "SahyadrushtiAI/2.1 (contact@sahyadrushti.org)"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for entry in data:
                    lat_f = float(entry.get("lat", 0))
                    lon_f = float(entry.get("lon", 0))
                    display = entry.get("display_name", clean_q)
                    results.append({
                        "id": f"geo_{entry.get('place_id', clean_q)}",
                        "name": entry.get("name", clean_q) or clean_q,
                        "name_mr": clean_q,
                        "name_hi": clean_q,
                        "region": "Geocoded Region (Maharashtra / Western Ghats)",
                        "coordinates": [lat_f, lon_f],
                        "lat": lat_f,
                        "lon": lon_f,
                        "elevation_m": 610.0,
                        "slope_deg": 8.0,
                        "category": "settlement",
                        "display_name": display,
                        "hazard_type": "flash_flood",
                        "status": "moderate",
                        "status_label": "Regional Area",
                        "risk_score": 35,
                        "guidance": f"Location: {display}. Exercise caution in mountain ghat roads and low-lying riverbeds.",
                        "guidance_mr": f"ठिकाण: {display}. घाट रस्ते व सखल भागात पावसाळ्यात दक्षता घ्यावी.",
                        "guidance_hi": f"स्थान: {display}. पहाड़ी रास्तों और निचले क्षेत्रों में सावधानी बरतें।",
                        "is_monitored": False
                    })
        except Exception:
            pass

    return results
