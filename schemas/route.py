from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.category import CategoryResponse

class RoutePointBase(BaseModel):
    name: str
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0
    order: Optional[int] = 0

class RoutePointCreate(RoutePointBase):
    pass

class RoutePointResponse(RoutePointBase):
    id: int
    route_id: int

    class Config:
        from_attributes = True


class RouteBase(BaseModel):
    title: str
    start: Optional[str] = None
    destination: Optional[str] = None
    description: Optional[str] = None
    distance_km: float
    duration_min: int
    fare: Optional[float] = 0.0
    category_id: Optional[int] = None

class RouteCreate(RouteBase):
    creator_id: Optional[int] = None
    category_name: Optional[str] = None
    stops: Optional[List[str]] = []
    points: Optional[List[RoutePointCreate]] = []

class RouteUpdate(BaseModel):
    title: Optional[str] = None
    start: Optional[str] = None
    destination: Optional[str] = None
    description: Optional[str] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    fare: Optional[float] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    stops: Optional[List[str]] = None
    points: Optional[List[RoutePointCreate]] = None

class RouteResponse(BaseModel):
    id: int
    title: str
    start: Optional[str] = None
    destination: Optional[str] = None
    description: Optional[str] = None
    distance_km: float
    duration_min: int
    fare: float
    rating: float
    created_at: Optional[datetime] = None
    category_id: int
    creator_id: int

    # Campos amigables y compatibles con el frontend
    category: Optional[str] = None
    creator_name: Optional[str] = None
    stops: List[str] = []
    points: List[RoutePointResponse] = []

    # Compatibilidad con los nombres exactos que usa el frontend en JS (camelCase)
    distanceKm: Optional[float] = None
    durationMin: Optional[int] = None
    creatorId: Optional[int] = None
    creatorName: Optional[str] = None
    createdAt: Optional[str] = None

    class Config:
        from_attributes = True
