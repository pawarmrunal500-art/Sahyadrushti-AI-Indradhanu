"""
app/config.py - Application configuration via environment variables.

Uses pydantic-settings / environment variable loader.
All secrets (JWT_SECRET, DB URL, API keys) come from here.
"""
import os
import sys
from typing import List, Optional


class Settings:
    """
    Application settings loaded from environment variables.
    Falls back to sensible development defaults.

    In production, all values should be set via .env or environment.
    """

    def __init__(self):
        self.APP_NAME: str = os.getenv("APP_NAME", "SAHYADRUSHTI AI")
        self.APP_VERSION: str = os.getenv("APP_VERSION", "2.1.0")
        self.DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

        # Database
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./sahyadrushti.db"
        )

        # CORS
        cors_origins = os.getenv("CORS_ORIGINS", "")
        if cors_origins:
            self.CORS_ORIGINS: List[str] = [o.strip() for o in cors_origins.split(",") if o.strip()]
        else:
            self.CORS_ORIGINS = ["*"] if self.DEBUG else ["http://localhost:5173", "http://127.0.0.1:5173"]

        # JWT / Auth (Phase 3)
        self.JWT_SECRET: str = os.getenv("JWT_SECRET", "sahyadrushti_dev_jwt_secret_key_minimum_32_bytes_long_12345")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_MINUTES", "30")
        )
        self.JWT_REFRESH_TOKEN_DAYS: int = int(
            os.getenv("JWT_REFRESH_TOKEN_DAYS", "7")
        )

        # Validate JWT_SECRET in production mode
        if not self.DEBUG:
            if not self.JWT_SECRET or len(self.JWT_SECRET) < 32 or "CHANGE_THIS" in self.JWT_SECRET or "dev" in self.JWT_SECRET.lower():
                raise RuntimeError(
                    "FATAL: In production mode (DEBUG=False), JWT_SECRET must be set to a secure string with at least 32 characters."
                )

        # Weather / Open-Meteo
        self.WEATHER_MODE: str = os.getenv("WEATHER_MODE", "live").lower()  # "live" or "demo"
        self.OPENMETEO_FORECAST_URL: str = os.getenv(
            "OPENMETEO_FORECAST_URL",
            "https://api.open-meteo.com/v1/forecast"
        )
        self.OPENMETEO_ARCHIVE_URL: str = os.getenv(
            "OPENMETEO_ARCHIVE_URL",
            "https://archive-api.open-meteo.com/v1/archive"
        )
        self.WEATHER_FETCH_INTERVAL_MINUTES: int = int(
            os.getenv("WEATHER_FETCH_INTERVAL_MINUTES", "30")
        )
        self.WEATHER_CACHE_TTL_MINUTES: int = int(
            os.getenv("WEATHER_CACHE_TTL_MINUTES", "15")
        )
        # Antecedent Precipitation Index daily decay factor (0.85-0.9 typical)
        self.API_DECAY_FACTOR: float = float(
            os.getenv("API_DECAY_FACTOR", "0.88")
        )
        # Bias-correction multiplier for raw precipitation (default 1.0; suspected underestimate in steep ghats)
        self.BIAS_MULTIPLIER: float = float(
            os.getenv("BIAS_MULTIPLIER", "1.0")
        )
        # Timezone
        self.TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")

        # Scheduler
        self.SCHEDULER_ENABLED: bool = os.getenv("SCHEDULER_ENABLED", "true").lower() in ("true", "1", "yes")

        # Pilot region default coordinates
        self.PILOT_LAT: float = float(os.getenv("PILOT_LAT", "18.755"))
        self.PILOT_LON: float = float(os.getenv("PILOT_LON", "73.395"))

        # Demo Mode (higher limits for hackathon / evaluation presentations)
        self.DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")

        # Rate limiting (configurable with defaults; shared NAT/venue WiFi counts as single IP)
        self.RATELIMIT_ENABLED: bool = os.getenv("RATELIMIT_ENABLED", "true").lower() in ("true", "1", "yes")
        self.RATE_LIMIT_LOGIN: str = os.getenv("RATE_LIMIT_LOGIN", "5/minute")
        self.RATE_LIMIT_REFRESH: str = os.getenv("RATE_LIMIT_REFRESH", "10/minute")
        self.RATE_LIMIT_PUBLIC_POST: str = os.getenv("RATE_LIMIT_PUBLIC_POST", "10/minute")
        if self.DEMO_MODE:
            self.RATE_LIMIT_PREDICT: str = os.getenv("RATE_LIMIT_PREDICT_DEMO", "120/minute")
            self.RATE_LIMIT_SIMULATE: str = os.getenv("RATE_LIMIT_SIMULATE_DEMO", "100/minute")
        else:
            self.RATE_LIMIT_PREDICT: str = os.getenv("RATE_LIMIT_PREDICT", "30/minute")
            self.RATE_LIMIT_SIMULATE: str = os.getenv("RATE_LIMIT_SIMULATE", "20/minute")


# Global singleton - import this everywhere
settings = Settings()
