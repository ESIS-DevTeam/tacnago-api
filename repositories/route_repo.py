from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_
from typing import Optional
from db.models.route import Route
from db.models.route_point import RoutePoint
from db.models.category import Category
from schemas.route import RouteCreate, RouteUpdate

class RouteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: RouteCreate, creator_id: int, category_id: int) -> Route:
        route = Route(
            title=data.title,
            start=data.start,
            destination=data.destination,
            description=data.description,
            distance_km=data.distance_km,
            duration_min=data.duration_min,
            fare=data.fare if data.fare is not None else 0.0,
            rating=0.0,
            category_id=category_id,
            creator_id=creator_id
        )
        self.db.add(route)
        self.db.flush()

        # Si vienen points estructurados
        if data.points:
            for pt in data.points:
                point = RoutePoint(
                    route_id=route.id,
                    name=pt.name,
                    latitude=pt.latitude,
                    longitude=pt.longitude,
                    order=pt.order
                )
                self.db.add(point)
        # Si vienen stops como strings
        elif data.stops:
            for idx, stop_name in enumerate(data.stops):
                point = RoutePoint(
                    route_id=route.id,
                    name=stop_name,
                    latitude=0.0,
                    longitude=0.0,
                    order=idx
                )
                self.db.add(point)

        self.db.commit()
        self.db.refresh(route)
        return route

    def get_all(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        creator_id: Optional[int] = None,
        paginate: bool = False,
        page: int = 1,
        page_size: int = 10
    ):
        query = (
            self.db.query(Route)
            .options(
                joinedload(Route.category),
                joinedload(Route.creator),
                selectinload(Route.points)
            )
        )

        if creator_id is not None:
            query = query.filter(Route.creator_id == creator_id)

        if category and category.lower() != "todas":
            query = query.join(Route.category).filter(Category.name.ilike(category))

        if search:
            s = f"%{search}%"
            query = query.filter(
                or_(
                    Route.title.ilike(s),
                    Route.start.ilike(s),
                    Route.destination.ilike(s),
                    Route.description.ilike(s)
                )
            )

        query = query.order_by(Route.created_at.desc())

        if not paginate:
            return query.all()

        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return items, total

    def get_by_id(self, id: int) -> Route:
        return (
            self.db.query(Route)
            .options(
                joinedload(Route.category),
                joinedload(Route.creator),
                selectinload(Route.points)
            )
            .filter(Route.id == id)
            .first()
        )

    def update(self, id: int, data: RouteUpdate, category_id: Optional[int] = None) -> Route:
        route = self.get_by_id(id)
        if not route:
            return None

        update_dict = data.model_dump(exclude_unset=True, exclude={"stops", "points", "category_name"})
        if category_id:
            update_dict["category_id"] = category_id

        for key, value in update_dict.items():
            setattr(route, key, value)

        # Actualizar paradas si se enviaron
        if data.points is not None:
            self.db.query(RoutePoint).filter(RoutePoint.route_id == route.id).delete()
            for pt in data.points:
                self.db.add(RoutePoint(
                    route_id=route.id,
                    name=pt.name,
                    latitude=pt.latitude,
                    longitude=pt.longitude,
                    order=pt.order
                ))
        elif data.stops is not None:
            self.db.query(RoutePoint).filter(RoutePoint.route_id == route.id).delete()
            for idx, stop_name in enumerate(data.stops):
                self.db.add(RoutePoint(
                    route_id=route.id,
                    name=stop_name,
                    latitude=0.0,
                    longitude=0.0,
                    order=idx
                ))

        self.db.commit()
        self.db.refresh(route)
        return route

    def delete(self, id: int) -> Route:
        route = self.get_by_id(id)
        if not route:
            return None
        self.db.delete(route)
        self.db.commit()
        return route
