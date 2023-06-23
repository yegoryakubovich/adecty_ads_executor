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

from bot.send_message import smart_send_message
from database import init_db, db
from database.models import Country, Order
from utils.logger import configure_logger


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
    await smart_send_message(order)

    # repo.sessions.session_add_new()
    # repo.proxies.add_new_proxy()
    # repo.groups.add_new_group()
    # check_new_proxy()
    # await check_wait_sessions()

    logger.info("Success init")


if __name__ == '__main__':
    asyncio.run(on_start_up())
