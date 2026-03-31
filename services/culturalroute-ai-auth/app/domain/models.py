from datetime import datetime
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID
    username: str
    password_hash: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(username: str, password_hash: str) -> "User":
        now = datetime.utcnow()
        return User(
            id=uuid4(),
            username=username.lower(),
            password_hash=password_hash,
            is_admin=False,
            is_active=True,
            created_at=now,
            updated_at=now
        )