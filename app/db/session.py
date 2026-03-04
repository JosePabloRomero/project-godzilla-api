"""Database engine and session factory. Reads DATABASE_URL from env."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_DEFAULT_URL = "sqlite+pysqlite:///./dev.db"
DATABASE_URL = os.environ.get("DATABASE_URL", _DEFAULT_URL)

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

def get_db():
    """Dependency that yields a DB session and closes it on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
