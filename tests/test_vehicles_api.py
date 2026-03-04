"""Tests for /api/v1/vehicles endpoints (FastAPI TestClient)."""

import uuid

BASE = "/api/v1/vehicles"


def test_create_vehicle_201_then_get_200(client):
    """Create vehicle -> 201, then get by id -> 200."""
    payload = {
        "make": "Nissan",
        "model": "Skyline GT-R R34",
        "year": 1999,
        "nickname": "Godzilla",
    }
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["make"] == "Nissan"
    assert data["model"] == "Skyline GT-R R34"
    assert data["year"] == 1999
    assert data["nickname"] == "Godzilla"
    assert "id" in data
    assert "created_at" in data
    assert r.headers.get("Location") == f"/api/v1/vehicles/{data['id']}"

    r2 = client.get(f"{BASE}/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == data["id"]


def test_list_vehicles_200(client):
    """List vehicles -> 200."""
    r = client.get(BASE)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_patch_vehicle_200_changes_nickname(client):
    """Patch vehicle -> 200 and nickname changes."""
    payload = {"make": "Toyota", "model": "Supra", "year": 1998, "nickname": "Original"}
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    vid = r.json()["id"]

    r2 = client.patch(f"{BASE}/{vid}", json={"nickname": "Updated"})
    assert r2.status_code == 200
    assert r2.json()["nickname"] == "Updated"


def test_delete_vehicle_204_then_get_404(client):
    """Delete vehicle -> 204, then get -> 404."""
    payload = {"make": "Mazda", "model": "RX-7", "year": 1995}
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    vid = r.json()["id"]

    r2 = client.delete(f"{BASE}/{vid}")
    assert r2.status_code == 204

    r3 = client.get(f"{BASE}/{vid}")
    assert r3.status_code == 404


def test_get_vehicle_nonexistent_404(client):
    """GET nonexistent vehicle -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.get(f"{BASE}/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"


def test_patch_vehicle_nonexistent_404(client):
    """PATCH nonexistent vehicle -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.patch(f"{BASE}/{fake_id}", json={"nickname": "Ghost"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"


def test_delete_vehicle_nonexistent_404(client):
    """DELETE nonexistent vehicle -> 404."""
    fake_id = str(uuid.uuid4())
    r = client.delete(f"{BASE}/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"
