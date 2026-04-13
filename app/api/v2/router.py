"""API v2 router: mounts all resource routes under /api/v2."""

from fastapi import APIRouter

from app.api.v2.routes import service_records, mods, vehicles

api_router = APIRouter()

api_router.include_router(vehicles.router)
api_router.include_router(mods.router)
api_router.include_router(service_records.router)
