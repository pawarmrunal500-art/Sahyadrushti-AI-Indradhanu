"""
app/routers/weather.py - Weather observations and forecasts.
"""
from fastapi import APIRouter, Depends
from typing import Optional
from sqlmodel import Session
from app.db import get_session
from app.services.weather import weather_service

router = APIRouter(prefix="/api/weather", tags=["Environmental Data"])

@router.get("/current")
def get_current_weather(
    location_id: Optional[str] = "bhushi_dam",
    session: Session = Depends(get_session)
):
    """
    Returns latest weather observations. Transparently identifies data provider
    and distinguishes measured telemetry from satellite/radar modelled estimates.
    """
    return weather_service.get_current_sync(
        location_id=location_id or "bhushi_dam",
        session=session
    )

@router.get("/forecast")
def get_weather_forecast():
    """Returns high-resolution precipitation forecasts with provider metadata and lead times."""
    return weather_service.get_forecast()
