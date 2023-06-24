from loguru import logger

from functions.other.checker import CheckAction
from functions.other.innovation import InnovationAction


class AssistantAction:
    def __init__(self):
        self.check_actions = CheckAction()
        self.innovation_actions = InnovationAction()

    async def start(self):
        logger.info(f"[Assistant] Запустился!")
