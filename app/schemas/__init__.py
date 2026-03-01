# app/schemas/__init__.py
from .mod import ModBase, ModCreate, ModOut, ModUpdate
from .service_record import (
    ServiceRecordBase,
    ServiceRecordCreate,
    ServiceRecordOut,
    ServiceRecordUpdate,
)
from .vehicle import VehicleBase, VehicleCreate, VehicleOut, VehicleUpdate

__all__ = [
    # Vehicle
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleOut",
    # Mod
    "ModBase",
    "ModCreate",
    "ModUpdate",
    "ModOut",
    # ServiceRecord
    "ServiceRecordBase",
    "ServiceRecordCreate",
    "ServiceRecordUpdate",
    "ServiceRecordOut",
]