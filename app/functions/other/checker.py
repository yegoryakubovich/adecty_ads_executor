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
import asyncio

import requests

from database import repo
from database.models import ProxyStates, ProxyTypes, SessionStates, GroupStates, SessionTask
from database.models.session_task import SessionTaskType, SessionTaskStates
from functions import BotAction


class CheckerAction:
    def __init__(self):
        pass

    @classmethod
    async def wait_proxy_check(cls):
        for proxy in repo.proxies.get_all_by_state(state=ProxyStates.wait):
            proxies = None
            if proxy.type == ProxyTypes.socks5:
                proxies = {
                    'http': f'socks5://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                    'https': f'socks5://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                }
            elif proxy.type == ProxyTypes.http:
                proxies = {
                    'http': f'https://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                    'https': f'https://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                }
            if proxies:
                try:
                    r = requests.get(url="https://ifconfig.me/all.json", proxies=proxies, timeout=5)
                    if r.status_code == 200:
                        repo.proxies.move_state(proxy, ProxyStates.enable)
                        continue
                except:
                    ...
            repo.proxies.move_state(proxy, ProxyStates.disable)

    @classmethod
    async def wait_session_check(cls):
        loop = asyncio.get_event_loop()
        new_functions = []
        for session in repo.sessions.get_all_by_state(state=SessionStates.wait):
            bot = BotAction(session=session)
            await bot.all_connection()
            async with bot.client:
                try:
                    await bot.executor.get_chat(chat_id="durov")
                    repo.sessions.move_state(session=session, state=SessionStates.free)
                    new_functions.append({'fun': BotAction(session=session), 'name': f"Bot_{session.id}"})
                except:
                    repo.sessions.set_banned()
        await asyncio.gather(
            *[loop.create_task(coro=function['fun'].start(), name=function['name']) for function in new_functions]
        )

    @classmethod
    async def wait_session_group(cls):
        for group in repo.groups.get_all_by_state(state=GroupStates.checking_waiting):
            st: SessionTask = repo.sessions_tasks.get_by_group(group=group)
            st = None
            if not st:
                repo.sessions_tasks.create(
                    session=repo.sessions.get_free(),
                    group=group,
                    type=SessionTaskType.check_group,
                    state=SessionTaskStates.enable
                )
