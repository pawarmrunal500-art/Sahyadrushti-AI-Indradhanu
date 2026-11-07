"""
app/routers/sensors.py - IoT Sensor telemetry and ingestion with database persistence.
"""
from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from backend.schemas import SensorNode
from app.db import get_session
from app.repositories import (
    get_sensors_status as repo_get_sensors_status,
    ingest_sensor_reading as repo_ingest_sensor_reading
)

router = APIRouter(prefix="/api/sensors", tags=["IoT Sensors"])

@router.get("/status")
def get_sensors_status(session: Session = Depends(get_session)):
    """Returns IoT sensor telemetry, battery levels, signal strength, and anomaly detection flags."""
    return repo_get_sensors_status(session)

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest_sensor_reading(
    node: SensorNode,
    session: Session = Depends(get_session)
):
    """Authorized endpoint for telemetry ingestion from field edge stations (LoRaWAN / Cellular)."""
    return repo_ingest_sensor_reading(session, node)
