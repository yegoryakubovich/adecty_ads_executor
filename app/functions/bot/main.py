from loguru import logger
from pyrogram import Client

from database import repo
from database.models import Session, SessionProxy
from functions.bot.executor import ExecutorAction
from functions.bot.simulator import SimulatorAction


class BotAction:
    client = None
    executor_actions = None
    simulator_actions = None

    def __init__(self, session: Session):
        self.session = session

    async def open_session(self) -> Client:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=self.session)
        return Client(
            f"{self.session.id}",
            session_string=self.session.string,
            api_id=self.session.api_id,
            api_hash=self.session.api_hash,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )

    async def start_session(self):
        await self.client.start()

    async def stop_session(self):
        await self.client.stop()

    async def start(self):
        self.client = await self.open_session()
        await self.start_session()
        self.executor_actions = ExecutorAction(self.client)
        self.simulator_actions = SimulatorAction(self.client)
        """CODE"""
        logger.info(f"[{self.session.id}] Запустился!")
        """END CODE"""
        await self.stop_session()
