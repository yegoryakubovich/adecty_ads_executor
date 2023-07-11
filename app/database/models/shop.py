from peewee import PrimaryKeyField, CharField

from database.db import BaseModel


class Shop(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=32)
    link = CharField(max_length=128, null=True)

    class Meta:
        db_table = 'shops'
