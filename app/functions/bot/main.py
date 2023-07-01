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
from random import randint

from loguru import logger
from pyrogram import Client
from pyrogram.errors import Forbidden

from core.constants import BOT_SLEEP_MAX_MIN, BOT_SLEEP_MIN_MIN
from database import repo
from database.models import Session, SessionProxy, SessionTask, SessionGroup, SessionStates, GroupStates, MessageStates
from database.models.session_group import SessionGroupState
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions.bot.executor import ExecutorAction
from functions.bot.simulator import SimulatorAction
from utils.decorators import func_logger


class BotAction:
    client = None
    executor = None
    simulator = None

    def __init__(self, session: Session):
        self.session = session
        self.prefix = f"Session #{self.session.id}"

    async def open_session(self) -> Client:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=self.session)
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
        self.executor = ExecutorAction(self.client)
        self.simulator = SimulatorAction(self.client)

    async def check(self, chat_id: [int, str] = "durov") -> bool:
        await self.start_session()
        try:
            await self.executor.get_chat(chat_id=chat_id)
            repo.sessions.update(self.session, state=SessionStates.free)
            await self.stop_session()
            return True
        except:
            repo.sessions.set_banned(self.session)
            await self.stop_session()
            return False

    async def task_check_group(self, task: SessionTask):
        """
            Задача проверки группы.

            ВХодит в группу, если ранее не был в ней (сохраняет в sessions_groups)
            Отправляет тестовое сообщение (сохраняет в messages)
        """

        group = repo.groups.get_by_id(task.group_id)
        chat = await self.executor.get_chat(group.name)
        repo.groups.update(group, subcribers=chat.members_count)
        if not repo.sessions_groups.check_subscribe(session=self.session, group=group):
            await self.executor.join_chat(chat_id=group.name)
            repo.sessions_groups.create(session=self.session, group=group)
            await asyncio.sleep(randint(BOT_SLEEP_MIN_MIN, BOT_SLEEP_MAX_MIN) * 60)
        sg: SessionGroup = repo.sessions_groups.get(session=self.session, group=group)
        msg = None
        try:
            msg = await self.executor.send_message(
                chat_id=group.name, text="\n".join([
                    "Обмен валют 💁‍♀️", "",
                    "🇷🇺RUB 🔃 USD 🇺🇸",
                    "🇺🇦UAH ➡️ USD 🇺🇸",
                    "🔐USDT ➡️ USD 🇺🇸", "",
                    "🖇 Безопасно, быстро, круглосуточно",
                ]))
            repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
        except Forbidden:
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively)
        if msg:
            repo.messages.create(session=self.session, group=group, message_id=msg.id)
            repo.groups.update(group, state=GroupStates.active)

    async def task_check_message(self, task: SessionTask):
        """
            Задача проверки сообщения.


        """
        message = repo.messages.get_by_id(id=task.message_id)
        group = repo.groups.get_by_id(message.group_id)
        msg = await self.executor.get_messages(chat_id=group.name, msg_id=message.message_id)
        if msg.empty:
            repo.messages.update(message=message, state=MessageStates.deleted)
        else:
            repo.messages.update(message, state=MessageStates.fine)
        repo.sessions_tasks.update(task, state=SessionTaskStates.finished)

    async def task_send_by_order(self, task: SessionTask):
        """
            Задача отправки сообщения.


        """
        logger.info('Im here')
        order = repo.orders.get_by_id(id=task.order_id)
        group = repo.groups.get_by_id(id=task.group_id)
        if not repo.sessions_groups.check_subscribe(session=self.session, group=group):
            logger.info("subscribe")
            await self.executor.join_chat(chat_id=group.name)
            repo.sessions_groups.create(session=self.session, group=group)
            await asyncio.sleep(randint(BOT_SLEEP_MIN_MIN, BOT_SLEEP_MAX_MIN) * 60)
        sg: SessionGroup = repo.sessions_groups.get(session=self.session, group=group)
        try:
            logger.info("send_msg")
            msg = await self.executor.send_message(chat_id=group.name, text=order.message)
            repo.sessions_tasks.update(task, state=SessionTaskStates.finished)
            repo.messages.create(session=self.session, group=group, order=order, message_id=msg.id, text=msg.text)
        except Forbidden:
            logger.info("forbidden")
            repo.sessions_groups.update(sg, state=SessionGroupState.banned)
            repo.sessions_tasks.update(task, state=SessionTaskStates.abortively)

    @func_logger
    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            await asyncio.sleep(randint(1, 30))
            my_tasks = repo.sessions_tasks.get_active_task(session=self.session)
            if my_tasks:
                await self.start_session()
                for task in my_tasks:
                    await asyncio.sleep(randint(BOT_SLEEP_MIN_MIN, BOT_SLEEP_MAX_MIN) * 60)
                    if task.type == SessionTaskType.check_group:
                        await self.task_check_group(task)
                    elif task.type == SessionTaskType.check_message:
                        await self.task_check_message(task)
                    elif task.type == SessionTaskType.send_by_order:
                        await self.task_send_by_order(task)
                    else:
                        pass
                await asyncio.sleep(randint(BOT_SLEEP_MIN_MIN, BOT_SLEEP_MAX_MIN) * 60)
                await self.stop_session()

            await asyncio.sleep(randint(BOT_SLEEP_MIN_MIN, BOT_SLEEP_MAX_MIN) * 60)
