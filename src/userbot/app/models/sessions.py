from datetime import datetime

from peewee import PrimaryKeyField, BigIntegerField, CharField, DateTimeField, ForeignKeyField

from db.base_model import BaseModel
from models import Country


class SessionStates:
    wait = "wait"
    not_file = "not_file"
    check = "check"
    free = "free"
    in_work = "in_work"
    banned = "banned"


class Session(BaseModel):
    id = PrimaryKeyField()
    phone = CharField(max_length=32, unique=True)
    country = ForeignKeyField(Country, to_field='id')
    api_id = BigIntegerField()
    api_hash = CharField(max_length=256)
    telegram_id = BigIntegerField()
    string = CharField(max_length=512)

    state = CharField(max_length=64, default=SessionStates.wait)
    state_description = CharField(max_length=2056, null=True)
    created_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'sessions'
