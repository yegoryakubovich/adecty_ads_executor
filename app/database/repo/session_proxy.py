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

from typing import List

from loguru import logger
from peewee import ModelObjectCursorWrapper

from core.constants import MAX_SESSION2ONE_PROXY
from database import db_manager, repo
from database.models import SessionProxy, Proxy, Session, ProxyStates

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
    def get_by_id(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def get_free_proxy(self):
        proxies: ModelObjectCursorWrapper = repo.proxies.get_all_by_state(state=ProxyStates.enable)
        for proxy in proxies:
            if len(self.get_by_proxy(proxy)) < MAX_SESSION2ONE_PROXY:
                return proxy
        logger.info("Not free proxy")

    @db_manager
    def get_by_session(self, session: Session):
        result = self.model.get_or_none(session=session)
        if not result:
            proxy = repo.sessions_proxies.get_free_proxy()
            if proxy:
                return self.create(session=session, proxy=proxy)[0]
        return result

    @db_manager
    def get_by_proxy(self, proxy: Proxy):
        return self.model.select().filter(proxy=proxy).execute()

    @db_manager
    def delete_by_session(self, session: Session):
        self.model.delete().where(self.model.session == session).execute()


sessions_proxies = SessionProxyRepository()
