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


from datetime import datetime, timedelta

from pyrogram import Client

from database import repo
from database.models import Session, SessionTaskType, SessionTaskStates, OurGroupStates
from functions.bot.executor import BotExecutorAction


class SimulatorAction:
    def __init__(self, client: Client, session: Session, executor: BotExecutorAction):
        self.client = client
        self.session = session
        self.executor = executor
        self.next_data: datetime = datetime.utcnow()

    def run(self):
        date_now = datetime.utcnow()
        if self.next_data > date_now:
            return
        self.session = repo.sessions.get(id=self.session.id)
        our_group = repo.ours_groups.get_by(state=OurGroupStates.active)
        session_our_group = repo.sessions_ours_groups.get_by(session=self.session, our_group=our_group)
        if not session_our_group:
            task = repo.sessions_tasks.get_by(
                session=self.session,
                our_group=our_group,
                type=SessionTaskType.join_group,
                state=SessionTaskStates.enable,
            )
            if task:
                return
            repo.sessions_tasks.create(
                session=self.session,
                our_group=our_group,
                type=SessionTaskType.join_group,
                state=SessionTaskStates.enable,
            )
        sleep = int(repo.settings.get_by(key="simulator_sleep").value)
        self.next_data = date_now + timedelta(seconds=sleep)
