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
from datetime import datetime, timedelta

from loguru import logger

from core.constants import hour2sec
from database import repo
from database.models import ProxyStates, SessionStates, GroupStates, MessageStates, Shop, ProxyTypes, GroupType, Group, \
    User, OrderUserStates, SessionTask, SessionTaskType, SessionTaskStates, OrderStates, OrderTypes, PersonalTypes, \
    Order, Setting, SettingTypes
from functions import BotAction
from functions.other.executor import AssistantExecutorAction
from modules import convert
from modules.tdata import tdata_converter
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
        for state in [SessionStates.free, SessionStates.spam_block]:
            for session in repo.sessions.get_all(state=state):
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
        self.logger(f"Проверяю {ProxyStates.wait} прокси")
        for proxy in repo.proxies.get_all(state=ProxyStates.wait):
            if await self.executor.check_proxy(proxy):
                await self.executor.proxy_new(proxy)
            else:
                await self.executor.proxy_disable(proxy)
        self.logger(f"Проверяю {ProxyStates.enable} прокси")
        for proxy in repo.proxies.get_all(state=ProxyStates.enable):
            if await self.executor.check_proxy(proxy):
                pass
            else:
                await self.executor.proxy_disable(proxy)
        self.logger(f"Проверяю {ProxyStates.disable} прокси")
        for proxy in repo.proxies.get_all(state=ProxyStates.disable):
            if await self.executor.check_proxy(proxy):
                await self.executor.proxy_enable(proxy, log=False)
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
                        api_id=elem["api_id"], api_hash=elem["api_hash"], country=country, shop=shop
                    )
        new_tdata_session = tdata_converter.start()
        if new_tdata_session:
            self.logger("Find new sessions")
            for item in new_tdata_session:
                shop = repo.shops.create(name=item['shop_name'])
                for session in item['items']:
                    elem = item['items'][session]
                    country_type = get_by_phone(elem["session_name"])
                    country = repo.countries.create(code=country_type.code, name=country_type.name)
                    repo.sessions.create(
                        phone=elem["session_name"], string=elem["string"], tg_user_id=elem["user_id"],
                        api_id=elem["api_id"], api_hash=elem["api_hash"], country=country, shop=shop
                    )

    # WAIT SESSION CHECK

    async def wait_session_check(self):
        self.logger("wait_session_check")
        setting: Setting = repo.settings.get_by(key="new_session_sleep")
        for session in repo.sessions.get_all(state=SessionStates.waiting):
            bot = BotAction(session=session)
            await bot.all_connection()
            if await bot.check():
                repo.sleeps.create(
                    session=session,
                    time_second=int(setting.value) if setting.type == SettingTypes.num else setting.value
                )
                asyncio.create_task(coro=BotAction(session=session).start(), name=f"Bot_{session.id}")
                session_shop: Shop = repo.shops.get(session.shop_id)
                await self.executor.session_added_log(
                    session_id=session.id, session_shop_id=session_shop.id, session_shop_name=session_shop.name
                )

    # SPAM_BLOCK SESSION CHECK

    async def session_spam_block_check(self):
        self.logger("session_spam_block_check")
        for state in [SessionStates.free, SessionStates.spam_block]:
            for session in repo.sessions.get_all(state=state):
                st = repo.sessions_tasks.get_by(
                    session=session, type=SessionTaskType.check_spamblock, state=SessionTaskStates.enable
                )
                if st:
                    continue
                repo.sessions_tasks.create(
                    session=session, type=SessionTaskType.check_spamblock, state=SessionTaskStates.enable
                )
        await asyncio.sleep(hour2sec(12))

    # WAIT SESSION_GROUP CHECK

    async def wait_session_group_check(self):
        self.logger("wait_session_group_check")
        for group in repo.groups.get_all(state=GroupStates.waiting):
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, type=SessionTaskType.join_group, state=SessionTaskStates.enable
            )
            if st:
                continue
            orders = []
            for og in repo.orders_groups.get_all(group=group):
                orders.append(repo.orders.get(id=og.order_id))
            session = repo.sessions.get_free(orders=orders, group=group)
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
            if group.state != GroupStates.active:
                repo.messages.update(message, state=MessageStates.fine)
                continue
            st: SessionTask = repo.sessions_tasks.get_by(
                group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.enable,
            )
            if st:
                continue
            st_last: SessionTask = repo.sessions_tasks.get_last(
                group=group, message=message, type=SessionTaskType.check_message, state=SessionTaskStates.finished
            )
            if st_last:
                time_now = datetime.utcnow()
                if (st_last.created + timedelta(hours=1)) < time_now:
                    logger.info(f"({st_last.created} + {timedelta(hours=1)}) < {time_now}")
                    continue
                logger.info(f"YES ({st_last.created} + {timedelta(hours=1)}) < {time_now}")

            session = await self.executor.get_session_from_message_check(spam=True)
            if not session:
                continue
            repo.sessions_tasks.create(
                session=session, group=group, message=message,
                type=SessionTaskType.check_message, state=SessionTaskStates.enable
            )

    # WAIT ORDER CHECK

    async def wait_ads_order_check(self):
        self.logger("wait_ads_order_check")
        date_now = datetime.utcnow()
        for order in repo.orders.get_all(state=OrderStates.waiting, type=OrderTypes.ads):
            order: Order
            if order.datetime_stop <= date_now:
                repo.orders.update(order, state=OrderStates.stopped)
                continue
            for od in repo.orders_groups.get_all(order=order):
                group: Group = repo.groups.get(od.group_id)
                if group.state != GroupStates.active:
                    continue
                if group.join_request:
                    repo.groups.update(group, state=GroupStates.inactive)
                    continue
                if group.type == GroupType.inactive:
                    if not group.can_image:
                        repo.groups.update(group, state=GroupStates.inactive)
                        continue

                last_message = repo.messages.get_last(order=order, group=group)
                if last_message:
                    self.logger(f"Group_{group.id}. Message {last_message} have state {last_message.state}")
                    if last_message.state == MessageStates.waiting:
                        continue
                st: SessionTask = repo.sessions_tasks.get_all(
                    order=order, group=group, type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                )
                if st:
                    continue
                self.logger(f"Group_{group.id}. Task not found")
                session = await self.executor.get_session_by_group(group=group, order=order)
                if session:
                    self.logger(f"Group_{group.id}. Found linked session")
                    repo.sessions_tasks.create(
                        session=session, group=group, order=order,
                        type=SessionTaskType.send_by_order, state=SessionTaskStates.enable
                    )
                else:
                    self.logger(f"Group_{group.id}. Not found linked session")
                    session = repo.sessions.get_free(orders=[order], group=group)
                    if session:
                        self.logger(f"Group_{group.id}. Found session for link")
                        repo.sessions_tasks.create(
                            session=session, group=group,
                            type=SessionTaskType.join_group, state=SessionTaskStates.enable
                        )

    async def wait_mailing_order_check(self):
        self.logger("wait_order_check")
        date_now = datetime.utcnow()
        for order in repo.orders.get_all(state=OrderStates.waiting, type=OrderTypes.mailing):
            if order.datetime_stop <= date_now:
                repo.orders.update(order, state=OrderStates.stopped)
                continue
            for ou in repo.orders_users.get_all(order=order, state=OrderUserStates.active):
                user: User = repo.users.get(ou.user_id)
                if not user.username:
                    repo.orders_users.update(ou, state=OrderUserStates.abort, state_description="NOT USERNAME")
                    continue
                st: SessionTask = repo.sessions_tasks.get_all(
                    order=order, user=user, type=SessionTaskType.send_by_mailing, state=SessionTaskStates.enable
                )
                if st:
                    continue
                session = await self.executor.get_session_by_order(order=order)
                if not session:
                    self.logger("Not find free session to mailing")
                    return
                repo.sessions_tasks.create(
                    session=session, user=user, order=order,
                    type=SessionTaskType.send_by_mailing, state=SessionTaskStates.enable
                )

    # Personals Check

    async def personals_check(self):
        self.logger("personals_check")
        change_fi = repo.sessions_tasks.get_all(state=SessionTaskStates.enable, type=SessionTaskType.change_fi)
        avatar = repo.sessions_tasks.get_all(state=SessionTaskStates.enable, type=SessionTaskType.change_avatar)
        for state in [SessionStates.free, SessionStates.spam_block]:
            for session in repo.sessions.get_all(state=state):
                if avatar and change_fi:
                    return self.logger(f"#{session.id} ALL OKAY")

                sps = repo.sessions_personals.get_all(session=session)
                if not sps and not change_fi:
                    self.logger(f"#{session.id} CHANGE FI")
                    repo.sessions_tasks.create(session=session, type=SessionTaskType.change_fi,
                                               state=SessionTaskStates.enable)
                    change_fi = True
                if not avatar:
                    personals_types = [repo.personals.get(sp.personal_id).type for sp in sps]
                    if PersonalTypes.avatar not in personals_types:
                        self.logger(f"#{session.id} AVATAR")
                        repo.sessions_tasks.create(
                            session=session,
                            type=SessionTaskType.change_avatar, state=SessionTaskStates.enable
                        )
                        avatar = True
