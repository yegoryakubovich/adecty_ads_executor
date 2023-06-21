from random import randint
from typing import List

import socks

from db.session import SessionLocal
from models import Country
from models.proxies import ProxyTypes

model = Country


class CountryRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result


countries = CountryRepository()
