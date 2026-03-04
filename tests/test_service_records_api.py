"""Tests for /api/v1/service-records endpoints (FastAPI TestClient)."""

import uuid

VEHICLES_BASE = "/api/v1/vehicles"
SERVICE_RECORDS_BASE = "/api/v1/service-records"


def test_create_vehicle_then_create_service_record_201(client):
    """Create vehicle -> create service record -> 201."""
    v = client.post(
        VEHICLES_BASE,
        json={
            "make": "Nissan",
            "model": "Skyline",
            "year": 1999,
        },
    )
    assert v.status_code == 201
    vehicle_id = v.json()["id"]

    record_payload = {
        "vehicle_id": vehicle_id,
        "service_type": "oil_change",
        "mileage": 120000,
        "service_date": "2024-03-01",
        "notes": "Full synthetic",
    }
    r = client.post(SERVICE_RECORDS_BASE, json=record_payload)
    assert r.status_code == 201
    data = r.json()
    assert data["vehicle_id"] == vehicle_id
    assert data["service_type"] == "oil_change"
    assert data["mileage"] == 120000
    assert "id" in data
    assert "created_at" in data
    assert r.headers.get("Location") == f"/api/v1/service-records/{data['id']}"


def test_create_service_record_with_nonexistent_vehicle_id_404(client):
    """Create service record with non-existent vehicle_id -> 404."""
    fake_id = str(uuid.uuid4())
    record_payload = {
        "vehicle_id": fake_id,
        "service_type": "oil_change",
        "mileage": 50000,
        "service_date": "2024-01-01",
    }
    r = client.post(SERVICE_RECORDS_BASE, json=record_payload)
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"


def test_get_service_record_nonexistent_404(client):
    """GET nonexistent service record -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.get(f"{SERVICE_RECORDS_BASE}/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Service record not found"


def test_delete_service_record_nonexistent_404(client):
    """DELETE nonexistent service record -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.delete(f"{SERVICE_RECORDS_BASE}/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Service record not found"


def test_patch_service_record_nonexistent_404(client):
    """PATCH nonexistent service record -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.patch(f"{SERVICE_RECORDS_BASE}/{fake_id}", json={"mileage": 99999})
    assert r.status_code == 404
    assert r.json()["detail"] == "Service record not found"


def test_patch_service_record_vehicle_id_nonexistent_404(client):
    """PATCH service record with vehicle_id pointing to nonexistent vehicle -> 404."""
    v = client.post(VEHICLES_BASE, json={"make": "Honda", "model": "S2000", "year": 2001})
    assert v.status_code == 201
    vid = v.json()["id"]

    rec = client.post(
        SERVICE_RECORDS_BASE,
        json={
            "vehicle_id": vid,
            "service_type": "brake_pad",
            "mileage": 80000,
            "service_date": "2023-06-01",
        },
    )
    assert rec.status_code == 201
    rec_id = rec.json()["id"]

    fake_vehicle = str(uuid.uuid4())
    r = client.patch(f"{SERVICE_RECORDS_BASE}/{rec_id}", json={"vehicle_id": fake_vehicle})
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"
