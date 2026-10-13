from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, Union

from db.base import SessionLocal
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from schemas.pagination_schema import Paginate
from services.category_service import CategoryService
from utils.pagination import create_paginated_response, should_paginate

router = APIRouter(tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)

@router.post("/", response_model=CategoryResponse)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.create_category(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=Union[list[CategoryResponse], Paginate[CategoryResponse]])
def list_categories(
    request: Request,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    service: CategoryService = Depends(get_category_service)
):
    if should_paginate(page, page_size):
        items, total = service.list_categories(paginate=True, page=page, page_size=page_size)
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        path = str(request.url.path)
        return create_paginated_response(
            items=items, total=total, page=page, page_size=page_size,
            base_url=base_url, path=path, query_params={}
        )
    return service.list_categories(paginate=False)

@router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id(
    id: int,
    service: CategoryService = Depends(get_category_service)
):
    cat = service.get_by_id(id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat

@router.put("/{id}", response_model=CategoryResponse)
def update_category(
    id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    cat = service.update_category(id, data)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat

@router.delete("/{id}")
def delete_category(
    id: int,
    service: CategoryService = Depends(get_category_service)
):
    cat = service.delete_category(id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"detail": "Categoría eliminada"}
