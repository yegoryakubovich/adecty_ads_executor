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

from core.constants import ASSISTANT_SLEEP_SEC, ASSISTANT_OFTEN_SLEEP_SEC, ASSISTANT_RARELY_SLEEP_SEC, min2sec
from database import repo
from database.models import GroupStates, MessageStates
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
            if "assistant_wait_mailing_order_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_mailing_order_check(), name="assistant_wait_mailing_order_check"
                )
            if "assistant_wait_sg_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_session_group_check(), name="assistant_wait_sg_check"
                )
            if "assistant_all_task_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.all_task_check(), name="assistant_all_task_check"
                )
            if "assistant_wait_message_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_message_check(), name="assistant_wait_message_check"
                )
            if "assistant_wait_ads_order_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_ads_order_check(), name="assistant_wait_ads_order_check"
                )
            if "assistant_personals_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.personals_check(), name="assistant_personals_check"
                )
            await asyncio.sleep(ASSISTANT_OFTEN_SLEEP_SEC)

    # rarely
    @func_logger
    async def rarely(self):
        while True:
            all_tasks_names = [task.get_name() for task in asyncio.all_tasks()]
            if "assistant_new_proxy_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.new_proxy_check(), name="assistant_new_proxy_check"
                )
            if "assistant_wait_proxy_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_proxy_check(), name="assistant_wait_proxy_check"
                )
            if "assistant_new_session_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.new_session_check(), name="assistant_new_session_check"
                )
            if "assistant_wait_session_check" not in all_tasks_names:
                asyncio.create_task(
                    coro=self.checker.wait_session_check(), name="assistant_wait_session_check"
                )
            # if "assistant_sb_session_check" not in all_tasks_names:
            #     asyncio.create_task(
            #         coro=self.checker.spam_block_session_check(), name="assistant_sb_session_check"
            #     )
            await asyncio.sleep(ASSISTANT_RARELY_SLEEP_SEC)

    # group_presence
    @func_logger
    async def group_presence(self):
        while True:
            self.logger("group_presence")
            text = []
            presence_count, all_count = 0, 0
            for group in repo.groups.get_all(state=GroupStates.active):
                messages_waiting = repo.messages.get_last(group=group, state=MessageStates.waiting)
                if messages_waiting:
                    link = await self.executor.create_link(group_name=group.name, post_id=messages_waiting.message_id)
                    text.append(f"🟢 {link}")
                    presence_count += 1
                else:
                    text.append(f"🔴 @{group.name}")
                all_count += 1
            await self.executor.change_log_message(
                text='\n'.join(text), presence_count=presence_count, all_count=all_count
            )
            await asyncio.sleep(min2sec(5))

    @func_logger
    async def start(self):
        while True:
            all_tasks_names = [task.get_name() for task in asyncio.all_tasks()]
            if "assistant_often" not in all_tasks_names:
                asyncio.create_task(coro=self.often(), name="assistant_often")
            if "assistant_rarely" not in all_tasks_names:
                asyncio.create_task(coro=self.rarely(), name="assistant_rarely")
            if "assistant_group_presence" not in all_tasks_names:
                asyncio.create_task(coro=self.group_presence(), name="assistant_group_presence")
            await asyncio.sleep(ASSISTANT_SLEEP_SEC)
