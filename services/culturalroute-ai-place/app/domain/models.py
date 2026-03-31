from datetime import datetime
from dataclasses import dataclass
from uuid import UUID, uuid4
from enum import Enum

class PlaceStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    INACTIVE = "inactive"


@dataclass
class Place:
    id: UUID
    name: str
    description: str
    category: str
    city: str
    address: str
    latitude: float
    longitude: float
    rating: float
    status: PlaceStatus
    source: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            name: str,
            description: str,
            category: str,
            city: str,
            address: str,
            latitude: float = 0,
            longitude: float = 0,
            source: str = "manual"
    ) -> "Place":
        now = datetime.utcnow()
        return Place(
            id=uuid4(),
            name=name,
            description=description,
            category=category,
            city=city,
            address=address,
            latitude=latitude,
            longitude=longitude,
            rating=0,
            status=PlaceStatus.DRAFT,
            source=source,
            created_at=now,
            updated_at=now
        )

    def publish(self) -> None:
        self.status = PlaceStatus.PUBLISHED
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.status = PlaceStatus.INACTIVE
        self.updated_at = datetime.utcnow()