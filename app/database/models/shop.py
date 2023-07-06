from peewee import PrimaryKeyField, CharField

from database.db import BaseModel


class ShopTypes:
    session_shop = "session_shop"
    proxy_shop = "proxy_shop"
    common = "common"


class Shop(BaseModel):
    id = PrimaryKeyField()
    type = CharField(max_length=32, default=ShopTypes.common)
    name = CharField(max_length=32)
    link = CharField(max_length=128, null=True)

    class Meta:
        db_table = 'shops'
