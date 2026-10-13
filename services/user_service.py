from sqlalchemy.orm import Session
from repositories.user_repo import UserRepository
from schemas.user import UserCreate, UserUpdate, UserLogin, UserResponse
from db.models.route import Route
from db.models.travel_history import TravelHistory

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def register(self, data: UserCreate):
        if self.repo.get_by_email(data.email):
            raise ValueError("Este correo ya está registrado.")
        user = self.repo.create(data)
        return self._format_user_response(user)

    def login(self, data: UserLogin):
        user = self.repo.get_by_email(data.email)
        if not user or user.password != data.password:
            raise ValueError("Correo o contraseña incorrectos.")
        return self._format_user_response(user)

    def list_users(self, paginate: bool = False, page: int = 1, page_size: int = 10):
        if paginate:
            users, total = self.repo.get_all(paginate=True, page=page, page_size=page_size)
            return [self._format_user_response(u) for u in users], total
        users = self.repo.get_all(paginate=False)
        return [self._format_user_response(u) for u in users]

    def get_by_id(self, id: int):
        user = self.repo.get_by_id(id)
        if not user:
            return None
        return self._format_user_response(user)

    def update_user(self, id: int, data: UserUpdate):
        user = self.repo.update(id, data)
        if not user:
            return None
        return self._format_user_response(user)

    def delete_user(self, id: int):
        return self.repo.delete(id)

    def _format_user_response(self, user) -> UserResponse:
        created_count = self.db.query(Route).filter(Route.creator_id == user.id).count()
        trips_count = self.db.query(TravelHistory).filter(TravelHistory.user_id == user.id).count()
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar,
            bio=user.bio,
            is_active=user.is_active,
            created_routes=created_count,
            completed_trips=trips_count
        )
