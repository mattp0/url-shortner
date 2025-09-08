from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as PgEnum, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urlshortner.core.db.base import Base, UuidPK


class UserRole(str, Enum):
    admin = "admin"
    editor = "editor"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UuidPK]
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(PgEnum(UserRole, name="user_role"), nullable=False, default=UserRole.editor)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    links: Mapped[list["Link"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

    # Uniqueness is case-insensitive on email
    __table_args__ = (
        Index("uq_users_email_lower", func.lower(email), unique=True),
    )
