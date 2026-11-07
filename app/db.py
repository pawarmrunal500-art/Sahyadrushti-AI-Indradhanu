"""
app/db.py - Database engine, session management, and SQLite pragmas.

Supports SQLite (default, with WAL mode and foreign keys enabled)
and PostgreSQL (switching via DATABASE_URL without code change).
"""
import os
from typing import Generator
from sqlalchemy import event, Engine
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Normalize postgres:// to postgresql:// if passed by hosting providers
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Determine connect_args based on DB dialect
connect_args = {}
engine_kwargs = {"echo": False}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 300

# Create engine
engine = create_engine(
    db_url,
    connect_args=connect_args,
    **engine_kwargs
)

# SQLite pragmas: enforce WAL mode and foreign key constraints on every connection
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def init_db(target_engine=None):
    """Create all tables defined in SQLModel metadata."""
    eng = target_engine or engine
    SQLModel.metadata.create_all(eng)

def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""
    with Session(engine) as session:
        yield session
