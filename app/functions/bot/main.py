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
import random
from random import randint
from typing import Optional

from loguru import logger
from pyrogram import Client, enums, errors
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import Message

from database import repo
from database.models import Session, SessionProxy, SessionStates, MessageStates, User, SessionTaskType, \
    SessionTaskStates, OrderAttachmentTypes, SessionDevice
from functions.bot.executor import BotExecutorAction
from functions.bot.simulator import SimulatorAction
from functions.bot.tasker import BotTaskerAction
from utils.decorators import func_logger
from utils.helpers import smart_sleep, smart_create_sleep


class BotAction:
    def __init__(self, session: Session):
        self.client: Client = None
        self.executor: BotExecutorAction = None
        self.simulator = None
        self.tasker = None

        self.session = session
        self.black_list = [session.tg_user_id, 777000]
        self.prefix = f"Session #{self.session.id}"

    async def open_session(self) -> Optional[Client]:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=self.session)
        if not sp:
            self.logger(f"No find proxy ({self.session.phone})")
            return
        sd: SessionDevice = repo.sessions_devices.get_by_session(session=self.session)
        device = repo.devices.get(id=sd.device_id)
        return Client(
            f"{self.session.id}", session_string=self.session.string,
            api_id=self.session.api_id, api_hash=self.session.api_hash,
            system_version=device.system_version, device_model=device.device_model,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def all_connection(self):
        self.client = await self.open_session()
        if not self.client:
            return

        @self.client.on_message()
        async def message_handler(client, message: Message):
            if message.chat.type != enums.ChatType.PRIVATE:
                return
            if message.chat.id == 777000 or message.chat.username == 'SpamBot':
                return
            if repo.sessions.check_exists(tg_user_id=message.chat.id):
                return
            so = repo.sessions_orders.get_by(session_id=self.session.id)
            if not so:
                self.logger(f"[start_answers] not sessions_orders")
                return
            order_attachment = repo.orders_attachments.get_by(
                order_id=so.order_id, type=OrderAttachmentTypes.text_answer
            )
            if not order_attachment:
                self.logger(f"[start_answers] not order_attachment")
                return
            try:
                user: User = repo.users.create(tg_user_id=message.from_user.id)
                await self.executor.update_user(user=user, tg_user=message.from_user)
                repo.messages.create(
                    session=self.session, user=user,
                    message_id=message.id, text=message.text or message.caption, state=MessageStates.from_user
                )
                msg_send = await message.reply(order_attachment.value, disable_web_page_preview=True)
                if msg_send and not msg_send.empty:
                    if msg_send.from_user:
                        await self.executor.update_session(msg_send.from_user)
                repo.messages.create(
                    session=self.session, user=user, message_id=msg_send.id,
                    text=msg_send.text, state=MessageStates.to_user
                )
                await self.executor.send_message_answer_log(
                    session_id=self.session.id, username=message.from_user.username, user_id=user.id
                )
            except errors.InputUserDeactivated:
                pass
            except errors.PeerFlood:
                pass
            except FloodWait as wait_err:
                await asyncio.sleep(wait_err.value)

        self.executor = BotExecutorAction(client=self.client, session=self.session)
        self.tasker = BotTaskerAction(client=self.client, session=self.session, executor=self.executor)
        self.simulator = SimulatorAction(client=self.client)
        if not await self.executor.start_session():
            return False
        return True

    """
        MAIN FUNCTION
    """

    @func_logger
    async def start(self):
        await asyncio.sleep(randint(30, 300))
        self.logger(f"Started!")
        if not await self.all_connection():
            return
        other_task_types = [
            SessionTaskType.join_group, SessionTaskType.send_by_order, SessionTaskType.send_by_mailing,
            SessionTaskType.check_spamblock, SessionTaskType.change_fi, SessionTaskType.change_avatar,
        ]
        while True:
            self.session = repo.sessions.get(id=self.session.id)
            if self.session.state == SessionStates.banned:
                return
            await asyncio.sleep(int(repo.settings.get_by(key="session_sleep_between").value))
            """SPAM ANSWER"""
            await self.spam_answer()
            """CHECK MESSAGE TASK"""
            check_message_task = repo.sessions_tasks.get_all(
                in_list=True, session=self.session, type=SessionTaskType.check_message, state=SessionTaskStates.enable
            )
            for task in check_message_task:
                await self.tasker.check_message(task)
                await asyncio.sleep(random.choice([1, 1, 2, 2, 2, 3, 3, 5, 10, 15]))
            """CHECK SLEEP"""
            sleep_time = await smart_sleep(self.session)
            if sleep_time > 0:
                self.logger(f"Спать ещё минимум {sleep_time} сек.")
                continue
            """OTHER TASK"""
            my_tasks = repo.sessions_tasks.get_all(in_list=True, session=self.session, state=SessionTaskStates.enable)
            if not my_tasks:  # Нет задач
                continue
            for task in my_tasks:
                if task.type not in other_task_types:  # Отсекаем ненужные
                    continue
                """Отправляем в работу"""
                if task.type == SessionTaskType.join_group:  # JOIN GROUP
                    await self.tasker.join_group(task)
                elif task.type == SessionTaskType.send_by_order:  # SEND BY ORDER
                    await self.tasker.send_by_order(task)
                elif task.type == SessionTaskType.send_by_mailing:  # SEND BY MAILING
                    await self.tasker.send_by_mailing(task)
                elif task.type == SessionTaskType.check_spamblock:  # SEND BY MAILING
                    await self.tasker.check_spamblock(task)
                elif task.type == SessionTaskType.change_fi:  # CHANGE FI
                    await self.tasker.change_fi(task)
                elif task.type == SessionTaskType.change_avatar:  # CHANGE AVATAR
                    await self.tasker.change_avatar(task)
                """Создаем сон"""
                sleep_min = int(repo.settings.get_by(key="session_sleep_min").value)
                sleep_max = int(repo.settings.get_by(key="session_sleep_max").value)
                await smart_create_sleep(self.session, minimum=sleep_min, maximum=sleep_max)
                break

    @func_logger
    async def spam_answer(self):
        active_session: Session = repo.sessions.get(id=self.session.id)
        logger.info(f"spam_answer {active_session.state}")
        try:
            await self.client.get_chat_history_count(chat_id="SpamBot")
        except Exception as e:
            return

        async for msg in self.client.get_chat_history(chat_id="SpamBot", limit=1):
            for answer in repo.answers.get_all():
                if answer.text_from in msg.text:
                    msg_to = await msg.reply(text=answer.text_to)
                    repo.messages.create(
                        session=self.session, message_id=msg.id, text=msg.text, state=MessageStates.from_user
                    )
                    repo.messages.create(
                        session=self.session, message_id=msg.id, text=msg_to.text, state=MessageStates.to_user
                    )
