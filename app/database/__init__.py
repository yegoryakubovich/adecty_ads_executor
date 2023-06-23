from .db import db
from .db_manager import db_manager
from .models import models


@db_manager
def init_db() -> None:
    print("1")
    db.create_tables(models)
