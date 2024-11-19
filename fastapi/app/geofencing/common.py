from datetime import datetime

from pydantic import BaseModel

from app.geofencing.models import Geolocation


class GeolocationRequestModel(BaseModel):
    longitude: float
    latitude: float
    timestamp: datetime = datetime.now()


class GeoFenceModelRequestModel(BaseModel):
    name: str
    address: str
    shape: list[Geolocation]
