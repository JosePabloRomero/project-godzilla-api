"""REST endpoints for service records."""

from uuid import uuid4, UUID

from fastapi import APIRouter, Query, Response

from app.schemas import ServiceRecordCreate, ServiceRecordOut, ServiceRecordUpdate
from app.storage.memory import (
    get_service_record_or_404,
    service_records_store,
    vehicle_exists,
    apply_patch,
    utc_now,
)

router = APIRouter(prefix="/service-records", tags=["service-records"])


@router.post("", response_model=ServiceRecordOut, status_code=201)
async def create_service_record(record: ServiceRecordCreate, response: Response):
    """Create a service record. 404 if vehicle_id does not exist. Returns 201 with Location header."""
    if not vehicle_exists(record.vehicle_id):
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Vehicle not found")
    now = utc_now()
    id_ = uuid4()
    out = ServiceRecordOut(
        id=id_,
        created_at=now,
        **record.model_dump(),
    )
    service_records_store[id_] = out
    response.headers["Location"] = f"/api/v1/service-records/{out.id}"
    return out


@router.get("", response_model=list[ServiceRecordOut])
async def list_service_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    vehicle_id: UUID | None = Query(None, description="Filter by vehicle"),
):
    """List service records. Optional filter by vehicle_id."""
    items = list(service_records_store.values())
    if vehicle_id is not None:
        items = [sr for sr in items if sr.vehicle_id == vehicle_id]
    return items[skip : skip + limit]


@router.get("/{record_id}", response_model=ServiceRecordOut)
async def get_service_record(record_id: str):
    """Get a service record by id. 404 if not found."""
    uid = UUID(record_id)
    return get_service_record_or_404(uid)


@router.patch("/{record_id}", response_model=ServiceRecordOut)
async def update_service_record(record_id: str, payload: ServiceRecordUpdate):
    """Partial update. 404 if not found. If vehicle_id is updated, it must exist."""
    uid = UUID(record_id)
    existing = get_service_record_or_404(uid)
    patch_data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in patch_data and not vehicle_exists(patch_data["vehicle_id"]):
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Vehicle not found")
    updated = apply_patch(existing, patch_data)
    service_records_store[uid] = updated
    return updated


@router.delete("/{record_id}", status_code=204)
async def delete_service_record(record_id: str):
    """Delete a service record. 404 if not found."""
    uid = UUID(record_id)
    get_service_record_or_404(uid)
    del service_records_store[uid]
    return None
