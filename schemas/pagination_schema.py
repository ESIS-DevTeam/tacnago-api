from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginateLinks(BaseModel):
    first: Optional[str] = None
    last: Optional[str] = None
    next: Optional[str] = None
    prev: Optional[str] = None

class PaginateMeta(BaseModel):
    current_page: int
    from_: int = Field(default=0, serialization_alias='from')
    last_page: int
    path: str
    per_page: int
    to: int
    total: int

    class Config:
        populate_by_name = True

class Paginate(BaseModel, Generic[T]):
    data: list[T]
    links: PaginateLinks
    meta: PaginateMeta
