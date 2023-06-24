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

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from database import init_db, db, repo
from database.models import Country, Order, SessionStates
from functions.bot.main import BotAction
from functions.other.main import AssistantAction
from utils.logger import configure_logger


async def hi_men():
    print("Hi men")


async def on_start_up():
    configure_logger(True)
    try:
        init_db()
        logger.info("Success connect database")
    except ConnectionRefusedError:
        logger.error("Failed to connect to database ")
        exit(1)
    with db:
        Country.get_or_create(name="Russia")
        order, _ = Order.get_or_create(name="Test1",
                                       message="Всем привет, хочу узнать как вообще здесь относятся к новеньким?")
    # await session_actions.smart_send_message(order)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(hi_men, 'interval', minutes=1, next_run_time=datetime.now())
    scheduler.start()

    # repo.sessions.session_add_new()
    # repo.proxies.add_new_proxy()
    # repo.groups.add_new_group()
    # check_new_proxy()
    # await check_wait_sessions()

    logger.info("Success init")


if __name__ == '__main__':
    all_functions = [AssistantAction()]
    for session in repo.sessions.get_all_by_state(state=SessionStates.free):
        all_functions.append(BotAction(session=session))
    loop = asyncio.get_event_loop()
    all_tasks = []
    for function in all_functions:
        all_tasks.append(
            loop.create_task(
                function.start()
            )
        )
    loop.run_until_complete(asyncio.wait(all_tasks))


    # loop = asyncio.get_event_loop()
    # loop.create_task(hi_men())
    # asyncio.run(on_start_up())
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(hi_men, 'interval', minutes=1, next_run_time=datetime.now())
    # scheduler.start()
    # loop.run_forever()
