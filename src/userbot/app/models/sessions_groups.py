from peewee import PrimaryKeyField, ForeignKeyField

from db.base_model import BaseModel
from models import Session, Group


class SessionGroup(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id')
    group = ForeignKeyField(Group, to_field='id')

    class Meta:
        db_table = 'sessions_groups'
