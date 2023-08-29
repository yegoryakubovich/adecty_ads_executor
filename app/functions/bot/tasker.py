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
from random import choice
from typing import Any

from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from core.constants import SEND_MSG_DELAY_MSG
from database import repo
from database.models import Session, SessionTask, GroupStates, MessageStates, Order, Group, SessionGroup, User, \
    PersonalTypes, PersonalSex, GroupType, SessionTaskStates, SessionGroupState, Personal, OrderUserStates
from functions.bot.executor import BotExecutorAction


class BotTaskerAction:
    def __init__(self, client: Client, session: Session, executor: BotExecutorAction):
        self.client = client
        self.session = session
        self.executor = executor
        self.prefix = f"[TASKER_{self.session.id}]"

    def logger(self, text: Any):
        logger.info(f"{self.prefix} {text}")

    async def join_group(self, task: SessionTask):
        self.logger("join_group")
        """
            Задача входа в группу.
        """
        group = repo.groups.get(task.group_id)

        chat = await self.executor.join_chat_by_group(group=group)

        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)
        repo.sessions_groups.create(session=self.session, group=group)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def check_group(self, task: SessionTask):
        self.logger("check_group")
        """
            Задача проверки группы.
        """
        group = repo.groups.get(task.group_id)

        chat = await self.executor.get_chat_by_group(group)
        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        repo.groups.update(group, subscribers=chat.members_count, state=GroupStates.active)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def check_message(self, task: SessionTask):
        self.logger("check_message")
        """
            Задача проверки сообщения.
        """
        message = repo.messages.get(id=task.message_id)
        group = repo.groups.get(id=message.group_id)

        chat = await self.executor.get_chat_by_group(group)

        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        repo.groups.update(group, subscribers=chat.members_count)
        chat_messages_ids = await self.executor.get_all_messages_ids(group.name, limit=SEND_MSG_DELAY_MSG)
        msg = await self.executor.get_messages(chat_id=group.name, msg_id=message.message_id)
        if msg.empty:
            repo.messages.update(message, state=MessageStates.deleted)
        else:
            if message.message_id in chat_messages_ids:
                return
            repo.messages.update(message, state=MessageStates.fine)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def send_by_order(self, task: SessionTask):
        self.logger("send_by_order")
        """
            Задача отправки сообщения.
        """
        order: Order = repo.orders.get(id=task.order_id)
        group: Group = repo.groups.get(id=task.group_id)
        sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)

        chat = await self.executor.get_chat_by_group(group)

        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        repo.groups.update(group, subscribers=chat.members_count)

        image = order.image_link if group.can_image else None
        if group.type == GroupType.link:
            text = order.message
        elif group.type == GroupType.no_link:
            text = order.message_no_link
        elif group.type == GroupType.short:
            text = order.message_short
        elif group.type == GroupType.replace:
            text = await self.executor.replace_text(order.message_short)
        else:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="No find text")
            return

        msg = await self.executor.send_message(chat_id=group.name, text=text, photo=image)

        if isinstance(msg, str):
            if msg in ["Forbidden", "BadRequest"]:
                repo.groups.update_to_next_type(group)
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=msg)

        if msg.empty:
            repo.groups.update_to_next_type(group)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Empty")

        if msg.from_user:
            await self.executor.update_session(msg.from_user)

        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
        repo.messages.create(
            session=self.session, group=group, order=order, message_id=msg.id,
            text=msg.caption if msg.caption else msg.text
        )

        await self.executor.send_message_log(
            session_id=self.session.id,
            order_id=order.id, order_name=order.name,
            group_id=group.id, group_name=group.name, post_id=msg.id,
            session_messages_count=len(repo.messages.get_all(session=self.session))
        )

    async def send_by_mailing(self, task: SessionTask):
        self.logger("send_by_mailing")
        """
            Задача отправки сообщения.
        """
        order: Order = repo.orders.get(id=task.order_id)
        user: User = repo.users.get(id=task.user_id)

        if not user.username:
            return repo.sessions_tasks.update(
                task, state=SessionTaskStates.abortively, state_description="Username not found"
            )

        tg_user = await self.executor.get_users(user.username)
        if isinstance(tg_user, str):
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=tg_user)
        elif not tg_user:
            pass
        else:
            await self.executor.update_user(user, tg_user)

        msg: Message = await self.executor.send_message(
            chat_id=user.username, text=order.message, photo=order.image_link
        )

        if isinstance(msg, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=msg)

        if msg.empty:
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Empty")

        if msg.from_user:
            await self.executor.update_session(msg.from_user)

        ou = repo.orders_users.get_by(user=user, order=order)

        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
        repo.orders_users.update(ou, state=OrderUserStates.finish)
        repo.messages.create(
            session=self.session, user=user, order=order, message_id=msg.id,
            text=msg.caption if msg.caption else msg.text, state=MessageStates.fine
        )

        await self.executor.send_message_mailing_log(
            session_id=self.session.id, user_id=user.id, username=user.username, order_name=f"{order.id} - {order.name}"
        )

    async def change_fi(self, task: SessionTask):
        self.logger("change_fi")
        my_sex = choice([PersonalSex.man, PersonalSex.woman])
        names = []
        surnames = []
        abouts = []
        for so in repo.sessions_orders.get_all(session=self.session):  # orders by session
            for op in repo.orders_personals.get_all(order=so.order_id):  # personals by order
                personal: Personal = repo.personals.get(op.personal_id)
                if personal.sex in [my_sex, PersonalSex.unisex]:
                    if personal.type == PersonalTypes.name:
                        names.append(personal)
                    elif personal.type == PersonalTypes.surname:
                        surnames.append(personal)
                    elif personal.type == PersonalTypes.about:
                        abouts.append(personal)
        self.logger(names)
        self.logger(surnames)
        self.logger(abouts)
        if not names and not surnames and not abouts:
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Not data")
        name = choice(names) if names else None
        surname = choice(surnames) if surnames else None
        about = choice(abouts) if abouts else None
        await self.executor.update_profile(
            name=name.value if name else None,
            surname=surname.value if surname else None,
            about=about.value if about else None
        )
        if name:
            repo.sessions_personals.create(session=self.session, personal=name, type=PersonalTypes.name)
        if surname:
            repo.sessions_personals.create(session=self.session, personal=surname, type=PersonalTypes.surname)
        if about:
            repo.sessions_personals.create(session=self.session, personal=about, type=PersonalTypes.about)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def change_avatar(self, task: SessionTask):
        self.logger("change_avatar")
        my_sex = repo.sessions_personals.get_sex(session=self.session)
        avatars = []
        for so in repo.sessions_orders.get_all(session=self.session):  # orders by session
            for op in repo.orders_personals.get_all(order=so.order_id):  # personals by order
                personal: Personal = repo.personals.get(op.personal_id)
                if personal.sex in [my_sex, PersonalSex.unisex]:
                    if personal.type == PersonalTypes.avatar:
                        avatars.append(personal)
        if not avatars:
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Not data")
        avatar = choice(avatars)
        await self.executor.update_profile_photo(
            photo=avatar.value if avatar else None
        )
        repo.sessions_personals.create(session=self.session, personal=avatar, type=PersonalTypes.avatar)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
