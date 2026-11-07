"""
app/routers/sensors.py - IoT Sensor telemetry and ingestion.
"""
from fastapi import APIRouter, status
from typing import List, Dict, Any
from backend.schemas import SensorNode
from backend.data_layer import SENSOR_NODES

router = APIRouter(prefix="/api/sensors", tags=["IoT Sensors"])

# In-memory storage for prototype (migrated to DB in Phase 1)
live_sensor_registry: List[Dict[str, Any]] = list(SENSOR_NODES)

@router.get("/status")
def get_sensors_status():
    """Returns IoT sensor telemetry, battery levels, signal strength, and anomaly detection flags."""
    return {
        "network_status": "ONLINE (Simulated Prototype Feeds)",
        "total_nodes": len(live_sensor_registry),
        "healthy_count": len([s for s in live_sensor_registry if s.get("health_status") == "HEALTHY"]),
        "nodes": live_sensor_registry,
        "anomaly_detection_rules": [
            "Flag SUSPICIOUS_STABLE if reading remains constant across 4 observation cycles during active rain.",
            "Flag OUT_OF_RANGE if rain intensity exceeds 150 mm/h or soil moisture > 100%.",
            "Flag PACKET_LOSS if last_seen exceeds 30 minutes."
        ]
    }

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest_sensor_reading(node: SensorNode):
    """Authorized endpoint for telemetry ingestion from field edge stations (LoRaWAN / Cellular)."""
    node_dict = node.model_dump() if hasattr(node, "model_dump") else node.dict()
    for idx, s in enumerate(live_sensor_registry):
        if s["sensor_id"] == node.sensor_id:
            live_sensor_registry[idx] = node_dict
            return {"status": "UPDATED", "sensor_id": node.sensor_id}
    live_sensor_registry.append(node_dict)
    return {"status": "REGISTERED", "sensor_id": node.sensor_id}
