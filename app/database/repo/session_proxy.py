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
from operator import itemgetter
from typing import Optional

from loguru import logger

from database import repo, db_manager
from database.base_repository import BaseRepository
from database.models import SessionProxy, ProxyStates, Proxy, Session


class SessionProxyRepository(BaseRepository):

    @db_manager
    def get_free_proxy(self, country_id: int) -> Optional[Proxy]:
        session_country = repo.countries.get(country_id)
        proxies = []
        for country in repo.countries_links.get_link_country(session_country):
            for proxy in repo.proxies.get_all(state=ProxyStates.enable, country=country):
                sessions = self.get_all(proxy=proxy)
                if len(sessions) < proxy.max_link:
                    proxies.append({'id': proxy.id, 'tasks': len(sessions)})
                    return proxy

        if proxies:
            logger.info(sorted(proxies, key=itemgetter('sessions')))
            return repo.proxies.get(sorted(proxies, key=itemgetter('sessions'))[0]['id'])
        logger.info("Not free proxy")

    @db_manager
    def get_by_session(self, session: Session):
        result = self.model.get_or_none(session=session)
        if not result:
            proxy = repo.sessions_proxies.get_free_proxy(country_id=session.country_id)
            if proxy:
                return self.create(session=session, proxy=proxy)
        return result


sessions_proxies = SessionProxyRepository(SessionProxy)
