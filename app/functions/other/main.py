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

from core.constants import ASSISTANT_SLEEP_SEC, ASSISTANT_OFTEN_SLEEP_SEC, ASSISTANT_RARELY_SLEEP_SEC
from functions.other.checker import CheckerAction
from functions.other.executor import AssistantExecutorAction
from functions.other.innovation import InnovationAction
from utils.decorators import func_logger


class AssistantAction:
    def __init__(self):
        self.executor = AssistantExecutorAction()
        self.checker = CheckerAction(self.executor)
        self.innovation = InnovationAction()
        self.prefix = "Assistant"

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    # often
    @func_logger
    async def often(self):
        while True:
            all_tasks_names = [task.get_name() for task in asyncio.all_tasks()]
            if "assistant_wait_message_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.wait_message_check(), name="assistant_wait_message_check")
            if "assistant_wait_order_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.wait_order_check(), name="assistant_wait_order_check")
            if "assistant_wait_sg_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.wait_session_group_check(), name="assistant_wait_sg_check")
            await asyncio.sleep(ASSISTANT_OFTEN_SLEEP_SEC)

    # rarely
    @func_logger
    async def rarely(self):
        while True:
            all_tasks_names = [task.get_name() for task in asyncio.all_tasks()]
            if "assistant_new_proxy_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.new_proxy_check(), name="assistant_new_proxy_check")
            if "assistant_new_session_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.new_session_check(), name="assistant_new_session_check")
            if "assistant_wait_proxy_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.wait_proxy_check(), name="assistant_wait_proxy_check")
            if "assistant_wait_session_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.wait_session_check(), name="assistant_wait_session_check")
            if "assistant_sb_session_check" not in all_tasks_names:
                asyncio.create_task(coro=self.checker.spam_block_session_check(), name="assistant_sb_session_check")
            await asyncio.sleep(ASSISTANT_RARELY_SLEEP_SEC)

    @func_logger
    async def start(self):
        while True:
            all_tasks_names = [task.get_name() for task in asyncio.all_tasks()]
            if "assistant_often" not in all_tasks_names:
                asyncio.create_task(coro=self.often(), name="assistant_often")
            if "assistant_rarely" not in all_tasks_names:
                asyncio.create_task(coro=self.rarely(), name="assistant_rarely")
            await asyncio.sleep(ASSISTANT_SLEEP_SEC)
