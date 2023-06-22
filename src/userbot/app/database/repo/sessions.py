from typing import List


from core.constants import SESSIONS_DIR, strings
from database import db_manager, repo
from database.models import Session, SessionStates

model = Session


class SessionRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs):
        self.model.get_or_create(**kwargs)

    @db_manager
    def session_add_new(self):
        for session in strings:
            item = strings[session]
            self.model.get_or_create(
                phone=item["phone"], tg_user_id=item["user_id"], string=item["string_session"],
                api_id=item["api_id"], api_hash=item["api_hash"], country=repo.countries.get(1)
            )

    @db_manager
    def get_count(self) -> int:
        return self.model.select().count()

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_by_id(id)

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def get_all_by_state(self, state: SessionStates) -> List[model]:
        return self.model.select().filter(state=state).execute()

    @db_manager
    def get_dict(self, id: int) -> dict:
        session = self.get(id)
        return {
            "session": f"{SESSIONS_DIR}/{session.phone}", "api_id": session.app_id, "api_hash": session.app_hash
        }

    @db_manager
    def move_state(self, session: Session, state: SessionStates):
        session.state = state
        session.save()


sessions = SessionRepository()
