#!/bin/sh
set -e

echo "Waiting for database..."
retries=30
until python -c "
from sqlalchemy import create_engine, text
import os
engine = create_engine(os.environ['DATABASE_URL'])
with engine.connect() as conn:
    conn.execute(text('SELECT 1'))
" 2>/dev/null; do
  retries=$((retries - 1))
  if [ "$retries" -le 0 ]; then
    echo "ERROR: database not ready after 30 attempts" >&2
    exit 1
  fi
  echo "  db not ready yet – retrying ($retries left)..."
  sleep 1
done
echo "Database is ready."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
