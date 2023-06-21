from peewee import Model

from db.session import SessionLocal


class BaseModel(Model):
    class Meta:
        database = SessionLocal
