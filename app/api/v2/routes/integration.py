"""Integration endpoints for multicloud payload relay."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Vehicle
from app.schemas import MultiCloudPayload, VehicleOut

router = APIRouter(prefix="/integration", tags=["integration"])


def _resolve_vehicle(payload: MultiCloudPayload, db: Session) -> Vehicle:
    """Find an existing vehicle or create one from payload/default seed."""
    if payload.vehicle_seed is not None:
        seed = payload.vehicle_seed
        stmt = select(Vehicle).where(
            Vehicle.make == seed.make,
            Vehicle.model == seed.model,
            Vehicle.year == seed.year,
            Vehicle.nickname == seed.nickname,
        )
        existing = db.scalar(stmt)
        if existing is not None:
            return existing

        created = Vehicle(**seed.model_dump())
        db.add(created)
        db.commit()
        db.refresh(created)
        return created

    fallback = db.scalar(select(Vehicle).limit(1))
    if fallback is not None:
        return fallback

    created = Vehicle(
        make="Unknown",
        model="Multicloud Car",
        year=2000,
        nickname="Integration Test Car",
    )
    db.add(created)
    db.commit()
    db.refresh(created)
    return created


@router.post("/multicloud")
async def receive_and_enrich_multicloud_payload(
    payload: MultiCloudPayload, db: Session = Depends(get_db)
):
    """
    Receives payload from API #1 and injects a serialized Vehicle entity.
    """
    vehicle = _resolve_vehicle(payload, db)
    enriched_payload = payload.model_dump(mode="python")
    enriched_payload["vehicle"] = VehicleOut.model_validate(vehicle).model_dump(mode="json")
    return enriched_payload
