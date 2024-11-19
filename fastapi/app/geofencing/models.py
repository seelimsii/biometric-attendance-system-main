from datetime import datetime
from pydantic import BaseModel


class Geolocation(BaseModel):
    latitude: float
    longitude: float


class Geofence(BaseModel):
    name: str
    shape: list[Geolocation]
