from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from db.base import SessionLocal
from schemas.extra_schemas import (
    ReviewCreate, ReviewResponse,
    TravelHistoryCreate, TravelHistoryResponse,
    FollowerCreate, FollowerResponse,
    NotificationResponse
)
from services.extra_service import ExtraService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_extra_service(db: Session = Depends(get_db)) -> ExtraService:
    return ExtraService(db)

# --- Reviews ---
@router.post("/routes/{route_id}/reviews", response_model=ReviewResponse, tags=["Reseñas"])
def add_review(
    route_id: int,
    data: ReviewCreate,
    user_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    return service.add_review(route_id, user_id, data)

@router.get("/routes/{route_id}/reviews", response_model=List[ReviewResponse], tags=["Reseñas"])
def get_route_reviews(
    route_id: int,
    service: ExtraService = Depends(get_extra_service)
):
    return service.list_reviews(route_id)

# --- Travel History (Recorridas) ---
@router.post("/travel-history", response_model=TravelHistoryResponse, tags=["Historial de Viajes"])
def record_travel(
    data: TravelHistoryCreate,
    user_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    return service.complete_trip(user_id, data)

@router.get("/travel-history", response_model=List[TravelHistoryResponse], tags=["Historial de Viajes"])
def get_user_travel_history(
    user_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    return service.list_travel_history(user_id)

# --- Followers (Comunidad) ---
@router.post("/users/follow", tags=["Comunidad"])
def follow_user(
    data: FollowerCreate,
    follower_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    try:
        service.follow(follower_id, data.followed_id)
        return {"success": True, "detail": "Usuario seguido exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/unfollow/{followed_id}", tags=["Comunidad"])
def unfollow_user(
    followed_id: int,
    follower_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    success = service.unfollow(follower_id, followed_id)
    if not success:
        raise HTTPException(status_code=404, detail="No se encontró el seguimiento")
    return {"success": True, "detail": "Se dejó de seguir al usuario"}

# --- Notificaciones ---
@router.get("/notifications", response_model=List[NotificationResponse], tags=["Notificaciones"])
def get_notifications(
    user_id: int = Query(...),
    unread_only: bool = Query(False),
    service: ExtraService = Depends(get_extra_service)
):
    return service.list_notifications(user_id, unread_only=unread_only)

@router.patch("/notifications/{id}/read", response_model=NotificationResponse, tags=["Notificaciones"])
def mark_notification_as_read(
    id: int,
    user_id: int = Query(...),
    service: ExtraService = Depends(get_extra_service)
):
    n = service.mark_read(id, user_id)
    if not n:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return n
