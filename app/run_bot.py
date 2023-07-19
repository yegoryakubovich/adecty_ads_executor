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

from database import init_db, repo
from database.models import SessionStates
from functions import BotAction, AssistantAction
from utils.logger import configure_logger


def on_start_up():
    configure_logger(True)
    try:
        init_db()
        logger.info("[Database] Success connect database")
    except ConnectionRefusedError:
        logger.error("[Database] Failed to connect to database ")
        exit(1)

    """temporary"""
    # repo.shops.fill()
    # repo.proxies.fill()
    # repo.sessions.fill()
    repo.groups.fill()
    repo.orders_groups.fill()
    """temporary"""

    loop = asyncio.get_event_loop()
    all_functions = [{'fun': AssistantAction(), 'name': 'Assistant'}]
    all_functions.extend([
        {
            'fun': BotAction(session=session), 'name': f"Bot_{session.id}"
        } for session in repo.sessions.get_all(state=SessionStates.free)
    ])

    all_tasks = [loop.create_task(coro=function['fun'].start(), name=function['name']) for function in all_functions]
    all_tasks.extend([loop.create_task(hello(), name="TEST")])

    for task in all_tasks:
        logger.info(task.get_name())
        loop.run_until_complete(task)

    logger.info("Success init")


async def hello():
    while True:
        # logger.info([{'name': task.get_name(), 'func': task.get_coro()} for task in asyncio.all_tasks()])
        all_tasks = []
        for task in asyncio.all_tasks():
            task_name = task.get_name()
            if task_name == 'Assistant' or task_name.split('_')[0] == 'Bot':
                all_tasks.append(task_name)
        print(all_tasks)
        await asyncio.sleep(80)


if __name__ == '__main__':
    on_start_up()
