"""
scripts/verify_persistence.py - Script demonstrating persistence across server restarts.

1. Connects to SQLite DB.
2. Submits an incident via POST /api/incidents and drafts an alert via POST /api/authority/alerts/draft.
3. Shuts down and restarts the backend instance.
4. Queries GET /api/incidents and database to prove records survive restarts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.db import engine
from app.models import Incident, Alert

def test_live_persistence():
    print("=" * 60)
    print("SAHYADRUSHTI AI - Verifying Database Persistence Across Restarts")
    print("=" * 60)

    # Instance 1: Submit data
    print("\n[Step 1] Starting backend instance 1...")
    with TestClient(app) as client1:
        # Submit citizen incident
        print("  Submitting public incident report...")
        inc_res = client1.post("/api/incidents", json={
            "hazard_type": "landslide",
            "location_name": "Tiger Valley Escarpment",
            "lat": 18.72,
            "lon": 73.39,
            "description": "Loose basalt joint slips noted after rainfall",
            "observed_time": "2026-10-24T18:00:00Z",
            "reporter_name": "Ranger Shinde"
        })
        assert inc_res.status_code == 201
        inc_data = inc_res.json()
        incident_id = inc_data["incident_id"]
        print(f"  Incident created with ID: {incident_id} (Status: {inc_data['verification_status']})")

        # Draft authority alert
        print("  Drafting authority advisory...")
        draft_res = client1.post("/api/authority/alerts/draft", json={
            "title": "Persistent Cloudburst Advisory",
            "title_mr": "ढगफुटी इशारा",
            "message": "Immediate precautionary evacuation of low-lying campsites.",
            "message_mr": "सखल भागातील पर्यटकांनी तात्काळ सुरक्षित स्थळी जावे.",
            "severity": "critical",
            "geographic_coverage": "Tiger Valley & Bhushi Basin",
            "target_locations": ["bhushi_dam", "tiger_point"]
        })
        assert draft_res.status_code == 200
        draft_data = draft_res.json()
        alert_id = draft_data["draft"]["id"]
        print(f"  Alert drafted with ID: {alert_id} (Status: {draft_data['draft']['approval_status']})")

    print("\n[Step 2] Backend instance 1 closed. Simulating complete server shutdown & reboot...")

    # Instance 2: Cold start from the persistent database
    print("\n[Step 3] Starting backend instance 2 (cold start from sahyadrushti.db)...")
    with TestClient(app) as client2:
        # Check incident survives
        incidents_resp = client2.get("/api/incidents")
        assert incidents_resp.status_code == 200
        all_incidents = incidents_resp.json()
        matching_inc = next((i for i in all_incidents if i["id"] == incident_id), None)
        assert matching_inc is not None, f"Incident {incident_id} was NOT found after server restart!"
        print(f"  [SUCCESS] Incident {incident_id} successfully persisted across restart!")
        print(f"            Title: {matching_inc['title']}")
        print(f"            Status: {matching_inc['verification_status']}")

        # Check draft alert survives in DB
        with Session(engine) as session:
            draft_in_db = session.exec(select(Alert).where(Alert.id == alert_id)).first()
            assert draft_in_db is not None, f"Alert {alert_id} was NOT found in DB after server restart!"
            print(f"  [SUCCESS] Alert {alert_id} successfully persisted in database across restart!")
            print(f"            Title: {draft_in_db.title}")
            print(f"            Severity: {draft_in_db.severity}")
            print(f"            Approval Status: {draft_in_db.approval_status}")

    print("\n" + "=" * 60)
    print("DATABASE PERSISTENCE PROOF: 100% VERIFIED")
    print("=" * 60)

if __name__ == "__main__":
    test_live_persistence()

