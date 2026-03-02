"""REST endpoints for mods."""

from uuid import uuid4, UUID

from fastapi import APIRouter, Query, Response

from app.schemas import ModCreate, ModOut, ModUpdate
from app.storage.memory import (
    get_mod_or_404,
    mods_store,
    vehicle_exists,
    apply_patch,
    utc_now,
)

router = APIRouter(prefix="/mods", tags=["mods"])


@router.post("", response_model=ModOut, status_code=201)
async def create_mod(mod: ModCreate, response: Response):
    """Create a mod. 404 if vehicle_id does not exist. Returns 201 with Location header."""
    if not vehicle_exists(mod.vehicle_id):
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Vehicle not found")
    now = utc_now()
    id_ = uuid4()
    out = ModOut(
        id=id_,
        created_at=now,
        **mod.model_dump(),
    )
    mods_store[id_] = out
    response.headers["Location"] = f"/api/v1/mods/{out.id}"
    return out


@router.get("", response_model=list[ModOut])
async def list_mods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    vehicle_id: UUID | None = Query(None, description="Filter by vehicle"),
):
    """List mods. Optional filter by vehicle_id."""
    items = list(mods_store.values())
    if vehicle_id is not None:
        items = [m for m in items if m.vehicle_id == vehicle_id]
    return items[skip : skip + limit]


@router.get("/{mod_id}", response_model=ModOut)
async def get_mod(mod_id: str):
    """Get a mod by id. 404 if not found."""
    uid = UUID(mod_id)
    return get_mod_or_404(uid)


@router.patch("/{mod_id}", response_model=ModOut)
async def update_mod(mod_id: str, payload: ModUpdate):
    """Partial update. 404 if not found. If vehicle_id is updated, it must exist."""
    uid = UUID(mod_id)
    existing = get_mod_or_404(uid)
    patch_data = payload.model_dump(exclude_unset=True)
    if "vehicle_id" in patch_data and not vehicle_exists(patch_data["vehicle_id"]):
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Vehicle not found")
    updated = apply_patch(existing, patch_data)
    mods_store[uid] = updated
    return updated


@router.delete("/{mod_id}", status_code=204)
async def delete_mod(mod_id: str):
    """Delete a mod. 404 if not found."""
    uid = UUID(mod_id)
    get_mod_or_404(uid)
    del mods_store[uid]
    return None
