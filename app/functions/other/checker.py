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

import httpx
from loguru import logger

from core.constants import URL_FOR_TEST_PROXY
from database import repo
from database.models import ProxyStates, SessionStates, GroupStates, SessionTask, MessageStates
from database.models.order import OrderStates
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions import BotAction


class CheckerAction:
    def __init__(self):
        pass

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

    @classmethod
    async def wait_session_group_check(cls):
        for group in repo.groups.get_all_by_state(state=GroupStates.checking_waiting):
            st: SessionTask = repo.sessions_tasks.get(
                group=group, state=SessionTaskStates.enable, type=SessionTaskType.check_group
            )
            if not st:
                session = repo.sessions.get_free()
                if session:
                    repo.sessions_tasks.create(
                        session=session, group=group,
                        type=SessionTaskType.check_group, state=SessionTaskStates.enable
                    )

    @classmethod
    async def wait_message_check(cls):
        for message in repo.messages.get_all_by_state(state=MessageStates.waiting):
            st: SessionTask = repo.sessions_tasks.get(
                message=message, state=SessionTaskStates.enable, type=SessionTaskType.check_message
            )
            if not st:
                session = repo.sessions.get_free()
                if session:
                    repo.sessions_tasks.create(
                        session=session, message=message,
                        type=SessionTaskType.check_message, state=SessionTaskStates.enable
                    )

    @classmethod
    async def wait_order_check(cls):
        for order in repo.orders.get_all_by_state(state=OrderStates.waiting):
            for od in repo.orders_groups.get_by_order(order=order):
                group = repo.groups.get_by_id(od.group_id)
                st: SessionTask = repo.sessions_tasks.get(
                    group=group, order=order,
                    state=SessionTaskStates.enable, type=SessionTaskType.send_by_order
                )
                if not st:
                    session = repo.sessions.get_free(group)
                    if session:
                        repo.sessions_tasks.create(
                            session=session, group=group, order=order,
                            type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                        )
