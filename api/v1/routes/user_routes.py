from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, Union

from db.base import SessionLocal
from schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from schemas.pagination_schema import Paginate
from services.user_service import UserService
from utils.pagination import create_paginated_response, should_paginate

router = APIRouter(tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/register", response_model=UserResponse)
def register(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
def login(
    data: UserLogin,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.login(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/", response_model=Union[list[UserResponse], Paginate[UserResponse]])
def list_users(
    request: Request,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    service: UserService = Depends(get_user_service)
):
    if should_paginate(page, page_size):
        items, total = service.list_users(paginate=True, page=page, page_size=page_size)
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        path = str(request.url.path)
        return create_paginated_response(
            items=items, total=total, page=page, page_size=page_size,
            base_url=base_url, path=path, query_params={}
        )
    return service.list_users(paginate=False)

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(
    id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    user = service.update_user(id, data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.delete("/{id}")
def delete_user(
    id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.delete_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado"}
