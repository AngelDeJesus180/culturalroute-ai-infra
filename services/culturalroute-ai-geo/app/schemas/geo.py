from pydantic import BaseModel

class GeoPoint(BaseModel):
    place_id: str
    latitude: float
    longitude: float
