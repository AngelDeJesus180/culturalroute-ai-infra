from uuid import UUID
from typing import Optional, List
import hashlib
import hmac
import base64
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from app.domain.models import User
from app.domain.repositories import UserRepository
from app.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.infrastructure.rabbitmq import rabbitmq

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mi-clave-secreta-super-segura-cambiar-en-produccion-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def hash_password(self, password: str) -> str:
        """Hash de contraseña usando SHA256 en lugar de bcrypt (más simple y sin límite de 72 bytes)"""
        salt = SECRET_KEY[:16]  # Usar parte de la clave secreta como salt
        salted_password = salt + password
        hash_bytes = hashlib.sha256(salted_password.encode('utf-8')).digest()
        return base64.b64encode(hash_bytes).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña - soporte para texto plano (para admin inicial)"""
        # Si el hash es texto plano (menos de 32 caracteres), comparar directamente
        if len(hashed_password) < 32:
            return plain_password == hashed_password

        # Si no, usar hash normal
        salt = SECRET_KEY[:16]
        salted_password = salt + plain_password
        hash_bytes = hashlib.sha256(salted_password.encode('utf-8')).digest()
        computed_hash = base64.b64encode(hash_bytes).decode('utf-8')
        return hmac.compare_digest(computed_hash, hashed_password)

    def create_access_token(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def register(self, request: UserRegisterRequest) -> User:
        """Registro público - todos son usuarios normales"""
        existing = await self.user_repository.find_by_username(request.username)
        if existing:
            raise ValueError("Username already exists")

        password_hash = self.hash_password(request.password)
        user = User.create(
            username=request.username,
            password_hash=password_hash
        )

        result = await self.user_repository.save(user)

        # Enviar evento a RabbitMQ (solo esto es nuevo)
        try:
            from app.infrastructure.rabbitmq import rabbitmq
            from datetime import datetime

            rabbitmq.publish('user_registered', {
                'user_id': str(result.id),
                'username': result.username,
                'is_admin': result.is_admin,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            print(f"⚠️ Error enviando mensaje a RabbitMQ: {e}")

        return result

    async def login(self, request: UserLoginRequest) -> dict:
        user = await self.user_repository.find_by_username(request.username)
        if not user:
            raise ValueError("Invalid credentials")

        if not self.verify_password(request.password, user.password_hash):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User is inactive")

        token = self.create_access_token(user.id)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    async def get_current_user(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = UUID(payload.get("sub"))
            return await self.user_repository.find_by_id(user_id)
        except (JWTError, ValueError):
            return None

    async def get_users(self, skip: int = 0, limit: int = 100, current_user: Optional[User] = None) -> List[User]:
        if not current_user or not current_user.is_admin:
            raise ValueError("Only admin can list users")
        return await self.user_repository.find_all(skip, limit)

    async def delete_user(self, user_id: UUID, current_user: Optional[User] = None) -> bool:
        if not current_user or not current_user.is_admin:
            raise ValueError("Only admin can delete users")
        return await self.user_repository.delete(user_id)