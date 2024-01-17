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

from database import repo
from database.models import Session, SessionStates, SessionProxy, Group, SessionGroup, GroupStates, User, \
    SessionGroupState
from functions import BaseExecutorAction


class BotExecutorAction(BaseExecutorAction):
    def __init__(self, client: Client, session: Session):
        super().__init__()
        self.client = client
        self.session = session
        self.prefix = f"[EXECUTOR_{self.session.id}]"
        self.started = False

    def logger(self, text: str):
        logger.info(f"{self.prefix} {text}")

    async def start_session(self):
        if self.started:
            return False
        try:
            await self.client.start()
            self.started = True
            return True
        except (
                errors.SessionExpired, errors.SessionRevoked, errors.UserDeactivated, errors.UserDeactivatedBan,
                errors.AuthKeyUnregistered, errors.AuthKeyDuplicated, errors.InputUserDeactivated
        ) as e:
            await self.session_banned()
            return False

    async def stop_session(self):
        if not self.started:
            return
        await self.client.stop()
        self.started = False

    """USERBOT"""

    async def get_chat_by_group(self, group: Group) -> [types.Chat, str]:
        try:
            return await self.get_chat(chat_id=group.name)
        except KeyError as ke:
            logger.info(f"KEY ERROR: {ke}")
            sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)
            if not sg:
                sg = repo.sessions_groups.create(session=self.session, group=group)
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            return "BanInGroup"
        except errors.UsernameNotOccupied:
            repo.groups.update(group, state=GroupStates.inactive)
            return "UsernameNotOccupied"
        except errors.UsernameInvalid:
            repo.groups.update(group, state=GroupStates.inactive)
            return "UsernameInvalid"

    async def get_chat(self, chat_id: [str, int]) -> types.Chat:
        result = await self.client.get_chat(chat_id=chat_id)

        return result

    async def get_users(self, user_id: [str, int]) -> [types.User, None]:
        try:
            result = await self.client.get_users(user_ids=user_id)
            return result
        except errors.UsernameNotOccupied:
            return "UsernameNotOccupied"
        except errors.UsernameInvalid:
            return "UsernameInvalid"
        except IndexError:
            return "IndexError"

    async def join_chat_by_group(self, group: Group) -> [types.Chat, str]:
        try:
            return await self.join_chat(chat_id=group.name)
        except KeyError as e:
            self.logger(str(e))
            sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)
            if sg:
                repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            else:
                repo.sessions_groups.create(session=self.session, group=group, state=SessionGroupState.banned)
            return "BanInGroup"
        except errors.UsernameNotOccupied:
            return "UsernameNotOccupied"
        except errors.InviteRequestSent:
            repo.groups.update(group, join_request=True)
            return "InviteRequestSent"
        except errors.ChatInvalid:
            return "ChatInvalid"
        except errors.ChannelInvalid:
            return "ChannelInvalid"
        except errors.UsernameInvalid:
            return "UsernameInvalid"

    async def join_chat_by_username(self, username: str) -> [types.Chat, str]:
        try:
            return await self.join_chat(chat_id=username)
        except KeyError as e:
            self.logger(str(e))
            return "BanInGroup"
        except errors.UsernameNotOccupied:
            return "UsernameNotOccupied"
        except errors.InviteRequestSent:
            return "InviteRequestSent"
        except errors.ChatInvalid:
            return "ChatInvalid"
        except errors.ChannelInvalid:
            return "ChannelInvalid"
        except errors.UserAlreadyParticipant:
            return self.get_chat(chat_id=username)

    async def join_chat(self, chat_id: [str, int]) -> [types.Chat, str]:
        result = await self.client.join_chat(chat_id=chat_id)
        return result

    async def get_messages(self, chat_id: [str, int], msg_id: int) -> types.Message:
        result = await self.client.get_messages(chat_id=chat_id, message_ids=msg_id)
        return result

    async def get_all_messages(self, chat_id: [str, int], limit: int = 0) -> List[types.Message]:
        result = [message async for message in self.client.get_chat_history(chat_id=chat_id, limit=limit)]
        return result

    async def get_all_messages_ids(self, chat_id: [str, int], limit: int = 0) -> List[int]:
        result = [message.id async for message in self.client.get_chat_history(chat_id=chat_id, limit=limit)]
        return result

    async def send_message(self, chat_id: [str, int], text: str = None, photo: str = None) -> [types.Message, str]:
        try:
            if photo:
                result = await self.client.send_photo(chat_id=chat_id, photo=photo, caption=text)
                return result
            else:
                result = await self.client.send_message(chat_id=chat_id, text=text)
                return result
        except errors.ChatAdminRequired:
            return "ChatAdminRequired"
        except errors.UserBannedInChannel:
            return "UserBannedInChannel"
        except errors.Forbidden:
            return "Forbidden"
        except errors.PeerFlood:
            return "PeerFlood"
        except errors.UsernameNotOccupied:
            return "UsernameNotOccupied"
        except errors.BadRequest:
            return "BadRequest"
        except errors.SlowmodeWait:
            return "SlowmodeWait"


    async def get_chat_history(self, chat_id: [str, int], limit: int = 0) -> list:
        try:
            result = [msg async for msg in self.client.get_chat_history(chat_id=chat_id, limit=limit)]
            return result
        except Exception as e:
            self.logger(f"get_chat_history\n {e}")

    async def update_profile(self, name=None, surname=None, about=None):
        result = await self.client.update_profile(first_name=name, last_name=surname, bio=about)
        return result

    async def update_profile_photo(self, photo=None):
        result = await self.client.set_profile_photo(photo=photo)
        return result

    """OTHER"""

    async def session_banned(self, new=False):
        self.logger("session_banned")
        session_shop = repo.shops.get(self.session.shop_id)
        if new:
            await self.new_session_banned_log(session=self.session, session_shop=session_shop)
        else:
            sp: SessionProxy = repo.sessions_proxies.get_by(session=self.session)
            messages_send = len(repo.messages.get_all(session=self.session))
            proxy = None
            proxy_shop = None
            if sp:
                proxy = repo.proxies.get(sp.proxy_id)
                repo.proxies.update(proxy, ban_count=proxy.ban_count + 1)
                proxy_shop = repo.shops.get(proxy.shop_id)
            so = repo.sessions_orders.get_by(session=self.session)
            order = repo.orders.get(id=so.order_id)
            await self.session_banned_log(
                session=self.session,
                session_shop=session_shop,
                proxy=proxy if proxy else None,
                proxy_shop=proxy_shop if proxy else None,
                order=order,
                messages_send=messages_send
            )

        for sgroup in repo.sessions_groups.get_all(session=self.session):
            repo.sessions_groups.remove(sgroup.id)
        for sorder in repo.sessions_orders.get_all(session=self.session):
            repo.sessions_orders.remove(sorder.id)
        for spersonal in repo.sessions_personals.get_all(session=self.session):
            repo.sessions_personals.remove(spersonal.id)
        for sproxy in repo.sessions_proxies.get_all(session=self.session):
            repo.sessions_proxies.remove(sproxy.id)
        for stask in repo.sessions_tasks.get_all(session=self.session):
            repo.sessions_tasks.remove(stask.id)
        for sleep in repo.sleeps.get_all(session=self.session):
            repo.sleeps.remove(sleep.id)

        repo.sessions.update(self.session, state=SessionStates.banned, work=False)

    async def update_session(self, tg_user: types.User):
        self.logger("update_session")
        updates = {}
        if self.session.username != tg_user.username:
            updates['username'] = tg_user.username
        if self.session.tg_user_id != tg_user.id:
            updates['tg_user_id'] = tg_user.id

        if updates:
            repo.sessions.update(self.session, **updates)

    async def update_user(self, user: User, tg_user: types.User):
        self.logger("update_user")
        updates = {}
        if user.username != tg_user.username:
            updates['username'] = tg_user.username
        if user.first_name != tg_user.first_name:
            updates['first_name'] = tg_user.first_name
        if user.last_name != tg_user.last_name:
            updates['last_name'] = tg_user.last_name
        if user.tg_user_id != tg_user.id:
            updates['tg_user_id'] = tg_user.id

        if updates:
            repo.users.update(user, **updates)

    async def check_by_key_word(self, messages: List[types.Message], key_words: List[str]):
        self.logger("check_by_key_word")
        my_sessions_ids = [session.tg_user_id for session in repo.sessions.get_all()]
        for key_word in key_words:
            for message in messages:
                message_text = message.text or message.caption
                if not message_text:
                    continue
                if key_word.lower() not in message_text.lower():
                    continue
                if not message.from_user:
                    continue
                if message.from_user.id in my_sessions_ids:
                    continue

                repo.users.create(
                    tg_user_id=message.from_user.id, username=message.from_user.username,
                    first_name=message.from_user.first_name, last_name=message.from_user.last_name
                )
