"""
app/routers/incidents.py - Incident reporting and retrieval.
"""
from fastapi import APIRouter, status
from typing import List, Dict, Any
import datetime
import uuid
from backend.schemas import IncidentRecord, IncidentSubmission
from backend.data_layer import HISTORICAL_INCIDENTS

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

# In-memory storage for prototype (migrated to DB in Phase 1)
user_submitted_incidents: List[Dict[str, Any]] = []

@router.get("", response_model=List[IncidentRecord])
def get_incidents(include_historical: bool = True):
    """
    Returns incident records with explicit verification status, source URLs,
    and casualty/impact attribution. Merges historical verified events with public submissions.
    """
    all_records = []
    if include_historical:
        all_records.extend(HISTORICAL_INCIDENTS)
    all_records.extend(user_submitted_incidents)
    return all_records

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_incident_report(payload: IncidentSubmission):
    """
    Allows residents or travellers to submit crowdsourced hazard observations.
    New reports are placed into 'Unverified report' queue until moderator review.
    """
    incident_id = f"CROWD-{uuid.uuid4().hex[:8].upper()}"
    new_record = {
        "id": incident_id,
        "hazard_type": payload.hazard_type,
        "title": f"Public Report: {payload.hazard_type.replace('_', ' ').title()} near {payload.location_name}",
        "title_mr": f"नागरी नोंद: {payload.location_name} परिसरात {payload.hazard_type}",
        "date_time": payload.observed_time or datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "location_name": payload.location_name,
        "coordinates": [payload.lat, payload.lon],
        "description": payload.description,
        "source_name": f"Citizen Submission ({payload.reporter_name})",
        "source_url": None,
        "verification_status": "Unverified report",
        "confidence": "Preliminary / Requires Field Verification",
        "impact_summary": "Under review by Maval Taluka Disaster Moderation Desk.",
        "casualties_reported": None,
        "is_historical": False
    }
    user_submitted_incidents.insert(0, new_record)
    return {
        "message": "Incident report submitted successfully for moderation.",
        "incident_id": incident_id,
        "verification_status": "Unverified report",
        "note": "Public safety alert classifications are not altered until verified by authority coordinators."
    }
