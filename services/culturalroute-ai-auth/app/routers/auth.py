from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID

from app.infrastructure.database import get_db, init_db
from app.infrastructure.repositories import SQLAlchemyUserRepository
from app.application.auth_service import AuthService
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    LoginResponse,
    UserListResponse
)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    return AuthService(repository)


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        auth_service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user


@router.on_event("startup")
async def startup_event():
    init_db()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(
        request: UserRegisterRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """Registrar nuevo usuario (público)"""
    try:
        user = await auth_service.register(request)
        token = auth_service.create_access_token(user.id)

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                username=user.username,
                is_admin=user.is_admin,
                is_active=user.is_active,
                created_at=user.created_at
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(
        request: UserLoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """Iniciar sesión"""
    try:
        result = await auth_service.login(request)
        return LoginResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(
                id=result["user"].id,
                username=result["user"].username,
                is_admin=result["user"].is_admin,
                is_active=result["user"].is_active,
                created_at=result["user"].created_at
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user


@router.get("/users", response_model=UserListResponse)
async def list_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        current_user: UserResponse = Depends(get_current_user),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Listar usuarios (solo admin)"""
    try:
        users = await auth_service.get_users(skip, limit, current_user)
        return UserListResponse(
            users=[UserResponse(
                id=u.id,
                username=u.username,
                is_admin=u.is_admin,
                is_active=u.is_active,
                created_at=u.created_at
            ) for u in users],
            total=len(users)
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: str,
        current_user: UserResponse = Depends(get_current_user),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Eliminar usuario (solo admin)"""
    try:
        deleted = await auth_service.delete_user(UUID(user_id), current_user)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))