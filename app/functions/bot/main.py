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

from core.constants import BOT_SLEEP_MAX, BOT_SLEEP_MIN
from database import repo
from database.models import Session, SessionProxy, SessionTask
from database.models.session_task import SessionTaskType
from functions.bot.executor import ExecutorAction
from functions.bot.simulator import SimulatorAction


def start_project():
    pass


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
            f"{self.session.id}",
            session_string=self.session.string,
            api_id=self.session.api_id,
            api_hash=self.session.api_hash,
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

    async def task_check_group(self, task: SessionTask):
        await self.start_session()
        # await asyncio.sleep(randint(BOT_SLEEP_MIN, BOT_SLEEP_MAX))
        group = repo.groups.get_by_id(task.group_id)
        logger.info(repo.sessions_groups.check_subscribe(session=self.session, group=group))
        if not repo.sessions_groups.check_subscribe(session=self.session, group=group):
            await self.executor.join_chat(chat_id=group.name)
            await repo.sessions_groups.create(session=self.session, group=group)
            await asyncio.sleep(randint(BOT_SLEEP_MIN, BOT_SLEEP_MAX))

        logger.info("Отправляю сообщение")
        msg = await self.executor.send_message(
            chat_id=group.name, text="\n".join([
                "Обмен валют 💁‍♀️",
                "",
                "🇷🇺RUB 🔃 USD 🇺🇸",
                "🇺🇦UAH ➡️ USD 🇺🇸",
                "🔐USDT ➡️ USD 🇺🇸",
                "",
                "🖇 Безопасно, быстро, круглосуточно",
            ]))
        repo.messages.create(
            session=self.session,
            group=group,
            message_id=msg.id
        )

        await asyncio.sleep(randint(BOT_SLEEP_MIN, BOT_SLEEP_MAX))
        await self.stop_session()

    async def task_check_message(self, task: SessionTask):
        await self.start_session()

        await self.stop_session()

    async def task_send_by_order(self, task: SessionTask):
        await self.start_session()

        await self.stop_session()

    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            await asyncio.sleep(randint(1, 30))
            my_tasks = repo.sessions_tasks.get_active_task(session=self.session)
            for task in my_tasks:
                if task.type == SessionTaskType.check_group:
                    await self.task_check_group(task)
                elif task.type == SessionTaskType.check_message:
                    await self.task_check_message(task)
                elif task.type == SessionTaskType.send_by_order:
                    await self.task_send_by_order(task)
                else:
                    pass

            await self.sleep()

        #     await self.start_session()
        #     # """CODE"""
        #     await asyncio.sleep(120)
        #     # """END CODE"""
        #     await self.stop_session()
        #     await asyncio.sleep(1 * 60 * 60)
