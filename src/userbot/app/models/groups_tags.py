from peewee import PrimaryKeyField, ForeignKeyField

from db.base_model import BaseModel
from models import Group, Tag


class GroupTag(BaseModel):
    id = PrimaryKeyField()
    group = ForeignKeyField(Group, to_field='id')
    tag = ForeignKeyField(Tag, to_field='id')

    class Meta:
        db_table = 'groups_tags'
