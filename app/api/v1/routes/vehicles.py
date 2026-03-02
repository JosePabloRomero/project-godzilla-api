"""REST endpoints for vehicles."""

from uuid import uuid4

from fastapi import APIRouter, Query, Response

from app.schemas import VehicleCreate, VehicleOut, VehicleUpdate
from app.storage.memory import (
    get_vehicle_or_404,
    vehicles_store,
    apply_patch,
    cascade_delete_vehicle,
    utc_now,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleOut, status_code=201)
async def create_vehicle(vehicle: VehicleCreate, response: Response):
    """Create a vehicle. Returns 201 with Location header."""
    now = utc_now()
    id_ = uuid4()
    out = VehicleOut(
        id=id_,
        created_at=now,
        **vehicle.model_dump(),
    )
    vehicles_store[id_] = out
    response.headers["Location"] = f"/api/v1/vehicles/{out.id}"
    return out


@router.get("", response_model=list[VehicleOut])
async def list_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """List vehicles with pagination (skip/limit)."""
    items = list(vehicles_store.values())
    return items[skip : skip + limit]


@router.get("/{vehicle_id}", response_model=VehicleOut)
async def get_vehicle(vehicle_id: str):
    """Get a vehicle by id. 404 if not found."""
    from uuid import UUID

    uid = UUID(vehicle_id)
    return get_vehicle_or_404(uid)


@router.patch("/{vehicle_id}", response_model=VehicleOut)
async def update_vehicle(vehicle_id: str, payload: VehicleUpdate):
    """Partial update. 404 if not found."""
    from uuid import UUID

    uid = UUID(vehicle_id)
    existing = get_vehicle_or_404(uid)
    updated = apply_patch(existing, payload.model_dump(exclude_unset=True))
    vehicles_store[uid] = updated
    return updated


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id: str):
    """Delete vehicle and cascade to mods and service records. 404 if not found."""
    from uuid import UUID

    uid = UUID(vehicle_id)
    get_vehicle_or_404(uid)  # 404 if missing
    cascade_delete_vehicle(uid)
    return None
