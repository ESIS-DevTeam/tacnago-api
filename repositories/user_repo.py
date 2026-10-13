from sqlalchemy.orm import Session
from db.models.user import User
from schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=data.email,
            password=data.password,
            avatar=data.avatar,
            bio=data.bio
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self, paginate: bool = False, page: int = 1, page_size: int = 10):
        query = self.db.query(User)
        if not paginate:
            return query.all()
        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return items, total

    def get_by_id(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def update(self, id: int, data: UserUpdate) -> User:
        user = self.get_by_id(id)
        if not user:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, id: int) -> User:
        user = self.get_by_id(id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
