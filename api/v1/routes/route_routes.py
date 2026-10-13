from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, Union

from db.base import SessionLocal
from schemas.route import RouteCreate, RouteUpdate, RouteResponse
from schemas.pagination_schema import Paginate
from services.route_service import RouteService
from utils.pagination import create_paginated_response, should_paginate

router = APIRouter(tags=["Rutas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_route_service(db: Session = Depends(get_db)) -> RouteService:
    return RouteService(db)

@router.post("/", response_model=RouteResponse)
def create_route(
    data: RouteCreate,
    creator_id: Optional[int] = Query(None),
    service: RouteService = Depends(get_route_service)
):
    try:
        return service.create_route(data, user_id=creator_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=Union[list[RouteResponse], Paginate[RouteResponse]])
def list_routes(
    request: Request,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    creator_id: Optional[int] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    service: RouteService = Depends(get_route_service)
):
    if should_paginate(page, page_size):
        items, total = service.list_routes(
            search=search, category=category, creator_id=creator_id,
            paginate=True, page=page, page_size=page_size
        )
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        path = str(request.url.path)
        params = {"search": search, "category": category, "creator_id": creator_id}
        return create_paginated_response(
            items=items, total=total, page=page, page_size=page_size,
            base_url=base_url, path=path, query_params=params
        )
    return service.list_routes(search=search, category=category, creator_id=creator_id, paginate=False)

@router.get("/{id}", response_model=RouteResponse)
def get_route_by_id(
    id: int,
    service: RouteService = Depends(get_route_service)
):
    route = service.get_by_id(id)
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return route

@router.put("/{id}", response_model=RouteResponse)
def update_route(
    id: int,
    data: RouteUpdate,
    user_id: Optional[int] = Query(None),
    service: RouteService = Depends(get_route_service)
):
    try:
        route = service.update_route(id, data, user_id=user_id)
        if not route:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return route
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
def delete_route(
    id: int,
    user_id: Optional[int] = Query(None),
    service: RouteService = Depends(get_route_service)
):
    try:
        route = service.delete_route(id, user_id=user_id)
        if not route:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return {"success": True, "id": id}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
