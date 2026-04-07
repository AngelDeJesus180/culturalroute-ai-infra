from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.models import Place


class PlaceRepository(ABC):

    @abstractmethod
    async def save(self, place: Place) -> Place:
        pass

    @abstractmethod
    async def find_by_id(self, place_id: UUID) -> Optional[Place]:
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Place]:
        pass

    @abstractmethod
    async def update(self, place: Place) -> Place:
        pass

    @abstractmethod
    async def delete(self, place_id: UUID) -> bool:
        pass