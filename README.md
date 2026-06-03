# Project Godzilla API 🦖🚗

A simple RESTful API to manage a JDM garage:
- **Vehicles**
- **Mods**
- **Service Records**

Two mounted API surfaces share the same FastAPI app:

| Version | Base path | What it includes |
|:--------|:----------|:-----------------|
| **v1** | `/api/v1` | Garage resources only (`vehicles`, `mods`, `service-records`). |
| **v2** | `/api/v2` | Same garage resources **plus** the multicloud integration endpoint (see below). |

**Swagger UI (per version):** `/api/v1/docs` · `/api/v2/docs`  
The root app also exposes `/docs` at the top level; use **`/api/v2/docs`** for the multicloud flow and v2 routes.

**Multicloud integration (v2 only):** `POST /api/v2/integration/multicloud` — accepts `cliente`, `podcast`, and optional `vehicle_id`, resolves or injects a **vehicle** in PostgreSQL, and returns the enriched payload (`cliente`, `podcast`, `vehicle`).

## Tech stack
- FastAPI
- Pydantic
- SQLAlchemy (ORM)
- Alembic (migrations)
- Google Cloud Platform (GCP)
- Google Kubernetes Engine (GKE Autopilot)
- Cloud SQL for PostgreSQL 18
- Artifact Registry
- Pytest (+ pytest-cov)
- Ruff
- Docker (Dockerfile + Compose)
- GitHub Actions (CI/CD)

## Branching & environments
- `develop` → **testing** environment (quality gate: **>= 60%** coverage)
- `main` → **production** environment (quality gate: **>= 85%** coverage)

## CI/CD & deployments
- Deploys are triggered from GitHub Actions **only after** lint, tests, and coverage gates pass.
- Testing (`develop`): lint, tests, and coverage only — **no deploy to GKE**.
- Production deploy: `main` → **Google Kubernetes Engine (GKE)**

Commits follow **GitMoji**.

## 🌐 Deployed environments (GCP)

Our API is deployed on **Google Kubernetes Engine (GKE)** in the `us-east4` region. The CI/CD pipeline uses GitHub Actions and Workload Identity Federation for secure, keyless authentication.

| Environment | Branch | Infrastructure |
|:-----------:|:------:|:---------------|
| **Testing** | `develop` | CI only (lint, tests, coverage gate >= 60%) |
| **Production** | `main` | GCP `us-east4`: GKE Autopilot (`godzilla-api-cluster`) + Cloud SQL PostgreSQL 18 + Artifact Registry |

> 📖 **API docs (Swagger UI)** — use **v2** for garage + multicloud:
> - `http://<GKE_EXTERNAL_IP>/api/v2/docs`
> *(Run `kubectl get service godzilla-api` to retrieve the current IP; replace `<GKE_EXTERNAL_IP>` accordingly.)*

## Canary Deployment

In production the API runs on Kubernetes as two Deployments—`godzilla-api-stable` and `godzilla-api-canary`—that share the `godzilla-api` Service. Both route traffic to Pods selected by the common label `app: godzilla-api`.

Call `GET /health` to tell whether a response came from the **stable** or **canary** release (see the `channel` field in the JSON).

```bash
kubectl get svc godzilla-api
curl http://<EXTERNAL-IP>/health
kubectl get pods -l app=godzilla-api --show-labels
```

Infrastructure is provisioned with Terraform; application deploys run from GitHub Actions on push to `main`.

## Multi-Cloud Architecture Diagram

This diagram shows an end-to-end request/response flow across two cloud providers. The transaction starts in GCP (`API 1 - Origen`), is enriched in AWS (`API 2 - Intermedia`), and is completed in GCP (`API 3 - Terminal`) to return a final aggregated message (`Client + Podcast + Vehicle`) to the user. Telemetry is collected independently through Grafana/Prometheus for `API_1` and `API_2`, while `API_3` reports errors to Sentry.

In this repository, the **terminal** enrichment step is implemented under **`/api/v2`** via `POST /api/v2/integration/multicloud` (see Swagger at `/api/v2/docs`).

![Multi-cloud architecture diagram](./multicloud-architecture.png)

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
- `http://localhost:8000/api/v1/docs` · `http://localhost:8000/api/v2/docs` (Swagger; **v2** for multicloud)

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

The recommended way to run the full stack locally (API + PostgreSQL) is with **Docker Compose**, which handles the database, migrations, and networking automatically.

### Run with Docker Compose (recommended)

```bash
make docker-up
```

or directly:

```bash
docker compose up --build
```

This starts **PostgreSQL** and the **API** with auto-migrations. Once running, open:
- `http://0.0.0.0:8000/` (welcome message)
- `http://0.0.0.0:8000/api/v2/docs` (Swagger UI — **v2** includes multicloud integration)

Stop everything:

```bash
make docker-down
```

### Standalone Docker (API only, no database)

If you only need the API container without Compose:

```bash
docker build -t project-godzilla-api:local .
docker run --rm -p 8000:8000 project-godzilla-api:local
```

> ⚠️ Running standalone requires an external PostgreSQL instance and the proper `DATABASE_URL` environment variable.

---