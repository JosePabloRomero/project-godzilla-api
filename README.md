# Project Godzilla API 🦖🚗

A simple RESTful API to manage a JDM garage:
- **Vehicles**
- **Mods**
- **Service Records**

> API base path: `/api/v1`  
> Swagger UI: `/docs`

## Tech stack
- FastAPI
- Pydantic
- Pytest (+ pytest-cov)
- Ruff
- Docker (Dockerfile)
- GitHub Actions (CI/CD)

## Branching & environments
- `develop` → **testing** environment (quality gate: **>= 60%** coverage)
- `main` → **production** environment (quality gate: **>= 85%** coverage)

Commits follow **GitMoji**.

---

## Local setup

### 1) Create a virtual env (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies (dev)
```bash
pip install -r requirements-dev.txt
```

### 3) Run the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:
- `http://localhost:8000/` (welcome message)
- `http://localhost:8000/docs`

---

## Commands

### Lint
```bash
ruff check .
```

### Tests
```bash
python -m pytest -q
```

### Coverage gate (testing / develop)
```bash
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=60
```

### Coverage gate (production / main)
```bash
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85
```

---

## Docker

### Build
```bash
docker build -t project-godzilla-api:local .
```

### Run
```bash
docker run --rm -p 8000:8000 project-godzilla-api:local
```

---

## Run with Docker Compose

Start Postgres + API (with auto-migrations) in one command:

```bash
make docker-up
```

or directly:

```bash
docker compose up --build
```

Stop everything:

```bash
make docker-down
```

---