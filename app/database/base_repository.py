#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


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
    def get_all(self, in_list: bool = None, **filters) -> List[ModelType]:
        if in_list:
            return [item for item in self.model.select().filter(**filters).order_by(self.model.id.asc()).execute()]
        return self.model.select().filter(**filters).order_by(self.model.id.asc()).execute()

    @db_manager
    def remove(self, id: int) -> None:
        self.model.delete().where(self.model.id == id).execute()

    @db_manager
    def update(self, db_obj: ModelType, **obj_in_data) -> ModelType:
        return self.model.update(**obj_in_data).where(self.model.id == db_obj.id).execute()

    @db_manager
    def count(self) -> int:
        return self.model.select().count()
