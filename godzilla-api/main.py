import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

class VehicleBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    make: str = Field(..., example="Nissan"),
    model: str = Field(..., example="Skyline GT-R R34"),
    year: int = Field(..., example=1999),
    nickname: str | None = Field(None, example="Godzilla")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the JDM Garage API!"}

@app.post("/vehicles")
async def create_vehicle(vehicle: VehicleBase):
    return vehicle