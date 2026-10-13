from pydantic import BaseModel
from typing import Optional, List
from schemas.category import CategoryResponse

class RoutePointBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    order: int

class RoutePointCreate(RoutePointBase):
    pass

class RoutePointResponse(RoutePointBase):
    id: int
    route_id: int

    class Config:
        from_attributes = True


class RouteBase(BaseModel):
    title: str
    description: Optional[str] = None
    distance_km: float
    duration_min: int
    fare: Optional[float] = 0.0
    category_id: int

class RouteCreate(RouteBase):
    points: List[RoutePointCreate] = []

class RouteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    fare: Optional[float] = None
    category_id: Optional[int] = None

class RouteResponse(RouteBase):
    id: int
    rating: float
    creator_id: int
    category: Optional[CategoryResponse] = None
    points: List[RoutePointResponse] = []

    class Config:
        from_attributes = True
