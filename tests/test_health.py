def test_health_defaults(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {
        "status": "ok",
        "app": "project-godzilla-api",
        "channel": "stable",
        "version": "1.0.0",
        "environment": "local",
        "git_sha": "local",
        "deploy_date": "local",
        "visible_change": "Stable release",
    }


def test_health_canary_channel(client, monkeypatch):
    monkeypatch.setenv("RELEASE_CHANNEL", "canary")
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["channel"] == "canary"


def test_root_canary_channel(client, monkeypatch):
    monkeypatch.setenv("RELEASE_CHANNEL", "canary")
    monkeypatch.setenv("APP_VERSION", "1.1.0-canary")
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["channel"] == "canary"
    assert data["version"] == "1.1.0-canary"
    assert data["message"] == "Welcome to the JDM Garage API - Canary Preview!"
    assert data["preview_feature"] == "Canary deployment validation"
