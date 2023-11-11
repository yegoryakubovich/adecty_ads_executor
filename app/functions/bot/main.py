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
from pyrogram import Client, errors, enums

from database import repo
from database.models import Session, SessionProxy, SessionStates, MessageStates, User, SessionTaskType, \
    SessionTaskStates, OrderAttachmentTypes, Setting, SettingTypes
from functions.bot.executor import BotExecutorAction
from functions.bot.simulator import SimulatorAction
from functions.bot.tasker import BotTaskerAction
from utils.decorators import func_logger
from utils.helpers import smart_sleep, smart_create_sleep


class BotAction:
    client = None
    executor = None
    simulator = None
    tasker = None
    started = False

    def __init__(self, session: Session):
        self.session = session
        self.black_list = [session.tg_user_id, 777000]
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
        if self.started:
            return
        try:
            await self.client.start()
            self.started = True
        except (
                errors.SessionExpired, errors.SessionRevoked, errors.UserDeactivated, errors.UserDeactivatedBan,
                errors.AuthKeyUnregistered, errors.AuthKeyDuplicated, errors.InputUserDeactivated
        ) as e:
            self.logger(f"{e}")
            return await self.executor.session_banned()

    async def stop_session(self):
        if not self.started:
            return
        await self.client.stop()
        self.started = False

    async def all_connection(self):
        self.client = await self.open_session()
        if not self.client:
            raise
        self.executor = BotExecutorAction(client=self.client, session=self.session)
        self.tasker = BotTaskerAction(client=self.client, session=self.session, executor=self.executor)
        self.simulator = SimulatorAction(client=self.client)

    async def check(self) -> bool:
        await self.start_session()
        await self.stop_session()
        await self.start_session()
        await self.stop_session()
        repo.sessions.update(self.session, state=SessionStates.free)
        return True

    """

        MAIN FUNCTION

    """

    @func_logger
    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            setting: Setting = repo.settings.get_by(key="assistant_sleep")
            await asyncio.sleep(await smart_sleep(self.session))
            my_tasks = repo.sessions_tasks.get_all(in_list=True, session=self.session, state=SessionTaskStates.enable)
            if my_tasks:
                self.logger("Find task")
                while my_tasks:
                    setting_mi: Setting = repo.settings.get_by(key="session_sleep_min")
                    sleep_min = int(setting_mi.value) if setting_mi.type == SettingTypes.num else setting_mi.value
                    setting_ma: Setting = repo.settings.get_by(key="session_sleep_max")
                    sleep_max = int(setting_ma.value) if setting_ma.type == SettingTypes.num else setting_ma.value

                    await self.start_session()
                    for task in my_tasks:
                        if task.type != SessionTaskType.check_message:
                            continue
                        await self.tasker.check_message(task)
                    await self.stop_session()

                    for task in my_tasks:
                        await self.start_answers()
                        await asyncio.sleep(await smart_sleep(self.session))
                        await self.start_session()
                        if task.type == SessionTaskType.check_message:
                            pass
                        elif task.type == SessionTaskType.join_group:  # JOIN GROUP
                            await self.tasker.join_group(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        elif task.type == SessionTaskType.send_by_order:  # SEND BY ORDER
                            await self.tasker.send_by_order(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        elif task.type == SessionTaskType.send_by_mailing:  # SEND BY MAILING
                            await self.tasker.send_by_mailing(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        elif task.type == SessionTaskType.check_spamblock:  # SEND BY MAILING
                            await self.tasker.check_spamblock(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        elif task.type == SessionTaskType.change_fi:  # CHANGE FI
                            await self.tasker.change_fi(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        elif task.type == SessionTaskType.change_avatar:  # CHANGE AVATAR
                            await self.tasker.change_avatar(task)
                            await self.stop_session()
                            await asyncio.sleep(await smart_create_sleep(self.session, mi=sleep_min, ma=sleep_max))
                        else:
                            self.logger(f"Task not found {task.type}")
                        await self.stop_session()
                        my_tasks = repo.sessions_tasks.get_all(
                            in_list=True, session=self.session, state=SessionTaskStates.enable
                        )
            else:
                self.logger("Not find task")
                await self.start_answers()
            await asyncio.sleep(int(setting.value) if setting.type == SettingTypes.num else setting.value)

    async def start_answers(self):
        so = repo.sessions_orders.get_by(session_id=self.session.id)
        if not so:
            return
        order = repo.orders.get(so.order_id)
        order_attachment = repo.orders_attachments.get_by(order_id=order.id, type=OrderAttachmentTypes.text_answer)
        if not order_attachment:
            return

        await self.start_session()
        try:
            async for dialog in self.client.get_dialogs(limit=25):
                if dialog.chat.type != enums.ChatType.PRIVATE:
                    continue
                if dialog.chat.id in self.black_list:
                    continue

                if dialog.chat.id in [178220800, 451867324]:
                    async for msg in self.client.get_chat_history(chat_id=dialog.chat.id, limit=1):
                        for answer in repo.answers.get_all():
                            if answer.text_from in msg.text:
                                msg_to = await msg.reply(text=answer.text_to)
                                repo.messages.create(
                                    session=self.session, message_id=msg.id,
                                    text=msg.text, state=MessageStates.from_user
                                )
                                repo.messages.create(
                                    session=self.session, message_id=msg.id,
                                    text=msg_to.text, state=MessageStates.to_user
                                )

                    continue

                async for msg in self.client.get_chat_history(chat_id=dialog.chat.id, limit=1):
                    if msg.from_user.id == self.session.tg_user_id:
                        continue
                    user: User = repo.users.create(tg_user_id=msg.from_user.id)
                    await self.executor.update_user(user=user, tg_user=msg.from_user)
                    repo.messages.create(
                        session=self.session, user=user, message_id=msg.id,
                        text=msg.text or msg.caption, state=MessageStates.from_user
                    )
                    msg_send = await msg.reply(order_attachment.value, disable_web_page_preview=True)
                    if msg_send and not msg_send.empty:
                        if msg_send.from_user:
                            await self.executor.update_session(msg_send.from_user)
                    repo.messages.create(
                        session=self.session, user=user, message_id=msg_send.id,
                        text=msg_send.text, state=MessageStates.to_user
                    )
                    await self.executor.send_message_answer_log(
                        session_id=self.session.id, username=msg.from_user.username, user_id=user.id
                    )
        except errors.PeerFlood:
            self.logger("PeerFlood")
        except errors.ChannelPrivate:
            self.logger("ChannelPrivate")
        except errors.InputUserDeactivated:
            self.logger("InputUserDeactivated")
        await self.stop_session()
