from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    route_id: int

class ReviewCreate(ReviewBase):
    user_id: Optional[int] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    user_name: Optional[str] = None

    class Config:
        from_attributes = True


class TravelHistoryBase(BaseModel):
    route_id: Optional[int] = None
    fare: Optional[float] = None

class TravelHistoryCreate(TravelHistoryBase):
    user_id: Optional[int] = None

class TravelHistoryResponse(TravelHistoryBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    route_title: Optional[str] = None

    class Config:
        from_attributes = True


class FollowerCreate(BaseModel):
    followed_id: int

class FollowerResponse(BaseModel):
    id: int
    follower_id: int
    followed_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    title: str
    message: str
    route_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
