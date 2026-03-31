from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models import User
from app.domain.repositories import UserRepository
from app.infrastructure.database import UserORM


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    async def save(self, user: User) -> User:
        user_orm = UserORM(
            id=str(user.id),
            username=user.username,
            password_hash=user.password_hash,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(user_orm)
        self.db.commit()
        return user

    async def find_by_username(self, username: str) -> Optional[User]:
        user_orm = self.db.query(UserORM).filter(UserORM.username == username.lower()).first()
        if not user_orm:
            return None
        return self._to_domain(user_orm)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        user_orm = self.db.query(UserORM).filter(UserORM.id == str(user_id)).first()
        if not user_orm:
            return None
        return self._to_domain(user_orm)

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        users_orm = self.db.query(UserORM).offset(skip).limit(limit).all()
        return [self._to_domain(u) for u in users_orm]

    async def delete(self, user_id: UUID) -> bool:
        user_orm = self.db.query(UserORM).filter(UserORM.id == str(user_id)).first()
        if user_orm:
            self.db.delete(user_orm)
            self.db.commit()
            return True
        return False

    def _to_domain(self, user_orm: UserORM) -> User:
        return User(
            id=UUID(user_orm.id),
            username=user_orm.username,
            password_hash=user_orm.password_hash,
            is_admin=user_orm.is_admin,
            is_active=user_orm.is_active,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at
        )