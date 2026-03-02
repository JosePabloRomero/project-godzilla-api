"""Tests for /api/v1/service-records endpoints (FastAPI TestClient)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VEHICLES_BASE = "/api/v1/vehicles"
SERVICE_RECORDS_BASE = "/api/v1/service-records"


def test_create_vehicle_then_create_service_record_201():
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


def test_create_service_record_with_nonexistent_vehicle_id_404():
    """Create service record with non-existent vehicle_id -> 404."""
    import uuid

    fake_id = str(uuid.uuid4())
    record_payload = {
        "vehicle_id": fake_id,
        "service_type": "oil_change",
        "mileage": 50000,
        "service_date": "2024-01-01",
    }
    r = client.post(SERVICE_RECORDS_BASE, json=record_payload)
    assert r.status_code == 404
