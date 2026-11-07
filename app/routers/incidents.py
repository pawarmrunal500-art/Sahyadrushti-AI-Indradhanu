"""
app/routers/incidents.py - Incident reporting and retrieval with database persistence.
"""
from fastapi import APIRouter, status, Depends
from typing import List
from sqlmodel import Session

from backend.schemas import IncidentRecord, IncidentSubmission
from app.db import get_session
from app.repositories import get_incidents as repo_get_incidents, create_incident as repo_create_incident

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentRecord])
def get_incidents(
    include_historical: bool = True,
    session: Session = Depends(get_session)
):
    """
    Returns incident records with explicit verification status, source URLs,
    and casualty/impact attribution. Merges historical verified events with public submissions.
    """
    return repo_get_incidents(session, include_historical=include_historical)

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_incident_report(
    payload: IncidentSubmission,
    session: Session = Depends(get_session)
):
    """
    Allows residents or travellers to submit crowdsourced hazard observations.
    New reports are placed into 'Unverified report' queue until moderator review.
    Persisted to database with audit log entry.
    """
    return repo_create_incident(session, payload)
