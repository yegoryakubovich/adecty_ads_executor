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

from core.constants import NEW_SESSION_SLEEP_SEC
from database import repo
from database.models import ProxyStates, SessionStates, GroupStates, MessageStates, Shop, ProxyTypes, GroupType, Group, \
    User, OrderUserStates, SessionTask, SessionTaskType, SessionTaskStates, OrderStates, OrderTypes
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

    """INSIDE"""

    async def all_task_check(self):
        for session in repo.sessions.get_all(state=SessionStates.free):
            if f"Bot_{session.id}" not in [task.get_name() for task in asyncio.all_tasks()]:
                self.logger(f"Повторный запуск Bot_{session.id}")
                repo.sessions.update(session, work=False)
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")
            else:
                repo.sessions.update(session, work=True)

    """
    PROXY
    """

    # NEW PROXY CHECK

    async def new_proxy_check(self):
        self.logger("new_proxy_check")
        shops = await new.get_proxy()
        if shops:
            self.logger("Find new proxy")
            for shop_name in shops:
                shop = repo.shops.create(name=shop_name)
                self.logger(shop_name)
                for item in shops[shop_name]:
                    item_data = item.split("@")
                    host, port = item_data[1].split(':')[0], item_data[1].split(':')[1]
                    user, password = item_data[0].split(':')[0], item_data[0].split(':')[1]
                    repo.proxies.create(
                        type=ProxyTypes.socks5, host=host, port=port, user=user, password=password, shop=shop
                    )

    # WAIT PROXY CHECK

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

        if randint(1, 5) == 1:
            for proxy in repo.proxies.get_all(state=ProxyStates.disable):
                if await self.executor.check_proxy(proxy):
                    pass
                else:
                    await self.executor.proxy_disable(proxy, log=False)

    """
    SESSION
    """

    # NEW SESSION CHECK

    async def new_session_check(self):
        self.logger("new_session_check")
        new_session = convert.start()
        if new_session:
            self.logger("Find new sessions")
            for item in new_session:
                shop = repo.shops.create(name=item['shop_name'])
                for session in item['items']:
                    elem = item['items'][session]
                    country_type = get_by_phone(elem["phone"])
                    country = repo.countries.create(code=country_type.code, name=country_type.name)
                    repo.sessions.create(
                        phone=elem["phone"], string=elem["string_session"], tg_user_id=elem["user_id"],
                        api_id=elem["api_id"], api_hash=elem["api_hash"],
                        country=country, shop=shop
                    )

    # WAIT SESSION CHECK

    async def wait_session_check(self):
        self.logger("wait_session_check")
        for session in repo.sessions.get_all(state=SessionStates.waiting):
            bot = BotAction(session=session)
            await bot.all_connection()
            if await bot.check():
                await bot.start_session()
                await bot.stop_session()
                repo.sleeps.create(session=session, time_second=NEW_SESSION_SLEEP_SEC)
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")
                session_shop: Shop = repo.shops.get(session.shop_id)
                await self.executor.session_added_log(
                    session_id=session.id, session_shop_id=session_shop.id, session_shop_name=session_shop.name
                )

    # SPAM_BLOCK SESSION CHECK

    async def spam_block_session_check(self):
        self.logger("spam_block_session_check")
        for session in repo.sessions.get_all(state=SessionStates.spam_block):
            bot = BotAction(session=session)
            await bot.all_connection()
            if await bot.spam_bot_check():
                repo.sleeps.create(session=session, time_second=NEW_SESSION_SLEEP_SEC)
                repo.sessions.update(session, state=SessionStates.free)
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")

    # WAIT SESSION_GROUP CHECK

    async def wait_session_group_check(self):
        self.logger("wait_session_group_check")
        for group in repo.groups.get_all(state=GroupStates.waiting):
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, type=SessionTaskType.check_group, state=SessionTaskStates.enable
            )

            if not st:
                session = await self.executor.get_session_by_group(group=group)
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

    # WAIT MESSAGE CHECK

    async def wait_message_check(self):
        self.logger("wait_message_check")
        for message in repo.messages.get_all(state=MessageStates.waiting):
            group = repo.groups.get(message.group_id)
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.enable,
            )
            if not st:
                session = await self.executor.get_session_by_group(group=group, spam=True)
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

    # WAIT ORDER CHECK

    async def wait_ads_order_check(self):
        self.logger("wait_ads_order_check")
        for order in repo.orders.get_all(state=OrderStates.waiting, type=OrderTypes.ads):
            for od in repo.orders_groups.get_all(order=order):
                group: Group = repo.groups.get(od.group_id)
                if group.state != GroupStates.active:
                    continue
                if group.type == GroupType.inactive:
                    if not group.can_image:
                        repo.groups.update(group, state=GroupStates.inactive)
                        continue
                    group = repo.groups.update(group, can_image=False, type=GroupType.link)

                last_message = repo.messages.get_last(order=order, group=group)
                if last_message:
                    self.logger(f"Group_{group.id}. Message {last_message} have state {last_message.state}")
                    if last_message.state == MessageStates.waiting:
                        continue
                st: SessionTask = repo.sessions_tasks.get_all(
                    order=order, group=group, type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                )
                if not st:
                    self.logger(f"Group_{group.id}. Task not found")
                    session = await self.executor.get_session_by_group(group=group)
                    if session:
                        self.logger(f"Group_{group.id}. Found linked session")
                        repo.sessions_tasks.create(
                            session=session, group=group, order=order,
                            type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                        )
                    else:
                        self.logger(f"Group_{group.id}. Not found linked session")
                        session = repo.sessions.get_free(group=group)
                        if session:
                            self.logger(f"Group_{group.id}. Found session for link")
                            repo.sessions_tasks.create(
                                session=session, group=group,
                                type=SessionTaskType.join_group, state=SessionTaskStates.enable
                            )

    async def wait_mailing_order_check(self):
        self.logger("wait_order_check")
        for order in repo.orders.get_all(state=OrderStates.waiting, type=OrderTypes.mailing):
            for ou in repo.orders_users.get_all(order=order, state=OrderUserStates.active):
                user: User = repo.users.get(ou.user_id)
                if not user.username:
                    repo.orders_users.update(ou, state=OrderUserStates.abort, state_description="NOT USERNAME")
                    continue
                st: SessionTask = repo.sessions_tasks.get_all(
                    order=order, user=user, type=SessionTaskType.send_by_mailing, state=SessionTaskStates.enable
                )
                if not st:
                    session = await self.executor.get_session_by_order(order=order)
                    if not session:
                        self.logger("Not find free session to mailing")
                        continue
                    repo.sessions_tasks.create(
                        session=session, user=user, order=order,
                        type=SessionTaskType.send_by_mailing, state=SessionTaskStates.enable
                    )

    # Personals Check

    async def personals_check(self):
        self.logger("personals_check")
        for session in repo.sessions.get_all(state=SessionStates.free):
            sp = repo.sessions_personals.get_all(session=session)
            self.logger(sp)

            if not sp:  # Not all
                self.logger(f"#{session.id} NOT ALL")
                if repo.sessions_tasks.get_all(state=SessionTaskStates.enable, type=SessionTaskType.change_fi):
                    continue
                repo.sessions_tasks.create(
                    session=session,
                    type=SessionTaskType.change_fi, state=SessionTaskStates.enable
                )
            elif len(sp) >= 4:
                self.logger(f"#{session.id} ALL")
                continue
            else:  # Not avatar
                self.logger(f"#{session.id} AVATAR")
                if repo.sessions_tasks.get_all(state=SessionTaskStates.enable, type=SessionTaskType.change_avatar):
                    continue
                repo.sessions_tasks.create(
                    session=session,
                    type=SessionTaskType.change_avatar, state=SessionTaskStates.enable
                )
