from peewee import PrimaryKeyField, CharField

from database.db import BaseModel


class DeviceTypes:
    app_version = 'app_version'
    device = 'device'
    avatar = 'avatar'
    about = 'about'


class Device(BaseModel):
    id = PrimaryKeyField()
    app_version = CharField(max_length=128)
    device_model = CharField(max_length=128)

    class Meta:
        db_table = 'devices'
