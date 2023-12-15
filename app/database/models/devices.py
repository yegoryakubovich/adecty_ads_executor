from peewee import PrimaryKeyField, CharField

from database.db import BaseModel


class Device(BaseModel):
    id = PrimaryKeyField()
    system_version = CharField(max_length=128)
    device_model = CharField(max_length=128)

    class Meta:
        db_table = 'devices'
