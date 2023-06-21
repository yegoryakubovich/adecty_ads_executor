from core.constants import groups_list
from db.session import SessionLocal
from models import Group

model = Group


class GroupRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def add_new_group(self, ):
        for item in groups_list:
            if item.count("@"):
                item = item[1:]
            with self.get_session():
                self.model.get_or_create(name=item)

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result


groups = GroupRepository()
