from peewee import PrimaryKeyField, ForeignKeyField

from db.base_model import BaseModel
from models import Group, Country


class GroupCountry(BaseModel):
    id = PrimaryKeyField()
    group = ForeignKeyField(Group, to_field='id')
    country = ForeignKeyField(Country, to_field='id')

    class Meta:
        db_table = 'groups_countries'
