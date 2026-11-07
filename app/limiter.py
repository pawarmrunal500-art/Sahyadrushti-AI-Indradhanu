"""
app/limiter.py - Rate limiting setup using slowapi.

Protects sensitive endpoints:
  - POST /api/auth/login
  - POST /api/incidents
  - POST /api/predict
  - POST /api/simulate

Note on Reverse Proxies:
  In production behind Nginx/Caddy/Cloudflare, ensure X-Forwarded-For headers
  are trusted and forwarded properly to identify true client IPs.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.RATELIMIT_ENABLED
)

