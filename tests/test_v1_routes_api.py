"""Integration tests for /api/v1 routes using a dedicated FastAPI app."""

import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.router import api_router
from app.db import get_db

BASE_VEHICLES = "/api/v1/vehicles"
BASE_MODS = "/api/v1/mods"
BASE_RECORDS = "/api/v1/service-records"


@pytest.fixture()
def v1_client(_session_factory):
    app = FastAPI()

    def _get_db():
        db = _session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    app.include_router(api_router, prefix="/api/v1")
    return TestClient(app)


def _create_vehicle(v1_client):
    response = v1_client.post(
        BASE_VEHICLES,
        json={
            "make": "Nissan",
            "model": "Skyline",
            "year": 1999,
            "nickname": "Godzilla",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_v1_vehicles_crud_and_404_paths(v1_client):
    vehicle_id = _create_vehicle(v1_client)

    listed = v1_client.get(BASE_VEHICLES, params={"skip": 0, "limit": 10})
    assert listed.status_code == 200
    assert any(item["id"] == vehicle_id for item in listed.json())

    fetched = v1_client.get(f"{BASE_VEHICLES}/{vehicle_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == vehicle_id

    patched = v1_client.patch(f"{BASE_VEHICLES}/{vehicle_id}", json={"nickname": "R34"})
    assert patched.status_code == 200
    assert patched.json()["nickname"] == "R34"

    deleted = v1_client.delete(f"{BASE_VEHICLES}/{vehicle_id}")
    assert deleted.status_code == 204

    not_found_get = v1_client.get(f"{BASE_VEHICLES}/{vehicle_id}")
    assert not_found_get.status_code == 404
    assert not_found_get.json()["detail"] == "Vehicle not found"

    fake_id = str(uuid.uuid4())
    not_found_patch = v1_client.patch(f"{BASE_VEHICLES}/{fake_id}", json={"nickname": "Ghost"})
    assert not_found_patch.status_code == 404
    assert not_found_patch.json()["detail"] == "Vehicle not found"

    not_found_delete = v1_client.delete(f"{BASE_VEHICLES}/{fake_id}")
    assert not_found_delete.status_code == 404
    assert not_found_delete.json()["detail"] == "Vehicle not found"


def test_v1_mods_success_filters_and_errors(v1_client):
    vehicle_id = _create_vehicle(v1_client)

    create_mod = v1_client.post(
        BASE_MODS,
        json={
            "vehicle_id": vehicle_id,
            "name": "Coilovers",
            "category": "suspension",
            "installed_at": "2020-01-01",
            "notes": "Track setup",
        },
    )
    assert create_mod.status_code == 201
    mod_id = create_mod.json()["id"]

    all_mods = v1_client.get(BASE_MODS)
    assert all_mods.status_code == 200
    assert any(item["id"] == mod_id for item in all_mods.json())

    filtered = v1_client.get(BASE_MODS, params={"vehicle_id": vehicle_id})
    assert filtered.status_code == 200
    assert all(item["vehicle_id"] == vehicle_id for item in filtered.json())

    mod_by_id = v1_client.get(f"{BASE_MODS}/{mod_id}")
    assert mod_by_id.status_code == 200
    assert mod_by_id.json()["id"] == mod_id

    updated = v1_client.patch(f"{BASE_MODS}/{mod_id}", json={"name": "Street Coilovers"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Street Coilovers"

    bad_vehicle_patch = v1_client.patch(
        f"{BASE_MODS}/{mod_id}",
        json={"vehicle_id": str(uuid.uuid4())},
    )
    assert bad_vehicle_patch.status_code == 404
    assert bad_vehicle_patch.json()["detail"] == "Vehicle not found"

    deleted = v1_client.delete(f"{BASE_MODS}/{mod_id}")
    assert deleted.status_code == 204

    not_found_get = v1_client.get(f"{BASE_MODS}/{mod_id}")
    assert not_found_get.status_code == 404
    assert not_found_get.json()["detail"] == "Mod not found"

    fake_id = str(uuid.uuid4())
    not_found_patch = v1_client.patch(f"{BASE_MODS}/{fake_id}", json={"name": "Ghost"})
    assert not_found_patch.status_code == 404
    assert not_found_patch.json()["detail"] == "Mod not found"

    not_found_delete = v1_client.delete(f"{BASE_MODS}/{fake_id}")
    assert not_found_delete.status_code == 404
    assert not_found_delete.json()["detail"] == "Mod not found"

    create_with_missing_vehicle = v1_client.post(
        BASE_MODS,
        json={
            "vehicle_id": str(uuid.uuid4()),
            "name": "Turbo",
            "category": "engine",
            "installed_at": "2021-01-01",
        },
    )
    assert create_with_missing_vehicle.status_code == 404
    assert create_with_missing_vehicle.json()["detail"] == "Vehicle not found"


def test_v1_service_records_success_filters_and_errors(v1_client):
    vehicle_id = _create_vehicle(v1_client)

    created = v1_client.post(
        BASE_RECORDS,
        json={
            "vehicle_id": vehicle_id,
            "service_type": "oil_change",
            "mileage": 120000,
            "service_date": "2024-03-01",
            "notes": "Full synthetic",
        },
    )
    assert created.status_code == 201
    record_id = created.json()["id"]

    all_records = v1_client.get(BASE_RECORDS)
    assert all_records.status_code == 200
    assert any(item["id"] == record_id for item in all_records.json())

    filtered = v1_client.get(BASE_RECORDS, params={"vehicle_id": vehicle_id})
    assert filtered.status_code == 200
    assert all(item["vehicle_id"] == vehicle_id for item in filtered.json())

    record_by_id = v1_client.get(f"{BASE_RECORDS}/{record_id}")
    assert record_by_id.status_code == 200
    assert record_by_id.json()["id"] == record_id

    updated = v1_client.patch(f"{BASE_RECORDS}/{record_id}", json={"mileage": 125000})
    assert updated.status_code == 200
    assert updated.json()["mileage"] == 125000

    bad_vehicle_patch = v1_client.patch(
        f"{BASE_RECORDS}/{record_id}",
        json={"vehicle_id": str(uuid.uuid4())},
    )
    assert bad_vehicle_patch.status_code == 404
    assert bad_vehicle_patch.json()["detail"] == "Vehicle not found"

    deleted = v1_client.delete(f"{BASE_RECORDS}/{record_id}")
    assert deleted.status_code == 204

    not_found_get = v1_client.get(f"{BASE_RECORDS}/{record_id}")
    assert not_found_get.status_code == 404
    assert not_found_get.json()["detail"] == "Service record not found"

    fake_id = str(uuid.uuid4())
    not_found_patch = v1_client.patch(f"{BASE_RECORDS}/{fake_id}", json={"mileage": 99999})
    assert not_found_patch.status_code == 404
    assert not_found_patch.json()["detail"] == "Service record not found"

    not_found_delete = v1_client.delete(f"{BASE_RECORDS}/{fake_id}")
    assert not_found_delete.status_code == 404
    assert not_found_delete.json()["detail"] == "Service record not found"

    create_with_missing_vehicle = v1_client.post(
        BASE_RECORDS,
        json={
            "vehicle_id": str(uuid.uuid4()),
            "service_type": "brake_pad",
            "mileage": 80000,
            "service_date": "2023-06-01",
        },
    )
    assert create_with_missing_vehicle.status_code == 404
    assert create_with_missing_vehicle.json()["detail"] == "Vehicle not found"
