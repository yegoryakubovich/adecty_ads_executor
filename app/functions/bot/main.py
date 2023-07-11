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
from pyrogram.errors import Forbidden

from core.constants import SEND_MSG_DELAY_MSG, ASSISTANT_SLEEP_SEC
from database import repo
from database.models import Session, SessionProxy, SessionTask, SessionGroup, SessionStates, GroupStates, MessageStates, \
    Order, Group
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

    async def task_join_group(self, task: SessionTask):
        self.logger("task_join_group")
        """
            Задача входа в группу.
        """
        group = repo.groups.get(task.group_id)
        await self.executor.join_chat(chat_id=group.name)
        repo.sessions_groups.create(session=self.session, group=group)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def task_check_group(self, task: SessionTask):
        self.logger("task_check_group")
        """
            Задача проверки группы.
        """
        group = repo.groups.get(task.group_id)
        chat = await self.executor.get_chat(group.name)
        repo.groups.update(group, subscribers=chat.members_count, state=GroupStates.active)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
        return self

    async def task_check_message(self, task: SessionTask):
        self.logger("task_check_message")
        """
            Задача проверки сообщения.
        """
        message = repo.messages.get(id=task.message_id)
        group = repo.groups.get(id=message.group_id)
        chat = await self.executor.get_chat(group.name)

        chat_messages_ids = await self.executor.get_all_messages_ids(group.name, limit=SEND_MSG_DELAY_MSG)
        repo.groups.update(group, subscribers=chat.members_count)

        if message.message_id in chat_messages_ids:
            return

        msg = await self.executor.get_messages(chat_id=group.name, msg_id=message.message_id)
        if msg.empty:
            repo.messages.update(message, state=MessageStates.deleted)
        else:
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

        chat = await self.executor.get_chat(group.name)
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

        try:
            self.logger(f"Send message to {group} by order {order}")
            msg = await self.executor.send_message(chat_id=group.name, text=text, photo=image)
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
        except Forbidden:
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively)

    """
    
        MAIN FUNCTION
    
    """

    @func_logger
    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            await asyncio.sleep(await smart_sleep(self.session))
            my_tasks = repo.sessions_tasks.get_all(session=self.session, state=SessionTaskStates.enable)
            if my_tasks:
                self.logger("Find task")
                try:
                    await self.start_session()
                    while my_tasks:
                        for task in my_tasks:
                            await asyncio.sleep(await smart_sleep(self.session))
                            if task.type == SessionTaskType.join_group:
                                await self.task_join_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_group:
                                await self.task_check_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_message:
                                await self.task_check_message(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.send_by_order:
                                await self.task_send_by_order(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            else:
                                logger.info("task not found")
                            my_tasks = repo.sessions_tasks.get_all(session=self.session, state=SessionTaskStates.enable)
                    await self.stop_session()
                except errors.UserDeactivatedBan:
                    await self.executor.session_banned()
                    return
            await asyncio.sleep(ASSISTANT_SLEEP_SEC)
