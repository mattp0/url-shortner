# scripts/seed_admin.py
"""
Seed or update an admin user.

Usage:
  uv run python scripts/seed_admin.py you@example.com 'StrongPass123!' [--role admin|editor] [--env-file .env]

Reads DATABASE_URL from:
  1) --env-file if provided, else
  2) nearest .env discovered via python-dotenv (project root), else
  3) current process environment
"""
from __future__ import annotations

import argparse
import asyncio
import os
from typing import Optional

from passlib.hash import bcrypt
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# --- dotenv support ---
try:
    from dotenv import load_dotenv, find_dotenv
except Exception as e:  # pragma: no cover
    raise SystemExit("python-dotenv not installed. Run: uv add python-dotenv") from e

from urlshortner.core.db.models import User, UserRole


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("email")
    p.add_argument("password")
    p.add_argument("--role", choices=[r.value for r in UserRole], default=UserRole.admin.value)
    p.add_argument("--env-file", help="Path to a .env file to load", default=None)
    p.add_argument("--override", action="store_true", help="Override already-set env vars when loading .env")
    return p.parse_args()


def load_env(env_file: Optional[str], override: bool) -> str:
    if env_file:
        if not load_dotenv(env_file, override=override):
            raise SystemExit(f"Could not load env file: {env_file}")
        used = env_file
    else:
        # find the nearest .env (walks up from CWD)
        used = find_dotenv(usecwd=True)
        if used:
            load_dotenv(used, override=override)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        where = used or "process environment"
        raise SystemExit(f"DATABASE_URL not found (checked {where}).")
    return db_url


async def main() -> None:
    args = parse_args()
    db_url = load_env(args.env_file, args.override)

    engine = create_async_engine(db_url, pool_pre_ping=True)
    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    email_lc = args.email.strip().lower()
    pwd_hash = bcrypt.hash(args.password)
    role = UserRole(args.role)

    # Connectivity check
    async with engine.begin():
        pass

    # Upsert by lower(email)
    async with Session.begin() as session:
        existing = await session.scalar(select(User).where(func.lower(User.email) == email_lc))
        if existing:
            await session.execute(
                update(User)
                .where(User.id == existing.id)
                .values(password_hash=pwd_hash, role=role)
            )
            action = "updated"
        else:
            session.add(User(email=email_lc, password_hash=pwd_hash, role=role))
            action = "created"

    await engine.dispose()
    print(f"Admin user {action}: {email_lc} (role={role.value})")


if __name__ == "__main__":
    asyncio.run(main())
