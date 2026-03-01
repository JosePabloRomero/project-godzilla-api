"""Unit tests for Mod schemas (no DB, no endpoints)."""

from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.mod import ModCreate


def test_mod_create_valid():
    """Valid data creates ModCreate successfully."""
    vehicle_id = uuid4()
    data = {
        "vehicle_id": vehicle_id,
        "name": "Racing Coilovers",
        "category": "suspension",
        "installed_at": date(2026, 1, 15),
        "notes": "Front and rear set.",
    }
    mod = ModCreate(**data)
    assert mod.vehicle_id == vehicle_id
    assert mod.name == "Racing Coilovers"
    assert mod.category == "suspension"
    assert mod.installed_at == date(2026, 1, 15)
    assert mod.notes == "Front and rear set."


def test_mod_create_invalid_name_empty():
    """Empty name raises ValidationError."""
    vehicle_id = uuid4()
    with pytest.raises(ValidationError):
        ModCreate(
            vehicle_id=vehicle_id,
            name="",
            category="suspension",
            installed_at=date(2026, 1, 15),
        )
