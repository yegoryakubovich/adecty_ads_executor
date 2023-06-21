from peewee import PrimaryKeyField, IntegerField, CharField, ForeignKeyField

from db.base_model import BaseModel
from models import Country


class ProxyTypes:
    http = "http"
    socks5 = "socks5"


class ProxyStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"


class Proxy(BaseModel):
    id = PrimaryKeyField()
    type = CharField(max_length=128)
    host = CharField(max_length=32)
    port = IntegerField()
    user = CharField(max_length=128)
    password = CharField(max_length=256)
    country = ForeignKeyField(Country, to_field='id')

    state = CharField(max_length=32, default=ProxyStates.wait)
    state_description = CharField(max_length=32)

    class Meta:
        db_table = 'proxies'
