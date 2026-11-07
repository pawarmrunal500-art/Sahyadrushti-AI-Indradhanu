"""
app/routers/alerts.py - Public alerts, authority operations desk, and moderation queue.
"""
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sqlmodel import Session, select
import logging
import datetime

from backend.schemas import AlertItem
from app.db import get_session
from app.models import Alert, Location, AuditLog, User
from app.auth import require_role, get_current_user
from app.repositories import (
    get_alerts as repo_get_alerts,
    create_alert_draft as repo_create_alert_draft,
    approve_alert as repo_approve_alert,
    log_audit
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Alerting & Authority Operations"])

@router.get("/api/alerts", response_model=List[AlertItem])
def get_alerts(session: Session = Depends(get_session)):
    """
    Returns active alerts. Strictly filters to approval_status='approved' so
    unapproved/drafted advisories are NEVER visible to the public.
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
    current_user: User = Depends(require_role("operator", "approver", "admin")),
    session: Session = Depends(get_session)
):
    """
    Allows authorized operators to draft an advisory before public dissemination.
    Stores creator identity for Four-Eyes enforcement.
    """
    payload_dict = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    return repo_create_alert_draft(
        session,
        payload_dict,
        user_id=current_user.username,
        user_pk=current_user.id
    )

@router.post("/api/authority/alerts/{alert_id}/approve")
def approve_authority_alert(
    alert_id: str,
    approver_role: Optional[str] = Query(None),
    current_user: User = Depends(require_role("approver", "admin")),
    session: Session = Depends(get_session)
):
    """
    Approve and publish a drafted alert with audit trail.
    Enforces Four-Eyes Principle: drafter cannot approve their own alert (HTTP 409).
    Identity and role derived strictly from JWT, query parameter is ignored.
    """
    if approver_role:
        logger.info(
            "Legacy query param approver_role='%s' provided by user '%s'; ignored in favor of verified JWT identity.",
            approver_role,
            current_user.username
        )

    # 1. Fetch draft alert
    statement = select(Alert).where(Alert.id == alert_id)
    alert = session.exec(statement).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Draft alert not found.")

    # 2. Four-Eyes Rule Enforcement (Using user ID as primary comparator)
    is_self_approval = False
    if alert.created_by_id is not None and current_user.id is not None:
        if alert.created_by_id == current_user.id:
            is_self_approval = True
    elif alert.created_by and alert.created_by == current_user.username:
        is_self_approval = True

    if is_self_approval:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Four-Eyes Principle violation: user '{current_user.username}' cannot approve an advisory they drafted."
        )

    # 3. Approve and publish
    actual_role_label = f"{current_user.username} ({current_user.role})"
    result = repo_approve_alert(
        session,
        alert_id,
        approver_role=actual_role_label,
        user_id=current_user.username
    )
    return result

@router.get("/api/authority/queue")
def get_authority_queue(
    current_user: User = Depends(require_role("operator", "approver", "admin")),
    session: Session = Depends(get_session)
):
    """
    Lists locations whose latest risk score crossed the critical threshold (>= 70)
    and are not yet addressed by an active approved alert.
    """
    # 1. High risk locations (score >= 70)
    high_risk_locs = session.exec(
        select(Location).where(Location.risk_score >= 70)
    ).all()

    # 2. Approved alerts to check coverage
    active_alerts = session.exec(
        select(Alert).where(Alert.approval_status == "approved")
    ).all()
    addressed_locations = set()
    for a in active_alerts:
        # Check title or message mentions or coverage
        for loc in high_risk_locs:
            if loc.id in (a.title + a.message + a.geographic_coverage).lower() or loc.name.lower() in (a.title + a.message).lower():
                addressed_locations.add(loc.id)

    unaddressed_queue = []
    for loc in high_risk_locs:
        unaddressed_queue.append({
            "location_id": loc.id,
            "name": loc.name,
            "name_mr": loc.name_mr,
            "risk_score": loc.risk_score,
            "status": loc.status,
            "hazard_type": loc.current_hazard,
            "slope_deg": loc.slope_deg,
            "requires_action": loc.id not in addressed_locations,
            "recommended_action": f"Draft early warning advisory for {loc.name} ({loc.current_hazard.replace('_', ' ').title()})"
        })

    return {
        "queue_count": len(unaddressed_queue),
        "count": len(unaddressed_queue),
        "unaddressed_count": sum(1 for item in unaddressed_queue if item["requires_action"]),
        "queue": unaddressed_queue,
        "pending_queue": unaddressed_queue
    }

@router.get("/api/authority/audit")
def get_authority_audit_log(
    limit: int = 100,
    current_user: User = Depends(require_role("approver", "admin")),
    session: Session = Depends(get_session)
):
    """Audit log viewer for platform administrators and approvers."""
    statement = select(AuditLog).order_by(AuditLog.ts.desc()).limit(limit)
    entries = session.exec(statement).all()
    records = [
        {
            "id": e.id,
            "ts": e.ts,
            "timestamp": e.ts,
            "user_id": e.user_id,
            "action": e.action,
            "entity": e.entity,
            "entity_id": e.entity_id,
            "details": e.details_json
        }
        for e in entries
    ]
    return {
        "total_records": len(entries),
        "count": len(entries),
        "records": records,
        "audit_logs": records
    }
