from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, SmallInteger, String, Text, func
from sqlalchemy import Enum as PgEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urlshortner.core.db.base import Base, UuidPK
from urlshortner.core.db.models import ClickEvent, LinkStatsDaily, User


class SafetyStatus(str, Enum):
    pending = "pending"
    safe = "safe"
    blocked = "blocked"
    suspicious = "suspicious"


class Link(Base):
    __tablename__ = "links"

    id: Mapped[UuidPK]
    # Global, case-insensitive uniqueness for slugs
    slug: Mapped[str] = mapped_column(String(64), nullable=False)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)

    owner_id: Mapped[UuidPK] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped[User] = relationship(back_populates="links")

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    redirect_type: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=301)  # 301 or 302

    safety_status: Mapped[SafetyStatus] = mapped_column(
        PgEnum(SafetyStatus, name="safety_status"), nullable=False, default=SafetyStatus.pending
    )
    safety_tags: Mapped[list[str] | None] = mapped_column(JSONB, default=list)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    clicks: Mapped[list[ClickEvent]] = relationship(back_populates="link", cascade="all, delete-orphan")
    stats_daily: Mapped[list[LinkStatsDaily]] = relationship(back_populates="link", cascade="all, delete-orphan")

    __table_args__ = (
        # Enforce allowed characters/length at the DB level
        CheckConstraint("slug ~ '^[A-Za-z0-9_-]{1,32}$'", name="slug_pattern"),
        # Case-insensitive unique slug
        Index("uq_links_slug_lower", func.lower(slug), unique=True),
        # Useful lookup indexes
        Index("ix_links_owner_id", owner_id),
        Index("ix_links_status", safety_status),
        Index("ix_links_created_at", created_at),
    )
