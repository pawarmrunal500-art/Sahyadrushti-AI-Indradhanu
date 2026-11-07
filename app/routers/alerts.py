"""
app/routers/alerts.py - Public alerts and authority operations desk.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from pydantic import BaseModel
import datetime
import uuid
from backend.schemas import AlertItem
from backend.data_layer import ALERTS_DATA

router = APIRouter(tags=["Alerting & Authority Operations"])

# In-memory storage for prototype (migrated to DB in Phase 1)
drafted_authority_alerts: List[Dict[str, Any]] = []

@router.get("/api/alerts", response_model=List[AlertItem])
def get_alerts():
    """
    Returns active alerts, explicitly distinguishing Official Government Warnings (IMD/NDMA)
    from AI-generated advisories. Includes exportable CAP format.
    """
    all_alerts = list(ALERTS_DATA)
    for draft in drafted_authority_alerts:
        if draft.get("approval_status") == "approved":
            all_alerts.insert(0, draft)
    return all_alerts

class DraftAlertRequest(BaseModel):
    title: str
    title_mr: str
    message: str
    message_mr: str
    severity: str
    geographic_coverage: str
    target_locations: List[str]

@router.post("/api/authority/alerts/draft")
def draft_authority_alert(payload: DraftAlertRequest):
    """Allows authorized personnel to draft an advisory before public dissemination."""
    alert_id = f"ALERT-DRAFT-{uuid.uuid4().hex[:6].upper()}"
    draft = {
        "id": alert_id,
        "alert_type": "ai_advisory",
        "severity": payload.severity,
        "issuer": "Maval Sub-Divisional Emergency Cell",
        "source": "Authority Operations Desk (Draft)",
        "source_url": None,
        "title": payload.title,
        "title_mr": payload.title_mr,
        "title_hi": payload.title,
        "message": payload.message,
        "message_mr": payload.message_mr,
        "message_hi": payload.message,
        "geographic_coverage": payload.geographic_coverage,
        "issue_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "expiry_time": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12)).isoformat(),
        "approval_status": "draft",
        "approved_by": None,
        "cap_format": None
    }
    drafted_authority_alerts.insert(0, draft)
    return {"message": "Alert drafted successfully. Awaiting approval.", "draft": draft}

@router.post("/api/authority/alerts/{alert_id}/approve")
def approve_authority_alert(alert_id: str, approver_role: str = Query("Maval Disaster Officer")):
    """Approve and publish a drafted alert with audit trail."""
    for draft in drafted_authority_alerts:
        if draft["id"] == alert_id:
            draft["approval_status"] = "approved"
            draft["approved_by"] = approver_role
            draft["approved_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return {"message": f"Alert {alert_id} approved and published.", "alert": draft}
    raise HTTPException(status_code=404, detail="Draft alert not found.")
