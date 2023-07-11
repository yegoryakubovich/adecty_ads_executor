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

from loguru import logger

from core.constants import NEW_SESSION_SLEEP_SEC
from database import repo
from database.models import ProxyStates, SessionStates, GroupStates, MessageStates, Shop, ProxyTypes
from database.models import SessionTask
from database.models.order import OrderStates
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions import BotAction
from functions.other.executor import AssistantExecutorAction
from modules import convert
from utils.country import get_by_phone
from utils.new import new


class CheckerAction:
    def __init__(self, executor: AssistantExecutorAction):
        self.executor = executor
        self.prefix = "Checker"

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def new_session_check(self):
        self.logger("new_session_check")
        new_session = convert.start()
        if new_session:
            self.logger("Find new sessions")
            for session in new_session:
                item = new_session[session]
                country_type = get_by_phone(item["phone"])
                country = repo.countries.create(code=country_type.code, name=country_type.name)
                shop = repo.shops.get(1)
                repo.sessions.create(
                    phone=item["phone"], string=item["string_session"], api_id=item["api_id"],
                    api_hash=item["api_hash"],
                    country=country, shop=shop
                )

    async def new_proxy_check(self):
        self.logger("new_proxy_check")
        new_proxy = await new.get_proxy()
        if new_proxy:
            self.logger("Find new proxy")
            for item in new_proxy:
                item_data = item.split("@")
                host, port = item_data[1].split(':')[0], item_data[1].split(':')[1]
                user, password = item_data[0].split(':')[0], item_data[0].split(':')[1]
                shop = repo.shops.get(1)
                repo.proxies.create(
                    type=ProxyTypes.socks5, host=host, port=port, user=user, password=password, shop=shop
                )

    async def wait_proxy_check(self):
        self.logger("wait_proxy_check")
        for proxy in repo.proxies.get_all(state=ProxyStates.wait):
            if await self.executor.check_proxy(proxy):
                await self.executor.proxy_new(proxy)
            else:
                await self.executor.proxy_disable(proxy)

        for proxy in repo.proxies.get_all(state=ProxyStates.enable):
            if await self.executor.check_proxy(proxy):
                pass
            else:
                await self.executor.proxy_disable(proxy)

    async def wait_session_check(self):
        self.logger("wait_session_check")
        for session in repo.sessions.get_all(state=SessionStates.waiting):
            bot = BotAction(session=session)
            await bot.all_connection()
            if await bot.check():
                repo.sleeps.create(session=session, time_second=NEW_SESSION_SLEEP_SEC)
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")
                session_shop: Shop = repo.shops.get(session.shop_id)
                await self.executor.session_added_log(
                    session_id=session.id, session_shop_id=session_shop.id, session_shop_name=session_shop.name
                )

    async def wait_session_group_check(self):
        self.logger("wait_session_group_check")
        for group in repo.groups.get_all(state=GroupStates.waiting):
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, type=SessionTaskType.check_group, state=SessionTaskStates.enable
            )

            if not st:
                session = await self.executor.get_session_by_group(group=group, send_msg=False)
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
        self.logger("wait_message_check")
        for message in repo.messages.get_all(state=MessageStates.waiting):
            group = repo.groups.get(message.group_id)
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.enable,
            )
            if not st:
                session = await self.executor.get_session_by_group(group=group)
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
        self.logger("wait_order_check")
        for order in repo.orders.get_all(state=OrderStates.waiting):
            for od in repo.orders_groups.get_all(order=order):
                group = repo.groups.get(od.group_id)
                if group.state != GroupStates.active:
                    continue
                last_message = repo.messages.get_last(order=order, group=group)
                if last_message:
                    self.logger(f"Message {last_message} have state {last_message.state}")
                    if last_message.state == MessageStates.waiting:
                        continue
                st: SessionTask = repo.sessions_tasks.get_by(group=group, state=SessionTaskStates.enable)
                if not st:
                    session = await self.executor.get_session_by_group(group=group)
                    if session:
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
