from fastapi import FastAPI
from app.schemas import VehicleCreate, VehicleOut

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}

@app.post("/vehicles")
async def create_vehicle(vehicle: VehicleCreate):
    return vehicle