from peewee import PrimaryKeyField, IntegerField, CharField, BooleanField

from db.base_model import BaseModel


class GroupStates:
    waiting = 'waiting'
    checking = 'checking'
    active = 'active'
    inactive = 'inactive'


class Group(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=128)
    state = CharField(max_length=32, default=GroupStates.waiting)

    subcribers = IntegerField()
    captcha_type = CharField(max_length=128)
    captcha_data = CharField(max_length=128)
    captcha_have = BooleanField(default=False)
    images_can = BooleanField(default=False)
    url_can = BooleanField(default=False)
    bigtext_can = BooleanField(default=False)

    class Meta:
        db_table = 'groups'
