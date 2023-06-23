from typing import List

from core.constants import MAX_SESSION2ONE_PROXY
from database import db_manager, repo
from database.models import SessionProxy, Proxy, Session

model = SessionProxy


class SessionProxyRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs):
        return self.model.get_or_create(**kwargs)

    @db_manager
    def get_count(self) -> int:
        return self.model.select().count()

    @db_manager
    def get(self, id: int) -> model:
        return self.model.get_by_id(id)

    @db_manager
    def get_by_session(self, session: Session):
        return self.model.get_or_none(session=session)

    @db_manager
    def get_by_proxy(self, proxy: Proxy):
        return self.model.select().filter(proxy=proxy).execute()

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def get_free_proxy(self):
        for proxy in repo.proxies.get_all()[::-1]:
            if len(self.get_by_proxy(proxy)) < MAX_SESSION2ONE_PROXY:
                return proxy


sessions_proxies = SessionProxyRepository()
