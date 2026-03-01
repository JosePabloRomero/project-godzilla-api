from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModBase(BaseModel):
    """Base schema for a vehicle modification."""

    vehicle_id: UUID
    name: str = Field(..., min_length=1, max_length=80, examples=["Racing Coilovers"])
    category: str = Field(..., max_length=30, examples=["suspension"])
    installed_at: date
    notes: Optional[str] = Field(None, max_length=200)


class ModCreate(ModBase):
    """Payload for mod creation."""
    pass


class ModUpdate(BaseModel):
    """
    Payload for updates (PATCH/PUT).
    All fields optional.
    """
    vehicle_id: Optional[UUID] = None
    name: Optional[str] = Field(None, min_length=1, max_length=80)
    category: Optional[str] = Field(None, max_length=30)
    installed_at: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=200)


class ModOut(ModBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
