"""Integration endpoints for multicloud payload relay."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Vehicle
from app.schemas import MultiCloudPayload, VehicleOut

router = APIRouter(prefix="/integration", tags=["integration"])


def _resolve_vehicle(payload: MultiCloudPayload, db: Session) -> Vehicle:
    """Resolve vehicle by id, then fallback, then create default."""
    if payload.vehicle_id is not None:
        by_id = db.get(Vehicle, payload.vehicle_id)
        if by_id is not None:
            return by_id

    fallback = db.scalar(select(Vehicle).limit(1))
    if fallback is not None:
        return fallback

    created = Vehicle(
        make="Unknown",
        model="Multicloud",
        year=2000,
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
    vehicle_serialized = VehicleOut.model_validate(vehicle).model_dump(mode="json")
    enriched_payload = {
        "cliente": payload.cliente,
        "podcast": payload.podcast,
        "vehicle": vehicle_serialized,
    }
    if payload.model_extra:
        enriched_payload.update(payload.model_extra)
    return enriched_payload
