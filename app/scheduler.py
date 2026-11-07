"""
app/scheduler.py - Background job scheduler.

Phase 2 will implement:
  - APScheduler AsyncIOScheduler started in FastAPI lifespan
  - refresh_all_locations job (fetch weather -> save snapshots ->
    run ml_engine -> save risk_scores -> flag threshold crossings)
  - Configurable interval (default 30 min)
  - Duplicate job guard for single-worker deployment

Currently a placeholder.
"""

SCHEDULER_PLACEHOLDER = True  # Replaced in Phase 2

