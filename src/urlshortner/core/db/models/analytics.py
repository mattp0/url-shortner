from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from urlshortner.core.db.base import Base, UuidPK


class ClickEvent(Base):
    __tablename__ = "click_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    link_id: Mapped[UuidPK] = mapped_column(ForeignKey("links.id", ondelete="CASCADE"), nullable=False)
    link: Mapped["Link"] = relationship(back_populates="clicks")

    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_hash: Mapped[str | None] = mapped_column(String(64))       # store hashes only (privacy)
    ua_hash: Mapped[str | None] = mapped_column(String(64))
    referer_domain: Mapped[str | None] = mapped_column(String(255))
    country_code: Mapped[str | None] = mapped_column(String(2))
    http_status: Mapped[int | None] = mapped_column(SmallInteger)  # e.g., 301/302 outcome

    __table_args__ = (
        Index("ix_clicks_link_id_ts", link_id, ts.desc()),
    )


class LinkStatsDaily(Base):
    __tablename__ = "link_stats_daily"

    link_id: Mapped[UuidPK] = mapped_column(ForeignKey("links.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    clicks: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    unique_ips: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    link: Mapped["Link"] = relationship(back_populates="stats_daily")

    __table_args__ = (
        Index("ix_stats_link_date", link_id, date),
    )
