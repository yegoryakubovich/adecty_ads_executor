import os

from loguru import logger
from telethon.errors import UserDeactivatedBanError, UnauthorizedError

import repo
from bot.sessions import session_actions
from core.constants import SESSIONS_DIR, NEW_SESSION_DIR
from models.sessions import SessionStates


async def check_new_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.wait):
        session_file = os.path.exists(f"{NEW_SESSION_DIR}/{session.phone}.session")
        if session_file:
            os.rename(f"{NEW_SESSION_DIR}/{session.phone}.session", f"{SESSIONS_DIR}/{session.id}.session")
            repo.sessions.move_state(session=session, state=SessionStates.check)
            repo.sessions_proxies.create(session=session, proxy=repo.sessions_proxies.get_free_proxy())
        else:
            repo.sessions.move_state(session=session, state=SessionStates.not_file)


async def check_free_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.check):
        client = await session_actions.open_session(session)
        async with client:
            try:
                await client.get_entity('durov')
                if session.id == 1:
                    raise UserDeactivatedBanError
            except:
                pass


async def check_banned_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.free):
        client = await session_actions.open_session(session)
        async with client:
            try:
                logger.info(await client.get_entity('durov'))
                if session.id == 1:
                    raise UserDeactivatedBanError
            except (UserDeactivatedBanError, UnauthorizedError):
                repo.sessions.move_state(SessionStates.banned)
