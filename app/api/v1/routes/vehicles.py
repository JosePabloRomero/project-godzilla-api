"""REST endpoints for vehicles."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Mod, ServiceRecord, Vehicle
from app.schemas import VehicleCreate, VehicleOut, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleOut, status_code=201)
async def create_vehicle(
    vehicle: VehicleCreate, response: Response, db: Session = Depends(get_db)
):
    """Create a vehicle. Returns 201 with Location header."""
    obj = Vehicle(**vehicle.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    response.headers["Location"] = f"/api/v1/vehicles/{obj.id}"
    return obj


@router.get("", response_model=list[VehicleOut])
async def list_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List vehicles with pagination (skip/limit)."""
    stmt = select(Vehicle).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{vehicle_id}", response_model=VehicleOut)
async def get_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    """Get a vehicle by id. 404 if not found."""
    obj = db.get(Vehicle, vehicle_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return obj


@router.patch("/{vehicle_id}", response_model=VehicleOut)
async def update_vehicle(
    vehicle_id: UUID, payload: VehicleUpdate, db: Session = Depends(get_db)
):
    """Partial update. 404 if not found."""
    obj = db.get(Vehicle, vehicle_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id: UUID, db: Session = Depends(get_db)):
    """Delete vehicle and cascade to mods and service records. 404 if not found."""
    obj = db.get(Vehicle, vehicle_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.execute(delete(Mod).where(Mod.vehicle_id == vehicle_id))
    db.execute(delete(ServiceRecord).where(ServiceRecord.vehicle_id == vehicle_id))
    db.delete(obj)
    db.commit()
    return None
