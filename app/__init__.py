"""
app/ - SAHYADRUSHTI AI Backend Application Package

This package provides the restructured modular backend for the
SAHYADRUSHTI AI hyperlocal landslide and flash-flood risk platform.

The original monolithic backend/main.py remains as the entry point
for backward compatibility. This package organises the code into:
  - app/config.py        : Environment-based configuration (pydantic-settings)
  - app/schemas.py       : Re-exports from backend/schemas.py (API contract)
  - app/db.py            : Database engine, session management (Phase 1)
  - app/models.py        : SQLModel/SQLAlchemy ORM models (Phase 1)
  - app/repositories.py  : Data access layer functions (Phase 1)
  - app/auth.py          : JWT authentication & RBAC (Phase 3)
  - app/scheduler.py     : APScheduler weather & risk refresh (Phase 2)
  - app/routers/         : FastAPI APIRouter modules
  - app/services/         : Business logic (weather, risk)
"""

