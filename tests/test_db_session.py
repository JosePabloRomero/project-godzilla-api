"""Tests for app.db.session helpers."""

from app.db import session as session_module


def test_get_db_yields_session_and_closes_it(monkeypatch):
    events = {"closed": False}

    class DummySession:
        def close(self):
            events["closed"] = True

    def fake_session_local():
        return DummySession()

    monkeypatch.setattr(session_module, "SessionLocal", fake_session_local)

    dependency = session_module.get_db()
    db = next(dependency)
    assert isinstance(db, DummySession)

    try:
        next(dependency)
    except StopIteration:
        pass

    assert events["closed"] is True
