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


from database import repo, db_manager
from database.base_repository import BaseRepository
from database.models import Message, SessionStates, Session, Order, Group


class MessageRepository(BaseRepository):
    model = Message

    @db_manager
    def get_session_from_send_message(self, order: Order, group: Group) -> Session:
        all_session_free = repo.sessions.get_all(SessionStates.free)
        for session in all_session_free:
            if not self.model.get_or_none(order=order, group=group, session=session):
                return session
        print("HI")
        my_session = all_session_free[0]
        for session in all_session_free[1:]:
            pass


messages = MessageRepository(Message)
