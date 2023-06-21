from peewee import PrimaryKeyField, ForeignKeyField

from db.base_model import BaseModel
from models import Session, Proxy


class SessionProxy(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id', on_delete='CASCADE')
    proxy = ForeignKeyField(Proxy, to_field='id', on_delete='CASCADE')

    class Meta:
        db_table = 'session_proxy'
