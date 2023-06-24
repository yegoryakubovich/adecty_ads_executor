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
from functions.bot.main import BotAction
from functions.other.main import AssistantAction
from utils.logger import configure_logger


def on_start_up():
    configure_logger(True)
    try:
        init_db()
        logger.info("[Database] Success connect database")
    except ConnectionRefusedError:
        logger.error("[Database] Failed to connect to database ")
        exit(1)

    all_functions = [AssistantAction()]
    all_functions.extend([
        BotAction(session=session) for session in repo.sessions.get_all_by_state(state=SessionStates.free)
    ])
    loop = asyncio.get_event_loop()
    all_tasks = [loop.create_task(function.start()) for function in all_functions]
    loop.run_until_complete(asyncio.wait(all_tasks))

    logger.info("Success init")


if __name__ == '__main__':
    on_start_up()
