from peewee import PrimaryKeyField, CharField

from db.base_model import BaseModel


class Tag(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=64)

    class Meta:
        db_table = 'tags'
