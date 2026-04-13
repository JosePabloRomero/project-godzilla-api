"""REST endpoints for service records."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ServiceRecord, Vehicle
from app.schemas import ServiceRecordCreate, ServiceRecordOut, ServiceRecordUpdate

router = APIRouter(prefix="/service-records", tags=["service-records"])


@router.post("", response_model=ServiceRecordOut, status_code=201)
async def create_service_record(
    record: ServiceRecordCreate, response: Response, db: Session = Depends(get_db)
):
    """Create a service record. 404 if vehicle_id does not exist. Returns 201 with Location header."""
    if db.get(Vehicle, record.vehicle_id) is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    obj = ServiceRecord(**record.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    response.headers["Location"] = f"/api/v1/service-records/{obj.id}"
    return obj


@router.get("", response_model=list[ServiceRecordOut])
async def list_service_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    vehicle_id: UUID | None = Query(None, description="Filter by vehicle"),
    db: Session = Depends(get_db),
):
    """List service records. Optional filter by vehicle_id."""
    stmt = select(ServiceRecord)
    if vehicle_id is not None:
        stmt = stmt.where(ServiceRecord.vehicle_id == vehicle_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{record_id}", response_model=ServiceRecordOut)
async def get_service_record(record_id: UUID, db: Session = Depends(get_db)):
    """Get a service record by id. 404 if not found."""
    obj = db.get(ServiceRecord, record_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Service record not found")
    return obj


@router.patch("/{record_id}", response_model=ServiceRecordOut)
async def update_service_record(
    record_id: UUID, payload: ServiceRecordUpdate, db: Session = Depends(get_db)
):
    """Partial update. 404 if not found. If vehicle_id is updated, it must exist."""
    obj = db.get(ServiceRecord, record_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Service record not found")
    patch_data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in patch_data and db.get(Vehicle, patch_data["vehicle_id"]) is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in patch_data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{record_id}", status_code=204)
async def delete_service_record(record_id: UUID, db: Session = Depends(get_db)):
    """Delete a service record. 404 if not found."""
    obj = db.get(ServiceRecord, record_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Service record not found")
    db.delete(obj)
    db.commit()
    return None
