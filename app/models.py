"""
app/models.py - SQLModel ORM entities for persistent storage.

Tables:
  - locations
  - incidents
  - alerts
  - weather_snapshots
  - risk_scores
  - audit_log (append-only)
  - users
  - sensor_nodes
  - sensor_readings
"""
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column
import sqlalchemy as sa
import datetime
import json

class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: str = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    name_mr: str
    name_hi: str
    category: str = Field(index=True)  # "tourist_spot", "corridor", "settlement", "water_body"
    lat: float
    lon: float
    elevation_m: float
    slope_deg: float
    upstream_catchment_km2: Optional[float] = None
    drainage_proximity_m: float
    status: str = Field(index=True)  # "low", "moderate", "high", "very_high", "unknown"
    status_label: str
    last_updated: str
    telemetry_status: str  # "live", "modelled", "telemetry_unavailable", "simulated"
    current_hazard: str  # "landslide", "flash_flood", "waterlogging", "rockfall", "corridor_disruption"
    risk_score: int
    guidance: str
    guidance_mr: str
    guidance_hi: str
    restrictions: Optional[str] = None
    upstream_info: Optional[str] = None
    photo_description: str
    image_url: Optional[str] = None
    tags_json: str = Field(default="[]")  # Serialized JSON list of strings

    def to_schema_dict(self) -> Dict[str, Any]:
        """Convert ORM model to dictionary conforming to LocationItem schema."""
        tags = []
        try:
            tags = json.loads(self.tags_json) if self.tags_json else []
        except Exception:
            tags = []
        return {
            "id": self.id,
            "name": self.name,
            "name_mr": self.name_mr,
            "name_hi": self.name_hi,
            "category": self.category,
            "coordinates": [self.lat, self.lon],
            "elevation_m": self.elevation_m,
            "slope_deg": self.slope_deg,
            "upstream_catchment_km2": self.upstream_catchment_km2,
            "drainage_proximity_m": self.drainage_proximity_m,
            "status": self.status,
            "status_label": self.status_label,
            "last_updated": self.last_updated,
            "telemetry_status": self.telemetry_status,
            "current_hazard": self.current_hazard,
            "risk_score": self.risk_score,
            "guidance": self.guidance,
            "guidance_mr": self.guidance_mr,
            "guidance_hi": self.guidance_hi,
            "restrictions": self.restrictions,
            "upstream_info": self.upstream_info,
            "photo_description": self.photo_description,
            "image_url": self.image_url,
            "tags": tags
        }


class Incident(SQLModel, table=True):
    __tablename__ = "incidents"

    id: str = Field(primary_key=True, index=True)
    location_id: Optional[str] = Field(default=None, index=True)
    hazard_type: str = Field(index=True)
    title: str
    title_mr: str
    date_time: str
    location_name: str
    lat: float
    lon: float
    description: str
    source_name: str
    source_url: Optional[str] = None
    verification_status: str = Field(index=True)  # "Verified official record", "Reported by media", "Unverified report"
    confidence: str
    impact_summary: str
    casualties_reported: Optional[str] = None
    image_url: Optional[str] = None
    is_historical: bool = Field(default=False, index=True)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None

    def to_schema_dict(self) -> Dict[str, Any]:
        """Convert ORM model to dictionary conforming to IncidentRecord schema."""
        return {
            "id": self.id,
            "hazard_type": self.hazard_type,
            "title": self.title,
            "title_mr": self.title_mr,
            "date_time": self.date_time,
            "location_name": self.location_name,
            "coordinates": [self.lat, self.lon],
            "description": self.description,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "verification_status": self.verification_status,
            "confidence": self.confidence,
            "impact_summary": self.impact_summary,
            "casualties_reported": self.casualties_reported,
            "image_url": self.image_url,
            "is_historical": self.is_historical
        }


