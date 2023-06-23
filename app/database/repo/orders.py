from database import db_manager
from database.models import Order

model = Order


class OrderRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs):
        self.model.get_or_create(**kwargs)

    @db_manager
    def add_new_order(self):
        self.create(name="TEST1", text="n".join([]))

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_by_id(id)


orders = OrderRepository()
