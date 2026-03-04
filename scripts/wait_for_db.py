"""Wait for the database to accept connections (retry with SELECT 1)."""

import os
import time

import sqlalchemy

engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])

for attempt in range(30):
    try:
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        print("DB ready")
        break
    except Exception:
        time.sleep(1)
else:
    raise RuntimeError("DB not ready after 30s")

engine.dispose()
