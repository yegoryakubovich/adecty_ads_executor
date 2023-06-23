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
from datetime import datetime, timedelta

from core.constants import DAY_OLD
from database import db_manager, repo
from database.models import Message, SessionStates, Session, Order, Group

model = Message


class MessageRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs) -> model:
        return self.model.create(**kwargs)

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_by(self, **kwargs) -> model:
        print(kwargs)
        return self.model.get_or_none(**kwargs)

    @db_manager
    def get_by_group(self, order_id, group_id: int, days_old: int = DAY_OLD) -> model:
        return self.model.select().filter(
            self.model.order == repo.orders.get(order_id),
            self.model.group == repo.groups.get(group_id),
            self.model.created <= datetime.utcnow() - timedelta(days=days_old)
        ).execute()

    @db_manager
    def get_session_from_send_message(self, order: Order, group: Group) -> Session:
        all_session_free = repo.sessions.get_all_by_state(SessionStates.free)
        for session in all_session_free:
            if not self.get_by(order=order, group=group, session=session):
                return session
        print("HI")
        my_session = all_session_free[0]
        for session in all_session_free[1:]:
            pass


messages = MessageRepository()
