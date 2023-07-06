from typing import TypeVar, Generic, Type, List, Optional

from database import db_manager
from database.db import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @db_manager
    def get(self, id: int) -> Optional[ModelType]:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_by(self, **filters) -> Optional[ModelType]:
        return self.model.get_or_none(**filters)

    @db_manager
    def get_last(self, **kwargs) -> Optional[ModelType]:
        return self.model.select().filter(**kwargs).order_by(self.model.id.desc()).get_or_none()

    @db_manager
    def create(self, **obj_in_data) -> ModelType:
        result, _ = self.model.get_or_create(**obj_in_data)
        return result

    @db_manager
    def get_all(self, **filters) -> List[ModelType]:
        return self.model.select().filter(**filters).execute()

    @db_manager
    def remove(self, id: int) -> None:
        self.model.delete().where(self.model.id == id).execute()

    @db_manager
    def update(self, db_obj: ModelType, **obj_in_data) -> ModelType:
        return self.model.update(**obj_in_data).where(self.model.id == db_obj.id).execute()

    @db_manager
    def count(self) -> int:
        return self.model.select().count()
