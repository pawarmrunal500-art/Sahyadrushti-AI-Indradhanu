"""
app/cli.py - Command-Line Interface for Administrative and Provisioning Tasks.

Commands:
  - python -m app.cli create-user --username <name> --role <operator|approver|admin> [--password <pass>]
  - python -m app.cli create-admin [--username <name>] [--password <pass>]
  - python -m app.cli create-device-key --node-id <id>
"""
import argparse
import getpass
import os
import sys
import secrets
from sqlmodel import Session, select

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import engine, init_db
from app.models import User, SensorNodeDB
from app.auth import hash_password, hash_token
from app.repositories import log_audit, seed_all_if_empty

def cmd_create_user(args):
    """Create a user with an assigned role and Argon2-hashed password."""
    init_db()
    username = args.username.strip()
    role = args.role.strip().lower()

    if role not in ("operator", "approver", "admin"):
        print(f"Error: Invalid role '{role}'. Must be one of: operator, approver, admin.")
        sys.exit(1)

    password = args.password
    if not password:
        password = os.getenv("SAHYADRUSHTI_USER_PASSWORD")
    if not password:
        password = getpass.getpass(f"Enter password for user '{username}' (min 8 chars): ")
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("Error: Passwords do not match.")
            sys.exit(1)

    if len(password) < 8:
        print("Error: Password must be at least 8 characters long.")
        sys.exit(1)

    with Session(engine) as session:
        # Check if user already exists
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print(f"Error: User '{username}' already exists.")
            sys.exit(1)

        p_hash = hash_password(password)
        new_user = User(
            username=username,
            password_hash=p_hash,
            role=role,
            is_active=True
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        log_audit(
            session=session,
            action="CREATE_USER_CLI",
            entity="user",
            entity_id=str(new_user.id),
            details={"username": username, "role": role}
        )

        print(f"[SUCCESS] User '{username}' created successfully with role '{role}' (ID: {new_user.id}).")


def cmd_create_admin(args):
    """Convenience helper to create an administrator account."""
    args.role = "admin"
    if not getattr(args, "username", None):
        args.username = input("Enter admin username [default: admin]: ").strip() or "admin"
    cmd_create_user(args)


def cmd_create_device_key(args):
    """Generate high-entropy per-device API key for sensor edge ingestion."""
    init_db()
    node_id = args.node_id.strip()

    with Session(engine) as session:
        seed_all_if_empty(session)
        node = session.exec(select(SensorNodeDB).where(SensorNodeDB.sensor_id == node_id)).first()
        if not node:
            print(f"Error: Sensor node '{node_id}' not found in database.")
            sys.exit(1)

        # Generate high-entropy API key
        raw_key = f"sahyadri_node_{secrets.token_urlsafe(32)}"
        key_hash = hash_token(raw_key)

        node.api_key_hash = key_hash
        session.add(node)
        session.commit()

        log_audit(
            session=session,
            action="CREATE_DEVICE_KEY",
            entity="sensor",
            entity_id=node_id,
            details={"node_id": node_id}
        )

        print("=" * 65)
        print(f"[SUCCESS] High-Entropy Device Key generated for node: {node_id}")
        print(f"X-Device-Key: {raw_key}")
        print("=" * 65)
        print("WARNING: This key is displayed only ONCE and stored as SHA-256 hash in DB.")
        print("Set this key in your IoT edge station's 'X-Device-Key' HTTP header.")
        print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="SAHYADRUSHTI AI Command-Line Interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create-user
    parser_user = subparsers.add_parser("create-user", help="Create a user with operator, approver, or admin role")
    parser_user.add_argument("--username", required=True, help="Username")
    parser_user.add_argument("--role", required=True, choices=["operator", "approver", "admin"], help="User role")
    parser_user.add_argument("--password", help="Plaintext password (optional, prompted if omitted)")
    parser_user.set_defaults(func=cmd_create_user)

    # create-admin
    parser_admin = subparsers.add_parser("create-admin", help="Create an administrator account")
    parser_admin.add_argument("--username", default="admin", help="Admin username")
    parser_admin.add_argument("--password", help="Plaintext password")
    parser_admin.set_defaults(func=cmd_create_admin)

    # create-device-key
    parser_key = subparsers.add_parser("create-device-key", help="Generate a secure device API key for IoT edge ingestion")
    parser_key.add_argument("--node-id", required=True, help="Sensor Node ID (e.g. SENS-LNV-01)")
    parser_key.set_defaults(func=cmd_create_device_key)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
