from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.infrastructure.database import get_db, init_db
from app.infrastructure.repositories import SQLAlchemyPlaceRepository
from app.application.place_service import PlaceService
from app.schemas.place import (
    PlaceCreateRequest,
    PlaceUpdateRequest,
    PlaceResponse,
    PlaceListResponse
)

router = APIRouter(prefix="/places", tags=["places"])

def get_place_service(db: Session = Depends(get_db)):
    repository = SQLAlchemyPlaceRepository(db)
    return PlaceService(repository)

@router.on_event("startup")
async def startup_event():
    init_db()

@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_place(
    request: PlaceCreateRequest,
    place_service: PlaceService = Depends(get_place_service)
):
    """Crear un nuevo lugar cultural"""
    try:
        place = await place_service.create_place(request)
        return PlaceResponse(
            id=place.id,
            name=place.name,
            description=place.description,
            category=place.category,
            city=place.city,
            address=place.address,
            latitude=place.latitude,
            longitude=place.longitude,
            rating=place.rating,
            status=place.status,
            source=place.source,
            created_at=place.created_at,
            updated_at=place.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=PlaceListResponse)
async def list_places(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    place_service: PlaceService = Depends(get_place_service)
):
    """Listar todos los lugares culturales"""
    try:
        print("=== LISTANDO LUGARES ===")
        places = await place_service.list_places(skip, limit)
        print(f"Encontrados: {len(places)} lugares")
        for p in places:
            print(f"  - {p.name}")
        return PlaceListResponse(
            places=[
                PlaceResponse(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    category=p.category,
                    city=p.city,
                    address=p.address,
                    latitude=p.latitude,
                    longitude=p.longitude,
                    rating=p.rating,
                    status=p.status,
                    source=p.source,
                    created_at=p.created_at,
                    updated_at=p.updated_at
                ) for p in places
            ],
            total=len(places)
        )
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(
    place_id: str,
    place_service: PlaceService = Depends(get_place_service)
):
    """Obtener un lugar por ID"""
    try:
        place = await place_service.get_place(UUID(place_id))
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        return PlaceResponse(
            id=place.id,
            name=place.name,
            description=place.description,
            category=place.category,
            city=place.city,
            address=place.address,
            latitude=place.latitude,
            longitude=place.longitude,
            rating=place.rating,
            status=place.status,
            source=place.source,
            created_at=place.created_at,
            updated_at=place.updated_at
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid place ID")


@router.put("/{place_id}", response_model=PlaceResponse)
async def update_place(
        place_id: str,
        request: PlaceUpdateRequest,
        place_service: PlaceService = Depends(get_place_service)
):
    """Actualizar un lugar"""
    try:
        print(f"📝 Actualizando lugar: {place_id}")
        print(f"   Datos: {request}")

        place = await place_service.update_place(UUID(place_id), request)
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")

        return PlaceResponse(
            id=place.id,
            name=place.name,
            description=place.description,
            category=place.category,
            city=place.city,
            address=place.address,
            latitude=place.latitude,
            longitude=place.longitude,
            rating=place.rating,
            status=place.status,
            source=place.source,
            created_at=place.created_at,
            updated_at=place.updated_at
        )
    except Exception as e:
        print(f"❌ Error en update: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(
    place_id: str,
    place_service: PlaceService = Depends(get_place_service)
):
    """Eliminar un lugar"""
    try:
        deleted = await place_service.delete_place(UUID(place_id))
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid place ID")