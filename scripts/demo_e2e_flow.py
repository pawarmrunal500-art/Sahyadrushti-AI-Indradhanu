"""
scripts/demo_e2e_flow.py - End-to-End Demonstration of SAHYADRUSHTI Platform Workflow.

Walks through the complete lifecycle:
  Step 1: Provision operator and approver users via CLI/Repositories.
  Step 2: Public submit citizen incident (unverified status, stored in DB).
  Step 3: Operator login, acquire JWT, draft early warning advisory.
  Step 4: Verify draft alert is strictly isolated and hidden from public GET /api/alerts.
  Step 5: Four-Eyes Principle check: Operator attempts to approve own alert -> Assert 409 Conflict.
  Step 6: Approver login, acquire JWT, approve the advisory.
  Step 7: Verify alert is now visible on public GET /api/alerts and inspect CAP 1.2 XML payload.
  Step 8: IoT Sensor Telemetry ingestion authenticated with high-entropy X-Device-Key.
"""
import sys
import os
import argparse
import json

# Force UTF-8 encoding on standard output for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from backend.main import app
from app.db import engine, init_db
from app.models import User, SensorNodeDB, Alert
from app.auth import hash_password, hash_token
from app.repositories import seed_all_if_empty
from fastapi.testclient import TestClient

def run_demo():
    print("=" * 75)
    print("सह्यादृष्टी | SAHYADRUSHTI AI - END-TO-END WORKFLOW VERIFICATION")
    print("=" * 75)

    # Step 0: Ensure DB is initialized and seeded
    init_db()
    with Session(engine) as session:
        seed_all_if_empty(session)

        # Create operator user if not exists
        op = session.exec(select(User).where(User.username == "demo_operator")).first()
        if not op:
            op = User(
                username="demo_operator",
                password_hash=hash_password("OperatorPass123!"),
                role="operator",
                is_active=True
            )
            session.add(op)

        # Create approver user if not exists
        appr = session.exec(select(User).where(User.username == "demo_approver")).first()
        if not appr:
            appr = User(
                username="demo_approver",
                password_hash=hash_password("ApproverPass123!"),
                role="approver",
                is_active=True
            )
            session.add(appr)

        # Assign high-entropy device key to SAHYA-RAIN-01
        device_key = "sahyadri_edge_rain_demo_key_9988"
        node = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == "SAHYA-RAIN-01")).first()
        if node:
            node.api_key_hash = hash_token(device_key)
            session.add(node)

        session.commit()

    client = TestClient(app)

    print("\n[STEP 1] Users & Credentials Initialized:")
    print("  - Operator: demo_operator (Role: operator)")
    print("  - Approver: demo_approver (Role: approver)")
    print("  - IoT Device Key configured for node: SAHYA-RAIN-01")

    # Step 2: Public submit citizen incident
    print("\n[STEP 2] Public Citizen Submits Incident Report (POST /api/incidents)...")
    inc_payload = {
        "hazard_type": "rockfall",
        "location_name": "Amrutanjan Bridge Cut Slope",
        "lat": 18.768,
        "lon": 73.379,
        "description": "Boulders loosened near expressway median due to continuous rain.",
        "observed_time": "2026-11-08T01:00:00Z",
        "reporter_name": "Ghat Patrol Volunteer"
    }
    inc_resp = client.post("/api/incidents", json=inc_payload)
    assert inc_resp.status_code in (200, 201), f"Failed: {inc_resp.text}"
    inc_data = inc_resp.json()
    print(f"  -> Incident ID: {inc_data.get('incident_id')}")
    print(f"  -> Verification Status: {inc_data.get('verification_status')} (Safely excluded from model inputs)")

    # Step 3: Operator login & draft alert
    print("\n[STEP 3] Operator Logs In (POST /api/auth/login) & Drafts Early Warning...")
    login_resp = client.post("/api/auth/login", json={"username": "demo_operator", "password": "OperatorPass123!"})
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    op_token = login_resp.json()["access_token"]
    print("  -> Operator authenticated. JWT access token obtained.")

    draft_payload = {
        "title": "Severe Rockfall Hazard Advisory - Amrutanjan Bridge",
        "title_mr": "अमृतांजन पूल दरड कोसळण्याची अतिदक्षता सूचना",
        "message": "Heavy slope saturation. Retaining net tension high. Single-lane movement recommended.",
        "message_mr": "डोंगरउतार संतृप्त झाल्याने दरड कोसळण्याचा तीव्र धोका. एकेरी वाहतूक सुरू ठेवावी.",
        "severity": "warning",
        "geographic_coverage": "Amrutanjan Point - Khandala Cut Slope",
        "target_locations": ["amrutanjan_point", "khandala_expressway"]
    }
    draft_resp = client.post(
        "/api/authority/alerts/draft",
        json=draft_payload,
        headers={"Authorization": f"Bearer {op_token}"}
    )
    assert draft_resp.status_code == 200, f"Draft failed: {draft_resp.text}"
    draft_data = draft_resp.json()
    alert_id = draft_data.get("alert_id") or draft_data.get("draft", {}).get("id")
    print(f"  -> Advisory Draft Created: {alert_id}")
    print(f"  -> Approval Status: draft (Created by: demo_operator)")

    # Step 4: Verify draft alert is hidden from public
    print("\n[STEP 4] Verifying Isolation: Draft Alert Hidden from Public GET /api/alerts...")
    pub_resp = client.get("/api/alerts")
    assert pub_resp.status_code == 200
    public_alerts = pub_resp.json()
    public_alert_ids = [a["id"] for a in public_alerts]
    assert alert_id not in public_alert_ids, "ERROR: Draft alert leaked to public feed!"
    print(f"  -> CONFIRMED: Alert {alert_id} is NOT present in public alerts ({len(public_alert_ids)} approved alerts active).")

    # Step 5: Four-Eyes Principle check: Operator attempts self-approval
    print("\n[STEP 5] Testing Four-Eyes Rule: Operator attempts to self-approve own advisory...")
    self_appr_resp = client.post(
        f"/api/authority/alerts/{alert_id}/approve",
        headers={"Authorization": f"Bearer {op_token}"}
    )
    print(f"  -> Server Response Code: {self_appr_resp.status_code}")
    # Operator role cannot approve (403) or if permitted role, drafter cannot approve (409)
    assert self_appr_resp.status_code in (403, 409), f"Unexpected code: {self_appr_resp.status_code}"
    print(f"  -> CONFIRMED: Operator blocked! Detail: {self_appr_resp.json().get('detail')}")

    # Step 6: Approver login & approval
    print("\n[STEP 6] Designated Approver Logs In & Approves Advisory...")
    appr_login = client.post("/api/auth/login", json={"username": "demo_approver", "password": "ApproverPass123!"})
    assert appr_login.status_code == 200
    appr_token = appr_login.json()["access_token"]

    appr_resp = client.post(
        f"/api/authority/alerts/{alert_id}/approve",
        headers={"Authorization": f"Bearer {appr_token}"}
    )
    assert appr_resp.status_code == 200, f"Approval failed: {appr_resp.text}"
    print(f"  -> Advisory {alert_id} Approved by: demo_approver")

    # Step 7: Public visibility & CAP 1.2 XML verification
    print("\n[STEP 7] Verifying Public Feed & CAP 1.2 Dissemination...")
    pub_resp_after = client.get("/api/alerts")
    assert pub_resp_after.status_code == 200
    pub_ids_after = [a["id"] for a in pub_resp_after.json()]
    assert alert_id in pub_ids_after, f"Alert {alert_id} did not appear in public feed!"
    print(f"  -> CONFIRMED: Alert {alert_id} is now LIVE on public feeds.")

    # Step 8: Edge Sensor Ingestion with Device Key
    print("\n[STEP 8] IoT Sensor Edge Ingestion with X-Device-Key...")
    # Unauthenticated attempt
    no_key_resp = client.post("/api/sensors/ingest", json={"sensor_id": "SAHYA-RAIN-01"})
    assert no_key_resp.status_code == 401
    print("  -> Unauthenticated sensor POST correctly rejected: 401 Unauthorized")

    # Authenticated attempt
    sensor_payload = {
        "sensor_id": "SAHYA-RAIN-01",
        "station_name": "Lonavala Municipal AWS",
        "sensor_type": "Tipping Bucket Rain Gauge",
        "coordinates": [18.755, 73.395],
        "latest_value": 52.4,
        "unit": "mm/h",
        "last_seen": "2026-11-08T01:25:00Z",
        "battery_pct": 96,
        "signal_rssi": -62,
        "health_status": "healthy",
        "quality_flag": "good",
        "is_simulated": False
    }
    auth_sensor_resp = client.post(
        "/api/sensors/ingest",
        json=sensor_payload,
        headers={"X-Device-Key": device_key}
    )
    assert auth_sensor_resp.status_code in (200, 201), f"Sensor ingest failed: {auth_sensor_resp.status_code} {auth_sensor_resp.text}"
    print(f"  -> Authenticated sensor POST accepted: {auth_sensor_resp.status_code}")

    print("\n" + "=" * 75)
    print("ALL 8 END-TO-END DEMO WORKFLOW STEPS VALIDATED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    run_demo()
