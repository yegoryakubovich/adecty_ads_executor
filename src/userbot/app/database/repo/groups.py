
from core.constants import groups_list
from database import db_manager
from database.models import Group

model = Group


class GroupRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def add_new_group(self, ):
        for item in groups_list:
            if item.count("@"):
                item = item[1:]
            self.model.get_or_create(name=item)

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_by_id(id)


groups = GroupRepository()
