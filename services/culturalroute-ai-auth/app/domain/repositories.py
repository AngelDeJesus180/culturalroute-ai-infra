from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.models import User


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        pass