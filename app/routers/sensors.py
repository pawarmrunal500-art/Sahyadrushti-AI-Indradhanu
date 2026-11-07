"""
app/routers/sensors.py - IoT Sensor telemetry and protected ingestion.
"""
from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from backend.schemas import SensorNode
from app.db import get_session
from app.auth import verify_sensor_device_key
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
    session: Session = Depends(get_session),
    device_auth = Depends(verify_sensor_device_key)
):
    """
    Protected endpoint for telemetry ingestion from field edge stations (LoRaWAN / Cellular).
    Requires a valid 'X-Device-Key' header mapped to a registered node.
    """
    return repo_ingest_sensor_reading(session, node, user_id=node.sensor_id)
