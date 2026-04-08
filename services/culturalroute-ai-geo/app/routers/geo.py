from fastapi import APIRouter
from app.schemas.geo_schema import GeoPoint
from app.application.geo_service import GeoService

router = APIRouter(prefix="/geo", tags=["Geo"])

geo_service = GeoService()

@router.post("/points")
def create_point(point: GeoPoint):
    return geo_service.save_point(point)

@router.get("/places/{place_id}")
def get_place_location(place_id: str):
    return geo_service.get_location(place_id)

@router.get("/distance")
def get_distance(lat1: float, lng1: float, lat2: float, lng2: float):
    return geo_service.calculate_distance(lat1, lng1, lat2, lng2)
