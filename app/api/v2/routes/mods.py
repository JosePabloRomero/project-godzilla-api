"""REST endpoints for mods."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Mod, Vehicle
from app.schemas import ModCreate, ModOut, ModUpdate

router = APIRouter(prefix="/mods", tags=["mods"])


@router.post("", response_model=ModOut, status_code=201)
async def create_mod(
    mod: ModCreate, response: Response, db: Session = Depends(get_db)
):
    """Create a mod. 404 if vehicle_id does not exist. Returns 201 with Location header."""
    if db.get(Vehicle, mod.vehicle_id) is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    obj = Mod(**mod.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    response.headers["Location"] = f"/api/v1/mods/{obj.id}"
    return obj


@router.get("", response_model=list[ModOut])
async def list_mods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    vehicle_id: UUID | None = Query(None, description="Filter by vehicle"),
    db: Session = Depends(get_db),
):
    """List mods. Optional filter by vehicle_id."""
    stmt = select(Mod)
    if vehicle_id is not None:
        stmt = stmt.where(Mod.vehicle_id == vehicle_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{mod_id}", response_model=ModOut)
async def get_mod(mod_id: UUID, db: Session = Depends(get_db)):
    """Get a mod by id. 404 if not found."""
    obj = db.get(Mod, mod_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    return obj


@router.patch("/{mod_id}", response_model=ModOut)
async def update_mod(
    mod_id: UUID, payload: ModUpdate, db: Session = Depends(get_db)
):
    """Partial update. 404 if not found. If vehicle_id is updated, it must exist."""
    obj = db.get(Mod, mod_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    patch_data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in patch_data and db.get(Vehicle, patch_data["vehicle_id"]) is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in patch_data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{mod_id}", status_code=204)
async def delete_mod(mod_id: UUID, db: Session = Depends(get_db)):
    """Delete a mod. 404 if not found."""
    obj = db.get(Mod, mod_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    db.delete(obj)
    db.commit()
    return None
