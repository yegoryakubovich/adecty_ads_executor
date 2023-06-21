from db.session import SessionLocal
from models import all_models


def init_db() -> None:
    with SessionLocal:
        SessionLocal.create_tables(all_models)
