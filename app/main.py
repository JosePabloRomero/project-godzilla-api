from fastapi import FastAPI
from app.schemas import VehicleCreate

app = FastAPI(title="Project Godzilla API")

@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}

@app.post("/vehicles")
async def create_vehicle(vehicle: VehicleCreate):
    return vehicle