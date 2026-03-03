"""ORM model for Vehicle."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.mod import Mod
    from app.models.service_record import ServiceRecord


class Vehicle(Base):
    """Vehicle table (vehicles)."""

    __tablename__ = "vehicles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    mods: Mapped[List["Mod"]] = relationship(
        "Mod",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )
    service_records: Mapped[List["ServiceRecord"]] = relationship(
        "ServiceRecord",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )
