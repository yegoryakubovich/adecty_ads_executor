import asyncio

from loguru import logger

from database import repo
from functions.other.checker import CheckAction
from functions.other.innovation import InnovationAction
from utils.checks.proxy import check_new_proxy
from utils.checks.sessions import check_wait_sessions


class AssistantAction:
    def __init__(self):
        self.check_actions = CheckAction()
        self.innovation_actions = InnovationAction()
        self.prefix = "Assistant"

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def start(self):
        self.logger("Запустился!")
        while True:
            self.logger("Начинаю проверку")
            # repo.sessions.session_add_new()
            # repo.proxies.add_new_proxy()
            # repo.groups.add_new_group()
            # check_new_proxy()
            # await check_wait_sessions()
            self.logger("Проверка закончена")

            await asyncio.sleep(120)
