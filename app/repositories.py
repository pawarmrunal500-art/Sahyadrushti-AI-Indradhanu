"""
app/repositories.py - Repository functions for database operations.

Encapsulates all database queries and updates, replacing the in-memory
Python lists with atomic database operations and audit logging.
"""
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
import datetime
import json
import uuid

from app.models import (
    Location, Incident, Alert, WeatherSnapshot,
    RiskScore, AuditLog, User, SensorNodeDB, SensorReading
)
from backend.schemas import IncidentSubmission, SensorNode
from backend.data_layer import LOCATIONS_DATA, HISTORICAL_INCIDENTS, ALERTS_DATA, SENSOR_NODES

# ======================== Audit Log ========================

def log_audit(
    session: Session,
    action: str,
    entity: str,
    entity_id: str,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Append-only audit logging for system actions."""
    audit_entry = AuditLog(
        ts=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        details_json=json.dumps(details, ensure_ascii=False) if details else None
    )
    session.add(audit_entry)
    session.commit()
    session.refresh(audit_entry)
    return audit_entry


# ======================== Locations ========================

def get_locations(session: Session, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all monitored locations, optionally filtered by category."""
    statement = select(Location)
    if category:
        statement = statement.where(Location.category == category)
    results = session.exec(statement).all()
    return [loc.to_schema_dict() for loc in results]

def get_location_by_id(session: Session, location_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single location by its primary key ID."""
    statement = select(Location).where(Location.id == location_id)
    loc = session.exec(statement).first()
    return loc.to_schema_dict() if loc else None

def seed_locations_if_empty(session: Session) -> int:
    """Idempotent seed from LOCATIONS_DATA if table is empty."""
    existing = session.exec(select(Location).limit(1)).first()
    if existing:
        return 0
    count = 0
    for item in LOCATIONS_DATA:
        loc = Location(
            id=item["id"],
            name=item["name"],
            name_mr=item["name_mr"],
            name_hi=item["name_hi"],
            category=item["category"],
            lat=item["coordinates"][0],
            lon=item["coordinates"][1],
            elevation_m=item["elevation_m"],
            slope_deg=item["slope_deg"],
            upstream_catchment_km2=item.get("upstream_catchment_km2"),
            drainage_proximity_m=item["drainage_proximity_m"],
            status=item["status"],
            status_label=item["status_label"],
            last_updated=item["last_updated"],
            telemetry_status=item["telemetry_status"],
            current_hazard=item["current_hazard"],
            risk_score=item["risk_score"],
            guidance=item["guidance"],
            guidance_mr=item["guidance_mr"],
            guidance_hi=item["guidance_hi"],
            restrictions=item.get("restrictions"),
            upstream_info=item.get("upstream_info"),
            photo_description=item["photo_description"],
            image_url=item.get("image_url"),
            tags_json=json.dumps(item.get("tags", []), ensure_ascii=False)
        )
        session.add(loc)
        count += 1
    session.commit()
    return count


# ======================== Incidents ========================

def get_incidents(session: Session, include_historical: bool = True) -> List[Dict[str, Any]]:
    """Retrieve incident records, merging historical and public submissions."""
    statement = select(Incident)
    if not include_historical:
        statement = statement.where(Incident.is_historical == False)  # noqa: E712
    # Order: newest first
    statement = statement.order_by(Incident.created_at.desc())
    results = session.exec(statement).all()
    return [inc.to_schema_dict() for inc in results]

def create_incident(session: Session, payload: IncidentSubmission, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Public citizen submission. Stored strictly with status='Unverified report'.
    Does not affect automated ML model calculations.
    """
    incident_id = f"CROWD-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    incident = Incident(
        id=incident_id,
        hazard_type=payload.hazard_type,
        title=f"Public Report: {payload.hazard_type.replace('_', ' ').title()} near {payload.location_name}",
        title_mr=f"नागरी नोंद: {payload.location_name} परिसरात {payload.hazard_type}",
        date_time=payload.observed_time or now_iso,
        location_name=payload.location_name,
        lat=payload.lat,
        lon=payload.lon,
        description=payload.description,
        source_name=f"Citizen Submission ({payload.reporter_name or 'Anonymous'})",
        source_url=None,
        verification_status="Unverified report",
        confidence="Preliminary / Requires Field Verification",
        impact_summary="Under review by Maval Taluka Disaster Moderation Desk.",
        casualties_reported=None,
        image_url=None,
        is_historical=False,
        data_origin="user_submitted",
        created_at=now_iso
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)

    log_audit(
        session=session,
        action="CREATE_INCIDENT",
        entity="incident",
        entity_id=incident_id,
        user_id=user_id,
        details={"location_name": payload.location_name, "hazard_type": payload.hazard_type}
    )

    return {
        "message": "Incident report submitted successfully for moderation.",
        "incident_id": incident_id,
        "verification_status": "Unverified report",
        "note": "Public safety alert classifications are not altered until verified by authority coordinators."
    }

def seed_incidents_if_empty(session: Session) -> int:
    """Idempotent seed from HISTORICAL_INCIDENTS if table is empty."""
    existing = session.exec(select(Incident).limit(1)).first()
    if existing:
        return 0
    count = 0
    for item in HISTORICAL_INCIDENTS:
        inc = Incident(
            id=item["id"],
            hazard_type=item["hazard_type"],
            title=item["title"],
            title_mr=item["title_mr"],
            date_time=item["date_time"],
            location_name=item["location_name"],
            lat=item["coordinates"][0],
            lon=item["coordinates"][1],
            description=item["description"],
            source_name=item["source_name"],
            source_url=item.get("source_url"),
            verification_status=item["verification_status"],
            confidence=item["confidence"],
            impact_summary=item["impact_summary"],
            casualties_reported=item.get("casualties_reported"),
            image_url=item.get("image_url"),
            is_historical=item.get("is_historical", True),
            data_origin=item.get("data_origin", "demo_seed"),
            created_at=item["date_time"]
        )
        session.add(inc)
        count += 1
    session.commit()
    return count


# ======================== Alerts ========================

def get_alerts(session: Session) -> List[Dict[str, Any]]:
    """Retrieve active and approved alerts."""
    statement = select(Alert).where(Alert.approval_status == "approved")
    # Newest first
    statement = statement.order_by(Alert.issue_time.desc())
    results = session.exec(statement).all()
    return [alert.to_schema_dict() for alert in results]

def create_alert_draft(
    session: Session,
    payload_dict: Dict[str, Any],
    user_id: Optional[str] = None,
    user_pk: Optional[int] = None
) -> Dict[str, Any]:
    """Create a draft alert awaiting authority approval."""
    alert_id = f"ALERT-DRAFT-{uuid.uuid4().hex[:6].upper()}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    expiry_iso = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12)).isoformat()

    alert = Alert(
        id=alert_id,
        alert_type="ai_advisory",
        severity=payload_dict["severity"],
        issuer="Maval Sub-Divisional Emergency Cell",
        source="Authority Operations Desk (Draft)",
        source_url=None,
        title=payload_dict["title"],
        title_mr=payload_dict["title_mr"],
        title_hi=payload_dict.get("title_hi", payload_dict["title"]),
        message=payload_dict["message"],
        message_mr=payload_dict["message_mr"],
        message_hi=payload_dict.get("message_hi", payload_dict["message"]),
        geographic_coverage=payload_dict["geographic_coverage"],
        coordinates_json=None,
        issue_time=now_iso,
        expiry_time=expiry_iso,
        approval_status="draft",
        approved_by=None,
        created_by=user_id,
        created_by_id=user_pk,
        cap_format=None,
        data_origin="live",
        created_at=now_iso
    )
    session.add(alert)
    session.commit()
    session.refresh(alert)

    log_audit(
        session=session,
        action="DRAFT_ALERT",
        entity="alert",
        entity_id=alert_id,
        user_id=user_id,
        details={"severity": payload_dict["severity"], "coverage": payload_dict["geographic_coverage"]}
    )

    return {
        "message": "Alert drafted successfully. Awaiting approval.",
        "alert_id": alert_id,
        "draft": alert.to_schema_dict()
    }

def approve_alert(
    session: Session,
    alert_id: str,
    approver_role: str = "Maval Disaster Officer",
    user_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Approve and publish a drafted alert with audit trail."""
    statement = select(Alert).where(Alert.id == alert_id)
    alert = session.exec(statement).first()
    if not alert:
        return None

    alert.approval_status = "approved"
    alert.approved_by = approver_role
    alert.approved_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    session.add(alert)
    session.commit()
    session.refresh(alert)

    log_audit(
        session=session,
        action="APPROVE_ALERT",
        entity="alert",
        entity_id=alert_id,
        user_id=user_id,
        details={"approver_role": approver_role}
    )

    return {
        "message": f"Alert {alert_id} approved and published.",
        "approval_status": "approved",
        "approved_by": user_id or approver_role,
        "alert": alert.to_schema_dict()
    }

def seed_alerts_if_empty(session: Session) -> int:
    """Idempotent seed from ALERTS_DATA if table is empty."""
    existing = session.exec(select(Alert).limit(1)).first()
    if existing:
        return 0
    count = 0
    for item in ALERTS_DATA:
        coords_str = json.dumps(item["coordinates"]) if item.get("coordinates") else None
        alert = Alert(
            id=item["id"],
            alert_type=item["alert_type"],
            severity=item["severity"],
            issuer=item["issuer"],
            source=item["source"],
            source_url=item.get("source_url"),
            title=item["title"],
            title_mr=item["title_mr"],
            title_hi=item["title_hi"],
            message=item["message"],
            message_mr=item["message_mr"],
            message_hi=item["message_hi"],
            geographic_coverage=item["geographic_coverage"],
            coordinates_json=coords_str,
            issue_time=item["issue_time"],
            expiry_time=item["expiry_time"],
            approval_status=item["approval_status"],
            approved_by=item.get("approved_by"),
            cap_format=item.get("cap_format"),
            data_origin=item.get("data_origin", "demo_seed"),
            created_at=item["issue_time"]
        )
        session.add(alert)
        count += 1
    session.commit()
    return count


# ======================== Sensors ========================

def get_sensors_status(session: Session) -> Dict[str, Any]:
    """Retrieve all sensor nodes, healthy count, and network status."""
    statement = select(SensorNodeDB)
    nodes = session.exec(statement).all()
    node_dicts = [node.to_schema_dict() for node in nodes]
    healthy_count = len([n for n in node_dicts if n.get("health_status") == "HEALTHY"])
    return {
        "network_status": "ONLINE (Persistent Sensor Feeds)",
        "total_nodes": len(node_dicts),
        "healthy_count": healthy_count,
        "nodes": node_dicts,
        "anomaly_detection_rules": [
            "Flag SUSPICIOUS_STABLE if reading remains constant across 4 observation cycles during active rain.",
            "Flag OUT_OF_RANGE if rain intensity exceeds 150 mm/h or soil moisture > 100%.",
            "Flag PACKET_LOSS if last_seen exceeds 30 minutes."
        ]
    }

def ingest_sensor_reading(
    session: Session,
    node: SensorNode,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """Ingest/update a sensor node reading and log to sensor_readings table."""
    node_dict = node.model_dump() if hasattr(node, "model_dump") else node.dict()
    statement = select(SensorNodeDB).where(SensorNodeDB.sensor_id == node.sensor_id)
    existing = session.exec(statement).first()

    status_str = "REGISTERED"
    if existing:
        existing.station_name = node.station_name
        existing.sensor_type = node.sensor_type
        existing.lat = node.coordinates[0]
        existing.lon = node.coordinates[1]
        existing.latest_value = node.latest_value
        existing.unit = node.unit
        existing.last_seen = node.last_seen
        existing.battery_pct = node.battery_pct
        existing.signal_rssi = node.signal_rssi
        existing.health_status = node.health_status
        existing.quality_flag = node.quality_flag
        existing.is_simulated = node.is_simulated
        existing.data_origin = "live"
        session.add(existing)
        status_str = "UPDATED"
    else:
        new_node = SensorNodeDB(
            sensor_id=node.sensor_id,
            station_name=node.station_name,
            sensor_type=node.sensor_type,
            lat=node.coordinates[0],
            lon=node.coordinates[1],
            latest_value=node.latest_value,
            unit=node.unit,
            last_seen=node.last_seen,
            battery_pct=node.battery_pct,
            signal_rssi=node.signal_rssi,
            health_status=node.health_status,
            quality_flag=node.quality_flag,
            is_simulated=node.is_simulated,
            data_origin="live"
        )
        session.add(new_node)

    # Save historical time-series reading
    reading = SensorReading(
        sensor_id=node.sensor_id,
        timestamp=node.last_seen,
        value=node.latest_value,
        battery_pct=node.battery_pct,
        signal_rssi=node.signal_rssi,
        quality_flag=node.quality_flag
    )
    session.add(reading)
    session.commit()

    log_audit(
        session=session,
        action="INGEST_SENSOR",
        entity="sensor",
        entity_id=node.sensor_id,
        user_id=user_id,
        details={"value": node.latest_value, "unit": node.unit, "quality": node.quality_flag}
    )

    return {"status": status_str, "sensor_id": node.sensor_id}

def seed_sensors_if_empty(session: Session) -> int:
    """Idempotent seed from SENSOR_NODES if table is empty."""
    existing = session.exec(select(SensorNodeDB).limit(1)).first()
    if existing:
        return 0
    count = 0
    for item in SENSOR_NODES:
        node = SensorNodeDB(
            sensor_id=item["sensor_id"],
            station_name=item["station_name"],
            sensor_type=item["sensor_type"],
            lat=item["coordinates"][0],
            lon=item["coordinates"][1],
            latest_value=item["latest_value"],
            unit=item["unit"],
            last_seen=item["last_seen"],
            battery_pct=item["battery_pct"],
            signal_rssi=item["signal_rssi"],
            health_status=item["health_status"],
            quality_flag=item["quality_flag"],
            is_simulated=item.get("is_simulated", True),
            data_origin=item.get("data_origin", "demo_seed")
        )
        session.add(node)
        count += 1
    session.commit()
    return count


# ======================== Master Seeder ========================

def seed_all_if_empty(session: Session):
    """Seed all tables if empty upon application startup."""
    seed_locations_if_empty(session)
    seed_incidents_if_empty(session)
    seed_alerts_if_empty(session)
    seed_sensors_if_empty(session)
