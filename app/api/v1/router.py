"""API v1 router: mounts all resource routes under /api/v1."""

from fastapi import APIRouter

from app.api.v1.routes import service_records, mods, vehicles

api_router = APIRouter()

api_router.include_router(vehicles.router)
api_router.include_router(mods.router)
api_router.include_router(service_records.router)
