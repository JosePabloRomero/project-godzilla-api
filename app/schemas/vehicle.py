from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=50, examples=["Nissan"])
    model: str = Field(..., min_length=1, max_length=80, examples=["Skyline GT-R R34"])
    year: int = Field(..., ge=1950, le=2050, examples=[1999])
    nickname: Optional[str] = Field(None, max_length=50, examples=["Godzilla"])

class VehicleCreate(VehicleBase):
    """Payload for vehicle creation"""
    pass

class VehicleUpdate(BaseModel):
    """
    Payload for updates (PATCH/PUT).
    All fields optional.
    """
    make: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=80)
    year: Optional[int] = Field(None, ge=1950, le=2050)
    nickname: Optional[str] = Field(None, max_length=50)

class VehicleOut(VehicleBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)