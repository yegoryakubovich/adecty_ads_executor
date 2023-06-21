from pyrogram import Client

import repo
from models import Session, SessionProxy
from utils.checks.sessions_proxies import find_new_link


class SessionActions:
    async def open_session(self, session: Session) -> Client:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=session)
        if not sp:
            await find_new_link(session)
        client = Client(f"{session.id}", session_string=session.string, api_id=session.app_id, api_hash=session.app_id,
                        proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id))
        return client


session_actions = SessionActions()
