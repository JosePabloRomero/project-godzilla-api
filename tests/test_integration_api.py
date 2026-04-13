"""Tests for /api/v2/integration endpoints (FastAPI TestClient)."""

BASE = "/api/v2/integration/multicloud"
VEHICLES_BASE = "/api/v2/vehicles"


def test_integration_enriches_payload_using_vehicle_seed(client):
    payload = {
        "api1_payload": {
            "cliente": {"id": "c-123", "nombre": "Akira"},
            "evaluacion": {"riesgo": "medio"},
            "solicitud": {"tipo": "cotizacion"},
        },
        "vehicle_seed": {
            "make": "Nissan",
            "model": "Skyline GT-R R34",
            "year": 1999,
            "nickname": "Godzilla",
        },
        "trace_id": "trace-001",
    }

    r = client.post(BASE, json=payload)
    assert r.status_code == 200
    data = r.json()

    assert data["api1_payload"] == payload["api1_payload"]
    assert data["trace_id"] == "trace-001"
    assert data["vehicle"]["make"] == "Nissan"
    assert data["vehicle"]["model"] == "Skyline GT-R R34"
    assert data["vehicle"]["year"] == 1999
    assert data["vehicle"]["nickname"] == "Godzilla"
    assert "id" in data["vehicle"]
    assert "created_at" in data["vehicle"]


def test_integration_uses_existing_vehicle_when_seed_not_sent(client):
    v = client.post(
        VEHICLES_BASE,
        json={"make": "Toyota", "model": "Supra", "year": 1998, "nickname": "MK4"},
    )
    assert v.status_code == 201
    existing_id = v.json()["id"]

    r = client.post(BASE, json={"api1_payload": {"cliente": {"id": "c-777"}}})
    assert r.status_code == 200
    data = r.json()

    assert data["api1_payload"]["cliente"]["id"] == "c-777"
    assert data["vehicle"]["id"] == existing_id
    assert data["vehicle"]["make"] == "Toyota"


def test_integration_creates_default_vehicle_when_db_is_empty(client):
    r = client.post(BASE, json={"api1_payload": {"solicitud": {"id": "s-1"}}})
    assert r.status_code == 200
    data = r.json()

    assert data["api1_payload"]["solicitud"]["id"] == "s-1"
    assert data["vehicle"]["make"] == "Unknown"
    assert data["vehicle"]["model"] == "Multicloud Car"
    assert data["vehicle"]["nickname"] == "Integration Test Car"
