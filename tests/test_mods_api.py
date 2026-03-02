"""Tests for /api/v1/mods endpoints (FastAPI TestClient)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VEHICLES_BASE = "/api/v1/vehicles"
MODS_BASE = "/api/v1/mods"


def test_create_vehicle_then_create_mod_201():
    """Create vehicle -> create valid mod -> 201."""
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

    mod_payload = {
        "vehicle_id": vehicle_id,
        "name": "Racing Coilovers",
        "category": "suspension",
        "installed_at": "2020-05-15",
        "notes": "Track setup",
    }
    r = client.post(MODS_BASE, json=mod_payload)
    assert r.status_code == 201
    data = r.json()
    assert data["vehicle_id"] == vehicle_id
    assert data["name"] == "Racing Coilovers"
    assert "id" in data
    assert "created_at" in data
    assert r.headers.get("Location") == f"/api/v1/mods/{data['id']}"


def test_create_mod_with_nonexistent_vehicle_id_404():
    """Create mod with non-existent vehicle_id -> 404."""
    import uuid

    fake_id = str(uuid.uuid4())
    mod_payload = {
        "vehicle_id": fake_id,
        "name": "Turbo",
        "category": "engine",
        "installed_at": "2021-01-01",
    }
    r = client.post(MODS_BASE, json=mod_payload)
    assert r.status_code == 404


def test_list_mods_with_vehicle_id_filter():
    """List mods with ?vehicle_id= returns only that vehicle's mods."""
    v1 = client.post(VEHICLES_BASE, json={"make": "A", "model": "M1", "year": 2000})
    v2 = client.post(VEHICLES_BASE, json={"make": "B", "model": "M2", "year": 2001})
    assert v1.status_code == 201 and v2.status_code == 201
    id1, id2 = v1.json()["id"], v2.json()["id"]

    client.post(
        MODS_BASE,
        json={
            "vehicle_id": id1,
            "name": "Mod1",
            "category": "suspension",
            "installed_at": "2020-01-01",
        },
    )
    client.post(
        MODS_BASE,
        json={
            "vehicle_id": id2,
            "name": "Mod2",
            "category": "engine",
            "installed_at": "2020-01-01",
        },
    )

    r = client.get(MODS_BASE, params={"vehicle_id": id1})
    assert r.status_code == 200
    items = r.json()
    assert all(m["vehicle_id"] == id1 for m in items)
    assert len(items) >= 1
