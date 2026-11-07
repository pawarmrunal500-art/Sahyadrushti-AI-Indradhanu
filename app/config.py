"""
app/config.py - Application configuration via environment variables.

Uses pydantic-settings to load from .env file and environment.
All secrets (JWT_SECRET, DB URL, API keys) come from here.
"""
import os
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
        cors_origins = os.getenv("CORS_ORIGINS", "*")
        if cors_origins == "*":
            self.CORS_ORIGINS: List[str] = ["*"]
        else:
            self.CORS_ORIGINS = [o.strip() for o in cors_origins.split(",")]

        # JWT / Auth (Phase 3)
        self.JWT_SECRET: Optional[str] = os.getenv("JWT_SECRET", None)
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_MINUTES", "30")
        )
        self.JWT_REFRESH_TOKEN_DAYS: int = int(
            os.getenv("JWT_REFRESH_TOKEN_DAYS", "7")
        )

        # Weather / Open-Meteo
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

        # Pilot region default coordinates
        self.PILOT_LAT: float = float(os.getenv("PILOT_LAT", "18.755"))
        self.PILOT_LON: float = float(os.getenv("PILOT_LON", "73.395"))

        # Rate limiting
        self.RATE_LIMIT_LOGIN: str = os.getenv("RATE_LIMIT_LOGIN", "5/minute")
        self.RATE_LIMIT_PUBLIC_POST: str = os.getenv(
            "RATE_LIMIT_PUBLIC_POST", "10/minute"
        )
        self.RATE_LIMIT_PREDICT: str = os.getenv(
            "RATE_LIMIT_PREDICT", "30/minute"
        )


# Global singleton - import this everywhere
settings = Settings()

