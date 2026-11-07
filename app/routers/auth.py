"""
app/routers/auth.py - Authentication Endpoints.

Endpoints:
  - POST /api/auth/login (rate-limited, anti-timing enumeration, lockout)
  - POST /api/auth/refresh (token rotation)
  - POST /api/auth/logout (token revocation)
  - GET  /api/auth/me (current user identity)
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from sqlmodel import Session, select
import datetime

from app.config import settings
from app.db import get_session
from app.models import User, RefreshToken
from app.repositories import log_audit
from app.limiter import limiter
from app.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_token,
    get_current_user,
    get_current_user_optional,
    DUMMY_HASH,
    pwd_context
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None

# Track failed attempts per (username, client_ip) to prevent distributed denial-of-service/lockout of legitimate users
ip_user_lockout_tracker: Dict[Any, Dict[str, Any]] = {}

@router.post("/login")
@limiter.limit(settings.RATE_LIMIT_LOGIN)
def login(payload: LoginRequest, request: Request, session: Session = Depends(get_session)):
    """Authenticate user, return JWT access token and rotating refresh token."""
    now = datetime.datetime.now(datetime.timezone.utc)
    client_ip = request.client.host if request.client else "127.0.0.1"
    tracker_key = (payload.username, client_ip)

    # 1. Check IP + Username scoped lockout
    tracker = ip_user_lockout_tracker.get(tracker_key)
    if tracker and tracker.get("locked_until"):
        lock_time = tracker["locked_until"]
        if now < lock_time:
            minutes_left = int((lock_time - now).total_seconds() / 60) + 1
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account temporarily locked due to multiple failed logins. Try again in {minutes_left} minutes."
            )
        else:
            ip_user_lockout_tracker.pop(tracker_key, None)

    user = session.exec(select(User).where(User.username == payload.username)).first()

    # Constant-time dummy verification if user does not exist (anti-enumeration)
    if not user:
        pwd_context.verify(payload.password, DUMMY_HASH)
        # Increment failure tracker for this IP probe
        if tracker_key not in ip_user_lockout_tracker:
            ip_user_lockout_tracker[tracker_key] = {"attempts": 0, "locked_until": None}
        ip_user_lockout_tracker[tracker_key]["attempts"] += 1
        if ip_user_lockout_tracker[tracker_key]["attempts"] >= 5:
            ip_user_lockout_tracker[tracker_key]["locked_until"] = now + datetime.timedelta(minutes=15)

        log_audit(
            session=session,
            action="LOGIN_FAILED",
            entity="user",
            entity_id=payload.username,
            details={"reason": "User not found", "client_ip": client_ip}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check password
    if not verify_password(payload.password, user.password_hash):
        if tracker_key not in ip_user_lockout_tracker:
            ip_user_lockout_tracker[tracker_key] = {"attempts": 0, "locked_until": None}
        ip_user_lockout_tracker[tracker_key]["attempts"] += 1
        attempts = ip_user_lockout_tracker[tracker_key]["attempts"]

        if attempts >= 5:
            lock_until = now + datetime.timedelta(minutes=15)
            ip_user_lockout_tracker[tracker_key]["locked_until"] = lock_until
            user.locked_until = lock_until.isoformat()
            log_audit(
                session=session,
                action="ACCOUNT_LOCKED",
                entity="user",
                entity_id=str(user.id),
                user_id=str(user.id),
                details={"reason": "5 consecutive failed logins", "client_ip": client_ip}
            )
        user.failed_login_attempts += 1
        session.add(user)
        session.commit()

        log_audit(
            session=session,
            action="LOGIN_FAILED",
            entity="user",
            entity_id=str(user.id),
            user_id=str(user.id),
            details={"attempts": attempts, "client_ip": client_ip}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Success: reset failed attempts
    ip_user_lockout_tracker.pop(tracker_key, None)
    user.failed_login_attempts = 0
    user.locked_until = None
    session.add(user)
    session.commit()

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(session, user)

    log_audit(
        session=session,
        action="LOGIN_SUCCESS",
        entity="user",
        entity_id=str(user.id),
        user_id=str(user.id),
        details={"role": user.role}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "expires_in": settings.JWT_ACCESS_TOKEN_MINUTES * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }

@router.post("/refresh")
@limiter.limit(settings.RATE_LIMIT_REFRESH)
def refresh_token(payload: RefreshRequest, request: Request, session: Session = Depends(get_session)):
    """Rotate refresh token: revoke existing token and issue a new pair."""
    t_hash = hash_token(payload.refresh_token)
    statement = (
        select(RefreshToken)
        .where(RefreshToken.token_hash == t_hash)
        .where(RefreshToken.revoked == False)  # noqa: E712
    )
    token_record = session.exec(statement).first()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token."
        )

    # Check expiry
    try:
        exp_time = datetime.datetime.fromisoformat(token_record.expires_at)
        if datetime.datetime.now(datetime.timezone.utc) > exp_time:
            token_record.revoked = True
            session.add(token_record)
            session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired. Please log in again."
            )
    except ValueError:
        pass

    # Revoke current token (rotation)
    token_record.revoked = True
    session.add(token_record)
    session.commit()

    # Load user
    user = session.exec(select(User).where(User.id == token_record.user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive or deleted."
        )

    new_access = create_access_token(user)
    new_refresh = create_refresh_token(session, user)

    log_audit(
        session=session,
        action="REFRESH_TOKEN",
        entity="user",
        entity_id=str(user.id),
        user_id=str(user.id)
    )

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_MINUTES * 60
    }

@router.post("/logout")
def logout(
    payload: Optional[LogoutRequest] = None,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Revoke refresh token and log user out."""
    if payload and payload.refresh_token:
        t_hash = hash_token(payload.refresh_token)
        statement = select(RefreshToken).where(RefreshToken.token_hash == t_hash)
        db_token = session.exec(statement).first()
        if db_token:
            db_token.revoked = True
            session.add(db_token)
            session.commit()

    user_id = str(current_user.id) if current_user else "anonymous"
    log_audit(
        session=session,
        action="LOGOUT",
        entity="user",
        entity_id=user_id,
        user_id=user_id
    )

    return {"message": "Logged out successfully."}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Return currently authenticated user profile."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active
    }
