from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ServiceRecordBase(BaseModel):
    """Base schema for a vehicle service/maintenance record."""

    vehicle_id: UUID
    service_type: str = Field(
        ..., min_length=1, max_length=40, examples=["oil_change"]
    )
    mileage: int = Field(..., ge=0, le=2_000_000, examples=[120000])
    service_date: date
    notes: Optional[str] = Field(None, max_length=200)


class ServiceRecordCreate(ServiceRecordBase):
    """Payload for service record creation."""
    pass


class ServiceRecordUpdate(BaseModel):
    """
    Payload for updates (PATCH/PUT).
    All fields optional.
    """
    vehicle_id: Optional[UUID] = None
    service_type: Optional[str] = Field(None, min_length=1, max_length=40)
    mileage: Optional[int] = Field(None, ge=0, le=2_000_000)
    service_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=200)


class ServiceRecordOut(ServiceRecordBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
