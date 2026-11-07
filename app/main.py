"""
app/main.py - FastAPI Application Factory and Root Assembly.
SAHYADRUSHTI AI - Hyperlocal Landslide & Flash-Flood Intelligence Platform.
UN SDG 13.1 & SDG 11.5
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.config import settings
from app.db import init_db, engine
from app.repositories import seed_all_if_empty
from app.scheduler import start_scheduler, shutdown_scheduler
from app.routers import (
    system,
    locations,
    weather,
    incidents,
    alerts,
    ml,
    sensors,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: database initialization, seeding, and scheduler."""
    # 1. Initialize tables
    init_db()
    # 2. Seed tables idempotently if empty
    with Session(engine) as session:
        seed_all_if_empty(session)
    # 3. Start background weather & risk scheduler
    start_scheduler()
    yield
    # 4. Graceful shutdown of scheduler
    shutdown_scheduler()

app = FastAPI(
    title="सह्यादृष्टी | SAHYADRUSHTI AI",
    description="Hyperlocal Climate-Risk Intelligence & Disaster Decision-Support Platform for Lonavala-Khandala-Maval (Western Ghats, Maharashtra). Aligned with UN SDG 13.1.",
    version=settings.APP_VERSION,
    lifespan=lifespan
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
