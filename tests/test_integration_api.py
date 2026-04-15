"""Tests for /api/v2/integration endpoints (FastAPI TestClient)."""

BASE = "/api/v2/integration/multicloud"
VEHICLES_BASE = "/api/v2/vehicles"


def test_integration_uses_vehicle_when_valid_id_is_sent(client):
    v = client.post(
        VEHICLES_BASE,
        json={"make": "Nissan", "model": "Skyline GT-R R34", "year": 1999, "nickname": "Godzilla"},
    )
    assert v.status_code == 201
    existing_id = v.json()["id"]

    payload = {
        "cliente": {"id": "c-123", "nombre": "Akira"},
        "podcast": {"id": "p-1", "titulo": "Episode One"},
        "vehicle_id": existing_id,
        "trace_id": "trace-001",
    }

    r = client.post(BASE, json=payload)
    assert r.status_code == 200
    data = r.json()

    assert data["cliente"] == payload["cliente"]
    assert data["podcast"] == payload["podcast"]
    assert data["vehicle"]["id"] == existing_id
    assert data["trace_id"] == "trace-001"
    assert data["vehicle"]["make"] == "Nissan"
    assert data["vehicle"]["model"] == "Skyline GT-R R34"
    assert data["vehicle"]["year"] == 1999
    assert data["vehicle"]["nickname"] == "Godzilla"
    assert "created_at" in data["vehicle"]


def test_integration_uses_existing_vehicle_when_id_not_sent(client):
    v = client.post(
        VEHICLES_BASE,
        json={"make": "Toyota", "model": "Supra", "year": 1998, "nickname": "MK4"},
    )
    assert v.status_code == 201
    existing_id = v.json()["id"]

    r = client.post(
        BASE,
        json={
            "cliente": {"id": "c-777"},
            "podcast": {"id": "p-777", "titulo": "Fallback episode"},
        },
    )
    assert r.status_code == 200
    data = r.json()

    assert data["cliente"]["id"] == "c-777"
    assert data["podcast"]["id"] == "p-777"
    assert data["vehicle"]["id"] == existing_id
    assert data["vehicle"]["make"] == "Toyota"


def test_integration_creates_default_vehicle_when_db_is_empty(client):
    payload = {
        "cliente": {"id": "c-empty"},
        "podcast": {"id": "p-empty"},
        "correlation_id": "corr-xyz",
    }
    r = client.post(BASE, json=payload)
    assert r.status_code == 200
    data = r.json()

    assert data["cliente"]["id"] == "c-empty"
    assert data["podcast"]["id"] == "p-empty"
    assert data["correlation_id"] == "corr-xyz"
    assert data["vehicle"]["make"] == "Unknown"
    assert data["vehicle"]["model"] == "Multicloud"
    assert data["vehicle"]["year"] == 2000
