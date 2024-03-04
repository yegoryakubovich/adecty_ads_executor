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


import asyncio
from random import choice
from typing import Any

from loguru import logger
from pyrogram import Client, types
from pyrogram.raw import types
from pyrogram.types import Message

from core.constants import GROUPS_ORDERS_TEXT_TYPES, min2sec
from database import repo
from database.models import Session, SessionTask, GroupStates, MessageStates, Order, Group, SessionGroup, User, \
    PersonalTypes, PersonalSex, SessionTaskStates, SessionGroupState, Personal, OrderUserStates, \
    OrderAttachmentTypes, GroupType, GroupCaptionType, SessionStates, Setting, SettingTypes
from functions.bot.executor import BotExecutorAction
from utils.helpers import smart_create_sleep


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
        """Задача входа в группу"""
        group = repo.groups.get(task.group_id)

        if group.captcha_have:
            if group.captcha_type == GroupCaptionType.join_group:
                captcha_chat = await self.executor.join_chat_by_username(username=group.captcha_data)
                if isinstance(captcha_chat, str):
                    return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively,
                                                      state_description=captcha_chat)
            elif group.captcha_type == GroupCaptionType.click_button:
                for i in range(5):
                    for msg in await self.executor.get_chat_history(chat_id=group.name, limit=10):
                        if msg.reply_markup:
                            await self.executor.client.request_callback_answer(
                                chat_id=msg.chat.id, message_id=msg.id,
                                callback_data=msg.reply_markup[0][0].callback_data
                            )
                            break
                    await asyncio.sleep(10)

        chat: types.Chat = await self.executor.join_chat_by_group(group=group)
        if isinstance(chat, str):
            if chat in ["InviteRequestSent", "ChatInvalid", "ChannelInvalid", "UsernameInvalid", "UsernameNotOccupied"]:
                repo.groups.update(group, state=GroupStates.inactive)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)
        if not chat.permissions:
            repo.groups.update(group, state=GroupStates.inactive)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Channel")
        if not chat.permissions.can_send_messages:
            repo.groups.update(group, state=GroupStates.inactive)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Not Chat")

        chat = await self.executor.get_chat_by_group(group=group)
        repo.groups.update(group, subscribers=chat.members_count,
                           can_image=chat.permissions.can_send_media_messages, join_request=False,
                           state=GroupStates.active)
        repo.sessions_groups.create(session=self.session, group=group)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def check_message(self, task: SessionTask):
        self.logger(f"check_message")
        """Задача проверки сообщения"""
        message = repo.messages.get(id=task.message_id)
        group = repo.groups.get(id=message.group_id)
        setting_msg: Setting = repo.settings.get_by(key="send_message_delay")
        setting_words: Setting = repo.settings.get_by(key="user_save_key_word")

        if repo.sessions_groups.get_all(session=self.session, group=group, state=SessionGroupState.banned):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="SG banned")

        chat = await self.executor.get_chat_by_group(group)
        self.logger(f"[check_message] group={group.name}, message={message.message_id}")

        if isinstance(chat, str):
            # repo.messages.update(message, state=MessageStates.fine)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        msg = await self.executor.get_messages(chat_id=group.name, msg_id=message.message_id)
        if msg.empty:
            self.logger(f"[check_message] empty")
            repo.messages.update(message, state=MessageStates.deleted)
            repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
            return

        repo.groups.update(group, subscribers=chat.members_count)
        chat_messages = await self.executor.get_all_messages(
            group.name, limit=int(setting_msg.value) if setting_msg.type == SettingTypes.num else setting_msg.value
        )
        await self.executor.check_by_key_word(messages=chat_messages, key_words=setting_words.value.split(','))
        chat_messages_ids = [chat_message.id for chat_message in chat_messages]

        if message.message_id in chat_messages_ids:
            self.logger(f"[check_message] В СПИСКЕ")
            return
        self.logger(f"[check_message] Вышел из списка")
        repo.messages.update(message, state=MessageStates.fine)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def send_by_order(self, task: SessionTask):
        self.logger("send_by_order")
        """Задача отправки сообщения"""
        order: Order = repo.orders.get(id=task.order_id)
        group: Group = repo.groups.get(id=task.group_id)
        sg: SessionGroup = repo.sessions_groups.get_by(session=self.session, group=group)

        chat = await self.executor.get_chat_by_group(group)

        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        repo.groups.update(group, subscribers=chat.members_count)

        if group.type == GroupType.inactive:
            text = None
        else:
            text_attachment = repo.orders_attachments.get_all(order=order, type=GROUPS_ORDERS_TEXT_TYPES[group.type])
            if not text_attachment:
                repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="No find text")
                return
            text = choice(text_attachment).value
            if group.type == GroupType.replace:
                text = await self.executor.replace_text(text)

        image_attachment = repo.orders_attachments.get_all(order=order, type=OrderAttachmentTypes.image_common)
        image = choice(image_attachment).value if image_attachment else None

        msg = await self.executor.send_message(chat_id=group.name, text=text, photo=image)

        if isinstance(msg, str):
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
            session=self.session,
            order=order,
            group=group,
            post_id=msg.id,
            session_messages_count=len(repo.messages.get_all(session=self.session))
        )

    async def send_by_mailing(self, task: SessionTask):
        self.logger("send_by_mailing")
        """Задача отправки сообщения"""
        order: Order = repo.orders.get(id=task.order_id)
        user: User = repo.users.get(id=task.user_id)

        if not user.username:
            return repo.sessions_tasks.update(
                task, state=SessionTaskStates.abortively, state_description="Username not found"
            )

        tg_user = await self.executor.get_users(user.username)
        if isinstance(tg_user, str):
            for ou in repo.orders_users.get_all(order=order, user=user):
                repo.orders_users.update(ou, state=OrderUserStates.abort, state_description=tg_user)
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=tg_user)
        elif not tg_user:
            pass
        else:
            await self.executor.update_user(user, tg_user)

        text_attachment = repo.orders_attachments.get_all(order=order, type=OrderAttachmentTypes.text_common)
        if not text_attachment:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="No find text")
            return
        text = choice(text_attachment).value

        image_attachment = repo.orders_attachments.get_all(order=order, type=OrderAttachmentTypes.image_common)
        image = choice(image_attachment).value if image_attachment else None

        await self.executor.send_message(chat_id=user.username, photo=image)
        msg: Message = await self.executor.send_message(chat_id=user.username, text=text)

        if isinstance(msg, str):
            for ou in repo.orders_users.get_all(order=order, user=user):
                repo.orders_users.update(ou, state=OrderUserStates.abort, state_description=msg)
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=msg)
            await asyncio.sleep(await smart_create_sleep(self.session, minimum=min2sec(45), maximum=min2sec(60)))
            return

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
            session_id=self.session.id, user_id=user.id, username=user.username,
            order_id=order.id, order_name=order.name
        )

    async def check_spamblock(self, task: SessionTask):
        self.logger("check_spamblock")
        good_words = ["no limits", "свободен"]
        await self.executor.send_message(chat_id="SpamBot", text="/start")
        await asyncio.sleep(30)
        messages = await self.executor.get_chat_history(chat_id="SpamBot", limit=2)
        if not messages:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Not message")
        good_bool = False
        for message in messages:
            for word in good_words:
                if word in message.text:
                    good_bool = True

        if good_bool:
            repo.sessions.update(self.session, state=SessionStates.free)
        else:
            for task in repo.sessions_tasks.get_all(session=self.session, state=SessionTaskStates.enable):
                repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="SpamBlock")
            repo.sessions.update(self.session, state=SessionStates.spam_block)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished, state_description=messages[0].text)

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
        await self.executor.update_profile_photo(photo=avatar.value if avatar else None)
        repo.sessions_personals.create(session=self.session, personal=avatar, type=PersonalTypes.avatar)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
