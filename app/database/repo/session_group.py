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
from typing import List

from database import db_manager
from database.models import SessionGroup, Session, Group

model = SessionGroup


class SessionGroupRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs):
        return self.model.get_or_create(**kwargs)

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
    def delete_by_session(self, session: Session):
        self.model.delete().where(self.model.session == session).execute()

    @db_manager
    def check_subscribe(self, session: Session, group: Group) -> bool:
        if self.model.select().where(self.model.session == session, self.model.group == group).execute():
            return True
        return False


sessions_groups = SessionGroupRepository()
