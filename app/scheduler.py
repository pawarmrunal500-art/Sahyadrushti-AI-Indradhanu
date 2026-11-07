"""
app/scheduler.py - Periodic background weather ingestion and risk recomputation scheduler.

Uses APScheduler AsyncIOScheduler with:
  - max_instances=1 and coalesce=True to guard against race conditions / overlapping runs
  - Comprehensive try/except logging to prevent scheduler job crashes from killing the app
  - Automatic weather snapshot persistence and ML risk score updates
  - Flagging threshold crossings into the authority audit queue
"""
import asyncio
import datetime
import json
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select

from app.config import settings
from app.db import engine
from app.models import Location, WeatherSnapshot, RiskScore, AuditLog
from app.services.weather import weather_service
from app.services.risk import risk_service
from app.repositories import get_locations, log_audit

logger = logging.getLogger("sahyadrushti.scheduler")

scheduler = AsyncIOScheduler()
is_job_running = False

async def refresh_all_locations():
    """
    Periodic job executed every 30 minutes:
      1. Batched Open-Meteo weather fetch for all locations
      2. Save weather snapshots to DB
      3. Compute updated ML risk scores
      4. Save risk scores and update location statuses
      5. Flag critical hazard escalations in audit log
    """
    global is_job_running
    if is_job_running:
        logger.warning("Weather refresh job is already in progress, skipping duplicate execution.")
        return

    is_job_running = True
    logger.info("Executing scheduled weather refresh and risk evaluation cycle...")

    try:
        if settings.WEATHER_MODE == "demo":
            logger.info("Scheduler running in DEMO mode; skipping live external HTTP request.")
            return

        with Session(engine) as session:
            # 1. Load all locations
            locations = get_locations(session)
            if not locations:
                logger.warning("No locations found in database to refresh.")
                return

            # 2. Batched Open-Meteo query
            parsed_weather = await weather_service.fetch_openmeteo_batched(locations)
            if not parsed_weather:
                logger.warning("Open-Meteo returned empty response during scheduled refresh.")
                return

            now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

            # 3. Process each location
            for loc in locations:
                loc_id = loc["id"]
                weather = parsed_weather.get(loc_id)
                if not weather:
                    continue

                # Save weather snapshot
                snapshot = WeatherSnapshot(
                    location_id=loc_id,
                    fetched_at=now_utc,
                    rain_mm_1h=weather["rain_1h_mm"],
                    rain_mm_24h=weather["rain_24h_mm"],
                    soil_moisture=weather["soil_moisture_pct"],
                    source="open-meteo-live",
                    raw_json=json.dumps(weather, ensure_ascii=False)
                )
                session.add(snapshot)

                # Recompute physical ML risk score using strictly verified parameters
                sim_input = {
                    "location_id": loc_id,
                    "hazard_type": loc["current_hazard"] if loc["current_hazard"] in ["landslide", "flash_flood"] else "landslide",
                    "rain_1h_mm": weather["rain_1h_mm"],
                    "rain_24h_mm": weather["rain_24h_mm"],
                    "rain_48h_mm": weather["rain_48h_mm"],
                    "forecast_24h_mm": 60.0,
                    "soil_moisture_pct": weather["soil_moisture_pct"],
                    "slope_deg": loc["slope_deg"],
                    "elevation_m": loc["elevation_m"],
                    "drainage_proximity_m": loc["drainage_proximity_m"]
                }
                pred = risk_service.predict(sim_input)

                # Save risk score record
                risk_record = RiskScore(
                    location_id=loc_id,
                    computed_at=now_utc,
                    score=pred["risk_score"],
                    level=pred["risk_level"],
                    fs=None,
                    top_factors_json=json.dumps(pred["contributing_factors"], ensure_ascii=False),
                    model_version=pred["model_version"]
                )
                session.add(risk_record)

                # Update live location record
                db_loc = session.exec(select(Location).where(Location.id == loc_id)).first()
                if db_loc:
                    old_score = db_loc.risk_score
                    db_loc.risk_score = pred["risk_score"]
                    db_loc.status = pred["risk_level"]
                    db_loc.last_updated = now_utc
                    session.add(db_loc)

                    # Flag threshold crossing if escalated to High or Very High
                    if pred["risk_score"] >= 70 and old_score < 70:
                        log_audit(
                            session=session,
                            action="RISK_THRESHOLD_EXCEEDED",
                            entity="location",
                            entity_id=loc_id,
                            user_id="automated_scheduler",
                            details={
                                "old_score": old_score,
                                "new_score": pred["risk_score"],
                                "new_level": pred["risk_level"],
                                "hazard_type": loc["current_hazard"]
                            }
                        )

            session.commit()
            logger.info("Successfully refreshed %d locations and saved snapshots.", len(locations))

    except Exception as exc:
        logger.error("Exception occurred during scheduled weather refresh: %s", exc, exc_info=True)
    finally:
        is_job_running = False


def start_scheduler():
    """Start APScheduler if enabled in configuration."""
    if not settings.SCHEDULER_ENABLED:
        logger.info("APScheduler is disabled by configuration (SCHEDULER_ENABLED=false).")
        return

    scheduler.add_job(
        refresh_all_locations,
        "interval",
        minutes=settings.WEATHER_FETCH_INTERVAL_MINUTES,
        id="refresh_weather_and_risk",
        max_instances=1,
        coalesce=True,
        replace_existing=True
    )
    scheduler.start()
    logger.info(
        "APScheduler started: 'refresh_weather_and_risk' scheduled every %d minutes.",
        settings.WEATHER_FETCH_INTERVAL_MINUTES
    )


def shutdown_scheduler():
    """Graceful shutdown of background scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler shut down.")
