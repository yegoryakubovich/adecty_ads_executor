import asyncio

from loguru import logger

from database import init_db, db, repo
from database.models import Country
from utils.checks.proxy import check_new_proxy
from utils.checks.sessions import check_free_sessions
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
    repo.sessions.session_add_new()
    repo.proxies.add_new_proxy()
    repo.groups.add_new_group()
    check_new_proxy()
    await check_free_sessions()

    logger.info("Success init")


if __name__ == '__main__':
    asyncio.run(on_start_up())
