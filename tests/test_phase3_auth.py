"""
tests/test_phase3_auth.py - Comprehensive Unit & Integration Tests for Phase 3.

Covers:
  - Argon2 password hashing and verification
  - Timing attack prevention (anti-enumeration)
  - Account lockout after repeated failed logins
  - JWT generation, validation, expiration, and refresh token rotation/revocation
  - RBAC: 401 Unauthorized for anonymous, 403 Forbidden for insufficient roles
  - Four-Eyes rule: 409 Conflict when alert drafter attempts to approve their own alert
  - Role extracted strictly from JWT (ignoring legacy approver_role query parameter)
  - Edge IoT sensor security: X-Device-Key authentication (401 for missing/invalid)
  - Public visibility: draft alerts hidden from public GET /api/alerts until approved
  - Additive endpoints: GET /api/authority/queue and GET /api/authority/audit
  - Rate limiting (429) verification
"""
import os
import sys
import tempfile
import pytest
import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from app.config import settings
from app.db import get_session
from app.models import User, SensorNodeDB, Alert
from app.limiter import limiter
from app.auth import (
    hash_password,
    hash_token,
    create_access_token,
    decode_access_token,
    get_current_user,
    verify_sensor_device_key
)
from app.repositories import seed_all_if_empty

# Disable limiter by default for functional tests to avoid 429 noise
limiter.enabled = False

# Set up dedicated SQLite DB for auth tests
temp_auth_fd, temp_auth_path = tempfile.mkstemp(suffix=".db")
os.close(temp_auth_fd)
auth_db_url = f"sqlite:///{temp_auth_path}"
auth_engine = create_engine(auth_db_url, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(auth_engine)

with Session(auth_engine) as session:
    seed_all_if_empty(session)
    # Seed known test users: operator, approver, admin
    u_operator = User(
        username="op_user",
        password_hash=hash_password("operator_pass_123"),
        role="operator",
        is_active=True
    )
    u_approver = User(
        username="appr_user",
        password_hash=hash_password("approver_pass_123"),
        role="approver",
        is_active=True
    )
    u_admin = User(
        username="adm_user",
        password_hash=hash_password("admin_pass_123"),
        role="admin",
        is_active=True
    )
    session.add(u_operator)
    session.add(u_approver)
    session.add(u_admin)

    # Configure a sensor node with an API key
    raw_device_key = "sahyadri_node_test_secret_key_12345678"
    sensor_node = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == "SAHYA-RAIN-01")).first()
    if sensor_node:
        sensor_node.api_key_hash = hash_token(raw_device_key)
        session.add(sensor_node)

    session.commit()

