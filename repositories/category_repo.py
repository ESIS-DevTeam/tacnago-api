from sqlalchemy.orm import Session
from db.models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_all(self, paginate: bool = False, page: int = 1, page_size: int = 10):
        query = self.db.query(Category)
        if not paginate:
            return query.all()
        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return items, total

    def get_by_id(self, id: int) -> Category:
        return self.db.query(Category).filter(Category.id == id).first()

    def get_by_name(self, name: str) -> Category:
        return self.db.query(Category).filter(Category.name.ilike(name)).first()

    def update(self, id: int, data: CategoryUpdate) -> Category:
        category = self.get_by_id(id)
        if not category:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, id: int) -> Category:
        category = self.get_by_id(id)
        if not category:
            return None
        self.db.delete(category)
        self.db.commit()
        return category
