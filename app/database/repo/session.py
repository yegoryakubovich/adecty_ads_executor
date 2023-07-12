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
from core.constants import MAX_TASKS_COUNT
from core.default_data import sessions_list
from database import repo, db_manager
from database.base_repository import BaseRepository
from database.models import Session, SessionStates, Group
from database.models.session_task import SessionTaskType, SessionTaskStates
from utils.country import get_by_phone


class SessionRepository(BaseRepository):

    @db_manager
    def fill(self):
        for session in sessions_list:
            item = sessions_list[session]
            country_type = get_by_phone(item["phone"])
            country = repo.countries.create(code=country_type.code, name=country_type.name)
            shop = repo.shops.get(1)
            self.create(
                phone=item["phone"], tg_user_id=item["user_id"], string=item["string_session"],
                api_id=item["api_id"], api_hash=item["api_hash"], country=country, shop=shop
            )

    @db_manager
    def get_free(self, group: Group = None) -> Session:
        for session in self.get_all(state=SessionStates.free):
            if group:
                if repo.sessions_groups.get_by(session=session, group=group):
                    continue
            tasks = []
            for task in repo.sessions_tasks.get_all(session=session, state=SessionTaskStates.enable):
                if not task.type == SessionTaskType.check_message:
                    tasks.append(task)
            if len(tasks) >= MAX_TASKS_COUNT:
                continue
            return session

    def to_check(self, session: Session):
        session.state = SessionStates.waiting
        repo.sessions_tasks.delete_by_session(session)
        repo.sessions_proxies.delete_by_session(session)
        repo.sessions_groups.delete_by_session(session)
        session.save()


sessions = SessionRepository(Session)
