import json
import os
from typing import List

import repo
from core.constants import NEW_SESSION_DIR, SESSIONS_DIR
from db.session import SessionLocal
from models import Session
from models.sessions import SessionStates

model = Session


class SessionRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def create(self, **kwargs):
        with self.get_session():
            self.model.get_or_create(**kwargs)

    def session_add_new(self):
        dir_list = os.listdir(NEW_SESSION_DIR)
        for item in dir_list:
            if item.split(".")[-1] == 'session':
                continue
            with open(f"{NEW_SESSION_DIR}/{item}") as f:
                json_data = json.load(f)
            with self.get_session():
                self.model.get_or_create(
                    phone=json_data['phone'], app_id=json_data["app_id"], app_hash=json_data["app_hash"],
                    country=repo.countries.get(1), state=SessionStates.wait
                )
            os.remove(f"{NEW_SESSION_DIR}/{item}")

    def get_count(self) -> int:
        with self.get_session():
            result = self.model.select().count()
        return result

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result

    def get_all(self) -> List[model]:
        with self.get_session():
            result = self.model.select().execute()
        return result

    def get_all_by_state(self, state: SessionStates) -> List[model]:
        with self.get_session():
            result = self.model.select().filter(state=state).execute()
        return result

    def get_dict(self, id: int) -> dict:
        session = self.get(id)
        return {
            "session": f"{SESSIONS_DIR}/{session.phone}", "api_id": session.app_id, "api_hash": session.app_hash
        }

    def move_state(self, session: Session, state: SessionStates):
        with self.get_session():
            session.state = state
            session.save()


sessions = SessionRepository()
