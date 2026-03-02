from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(title="Project Godzilla API")


@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}


app.include_router(api_router, prefix="/api/v1")
