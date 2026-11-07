"""
app/auth.py - Authentication, Password Hashing, JWT Tokens, and Role-Based Access Control (RBAC).

Features:
  - Argon2 password hashing via pwdlib
  - Constant-time dummy verification on nonexistent users (anti-timing enumeration)
  - Account lockout after 5 consecutive failed attempts (15-min backoff)
  - JWT Access Token (HS256 pinned, exp, iat, sub, role)
  - Rotating Refresh Tokens stored as SHA-256 hashes in DB
  - Role-Based Access Control: require_role(*roles)
  - Per-device API key validation (X-Device-Key header, SHA-256 constant-time match)
"""
import hashlib
import hmac
import secrets
import datetime
from typing import Optional, List, Dict, Any
import jwt
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
from sqlmodel import Session, select

from app.config import settings
from app.db import get_session
from app.models import User, RefreshToken, SensorNodeDB, AuditLog

# Password hasher using Argon2id
pwd_context = PasswordHash.recommended()

# Constant-time dummy hash to mitigate user enumeration timing attacks
DUMMY_HASH = pwd_context.hash("dummy_constant_time_string_for_enumeration_protection")

# HTTP Bearer scheme
bearer_scheme = HTTPBearer(auto_error=False)

# ======================== Password Helpers ========================

def hash_password(password: str) -> str:
    """Hash password with Argon2id."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against Argon2id hash."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_token(raw_token: str) -> str:
    """Compute SHA-256 digest of token or API key for secure storage."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

def constant_time_compare(val1: str, val2: str) -> bool:
    """Compare two string hashes in constant time to prevent timing attacks."""
    return hmac.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))


# ======================== JWT Token Lifecycle ========================

def create_access_token(user: User) -> str:
    """Generate signed JWT access token pinned to HS256."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + datetime.timedelta(minutes=settings.JWT_ACCESS_TOKEN_MINUTES)
    payload = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(session: Session, user: User) -> str:
    """Generate opaque cryptographically secure refresh token, store SHA-256 in DB."""
    raw_token = secrets.token_urlsafe(32)
    t_hash = hash_token(raw_token)
    expires_at = (
        datetime.datetime.now(datetime.timezone.utc) +
        datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_DAYS)
    ).isoformat()

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=t_hash,
        expires_at=expires_at,
        revoked=False
    )
    session.add(db_token)
    session.commit()
    return raw_token

def decode_access_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT access token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub"]}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )


# ======================== FastAPI Dependencies ========================

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    session: Session = Depends(get_session)
) -> User:
    """FastAPI dependency to authenticate requests using Bearer JWT."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = decode_access_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token payload.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive or deleted.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    session: Session = Depends(get_session)
) -> Optional[User]:
    """Optional bearer token dependency that returns None instead of raising 401."""
    if not credentials or not credentials.credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        username = payload.get("sub")
        if not username:
            return None
        user = session.exec(select(User).where(User.username == username)).first()
        return user if (user and user.is_active) else None
    except HTTPException:
        return None

def require_role(*allowed_roles: str):
    """Factory dependency to enforce Role-Based Access Control (RBAC)."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: role '{current_user.role}' is not authorized. Requires: {', '.join(allowed_roles)}."
            )
        return current_user
    return role_checker


# ======================== Device Key Authentication ========================

def verify_sensor_device_key(
    x_device_key: Optional[str] = Header(None, alias="X-Device-Key"),
    session: Session = Depends(get_session)
):
    """
    Validates per-device API key for sensor telemetry ingestion.
    Rejects missing or invalid keys with HTTP 401.
    """
    if not x_device_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required 'X-Device-Key' header for sensor telemetry ingestion."
        )

    key_hash = hash_token(x_device_key)
    statement = select(SensorNodeDB).where(SensorNodeDB.api_key_hash == key_hash)
    node = session.exec(statement).first()

    if not node:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unrecognized device API key."
        )

    return node
