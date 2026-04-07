from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models import Place, PlaceStatus
from app.domain.repositories import PlaceRepository
from app.infrastructure.database import PlaceORM, PlaceStatusDB


class SQLAlchemyPlaceRepository(PlaceRepository):

    def __init__(self, db: Session):
        self.db = db

    async def save(self, place: Place) -> Place:
        place_orm = PlaceORM(
            id=str(place.id),
            name=place.name,
            description=place.description,
            category=place.category,
            city=place.city,
            address=place.address,
            latitude=place.latitude,
            longitude=place.longitude,
            rating=place.rating,
            status=PlaceStatusDB(place.status.value),
            source=place.source,
            created_at=place.created_at,
            updated_at=place.updated_at
        )
        self.db.add(place_orm)
        self.db.commit()
        return place

    async def find_by_id(self, place_id: UUID) -> Optional[Place]:
        place_orm = self.db.query(PlaceORM).filter(PlaceORM.id == str(place_id)).first()
        if not place_orm:
            return None
        return self._to_domain(place_orm)

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Place]:
        try:
            places_orm = self.db.query(PlaceORM).offset(skip).limit(limit).all()
            return [self._to_domain(p) for p in places_orm]
        except Exception as e:
            print(f"Error en find_all: {e}")
            return []

    async def update(self, place: Place) -> Place:
        place_orm = self.db.query(PlaceORM).filter(PlaceORM.id == str(place.id)).first()
        if place_orm:
            place_orm.name = place.name
            place_orm.description = place.description
            place_orm.category = place.category
            place_orm.city = place.city
            place_orm.address = place.address
            place_orm.latitude = place.latitude
            place_orm.longitude = place.longitude
            place_orm.rating = place.rating
            place_orm.status = PlaceStatusDB(place.status.value)
            place_orm.updated_at = place.updated_at
            self.db.commit()
            self.db.refresh(place_orm)
        return place

    async def delete(self, place_id: UUID) -> bool:
        place_orm = self.db.query(PlaceORM).filter(PlaceORM.id == str(place_id)).first()
        if place_orm:
            self.db.delete(place_orm)
            self.db.commit()
            return True
        return False

    def _to_domain(self, place_orm: PlaceORM) -> Place:
        # Convertir status a minúsculas
        status_value = place_orm.status.lower() if place_orm.status else "draft"
        return Place(
            id=UUID(place_orm.id),
            name=place_orm.name,
            description=place_orm.description,
            category=place_orm.category,
            city=place_orm.city,
            address=place_orm.address,
            latitude=float(place_orm.latitude) if place_orm.latitude else 0,
            longitude=float(place_orm.longitude) if place_orm.longitude else 0,
            rating=float(place_orm.rating) if place_orm.rating else 0,
            status=PlaceStatus(status_value),
            source=place_orm.source,
            created_at=place_orm.created_at,
            updated_at=place_orm.updated_at
        )




