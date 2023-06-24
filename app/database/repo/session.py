#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import List, Optional

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
                api_id=item["api_id"], api_hash=item["api_hash"], country=repo.countries.get_by_id(1)
            )

    @db_manager
    def get_count(self) -> int:
        return self.model.select().count()

    @db_manager
    def get_by_id(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def get_all_by_state(self, state: SessionStates) -> List[model]:
        return self.model.select().filter(state=state).execute()

    @db_manager
    def get_dict(self, id: int) -> dict:
        session = self.get_by_id(id)
        return {
            "session": f"{SESSIONS_DIR}/{session.phone}", "api_id": session.app_id, "api_hash": session.app_hash
        }


    @db_manager
    def move_state(self, session: Session, state: SessionStates):
        session.state = state
        session.save()


sessions = SessionRepository()
