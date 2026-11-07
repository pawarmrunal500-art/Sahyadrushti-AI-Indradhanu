"""
app/routers/weather.py - Weather observations and forecasts.
"""
from fastapi import APIRouter
from typing import Optional
from app.services.weather import weather_service

router = APIRouter(prefix="/api/weather", tags=["Environmental Data"])

@router.get("/current")
def get_current_weather(location_id: Optional[str] = "bhushi_dam"):
    """
    Returns latest weather observations. Transparently identifies data provider
    and distinguishes measured telemetry from satellite/radar modelled estimates.
    """
    return weather_service.get_current(location_id=location_id or "bhushi_dam")

@router.get("/forecast")
def get_weather_forecast():
    """Returns high-resolution precipitation forecasts with provider metadata and lead times."""
    return weather_service.get_forecast()
