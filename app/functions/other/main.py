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

from loguru import logger

from database import repo
from functions.other.checker import CheckerAction
from functions.other.innovation import InnovationAction


class AssistantAction:
    def __init__(self):
        self.checker = CheckerAction()
        self.innovation = InnovationAction()
        self.prefix = "Assistant"

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def start(self):
        self.logger(f"Started!")

        while True:
            self.logger("Start checks")
            # await self.checker.wait_proxy_check()
            # await self.checker.wait_session_check()
            await self.checker.wait_session_group()
            repo.sessions.set_banned(repo.sessions.get_by_id(1))

            # repo.sessions.session_add_new()
            # repo.proxies.add_new_proxy()
            # repo.groups.add_new_group()
            # check_new_proxy()
            # await check_wait_sessions()

            await asyncio.sleep(10)
