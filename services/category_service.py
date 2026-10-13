from sqlalchemy.orm import Session
from repositories.category_repo import CategoryRepository
from schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create_category(self, data: CategoryCreate):
        if self.repo.get_by_name(data.name):
            raise ValueError("Ya existe una categoría con ese nombre")
        return self.repo.create(data)

    def list_categories(self, paginate: bool = False, page: int = 1, page_size: int = 10):
        return self.repo.get_all(paginate=paginate, page=page, page_size=page_size)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def update_category(self, id: int, data: CategoryUpdate):
        return self.repo.update(id, data)

    def delete_category(self, id: int):
        return self.repo.delete(id)
