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

from pyrogram import Client, types, errors

from database import repo
from database.models import Session, SessionStates


class ExecutorAction:
    def __init__(self, client: Client, session: Session):
        self.client = client
        self.session = session

    async def get_chat(self, chat_id: [str, int]) -> types.Chat:
        return await self.client.get_chat(chat_id=chat_id)

    async def join_chat(self, chat_id: [str, int]) -> types.Chat:
        return await self.client.join_chat(chat_id=chat_id)

    async def get_messages(self, chat_id: [str, int], msg_id: int) -> types.Message:
        return await self.client.get_messages(chat_id=chat_id, message_ids=msg_id)

    async def get_all_messages(self, chat_id: [str, int], limit: int = 0) -> List[types.Message]:
        return [message async for message in self.client.get_chat_history(chat_id=chat_id, limit=limit)]

    async def get_all_messages_ids(self, chat_id: [str, int], limit: int = 0) -> List[int]:
        return [message.id async for message in self.client.get_chat_history(chat_id=chat_id, limit=limit)]

    async def send_message(self, chat_id: [str, int], text: str, photo: str = None):
        try:
            if photo:
                return await self.client.send_photo(chat_id=chat_id, photo=photo, caption=text)
            else:
                return await self.client.send_message(chat_id=chat_id, text=text)
        except errors.UserBannedInChannel:
            repo.sessions.update(self.session, state=SessionStates.spam_block)
