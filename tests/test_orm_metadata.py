"""Smoke tests for ORM metadata — no real DB connection required."""

from __future__ import annotations

from sqlalchemy.orm import class_mapper

from app.models import Base, Vehicle


EXPECTED_TABLES = {"vehicles", "mods", "service_records"}


def test_all_tables_registered_in_metadata():
    registered = set(Base.metadata.tables.keys())
    assert EXPECTED_TABLES.issubset(registered), (
        f"Faltan tablas en Base.metadata: {EXPECTED_TABLES - registered}"
    )


def test_vehicles_columns():
    table = Base.metadata.tables["vehicles"]
    col_names = {c.name for c in table.columns}
    for expected in ("id", "make", "model", "year", "nickname", "created_at"):
        assert expected in col_names, f"Columna '{expected}' no encontrada en vehicles"


def test_mods_columns():
    table = Base.metadata.tables["mods"]
    col_names = {c.name for c in table.columns}
    for expected in ("id", "vehicle_id", "name", "category", "installed_at", "created_at"):
        assert expected in col_names, f"Columna '{expected}' no encontrada en mods"


def test_service_records_columns():
    table = Base.metadata.tables["service_records"]
    col_names = {c.name for c in table.columns}
    for expected in ("id", "vehicle_id", "service_type", "mileage", "service_date", "created_at"):
        assert expected in col_names, f"Columna '{expected}' no encontrada en service_records"


def test_vehicle_has_mods_relationship():
    mapper = class_mapper(Vehicle)
    rel_names = {r.key for r in mapper.relationships}
    assert "mods" in rel_names, "Vehicle no tiene relación 'mods'"


def test_vehicle_has_service_records_relationship():
    mapper = class_mapper(Vehicle)
    rel_names = {r.key for r in mapper.relationships}
    assert "service_records" in rel_names, "Vehicle no tiene relación 'service_records'"
