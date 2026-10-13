from sqlalchemy.orm import Session
from typing import Optional
from repositories.route_repo import RouteRepository
from repositories.category_repo import CategoryRepository
from repositories.user_repo import UserRepository
from schemas.route import RouteCreate, RouteUpdate, RouteResponse, RoutePointResponse

class RouteService:
    def __init__(self, db: Session):
        self.repo = RouteRepository(db)
        self.category_repo = CategoryRepository(db)
        self.user_repo = UserRepository(db)
        self.db = db

    def create_route(self, data: RouteCreate, user_id: Optional[int] = None):
        creator_id = user_id or data.creator_id
        if not creator_id:
            raise ValueError("No se indicó el creador de la ruta.")

        creator = self.user_repo.get_by_id(creator_id)
        if not creator:
            raise ValueError("No se encontró al creador de la ruta.")

        category_id = data.category_id
        if not category_id and data.category_name:
            cat = self.category_repo.get_by_name(data.category_name)
            if not cat:
                # Crear categoría automática si no existe
                cat = self.category_repo.create(type("Cat", (), {"model_dump": lambda s: {"name": data.category_name, "description": None}})())
            category_id = cat.id

        if not category_id:
            # Categoría por defecto
            cat = self.category_repo.get_by_name("Transporte")
            if not cat:
                cat = self.category_repo.create(type("Cat", (), {"model_dump": lambda s: {"name": "Transporte", "description": None}})())
            category_id = cat.id

        # Si no se definieron start o destination pero hay stops o points
        if not data.start:
            if data.stops:
                data.start = data.stops[0]
            elif data.points:
                data.start = data.points[0].name

        if not data.destination:
            if data.stops:
                data.destination = data.stops[-1]
            elif data.points:
                data.destination = data.points[-1].name

        route = self.repo.create(data, creator_id=creator_id, category_id=category_id)
        return self._format_route_response(route)

    def list_routes(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        creator_id: Optional[int] = None,
        paginate: bool = False,
        page: int = 1,
        page_size: int = 10
    ):
        if paginate:
            routes, total = self.repo.get_all(
                search=search, category=category, creator_id=creator_id,
                paginate=True, page=page, page_size=page_size
            )
            return [self._format_route_response(r) for r in routes], total

        routes = self.repo.get_all(
            search=search, category=category, creator_id=creator_id, paginate=False
        )
        return [self._format_route_response(r) for r in routes]

    def get_by_id(self, id: int):
        route = self.repo.get_by_id(id)
        if not route:
            return None
        return self._format_route_response(route)

    def update_route(self, id: int, data: RouteUpdate, user_id: Optional[int] = None):
        route = self.repo.get_by_id(id)
        if not route:
            return None

        if user_id and route.creator_id != user_id:
            raise PermissionError("No puedes editar una ruta de otro usuario.")

        category_id = data.category_id
        if not category_id and data.category_name:
            cat = self.category_repo.get_by_name(data.category_name)
            if cat:
                category_id = cat.id

        updated = self.repo.update(id, data, category_id=category_id)
        return self._format_route_response(updated)

    def delete_route(self, id: int, user_id: Optional[int] = None):
        route = self.repo.get_by_id(id)
        if not route:
            return None

        if user_id and route.creator_id != user_id:
            raise PermissionError("No puedes eliminar una ruta de otro usuario.")

        deleted = self.repo.delete(id)
        return deleted

    def _format_route_response(self, route) -> RouteResponse:
        points_resp = [
            RoutePointResponse(
                id=pt.id,
                route_id=pt.route_id,
                name=pt.name,
                latitude=pt.latitude,
                longitude=pt.longitude,
                order=pt.order
            )
            for pt in (route.points or [])
        ]
        stops_list = [pt.name for pt in (route.points or [])]
        if not stops_list:
            if route.start and route.destination:
                stops_list = [route.start, route.destination]

        category_name = route.category.name if route.category else "General"
        creator_name = route.creator.name if route.creator else "Usuario"

        created_at_str = route.created_at.strftime("%Y-%m-%d") if route.created_at else None

        return RouteResponse(
            id=route.id,
            title=route.title,
            start=route.start or (stops_list[0] if stops_list else ""),
            destination=route.destination or (stops_list[-1] if stops_list else ""),
            description=route.description,
            distance_km=route.distance_km,
            duration_min=route.duration_min,
            fare=route.fare or 0.0,
            rating=route.rating or 0.0,
            created_at=route.created_at,
            category_id=route.category_id,
            creator_id=route.creator_id,
            category=category_name,
            creator_name=creator_name,
            stops=stops_list,
            points=points_resp,
            # Dual props para frontend
            distanceKm=route.distance_km,
            durationMin=route.duration_min,
            creatorId=route.creator_id,
            creatorName=creator_name,
            createdAt=created_at_str
        )
