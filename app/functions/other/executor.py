from operator import itemgetter
from operator import itemgetter
from typing import List

import httpx
from loguru import logger

from core.constants import URL_FOR_TEST_PROXY, MAX_TASKS_COUNT
from database import repo
from database.models import Proxy, ProxyStates, Shop, SessionGroup, Group, SessionStates, Sleep, SleepStates, \
    SessionTask
from database.models.session_group import SessionGroupState
from database.models.session_task import SessionTaskStates, SessionTaskType
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

    async def proxy_disable(self, proxy: Proxy, log: bool = True):
        proxy_shop: Shop = repo.shops.get(proxy.shop_id)
        for sp in repo.sessions_proxies.get_all(proxy=proxy):
            repo.sessions_proxies.remove(sp.id)
        repo.proxies.update(proxy, state=ProxyStates.disable)
        if log:
            await self.proxy_disable_log(
                proxy_id=proxy.id, proxy_shop_id=proxy_shop.id, proxy_shop_name=proxy_shop.name
            )

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
                if len(sleeps):
                    continue
                tasks = []
                for task in repo.sessions_tasks.get_all(session=session, state=SessionTaskStates.enable):
                    if not task.type == SessionTaskType.check_message:
                        tasks.append(task)
                if len(tasks) >= MAX_TASKS_COUNT:
                    continue
                maybe_sessions.append({'id': session.id, 'tasks': len(tasks)})

        if maybe_sessions:
            logger.info(sorted(maybe_sessions, key=itemgetter('tasks')))
            return repo.sessions.get(sorted(maybe_sessions, key=itemgetter('tasks'))[0]['id'])
