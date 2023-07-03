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
from datetime import datetime

import httpx
from loguru import logger

from core.constants import URL_FOR_TEST_PROXY, SEND_MSG_DELAY_SEC
from database import repo
from database.models import ProxyStates, SessionStates, GroupStates, SessionTask, MessageStates, SessionGroup, Message, \
    Group
from database.models.order import OrderStates
from database.models.session_group import SessionGroupState
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions import BotAction


class CheckerAction:
    def __init__(self):
        self.prefix = "Checker"

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    @classmethod
    async def wait_proxy_check(cls):
        for proxy in repo.proxies.get_all_by_state(state=ProxyStates.wait):
            try:
                r = httpx.get(url=URL_FOR_TEST_PROXY, timeout=5,
                              proxies=f'{proxy.type}://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}')
                if r.status_code == 200:
                    repo.proxies.update(proxy, state=ProxyStates.enable)
                    continue
            except:
                ...
            repo.proxies.update(proxy, state=ProxyStates.disable)

    @classmethod
    async def wait_session_check(cls):
        for session in repo.sessions.get_all_by_state(state=SessionStates.waiting):
            bot = BotAction(session=session)
            await bot.all_connection()
            if await bot.check():
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")

    async def get_session_by_group(self, group: Group):
        for session in repo.sessions.get_all_by_state(state=SessionStates.free):
            sg: SessionGroup = repo.sessions_groups.get(session=session, group=group)
            if sg:
                if sg.state == SessionGroupState.banned:
                    continue
                delay_seconds = SEND_MSG_DELAY_SEC
                last_message_session: Message = repo.messages.get_last(session=session)
                if last_message_session:
                    delay_seconds = (datetime.utcnow() - last_message_session.created).total_seconds()
                self.logger(f"{delay_seconds} > {SEND_MSG_DELAY_SEC}")
                if delay_seconds >= SEND_MSG_DELAY_SEC:
                    return session

    async def wait_session_group_check(self):
        for group in repo.groups.get_all_by_state(state=GroupStates.waiting):
            st: SessionTask = repo.sessions_tasks.get(
                group=group, type=SessionTaskType.check_group, state=SessionTaskStates.enable
            )
            if not st:
                session = await self.get_session_by_group(group=group)
                if session:
                    repo.sessions_tasks.create(
                        session=session,
                        group=group, type=SessionTaskType.check_group, state=SessionTaskStates.enable
                    )
                else:
                    session = repo.sessions.get_free(group=group)
                    if session:
                        repo.sessions_tasks.create(
                            session=session,
                            group=group, type=SessionTaskType.join_group, state=SessionTaskStates.enable
                        )

    async def wait_message_check(self):
        for message in repo.messages.get_all_by_state(state=MessageStates.waiting):
            group = repo.groups.get_by_id(message.group_id)
            st: SessionTask = repo.sessions_tasks.get(
                group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.enable,
            )
            if not st:
                session = await self.get_session_by_group(group=group)
                if session:
                    repo.sessions_tasks.create(
                        session=session,
                        group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.enable
                    )
                else:
                    session = repo.sessions.get_free(group=group)
                    if session:
                        repo.sessions_tasks.create(
                            session=session,
                            group=group, type=SessionTaskType.join_group, state=SessionTaskStates.enable
                        )

    async def wait_order_check(self):
        for order in repo.orders.get_all_by_state(state=OrderStates.waiting):
            for od in repo.orders_groups.get_by_order(order=order):
                group = repo.groups.get_by_id(od.group_id)
                if group.state != GroupStates.active:
                    return
                last_message = repo.messages.get_last(order=order, group=group)
                if last_message:
                    self.logger(f"Message {last_message} have state {last_message.state}")
                    if last_message.state == MessageStates.waiting:
                        return
                self.logger(group.name)
                st: SessionTask = repo.sessions_tasks.get(group=group, state=SessionTaskStates.enable)
                if not st:
                    self.logger("1")
                    session = await self.get_session_by_group(group=group)
                    if session:
                        self.logger("1")
                        repo.sessions_tasks.create(
                            session=session, group=group, order=order,
                            type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                        )
                    else:
                        session = repo.sessions.get_free(group=group)
                        if session:
                            repo.sessions_tasks.create(
                                session=session, group=group,
                                type=SessionTaskType.join_group, state=SessionTaskStates.enable
                            )
