"""
backend/main.py - Backward-Compatibility Adapter for SAHYADRUSHTI AI.

This module wraps the modular app/ package while preserving
all legacy imports and run commands (e.g. uvicorn.run("backend.main:app")).
"""
import sys
import os

# Ensure project root is in search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.main import app  # Canonical FastAPI application
from app.services.risk import risk_service
ml_service = risk_service.engine

# Legacy list compatibility placeholders
user_submitted_incidents = []
drafted_authority_alerts = []
live_sensor_registry = []

__all__ = [
    "app",
    "user_submitted_incidents",
    "drafted_authority_alerts",
    "live_sensor_registry",
    "ml_service",
]