class Alert(SQLModel, table=True):
    __tablename__ = "alerts"

    id: str = Field(primary_key=True, index=True)
    alert_type: str = Field(index=True)  # "official_warning", "ai_advisory", "incident_alert", "corridor_closure"
    severity: str = Field(index=True)    # "advisory", "watch", "warning", "critical"
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
    coordinates_json: Optional[str] = None  # JSON list [lat, lon] or polygon
    issue_time: str
    expiry_time: str
    approval_status: str = Field(index=True)  # "draft", "approved", "rejected", "dispatched", "cancelled"
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    created_by: Optional[str] = None
    created_by_id: Optional[int] = Field(default=None, index=True)
    cap_format: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_schema_dict(self) -> Dict[str, Any]:
        """Convert ORM model to dictionary conforming to AlertItem schema."""
        coords = None
        if self.coordinates_json:
            try:
                coords = json.loads(self.coordinates_json)
            except Exception:
                coords = None
        return {
            "id": self.id,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "issuer": self.issuer,
            "source": self.source,
            "source_url": self.source_url,
            "title": self.title,
            "title_mr": self.title_mr,
            "title_hi": self.title_hi,
            "message": self.message,
            "message_mr": self.message_mr,
            "message_hi": self.message_hi,
            "geographic_coverage": self.geographic_coverage,
            "coordinates": coords,
            "issue_time": self.issue_time,
            "expiry_time": self.expiry_time,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "cap_format": self.cap_format
        }


class WeatherSnapshot(SQLModel, table=True):
    __tablename__ = "weather_snapshots"

    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: str = Field(index=True)
    fetched_at: str = Field(index=True, default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    rain_mm_1h: float
    rain_mm_24h: float
    soil_moisture: float
    source: str  # "open-meteo-live", "open-meteo-archive", "mock-pilot"
    raw_json: str  # Full raw payload for auditability


class RiskScore(SQLModel, table=True):
    __tablename__ = "risk_scores"

    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: str = Field(index=True)
    computed_at: str = Field(index=True, default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    score: int
    level: str  # "low", "moderate", "high", "very_high"
    fs: Optional[float] = None  # Factor of Safety
    top_factors_json: str  # Serialized JSON list of contributing factors
    model_version: str


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    ts: str = Field(index=True, default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    user_id: Optional[str] = Field(default=None, index=True)
    action: str = Field(index=True)  # e.g. "CREATE", "UPDATE", "APPROVE", "INGEST", "LOGIN"
    entity: str = Field(index=True)  # e.g. "incident", "alert", "sensor", "user"
    entity_id: str
    details_json: Optional[str] = None


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="operator", index=True)  # "operator", "approver", "admin"
    is_active: bool = Field(default=True)
    failed_login_attempts: int = Field(default=0)
    locked_until: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    token_hash: str = Field(unique=True, index=True)
    expires_at: str = Field(index=True)
    revoked: bool = Field(default=False, index=True)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class SensorNodeDB(SQLModel, table=True):
    __tablename__ = "sensor_nodes"

    sensor_id: str = Field(primary_key=True, index=True)
    station_name: str
    sensor_type: str
    lat: float
    lon: float
    latest_value: float
    unit: str
    last_seen: str
    battery_pct: int
    signal_rssi: int
    health_status: str  # "HEALTHY", "WARNING", "FAULTY"
    quality_flag: str   # "NOMINAL", "SUSPICIOUS_STABLE", "OUT_OF_RANGE", "PACKET_LOSS"
    is_simulated: bool = Field(default=True)
    api_key_hash: Optional[str] = None  # For Phase 3 device auth

    def to_schema_dict(self) -> Dict[str, Any]:
        """Convert ORM model to dictionary conforming to SensorNode schema."""
        return {
            "sensor_id": self.sensor_id,
            "station_name": self.station_name,
            "sensor_type": self.sensor_type,
            "coordinates": [self.lat, self.lon],
            "latest_value": self.latest_value,
            "unit": self.unit,
            "last_seen": self.last_seen,
            "battery_pct": self.battery_pct,
            "signal_rssi": self.signal_rssi,
            "health_status": self.health_status,
            "quality_flag": self.quality_flag,
            "is_simulated": self.is_simulated
        }


class SensorReading(SQLModel, table=True):
    __tablename__ = "sensor_readings"

    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: str = Field(index=True)
    timestamp: str = Field(index=True, default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    value: float
    battery_pct: int
    signal_rssi: int
    quality_flag: str
