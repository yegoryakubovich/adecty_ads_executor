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
from typing import Optional

from loguru import logger
from pyrogram import Client, errors
from pyrogram.enums import ChatType
from pyrogram.types import Message

from core.constants import SEND_MSG_DELAY_MSG, ASSISTANT_SLEEP_SEC, SPAM_MESSAGE_ANSWERS, SPAM_STOP_MESSAGE, \
    SPAM_REPLY_ANSWERS, SPAM_FREE_MESSAGE, ANSWER_MESSAGE
from database import repo
from database.models import Session, SessionProxy, SessionTask, SessionStates, GroupStates, MessageStates, \
    Order, Group, SessionGroup, User
from database.models.session_group import SessionGroupState
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions.bot.executor import BotExecutorAction
from functions.bot.simulator import SimulatorAction
from utils.decorators import func_logger
from utils.helpers import smart_sleep, smart_create_sleep


class BotAction:
    client = None
    executor = None
    simulator = None

    def __init__(self, session: Session):
        self.session = session
        self.black_list = [session.id, 777000]
        self.prefix = f"Session #{self.session.id}"

    async def open_session(self) -> Optional[Client]:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=self.session)
        if not sp:
            self.logger("No find proxy")
            return
        return Client(
            f"{self.session.id}", session_string=self.session.string,
            api_id=self.session.api_id, api_hash=self.session.api_hash,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def start_session(self):
        await self.client.start()

    async def stop_session(self):
        await self.client.stop()

    async def all_connection(self):
        self.client = await self.open_session()
        if not self.client:
            raise
        self.executor = BotExecutorAction(client=self.client, session=self.session)
        self.simulator = SimulatorAction(client=self.client)

    async def check(self, chat_id: [int, str] = "durov") -> bool:
        try:
            await self.start_session()
            await self.executor.get_chat(chat_id=chat_id)

            repo.sessions.update(self.session, state=SessionStates.free)
            await self.stop_session()
            return True
        except:
            await self.executor.session_banned()
            return False

    async def change_profile(self):
        self.logger("change_profile")
        items = repo.personals.get_random_pack()
        self.logger(items)
        if items[0] or items[1] or items[2]:
            await self.executor.update_profile(name=items[0], surname=items[1], about=items[2])
        # if items[3]:
        #     await self.executor.update_profile_photo(photo=items[3])

    async def spam_bot_check(self):
        try:
            await asyncio.sleep(await smart_sleep(self.session))
            chat_id = "SpamBot"
            self.logger("Начинаю проверку")
            await self.start_session()
            await self.executor.send_message(chat_id, '/start')
            self.logger("Отправил start")
            while True:
                msg = (await self.executor.get_chat_history(chat_id, limit=1))[0]
                try:
                    keyboard = msg.reply_markup.keyboard
                except:
                    keyboard = None
                if keyboard:
                    if str(keyboard) in SPAM_REPLY_ANSWERS:
                        self.logger(f"Ответ: {SPAM_REPLY_ANSWERS[str(keyboard)]}")
                        await self.executor.send_message(chat_id=chat_id, text=SPAM_REPLY_ANSWERS[str(keyboard)])
                        await asyncio.sleep(5)
                    else:
                        self.logger(f"Найден новый ответ: \n{msg.text}\n{msg.reply_markup.keyboard}")
                        break
                elif msg.text in SPAM_STOP_MESSAGE:
                    self.logger("СТОП")
                    break
                elif msg.text in SPAM_MESSAGE_ANSWERS:
                    await self.executor.send_message(chat_id=chat_id, text=SPAM_MESSAGE_ANSWERS[msg.text])
                    await asyncio.sleep(5)
                else:
                    self.logger(f"Найден новый ответ: \n{msg.text}")
                    break

                if msg.text in SPAM_FREE_MESSAGE:
                    self.logger("КАЕФ")
                    await self.client.stop()
                    return True
            await self.client.stop()
            return False
        except errors.UserDeactivatedBan:
            await self.executor.session_banned()
            return False
        except errors.AuthKeyDuplicated:
            await self.executor.session_banned()
            return

    async def task_join_group(self, task: SessionTask):
        self.logger("task_join_group")
        """
            Задача входа в группу.
        """
        group = repo.groups.get(task.group_id)

        chat = await self.executor.join_chat_by_group(group=group)

        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)
        repo.sessions_groups.create(session=self.session, group=group)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def task_check_group(self, task: SessionTask):
        self.logger("task_check_group")
        """
            Задача проверки группы.
        """
        group = repo.groups.get(task.group_id)

        chat = await self.executor.get_chat_by_group(group)
        if isinstance(chat, str):
            return repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=chat)

        repo.groups.update(group, subscribers=chat.members_count, state=GroupStates.active)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def task_check_message(self, task: SessionTask):
        self.logger("task_check_message")
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

    async def task_send_by_order(self, task: SessionTask):
        self.logger("task_send_by_order")
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
        if group.can_message:
            text = order.message
        elif group.can_message_no_url:
            text = order.message_no_link
        elif group.can_message_short:
            text = order.message_short
        else:
            text = await self.executor.replace_text(order.message_short)

        msg = await self.executor.send_message(chat_id=group.name, text=text, photo=image)

        if isinstance(msg, str):
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=msg)
            return

        if msg.empty:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Empty")
            return

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

    async def task_send_by_mailing(self, task: SessionTask):
        self.logger("task_send_by_mailing")
        """
            Задача отправки сообщения.
        """
        order: Order = repo.orders.get(id=task.order_id)
        user: User = repo.users.get(id=task.user_id)

        if not user.username:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Username not found")
            return

        tg_user = await self.executor.get_users(user.username)
        if tg_user:
            await self.executor.update_user(user, tg_user)

        msg: Message = await self.executor.send_message(
            chat_id=user.username, text=order.message, photo=order.image_link
        )

        if isinstance(msg, str):
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description=msg)
            return

        if msg.empty:
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively, state_description="Empty")
            return

        if msg.from_user:
            await self.executor.update_session(msg.from_user)

        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
        repo.messages.create(
            session=self.session, user=user, order=order, message_id=msg.id,
            text=msg.caption if msg.caption else msg.text, state=MessageStates.fine
        )

        await self.executor.send_message_mailing_log(
            session_id=self.session.id, user_id=user.id, username=user.username
        )

    """

        MAIN FUNCTION

    """

    @func_logger
    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            await asyncio.sleep(await smart_sleep(self.session))
            my_tasks = repo.sessions_tasks.get_all(
                in_list=True, session=self.session, state=SessionTaskStates.enable
            )
            if my_tasks:
                self.logger("Find task")
                try:
                    await self.start_session()
                    while my_tasks:
                        for task in my_tasks:
                            await self.start_answers()
                            await asyncio.sleep(await smart_sleep(self.session))
                            if task.type == SessionTaskType.join_group:
                                await self.task_join_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_group:
                                await self.task_check_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_message:
                                await self.task_check_message(task)
                            elif task.type == SessionTaskType.send_by_order:
                                await self.task_send_by_order(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.send_by_mailing:
                                await self.task_send_by_mailing(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            else:
                                self.logger(f"Task not found {task.type}")
                            my_tasks = repo.sessions_tasks.get_all(
                                in_list=True, session=self.session, state=SessionTaskStates.enable
                            )
                        await asyncio.sleep(ASSISTANT_SLEEP_SEC)
                    await self.stop_session()
                except errors.UserDeactivatedBan:
                    self.logger("UserDeactivatedBan")
                    await self.executor.session_banned()
                    return
                except errors.AuthKeyDuplicated:
                    self.logger("AuthKeyDuplicated")
                    await self.executor.session_banned()
                    return
                except errors.InputUserDeactivated:
                    self.logger("InputUserDeactivated")
                    await self.stop_session()
            else:
                try:
                    self.logger("Not find task")
                    await self.start_session()
                    await self.start_answers()
                    await self.stop_session()
                except errors.UserDeactivatedBan:
                    self.logger("UserDeactivatedBan")
                    await self.executor.session_banned()
                    return
                except errors.AuthKeyDuplicated:
                    self.logger("AuthKeyDuplicated")
                    await self.executor.session_banned()
                    return
                except errors.InputUserDeactivated:
                    self.logger("InputUserDeactivated")
                    await self.stop_session()

            await asyncio.sleep(ASSISTANT_SLEEP_SEC)

    async def start_answers(self):
        try:
            async for dialog in self.client.get_dialogs(limit=100):
                if dialog.chat.type == ChatType.PRIVATE:
                    if dialog.chat.id in self.black_list:
                        continue

                    async for msg in self.client.get_chat_history(chat_id=dialog.chat.id, limit=1):
                        if msg.from_user.id == self.session.tg_user_id:
                            continue

                        user: User = repo.users.create(tg_user_id=msg.from_user.id)
                        await self.executor.update_user(user=user, tg_user=msg.from_user)
                        repo.messages.create(
                            user=user, message_id=msg.id, text=msg.text or msg.caption, state=MessageStates.from_user
                        )

                        msg_send = await msg.reply("\n".join(ANSWER_MESSAGE), disable_web_page_preview=True)
                        if msg_send and not msg_send.empty:
                            if msg_send.from_user:
                                await self.executor.update_session(msg_send.from_user)

                        repo.messages.create(
                            user=user, message_id=msg_send.id, text=msg_send.text, state=MessageStates.to_user
                        )
                        await self.executor.send_message_answer_log(
                            session_id=self.session.id, username=msg.from_user.username, user_id=user.id
                        )
        except errors.UserDeactivatedBan:
            self.logger("UserDeactivatedBan")
            await self.executor.session_banned()
            return False
        except errors.AuthKeyDuplicated:
            self.logger("AuthKeyDuplicated")
            await self.executor.session_banned()
            return
        except errors.InputUserDeactivated:
            self.logger("InputUserDeactivated")
