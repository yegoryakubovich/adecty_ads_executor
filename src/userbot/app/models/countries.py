from peewee import PrimaryKeyField, CharField

from db.base_model import BaseModel


class Country(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=128)

    class Meta:
        db_table = 'countries'
