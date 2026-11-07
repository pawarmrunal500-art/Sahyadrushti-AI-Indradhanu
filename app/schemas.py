"""
app/schemas.py - Re-export of API contract schemas.

The canonical Pydantic schemas live in backend/schemas.py
and define the API contract with the frontend. This module
re-exports them so that the new app/ package can import
from a single consistent location.

IMPORTANT: These schemas are the API contract. Never rename or
remove fields. Only additive changes (new optional fields) are safe.
"""

# Re-export everything from the original schemas module
from backend.schemas import (  # noqa: F401
    Coordinate,
    HazardFactor,
    LocationItem,
    WeatherObservation,
    WeatherForecast,
    PredictionRequest,
    PredictionResponse,
    IncidentRecord,
    IncidentSubmission,
    AlertItem,
    SensorNode,
    ShelterItem,
    CorridorItem,
    SimulationScenarioRequest,
    ReplayFrame,
)

