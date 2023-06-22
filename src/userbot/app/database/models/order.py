from peewee import PrimaryKeyField, CharField, DateTimeField

from database.db import BaseModel


class OrderStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"


class Order(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=128)
    message = CharField(max_length=256)

    state = CharField(max_length=32, default=OrderStates.wait)
    datetime_stop = DateTimeField()

    class Meta:
        db_table = 'orders'