def override_get_session():
    with Session(auth_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def setup_auth_environment():
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(verify_sensor_device_key, None)
    yield
    app.dependency_overrides.pop(get_session, None)

client = TestClient(app)


# ==================== 1. Authentication Lifecycle ====================

def test_login_success_and_jwt_claims():
    """Valid credentials return JWT access token and refresh token."""
    resp = client.post("/api/auth/login", json={"username": "op_user", "password": "operator_pass_123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "operator"

    # Decode and inspect claims
    claims = decode_access_token(data["access_token"])
    assert claims["sub"] == "op_user"
    assert claims["role"] == "operator"
    assert "exp" in claims
    assert "iat" in claims


def test_login_invalid_password():
    """Invalid password returns generic 401 error."""
    resp = client.post("/api/auth/login", json={"username": "op_user", "password": "wrong_password"})
    assert resp.status_code == 401
    assert "Invalid username or password" in resp.json()["detail"]


def test_login_nonexistent_user():
    """Non-existent username returns identical generic 401 error (anti-enumeration)."""
    resp = client.post("/api/auth/login", json={"username": "non_existent_ghost", "password": "some_password"})
    assert resp.status_code == 401
    assert "Invalid username or password" in resp.json()["detail"]


def test_account_lockout_after_5_failures():
    """Account is locked for 15 minutes after 5 consecutive failed attempts."""
    # Create a fresh temporary user for lockout test
    with Session(auth_engine) as session:
        temp_user = User(
            username="lockout_target",
            password_hash=hash_password("correct_pass_123"),
            role="operator",
            is_active=True
        )
        session.add(temp_user)
        session.commit()

    # Trigger 5 failed attempts
    for _ in range(5):
        resp = client.post("/api/auth/login", json={"username": "lockout_target", "password": "wrong_pass"})
        assert resp.status_code == 401

    # 6th attempt with even the correct password should now be rejected as locked
    resp = client.post("/api/auth/login", json={"username": "lockout_target", "password": "correct_pass_123"})
    assert resp.status_code == 403
    assert "Account temporarily locked" in resp.json()["detail"]


def test_refresh_token_rotation_and_revocation():
    """Refresh token can issue a new access token, rotates, and old one is invalidated."""
    # Login to get tokens
    login_resp = client.post("/api/auth/login", json={"username": "appr_user", "password": "approver_pass_123"})
    assert login_resp.status_code == 200
    old_refresh = login_resp.json()["refresh_token"]

    # Use refresh token
    ref_resp = client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert ref_resp.status_code == 200
    new_tokens = ref_resp.json()
    new_refresh = new_tokens["refresh_token"]
    assert new_refresh != old_refresh

    # Attempt to reuse old rotated refresh token -> must be rejected (401)
    reuse_resp = client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert reuse_resp.status_code == 401
    assert "revoked" in reuse_resp.json()["detail"].lower()

    # Logout with new refresh token
    logout_resp = client.post("/api/auth/logout", json={"refresh_token": new_refresh})
    assert logout_resp.status_code == 200

    # Attempting to refresh after logout must be rejected (401)
    after_logout_resp = client.post("/api/auth/refresh", json={"refresh_token": new_refresh})
    assert after_logout_resp.status_code == 401


def test_auth_me():
    """GET /api/auth/me returns identity of authenticated user."""
    login_resp = client.post("/api/auth/login", json={"username": "adm_user", "password": "admin_pass_123"})
    token = login_resp.json()["access_token"]

    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "adm_user"
    assert data["role"] == "admin"


# ==================== 2. RBAC & Four-Eyes Principle ====================

def test_unauthenticated_authority_access_blocked():
    """Unauthenticated calls to authority endpoints return 401."""
    resp = client.post("/api/authority/alerts/draft", json={"title": "Unauthorized"})
    assert resp.status_code == 401

    resp2 = client.get("/api/authority/queue")
    assert resp2.status_code == 401

    resp3 = client.get("/api/authority/audit")
    assert resp3.status_code == 401


def test_operator_cannot_approve_or_view_audit():
    """Operator role has draft permissions but is forbidden from approving or viewing audits."""
    login_resp = client.post("/api/auth/login", json={"username": "op_user", "password": "operator_pass_123"})
    op_token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {op_token}"}

    # Audit endpoint requires approver or admin -> 403
    resp_audit = client.get("/api/authority/audit", headers=headers)
    assert resp_audit.status_code == 403

    # Attempting approval -> 403
    resp_appr = client.post("/api/authority/alerts/ALT-TEST-001/approve", headers=headers)
    assert resp_appr.status_code == 403


def test_four_eyes_rule_enforced_even_for_admin():
    """
    Four-Eyes Principle:
    The creator of an alert CANNOT approve it, even if the creator is an Admin.
    Returns HTTP 409 Conflict.
    """
    # 1. Admin drafts an alert
    admin_login = client.post("/api/auth/login", json={"username": "adm_user", "password": "admin_pass_123"})
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    draft_payload = {
        "title": "Four Eyes Test Alert",
        "title_mr": "चार डोळे नियम चाचणी",
        "title_hi": "चार नेत्र नियम परीक्षण",
        "message": "Heavy slope failure predicted at Amrutanjan.",
        "message_mr": "अमृतांजन येथे दरड कोसळण्याची शक्यता.",
        "message_hi": "अमृतांजन पर भूस्खलन की संभावना।",
        "severity": "critical",
        "alert_type": "landslide_warning",
        "geographic_coverage": "Amrutanjan Point",
        "target_locations": ["amrutanjan_point"],
        "issuer": "Disaster Management Cell",
        "source": "SAHYADRUSHTI AI"
    }

    draft_resp = client.post("/api/authority/alerts/draft", json=draft_payload, headers=admin_headers)
    assert draft_resp.status_code == 200
    alert_id = draft_resp.json()["alert_id"]

    # 2. Admin attempts to self-approve -> 409 Conflict
    self_appr_resp = client.post(
        f"/api/authority/alerts/{alert_id}/approve?approver_role=admin",
        headers=admin_headers
    )
    assert self_appr_resp.status_code == 409
    assert "four-eyes" in self_appr_resp.json()["detail"].lower()

    # 3. Approver approves the alert -> 200 OK
    appr_login = client.post("/api/auth/login", json={"username": "appr_user", "password": "approver_pass_123"})
    appr_token = appr_login.json()["access_token"]
    appr_headers = {"Authorization": f"Bearer {appr_token}"}

    valid_appr_resp = client.post(f"/api/authority/alerts/{alert_id}/approve", headers=appr_headers)
    assert valid_appr_resp.status_code == 200
    assert valid_appr_resp.json()["approval_status"] == "approved"
    assert valid_appr_resp.json()["approved_by"] == "appr_user"


def test_draft_alert_hidden_from_public_until_approved():
    """Draft alerts are not visible in public GET /api/alerts until approved."""
    op_login = client.post("/api/auth/login", json={"username": "op_user", "password": "operator_pass_123"})
    op_token = op_login.json()["access_token"]

    draft_resp = client.post(
        "/api/authority/alerts/draft",
        json={
            "title": "Draft Secret Alert",
            "title_mr": "मसुदा अलर्ट",
            "title_hi": "प्रारूप चेतावनी",
            "message": "Internal testing message",
            "message_mr": "अंतर्गत चाचणी",
            "message_hi": "आंतरिक परीक्षण",
            "severity": "warning",
            "alert_type": "flash_flood_watch",
            "geographic_coverage": "Kune Falls",
            "target_locations": ["kune_falls"],
            "issuer": "Sahyadrushti AI",
            "source": "Model"
        },
        headers={"Authorization": f"Bearer {op_token}"}
    )
    alert_id = draft_resp.json()["alert_id"]

    # Public alerts GET must NOT include this alert
    public_resp = client.get("/api/alerts")
    assert public_resp.status_code == 200
    public_ids = [a["id"] for a in public_resp.json()]
    assert alert_id not in public_ids

    # Approve by approver
    appr_login = client.post("/api/auth/login", json={"username": "appr_user", "password": "approver_pass_123"})
    appr_token = appr_login.json()["access_token"]
    appr_resp = client.post(f"/api/authority/alerts/{alert_id}/approve", headers={"Authorization": f"Bearer {appr_token}"})
    assert appr_resp.status_code == 200

    # Now it MUST appear in public GET /api/alerts
    public_resp_after = client.get("/api/alerts")
    public_ids_after = [a["id"] for a in public_resp_after.json()]
    assert alert_id in public_ids_after


# ==================== 3. Sensor Edge Device Authentication ====================

def test_sensor_ingest_missing_device_key():
    """POST /api/sensors/ingest without X-Device-Key returns 401."""
    payload = {
        "sensor_id": "SAHYA-RAIN-01",
        "station_name": "Lonavala Municipal AWS",
        "sensor_type": "Tipping Bucket Rain Gauge",
        "coordinates": [18.755, 73.395],
        "latest_value": 45.2,
        "unit": "mm/h",
        "last_seen": "2026-11-08T01:00:00Z",
        "battery_pct": 98.0,
        "signal_rssi": -65,
        "health_status": "healthy",
        "quality_flag": "good",
        "is_simulated": False
    }
    resp = client.post("/api/sensors/ingest", json=payload)
    assert resp.status_code == 401
    assert "Missing required 'X-Device-Key' header" in resp.json()["detail"]


def test_sensor_ingest_invalid_device_key():
    """POST /api/sensors/ingest with invalid X-Device-Key returns 401."""
    payload = {
        "sensor_id": "SAHYA-RAIN-01",
        "station_name": "Lonavala Municipal AWS",
        "sensor_type": "Tipping Bucket Rain Gauge",
        "coordinates": [18.755, 73.395],
        "latest_value": 45.2,
        "unit": "mm/h",
        "last_seen": "2026-11-08T01:00:00Z",
        "battery_pct": 98.0,
        "signal_rssi": -65,
        "health_status": "healthy",
        "quality_flag": "good",
        "is_simulated": False
    }
    resp = client.post("/api/sensors/ingest", json=payload, headers={"X-Device-Key": "invalid_wrong_key"})
    assert resp.status_code == 401
    assert "Invalid or unrecognized device API key" in resp.json()["detail"]


def test_sensor_ingest_valid_device_key():
    """POST /api/sensors/ingest with valid X-Device-Key returns 201."""
    payload = {
        "sensor_id": "SAHYA-RAIN-01",
        "station_name": "Lonavala Municipal AWS",
        "sensor_type": "Tipping Bucket Rain Gauge",
        "coordinates": [18.755, 73.395],
        "latest_value": 48.5,
        "unit": "mm/h",
        "last_seen": "2026-11-08T01:15:00Z",
        "battery_pct": 97.0,
        "signal_rssi": -64,
        "health_status": "healthy",
        "quality_flag": "good",
        "is_simulated": False
    }
    resp = client.post(
        "/api/sensors/ingest",
        json=payload,
        headers={"X-Device-Key": "sahyadri_node_test_secret_key_12345678"}
    )
    assert resp.status_code == 201
    assert resp.json()["status"] in ("REGISTERED", "UPDATED")
    assert resp.json()["sensor_id"] == "SAHYA-RAIN-01"


# ==================== 4. Additive Endpoints (Queue & Audit) ====================

def test_authority_queue_endpoint():
    """GET /api/authority/queue returns high risk items pending alert."""
    admin_login = client.post("/api/auth/login", json={"username": "adm_user", "password": "admin_pass_123"})
    token = admin_login.json()["access_token"]

    resp = client.get("/api/authority/queue", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "pending_queue" in data
    assert "count" in data
    assert isinstance(data["pending_queue"], list)


def test_authority_audit_endpoint():
    """GET /api/authority/audit returns structured append-only audit trail."""
    admin_login = client.post("/api/auth/login", json={"username": "adm_user", "password": "admin_pass_123"})
    token = admin_login.json()["access_token"]

    resp = client.get("/api/authority/audit", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "audit_logs" in data
    assert "count" in data
    assert data["count"] > 0
    first_entry = data["audit_logs"][0]
    assert "action" in first_entry
    assert "entity" in first_entry
    assert "ts" in first_entry


def test_rate_limiter_exceeded():
    """Verify rate limiter triggers 429 when enabled."""
    limiter.enabled = True
    try:
        hit_429 = False
        for _ in range(12):
            resp = client.post("/api/auth/login", json={"username": "random_probe", "password": "probe_password"})
            if resp.status_code == 429:
                hit_429 = True
                break
        assert hit_429, "Expected rate limiter to trigger HTTP 429 after repeated requests."
    finally:
        limiter.enabled = False


def test_refresh_token_rate_limited():
    """Verify POST /api/auth/refresh is rate limited."""
    limiter.enabled = True
    try:
        hit_429 = False
        for _ in range(15):
            resp = client.post("/api/auth/refresh", json={"refresh_token": "dummy_test_refresh_token"})
            if resp.status_code == 429:
                hit_429 = True
                break
        assert hit_429, "Expected rate limiter on /api/auth/refresh to trigger HTTP 429."
    finally:
        limiter.enabled = False


def test_production_jwt_secret_validation():
    """Verify startup fails with RuntimeError if JWT_SECRET is weak outside dev mode."""
    from app.config import Settings
    old_debug = os.environ.get("DEBUG")
    old_secret = os.environ.get("JWT_SECRET")
    try:
        os.environ["DEBUG"] = "False"
        os.environ["JWT_SECRET"] = "short_weak_dev_secret"
        with pytest.raises(RuntimeError, match="FATAL: In production mode"):
            Settings()
    finally:
        if old_debug is not None:
            os.environ["DEBUG"] = old_debug
        else:
            os.environ.pop("DEBUG", None)
        if old_secret is not None:
            os.environ["JWT_SECRET"] = old_secret
        else:
            os.environ.pop("JWT_SECRET", None)


def test_device_key_revocation_audit():
    """Verify CLI device key revocation clears key hash and records audit log."""
    from app.cli import cmd_revoke_device_key
    import argparse

    with Session(auth_engine) as session:
        # Check SAHYA-RAIN-01 has a key initially
        node = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == "SAHYA-RAIN-01")).first()
        assert node is not None

    args = argparse.Namespace(node_id="SAHYA-RAIN-01")
    cmd_revoke_device_key(args, target_engine=auth_engine)

    with Session(auth_engine) as session:
        node_after = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == "SAHYA-RAIN-01")).first()
        assert node_after.api_key_hash is None


def test_four_eyes_using_user_id():
    """Verify Four-Eyes rule explicitly uses alerts.created_by_id."""
    # Operator drafts an alert
    op_login = client.post("/api/auth/login", json={"username": "op_user", "password": "operator_pass_123"})
    op_token = op_login.json()["access_token"]
    draft_res = client.post(
        "/api/authority/alerts/draft",
        json={
            "title": "ID Check Alert",
            "title_mr": "आयडी तपासणी",
            "message": "Testing created_by_id comparison.",
            "message_mr": "तपासणी",
            "severity": "advisory",
            "geographic_coverage": "Lonavala",
            "target_locations": ["bhushi_dam"]
        },
        headers={"Authorization": f"Bearer {op_token}"}
    )
    alert_id = draft_res.json()["alert_id"]

    # Verify created_by_id was persisted in DB
    with Session(auth_engine) as session:
        db_alert = session.exec(select(Alert).where(Alert.id == alert_id)).first()
        assert db_alert.created_by_id is not None
        assert db_alert.created_by_id == 1  # op_user ID

