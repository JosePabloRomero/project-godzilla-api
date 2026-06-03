import os

from fastapi import FastAPI

from app.api.v1.router import api_router as api_v1_router
from app.api.v2.router import api_router as api_v2_router

app = FastAPI(title="Project Godzilla API", version="2.0.0")

api_v1_app = FastAPI(title="Project Godzilla API v1", version="1.0.0")
api_v2_app = FastAPI(title="Project Godzilla API v2", version="2.0.0")

# Share the same overrides mapping used in tests.
api_v1_app.dependency_overrides = app.dependency_overrides
api_v2_app.dependency_overrides = app.dependency_overrides

api_v1_app.include_router(api_v1_router)
api_v2_app.include_router(api_v2_router)

# Reuse dependency overrides from the parent app (used by tests).
api_v1_app.router.dependency_overrides_provider = app
api_v2_app.router.dependency_overrides_provider = app

app.mount("/api/v1", api_v1_app)
app.mount("/api/v2", api_v2_app)


@api_v1_app.get("/")
async def v1_root():
    return {"message": "Welcome to the JDM Garage API v1!"}


@api_v2_app.get("/")
async def v2_root():
    return {"message": "Welcome to the JDM Garage API v2!"}


@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": "project-godzilla-api",
        "channel": os.getenv("RELEASE_CHANNEL", "stable"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("APP_ENV", "local"),
        "git_sha": os.getenv("GIT_SHA", "local"),
        "deploy_date": os.getenv("DEPLOY_DATE", "local"),
        "visible_change": os.getenv("VISIBLE_CHANGE", "Stable release"),
    }
