from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    lat: float
    lon: float

class HazardFactor(BaseModel):
    factor: str
    weight: float
    direction: str  # "increase" or "decrease"
    description: str

class LocationItem(BaseModel):
    id: str
    name: str
    name_mr: str
    name_hi: str
    category: str  # "tourist_spot", "corridor", "settlement", "water_body"
    coordinates: List[float]  # [lat, lon]
    elevation_m: float
    slope_deg: float
    upstream_catchment_km2: Optional[float] = None
    drainage_proximity_m: float
    status: str  # "low", "moderate", "high", "very_high", "unknown"
    status_label: str
    last_updated: str
    telemetry_status: str  # "live", "modelled", "telemetry_unavailable", "simulated"
    current_hazard: str  # "landslide", "flash_flood", "waterlogging", "rockfall", "corridor_disruption"
    risk_score: int  # 0 to 100
    guidance: str
    guidance_mr: str
    guidance_hi: str
    restrictions: Optional[str] = None
    upstream_info: Optional[str] = None
    photo_description: str
    image_url: Optional[str] = None
    tags: List[str] = []

class WeatherObservation(BaseModel):
    location_id: str
    station_name: str
    observation_time: str
    rain_1h_mm: float
    rain_3h_mm: float
    rain_24h_mm: float
    rain_48h_mm: float
    rain_intensity_mm_hr: float
    soil_moisture_pct: float
    temperature_c: float
    humidity_pct: float
    data_source: str
    data_status: str  # "verified_observation", "satellite_modelled", "simulated_station"

class WeatherForecast(BaseModel):
    forecast_time: str
    provider: str
    forecast_3h_mm: float
    forecast_6h_mm: float
    forecast_24h_mm: float
    general_alert: str
    lead_time_hours: int

class PredictionRequest(BaseModel):
    location_id: Optional[str] = None
    hazard_type: str = "landslide"  # "landslide" or "flash_flood"
    rain_1h_mm: float
    rain_24h_mm: float
    rain_48h_mm: float
    forecast_24h_mm: float
    soil_moisture_pct: float
    slope_deg: float
    elevation_m: float = 650.0
    drainage_proximity_m: float = 120.0
    disturbed_slope_prox_m: float = 50.0
    veg_cover_pct: float = 40.0

class PredictionResponse(BaseModel):
    location_id: Optional[str] = None
    hazard_type: str
    risk_level: str  # "low", "moderate", "high", "very_high"
    risk_score: int  # Hyperlocal risk index (0-100)
    score_capped: Optional[bool] = False  # True when score hits model cap (e.g. 96 for hydrological runoff)
    trigger_index: float  # 0.0 - 1.0
    calibrated_probability: Optional[float] = None
    contributing_factors: List[HazardFactor]
    missing_data_flags: List[str]
    uncertainty_level: str  # "low", "medium", "high"
    precautions: List[str]
    model_version: str
    inference_time: str
    validation_status: str

class IncidentRecord(BaseModel):
    id: str
    hazard_type: str
    title: str
    title_mr: str
    date_time: str
    location_name: str
    coordinates: List[float]
    description: str
    source_name: str
    source_url: Optional[str] = None
    verification_status: str  # "Verified official record", "Reported by media", "Unverified report"
    confidence: str  # "High", "Medium", "Approximate location"
    impact_summary: str
    casualties_reported: Optional[str] = None
    image_url: Optional[str] = None
    is_historical: bool = True
    data_origin: Optional[str] = "demo_seed"  # "demo_seed", "live", "user_submitted"

class IncidentSubmission(BaseModel):
    hazard_type: str
    location_name: str
    lat: float
    lon: float
    description: str
    observed_time: str
    reporter_name: Optional[str] = "Anonymous Citizen"
    reporter_contact: Optional[str] = None
    photo_description: Optional[str] = None

class AlertItem(BaseModel):
    id: str
    alert_type: str  # "official_warning", "ai_advisory", "incident_alert", "corridor_closure"
    severity: str    # "advisory", "watch", "warning", "critical"
    issuer: str
    source: str
    source_url: Optional[str] = None
    title: str
    title_mr: str
    title_hi: str
    message: str
    message_mr: str
    message_hi: str
    geographic_coverage: str
    coordinates: Optional[List[float]] = None
    issue_time: str
    expiry_time: str
    approval_status: str  # "approved", "draft", "rejected"
    approved_by: Optional[str] = None
    cap_format: Optional[str] = None
    data_origin: Optional[str] = "demo_seed"  # "demo_seed", "live", "user_submitted"

class SensorNode(BaseModel):
    sensor_id: str
    station_name: str
    sensor_type: str  # "Tipping Bucket Rain Gauge", "FDR Soil Moisture", "Ultrasonic Water Level"
    coordinates: List[float]
    latest_value: float
    unit: str
    last_seen: str
    battery_pct: int
    signal_rssi: int
    health_status: str  # "HEALTHY", "WARNING", "FAULTY"
    quality_flag: str   # "NOMINAL", "SUSPICIOUS_STABLE", "OUT_OF_RANGE", "PACKET_LOSS"
    is_simulated: bool = True
    data_origin: Optional[str] = "demo_seed"  # "demo_seed", "live", "user_submitted"

class ShelterItem(BaseModel):
    id: str
    name: str
    name_mr: str
    name_hi: str
    location_name: str
    coordinates: List[float]
    capacity_persons: int
    facilities: List[str]
    official_contact: str
    managed_by: str
    status: str  # "STANDBY", "ACTIVE_OPEN", "FULL"
    data_origin: Optional[str] = "demo_seed"  # "demo_seed", "live", "user_submitted"

class CorridorItem(BaseModel):
    id: str
    corridor_name: str
    segment_name: str
    coordinates_start: List[float]
    coordinates_end: List[float]
    center_coords: List[float]
    hazard_type: str
    current_status: str  # "NORMAL", "CAUTION", "RESTRICTED", "CLOSED"
    slope_susceptibility: str
    rainfall_trigger_status: str
    verified_disruption: bool
    latest_report_time: str
    source: str
    official_channel: str
    traffic_notes: Optional[str] = None
    data_origin: Optional[str] = "demo_seed"  # "demo_seed", "live", "user_submitted"

class SimulationScenarioRequest(BaseModel):
    scenario_name: str = "Custom Stress Test"
    rain_1h_mm: float
    rain_24h_mm: float
    rain_48h_mm: float
    forecast_24h_mm: float
    soil_moisture_pct: float
    baseline_location_ids: List[str] = ["bhushi_dam", "khandala_expressway", "patan_village", "lonavala_town"]

class ReplayFrame(BaseModel):
    step_index: int
    timestamp_label: str
    rainfall_1h_mm: float
    cumulative_24h_mm: float
    soil_saturation_pct: float
    storm_stage: str
    narrative: str
    narrative_mr: str
    points_state: Dict[str, Dict[str, Any]]
    active_incidents: List[str]
