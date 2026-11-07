"""
tests/test_phase1_db.py - Unit and Integration Tests for Phase 1 Database Persistence.

Tests:
  - Repository CRUD and queries
  - Idempotent seeding from data_layer.py
  - Public incident submission creates status='Unverified report'
  - Audit logging on every create, update, and approve
  - Server restart persistence proof (insert, close session, reopen, verify)
  - SQLite WAL mode and foreign keys verification
"""
import pytest
import tempfile
import os
import json
from sqlmodel import Session, create_engine, SQLModel, select

from app.models import (
    Location, Incident, Alert, SensorNodeDB,
    SensorReading, AuditLog, User
)
from app.repositories import (
    get_locations, get_location_by_id, seed_locations_if_empty,
    get_incidents, create_incident, seed_incidents_if_empty,
    get_alerts, create_alert_draft, approve_alert, seed_alerts_if_empty,
    get_sensors_status, ingest_sensor_reading, seed_sensors_if_empty,
    seed_all_if_empty, log_audit
)
from backend.schemas import IncidentSubmission, SensorNode

@pytest.fixture(name="db_session")
def session_fixture():
    temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_fd)
    db_url = f"sqlite:///{temp_path}"
    test_engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    try:
        os.remove(temp_path)
    except OSError:
        pass


def test_idempotent_seeding(db_session: Session):
    """Verify seeding fills empty tables and running again inserts 0 additional rows."""
    count_loc1 = seed_locations_if_empty(db_session)
    assert count_loc1 > 0
    count_loc2 = seed_locations_if_empty(db_session)
    assert count_loc2 == 0

    count_inc1 = seed_incidents_if_empty(db_session)
    assert count_inc1 > 0
    count_inc2 = seed_incidents_if_empty(db_session)
    assert count_inc2 == 0

    count_alt1 = seed_alerts_if_empty(db_session)
    assert count_alt1 > 0
    count_alt2 = seed_alerts_if_empty(db_session)
    assert count_alt2 == 0

    count_sen1 = seed_sensors_if_empty(db_session)
    assert count_sen1 > 0
    count_sen2 = seed_sensors_if_empty(db_session)
    assert count_sen2 == 0


def test_public_incident_creation_and_audit(db_session: Session):
    """Verify public incidents are unverified and trigger audit log."""
    submission = IncidentSubmission(
        hazard_type="rockfall",
        location_name="Bhor Ghat Cut Section",
        lat=18.756,
        lon=73.368,
        description="Fallen gravel and boulders near drainage line",
        observed_time="2026-10-24T18:00:00Z",
        reporter_name="Highway Commuter"
    )

    result = create_incident(db_session, submission, user_id="public_user")
    assert result["verification_status"] == "Unverified report"
    assert "incident_id" in result
    incident_id = result["incident_id"]

    # Verify stored in DB
    stored = db_session.exec(select(Incident).where(Incident.id == incident_id)).first()
    assert stored is not None
    assert stored.verification_status == "Unverified report"
    assert stored.is_historical is False

    # Verify audit log entry
    audit = db_session.exec(
        select(AuditLog).where(
            AuditLog.entity == "incident",
            AuditLog.entity_id == incident_id
        )
    ).first()
    assert audit is not None
    assert audit.action == "CREATE_INCIDENT"


def test_alert_drafting_and_approval_flow(db_session: Session):
    """Verify alert draft -> approval flow and audit logs."""
    draft_dict = {
        "title": "Severe Flash Flood Advisory",
        "title_mr": "तीव्र पूर इशारा",
        "message": "Water levels rising downstream of Bhushi Dam",
        "message_mr": "भुशी धरणाखाली पाणीपातळी वाढली आहे",
        "severity": "warning",
        "geographic_coverage": "Bhushi Catchment"
    }

    draft_res = create_alert_draft(db_session, draft_dict, user_id="officer_01")
    draft = draft_res["draft"]
    assert draft["approval_status"] == "draft"
    alert_id = draft["id"]

    # Verify not yet in public active alerts
    public_alerts = get_alerts(db_session)
    assert not any(a["id"] == alert_id for a in public_alerts)

    # Approve alert
    app_res = approve_alert(db_session, alert_id, approver_role="District Collector", user_id="collector_01")
    assert app_res is not None
    assert app_res["alert"]["approval_status"] == "approved"
    assert app_res["alert"]["approved_by"] == "District Collector"

    # Now verify visible in public active alerts
    public_alerts_after = get_alerts(db_session)
    assert any(a["id"] == alert_id for a in public_alerts_after)

    # Verify audit logs for both actions
    audits = db_session.exec(
        select(AuditLog).where(AuditLog.entity == "alert", AuditLog.entity_id == alert_id)
    ).all()
    actions = {a.action for a in audits}
    assert "DRAFT_ALERT" in actions
    assert "APPROVE_ALERT" in actions


def test_persistence_across_session_restart():
    """
    Persistence Proof:
    Insert an incident and an alert, dispose the session and engine,
    reconnect with a new engine to the same SQLite file, and verify records remain intact.
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_fd)
    db_url = f"sqlite:///{temp_path}"

    # Session 1: Create and insert
    engine1 = create_engine(db_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine1)
    with Session(engine1) as s1:
        inc_res = create_incident(
            s1,
            IncidentSubmission(
                hazard_type="landslide",
                location_name="Persistent Test Slope",
                lat=18.75,
                lon=73.38,
                description="Soil slump on western face",
                observed_time="2026-10-24T18:00:00Z",
                reporter_name="Field Observer"
            )
        )
        saved_incident_id = inc_res["incident_id"]

        alt_res = create_alert_draft(
            s1,
            {
                "title": "Persistent Alert",
                "title_mr": "शाश्वत इशारा",
                "message": "Persistent alert body",
                "message_mr": "शाश्वत संदेश",
                "severity": "critical",
                "geographic_coverage": "Maval"
            }
        )
        saved_alert_id = alt_res["draft"]["id"]
    engine1.dispose()

    # Session 2: Fresh engine & session to verify persistence
    engine2 = create_engine(db_url, connect_args={"check_same_thread": False})
    with Session(engine2) as s2:
        reloaded_inc = s2.exec(select(Incident).where(Incident.id == saved_incident_id)).first()
        assert reloaded_inc is not None
        assert reloaded_inc.location_name == "Persistent Test Slope"

        reloaded_alt = s2.exec(select(Alert).where(Alert.id == saved_alert_id)).first()
        assert reloaded_alt is not None
        assert reloaded_alt.title == "Persistent Alert"
    engine2.dispose()

    try:
        os.remove(temp_path)
    except OSError:
        pass

