from datetime import datetime
from operator import itemgetter
from typing import List

import httpx

from core.constants import SEND_MSG_DELAY_SEC, URL_FOR_TEST_PROXY
from database import repo
from database.models import Proxy, ProxyStates, Shop, SessionGroup, Group, SessionStates, Message, Sleep, SleepStates
from database.models.session_group import SessionGroupState
from database.models.session_task import SessionTaskStates
from functions.base_executor import BaseExecutorAction
from utils.country import get_by_ip


class AssistantExecutorAction(BaseExecutorAction):

    async def check_proxy(self, proxy: Proxy) -> bool:
        try:
            r = httpx.get(url=URL_FOR_TEST_PROXY, timeout=10,
                          proxies=f'{proxy.type}://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}')
            if r.status_code == 200:
                country_type = get_by_ip(r.json()['ip_addr'])
                country = repo.countries.create(code=country_type.code, name=country_type.name)
                repo.proxies.update(proxy, country=country)
                return True
        except:
            pass
        return False

    async def proxy_disable(self, proxy: Proxy):
        proxy_shop: Shop = repo.shops.get(proxy.shop_id)
        for sp in repo.sessions_proxies.get_all(proxy=proxy):
            repo.sessions_proxies.remove(sp.id)
        repo.proxies.update(proxy, state=ProxyStates.disable)

        await self.proxy_disable_log(proxy_id=proxy.id, proxy_shop_id=proxy_shop.id, proxy_shop_name=proxy_shop.name)

    async def proxy_new(self, proxy: Proxy):
        repo.proxies.update(proxy, state=ProxyStates.enable)
        proxy_shop: Shop = repo.shops.get(proxy.shop_id)
        await self.proxy_added_log(
            proxy_id=proxy.id, proxy_shop_id=proxy_shop.id, proxy_shop_name=proxy_shop.name
        )

    async def get_session_by_group(self, group: Group, send_msg: bool = True):
        maybe_sessions = []
        for session in repo.sessions.get_all(state=SessionStates.free):
            sg: SessionGroup = repo.sessions_groups.get_by(session=session, group=group)
            if sg:
                if sg.state == SessionGroupState.banned:
                    continue
                sleeps: List[Sleep] = repo.sleeps.get_all(session=session, state=SleepStates.enable)
                if not len(sleeps):
                    tasks = repo.sessions_tasks.get_all(session=session, state=SessionTaskStates.enable)
                    maybe_sessions.append({'id': session.id, 'tasks': len(tasks)})
        if maybe_sessions:
            return repo.sessions.get(sorted(maybe_sessions, key=itemgetter('tasks'))[0]['id'])
