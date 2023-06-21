from db.session import SessionLocal
from models import Order

model = Order


class OrderRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def add_new_order(self, ):
        with self.get_session():
            self.model.get_or_create(name="TEST1",
                                     text="n".join([]))

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result


orders = OrderRepository()
