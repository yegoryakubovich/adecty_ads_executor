from telethon import TelegramClient

import repo
from models import Session, SessionProxy
from utils.checks.sessions_proxies import find_new_link


class SessionActions:
    async def open_session(self, session: Session) -> TelegramClient:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=session)
        if not sp:
            await find_new_link(session)
        client = TelegramClient(
            str(session.id), api_id=session.app_id, api_hash=session.app_id,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )
        return client


session_actions = SessionActions()
