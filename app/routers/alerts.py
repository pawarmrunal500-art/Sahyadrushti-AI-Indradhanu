"""
app/routers/alerts.py - Public alerts and authority operations desk with database persistence.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Session

from backend.schemas import AlertItem
from app.db import get_session
from app.repositories import (
    get_alerts as repo_get_alerts,
    create_alert_draft as repo_create_alert_draft,
    approve_alert as repo_approve_alert
)

router = APIRouter(tags=["Alerting & Authority Operations"])

@router.get("/api/alerts", response_model=List[AlertItem])
def get_alerts(session: Session = Depends(get_session)):
    """
    Returns active alerts, explicitly distinguishing Official Government Warnings (IMD/NDMA)
    from AI-generated advisories. Includes exportable CAP format.
    """
    return repo_get_alerts(session)

class DraftAlertRequest(BaseModel):
    title: str
    title_mr: str
    message: str
    message_mr: str
    severity: str
    geographic_coverage: str
    target_locations: List[str]

@router.post("/api/authority/alerts/draft")
def draft_authority_alert(
    payload: DraftAlertRequest,
    session: Session = Depends(get_session)
):
    """Allows authorized personnel to draft an advisory before public dissemination."""
    payload_dict = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    return repo_create_alert_draft(session, payload_dict)

@router.post("/api/authority/alerts/{alert_id}/approve")
def approve_authority_alert(
    alert_id: str,
    approver_role: str = Query("Maval Disaster Officer"),
    session: Session = Depends(get_session)
):
    """Approve and publish a drafted alert with audit trail."""
    result = repo_approve_alert(session, alert_id, approver_role=approver_role)
    if not result:
        raise HTTPException(status_code=404, detail="Draft alert not found.")
    return result
