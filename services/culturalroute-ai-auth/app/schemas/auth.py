from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

# Request schemas
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)

class UserLoginRequest(BaseModel):
    username: str
    password: str

# Response schemas
class UserResponse(BaseModel):
    id: UUID
    username: str
    is_admin: bool
    is_active: bool
    created_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int