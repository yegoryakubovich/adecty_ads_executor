from peewee import PrimaryKeyField, CharField

from database.db import BaseModel


class PersonalTypes:
    name = 'name'
    surname = 'surname'
    avatar = 'avatar'
    about = 'about'


class PersonalSex:
    man = 'man'
    woman = 'woman'
    unisex = 'unisex'


class Personal(BaseModel):
    id = PrimaryKeyField()
    type = CharField(max_length=64)
    sex = CharField(max_length=64, default=PersonalSex.unisex)
    value = CharField(max_length=512)

    class Meta:
        db_table = 'personals'
