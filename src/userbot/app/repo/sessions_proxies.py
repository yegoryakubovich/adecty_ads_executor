from typing import List

import repo
from core.constants import MAX_SESSION2ONE_PROXY
from db.session import SessionLocal
from models import SessionProxy, Proxy, Session

model = SessionProxy


class SessionProxyRepository:
    def __init__(self):
        self.model = model

    @staticmethod
    def get_session():
        return SessionLocal

    def create(self, **kwargs):
        with self.get_session():
            result = self.model.get_or_create(**kwargs)
        return result

    def check_all(self):
        """Удаляем устаревшие"""

    def get_count(self) -> int:
        with self.get_session():
            result = self.model.select().count()
        return result

    def get(self, id: int) -> model:
        with self.get_session():
            result = self.model.get_by_id(id)
        return result

    def get_by_session(self, session: Session):
        with self.get_session():
            result = self.model.get_or_none(session=session)
        return result

    def get_by_proxy(self, proxy: Proxy):
        with self.get_session():
            result = self.model.select().filter(proxy=proxy).execute()
        return result

    def get_all(self) -> List[model]:
        with self.get_session():
            result = self.model.select().execute()
        return result

    def get_free_proxy(self):
        for proxy in repo.proxies.get_all()[::-1]:
            if len(self.get_by_proxy(proxy)) < MAX_SESSION2ONE_PROXY:
                return proxy


sessions_proxies = SessionProxyRepository()
