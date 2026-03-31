from datetime import datetime
from uuid import UUID
from typing import Optional, List
from app.domain.models import Place, PlaceStatus
from app.domain.repositories import PlaceRepository
from app.schemas.place import PlaceCreateRequest, PlaceUpdateRequest


class PlaceService:

    def __init__(self, place_repository: PlaceRepository):
        self.place_repository = place_repository

    async def create_place(self, request: PlaceCreateRequest) -> Place:
        """Crear un nuevo lugar"""
        place = Place.create(
            name=request.name,
            description=request.description,
            category=request.category,
            city=request.city,
            address=request.address,
            latitude=request.latitude,
            longitude=request.longitude
        )
        return await self.place_repository.save(place)

    async def get_place(self, place_id: UUID) -> Optional[Place]:
        """Obtener lugar por ID"""
        return await self.place_repository.find_by_id(place_id)

    async def list_places(self, skip: int = 0, limit: int = 100) -> List[Place]:
        """Listar todos los lugares"""
        print(f"📋 list_places llamado con skip={skip}, limit={limit}")
        try:
            result = await self.place_repository.find_all(skip, limit)
            print(f"✅ Se encontraron {len(result)} lugares")
            return result
        except Exception as e:
            print(f"❌ Error en list_places: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def update_place(self, place_id: UUID, request: PlaceUpdateRequest) -> Optional[Place]:
        """Actualizar lugar"""
        place = await self.place_repository.find_by_id(place_id)
        if not place:
            return None

        if request.name:
            place.name = request.name
        if request.description:
            place.description = request.description
        if request.category:
            place.category = request.category
        if request.city:
            place.city = request.city
        if request.address is not None:
            place.address = request.address
        if request.latitude is not None:
            place.latitude = request.latitude
        if request.longitude is not None:
            place.longitude = request.longitude
        if request.rating is not None:
            place.rating = request.rating
        if request.status:
            place.status = request.status

        place.updated_at = datetime.utcnow()
        return await self.place_repository.update(place)

    async def delete_place(self, place_id: UUID) -> bool:
        """Eliminar lugar"""
        return await self.place_repository.delete(place_id)