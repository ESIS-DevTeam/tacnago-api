from typing import List, TypeVar, Any
from urllib.parse import urlencode
from math import ceil
from schemas.pagination_schema import Paginate, PaginateLinks, PaginateMeta

T = TypeVar('T')

def create_paginated_response(
    items: List[T],
    total: int,
    page: int,
    page_size: int,
    base_url: str,
    path: str,
    query_params: dict = None
) -> Paginate[T]:
    last_page = ceil(total / page_size) if page_size > 0 else 1
    from_index = ((page - 1) * page_size) + 1 if total > 0 else 0
    to_index = min(page * page_size, total)
    
    if query_params is None:
        query_params = {}
    clean_params = {k: v for k, v in query_params.items() if v is not None}
    
    def build_url(page_num: int) -> str:
        params = {**clean_params, "page": page_num, "page_size": page_size}
        query_string = urlencode(params)
        return f"{base_url}{path}?{query_string}"
    
    links = PaginateLinks(
        first=build_url(1) if total > 0 else None,
        last=build_url(last_page) if total > 0 else None,
        next=build_url(page + 1) if page < last_page else None,
        prev=build_url(page - 1) if page > 1 else None
    )
    
    meta = PaginateMeta(
        current_page=page,
        from_=from_index,
        last_page=last_page,
        path=path,
        per_page=page_size,
        to=to_index,
        total=total
    )
    
    return Paginate(
        data=items,
        links=links,
        meta=meta
    )

def should_paginate(page: int = None, page_size: int = None) -> bool:
    return page is not None and page_size is not None
