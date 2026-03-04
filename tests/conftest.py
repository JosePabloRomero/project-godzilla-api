"""Shared fixtures for API tests using a temporary SQLite database."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.db import get_db
from app.main import app
from app.models import Base, Mod, ServiceRecord, Vehicle


@pytest.fixture(scope="session")
def _engine(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    engine = create_engine(
        f"sqlite+pysqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def _session_factory(_engine):
    return sessionmaker(
        bind=_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


@pytest.fixture(autouse=True)
def db_session(_session_factory):
    """Provide a clean DB state for every test."""
    session = _session_factory()
    session.execute(delete(ServiceRecord))
    session.execute(delete(Mod))
    session.execute(delete(Vehicle))
    session.commit()
    session.close()


@pytest.fixture(scope="session", autouse=True)
def _override_db(_session_factory):
    """Wire the app's get_db dependency to use the test database."""
    def _get_db():
        db = _session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client():
    return TestClient(app)
