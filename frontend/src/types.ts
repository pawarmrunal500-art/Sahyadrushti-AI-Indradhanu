export type HazardType = 'landslide' | 'flash_flood' | 'waterlogging' | 'rockfall' | 'corridor_disruption';

export type RiskLevel = 'low' | 'moderate' | 'high' | 'very_high' | 'unknown';

export interface HazardFactor {
  factor: string;
  weight: number;
  direction: 'increase' | 'decrease';
  description: string;
}

export interface LocationItem {
  id: string;
  name: string;
  name_mr: string;
  name_hi: string;
  category: 'tourist_spot' | 'corridor' | 'settlement' | 'water_body';
  coordinates: [number, number]; // [lat, lon]
  elevation_m: number;
  slope_deg: number;
  upstream_catchment_km2?: number;
  drainage_proximity_m: number;
  status: RiskLevel;
  status_label: string;
  last_updated: string;
  telemetry_status: 'live' | 'modelled' | 'telemetry_unavailable' | 'simulated';
  current_hazard: HazardType;
  risk_score: number;
  guidance: string;
  guidance_mr: string;
  guidance_hi: string;
  restrictions?: string;
  upstream_info?: string;
  photo_description: string;
  image_url?: string;
  tags: string[];
}

export interface WeatherObservation {
  location_id: string;
  station_name: string;
  observation_time: string;
  rain_1h_mm: number;
  rain_3h_mm: number;
  rain_24h_mm: number;
  rain_48h_mm: number;
  rain_intensity_mm_hr: number;
  soil_moisture_pct: number;
  temperature_c: number;
  humidity_pct: number;
  data_source: string;
  data_status: string;
}

export interface IncidentRecord {
  id: string;
  hazard_type: string;
  title: string;
  title_mr: string;
  date_time: string;
  location_name: string;
  coordinates: [number, number];
  description: string;
  source_name: string;
  source_url?: string;
  verification_status: 'Verified official record' | 'Reported by media' | 'Unverified report';
  confidence: string;
  impact_summary: string;
  casualties_reported?: string;
  image_url?: string;
  is_historical: boolean;
  data_origin?: 'demo_seed' | 'live' | 'user_submitted';
}

export interface AlertItem {
  id: string;
  alert_type: 'official_warning' | 'ai_advisory' | 'incident_alert' | 'corridor_closure';
  severity: 'advisory' | 'watch' | 'warning' | 'critical';
  issuer: string;
  source: string;
  source_url?: string;
  title: string;
  title_mr: string;
  title_hi: string;
  message: string;
  message_mr: string;
  message_hi: string;
  geographic_coverage: string;
  coordinates?: [number, number];
  issue_time: string;
  expiry_time: string;
  approval_status: 'draft' | 'approved' | 'rejected';
  approved_by?: string;
  cap_format?: string;
  data_origin?: 'demo_seed' | 'live' | 'user_submitted';
}

export interface ShelterItem {
  id: string;
  name: string;
  name_mr: string;
  name_hi: string;
  location_name: string;
  coordinates: [number, number];
  capacity_persons: number;
  facilities: string[];
  official_contact: string;
  managed_by: string;
  status: 'STANDBY' | 'ACTIVE_OPEN' | 'FULL';
  data_origin?: 'demo_seed' | 'live' | 'user_submitted';
}

export interface CorridorItem {
  id: string;
  corridor_name: string;
  segment_name: string;
  coordinates_start: [number, number];
  coordinates_end: [number, number];
  center_coords: [number, number];
  hazard_type: string;
  current_status: 'NORMAL' | 'CAUTION' | 'RESTRICTED' | 'CLOSED';
  slope_susceptibility: string;
  rainfall_trigger_status: string;
  verified_disruption: boolean;
  latest_report_time: string;
  source: string;
  official_channel: string;
  traffic_notes?: string;
  data_origin?: 'demo_seed' | 'live' | 'user_submitted';
}

export interface SensorNode {
  sensor_id: string;
  station_name: string;
  sensor_type: string;
  coordinates: [number, number];
  latest_value: number;
  unit: string;
  last_seen: string;
  battery_pct: number;
  signal_rssi: number;
  health_status: 'HEALTHY' | 'WARNING' | 'FAULTY';
  quality_flag: 'NOMINAL' | 'SUSPICIOUS_STABLE' | 'OUT_OF_RANGE' | 'PACKET_LOSS';
  is_simulated: boolean;
  data_origin?: 'demo_seed' | 'live' | 'user_submitted';
}

export interface ReplayFrame {
  step_index: number;
  timestamp_label: string;
  rainfall_1h_mm: number;
  cumulative_24h_mm: number;
  soil_saturation_pct: number;
  storm_stage: string;
  narrative: string;
  narrative_mr: string;
  points_state: Record<string, { risk_level: RiskLevel; score: number }>;
  active_incidents: string[];
}

export interface DemoComparison {
  location_name: string;
  lat_lon: [number, number];
  slope_deg: number;
  soil_type: string;
  soil_moisture_pct: number;
  drainage_prox_m: number;
  predicted_hazard: string;
  risk_score: number;
  risk_level: RiskLevel;
  verdict: string;
  verdict_mr: string;
}

export interface DemoScenarioData {
  storm_name: string;
  applied_uniform_rainfall_24h_mm: number;
  applied_uniform_rain_1h_mm: number;
  demonstration_purpose: string;
  comparisons: DemoComparison[];
}

export interface PredictionResponse {
  location_id?: string;
  hazard_type: string;
  risk_level: RiskLevel;
  risk_score: number;
  trigger_index: number;
  calibrated_probability?: number;
  contributing_factors: HazardFactor[];
  missing_data_flags: string[];
  uncertainty_level: 'low' | 'medium' | 'high';
  precautions: string[];
  model_version: string;
  inference_time: string;
  validation_status: string;
}
