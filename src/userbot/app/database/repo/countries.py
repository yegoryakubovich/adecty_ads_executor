from database import db_manager
from database.models import Country

model = Country


class CountryRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_by_id(id)


countries = CountryRepository()
