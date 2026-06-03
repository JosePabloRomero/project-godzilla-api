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
