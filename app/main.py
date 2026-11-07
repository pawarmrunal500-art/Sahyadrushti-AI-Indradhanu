"""
app/main.py - FastAPI Application Factory and Root Assembly.
SAHYADRUSHTI AI - Hyperlocal Landslide & Flash-Flood Intelligence Platform.
UN SDG 13.1 & SDG 11.5
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

from app.routers import (
    system,
    locations,
    weather,
    incidents,
    alerts,
    ml,
    sensors,
)

app = FastAPI(
    title="सह्यादृष्टी | SAHYADRUSHTI AI",
    description="Hyperlocal Climate-Risk Intelligence & Disaster Decision-Support Platform for Lonavala-Khandala-Maval (Western Ghats, Maharashtra). Aligned with UN SDG 13.1.",
    version=settings.APP_VERSION,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular Routers
app.include_router(system.router)
app.include_router(locations.router)
app.include_router(weather.router)
app.include_router(incidents.router)
app.include_router(alerts.router)
app.include_router(ml.router)
app.include_router(sensors.router)
