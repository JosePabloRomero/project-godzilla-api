"""In-memory stores and helpers for vehicles, mods, and service records."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, TypeVar
from uuid import UUID

from fastapi import HTTPException

from app.schemas import ModOut, ServiceRecordOut, VehicleOut

# Stores: id -> Out model
vehicles_store: dict[UUID, VehicleOut] = {}
mods_store: dict[UUID, ModOut] = {}
service_records_store: dict[UUID, ServiceRecordOut] = {}


def get_vehicle_or_404(vehicle_id: UUID) -> VehicleOut:
    """Return vehicle or raise 404."""
    if vehicle_id not in vehicles_store:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicles_store[vehicle_id]


def get_mod_or_404(mod_id: UUID) -> ModOut:
    """Return mod or raise 404."""
    if mod_id not in mods_store:
        raise HTTPException(status_code=404, detail="Mod not found")
    return mods_store[mod_id]


def get_service_record_or_404(record_id: UUID) -> ServiceRecordOut:
    """Return service record or raise 404."""
    if record_id not in service_records_store:
        raise HTTPException(status_code=404, detail="Service record not found")
    return service_records_store[record_id]


def vehicle_exists(vehicle_id: UUID) -> bool:
    """Check if a vehicle exists (for referential integrity)."""
    return vehicle_id in vehicles_store


T = TypeVar("T")


def apply_patch(existing: T, update: Any) -> T:
    """
    Apply only set fields from an Update model to an Out model.
    update should have model_dump(exclude_unset=True).
    """
    if not update:
        return existing
    data = existing.model_dump()
    data.update(update)
    return type(existing)(**data)


def cascade_delete_vehicle(vehicle_id: UUID) -> None:
    """
    Delete a vehicle and all mods and service records associated with it.
    Caller must ensure vehicle exists (or handle 404 separately).
    """
    # Remove mods for this vehicle
    to_remove_mods = [
        mid for mid, m in mods_store.items() if m.vehicle_id == vehicle_id
    ]
    for mid in to_remove_mods:
        del mods_store[mid]
    # Remove service records for this vehicle
    to_remove_sr = [
        rid for rid, sr in service_records_store.items() if sr.vehicle_id == vehicle_id
    ]
    for rid in to_remove_sr:
        del service_records_store[rid]
    # Remove vehicle
    del vehicles_store[vehicle_id]


def utc_now() -> datetime:
    """Current UTC time for created_at."""
    return datetime.now(timezone.utc)
