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

from loguru import logger
from pyrogram import Client, types, errors
from pyrogram.errors import UsernameNotOccupied, InviteRequestSent

from database import repo
from database.models import Session, SessionStates, SessionProxy, Group, SessionGroup, GroupStates
from database.models.session_group import SessionGroupState
from functions.base_executor import BaseExecutorAction


class BotExecutorAction(BaseExecutorAction):
    def __init__(self, client: Client, session: Session):
        super().__init__()
        self.client = client
        self.session = session
        self.prefix = f"[EXECUTOR_{self.session.id}]"

    def logger(self, text: str):
        logger.info(f"{self.prefix} {text}")

    """USERBOT"""

    async def get_chat_by_group(self, group: Group) -> types.Chat:
        try:
            return await self.get_chat(chat_id=group.name)
        except KeyError:
            sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
        except UsernameNotOccupied:
            repo.groups.update(group, state=GroupStates.inactive)

    async def get_chat(self, chat_id: [str, int]) -> types.Chat:
        return await self.client.get_chat(chat_id=chat_id)

    async def join_chat_by_group(self, group: Group) -> types.Chat:
        try:
            return await self.join_chat(chat_id=group.name)
        except KeyError:
            sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
        except UsernameNotOccupied:
            repo.groups.update(group, state=GroupStates.inactive)
        except InviteRequestSent:
            self.logger(f"Запрос в группу {group.name} отправлен от сессии #{self.session}")

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
            return errors.UserBannedInChannel
        except errors.Forbidden:
            return errors.Forbidden

    async def get_chat_history(self, chat_id: [str, int], limit: int = 0):
        try:
            return [msg async for msg in self.client.get_chat_history(chat_id=chat_id, limit=limit)]
        except Exception as e:
            self.logger(f"get_chat_history\n {e}")

    """OTHER"""

    async def session_banned(self, new=False):
        session_shop = repo.shops.get(self.session.shop_id)
        if new:
            await self.new_session_banned_log(session_id=self.session.id,
                                              session_shop_id=session_shop.id, session_shop_name=session_shop.name, )
        else:
            sp: SessionProxy = repo.sessions_proxies.get_by(session=self.session)
            messages_send = len(repo.messages.get_all(session=self.session))
            proxy = None
            proxy_shop = None
            if sp:
                proxy = repo.proxies.get(sp.proxy_id)
                proxy_shop = repo.shops.get(proxy.shop_id)
            await self.session_banned_log(session_id=self.session.id, proxy_id=proxy.id if proxy else None,
                                          session_shop_id=session_shop.id, session_shop_name=session_shop.name,
                                          proxy_shop_id=proxy_shop.id if proxy else None,
                                          proxy_shop_name=proxy_shop.name,
                                          messages_send=messages_send)
            repo.sessions.update(self.session, messages_send=messages_send)

        for st in repo.sessions_tasks.get_all(session=self.session):
            repo.sessions_tasks.remove(st.id)
        for sp in repo.sessions_proxies.get_all(session=self.session):
            repo.sessions_proxies.remove(sp.id)
        for sg in repo.sessions_groups.get_all(session=self.session):
            repo.sessions_groups.remove(sg.id)
        for sleep in repo.sleeps.get_all(session=self.session):
            repo.sleeps.remove(sleep.id)

        repo.sessions.update(self.session, state=SessionStates.banned)
