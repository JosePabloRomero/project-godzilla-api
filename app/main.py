from fastapi import FastAPI

from app.api.v2.router import api_router

app = FastAPI(title="Project Godzilla API", version="2.0.0")


@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}


app.include_router(api_router, prefix="/api/v2")
