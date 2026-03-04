"""Unit tests for Vehicle schemas (no DB, no endpoints)."""

import pytest
from pydantic import ValidationError

from app.schemas.vehicle import VehicleCreate


def test_vehicle_create_valid():
    """Valid data creates VehicleCreate successfully."""
    data = {
        "make": "Nissan",
        "model": "Skyline GT-R R34",
        "year": 1999,
        "nickname": "Godzilla",
    }
    vehicle = VehicleCreate(**data)
    assert vehicle.make == "Nissan"
    assert vehicle.model == "Skyline GT-R R34"
    assert vehicle.year == 1999
    assert vehicle.nickname == "Godzilla"


def test_vehicle_create_invalid_make_empty():
    """Empty make raises ValidationError."""
    with pytest.raises(ValidationError):
        VehicleCreate(
            make="",
            model="Skyline GT-R R34",
            year=1999,
        )
