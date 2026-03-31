from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from enum import Enum

class PlaceStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    INACTIVE = "inactive"

# Request schemas
class PlaceCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    address: Optional[str] = None
    latitude: float = 0
    longitude: float = 0

class PlaceUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    status: Optional[PlaceStatus] = None

# Response schemas
class PlaceResponse(BaseModel):
    id: UUID
    name: str
    description: str
    category: str
    city: str
    address: Optional[str]
    latitude: float
    longitude: float
    rating: float
    status: PlaceStatus
    source: str
    created_at: datetime
    updated_at: datetime

class PlaceListResponse(BaseModel):
    places: List[PlaceResponse]
    total: int